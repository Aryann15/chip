from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
from langchain.document_loaders import YoutubeLoader
from langchain.llms import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import CharacterTextSplitter


app = Flask(__name__)
CORS(app)


@app.route("/review", methods=["POST"])
def prod_review():
    load_dotenv()

    urls = request.form["product"]

    if urls:
        
        url_lists = [
            "https://www.youtube.com/watch?v=_i_XWx05FTw",
            "https://www.youtube.com/watch?v=f4g2nPY-VZc",
            "https://www.youtube.com/watch?v=3XpK9fM_HDM",
        ]
        llm = OpenAI(temperature=0)
        texts = ""

        for url in url_lists:
            loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
            result = loader.load()
            for document in result:
                texts += document.page_content + " "

        text_splitter = CharacterTextSplitter(separator = " ",chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_text(texts)
        


if __name__ == "__main__":
    app.run(debug=True)
