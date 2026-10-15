"""Phân tích phiếu mô phỏng, không ước lượng thị trường thật."""
from __future__ import annotations

from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def table(headers: list[str], rows: list[list]) -> list[str]:
    return ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"] + [
        "| " + " | ".join(map(str, row)) + " |" for row in rows]


def analyze(rows: list[dict]) -> str:
    target: list[dict] = [r for r in rows if r["Q01"] != "Không phải sinh viên" and r["Q02"] != "Ngoài Hà Nội"]
    buyers: list[dict] = [r for r in target if r["Q05_status"] == "answered"]
    sellers: list[dict] = [r for r in target if r["Q08_status"] == "answered"]
    both: int = sum(r["Q03"] == "Cả hai" for r in target)
    lines: list[str] = ["# Phân tích kịch bản Second Chance", "",
        "Summary: Đối chiếu hai phía thị trường và lựa chọn thử nghiệm kinh doanh từ 50 phiếu giả lập, kèm mẫu số và giới hạn.", "",
        "## Phạm vi và mức bằng chứng", "",
        "**Đây là dữ liệu mô phỏng, không có người thật tham gia.** Các số đếm là [Observed] từ bộ dữ liệu do chương trình tạo, không phải bằng chứng về thị trường.",
        "Các hành động đề xuất là [Inferred] theo kịch bản: tiền đề gồm các số đếm dưới đây và phạm vi khách hàng trong [Marketing](docs/Marketing.md#khách-hàng-mục-tiêu).",
        "Ngân hàng câu hỏi ở [Form](Form.md); giả định, quan hệ có điều kiện và cách kiểm tra ở [Methodology](Methodology.md).", "",
        f"Tổng mẫu: {len(rows)} người. Nhóm phân tích mục tiêu: {len(target)} sinh viên có khu vực tại Hà Nội; ngoài nhóm: {len(rows) - len(target)} người.",
        f"Trong nhóm mục tiêu: {len(buyers)} người mua, {len(sellers)} người bán, trong đó {both} người có cả hai vai trò. Không cộng hai phía để tính tổng người.", "",
        "## 1. Cơ cấu mẫu được đặt trước", ""]
    counts = Counter(r["Q03"] for r in rows)
    lines += table(["Vai trò", "Số phiếu / 50"], [[role, count] for role, count in counts.items()])
    lines += ["", "Cơ cấu này do cấu hình quy định, không phải phát hiện về tỷ lệ người có nhu cầu.", "",
              "## 2. Danh mục × cụm địa lý: chọn nơi bổ sung nguồn cung", "",
              "Đếm số người chọn một danh mục ưu tiên. Chênh lệch = người mua − người bán; không phải số món hàng thiếu.", ""]
    cells: list[list] = []
    mapping: dict[str, str] = {"Nhận pass phòng trọ": "Pass phòng đang thuê"}
    for area in sorted({r["Q02"] for r in target}):
        for category in ("Laptop", "Điện thoại", "Xe máy", "Nhận pass phòng trọ", "Đồ khác"):
            buy: int = sum(r["Q02"] == area and r["Q05"] == category for r in buyers)
            sell: int = sum(r["Q02"] == area and r["Q08"] == mapping.get(category, category) for r in sellers)
            if buy or sell:
                cells.append([area, category, buy, sell, buy - sell])
    lines += table(["Cụm", "Danh mục", "Mua", "Bán", "Chênh lệch"], cells)
    if cells:
        gap = max(cells, key=lambda c: c[4])
        if gap[4] > 0:
            lines += ["", f"**Quyết định minh họa:** ô {gap[0]} / {gap[1]} có {gap[2]} người mua và {gap[3]} người bán, chênh {gap[4]}. Vì vậy, thử tuyển thêm người bán phù hợp tại ô này trước khi kéo thêm người mua; không nhập kho."]
        else:
            lines += ["", "**Quyết định minh họa:** không có ô thiếu phía bán theo số người; kiểm tra chất lượng tin và nhu cầu cụ thể trước khi chi ngân sách bổ sung nguồn cung."]
    lines += ["", "**Giới hạn:** số người từng phía của mỗi ô được ghi trong bảng; không có model máy, giá, tình trạng, thời điểm riêng cho mỗi phía hoặc sự đồng ý của chủ trọ. Vì vậy chưa biết cung và cầu có khớp để giao dịch hay không. Không dùng bảng để chọn cụm triển khai thật.", "",
              "## 3. Người bán để mời thử nghiệm", ""]
    ready: list[dict] = [r for r in sellers if r["Q04"] == "Trong 1 tháng" and
                        r["Q10"] == "Sẵn sàng thực hiện" and r["Q13"] == "Thử dùng cho nhu cầu hiện có"]
    lines += [f"Có {len(ready)}/{len(sellers)} người bán mục tiêu đồng thời có nhu cầu gần, sẵn sàng xác minh và định thử dùng.", ""]
    channels = Counter(r["Q11"] for r in ready)
    if ready:
        lines += table(["Kênh của nhóm đủ ba điều kiện", "Số người"], [[k, v] for k, v in channels.most_common()])
        lines += ["", "**Quyết định minh họa:** ưu tiên mời thử nhóm đủ ba điều kiện trên và dùng kênh họ chọn để tuyển mẫu thử."]
    else:
        lines += ["**Quyết định minh họa:** chưa có ai đủ ba điều kiện trong kịch bản này. Vì vậy, phỏng vấn về thời điểm, xác minh và ý định trước khi chạy quảng cáo; chưa có cơ sở chọn kênh từ nhóm này."]
    lines += ["**Cần kiểm chứng:** đo số người thực sự xác minh và đăng tin theo từng đường dẫn; chưa có dữ liệu chi phí để phân bổ lại ngân sách 5 triệu đồng.", "",
              "## 4. Trở ngại người mua và thông điệp thử nghiệm", ""]
    barriers = Counter(r["Q06"] for r in buyers)
    lines += table(["Trở ngại đứng đầu", f"Số người / {len(buyers)} người mua mục tiêu"], [[k, v] for k, v in barriers.most_common()])
    pairs = Counter((r["Q06"], r["Q12"]) for r in buyers if r["Q13"] == "Thử dùng cho nhu cầu hiện có")
    lines += ["", "Đối chiếu thêm trong nhóm định thử dùng:", ""]
    lines += table(["Trở ngại", "Điểm muốn đổi kênh", "Số người"], [[a, b, n] for (a, b), n in pairs.most_common()])
    lines += ["", "**Quyết định minh họa:** thử thông điệp gần trường cho nhóm thiếu tin, bằng chứng tình trạng cho nhóm lo sai mô tả, hoặc điều kiện hoàn tiền cho nhóm lo cọc. Nếu Q06 và Q12 không cùng hướng, phỏng vấn lý do thay vì tự sửa phiếu.",
              "**Giới hạn:** chưa đo thông điệp nào tạo đăng ký hoặc giao dịch; không gọi đây là kết quả thử nghiệm marketing.", "",
              "## 5. Phí thử nghiệm: chọn nhóm kiểm tra khả năng thu tiền", ""]
    fee_cells: list[list] = []
    for category in sorted({r["Q05"] for r in buyers}):
        group: list[dict] = [r for r in buyers if r["Q05"] == category]
        pay: int = sum(r["Q07"] == "Sẵn sàng trả 20.000 đồng" for r in group)
        conditional: int = sum(r["Q07"] == "Cần biết thêm điều kiện hoàn tiền" for r in group)
        fee_cells.append([category, len(group), pay, conditional])
    lines += table(["Danh mục", "Người mua", "Chấp nhận 20.000 đ", "Cần điều kiện hoàn tiền"], fee_cells)
    lines += ["", "**Quyết định minh họa:** mời nhóm chấp nhận phí thử quy trình và mức giá; giải thích điều kiện cho nhóm còn hỏi về hoàn tiền trước khi đo lại. Không cộng nhóm còn cần thông tin vào nhóm chấp nhận trả tiền.",
              "**Giới hạn:** chưa có thanh toán thật hoặc báo giá đối tác. Vì vậy không tính doanh thu dự báo, lợi nhuận hay giá tối ưu. Không sửa chính sách phí chưa chốt trong [TrustAndSafety](docs/TrustAndSafety.md#hai-chế-độ-giao-dịch).", "",
              "## 6. Câu mở và kinh nghiệm giao dịch", ""]
    comments = Counter(r["Q14"] for r in target if r["Q14_status"] == "answered")
    lines += table(["Nội dung giả lập", "Số lần"], [[k, v] for k, v in comments.most_common()])
    lines += ["", "Câu mở lấy từ ngân hàng câu ngắn có điều kiện, không phải lời nói của người được phỏng vấn. Không trích dẫn như bằng chứng khách hàng.", ""]
    experience = Counter(r["Q15"] for r in target)
    lines += table(["Kinh nghiệm 12 tháng qua", f"Số người / {len(target)}"], [[k, v] for k, v in experience.items()])
    lines += ["", "**Quyết định minh họa:** tách người chưa giao dịch để thử hướng dẫn nhập môn; phỏng vấn người có kinh nghiệm về trở ngại họ vẫn gặp. Không nhận diện VIP hay tăng trọng số từ số lần giao dịch.", "",
              "## Điều kiện để dùng cho kinh doanh thật", "",
              "Thu mẫu thật có cách tuyển người rõ ràng; kiểm tra tin đăng và giao dịch thật; đo chi phí thu hút theo kênh và phí đối tác. Phân tích mẫu thật riêng, không trộn với 50 phiếu này.", ""]
    return "\n".join(lines)
