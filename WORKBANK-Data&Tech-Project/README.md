# Phân tích tác động của trí tuệ nhân tạo đối với lực lượng lao động công nghệ và dữ liệu

Dự án này cung ứng một dashboard mô phỏng động trực quan hóa và định lượng hóa tác động của trí tuệ nhân tạo (AI) đối với thị trường lao động ngành công nghệ thông tin (IT) và dữ liệu. Hệ thống sử dụng thuật toán phân cụm **K-Means** trên dữ liệu tác vụ gốc của **O*NET (Mỹ)** kết hợp với số liệu khảo sát thực tế và mô hình toán học dự báo sự phát triển công nghệ để đưa ra các gợi ý dịch chuyển nghề nghiệp tối ưu cho lao động Việt Nam.

---

## Các tính năng cốt lõi của ứng dụng

### 1. Hiện trạng nhân sự và bản đồ rủi ro công nghiệp (Dữ liệu gốc O*NET của Mỹ)
- **Phân bổ kinh nghiệm làm việc:** Trực quan hóa cơ cấu phân phối thâm niên (Junior, Mid, Senior) từ dữ liệu khảo sát thực tế của ngành.
- **Bản đồ tác vụ K-Means:** Phân cụm toàn bộ các tác vụ công việc thành 4 vùng rủi ro (vùng an toàn, vùng ổn định, vùng tiềm ẩn nguy cơ, và vùng báo động) dựa trên 6 chỉ số đa chiều: khả năng tự động hóa, mong muốn tự động hóa, yêu cầu chuyên môn, mức độ bất định, yêu cầu giao tiếp và mức lương trung bình.

### 2. Động lực chuyển giao và tấm khiên phòng ngự con người (Dữ liệu gốc O*NET của Mỹ)
- **Động cơ tự động hóa:** Khảo sát cường độ mong muốn chuyển giao tác vụ cho AI của người lao động.
- **Rào cản phòng ngự phi kỹ thuật:** Trực quan hóa mật độ phân bổ của hai chiều rào cản cốt lõi: mức độ bất định (Involved Uncertainty) và yêu cầu giao tiếp tương tác liên nhân sự (Interpersonal Communication Requirement).
- **Bẫy năng lực và độ lệch kiểm duyệt (Verification Deficit):** Phân tích so sánh hành vi lạm dụng LLM ở nhóm Junior gây trì trệ phát triển năng lực với cách sử dụng AI như công cụ nhân hiệu suất của nhóm Senior.
- **Tấm khiên thích ứng:** Biểu đồ so sánh khả năng tự động hóa của các nhóm tác vụ kỹ năng cốt lõi với phối màu theo chủ đề **rừng già (deep forest)** thanh lịch.

### 3. Mô phỏng đà phát triển AI và dự báo rủi ro tác vụ tại Việt Nam
- **Mô phỏng đà phát triển AI:** Sử dụng mô hình toán học phát triển hàm số mũ để mô phỏng năng lực AI của Mỹ ($g_{US} = 24.1\%$) và Việt Nam ($g_{VN} = 20.0\%$), tích hợp chênh lệch Chỉ số sẵn sàng AI quốc gia ($K_{Readiness} \approx 67.9\%$).
- **Sự lệ thuộc công nghệ lõi:** Phân tích các tác động vĩ mô khi Việt Nam phụ thuộc hoàn toàn vào các mô hình AI ngoại nhập (LLM foundation models) đối với thị trường outsourcing lao động IT.

### 4. Hệ thống khuyến nghị dịch chuyển nghề nghiệp
- **Chỉ số Độ sẵn sàng Chuyển đổi (Transition Readiness Score - TRS):** Lượng hóa tỷ lệ phần trăm kỹ năng đã có sẵn từ ngành cũ có thể mang sang áp dụng ngay cho ngành mới:
  $$TRS = 100\% - \text{Gánh nặng Đào tạo lại}$$
