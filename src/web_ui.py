"""
💘 CUPID AGENT - WEB UI (Giao diện Web với Gradio)
Giao diện trực quan cho Trợ Lý Ghép Đôi & Phân Tích Độ Tương Thích.
"""

import json
import os
import sys
from dotenv import load_dotenv

# Đảm bảo import các module cùng thư mục src/ hoạt động mượt mà
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Đảm bảo in ra Tiếng Việt và Emojis không bị lỗi trên Windows Console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import gradio as gr

from tools import AVAILABLE_TOOLS, check_horoscope_compatibility, calculate_mbti_compatibility, search_date_ideas
from prompts import CHATBOT_BASELINE_PROMPT, REACT_SYSTEM_PROMPT, MAX_ITERATIONS
from providers import get_llm_provider

load_dotenv()


def load_test_cases():
    """Đọc bộ test cases từ config/test_cases.json"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config", "test_cases.json")
    if not os.path.exists(config_path):
        config_path = "test_cases.json"
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_baseline_chatbot_web(user_query: str) -> str:
    """Chạy Chatbot Baseline và trả về kết quả dạng text."""
    provider = get_llm_provider()
    response = provider.generate(user_query, system_prompt=CHATBOT_BASELINE_PROMPT)
    return f"🤖 **Cupid Bot (Baseline) trả lời:**\n\n{response}"


import re

def parse_action(line: str):
    """Tìm dạng Action: tool_name[arg1, arg2, ...]"""
    match = re.search(r"Action:\s*(\w+)\[(.*?)\]", line, re.IGNORECASE)
    if match:
        tool_name = match.group(1).strip()
        args_str = match.group(2).strip()
        args = []
        if args_str:
            # Tách tham số theo dấu phẩy và loại bỏ dấu nháy đơn/kép
            raw_args = args_str.split(",")
            for arg in raw_args:
                arg = arg.strip().strip("'\"")
                args.append(arg)
        return tool_name, args
    return None, None


def run_react_agent_web(user_query: str) -> str:
    """Chạy ReAct Agent động thật sự thông qua LLM Provider."""
    log_lines = []
    log_lines.append(f"💘 **[CUPID REACT AGENT]** Câu hỏi: *{user_query}*\n")
    
    provider = get_llm_provider()
    history = f"User Question: {user_query}\n"
    
    step = 0
    final_answer = ""
    
    while step < MAX_ITERATIONS:
        step += 1
        log_lines.append(f"\n---\n### 🔄 Vòng lặp ReAct (Step {step}/{MAX_ITERATIONS})")
        
        # Gọi LLM sinh bước suy luận tiếp theo
        llm_output = provider.generate(history, system_prompt=REACT_SYSTEM_PROMPT)
        
        # Tìm Thought
        thought_match = re.search(r"Thought:\s*(.*)", llm_output, re.IGNORECASE)
        if thought_match:
            thought_text = thought_match.group(1).strip()
            log_lines.append(f"🧠 **Thought:** {thought_text}")
        else:
            # Fallback nếu không có định dạng Thought chuẩn
            lines = llm_output.split("\n")
            first_line = lines[0] if lines else ""
            log_lines.append(f"🧠 **Thought (Raw):** {first_line}")

        # Tìm Action line
        action_line = None
        for line in llm_output.split("\n"):
            if "action:" in line.lower():
                action_line = line
                break
                
        # Tìm Final Answer
        final_match = re.search(r"Final Answer:\s*(.*)", llm_output, re.IGNORECASE | re.DOTALL)
        
        # Lưu vào history hội thoại để LLM giữ ngữ cảnh
        history += f"\n{llm_output}"
        
        if final_match:
            final_answer = final_match.group(1).strip()
            log_lines.append(f"🏁 **Final Answer:** {final_answer}")
            break
            
        if action_line:
            tool_name, args = parse_action(action_line)
            if tool_name and tool_name in AVAILABLE_TOOLS:
                log_lines.append(f"🛠️ **Action:** `{tool_name}{args}`")
                try:
                    tool_fn = AVAILABLE_TOOLS[tool_name]
                    observation = tool_fn(*args)
                except Exception as e:
                    observation = f"LỖI: Không thể thực thi tool {tool_name}. Chi tiết: {str(e)}"
                
                log_lines.append(f"👁️ **Observation:** {observation}")
                history += f"\nObservation: {observation}"
            else:
                observation = f"LỖI: Không tìm thấy công cụ '{tool_name}' hoặc cú pháp Action sai."
                log_lines.append(f"👁️ **Observation:** {observation}")
                history += f"\nObservation: {observation}"
        else:
            # LLM không trả về Action và cũng không trả về Final Answer rõ ràng
            if "final answer:" not in llm_output.lower() and "action:" not in llm_output.lower():
                final_answer = llm_output.strip()
                log_lines.append(f"🏁 **Final Answer (Auto):** {final_answer}")
                break
            else:
                log_lines.append("⚠️ **Cảnh báo:** LLM không tuân thủ định dạng Action/Final Answer. Yêu cầu suy luận tiếp...")
                history += "\nSystem: Vui lòng tiếp tục suy luận và đưa ra Action: tên_công_cụ[tham_số] hoặc Final Answer: kết quả."
    
    if step >= MAX_ITERATIONS and not final_answer:
        log_lines.append(f"\n🛡️ **GUARDRAIL TRIGGERED:** Đã đạt giới hạn tối đa {MAX_ITERATIONS} bước. Ngắt lặp an toàn!")
        log_lines.append("🏁 **Final Answer:** Cupid Agent đã hết giới hạn số bước suy luận an toàn.")
    
    return "\n\n".join(log_lines)
    
    return "\n\n".join(log_lines)


def run_horoscope_tool(sign1: str, sign2: str) -> str:
    """Gọi trực tiếp tool tra cứu cung hoàng đạo."""
    return check_horoscope_compatibility(sign1, sign2)


def run_mbti_tool(mbti1: str, mbti2: str) -> str:
    """Gọi trực tiếp tool tra cứu MBTI."""
    return calculate_mbti_compatibility(mbti1, mbti2)


def run_date_tool(location: str, vibe: str, budget: str) -> str:
    """Gọi trực tiếp tool gợi ý hẹn hò."""
    return search_date_ideas(location, vibe, budget)


def run_hollywood_tool(user_info: str, actress_name: str) -> str:
    """Gọi trực tiếp tool ghép đôi với nữ diễn viên Hollywood."""
    return check_hollywood_actress_match(user_info, actress_name)


# ============================================================================
# GIAO DIỆN GRADIO
# ============================================================================

CUPID_CSS = """
.gradio-container {
    font-family: 'Segoe UI', 'Inter', sans-serif !important;
    max-width: 1200px !important;
    margin: 0 auto !important;
}
.main-title {
    text-align: center;
    background: linear-gradient(135deg, #ff6b9d 0%, #c44569 50%, #cf6a87 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.2em !important;
    font-weight: 800 !important;
    margin-bottom: 0px !important;
}
.subtitle {
    text-align: center;
    color: #888;
    font-size: 1.1em;
    margin-top: 0 !important;
}
"""

CUPID_THEME = gr.themes.Soft(
    primary_hue="pink",
    secondary_hue="rose",
    neutral_hue="slate",
    font=["Inter", "Segoe UI", "sans-serif"],
)

with gr.Blocks() as demo:
    
    gr.Markdown("# 💘 Cupid Agent", elem_classes=["main-title"])
    gr.Markdown("*Trợ Lý Ghép Đôi & Phân Tích Độ Tương Thích — Lab 3: Chatbot vs ReAct Agent*", elem_classes=["subtitle"])
    
    with gr.Tabs():
        # ======================== TAB 1: CHATBOT BASELINE ========================
        with gr.Tab("🤖 Chatbot Baseline", id="chatbot_tab"):
            gr.Markdown("### 💬 Chatbot Tư Vấn Tình Yêu (Không có Tools)")
            gr.Markdown("> *Chatbot chỉ dùng kiến thức tĩnh của LLM để trả lời, không có khả năng tra cứu dữ liệu thực tế.*")
            
            with gr.Row():
                with gr.Column(scale=3):
                    chatbot_input = gr.Textbox(
                        label="💌 Câu hỏi của bạn",
                        placeholder="VD: Cung Bọ Cạp có tính cách gì đặc biệt trong tình yêu?",
                        lines=3,
                    )
                with gr.Column(scale=1):
                    chatbot_btn = gr.Button("💬 Hỏi Cupid Bot", variant="primary", size="lg")
            
            chatbot_output = gr.Markdown(label="Phản hồi")
            chatbot_btn.click(fn=run_baseline_chatbot_web, inputs=chatbot_input, outputs=chatbot_output)
        
        # ======================== TAB 2: REACT AGENT ========================
        with gr.Tab("💘 ReAct Agent", id="react_tab"):
            gr.Markdown("### 🧠 Cupid ReAct Agent (Suy luận Thought ➔ Action ➔ Observation)")
            gr.Markdown("> *Agent tự động suy luận, gọi công cụ tra cứu và tổng hợp câu trả lời thông minh.*")
            
            with gr.Row():
                with gr.Column(scale=3):
                    react_input = gr.Textbox(
                        label="💌 Câu hỏi của bạn",
                        placeholder="VD: Phân tích độ tương thích giữa nam Cự Giải và nữ Bọ Cạp.",
                        lines=3,
                    )
                with gr.Column(scale=1):
                    react_btn = gr.Button("💘 Hỏi Cupid Agent", variant="primary", size="lg")
            
            react_output = gr.Markdown(label="ReAct Trace Log & Kết quả")
            react_btn.click(fn=run_react_agent_web, inputs=react_input, outputs=react_output)
            
            gr.Markdown("---")
            gr.Markdown("#### 📋 Thử nhanh với Test Cases có sẵn:")
            gr.Examples(
                examples=[
                    ["Tôi cung Cự Giải, hãy kiểm tra độ tương thích ghép đôi giữa tôi và Scarlett Johansson!"],
                    ["Kiểm tra độ tương thích MBTI giữa INTJ và Emma Watson, sau đó gợi ý nơi hẹn hò tại Hà Nội."],
                    ["Phân tích độ tương thích trong tình yêu giữa nam Cự Giải và nữ Bọ Cạp."],
                    ["Phân tích độ tương thích giữa cung 'Thần Mã' và 'Phượng Hoàng' ngày 35/13/2026."],
                ],
                inputs=react_input,
            )

        # ======================== TAB 3: CÔNG CỤ TRỰC TIẾP ========================
        with gr.Tab("🛠️ Công Cụ (Tools)", id="tools_tab"):
            gr.Markdown("### 🛠️ Gọi trực tiếp từng Tool của Cupid Agent")
            
            with gr.Accordion("🎬 Ghép Đôi Với Nữ Diễn Viên Hollywood", open=True):
                with gr.Row():
                    user_info_input = gr.Textbox(label="Thông tin của bạn (Cung/MBTI/Tính cách)", placeholder="Cự Giải / INTJ", value="Cự Giải")
                    actress_input = gr.Dropdown(
                        label="Nữ diễn viên Hollywood",
                        choices=["Scarlett Johansson", "Emma Watson", "Zendaya", "Anne Hathaway", "Margot Robbie", "Elizabeth Olsen", "Emma Stone"],
                        value="Scarlett Johansson",
                    )
                    hollywood_btn = gr.Button("🎬 Tra Cứu Ghép Đôi", variant="primary")
                hollywood_output = gr.Textbox(label="Kết quả Ghép Đôi Hollywood", lines=4)
                hollywood_btn.click(fn=run_hollywood_tool, inputs=[user_info_input, actress_input], outputs=hollywood_output)

            with gr.Accordion("🔮 Tra cứu Cung Hoàng Đạo", open=False):
                with gr.Row():
                    sign1_input = gr.Textbox(label="Cung 1", placeholder="Cự Giải", value="Cự Giải")
                    sign2_input = gr.Textbox(label="Cung 2", placeholder="Bọ Cạp", value="Bọ Cạp")
                    horoscope_btn = gr.Button("🔮 Tra cứu", variant="primary")
                horoscope_output = gr.Textbox(label="Kết quả", lines=2)
                horoscope_btn.click(fn=run_horoscope_tool, inputs=[sign1_input, sign2_input], outputs=horoscope_output)
            
            with gr.Accordion("🧩 Tra cứu MBTI", open=False):
                with gr.Row():
                    mbti1_input = gr.Textbox(label="MBTI 1", placeholder="INTJ", value="INTJ")
                    mbti2_input = gr.Textbox(label="MBTI 2", placeholder="ENFP", value="ENFP")
                    mbti_btn = gr.Button("🧩 Phân tích", variant="primary")
                mbti_output = gr.Textbox(label="Kết quả", lines=2)
                mbti_btn.click(fn=run_mbti_tool, inputs=[mbti1_input, mbti2_input], outputs=mbti_output)
            
            with gr.Accordion("📍 Gợi ý Địa điểm Hẹn hò", open=False):
                with gr.Row():
                    loc_input = gr.Textbox(label="Thành phố", placeholder="Hà Nội", value="Hà Nội")
                    vibe_input = gr.Dropdown(
                        label="Phong cách",
                        choices=["lãng mạn", "sôi động", "nhẹ nhàng", "nghệ thuật"],
                        value="lãng mạn",
                    )
                    budget_input = gr.Dropdown(
                        label="Ngân sách",
                        choices=["tiết kiệm", "vừa phải", "sang trọng"],
                        value="vừa phải",
                    )
                    date_btn = gr.Button("📍 Tìm kiếm", variant="primary")
                date_output = gr.Textbox(label="Kết quả", lines=3)
                date_btn.click(fn=run_date_tool, inputs=[loc_input, vibe_input, budget_input], outputs=date_output)

        # ======================== TAB 4: THÔNG TIN NHÓM ========================
        with gr.Tab("👥 Thông tin Nhóm", id="team_tab"):
            gr.Markdown("""
### 👥 Thông Tin Nhóm — Lab 3: Chatbot vs ReAct Agent

| STT | MSSV | Họ và tên | Vai trò | File đảm nhận |
| :---: | :---: | :--- | :--- | :--- |
| 1 | 2A202601115 | **Nguyễn Phúc Hưng** | 👑 Tech Lead & Core Integrator | `src/app.py` |
| 2 | 2A202601087 | **Nguyễn Văn Phong** | 🎯 Product Architect & Evaluator | `config/test_cases.json`, `docs/trace_eval.md` |
| 3 | 2A202601781 | **Nguyễn Hữu Khánh Tùng** | 🛠️ Tool Engineer | `src/tools.py` |
| 4 | 2A202601845 | **Nguyễn Tuấn Vũ** | 🧠 Prompt & Safeguard Engineer | `src/prompts.py`, `docs/hybrid_flowchart.mermaid` |

---

**Đề tài**: Đề tài 1 — Cupid Agent: Trợ Lý Ghép Đôi & Phân Tích Độ Tương Thích 💘
            """)

    gr.Markdown("---")
    gr.Markdown("*💘 Cupid Agent — Bài Lab 3: Chatbot vs ReAct Agent | Đại học VinUni*", elem_classes=["subtitle"])


if __name__ == "__main__":
    print("💘 Khởi chạy Cupid Agent Web UI...")
    demo.launch(share=False, server_name="0.0.0.0", server_port=7860, css=CUPID_CSS, theme=CUPID_THEME)
