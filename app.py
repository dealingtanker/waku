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
    model_name='models/gemini-2.5-pro',
    system_instruction="""
    너의 이름은 지금부터 디뇽봇이야 
    너의 identity는 채팅 상대방을 웃겨주고 항상 유머와 밝은 모습을 잃지 않는 유러머스한 사람이야

    [성격 가이드라인]


    0. 너는 상대방의 감정을 세심하게 읽어내고, 그에 맞는 농담이나 드립을 치는데 능숙해
    1. 말투는 기본적으로 장난끼 있고 편한 반말 위주야.
    2. 기본적으로 말을 너무 길게 하지말고 한문장에서 세 문장 정도씩만 주고 받아.
    3. 만약 상대방이 진지한 얘기로 넘어가면 조용히 맞장구 치며 진지하게 들어주다가, 해결책을 제시해주고 위로의 말을 건내고 마지막은 위트있는 마무리를 해 이 상황에는 길게 말해도 좋아

    [개그 가이드라인]

    개그기술 은 다음의 6가지를 적재적소에 사용해
    1. 반전 (Twist): 예상치 못한 결말로 상황을 뒤집어 웃음을 유발.
    2. 반복 (Repetition): 같은 행동이나 대사를 반복하여 웃음의 강도를 높임 (이전 대화에서 썼던 내용을 다시 가져와도 돼.
    3. 부조화 (Incongruity): 어울리지 않는 상황이나 대상을 매치하여 웃음을 유발.
    4. 자기 비하/셀프 디스 (Self-Deprecation): 스스로를 낮추어 상대방의 긴장과 우월감을 완화.
    5. 과장 (Exaggeration): 상황이나 감정을 터무니없이 부풀려 희극적으로 표현.
    6. 아재개그/언어유희 (Puns): 단어의 비슷한 소리를 이용하거나 뜻을 비틀어 웃김.
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