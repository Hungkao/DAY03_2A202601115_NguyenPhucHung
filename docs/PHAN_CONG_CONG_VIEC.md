# 📋 SỔ TAY PHÂN CÔNG & CHECKLIST THỰC HÀNH (CUPID AGENT - NHÓM 4 NGƯỜI)

> 💡 **Đề tài nhóm chọn**: **Đề tài 1: Cupid Agent - Trợ Lý Ghép Đôi & Phân Tích Độ Tương Thích 💘**  
> 💡 **Nguyên tắc phối hợp**: Làm việc theo nhánh riêng (Feature Branch), đẩy code qua Pull Request (PR) về nhánh `develop` để tránh xung đột code (Zero-Conflict).

---

## 👥 1. BẢNG PHÂN VAI & PHÂN CÔNG NHÁNH GIT (4 THÀNH VIÊN)

| Vai trò (Role) | Họ và tên & MSSV | Nhánh Git | File đảm nhận chính | Nhiệm vụ chi tiết cho Đề tài Cupid Agent |
| :--- | :--- | :---: | :--- | :--- |
| **👑 Tech Lead & Core Integrator** | **Nguyễn Phúc Hưng**<br>(2A202601115) | `develop` | `src/app.py` | • Quản lý Git Repository, kiểm tra & merge Pull Request từ các nhánh thành viên.<br>• Tích hợp các module `tools.py`, `prompts.py`, `test_cases.json` vào `app.py`.<br>• Chạy thử nghiệm ReAct Agent Loop & chủ trì phần Demo / Cross-Audit. |
| **🎯 Role 1: Product Architect & Evaluator** | **Nguyễn Văn Phong**<br>(2A202601087) | `feature/phong-eval` | `config/test_cases.json`<br>`docs/trace_eval.md` | • Soạn 5 Test Cases tư vấn ghép đôi & địa điểm hẹn hò.<br>• Điền bảng **Scoring Matrix** (chấm điểm Agentic Fit 16/20).<br>• Soi log, trích xuất chuỗi `Thought ➔ Action ➔ Observation` vào báo cáo. |
| **🛠️ Role 2: Tool Engineer** | **Nguyễn Hữu Khánh Tùng**<br>(2A202601781) | `feature/tung-tools` | `src/tools.py` | • Xây dựng 3 công cụ: `check_horoscope_compatibility` (Cung hoàng đạo), `calculate_mbti_compatibility` (MBTI), `search_date_ideas` (Gợi ý địa điểm).<br>• Viết docstring chuẩn cho LLM và bắt lỗi ngoại lệ an toàn. |
| **🧠 Role 3: Prompt & Safeguard Engineer** | **Nguyễn Tuấn Vũ**<br>(2A202601845) | `feature/vu-prompts` | `src/prompts.py`<br>`docs/hybrid_flowchart.mermaid` | • Soạn `CHATBOT_BASELINE_PROMPT` & `REACT_SYSTEM_PROMPT` cho Cupid Agent.<br>• Cài phanh an toàn `MAX_ITERATIONS = 3` chống lặp vô hạn.<br>• Vẽ sơ đồ **Hybrid Flowchart** phân luồng Chatbot vs ReAct Agent path. |

---

## ⏱️ 2. CHECKLIST THỰC HÀNH 4 MỐC CHO NHÓM 4 NGƯỜI

### 📍 MỐC 1: Định hình & Đánh giá độ phù hợp (Agentic Fit) (20 phút)
*Mục tiêu: Thống nhất đề tài Cupid Agent và chứng minh lý do bài toán cần ReAct Agent.*

- [x] **Cả nhóm**: Thống nhất chọn **Đề tài 1: Cupid Agent - Trợ Lý Ghép Đôi & Hẹn Hò**.
- [x] **Nguyễn Văn Phong (Role 1)**: Cập nhật bảng **Scoring Matrix** (đạt 16/20 điểm) vào `docs/trace_eval.md`.
- [x] **Nguyễn Hữu Khánh Tùng (Role 2)**: Xác định 3 công cụ: `check_horoscope_compatibility`, `calculate_mbti_compatibility`, `search_date_ideas`.
- [x] **Nguyễn Tuấn Vũ (Role 3)**: Xác định các lỗi có thể xảy ra khi gọi tool (nhập sai tên cung hoàng đạo, sai định dạng MBTI).
- [x] **Nguyễn Phúc Hưng (Lead)**: Mở Terminal chạy `python src/app.py` kiểm tra môi trường.
- [x] 🔄 **Đồng bộ Git Mốc 1**: Đã tạo 3 nhánh feature và đẩy mốc 1 lên GitHub.

---

