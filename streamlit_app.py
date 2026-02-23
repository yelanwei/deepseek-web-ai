import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="DeepSeek AI 聊天", page_icon="🤖")
st.title("🤖 DeepSeek AI 聊天机器人")

# 侧边栏输入API Key
with st.sidebar:
    st.header("设置")
    api_key = st.text_input("DeepSeek API Key", type="password")
    st.markdown("[获取API Key](https://platform.deepseek.com/api_keys)")
    
    if st.button("检查连接"):
        if api_key:
            try:
                client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")
                st.success("✅ 连接成功！")
            except:
                st.error("❌ 连接失败")

# 初始化聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 聊天输入
if prompt := st.chat_input("说点什么..."):
    if not api_key:
        st.error("请在侧边栏输入API Key")
        st.stop()
    
    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 获取AI回复
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "system", "content": "你是一个友好的AI助手"}] + st.session_state.messages[-10:],
            stream=True
        )
        
        for chunk in response:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
