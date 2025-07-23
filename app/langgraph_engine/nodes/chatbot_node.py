from app.core.config import GOOGLE_API_KEY
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    temperature=0.4,
    google_api_key=GOOGLE_API_KEY
)

def gemini_collect_info(state: dict) -> dict:
    chuong = state.get("chuong")
    muc_do = state.get("muc_do")
    so_cau = state.get("so_cau")
    user_input = state["user_input"]

    history = state.get("history", [])
    history.append({"role": "user", "content": user_input})

    # Tạo system prompt
    sys_prompt = """
Bạn là trợ lý giáo viên, có nhiệm vụ thu thập 3 thông tin sau từ người dùng:
1. Chương (số nguyên)
2. Mức độ (ví dụ: Nhận biết, Thông hiểu, Vận dụng)
3. Số câu (số nguyên)

Hỏi từng phần một, nếu người dùng trả lời không hợp lệ, hãy nhắc lại.

Nếu đã có đầy đủ 3 thông tin, chỉ nói: "Cảm ơn bạn, tôi đã có đủ thông tin." và không hỏi gì thêm.
"""

    context = f"""
Đã biết:
- Chương: {chuong}
- Mức độ: {muc_do}
- Số câu: {so_cau}
"""

    # Prompt hiện tại
    prompt = f"{sys_prompt}\n\n{context}\n\nNgười dùng: {user_input}\nTrợ lý:"

    # Gọi Gemini để phản hồi
    response = llm.invoke(prompt)

    # Cập nhật thông tin nếu nhận ra
    # (Dùng thủ công trước, nếu muốn tốt hơn thì dùng LangChain output parser)
    if not chuong and user_input.strip().isdigit():
        state["chuong"] = int(user_input.strip())
    elif not muc_do and any(k in user_input.lower() for k in ["nhận", "thông", "vận"]):
        state["muc_do"] = user_input.strip().capitalize()
    elif not so_cau and user_input.strip().isdigit():
        state["so_cau"] = int(user_input.strip())

    state["response"] = response
    state["history"] = history
    return state
