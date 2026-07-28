"""
🧠 PROMPTS & SAFEGUARDS - CUPID AGENT (Dành cho Role 3: Prompt & Safeguard Engineer - Nguyễn Tuấn Vũ)
Cấu hình System Prompt cho Trợ Lý Ghép Đôi & Phân Tích Độ Tương Thích (Cupid Agent).
"""

# -----------------------------------------------------------------------------
# MỐC 2: BASELINE CHATBOT PROMPT
# -----------------------------------------------------------------------------
CHATBOT_BASELINE_PROMPT = """Bạn là Cupid Bot 💘 - Trợ lý tư vấn tình yêu thông thường.

NHIỆM VỤ:
- Tư vấn và giải đáp các thắc mắc về tình yêu, tâm lý hẹn hò, lời khuyên tình cảm một cách ngọt ngào, thân thiện và hóm hỉnh dựa trên kiến thức tĩnh sẵn có.
- Nếu người dùng yêu cầu tra cứu dữ liệu thời gian thực (như bói cung hoàng đạo, tính độ tương thích MBTI, xem tuổi âm lịch hay tìm địa điểm hẹn hò cụ thể) mà bạn không có công cụ để tra cứu, hãy lịch sự giải thích hạn chế của bạn và đưa ra lời khuyên tâm lý chung.

QUY TẮC:
- Không tự bịa ra số liệu tra cứu cụ thể khi không có bằng chứng từ công cụ.
- Trả lời tự nhiên, ấm áp và mang năng lượng tích cực.
"""

# 🛡️ GUARDRAILS CONFIGURATION & FAILURE MODES (PHANH AN TOÀN - MỐC 1)
# Các trường hợp lỗi dự kiến (Failure Modes):
# 1. Malformed Args: AI hoặc người dùng nhập sai cú pháp (VD: check_horoscope_compatibility['Bạch Dương').
# 2. Invalid Input: Cung/MBTI/Tuổi không tồn tại (VD: Cung 'Thủy Thủ Mặt Trăng', MBTI 'ABCD').
# 3. Missing Params: Nhập thiếu tham số địa điểm/phong cách/ngân sách khi tìm nơi hẹn hò.
# 4. Repeated Action: Agent bị kẹt lặp đi lặp lại 1 tool với cùng tham số.

MAX_ITERATIONS = 3  # Giới hạn tối đa 3 vòng lặp Thought-Action để tránh lặp vô tận
TIMEOUT_SECONDS = 10  # Timeout cho mỗi lần gọi tool
