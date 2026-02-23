import streamlit as st
import openai

st.set_page_config(page_title="DeepSeek AI 聊天", page_icon="🤖")
st.title("🤖 DeepSeek AI 聊天机器人")

# 侧边栏设置
with st.sidebar:
    st.header("设置")
    api_key = st.text_input("DeepSeek API Key", type="password")
    st.markdown("[获取API Key](https://platform.deepseek.com/api_keys)")
    
    if st.button("检查连接"):
        if api_key:
            try:
                # 使用旧版API方式
                openai.api_key = api_key
                openai.api_base = "https://api.deepseek.com/v1"
                
                # 简单测试
                response = openai.ChatCompletion.create(
                    model="deepseek-chat",
                    messages=[{"role": "user", "content": "ping"}],
                    max_tokens=5
                )
                st.success("✅ 连接成功！")
            except Exception as e:
                st.error(f"❌ 连接失败: {str(e)[:50]}...")

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
        
        try:
            # 设置API
            openai.api_key = api_key
            openai.api_base = "https://api.deepseek.com/v1"
            
            # 准备消息历史
            messages = [{"role": "system", "content": "你是一个友好的AI助手"}] + st.session_state.messages[-10:]
            
            # 调用API（非流式，避免兼容性问题）
            response = openai.ChatCompletion.create(
                model="deepseek-chat",
                messages=messages,
                stream=False,
                temperature=0.7
            )
            
            full_response = response.choices[0].message.content
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            full_response = f"错误: {str(e)}"
            message_placeholder.markdown(full_response)
        
        # 保存AI回复
        st.session_state.messages.append({"role": "assistant", "content": full_response})
