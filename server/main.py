from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
from langchain.document_loaders import YoutubeLoader
from langchain.llms import OpenAI
from langchain.chains.summarize import load_summarize_chain

app= Flask (__name__)
CORS(app)

@app.route("/review",methods= ["POST"])
def prod_review():
    load_dotenv()
    product = request.form["product"]

    if product:
        link = (f"youtube link: {product}")
        loader = YoutubeLoader.from_youtube_url(link,add_video_info = True)
    




if __name__ == "__main__":
    app.run(debug=True)
