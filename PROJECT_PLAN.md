# Kế hoạch đồ án: Phân tích xu hướng và cảm xúc trên Reddit

## 1. Tóm tắt đề tài

**Câu hỏi nghiên cứu:** Trong các cộng đồng Reddit thuộc một chủ đề được chọn, những chủ đề thảo luận nào nổi bật, cảm xúc thể hiện ra sao, và mức độ/chủ đề/cảm xúc thay đổi thế nào theo thời gian?

**Phạm vi đề xuất:** Phân tích nhiều subreddit, không giới hạn ở DeepSeek. Để dữ liệu có ý nghĩa và hoàn tất trong hai tuần, phạm vi Core nên giới hạn ở các cộng đồng Data Science/AI nếu chọn bộ Reddit Data Science Posts (500k+). Kết luận phải nêu rõ phạm vi này, không khái quát thành toàn bộ Reddit.

**Sản phẩm Core:** báo cáo viết trên Overleaf; pipeline ETL có thể chạy lại; phân tích xu hướng, topic và sentiment; ứng dụng demo gọn để lọc cộng đồng/khoảng thời gian và xem biểu đồ.

**Stretch:** phân tích mạng phản hồi nếu dataset có quan hệ reply/comment và đủ thời gian; so sánh thêm mô hình sentiment; triển khai demo ngoài Colab.

## 2. Dataset khảo sát và quyết định đề xuất

### Dataset nhóm đã chốt — bước đầu là kiểm tra dữ liệu thật

