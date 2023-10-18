from flask import Flask, request, jsonify
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
from apiclient.discovery import build
import os
app = Flask(__name__)
CORS(app)


@app.route("/review", methods=["POST"])
def prod_review():
    load_dotenv()

    api_key = os.environ.get("YOUTUBE_API_KEY")
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    query = request.form["query"]
    if query:
        youtube = build ('youtube', 'v3', developerKey = api_key)
        product = query
        channel_ids = [
            "UCBJycsmduvYEL83R_U4JriQ", 
            "UCMiJRAwDNSNzuYeN2uWa0pA",
            "UCXuqSBlHAE6Xw-yeJA0Tunw"
            ]
        url_lists= []


        for channel_id in channel_ids:
            req = youtube.search().list (q= product + " review" , part= "snippet" , channelId=channel_id , type = 'video', maxResults = 1)
            res = req.execute()
            link = res.get("items")[0]["id"]["videoId"]
            youtube_link = "https://www.youtube.com/watch?v=" + link
            

        llm = ChatOpenAI(temperature=0 ,api_key = openai_api_key)
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
            embeddings = OpenAIEmbeddings(api_key= openai_api_key)
            print(cb)
        vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)
        print("vs init")

        memory = ConversationBufferMemory(
            memory_key="chat_history", k=8, return_messages=True
        )
        print("finished conversational memory")
        conv_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
            memory=memory,
        )
        print("finished conversational chain")

        answer = conv_chain({"question": query})
        if "chat_history" in answer and len(answer["chat_history"]) > 0:
            response = {"answer": answer["chat_history"][-1].content, "question": query}
        else:
            response = {"answer": "No answer found", "question": query}

        return jsonify(response)

        # print (answer)
        # return (answer)

    return chunks


if __name__ == "__main__":
    app.run(debug=True)
