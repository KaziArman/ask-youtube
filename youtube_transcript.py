class YT_transcript:
    def __init__(self,lnk):
        self.lnk = lnk

    def script(self):
        from llama_index import download_loader
        import os
        from transformers import GPT2TokenizerFast
        from langchain.document_loaders import PyPDFLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain.embeddings import OpenAIEmbeddings
        from langchain.vectorstores import FAISS
        from langchain.chains.question_answering import load_qa_chain
        from langchain.llms import OpenAI
        from langchain.chains import ConversationalRetrievalChain

        YoutubeTranscriptReader = download_loader("YoutubeTranscriptReader")
        loader = YoutubeTranscriptReader()
        documents = loader.load_data(ytlinks=[self.lnk])
        text=documents[0].text
        return text
class YT_transcript:
    def __init__(self,lnk):
        self.lnk = lnk

    def script(self):
        from llama_index import download_loader
        import os
        from transformers import GPT2TokenizerFast
        from langchain.document_loaders import PyPDFLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain.embeddings import OpenAIEmbeddings
        from langchain.vectorstores import FAISS
        from langchain.chains.question_answering import load_qa_chain
        from langchain.llms import OpenAI
        from langchain.chains import ConversationalRetrievalChain
        # Step 2: Save to .txt and reopen (helps prevent issues)
        #with open('output.txt', 'r') as f:
        #    text = f.read()
        YoutubeTranscriptReader = download_loader("YoutubeTranscriptReader")
        loader = YoutubeTranscriptReader()
        documents = loader.load_data(ytlinks=[self.lnk])
        text=documents[0].text
        return text

