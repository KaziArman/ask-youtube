class YT_transcript:
    def __init__(self,lnk):
        self.lnk = lnk

    def script(self):
        from llama_index import download_loader
        from llama_hub.youtube_transcript import YoutubeTranscriptReader
        import os
        from transformers import GPT2TokenizerFast
        from langchain.document_loaders import PyPDFLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain.embeddings import OpenAIEmbeddings
        from langchain.vectorstores import FAISS
        from langchain.chains.question_answering import load_qa_chain
        from langchain.llms import OpenAI
        from langchain.chains import ConversationalRetrievalChain

        #YoutubeTranscriptReader = download_loader("YoutubeTranscriptReader", custom_path="local_dir")
        loader = YoutubeTranscriptReader()
        documents = loader.load_data(ytlinks=[self.lnk])
        text=documents[0].text
        return text
