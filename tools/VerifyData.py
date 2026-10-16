"""Kiểm tra workflow tạo phiếu, tệp lưu và báo cáo dẫn xuất."""
from __future__ import annotations

import argparse
import copy
import csv
import io
import json
from collections import Counter
from pathlib import Path

from AnalyzeData import analyze
from GenerateData import DATA, ROOT, artifacts, load_inputs, visible


def validate(rows: list[dict], survey: dict, config: dict) -> None:
    questions: list[dict] = survey["questions"]
    assert 10 <= len(questions) <= 15, "Số câu ngoài phạm vi đã duyệt"
    assert [q["id"] for q in questions] == [f"Q{i:02d}" for i in range(1, len(questions) + 1)]
    assert len(rows) == sum(config["role_counts"].values()) == 50, "Phải có 50 phiếu"
    assert len({r["response_id"] for r in rows}) == len(rows), "Trùng mã phiếu"
    assert Counter(r["Q03"] for r in rows) == Counter(config["role_counts"]), "Sai cơ cấu kịch bản"
    expected_fields = {"response_id", "data_origin"} | {key for q in questions
                       for key in (q["id"], q["id"] + "_status")}
    open_rows: list[dict] = [r for r in rows if r["Q14_status"] == "answered"]
    assert 15 <= len(open_rows) <= 20, "Q14 phải có 15–20 phiếu trả lời"
    normalized: list[str] = [" ".join(r["Q14"].split()).casefold() for r in open_rows]
    assert len(set(normalized)) == len(normalized), "Q14 có câu trả lời trùng nhau"
    assert {r["response_id"]: r["Q14"] for r in open_rows} == config["open_responses"], "Q14 không khớp bản viết tay"
    for row in rows:
        assert set(row) == expected_fields, "Sai cột dữ liệu"
        assert row["data_origin"] == "synthetic", "Thiếu nhãn mô phỏng"
        for q in questions:
            qid: str = q["id"]
            status: str = row[qid + "_status"]
            value: str = row[qid]
            if not visible(q, row["Q03"]):
                assert status == "not_shown" and value == "", f"{row['response_id']}: sai nhánh {qid}"
            elif q.get("optional") and not value:
                assert status == "skipped_optional", "Sai trạng thái câu tự nguyện"
            else:
                assert status == "answered" and value.strip(), f"Thiếu câu bắt buộc {qid}"
                if "options" in q:
                    if q.get("selection") == "multiple":
                        try:
                            selected = json.loads(value)
                        except json.JSONDecodeError as error:
                            raise AssertionError(f"Sai định dạng JSON {qid}: {value}") from error
                        assert isinstance(selected, list) and selected, f"Phải chọn ít nhất một đáp án {qid}"
                        assert all(isinstance(item, str) and item in q["options"] for item in selected), f"Đáp án ngoài ngân hàng {qid}"
                        assert len(selected) == len(set(selected)), f"Trùng đáp án {qid}"
                    else:
                        assert value in q["options"], f"Đáp án ngoài ngân hàng {qid}"
        if row["Q03"] == "Chưa có nhu cầu":
            assert row["Q13"] != "Thử dùng cho nhu cầu hiện có", "Ý định không khớp nhu cầu"
        if row["Q10"] == "Không muốn thực hiện":
            assert row["Q13"] != "Thử dùng cho nhu cầu hiện có", "Kịch bản từ chối xác minh chưa nhất quán"


def rejection_checks(rows: list[dict], survey: dict, config: dict) -> int:
    # Thử phá dữ liệu đầu ra của bộ sinh thật, không chép thuật toán sinh vào test.
    cases: list[tuple[str, str, str]] = [
        ("nhãn mô phỏng", "data_origin", "real"),
        ("đáp án ngoài lựa chọn", "Q01", "Đáp án không tồn tại"),
        ("câu bắt buộc", "Q01", ""),
    ]
    tested: int = 0
    for name, key, value in cases:
        broken = copy.deepcopy(rows)
        broken[0][key] = value
        try:
            validate(broken, survey, config)
        except AssertionError as error:
            print(f"Đã chặn {name}: {error}")
        else:
            raise AssertionError(f"Không chặn được {name}")
        tested += 1
    broken = copy.deepcopy(rows)
    inactive = next(r for r in broken if r["Q03"] == "Chưa có nhu cầu")
    inactive["Q05"], inactive["Q05_status"] = "Laptop", "answered"
    try:
        validate(broken, survey, config)
    except AssertionError as error:
        print(f"Đã chặn đi sai nhánh: {error}")
    else:
        raise AssertionError("Không chặn được đi sai nhánh")
    tested += 1
    for qid in ("Q05", "Q08"):
        for value in ('[]', '["Không tồn tại"]', '["Laptop", "Laptop"]', '"Laptop"', '[1]', 'Laptop'):
            broken = copy.deepcopy(rows)
            active = next(r for r in broken if r[qid + "_status"] == "answered")
            active[qid] = value
            try:
                validate(broken, survey, config)
            except AssertionError as error:
                print(f"Đã chặn {qid}={value}: {error}")
            else:
                raise AssertionError(f"Không chặn được {qid}={value}")
            tested += 1
    for case in ("trùng tự luận", "thiếu tự luận", "thừa tự luận"):
        broken = copy.deepcopy(rows)
        answered: list[dict] = [r for r in broken if r["Q14_status"] == "answered"]
        if case == "trùng tự luận":
            answered[1]["Q14"] = answered[0]["Q14"]
        elif case == "thiếu tự luận":
            for row in answered[14:]:
                row["Q14"], row["Q14_status"] = "", "skipped_optional"
        else:
            skipped: list[dict] = [r for r in broken if r["Q14_status"] == "skipped_optional"]
            for index, row in enumerate(skipped[:21 - len(answered)]):
                row["Q14"], row["Q14_status"] = f"Tự luận kiểm tra {index}", "answered"
        try:
            validate(broken, survey, config)
        except AssertionError as error:
            print(f"Đã chặn {case}: {error}")
        else:
            raise AssertionError(f"Không chặn được {case}")
        tested += 1
    return tested