**Reddit Data Science Posts (500k+)** trên Kaggle. Tài liệu mô tả hơn 500.000 bài từ 19 subreddit liên quan Data Science, có nội dung, subreddit, `created_date`/`created_timestamp`, score và số bình luận. Các trường này hỗ trợ phân tích nội dung, cộng đồng, tương tác và biến đổi theo thời gian. Nguồn mô tả schema: [Reddit-Data-Science-Posts README](https://github.com/Nordant/Reddit-Data-Science-Posts); notebook Kaggle dùng bộ dữ liệu: [How is Data Science on Reddit?](https://www.kaggle.com/code/maksymshkliarevskyi/how-is-data-science-on-reddit-eda-rapids).

**Giới hạn:** chỉ có các subreddit thuộc Data Science, không đại diện cho Reddit nói chung; nội dung comments có thể không nằm trong file chính. Trước khi chốt cần tải/đọc metadata để kiểm tra license, phiên bản, kích thước, schema, khoảng thời gian, missing/duplicate và khả năng lấy dữ liệu.

### Phương án dự phòng

- [1 Million Reddit Comments from 40 Subreddits](https://www.kaggle.com/smagnan/1-million-reddit-comments-from-40-subreddits/metadata): độ rộng cộng đồng và lượng văn bản tốt, nhưng bản Kaggle công bố các cột body, subreddit, controversiality và score, không có timestamp. Dùng được để so sánh sentiment/topic giữa subreddit; không đủ để kết luận xu hướng thời gian.
- [Reddit Posts and Comments from r/WallStreetBets](https://www.kaggle.com/datasets/curiel/rwallstreetbets-posts-and-comments): có timestamp và tương tác, nhưng chỉ tập trung một subreddit/tài chính; không khớp yêu cầu phân tích nhiều cộng đồng rộng hơn.

**Trạng thái:** nhóm đã chốt bộ này. Task DATA-01 vẫn cần tải và xác minh file thực tế, license, schema và khoảng thời gian trước khi phân tích. Nếu bộ dữ liệu không truy cập được hoặc thiếu trường cốt lõi, báo lại để nhóm quyết định phạm vi điều chỉnh; không tự thay dataset.

## 3. Phương pháp dự kiến

- **Đơn vị phân tích:** một bài đăng Reddit; ghép title và body thành văn bản phân tích, nhưng giữ riêng cột gốc và metadata.
- **ETL:** lưu raw bất biến; tạo clean CSV/Parquet có schema, parse timestamp UTC, chuẩn hóa text tối thiểu, loại bản ghi rỗng/duplicate theo quy tắc ghi lại; tạo manifest nguồn, version, checksum và số dòng từng bước.
- **Xu hướng:** số lượng bài theo tuần/tháng; thay đổi score/num_comments; xu hướng theo subreddit. Cẩn trọng khi so sánh score giữa cộng đồng.
- **Sentiment:** VADER làm baseline cho văn bản tiếng Anh ngắn, informal; kiểm tra thủ công một mẫu có phân tầng theo nhãn/cộng đồng và ghi nhận sarcasm, ngôn ngữ khác, bài chỉ có link. Không gọi điểm lexicon là ground truth.
- **Topics:** TF-IDF + NMF làm baseline giải thích được; số topic chọn trên tập phát triển và kiểm tra chất lượng bằng đọc mẫu từ từng topic. Chủ đề theo thời gian là phần phân tích chính.
- **Đánh giá:** báo cáo coverage/thiếu dữ liệu, phân bố sentiment, mẫu kiểm tra thủ công và độ ổn định chủ đề; không dùng accuracy nếu không có nhãn chuẩn độc lập.
- **Demo:** Streamlit trong Colab hoặc notebook có widgets, tùy thời gian tích hợp; ưu tiên bộ lọc subreddit/ngày và biểu đồ topic/sentiment.
- **Nghiên cứu:** dùng Patel et al. làm khung sentiment-topic-network, nhưng chỉ tuyên bố tái hiện các phần thực sự có dữ liệu; tham khảo Thelwall et al. về sentiment strength trong văn bản ngắn informal. Xác minh chi tiết bài báo và cách trích dẫn trong task LIT-01.

## 4. Lịch và phân công

Giả định lập lịch: bắt đầu 05/11/2026, bàn giao 19/11/2026; “làm full tuần” được hiểu là ưu tiên làm đồ án hằng ngày. Chưa có số giờ/ngày hoặc tên thành viên nên owner tạm dùng Thành viên A; effort bên dưới là ước lượng người-ngày và cần điều chỉnh theo số giờ thực tế. Một thành viên tự phụ trách các task và tự kiểm tra bằng checklist/evidence; dành ít nhất 2 ngày làm việc để tích hợp, sửa lỗi và chuẩn bị trình bày.

| ID | Công việc / kết quả | Owner tạm | Phụ thuộc | Thời gian | Hoàn thành khi |
|---|---|---:|---|---:|---|
| START-01 | Chốt câu hỏi nghiên cứu, rubric (hiện chưa có), ranh giới kết luận | A | — | 0.5 ngày | README dự án ghi rõ mục tiêu và giới hạn; xác nhận dataset đầu vào |
| DATA-01 | Tải và kiểm tra dataset Kaggle, license, files/schema/time range | A | START-01 | 1 ngày | Đã xác minh qua manifest: 1 CSV, 545,427 dòng, 13 cột, 340,112,365 bytes, khoảng 2008-03-19 đến 2022-05-08 UTC; `post` thiếu 271,218 dòng, `title` không thiếu; checksum được ghi lại |
| LIT-01 | Đọc Patel/Thelwall; tóm tắt phương pháp và tạo BibTeX | A | START-01 | 1.5 ngày | Có bảng literature: câu hỏi, dữ liệu, phương pháp, kết quả, giới hạn; BibTeX/DOI kiểm tra được |
| ENV-01 | Chuẩn hóa Colab setup; lưu cấu hình môi trường, hướng dẫn chạy; chọn cách truy cập Kaggle | A | DATA-01 | 0.5 ngày | Notebook khởi động được, tải/đọc một mẫu dữ liệu; không đưa token cá nhân vào repo |
| ING-01 | Raw ingestion vào `data/raw` hoặc MinIO; manifest + checksum | A | DATA-01, ENV-01 | 0.5 ngày | Raw được lưu nguyên bản, có nguồn/version/checksum; có hướng dẫn lấy lại |
| QA-01 | Profiling và data quality report | A | ING-01 | 0.5 ngày | Báo cáo missing, duplicate, null/empty text, timestamp parse, subreddit counts, độ dài text |
| ETL-01 | Tạo clean dataset Parquet/CSV cùng log lineage | A | QA-01 | 1 ngày | Script/notebook ETL chạy lại; số dòng input/output và quy tắc loại bỏ được lưu |
| EDA-01 | Biểu đồ phân bố thời gian, subreddit, score/comments và độ dài | A | ETL-01 | 1 ngày | Notebook có hình và nhận xét định lượng, không chỉ ảnh chụp |
| SPL-01 | Chốt quy tắc phát triển/kiểm tra cho topics và kiểm định sentiment mẫu | A | ETL-01 | 0.5 ngày | Có seed, mẫu, quy tắc không rò rỉ và file ID của mẫu kiểm tra |
| FTR-01 | Pipeline text normalization + TF-IDF; lưu vocabulary/config | A | SPL-01 | 1 ngày | Fit chỉ trên dữ liệu phát triển; transform nhất quán; cấu hình có thể tái lập |
| BAS-01 | VADER sentiment baseline và kiểm tra thủ công | A | ETL-01, SPL-01 | 1 ngày | Có phân bố sentiment theo tuần/subreddit và bảng audit mẫu kèm lỗi/giới hạn |
| MOD-01 | NMF topic model baseline; chủ đề và ví dụ đại diện | A | FTR-01 | 1 ngày | Có topic terms, mẫu đại diện, cách chọn số topic và nhận xét coherence/diễn giải |
| TREND-01 | Tổng hợp trend theo thời gian, topic và sentiment | A | BAS-01, MOD-01 | 1 ngày | Có biểu đồ tuần/tháng và so sánh cộng đồng; xử lý mùa vụ/quy mô khi diễn giải |
| DEMO-01 | Ứng dụng demo lọc subreddit/khoảng thời gian | A | TREND-01 | 1.5 ngày | Người dùng chọn bộ lọc và xem KPI/biểu đồ; có lệnh chạy và ảnh minh họa |
| REPORT-01 | Báo cáo Overleaf: phương pháp, dữ liệu, kết quả, hạn chế, tài liệu | A | LIT-01, QA-01, TREND-01 | 2 ngày | Compile PDF; mọi bảng/hình khớp notebook; nguồn và giới hạn được trích dẫn |
| REL-01 | Chạy lại từ hướng dẫn, kiểm tra artifact và bàn giao | A | DEMO-01, REPORT-01 | 1 ngày | Có thể tự chạy lại theo hướng dẫn; có checklist, versions, logs và output |

**DATA-01 evidence đã nhận:** manifest dataset cho biết file `reddit_database.csv`, 545,427 dòng, 13 cột, khoảng thời gian 2008-03-19 đến 2022-05-08 UTC. `post` thiếu 271,218 dòng (49.7%); `title` và timestamp không thiếu.\n\n**ETL/QA evidence đã nhận từ `etl_report.json`:** giữ 545,427/545,427 dòng; không loại ID trùng, text rỗng hoặc timestamp lỗi; 19 subreddit. `num_crossposts` thiếu 112,425; `subreddit_subscribers` thiếu 139,617; số bài từng subreddit rất lệch (MachineLearning 121,385 so với kaggle 627). Tháng không có dòng gồm 2013; vì vậy trend theo tháng phải giữ khoảng trống là thiếu dữ liệu, không gán bằng 0. Văn bản là title + post; title-only rows vẫn được giữ. Cần bổ sung phân bố độ dài và xác minh license trước khi báo cáo cuối. Đơn vị phân tích là bài đăng, không phải cá nhân; dataset không có comment tree để làm network analysis.\n\n### Mốc bàn giao

- **Ngày 1–2 (06–07/11):** chốt dataset; xác nhận schema/license/khả năng tải; tóm tắt bài báo.
- **Ngày 3–5 (08–10/11):** ingestion, QA, ETL, EDA; khóa ranh giới phân tích.
- **Ngày 6–9 (11–14/11):** sentiment baseline, topic model, xu hướng; bắt đầu viết kết quả Overleaf.
- **Ngày 10–12 (15–17/11):** tích hợp demo và báo cáo; tự rà theo checklist.
- **Ngày 13–14 (18–19/11):** chạy lại, sửa lỗi, hoàn tất PDF và demo.

## 5. Cấu trúc thư mục đề xuất

```text
Bigdata/
├── data/
│   ├── raw/                 # nguyên bản; không commit lên Git
│   ├── processed/           # clean/parquet
│   └── manifests/
├── notebooks/
│   ├── 01_data_audit.ipynb\n│   ├── 02_etl.ipynb\n│   ├── 03_sentiment_trends.ipynb
│   ├── 02_eda_etl.ipynb
│   ├── 03_sentiment_topics.ipynb
│   └── 04_trends_demo.ipynb
├── src/
├── reports/                 # file nguồn Overleaf hoặc link handoff
├── compose.yaml             # MinIO cục bộ, nếu cần lưu raw
├── requirements.txt
└── PROJECT_PLAN.md
```

## 6. Hạ tầng và lưu ý

- Phân tích chính chạy trên Google Colab; 16 GB RAM đủ cho sample/Parquet có kiểm soát nhưng không nạp nguyên dataset nhiều GB vào RAM nếu chưa kiểm tra kích thước. Dùng chunking hoặc sample cho profiling, rồi xử lý phần cần thiết.
- Kaggle API token chỉ lưu trong Secrets của Colab; không commit `kaggle.json`.
- MinIO hiện có thể dùng làm kho local tùy chọn cho raw/backup. Colab không truy cập `localhost` của máy người dùng trực tiếp; không phụ thuộc MinIO local trong notebook Colab nếu chưa thiết lập kết nối an toàn. Có thể để raw trên Google Drive/Kaggle input hoặc tải từ Kaggle trong Colab, còn MinIO là bản lưu local.
- Mặc định không dùng GPU vì VADER, TF-IDF và NMF baseline chạy CPU; GPU chỉ cần nếu nhóm mở rộng sang embedding/transformer.

## 7. Thông tin còn cần chốt nội bộ

- Tên thành viên để thay owner A.
- Xác nhận “full tuần” có nghĩa là số giờ/ngày nào; lịch trong bảng đang là ước lượng.
- Dataset đã chốt; cần mở/tải và kiểm tra ngày đầu. Dataset bao phủ nhiều subreddit trong mảng Data Science/AI, không đại diện tất cả lĩnh vực Reddit.

