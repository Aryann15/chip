from flask import Flask, request , jsonify
from flask_cors import CORS
import json
from dotenv import load_dotenv
from langchain.document_loaders import YoutubeLoader
from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.callbacks import get_openai_callback
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

app = Flask(__name__)
CORS(app)


@app.route("/review", methods=["POST"])
def prod_review():
    load_dotenv()

    query = request.form["query"]

    if query:
        url_lists = [
            "https://www.youtube.com/watch?v=_i_XWx05FTw",
            "https://www.youtube.com/watch?v=f4g2nPY-VZc",
            "https://www.youtube.com/watch?v=3XpK9fM_HDM",
        ]
        llm = ChatOpenAI(temperature=0)
        texts = ""

        for url in url_lists:
            loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
            result = loader.load()
            for document in result:
                texts += document.page_content + " "

        text_splitter = CharacterTextSplitter(
            separator=" ", chunk_size=1500, chunk_overlap=200
        )
        chunks = text_splitter.split_text(texts)
        with get_openai_callback() as cb:
            embeddings = OpenAIEmbeddings()
            print(cb)
        vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)
        print("vs init")

        memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        ) 
        print("finished conversational memory")
        conv_chain = ConversationalRetrievalChain.from_llm(
            llm=llm, retriever=vectorstore.as_retriever(), memory=memory
        )
        print("finished conversational chain")

        answer =  (conv_chain({"question":query}))
        if 'chat_history' in answer and len(answer['chat_history']) > 0:
            response = {
                "answer": answer['chat_history'][-1].content,  # Assuming the last message is the answer
                "question": query
            }
        else:
            response = {
                "answer": "No answer found",
                "question": query
            }

        return jsonify(response)







        # # print (answer)
        # # return (answer)
    

        

    # return chunks


if __name__ == "__main__":
    app.run(debug=True)