- **Phân rã lộ trình học tập:** Phân loại các tác vụ mới cần học thành nhóm **tác vụ bổ trợ dễ học** và **tác vụ chuyên sâu cần đào tạo** để tránh gây nản lòng cho người lao động.
- **Khuyến nghị chính sách vĩ mô:** 3 chiến lược quốc gia thiết thực cho Việt Nam (Dịch chuyển chuỗi giá trị IT, Tối ưu hóa lộ trình thích ứng và tăng cường tấm khiên thích ứng quốc gia).

---

## Cơ sở lý thuyết và Mô hình toán học

### 1. Chỉ số tương đồng kỹ năng Jaccard
Đo lường mức độ trùng lặp kỹ năng yêu cầu giữa ngành nguồn ($S_{source}$) và ngành mục tiêu ($S_{target}$):
$$J(S_{source}, S_{target}) = \frac{|S_{source} \cap S_{target}|}{|S_{source} \cup S_{target}|} \times 100\%$$

### 2. Mô hình giả lập năng lực AI tại Việt Nam theo thời gian $t$
$$AI_{VN}(t) = AI_{US}(0) \times K_{Readiness} \times (1 + g_{VN} \times m)^n$$
- Trong đó $n = t - 2025$.
- $m$ là hệ số điều chỉnh tốc độ tự động hóa của phân cụm tác vụ K-Means ($m_{Alert} = 1.5$, $m_{At-risk} = 1.2$, $m_{Stable} = 0.8$, $m_{Safe} = 0.5$).

### 3. Bộ lọc ràng buộc chuyển dịch tối ưu
- **An toàn công nghệ:** $AI_{target}(t) < AI_{source}(t)$
- **Bảo vệ thu nhập:** $Wage_{target} \ge 85\% \times Wage_{source}$
- **Tương đồng kỹ năng:** $J(S_{source}, S_{target}) \ge 20\%$ (nới lỏng xuống 10% nếu cần).

---

## Cấu trúc thư mục dự án

```text
├── BTCN.py                          # Ứng dụng web Streamlit chính
├── generate_pdf_report.py           # Chương trình xuất báo cáo phân tích PDF học thuật
├── data/
│   ├── task_statement_with_metadata.csv  # Dữ liệu tác vụ O*NET gốc
│   ├── expert_rated_technological_capability.csv # Đánh giá năng lực tự động hóa chuyên gia
│   └── domain_worker_metadata.csv   # Dữ liệu khảo sát nhân sự và thâm niên IT
├── Báo cáo phân tích tác động của trí tuệ nhân tạo đối với lực lượng lao động công nghệ và dữ liệu.pdf # Báo cáo PDF Times New Roman được sinh tự động
└── README.md                        # Hướng dẫn dự án bằng tiếng Việt
```

---

## Hướng dẫn cài đặt và Khởi chạy

### 1. Cài đặt các thư viện cần thiết
Dự án yêu cầu Python 3.10 trở lên. Hãy cài đặt các thư viện phụ thuộc bằng lệnh:
```bash
pip install streamlit pandas numpy matplotlib plotly scikit-learn reportlab pillow
```

### 2. Sinh báo cáo phân tích dạng PDF
Để tạo tệp báo cáo PDF bằng font **Times New Roman** (không chứa icon, định dạng Sentence case chuẩn), hãy chạy lệnh:
```bash
python generate_pdf_report.py
```
Tập lệnh sẽ kết xuất tệp PDF chuyên nghiệp trực tiếp vào gốc thư mục dự án để ứng dụng Streamlit có thể đọc và cho phép người dùng tải xuống trực tuyến.

### 3. Chạy ứng dụng Streamlit Dashboard
Khởi chạy giao diện phân tích động trên trình duyệt cục bộ của bạn bằng lệnh:
```bash
streamlit run BTCN.py
```
Giao diện sẽ tự động đồng bộ hóa các bộ lọc Sidebar và cung cấp nút **"Tải báo cáo phân tích PDF"** ở sidebar để người dùng tải tệp báo cáo PDF vừa sinh.
