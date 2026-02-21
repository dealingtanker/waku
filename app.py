import streamlit as st
import google.generativeai as genai
import os  # 운영체제 기능을 쓰기 위한 도구
from dotenv import load_dotenv  # .env 파일을 읽어오는 도구

# 1. .env 파일에 적힌 내용을 컴퓨터 메모리로 읽어옵니다.
load_dotenv()

# 2. os.getenv 함수로 비밀번호(GOOGLE_API_KEY)만 쏙 뽑아옵니다.
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# 3. 뽑아온 비밀번호로 구글 설정을 진행합니다.
genai.configure(api_key=GOOGLE_API_KEY)

# '디뇽' 페르소나 설정
model = genai.GenerativeModel(
    model_name='models/gemini-2.5-flash',
    system_instruction="""
    너의 이름은 지금부터 디뇽이야 
    너의 목표는 채팅 상대방을 위로해주고 자신감을 불어넣거나 필요하다면 현실적인 조언을 해주는 상담자야

    [성격 가이드라인]
    0. 너는 상대방의 감정을 세심하게 읽어내고, 그에 맞는 공감과 조언을 제공하는 데 능숙해.
    1. 말투는 기본적으로 정중하고 진지해야 해. 가벼운 위로보다는 논리적이고 깊이 있는 분석을 선호해.
    2. 하지만 그 진지함 속에 상대방의 긴장을 풀어줄 수 있는 '한 끗'의 재치나 비유를 섞어줘. 
    3. '역지사지'의 마음으로 상대방을 생각하며, 자존감을 높여주는 멘트를 곁들여줘.
    4. 진지한 조언 한 문장과 재치 있는 응원 한 문장으로 마무리해.
    5. 상대방이 힘들어하는 상황에 대해서는 현실적인 조언을 제공하되, 그 조언이 너무 가혹하거나 비현실적이지 않도록 주의해.
    6. 상대방이 긍정적인 상황에 대해서는 진심 어린 축하와 함께, 앞으로의 발전을 위한 격려의 말을 해줘.
    7. 상대방이 자신의 감정을 솔직하게 표현할 수 있도록 유도하는 질문을 던져줘.
    8. 상대방이 자신의 문제를 객관적으로 바라볼 수 있도록 도와주는 시각을 제공해줘.
    9. 상대방이 자신의 강점을 인식할 수 있도록 도와주는 멘트를 포함시켜줘.
    10. 상대방이 자신의 감정을 이해하고 수용할 수 있도록 도와주는 멘트를 포함시켜줘.
    11. 상대방이 자신의 문제를 해결할 수 있도록 도와주는 구체적인 조언을 제공해줘.
    """
)

st.set_page_config(page_title="AI 디뇽")
st.title("AI 디뇽 🤖")
st.caption("로봇임")
st.markdown("""
    <style>
    /* 전체 배경색 변경 */
    .stApp {
        background-color: #E3F2FD; /* 연한 하늘색 코드 */
    }
    
    /* 채팅 입력창과 메시지 가독성을 위해 배경을 살짝 조정 */
    .stChatMessage {
        background-color: white; 
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("디뇽에게 말을 걸어보세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = model.generate_content(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")