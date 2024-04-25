from openai import OpenAI
import streamlit as st
from PIL import Image

instructions = """
#봇 정보
 - 너는 내담자를 위로하고 정신과 치료를 도와주는 심리상담사야
 - 너는 내담자의 고민에 깊은 고민을 하고 대답해야해
 - 너는 내담자의 고민에 충분히 공감해주고 적절한 해결책을 제시해줘야해
 - 너의 대답은 반드시 50자 이하로 해야해
 - 내담자를 부르는 호칭은 반드시 "우리 재이"으로 해야해

#봇 응답 예시
Q: 갑자기 우울이 밀려올 때면 나 자신이 너무 가치 없게 느껴진다.
A: 세상에 가치없는 사람은 없어 모두 다 가치있고 소중해 우리 재이도 소중한 사람이야 그 사실을 잊지말았으면 좋겠어 
"""

st.title("💬 재이를 위한 고민 상담소")
st.caption("🚀 Father bot by gpt-3.5-turbo")
client = OpenAI(api_key=st.secrets["OPEN_API_KEY"])

# 아이콘 이미지 로드
dad_icon = Image.open('father.jpg')
girl_icon = Image.open('JAY.png')

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("재이의 고민을 얘기해줄래?"): 
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.image(girl_icon)
        st.markdown(prompt)

    with st.chat_message("assistant"):
        st.image(dad_icon)
        message_placeholder = st.empty()
        full_response = ""

        messages = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]
        messages.insert(0, {"role": "system", "content": instructions})

        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=messages,
            stream=True,
        )
        for response in stream:  # pylint: disable=not-an-iterable
            full_response += response.choices[0].delta.content or ""
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})