import openai
import streamlit as st
import os
import utils as utl
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.question_answering import load_qa_chain
from youtube_transcript import YT_transcript
from chunk import chunking
IFRAME = '<iframe src="https://ghbtns.com/github-btn.html?user=KaziArman&repo=ask-youtube&type=star&count=true&size=large" frameborder="0" scrolling="0" width="170" height="30" title="GitHub"></iframe>'

ss = st.session_state
st.set_page_config(
	page_icon="https://i.pinimg.com/originals/4b/85/c9/4b85c95c93eff810b0fe0a755be081a6.png",
	#page_icon="web.png",
	layout="wide",
	page_title='Ask Youtube',
	initial_sidebar_state="expanded"
)

st.markdown(f'<div class="header"><figure style="background-color: #FFFFFF;"><img src="https://i.pinimg.com/originals/41/f6/4d/41f64d3b4b21cb08eb005b11016bf707.png" width="400" style="display: block; margin: 0 auto; background-color: #FFFFFF;"><figcaption></figcaption></figure><h4 style="text-align: center"> Ask Youtube is a conversional AI based tool, where you can ask about any youtube video and it will answer  {IFRAME}</h4></div>', unsafe_allow_html=True)
#st.markdown(f'<div class="header"><figure><img src="logo.png" width="500"><figcaption><h1>Welcome to Ask Youtube</h1></figcaption></figure><h3>Ask Youtube is a conversional AI based tool, where you can ask about any youtube video and it will answer.</h3></div>', unsafe_allow_html=True)

with st.expander("How to use Ask Youtube 🤖", expanded=False):
	st.markdown(
		"""
		Please refer to [our dedicated guide](https://www.impression.co.uk/resources/tools/oapy/) on how to use Ask Youtube.
		"""
    )

with st.sidebar.expander("Credits 🏆", expanded=True):
	st.markdown(
		"""Ask Youtube was created by [Kazi Arman Ahmed](https://www.linkedin.com/in/r4h4t/) and [Md Shamim Hasan](https://www.linkedin.com/in/md-shamim-hasan/)  at [LandQuire](https://www.linkedin.com/company/landquire/) in Bangladesh 
	    """
    )
def on_btn_click():
    del st.session_state["messages"]
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi, I am an AI bot created by LandQuire Data Team\nHow can I help you regarding this YouTube video?"}]


api_key = st.sidebar.text_input('Enter your API key')

youtube_link = st.sidebar.text_input('Enter your YouTube video link')
temp_slider = st.sidebar.slider('Set the temperature of the completion. Higher values make the output more random,  lower values make it more focused.', 0.0, 1.0, 0.7)
st.sidebar.button("Clear messages", use_container_width=True,on_click=on_btn_click)
summarize = st.sidebar.button("Summarize", use_container_width=True)
chatgpt = st.sidebar.checkbox('Use ChatGPT', False,
			help='Allow the bot to collect answers to any specific questions from outside of the video content')

def youtube(link,key):
    openai.api_key = key
    os.environ["OPENAI_API_KEY"] = key
    ll = link
    yt_script = YT_transcript(link)
    transcript = yt_script.script()
    text = """\n\n\nPlease briefly summarize this YouTube video in 2-3 concise paragraphs.
            First, analyze the video line-by-line, distilling each line into a simple summary sentence.
           Then combine these sentence summaries into a short summary covering the key points. 
           Please make sure to accurately capture the essence and meaning of the video content.
           I will ask some questions about the video - please answer them precisely with relevant details from the summary you generated.
           Aim for answers that are around 50 lines long.
           The goal is for your summary to allow me to get the key information from the video without watching it, and have enough detail to answer specific questions"""

    transcript = transcript + text
    chnk = chunking(transcript)
    chunks = chnk.yt_data()
    # Get embedding model
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(chunks, embeddings)
    return db



st.write('### Ask Questions')
chat = st.chat_input()

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi, I am an AI bot created by LandQuire Data Team\nHow can I help you regarding this YouTube video?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


if chatgpt:

    if prompt := chat:
        if not api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()
        openai.api_key = api_key
        prompt = f'##### {prompt}'
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        temp = temp_slider
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",temperature=temp, messages=st.session_state.messages)
        msg = response.choices[0].message
        st.session_state.messages.append(msg)
        st.chat_message("assistant").write(msg.content)


else:
    if summarize:
        if not api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()
        data = youtube(youtube_link, api_key)
        prompt1 = "Please summarize this YouTube video briefly. Your summary should be brief enough that I don't need to watch the video to understand the key points. Include the most important details and topics covered in the video by accurately extracting the core essence and main ideas from the content. Make sure to cover all the key points mentioned without leaving any major details out. The objective is to provide a brief and comprehensive text summary so I can get all the key information from the video without having to view it."
        prompt2 = "Summarize the video"
        openai.api_key = api_key
        prompt = f'##### {prompt2}'

        st.session_state.messages.append({"role": "user", "content": prompt2})
        st.chat_message("user").write(prompt2)

        temp = temp_slider
        model = OpenAI(model="text-davinci-003", temperature=temp)
        chain = load_qa_chain(model, chain_type="stuff")  # chain_type="stuff"
        docs = data.similarity_search(prompt1)
        res = chain.run(input_documents=docs, question=prompt1, messages=st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": res})
        st.chat_message("assistant").write(res)


    if prompt := chat:
        if not api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()
        data = youtube(youtube_link, api_key)

        openai.api_key = api_key
        prompt = f'##### {prompt}'

        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        temp = temp_slider
        model = OpenAI(model="text-davinci-003", temperature=temp)
        chain = load_qa_chain(model, chain_type="stuff") #chain_type="stuff"
        docs = data.similarity_search(prompt)
        res = chain.run(input_documents=docs, question=prompt, messages=st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": res})
        st.chat_message("assistant").write(res)





