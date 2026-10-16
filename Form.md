# Khảo sát mô phỏng nhu cầu Second Chance

Summary: 15 câu khảo sát mô phỏng, nhánh trả lời và lý do gắn với quyết định kinh doanh.

Bộ khảo sát và phản hồi giả lập phục vụ bài tập Kĩ năng khởi nghiệp, không phải kết quả khảo sát người thật. Second Chance được mô tả như một ý tưởng nền tảng cho sinh viên Hà Nội; các dịch vụ dưới đây chưa được xác nhận đã vận hành. Không thu tên, số điện thoại, CCCD hoặc địa chỉ cụ thể.

## Cách đọc

Nguồn duy nhất của câu hỏi và lựa chọn là [Survey.json](fake_data/Survey.json); tài liệu này được sinh tự động.
Q03 quyết định nhánh: chỉ mua trả lời Q05–Q07; chỉ bán trả lời Q08–Q10; cả hai trả lời cả hai nhóm.
Người chưa có nhu cầu bỏ Q04–Q10. Mọi người trả lời Q01–Q03 và Q11–Q15; chỉ Q14 tự nguyện.
Vì vậy mỗi người thấy 8, 12 hoặc 15 câu. Q05 và Q08 chọn nhiều đáp án (ít nhất một); các câu lựa chọn còn lại chọn đúng một đáp án.
Các mục Why dưới đây là suy luận thiết kế: nêu dữ liệu cần kết hợp, quyết định được hỗ trợ và giới hạn.

## Q01. Bạn thuộc nhóm nào?

**Hiển thị:** Mọi người. **Bắt buộc:** Có.

**Lựa chọn:** Sinh viên năm 1; Sinh viên năm 2–3; Sinh viên năm cuối; Không phải sinh viên.

**Why — quyết định kinh doanh:** Đối chiếu giai đoạn học với vai trò Q03 và nhu cầu Q05/Q08 để chọn nhóm tuyển người bán hoặc tiếp cận người mua. Không mặc định sinh viên năm cuối luôn bán đồ; người ngoài nhóm mục tiêu vẫn được giữ để phân tích riêng.

## Q02. Bạn thường học tập hoặc sinh hoạt gần cụm nào nhất tại Hà Nội?

**Hiển thị:** Mọi người. **Bắt buộc:** Có.

**Lựa chọn:** Bách khoa – Kinh tế Quốc dân – Xây dựng; Cầu Giấy – Xuân Thủy; Hà Đông – Thanh Xuân; Khu vực khác tại Hà Nội; Ngoài Hà Nội.

**Why — quyết định kinh doanh:** Ghép cụm địa lý với danh mục mua/bán và thời hạn để tìm nơi có cả hai phía, hoặc nơi cần tuyển người bán bổ sung trước quảng cáo. Chỉ tính mức độ trùng nhu cầu, không coi những người cùng cụm là các giao dịch chắc chắn.

## Q03. Trong 3 tháng tới, bạn có nhu cầu nào với đồ cũ hoặc pass phòng?

**Hiển thị:** Mọi người. **Bắt buộc:** Có.

**Lựa chọn:** Chỉ mua hoặc nhận pass phòng; Chỉ bán hoặc pass phòng đang thuê; Cả hai; Chưa có nhu cầu.

**Why — quyết định kinh doanh:** Tách nguồn cung và nhu cầu để chọn phía cần thu hút trước ở từng cụm/danh mục. Người có cả hai nhu cầu được tính ở cả hai phía, nhưng tổng người tham gia vẫn chỉ tính một lần. Không suy ra quy mô thị trường từ cơ cấu mẫu.

## Q04. Bạn dự kiến thực hiện nhu cầu gần nhất khi nào? Nếu có cả hai, chọn thời điểm sớm hơn.

**Hiển thị:** Có nhu cầu ở Q03. **Bắt buộc:** Có.

**Lựa chọn:** Trong 1 tháng; Trong tháng thứ 2–3; Chưa chốt thời điểm.

**Why — quyết định kinh doanh:** Ưu tiên tiếp cận nhóm có thời điểm gần thay vì dồn ngân sách vào toàn bộ người nói có nhu cầu. Với người vừa mua vừa bán, câu này không cho biết thời điểm của từng phía; không dùng để khẳng định hai giao dịch sẽ diễn ra cùng lúc.

## Q05. Trong 3 tháng tới, bạn đang cân nhắc mua hoặc nhận pass những gì? Chọn tất cả phương án phù hợp, kể cả khi bạn chỉ định chọn một trong số đó.