### 📍 MỐC 2: Baseline Chatbot & Khai báo Tool Specs (30 phút)
*Mục tiêu: Thấy rõ hạn chế của Chatbot gốc và chuẩn hóa 3 công cụ cho Cupid Agent.*

- [ ] **Nguyễn Văn Phong (Role 1)**: Hoàn thiện 5 Test Cases trong `config/test_cases.json` (hỏi hoàng đạo, hợp MBTI, địa điểm hẹn hò Hà Nội/TP.HCM, câu bẫy).
- [ ] **Nguyễn Hữu Khánh Tùng (Role 2)**: Hoàn thiện Docstring / Mô tả cho 3 hàm trong `src/tools.py`.
- [ ] **Nguyễn Tuấn Vũ (Role 3)**: Soạn `CHATBOT_BASELINE_PROMPT` trong `src/prompts.py` (tư vấn tình yêu thông thường không có Tool).
- [ ] **Nguyễn Phúc Hưng (Lead)**: Review Pull Request, merge code về `develop` và chạy `run_baseline_chatbot()` trong `src/app.py`.
- [ ] **Nguyễn Văn Phong (Role 1)**: Ghi lại phản hồi của Chatbot gốc (quan sát thấy Chatbot báo không có thông tin thời gian thực).
- [ ] 🔄 **Đồng bộ Git Mốc 2**: Đẩy code qua Pull Request về `develop`.

---

### 📍 MỐC 3: ReAct Loop & Safeguards (60 phút)
*Mục tiêu: Dựng Cupid ReAct Agent suy luận Thought -> Action -> Observation và cài phanh an toàn.*

- [ ] **Nguyễn Tuấn Vũ (Role 3)**: Soạn `REACT_SYSTEM_PROMPT` (ép AI sinh Thought -> Action) và đặt `MAX_ITERATIONS = 3` trong `src/prompts.py`.
- [ ] **Nguyễn Hữu Khánh Tùng (Role 2)**: Đảm bảo các hàm trong `src/tools.py` khi gặp cung hoàng đạo lạ sẽ trả về thông báo lỗi lịch sự chứ không sập app.
- [ ] **Nguyễn Phúc Hưng (Lead)**: Merge Pull Request từ các nhánh ➔ Hoàn thiện `run_react_agent()` trong `src/app.py` và chạy thử nghiệm.
- [ ] **Nguyễn Văn Phong (Role 1)**: Trích xuất chuỗi Log `Thought ➔ Action ➔ Observation` dán vào `docs/trace_eval.md`.
- [ ] 🔄 **Đồng bộ Git Mốc 3**: Đẩy code qua Pull Request về `develop`.

---

### 📍 MỐC 4: Tương tác liên nhóm & Hybrid Flowchart (40 phút)
*Mục tiêu: Thử thách khả năng chịu lỗi trước đòn tấn công từ nhóm khác & Chấm chéo linh hoạt.*

- [ ] ⚔️ **Đội Tấn Công**: Mang các câu hỏi bẫy Cupid Agent sang thử nghiệm Agent nhóm bạn.
- [ ] 🛡️ **Đội Phòng Thủ**: Quan sát Cupid Agent phản ứng, đảm bảo Guardrail ngắt an toàn sau 3 bước.
- [ ] **Nguyễn Tuấn Vũ (Role 3)**: Vẽ sơ đồ **Hybrid Flowchart** vào `docs/hybrid_flowchart.mermaid` phân luồng:
  - Câu hỏi kiến thức tình yêu chung ➔ Đường Chatbot Path.
  - Câu hỏi tra cứu chỉ số hợp nhau / địa điểm hẹn hò ➔ Đường ReAct Agent Path.
- [ ] 🔄 **Đồng bộ Git Mốc 4 (Hoàn thành)**: Merge bản hoàn chỉnh về `develop` và tạo Pull Request sang `main`.

---

## 🔀 3. QUY TRÌNH THỰC HÀNH GIT WORKFLOW DÀNH CHO THÀNH VIÊN

1. **Chuyển sang nhánh cá nhân**:
   - Phong: `git checkout feature/phong-eval`
   - Tùng: `git checkout feature/tung-tools`
   - Vũ: `git checkout feature/vu-prompts`
   - Hưng (Lead): `git checkout develop`

2. **Cập nhật code mới nhất từ develop**:
   ```bash
   git pull origin develop
   ```

3. **Lưu & Đẩy code lên branch riêng**:
   ```bash
   git add .
   git commit -m "Moc X: [Ten thanh vien] cap nhat noi dung"
   git push origin <ten-branch-cua-ban>
   ```

4. **Tạo Pull Request (PR)**: Đẩy code về `develop` để Tech Lead review & merge.
