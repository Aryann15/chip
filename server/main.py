from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
from langchain.document_loaders import YoutubeLoader
from langchain.llms import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json

app= Flask (__name__)
CORS(app)

@app.route("/review",methods= ["POST"])
def prod_review():
    load_dotenv()
    data = json.loads(request.data.decode("utf-8"))
    urls = data["product"]

    if urls:
        # link = (f"youtube link: {product}")
        text_splitter = RecursiveCharacterTextSplitter (chunk_size = 1300 , chunk_overlap = 200)
        url_lists = [urls]
        llm = OpenAI(temperature=0.5)
        texts = []
       

        return url_lists    
        # for url in url_lists:
        #     loader = YoutubeLoader.from_youtube_url(url,add_video_info = True)
        #     result = loader.load();
        #     texts.extend(text_splitter.split_documents(result))
        
        # # texts = text_splitter.split_documents(result)
        # chain = load_summarize_chain (llm , chain_type="map_reduce",verbose=True)
        # summary = chain.run(texts)
        # return summary


if __name__ == "__main__":
    app.run(debug=True)