**Hiển thị:** Có nhu cầu mua/nhận pass ở Q03. **Bắt buộc:** Có.

**Lựa chọn (chọn nhiều, ít nhất một):** Laptop; Điện thoại; Xe máy; Nhận pass phòng trọ; Đồ khác.

**Why — quyết định kinh doanh:** Ghi nhận các danh mục người mua cân nhắc, ghép Q02 và Q08 để chọn nơi tìm hiểu và tuyển người bán phù hợp, không bỏ qua nhu cầu ngoài ưu tiên số một. Mỗi người được tính một lần trong từng danh mục đã chọn; không cộng các danh mục thành tổng người hoặc số giao dịch. Chưa phân biệt muốn mua nhiều món với chỉ chọn một trong nhiều phương án, chưa biết thứ tự ưu tiên. Second Chance kết nối người bán, không nhập kho; nhận pass phòng là thuê tiếp, không phải mua nhà.

## Q06. Điều gì cản trở bạn nhiều nhất khi mua đồ cũ hoặc nhận pass phòng qua kênh hiện tại?

**Hiển thị:** Có nhu cầu mua/nhận pass ở Q03. **Bắt buộc:** Có.

**Lựa chọn:** Thiếu tin phù hợp gần mình; Lo hàng hoặc phòng khác mô tả; Lo mất tiền cọc; Khó sắp xếp kiểm tra trực tiếp; Chưa gặp trở ngại rõ ràng.

**Why — quyết định kinh doanh:** Nếu thiếu tin, thử tuyển người bán; nếu lo sai mô tả, thử chuẩn hóa bằng chứng; nếu lo cọc, thử quy trình thanh toán đảm bảo. Đối chiếu Q12/Q13 để tránh xây tính năng mà người trả lời vẫn không có ý định dùng. Một câu chọn một chỉ cho biết trở ngại đứng đầu.

## Q07. Giả sử đối tác có giấy phép giữ tiền đến khi nhận đúng hàng; với phòng trọ, đến khi ký hợp đồng mới. Nếu phí thử nghiệm là 20.000 đồng/giao dịch, bạn chọn gì? Đây không phải mức phí đã chốt.

**Hiển thị:** Có nhu cầu mua/nhận pass ở Q03. **Bắt buộc:** Có.

**Lựa chọn:** Sẵn sàng trả 20.000 đồng; Chỉ dùng nếu miễn phí; Ưu tiên gặp trực tiếp, không dùng dịch vụ; Cần biết thêm điều kiện hoàn tiền.

**Why — quyết định kinh doanh:** Ghép mức chấp nhận phí với danh mục và nỗi lo để chọn nhóm thử nghiệm dịch vụ sau ưu đãi. Đây chỉ là phản ứng với một mức giá giả định, không phải giá tối ưu hay doanh thu. Chưa có báo giá đối tác nên không thể kết luận lợi nhuận; người mua xe hoặc xem phòng trực tiếp không mặc định cần giữ tiền.

## Q08. Trong 3 tháng tới, bạn đang cân nhắc bán hoặc pass những gì? Chọn tất cả phương án phù hợp, kể cả khi bạn chỉ định chọn một trong số đó.

**Hiển thị:** Có nhu cầu bán/pass ở Q03. **Bắt buộc:** Có.

**Lựa chọn (chọn nhiều, ít nhất một):** Laptop; Điện thoại; Xe máy; Pass phòng đang thuê; Đồ khác.

**Why — quyết định kinh doanh:** Ghi nhận các danh mục người bán cân nhắc, ghép Q02 và Q05 để chọn nhóm mời đăng tin thử nghiệm. Mỗi người được tính một lần trong từng danh mục đã chọn; không cộng các danh mục thành tổng người, số món, số tin hoặc số giao dịch. Chưa biết người bán định bán tất cả hay chỉ chọn một phương án, chưa biết danh mục ưu tiên. Ý định bán chưa phải tin đã xác minh hoặc hàng khớp nhu cầu người mua.

## Q09. Bạn muốn tìm được người mua hoặc người nhận pass trong bao lâu kể từ khi đăng tin?

**Hiển thị:** Có nhu cầu bán/pass ở Q03. **Bắt buộc:** Có.

**Lựa chọn:** Trong 7 ngày; Trong 8–30 ngày; Có thể chờ hơn 30 ngày.

**Why — quyết định kinh doanh:** Ghép mức cần bán sớm với danh mục và cụm để chọn nhóm hỗ trợ đăng tin đầu tiên. Đây là thời gian mong muốn, không phải thời gian bán thực tế; không dùng để hứa bán được trong 7 ngày.

