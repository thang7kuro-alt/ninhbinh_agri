# --- Chức năng 6: Khung Chat hỏi đáp với Gemini ---
st.subheader("6. Chat với Gemini 💬")

# Lưu lịch sử hội thoại (Session state)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Không tìm thấy Khóa API 'GEMINI_API_KEY'. Vui lòng cấu hình trong Streamlit Secrets.")
else:
    client = genai.Client(api_key=api_key)
    model_name = "gemini-2.5-flash"

    # Hiển thị khung chat
    user_input = st.chat_input("Nhập câu hỏi hoặc yêu cầu của bạn...")

    if user_input:
        # Gửi tin nhắn người dùng
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        # Gọi Gemini trả lời
        with st.chat_message("assistant"):
            with st.spinner("Gemini đang trả lời..."):
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=user_input
                    )
                    ai_reply = response.text
                except Exception as e:
                    ai_reply = f"⚠️ Lỗi khi gọi Gemini: {e}"

                st.markdown(ai_reply)
                st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})

    # Hiển thị lại toàn bộ hội thoại
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

