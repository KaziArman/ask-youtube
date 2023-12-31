class chunking:
    def __init__(self,text):
        self.text = text

    def yt_data(self):
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
        # Step 3: Create function to count tokens
        tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
        text = self.text
        def count_tokens(text: str) -> int:
            return len(tokenizer.encode(text))

        # Step 4: Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            # Set a really small chunk size, just to show.
            chunk_size=800,
            chunk_overlap=100,
            length_function=count_tokens,
        )

        chunks = text_splitter.create_documents([text])

        return chunks
    def yt_data_gpt(self):
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
        # Step 3: Create function to count tokens
        tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
        text = self.text
        def count_tokens(text: str) -> int:
            return len(tokenizer.encode(text))

        # Step 4: Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            # Set a really small chunk size, just to show.
            chunk_size=3000,
            chunk_overlap=100,
            length_function=count_tokens,
        )

        chunks = text_splitter.create_documents([text])

        return chunks