## Q10. Nếu đăng bán cần xác minh danh tính qua đối tác và cung cấp bằng chứng hàng/phòng phù hợp, bạn sẽ làm gì? Không gửi giấy tờ trong khảo sát này.

**Hiển thị:** Có nhu cầu bán/pass ở Q03. **Bắt buộc:** Có.

**Lựa chọn:** Sẵn sàng thực hiện; Cần hiểu cách bảo vệ dữ liệu trước; Cần hướng dẫn chuẩn bị giấy tờ; Không muốn thực hiện.

**Why — quyết định kinh doanh:** Chọn hình thức hỗ trợ người bán: hướng dẫn giấy tờ hay giải thích bảo vệ dữ liệu. Theo dõi mức rơi dự kiến trước bước đăng tin; câu trả lời không thay thế tỷ lệ hoàn thành xác minh thật và không phải lý do bỏ yêu cầu xác minh của thiết kế hiện tại.

## Q11. Nếu tìm hoặc đăng đồ cũ/pass phòng, kênh bạn ưu tiên đầu tiên là gì?

**Hiển thị:** Mọi người. **Bắt buộc:** Có.

**Lựa chọn:** Nhóm Facebook của trường hoặc khu vực; Facebook Marketplace; Chợ Tốt; Bạn bè hoặc câu lạc bộ; Chưa có kênh ưu tiên.

**Why — quyết định kinh doanh:** Đối chiếu kênh với nguồn cung có nhu cầu gần và sẵn sàng xác minh để chọn nơi tuyển người bán thử nghiệm. Không coi kênh được nhắc nhiều là kênh có chi phí thu hút thấp nhất; cần đo số người đăng tin thực và chi phí bằng đường dẫn riêng.

## Q12. Một điểm nào sau đây có thể khiến bạn cân nhắc Second Chance thay cho kênh hiện tại?

**Hiển thị:** Mọi người. **Bắt buộc:** Có.

**Lựa chọn:** Tin phù hợp gần trường; Người bán đã xác minh; Bằng chứng tình trạng hàng hoặc phòng; Thanh toán đảm bảo qua đối tác; Chưa thấy lý do để đổi kênh.

**Why — quyết định kinh doanh:** So với rào cản Q06 và ý định Q13 để chọn thông điệp thử nghiệm, ví dụ gần trường hay xác minh người bán. Đây là sở thích tự khai khi được giới thiệu ý tưởng; cần thử thông điệp thực để biết yếu tố nào tạo đăng ký và giao dịch.

## Q13. Nếu có tin phù hợp tại khu vực bạn cần, bạn dự định làm gì với Second Chance trong 3 tháng tới?

**Hiển thị:** Mọi người. **Bắt buộc:** Có.

**Lựa chọn:** Thử dùng cho nhu cầu hiện có; Chỉ xem và tìm hiểu; Chưa định dùng.

**Why — quyết định kinh doanh:** Kết hợp nhu cầu, thời điểm và vai trò để chọn nhóm mời thử nghiệm thay vì coi mọi người quan tâm là khách hàng sắp mua. Không suy từ ý định có điều kiện thành tỷ lệ chuyển đổi hoặc doanh thu thật.

## Q14. Bạn muốn Second Chance giải quyết bất tiện cụ thể nào? Có thể bỏ trống; không ghi thông tin nhận dạng.

**Hiển thị:** Mọi người. **Bắt buộc:** Không.

**Trả lời:** Văn bản tự do.

**Why — quyết định kinh doanh:** Mã hóa câu mở thành vấn đề cụ thể để phát hiện yêu cầu còn thiếu trong lựa chọn đóng và thiết kế phỏng vấn tiếp. Một ý kiến chỉ tạo giả thuyết kiểm tra, không tự động trở thành tính năng ưu tiên.

## Q15. Trong 12 tháng qua, bạn đã hoàn tất bao nhiêu lần mua/bán đồ cũ hoặc nhận/pass phòng? Tính mỗi giao dịch một lần.

**Hiển thị:** Mọi người. **Bắt buộc:** Có.

**Lựa chọn:** 0 lần; 1–2 lần; 3 lần trở lên.

**Why — quyết định kinh doanh:** Đối chiếu kinh nghiệm giao dịch với rào cản để tách hướng dẫn cho người mới và vấn đề của người đã giao dịch nhiều lần. Không gọi người có nhiều giao dịch là VIP: chưa đo giá trị giao dịch, biên lợi nhuận hoặc doanh thu họ mang lại. Không tùy ý tăng trọng số nhóm này khi báo cáo tỷ lệ chung.
