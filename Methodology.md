# Phương pháp mô phỏng Second Chance

Summary: Giả định tạo 50 phiếu, giới hạn suy luận, nguồn câu hỏi và cách tái tạo/kiểm tra các tệp dẫn xuất.

## Mục đích và nguồn thiết kế

Bộ dữ liệu phục vụ bài tập Kĩ năng khởi nghiệp, minh họa cách chuyển câu trả lời thành giả thuyết và quyết định thử nghiệm. Không có khảo sát người thật; không dùng bộ dữ liệu này để chứng minh nhu cầu thị trường hoặc kết quả kinh doanh.

Phạm vi dựa trên sinh viên Hà Nội và các danh mục trong [Marketing](docs/Marketing.md#khách-hàng-mục-tiêu). Câu về xác minh và thanh toán đảm bảo dựa trên thiết kế trong [TrustAndSafety](docs/TrustAndSafety.md#hai-chế-độ-giao-dịch), không phải thông báo các dịch vụ đã hoạt động. Bộ mô phỏng không kiểm chứng lại các dẫn nguồn pháp lý hoặc thị trường trong hai tài liệu đó.

Yêu cầu thiết kế đã được khôi phục từ session FakeData `1b73d823` và `2a97c2df`: mục Why phải nối dữ liệu với quyết định kinh doanh có ích; có thể thay câu hỏi; kết luận không vượt quá tiền đề. Người thực hiện duyệt phạm vi 10–15 câu và 50 phiếu ngày 15/10/2026. Bản hiện tại chọn 15 câu.

## Nguồn dữ liệu và tài liệu

Đọc câu hỏi, lựa chọn, nhánh và Why trong [Form](Form.md). Nguồn biên soạn duy nhất là [Survey.json](fake_data/Survey.json); Form được chương trình tạo từ nguồn đó để tránh hai bản câu hỏi lệch nhau.

Dữ liệu để phân tích nằm trong [Responses.csv](fake_data/Responses.csv). Mỗi dòng là một người giả lập; `response_id` là mã phiếu, `data_origin=synthetic` là nhãn mô phỏng. Các cột Q01–Q15 giữ đáp án nguyên văn; cột `_status` đi kèm phân biệt `answered` (đã trả lời), `not_shown` (không hiện theo nhánh), `skipped_optional` (hiện nhưng bỏ câu tự nguyện). Không chuyển các trạng thái này thành câu hỏi khảo sát.

Cơ cấu vai trò và seed nằm trong [SimulationConfig.json](fake_data/SimulationConfig.json). Cơ cấu này được đặt trước, không phải kết quả phát hiện thị trường. Số phiếu của từng nhóm không có ý nghĩa về độ phổ biến ngoài thực tế.

Bộ sinh thật là `generate()` trong [GenerateData.py](tools/GenerateData.py). Các liên hệ có điều kiện về thời điểm, ý định thử dùng, nỗi lo cọc và xác minh là giả định thiết kế. Vì vậy, tương quan thu được không thể được báo cáo như một khám phá độc lập. Các lựa chọn còn lại được lấy mẫu từ ngân hàng; mẫu không được hiệu chỉnh để tạo chênh lệch cung/cầu có lợi cho một danh mục.

Câu mở dùng ngân hàng câu ngắn theo rào cản, có thể lặp và có phiếu bỏ trống. Không dùng mô hình ngôn ngữ hoặc tạo danh tính giả. Bộ dữ liệu hướng tới đáp án hợp lệ và quan hệ đã khai báo; không tuyên bố mô phỏng đầy đủ cách người thật suy nghĩ hoặc viết.

## Giới hạn quyết định

- Đối chiếu mua/bán theo danh mục và cụm chỉ gợi ý nơi cần kiểm tra nguồn cung. Không có giá, model máy, tình trạng, địa chỉ cụ thể hoặc thời điểm riêng của cả hai phía để xác nhận khớp giao dịch.
- Người có hai vai trò xuất hiện trong cả hai phía nhưng chỉ là một người. Không cộng tổng hai phía thành cỡ mẫu.
- Thời gian bán mong muốn không phải thời gian bán thực tế; ý định dùng có điều kiện không phải chuyển đổi thật.
- Giá 20.000 đồng là tình huống thử nghiệm ở một mức giá duy nhất. Không có dữ liệu để ước lượng đường cầu, giá tối ưu, doanh thu hoặc lợi nhuận.
- Tần suất giao dịch quá khứ chưa đủ để xác định VIP; không tăng trọng số người giao dịch nhiều khi báo cáo tỷ lệ chung.
- Không thu thập giấy tờ, tên, email, số tài khoản hoặc thông tin nhận dạng. Không nhập lên Google Forms, không đăng công khai repository trong phạm vi này.

Các bảng, mẫu số và quyết định minh họa nằm trong [Analysis](Analysis.md). Khi có mẫu thật, lưu và phân tích riêng, kèm cách tuyển người và bằng chứng giao dịch; không trộn với dữ liệu mô phỏng.

## Tái tạo và kiểm tra

Dùng Python 3, thư viện chuẩn, không cần cài gói ngoài. Chạy tại thư mục gốc project:

```sh
python3 tools/VerifyData.py --write
```

Lệnh chạy bộ sinh thật, kiểm tra phiếu, tạo lại CSV, Form, Analysis và [Validation.json](fake_data/Validation.json), rồi đối chiếu nội dung đã lưu. Với cùng nguồn và seed trong cùng môi trường Python, đầu ra được đối chiếu chính xác từng byte. Chưa xác nhận tái tạo giống từng byte giữa các phiên bản Python khác nhau.

Để chỉ kiểm tra mà không ghi lại:

```sh
python3 tools/VerifyData.py
```

Kiểm tra bao gồm 50 phiếu đã lưu và bốn ca cố ý phá dữ liệu: mất nhãn mô phỏng, đáp án ngoài lựa chọn, thiếu câu bắt buộc và trả lời câu không hiện. Những ca lỗi này phải bị từ chối; kiểm tra thất bại sẽ trả mã thoát khác 0. Đây là kiểm tra workflow dữ liệu, không phải kiểm chứng thị trường.

Kiểm tra được nối vào pre-commit cục bộ; hook toàn cục hiện có tiếp tục chạy các kiểm tra tệp đã stage. Sau khi clone sang máy khác, cài hook cục bộ bằng:

```sh
python3 tools/InstallHooks.py
```

Tệp kết quả kiểm tra là đầu ra tái tạo, không phải nhật ký có dấu thời gian hoặc bằng chứng đã khảo sát. Kết quả thực thi hiện tại được in trực tiếp trong terminal.
