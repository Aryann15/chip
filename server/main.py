from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
from langchain.document_loaders import YoutubeLoader
from langchain.llms import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import PromptTemplate
from langchain.schema import SystemMessage
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

        Write a detailed review of the product using the following text:

        "{texts}"

        SUMMARY:

        """

        map_prompt_template = PromptTemplate(
            template=map_prompt, input_variables=["texts"]
        )


        system_message = SystemMessage(
            content="""You are a world class tech product Reviewer, who can do detailed research on any tech product facts based results; 
            Your goal is to provide an accurate, unbiased review of the product based on thorough research.
            
            Please make sure you complete the objective above with the following rules:
            1/ You should do enough research to gather as much information as possible about the objective
            2/ Clearly state the purpose, features and specs of the product based on the information provided.
            3/ Identify any issues, limitations, or areas for improvement in the product and I;llustrate the pros and cons of the product
            4/ Use a professional, constructive tone without inflammatory language.
            5/ The Review should not be too concise but an in-depth product review
            6/ Give an overall rating between 1 to 5 with justification from your research""")

        chain = load_summarize_chain(
            llm,
            chain_type="map_reduce",
            map_prompt=map_prompt_template,
            combine_prompt=map_prompt_template,
            verbose=True,
        )
        summary = chain.run(texts)
        return summary


if __name__ == "__main__":
    app.run(debug=True)
