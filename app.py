from flask import Flask, render_template, request
import json
import os


app = Flask(
    __name__
)


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


with open(
    os.path.join(BASE_DIR, "qa_raw.json"),
    "r",
    encoding="utf-8"
) as f:

    database = json.load(f)



def find_question(qid):

    for item in database:

        if item["id"].lower() == qid.lower():

            return item

    return None



@app.route("/", methods=["GET", "POST"])
def index():

    result = None
    error = None


    if request.method == "POST":

        qid = request.form["qid"].strip()


        result = find_question(qid)


        if result is None:

            error = "沒有找到這個問題"



    return render_template(
        "index.html",
        result=result,
        error=error
    )



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )