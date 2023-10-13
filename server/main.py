from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv


app= Flask (__name__)
CORS(app)

@app.route("/review",method = ["POST"])
def prod_review():
    product = request.form["product"]

    if product:
        prompt = (f"youtube link: {product}")
        return prompt

if __name__ == "__main__":
    app.run(debug=True)
