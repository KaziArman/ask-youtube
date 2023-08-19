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


with st.expander("How to use Ask Youtube 🤖", expanded=False):
	st.markdown(
		"""
		Please refer to [our dedicated guide](#) on how to use Ask Youtube.
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


api_key = st.sidebar.text_input('Enter your API key',type="password")

youtube_link = st.sidebar.text_input('Enter your YouTube video link')
temp_slider = st.sidebar.slider('Set the temperature of the completion. Higher values make the output more random,  lower values make it more focused.', 0.0, 1.0, 0.7)
st.sidebar.button("Clear messages", use_container_width=True,on_click=on_btn_click)
summarize = st.sidebar.button("Summarize Part by Part", use_container_width=True)
chatgpt = st.sidebar.checkbox('Use ChatGPT', False,
			help='Allow the bot to collect answers to any specific questions from outside of the video content')


link=""
if youtube_link:
    link = youtube_link
    yt_script = YT_transcript(link)
    transcript = yt_script.script()
    text = """\n\n\nPlease summarize this YouTube video briefly. 
                Your summary should be brief enough that I don't need to watch the video to understand the key points. 
                Include the most important details and topics covered in the video by accurately extracting the core essence and main ideas from the content. 
                Make sure to cover all the key points mentioned without leaving any major details out. 
                The objective is to provide a details so I can get all the key information from the video without having to view it.
                First, analyze the video line-by-line, distilling each line into a simple summary sentence.
               Then combine these sentence summaries into a short summary covering the key points. 
               Please make sure to accurately capture the essence and meaning of this youtube video content.
               I will ask some questions about the video - please answer them precisely with relevant details from the source database."""

    transcript = transcript + text
    chnk = chunking(transcript)
    chunks = chnk.yt_data()
    if api_key:
        openai.api_key = api_key
        os.environ["OPENAI_API_KEY"] = api_key

        embeddings = OpenAIEmbeddings()
        db = FAISS.from_documents(chunks, embeddings)

    else:
        st.info("Please add your OpenAI API key to continue.")





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
        prompt = f'{prompt}'
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
        data = db
        prompt1 = "Please summarize this YouTube video briefly. Your summary should be brief enough that I don't need to watch the video to understand the key points. Include the most important details and topics covered in the video by accurately extracting the core essence and main ideas from the content. Make sure to cover all the key points mentioned without leaving any major details out. The objective is to provide a details at least 3 paragrapghs and comprehensive text summary so I can get all the key information from the video without having to view it."
        prompt3 = 'First, divide the entire video transcription into three parts based on duration. Then, begin by describing the content of the first part according to the dividation. Your response should be accurate, and contain as much information as required to create a informative summary.'
        prompt4 = 'Now, begin by describing the content of the second part according to the previous dividation. Your response should be accurate, and contain as much information as required to create a informative summary. Please make sure that you are not repeating the summary that you use in the first part'
        prompt5 = 'Now, begin by describing the content of the third part according to the previous dividation. Your response should be accurate, and contain as much information as required to create a informative summary. Please make sure that you are not repeating the summary that you use in the first and second part'
        prompt6 = "Now, provide a summary of the entire video  while ensuring all the topics covered are included.Your response should be accurate, and contain at least 100 words or 10 sentences. Make sure to start the passage writing 'In Summary: -' and start the passage from the next new line "
        prompt2 = "Summarize the video"
        openai.api_key = api_key
        prompt = f'{prompt3}'
        st.session_state.messages.append({"role": "user", "content": prompt2})
        st.chat_message("user").write(prompt2)
        out = ""
        ll = [prompt3, prompt4, prompt5, prompt6]
        for i in ll:
            pp = i
            print(pp)
            temp = temp_slider
            model = OpenAI(model="text-davinci-003", temperature=temp)
            chain = load_qa_chain(model, chain_type="stuff")  # chain_type="stuff"
            docs = data.similarity_search(pp)
            res = chain.run(input_documents=docs, question=pp, messages=st.session_state.messages)
            out = out + "\n\n" + res

        st.session_state.messages.append({"role": "assistant", "content": out})
        st.chat_message("assistant").write(out)


    if prompt := chat:
        if not api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()

        data = db

        openai.api_key = api_key
        prompt = f'{prompt}'

        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        temp = temp_slider
        model = OpenAI(model="text-davinci-003", temperature=temp)
        chain = load_qa_chain(model, chain_type="stuff") #chain_type="stuff"
        docs = data.similarity_search(prompt)
        res = chain.run(input_documents=docs, question=prompt, messages=st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": res})
        st.chat_message("assistant").write(res)