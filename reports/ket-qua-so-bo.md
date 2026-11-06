# Kết quả thực nghiệm sơ bộ

> Bản nháp nội dung để chuyển sang báo cáo Overleaf. Các con số dưới đây được tổng hợp từ các CSV đầu ra hiện có trong `data/processed/`. Cần đối chiếu lại với notebook/Drive trước khi nộp báo cáo.

## Phạm vi và dữ liệu

Nghiên cứu phân tích **bài đăng** trong 19 subreddit liên quan đến khoa học dữ liệu, thống kê và trí tuệ nhân tạo; không phân tích bình luận hay mạng lưới phản hồi, và không đại diện cho toàn bộ Reddit. Tập dữ liệu có 545.427 bài, trải từ 19/03/2008 đến 08/05/2022. Văn bản đầu vào được tạo bằng cách ghép tiêu đề với nội dung bài đăng nếu có. Trường nội dung `post` thiếu 271.218/545.427 bản ghi (xấp xỉ 49,7%), do đó một phần phân tích chỉ dựa trên tiêu đề.

## Phân bố và xu hướng cảm xúc

VADER gán 56,83% bài là tích cực, 31,86% trung tính và 11,31% tiêu cực. Đây là nhãn từ bộ từ vựng/quy tắc, không phải nhãn cảm xúc chuẩn được con người xác nhận. Kết quả mô tả sắc thái ngôn ngữ trong bài đăng, không thể hiện cảm xúc cá nhân của mọi người dùng.

Lượng bài tăng mạnh trong các năm cuối của chuỗi thời gian: năm 2021 có 124.246 bài, nhiều nhất trong các năm hoàn chỉnh có trong dữ liệu. Tháng có nhiều bài nhất là 05/2021 với 12.745 bài. Không có bản ghi trong toàn bộ năm 2013; khoảng trống này phải được hiển thị là dữ liệu thiếu, không phải tháng có 0 bài. Tập dữ liệu kết thúc vào tháng 05/2022 nên năm 2022 là năm chưa đầy đủ.

Tỷ lệ cảm xúc tích cực VADER cao nhất trong các subreddit có nhiều bài là `AskStatistics` (72,36%), `learnmachinelearning` (65,11%) và `datascience` (61,53%). `DataScienceJobs` có tỷ lệ tích cực thấp hơn (29,68%) và compound trung bình thấp nhất trong 19 subreddit (0,145). Đây là mô tả của các bài được thu thập, không nên diễn giải thành khác biệt nhân quả giữa cộng đồng; độ dài, loại bài và quy mô mẫu có thể khác nhau.

## Chủ đề thảo luận

Notebook 04 huấn luyện TF-IDF + NMF với 12 chủ đề trên mẫu cố định tối đa 50.000 bài, sau đó gán chủ đề cho toàn bộ dữ liệu theo batch. Các nhóm từ khóa gợi ý các chủ đề như học máy, nghề nghiệp/khoa học dữ liệu, trí tuệ nhân tạo, tuyển dụng, deep learning, mạng nơ-ron, thị giác máy tính, câu hỏi thống kê và hồi quy.

Tuy nhiên, topic 0 chiếm 333.359 bài (61,12%) và có các từ khóa chung như `data`, `time`, `model`, `work`, `looking`, `need`, `question`. Vì vậy đây là một nhóm rộng/hỗn hợp, không nên gọi là một chủ đề nội dung cụ thể hoặc dùng tỷ trọng của nó để kết luận một chủ đề thống trị. Topic 8 chỉ có 2.831 bài (0,52%) và chứa nhiều từ riêng về một cuộc phỏng vấn/sản phẩm; nên kiểm tra thêm bài đại diện trước khi đặt tên. Các nhãn NMF là kết quả khám phá, không phải phân loại chủ đề đã được gán nhãn chuẩn.

## Đối chiếu VADER trên mẫu audit

Mẫu audit gồm 150 bài được lấy cân bằng theo ba nhãn VADER (tối đa 50 bài mỗi nhãn). Ma trận đối chiếu hiện tại cho thấy agreement 46,67% và Cohen's kappa 0,20. Trong số bài được rà là trung tính, VADER gán 37 bài thành tiêu cực và 33 bài thành tích cực; điều này gợi ý bộ từ vựng có thể phản ứng với từ ngữ mang sắc thái như “help”, “hard” trong các câu hỏi/xin hỗ trợ, dù toàn câu không thể hiện rõ cảm xúc.

Các con số audit hiện được xem là **kết quả rà soát có hỗ trợ của trợ lý AI**, chưa phải đánh giá độc lập của người gán nhãn. Cần người nghiên cứu kiểm tra và xác nhận từng `human_label`, đặc biệt các câu hỏi, bài chỉ có tiêu đề, liên kết quảng bá và văn bản thiếu ngữ cảnh, trước khi trình bày agreement/kappa như đánh giá thủ công. Do mẫu được phân tầng theo nhãn VADER, không dùng mẫu này để ước lượng tỷ lệ cảm xúc trong toàn bộ 545.427 bài.

## Giới hạn và bước tiếp theo

1. Xác nhận nhãn audit bởi người nghiên cứu; lưu phiên bản cuối và ghi rõ quy tắc gán nhãn.
2. Kiểm tra lại bài đại diện và mức độ diễn giải được của từng topic; cân nhắc báo cáo topic 0 như nhóm hỗn hợp hoặc tinh chỉnh mô hình nếu còn thời gian.
3. Khi phân tích xu hướng, giữ nguyên các tháng thiếu dữ liệu và đánh dấu năm 2022 là chưa đầy đủ.
4. Trong báo cáo cuối, nêu rõ tập dữ liệu là các bài đăng trong nhóm subreddit Data Science/AI đã chọn; không suy rộng kết quả cho toàn Reddit hay cho cảm xúc cá nhân của người dùng.