def analysis_checks(rows: list[dict]) -> None:
    # Chạy báo cáo thật với các lựa chọn chồng lấp và khác nhau giữa hai phía.
    fixtures: list[dict] = [copy.deepcopy(next(r for r in rows if r["Q03"] == "Cả hai")) for _ in range(2)]
    for row in fixtures:
        row["Q01"], row["Q02"] = "Sinh viên năm 1", "Cầu Giấy – Xuân Thủy"
        row["Q07"] = "Sẵn sàng trả 20.000 đồng"
    fixtures[0]["Q05"] = '["Laptop", "Điện thoại"]'
    fixtures[0]["Q08"] = '["Điện thoại", "Pass phòng đang thuê"]'
    fixtures[1]["Q05"] = '["Laptop"]'
    fixtures[1]["Q08"] = '["Pass phòng đang thuê"]'
    report: str = analyze(fixtures)
    for expected in (
        "| Cầu Giấy – Xuân Thủy | Laptop | 2 | 0 | 2 |",
        "| Cầu Giấy – Xuân Thủy | Điện thoại | 1 | 1 | 0 |",
        "| Cầu Giấy – Xuân Thủy | Nhận pass phòng trọ | 0 | 2 | -2 |",
        "| Laptop | 2 | 2 | 0 |", "| Điện thoại | 1 | 1 | 0 |",
        "2 người mua, 2 người bán, trong đó 2 người có cả hai vai trò",
    ):
        assert expected in report, f"Báo cáo đếm sai lựa chọn chồng lấp: {expected}"
    print("ĐẠT: báo cáo đếm từng danh mục, ánh xạ pass phòng, nhóm phí và tổng người không trùng.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Tạo lại toàn bộ đầu ra trước khi kiểm tra")
    args = parser.parse_args()
    survey, config = load_inputs()
    expected: dict[Path, str] = artifacts(survey, config)
    rows: list[dict] = list(csv.DictReader(io.StringIO(expected[DATA / "Responses.csv"])))
    validate(rows, survey, config)
    rejected: int = rejection_checks(rows, survey, config)
    for qid in ("Q05", "Q08"):
        selections: list[list[str]] = [json.loads(r[qid]) for r in rows if r[qid + "_status"] == "answered"]
        assert any(len(items) == 1 for items in selections), f"Chưa kiểm tra chọn một ở {qid}"
        assert any(len(items) > 1 for items in selections), f"Chưa kiểm tra chọn nhiều ở {qid}"
    analysis_checks(rows)
    expected[ROOT / "Analysis.md"] = analyze(rows)
    result: dict = {
        "data_origin": "synthetic", "responses_checked": len(rows),
        "questions_checked": len(survey["questions"]), "negative_cases_passed": rejected,
        "checks": ["cột và mã phiếu", "nhãn mô phỏng", "đáp án hợp lệ", "nhánh hiển thị",
                   "câu bắt buộc và tự nguyện", "cơ cấu kịch bản", "chọn nhiều không rỗng và không trùng",
                   "báo cáo danh mục chồng lấp và tổng người", "15–20 tự luận viết riêng không trùng",
                   "tái tạo đầu ra và báo cáo"],
        "result": "passed",
        "limits": "Không kiểm chứng nhu cầu thật, tính tự nhiên của ngôn ngữ hoặc hiệu quả kinh doanh."
    }
    expected[DATA / "Validation.json"] = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.write:
        for path, content in expected.items():
            path.write_text(content, encoding="utf-8", newline="")
            print(f"Đã lưu {path.relative_to(ROOT)}")
    for path, content in expected.items():
        assert path.read_bytes() == content.encode("utf-8"), f"Tệp không khớp nguồn: {path}"
    saved: list[dict] = list(csv.DictReader((DATA / "Responses.csv").open(encoding="utf-8", newline="")))
    validate(saved, survey, config)
    assert saved == rows, "CSV lưu không khớp dữ liệu được tạo"
    print(f"ĐẠT: {len(saved)} phiếu, {len(survey['questions'])} câu, {rejected} ca dữ liệu lỗi bị chặn; đầu ra tái tạo khớp.")


if __name__ == "__main__":
    main()
