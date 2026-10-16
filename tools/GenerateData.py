"""Tạo phiếu mô phỏng và các tài liệu dẫn xuất từ ngân hàng câu hỏi."""
from __future__ import annotations

import csv
import io
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "fake_data"


def load_inputs() -> tuple[dict, dict]:
    return (json.loads((DATA / "Survey.json").read_text()),
            json.loads((DATA / "SimulationConfig.json").read_text()))


def visible(question: dict, role: str) -> bool:
    audience: str = question["audience"]
    return (audience == "all" or audience == "active" and role != "Chưa có nhu cầu"
            or audience == "buyer" and role in ("Chỉ mua hoặc nhận pass phòng", "Cả hai")
            or audience == "seller" and role in ("Chỉ bán hoặc pass phòng đang thuê", "Cả hai"))


def generate(survey: dict, config: dict) -> list[dict]:
    rng = random.Random(config["seed"])
    multiple: dict = config["multiple_selection"]
    selection_rng = random.Random(multiple["seed"])
    questions: dict[str, dict] = {q["id"]: q for q in survey["questions"]}
    roles: list[str] = [role for role, count in config["role_counts"].items()
                        for _ in range(count)]
    rng.shuffle(roles)
    rows: list[dict] = []
    for index, role in enumerate(roles, 1):
        row: dict = {"response_id": f"SC-SIM-{index:03d}", "data_origin": "synthetic"}
        for q in survey["questions"]:
            qid: str = q["id"]
            if not visible(q, role):
                row[qid], row[qid + "_status"] = "", "not_shown"
                continue
            if qid == "Q14":
                value: str = ""
            else:
                value = rng.choice(q["options"])
                if q.get("selection") == "multiple":
                    count: int = selection_rng.choices(multiple["counts"], multiple["weights"])[0]
                    others: list[str] = [option for option in q["options"] if option != value]
                    selected: list[str] = [value] + selection_rng.sample(others, count - 1)
                    value = json.dumps([option for option in q["options"] if option in selected], ensure_ascii=False)
            row[qid], row[qid + "_status"] = value, "answered"
        row["Q03"] = role
        row["Q01"] = rng.choices(questions["Q01"]["options"], [3, 4, 4, 1])[0]
        if role == "Chưa có nhu cầu":
            row["Q13"] = rng.choice(["Chỉ xem và tìm hiểu", "Chưa định dùng"])
        elif row["Q04"] == "Trong 1 tháng":
            row["Q13"] = rng.choices(questions["Q13"]["options"], [6, 3, 1])[0]
        if row["Q06"] == "Lo mất tiền cọc":
            row["Q07"] = rng.choices(questions["Q07"]["options"], [3, 2, 1, 6])[0]
        if row["Q10"] == "Không muốn thực hiện":
            row["Q13"] = rng.choice(["Chỉ xem và tìm hiểu", "Chưa định dùng"])
        if row["Q09"] == "Trong 7 ngày" and row["Q10"] == "Sẵn sàng thực hiện":
            row["Q13"] = rng.choices(questions["Q13"]["options"], [7, 2, 1])[0]
        # Câu mở bám rào cản của phiếu; không thêm tên hoặc giấy tờ giả.
        comments: dict[str, list[str]] = {
            "Lo mất tiền cọc": ["Muốn biết khi nào được hoàn cọc.", "Đừng bắt chuyển cọc cho người lạ."],
            "Lo hàng hoặc phòng khác mô tả": ["Ảnh thật với ghi rõ lỗi giúp mình dễ chọn hơn.", "Cần xem đúng tình trạng trước khi quyết định."],
            "Thiếu tin phù hợp gần mình": ["Muốn lọc tin gần trường để đi xem.", "Tìm mãi chưa có món phù hợp ở gần."],
            "Khó sắp xếp kiểm tra trực tiếp": ["Có lịch hẹn xem thì đỡ nhắn qua lại.", "Mình cần thống nhất giờ xem trước."],
        }
        if rng.random() < 0.36:
            row["Q14_status"] = "skipped_optional"
        else:
            choices: list[str] = comments.get(row["Q06"], [
                "Ghi rõ quy trình và phí trước nhé.", "Có hướng dẫn cho người mới thì tốt.",
                "Chưa có góp ý thêm.", "Muốn xem thử vài tin trước đã."])
            if row["Q10"] == "Cần hướng dẫn chuẩn bị giấy tờ":
                choices = ["Cần danh sách giấy tờ cần chuẩn bị.", "Hướng dẫn đăng tin từng bước nhé."]
            row["Q14"] = rng.choice(choices)
        rows.append(row)
    return rows


def render_form(survey: dict) -> str:
    labels: dict[str, str] = {"all": "Mọi người", "active": "Có nhu cầu ở Q03",
                              "buyer": "Có nhu cầu mua/nhận pass ở Q03",
                              "seller": "Có nhu cầu bán/pass ở Q03"}
    lines: list[str] = ["# " + survey["title"], "",
        "Summary: 15 câu khảo sát mô phỏng, nhánh trả lời và lý do gắn với quyết định kinh doanh.", "",
        survey["introduction"], "", "## Cách đọc", "",
        "Nguồn duy nhất của câu hỏi và lựa chọn là [Survey.json](fake_data/Survey.json); tài liệu này được sinh tự động.",
        "Q03 quyết định nhánh: chỉ mua trả lời Q05–Q07; chỉ bán trả lời Q08–Q10; cả hai trả lời cả hai nhóm.",
        "Người chưa có nhu cầu bỏ Q04–Q10. Mọi người trả lời Q01–Q03 và Q11–Q15; chỉ Q14 tự nguyện.",
        "Vì vậy mỗi người thấy 8, 12 hoặc 15 câu. Q05 và Q08 chọn nhiều đáp án (ít nhất một); các câu lựa chọn còn lại chọn đúng một đáp án.",
        "Các mục Why dưới đây là suy luận thiết kế: nêu dữ liệu cần kết hợp, quyết định được hỗ trợ và giới hạn.", ""]
    for q in survey["questions"]:
        lines.extend([f"## {q['id']}. {q['text']}", "",
                      f"**Hiển thị:** {labels[q['audience']]}. **Bắt buộc:** {'Không' if q.get('optional') else 'Có'}.", ""])
        if "options" in q:
            label: str = "**Lựa chọn (chọn nhiều, ít nhất một):** " if q.get("selection") == "multiple" else "**Lựa chọn:** "
            lines.append(label + "; ".join(q["options"]) + ".")
        else:
            lines.append("**Trả lời:** Văn bản tự do.")
        lines.extend(["", "**Why — quyết định kinh doanh:** " + q["why"], ""])
    return "\n".join(lines)


def artifacts(survey: dict, config: dict) -> dict[Path, str]:
    rows: list[dict] = generate(survey, config)
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return {DATA / "Responses.csv": buffer.getvalue(), ROOT / "Form.md": render_form(survey)}


if __name__ == "__main__":
    for path, content in artifacts(*load_inputs()).items():
        path.write_text(content, encoding="utf-8", newline="")
        print(f"Đã tạo {path.relative_to(ROOT)}")
