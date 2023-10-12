from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
from langchain.document_loaders import YoutubeLoader
from langchain.llms import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter


app = Flask(__name__)
CORS(app)


@app.route("/review", methods=["POST"])
def prod_review():
    load_dotenv()

    urls = request.form["product"]

    if urls:
        # link = (f"youtube link: {product}")
        text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n"], chunk_size=1500, chunk_overlap=200
        )
        url_lists = ["", ""]
        llm = OpenAI(temperature=0)
        texts = []

        for url in url_lists:
            loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
            result = loader.load()
            texts.extend(text_splitter.split_documents(result))

        # texts = text_splitter.split_documents(result)
        map_prompt = """

        Write a detailed review of the product using the followinf text:

        "{texts}"

        SUMMARY:

        """

        chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=True)
        summary = chain.run(texts)
        return summary


if __name__ == "__main__":
    app.run(debug=True)
