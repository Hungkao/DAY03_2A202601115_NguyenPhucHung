# 👥 DANH SÁCH THÀNH VIÊN VÀ PHÂN CÔNG NHÓM (LAB 3 - RE-ACT AGENT)

## 📋 THÔNG TIN NHÓM

| STT | MSSV | Họ và tên | Vai trò | File đảm nhận chính | Nhiệm vụ chính |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **1** | **2A202601115** | **Nguyễn Phúc Hưng** | **Tech Lead & Core Integrator** | `src/app.py` | • Quản lý Git Repository (`develop`, `main`), duyệt code & phân công.<br>• Tích hợp các module (`tools.py`, `prompts.py`, `test_cases.json`) vào `app.py`.<br>• Chạy thử nghiệm ReAct Agent Loop & làm đầu mối Demo / Cross-Audit. |
| **2** | **2A202601087** | **Nguyễn Văn Phong** | **Product Architect & Evaluator** | `config/test_cases.json`<br>`docs/trace_eval.md` | • Định hướng bài toán thực tế cho Agent.<br>• Xây dựng 5 Test Cases (Đơn giản, Multi-step, Edge case).<br>• Đánh giá Scoring Matrix & trích xuất Trace Log (`Thought -> Action -> Observation`). |
| **3** | **2A202601781** | **Nguyễn Hữu Khánh Tùng** | **Tool Engineer** | `src/tools.py` | • Định nghĩa và phát triển các hàm Tool cho Agent.<br>• Viết docstring/description chuẩn xác để LLM dễ nhận diện Tool.<br>• Xử lý ngoại lệ (tránh crash ứng dụng khi Tool bị lỗi). |
| **4** | **2A202601845** | **Nguyễn Tuấn Vũ** | **Prompt & Safeguard Engineer** | `src/prompts.py`<br>`docs/hybrid_flowchart.mermaid` | • Soạn `CHATBOT_BASELINE_PROMPT` và `REACT_SYSTEM_PROMPT` (ép AI suy luận Thought ➔ Action).<br>• Thiết lập Guardrails (`MAX_ITERATIONS`, phanh an toàn chống lặp vô hạn).<br>• Vẽ sơ đồ phân luồng **Hybrid Flowchart** (Chatbot Path vs ReAct Agent Path). |

---

## ⏱️ QUI TRÌNH LÀM VIỆC DÀNH CHO CÁC THÀNH VIÊN

1. **Trước khi thực hiện công việc**:
   ```bash
   git pull origin develop
   ```

2. **Sau khi hoàn thành công việc tại mỗi Mốc**:
   ```bash
   git add .
   git commit -m "Moc X: [Tên thành viên] - [Nội dung cập nhật]"
   git push origin develop
   ```
