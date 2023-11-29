import openai
import streamlit as st

# 設定 OpenAI API
openai.api_type = ""
openai.api_base = ""
openai.api_version = ""
openai.api_key = ""

# 初始化 Session State
if "chat_rooms" not in st.session_state:
    st.session_state.chat_rooms = {}
if "selected_chat_room" not in st.session_state:
    st.session_state.selected_chat_room = None
if "messages" not in st.session_state:
    st.session_state.messages = {}

# 側邊欄：創建和選擇聊天室
with st.sidebar:
    st.title("聊天室")
    chat_room_name = st.text_input("創建新聊天室：")
    if st.button("創建"):
        if chat_room_name and chat_room_name not in st.session_state.chat_rooms:
            st.session_state.chat_rooms[chat_room_name] = True
            st.session_state.messages[chat_room_name] = []
            st.session_state.selected_chat_room = chat_room_name
        elif chat_room_name:
            st.warning("聊天室名稱已存在")

    st.title("選擇現有聊天室：")
    for room in st.session_state.chat_rooms.keys():
        if st.button(room):
            st.session_state.selected_chat_room = room

# 主頁面：聊天室
if st.session_state.selected_chat_room:
    st.title("💬大林慈濟恰特GPT")
    st.header(f"聊天室：{st.session_state.selected_chat_room}")
    selected_room = st.session_state.selected_chat_room
    if selected_room not in st.session_state.messages:
        st.session_state.messages[selected_room] = []
    # 顯示對話記錄
    for msg in st.session_state.messages.get(selected_room, []):
        st.chat_message(msg["role"]).write(msg["content"])

    # 處理使用者輸入
    user_input = st.chat_input()
    if user_input:
        # 確保當前聊天室的對話記錄是列表
        if selected_room not in st.session_state.messages:
            st.session_state.messages[selected_room] = []
        st.chat_message("user").write(user_input)
        # 更新當前聊天室的對話記錄
        st.session_state.messages[selected_room].append({"role": "user", "content": user_input})

        # 僅使用最新的用戶輸入和之前的回應構建對話歷史
        chat_history = [{"role": "system", "content": "The following is a conversation with an AI assistant."}]
        if len(st.session_state.messages[selected_room]) > 1:
            chat_history.append(st.session_state.messages[selected_room][-2])
        chat_history.append({"role": "user", "content": user_input})
        try:
            # 調用 OpenAI API
            response = openai.ChatCompletion.create(
                engine="dalintzuchi",
                messages=chat_history,
                temperature=0.7,
                max_tokens=800,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None
            )

            # 處理回應
            answer = response['choices'][0]['message']['content']
            st.session_state.messages[selected_room].append({"role": "assistant", "content": answer})
            st.chat_message("assistant").write(answer)
        except Exception as e:
            st.error(f"發生問題：{e}")
else:
    st.title("請從側邊欄選擇或創建一個聊天室。")