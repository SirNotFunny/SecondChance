# Quản lý giao dịch và chống lừa đảo

Summary: Làm sao để giao dịch trên Second Chance diễn ra đúng thỏa thuận và không bị lừa đảo? Tài liệu gồm nghĩa vụ pháp lý, hai chế độ giao dịch, quy trình thanh toán đảm bảo (cả cọc phòng trọ), xác minh người dùng, kiểm duyệt tin đăng, đánh giá và xử lý tranh chấp.
Why: đồ cũ giá trị cao (laptop, điện thoại, xe máy) và tiền cọc phòng trọ là nơi sinh viên dễ bị lừa nhất. Nếu người dùng không tin nền tảng thì marketing cũng vô ích.

Khách hàng mục tiêu và danh mục hàng hóa được định nghĩa trong [Marketing](Marketing.md#khách-hàng-mục-tiêu).

## Nghĩa vụ pháp lý

Second Chance là **nền tảng thương mại điện tử trung gian** theo Luật Thương mại điện tử số 122/2025/QH15, có hiệu lực từ 01/07/2026 ([văn bản](https://luatvietnam.vn/thuong-mai/luat-thuong-mai-dien-tu-2025-so-122-2025-qh15-423356-d1.html)). Các nghĩa vụ ảnh hưởng trực tiếp đến thiết kế:

| Nghĩa vụ | Căn cứ | Cách Second Chance đáp ứng |
|---|---|---|
| Xác thực điện tử danh tính người bán **trước khi** cho phép bán | Điều 17 khoản 1 điểm c; với cá nhân trong nước: họ tên, ngày sinh, số định danh cá nhân (Nghị định 248/2026/NĐ-CP) | Bắt buộc eKYC bằng CCCD gắn chip trước khi đăng tin đầu tiên |
| Kiểm duyệt nội dung tin đăng **trước khi** hiển thị, để chặn hàng không rõ nguồn gốc | Điều 17 khoản 1 điểm đ | Xem [Kiểm duyệt tin đăng](#kiểm-duyệt-tin-đăng) |
| Lưu dữ liệu tin đăng ít nhất 01 năm | Điều 17 khoản 1 điểm e | Tin bị xóa chỉ bị ẩn, không bị xóa khỏi cơ sở dữ liệu |
| Nếu nền tảng có chức năng đặt hàng trực tuyến: tiếp nhận lại hàng không đúng mô tả | Điều 17 khoản 2 điểm b | Chế độ thanh toán đảm bảo có quy trình trả hàng, xem [Xử lý tranh chấp](#xử-lý-tranh-chấp) |

Second Chance **không tự giữ tiền** của người dùng. Tự giữ tiền là cung ứng dịch vụ trung gian thanh toán, cần giấy phép của Ngân hàng Nhà nước và vốn điều lệ tối thiểu 50 tỷ đồng (Nghị định 52/2024/NĐ-CP, Điều 22 khoản 2 điểm b, [văn bản](https://congluatviet.vn/van-ban/nghi-dinh-quy-dinh-ve-thanh-toan-khong-dung-tien-mat-52-2024-nd-cp)). Vì vậy, tiền đảm bảo được giữ bởi một đối tác đã có giấy phép, ví dụ một ví điện tử hoặc cổng thanh toán.

## Hai chế độ giao dịch

| | Giao dịch trực tiếp (mặc định) | Thanh toán đảm bảo (tùy chọn) |
|---|---|---|
| Ai giữ tiền | Người mua trả thẳng cho người bán | Đối tác thanh toán có giấy phép giữ đến khi người mua xác nhận |
| Phù hợp với | Gặp mặt tại trường, hàng giá thấp, xe máy | Giao hàng qua đơn vị vận chuyển, laptop và điện thoại giá cao, tiền cọc giữ phòng trọ |
| Phí | Miễn phí | Người mua trả phí; mức phí chốt sau khi có báo giá của đối tác |
| Nền tảng bảo vệ | Cảnh báo lừa đảo, đánh giá, báo cáo, khóa tài khoản | Tất cả bên trái + hoàn tiền khi không nhận được hàng hoặc hàng sai mô tả |

Chợ Tốt từng ra mắt tính năng tương tự ("Thanh toán đảm bảo", 2022, qua MoMo và Payoo) ([nguồn](https://www.chotot.com/kinh-nghiem/cach-mua-hang-va-thanh-toan-online-tren-cho-tot.html)) rồi ngừng từ 20/11/2024 ([thông báo](https://trogiup.chotot.com/thong-bao-ngung-cung-cap-tinh-nang-thanh-toan-dam-bao-tren-cho-tot/)). Chợ Tốt không công bố lý do ngừng. Do đó Second Chance giữ giao dịch trực tiếp làm mặc định, và chỉ vận hành thanh toán đảm bảo khi đối tác chịu phần giữ tiền.

## Quy trình thanh toán đảm bảo

Mỗi đơn hàng là một máy trạng thái (state machine). Tiền chỉ rời khỏi tài khoản đối tác ở hai trạng thái kết thúc: `COMPLETED` (trả người bán) hoặc `REFUNDED` (trả người mua).

```python
from enum import Enum

CONFIRM_WINDOW_HOURS: int = 72      # thời gian người mua kiểm tra hàng sau khi nhận
SHIP_DEADLINE_HOURS: int = 48       # thời gian người bán phải gửi hàng sau khi người mua trả tiền

class State(Enum):
    PAID = 1          # đối tác đang giữ tiền của người mua
    SHIPPED = 2       # người bán đã giao cho đơn vị vận chuyển, có mã vận đơn
    DELIVERED = 3     # đơn vị vận chuyển báo đã giao
    DISPUTED = 4      # người mua khiếu nại trong thời hạn kiểm tra
    COMPLETED = 5     # tiền chuyển cho người bán
    REFUNDED = 6      # tiền hoàn cho người mua

def on_hour_tick(order: Order, now_hours: int) -> None:
    """Chạy định kỳ; tự động kết thúc đơn hàng khi một bên không hành động."""
    if order.state == State.PAID and now_hours - order.paid_at > SHIP_DEADLINE_HOURS:
        partner.refund(order)                  # partner: API của đối tác thanh toán có giấy phép
        order.state = State.REFUNDED
    elif order.state == State.DELIVERED and now_hours - order.delivered_at > CONFIRM_WINDOW_HOURS:
        partner.release_to_seller(order)       # im lặng quá hạn = đồng ý
        order.state = State.COMPLETED

def buyer_confirms(order: Order) -> None:
    assert order.state == State.DELIVERED
    partner.release_to_seller(order)
    order.state = State.COMPLETED

def buyer_disputes(order: Order, evidence: list[Video]) -> None:
    assert order.state == State.DELIVERED
    assert any(v.is_unboxing for v in evidence)  # bắt buộc video mở hộp liền mạch
    order.state = State.DISPUTED                   # tiền tiếp tục bị giữ; xem "Xử lý tranh chấp"
```

Trace với ví dụ: sinh viên A mua laptop 6.000.000 đ, trả tiền lúc giờ 0 → `PAID`. Người bán gửi hàng ở giờ 20 → `SHIPPED`. Đơn vị vận chuyển giao ở giờ 50 → `DELIVERED`, `delivered_at = 50`. A không làm gì. Ở giờ 123, `123 - 50 = 73 > 72` nên `release_to_seller` chạy → `COMPLETED`, người bán nhận 6.000.000 đ trừ phí. Nếu ở giờ 60 A mở khiếu nại kèm video mở hộp cho thấy màn hình vỡ → `DISPUTED`, tiền vẫn bị giữ.

### Cọc phòng trọ

Với pass phòng, "hàng" là quyền thuê tiếp phòng. Vì vậy, bước giao hàng được thay bằng hai bước: người thuê mới xem phòng tại chỗ, sau đó ký hợp đồng với chủ trọ. Tiền cọc giữ phòng chỉ đến tay người đăng khi hợp đồng mới đã ký.

```python
VIEW_DEADLINE_HOURS: int = 72     # người thuê mới phải đến xem phòng trong thời hạn này, thay cho SHIP_DEADLINE_HOURS
SIGN_DEADLINE_HOURS: int = 168    # quá 7 ngày sau khi xem mà chưa ký hợp đồng thì chuyển sang DISPUTED để nhân viên xem xét

def room_viewed(order: Order, matches_listing: bool) -> None:
    """Người thuê mới báo đã xem phòng tại chỗ."""
    assert order.state == State.PAID
    if matches_listing:
        order.state = State.DELIVERED          # phòng đúng như tin đăng, chờ ký hợp đồng
    else:
        partner.refund(order)                  # phòng khác ảnh hoặc không tồn tại: hoàn cọc
        order.state = State.REFUNDED

def lease_signed(order: Order, contract: Document) -> None:
    assert order.state == State.DELIVERED
    assert contract.tenant_id == order.buyer_id   # hợp đồng mới đứng tên người thuê mới
    partner.release_to_seller(order)
    order.state = State.COMPLETED
```

Trace với ví dụ: sinh viên B cọc 1.000.000 đ giữ phòng ở giờ 0 → `PAID`. B đến xem ở giờ 30, phòng đúng như video → `DELIVERED`. Ở giờ 80, B tải lên hợp đồng mới đứng tên B → `COMPLETED`, người đăng nhận 1.000.000 đ trừ phí. Nếu ở giờ 30 B thấy phòng khác hẳn video → `REFUNDED`, B nhận lại 1.000.000 đ.

### Đồng kiểm khi giao hàng

Khi giao qua đơn vị vận chuyển, Second Chance bật **đồng kiểm** (người nhận xem hàng trước khi nhận). GHN cho người nhận tối đa 15 phút để xem hàng ([nguồn](https://ghn.vn/blogs/thong-tin-giao-hang/ship-cod-duoc-kiem-tra-hang-khong)).

## Xác minh người dùng

| Cấp | Điều kiện | Quyền |
|---|---|---|
| Khách | Chỉ đăng ký bằng số điện thoại | Xem tin, nhắn tin |
| Người bán | eKYC bằng CCCD gắn chip (bắt buộc theo luật) | Đăng tin |
| Sinh viên đã xác minh | eKYC + email trường (`.edu.vn`) còn hoạt động | Huy hiệu "Sinh viên", tin được ưu tiên trong kết quả tìm kiếm |

Huy hiệu "Sinh viên" là lợi thế cạnh tranh chính so với các nhóm Facebook: người mua biết người bán là sinh viên thật, có trường và danh tính thật.

## Kiểm duyệt tin đăng

Mọi tin đăng qua bộ lọc tự động trước khi hiển thị. Tin bị gắn cờ đi vào hàng đợi duyệt thủ công.

| Danh mục | Thông tin bắt buộc khi đăng | Lý do |
|---|---|---|
| Điện thoại | IMEI, ảnh màn hình trạng thái "Tìm iPhone" đã tắt (với iPhone) | Máy còn dính iCloud (Activation Lock) có thể bị chủ cũ khóa từ xa ([nguồn](https://hoanghamobile.com/tin-tuc/cach-kiem-tra-icloud-iphone-cu/)). IMEI dùng để tra máy báo mất |
| Laptop | Số serial, ảnh cấu hình hệ thống | Tra bảo hành, chống mô tả sai cấu hình |
| Xe máy | Ảnh giấy đăng ký xe; tên trên giấy trùng tên đã eKYC | Khi bán xe, chủ xe phải làm thủ tục thu hồi đăng ký, người mua làm thủ tục sang tên (Thông tư 79/2024/TT-BCA, Điều 15, [văn bản](https://hethongphapluat.com/thong-tu-79-2024-tt-bca-quy-dinh-ve-cap-thu-hoi-chung-nhan-dang-ky-xe-bien-so-xe-co-gioi-xe-may-chuyen-dung-do-bo-truong-bo-cong-an-ban-hanh/chuong-2/muc-2)). Tên không trùng là dấu hiệu xe không chính chủ |
| Phòng trọ | Ảnh hợp đồng thuê đứng tên người đăng (trùng tên eKYC); video quay thật phòng, không chỉ ảnh; số điện thoại chủ trọ | Người thuê chỉ được cho thuê lại khi chủ trọ đồng ý (Bộ luật Dân sự 2015, Điều 475, [văn bản](https://hethongphapluat.com/bo-luat-dan-su-2015/dieu-475)), nên nhân viên gọi chủ trọ xác nhận trước khi duyệt tin. Video phòng trọ giá rẻ trên mạng thường là video lấy cắp từ nơi khác ([Tiền Phong, 2026](https://svvn.tienphong.vn/su-that-ve-nhung-video-quang-cao-phong-tro-vai-tram-nghin-dong-tai-trung-tam-ha-noi-post1872089.tpo)) |

Bộ lọc tự động gắn cờ khi gặp một trong các dấu hiệu sau:

- Giá thấp hơn 50% giá trung vị của cùng mẫu máy, hoặc của phòng trọ cùng phường, trên nền tảng.
- Nội dung chứa số tài khoản ngân hàng, đường link ngoài, hoặc mời nhắn qua Zalo/Messenger.
- Ảnh trùng với ảnh của một tin khác (cùng mã băm ảnh).
- Tài khoản mới dưới 7 ngày đăng từ 3 tin giá trị cao trở lên.

## Cảnh báo lừa đảo trong tin nhắn

Thủ đoạn phổ biến nhất khi mua đồ cũ online là yêu cầu chuyển tiền cọc "giữ hàng" rồi chặn liên lạc ([Thanh Niên, 2025](https://thanhnien.vn/mua-do-cu-tren-mang-coi-chung-sap-bay-thu-doan-lua-dao-185250318195006877.htm)). Khi tin nhắn chứa các từ "cọc", "chuyển khoản trước", số tài khoản hoặc mã QR, ứng dụng hiện cảnh báo:

> Second Chance không bao giờ yêu cầu chuyển cọc ngoài nền tảng. Hãy dùng Thanh toán đảm bảo hoặc gặp mặt để kiểm tra hàng. Không cọc phòng trọ trước khi xem phòng tận nơi.

Với giao dịch trực tiếp, ứng dụng gợi ý điểm gặp mặt an toàn: cổng trường, thư viện, hoặc trụ sở công an phường (với xe máy).

## Đánh giá người dùng

- Chỉ người đã hoàn tất giao dịch (`COMPLETED`, hoặc cả hai bên xác nhận "đã giao dịch" với giao dịch trực tiếp) mới được đánh giá. Điều kiện này chặn đánh giá ảo.
- Mỗi giao dịch cho phép mỗi bên đúng 1 đánh giá (1–5 sao và bình luận).
- Hồ sơ hiển thị số giao dịch thành công, điểm trung bình và tỷ lệ tranh chấp.

## Xử lý tranh chấp

| Bước | Thời hạn | Việc |
|---|---|---|
| 1. Thương lượng | 24 giờ | Hai bên trao đổi trong khung chat của đơn hàng |
| 2. Nền tảng phán quyết | 72 giờ | Nhân viên xem video mở hộp, ảnh tin đăng, lịch sử chat |
| 3. Kết quả | — | Hàng sai mô tả: người mua gửi trả, `REFUNDED` khi người bán nhận lại hàng. Người mua khiếu nại sai: `COMPLETED` |

Chế tài cho người vi phạm: lần 1 cảnh cáo; lần 2 khóa đăng tin 30 ngày; lừa đảo có chủ đích thì khóa vĩnh viễn và cung cấp thông tin eKYC cho công an khi có yêu cầu.
