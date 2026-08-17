from flask import Flask, render_template, request
import json
import os


app = Flask(
    __name__
)


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# ============================================================
# 加载新的 QA 数据
# ============================================================

with open(
    os.path.join(
        BASE_DIR,
        "qa_raw_new.json"
    ),
    "r",
    encoding="utf-8"
) as f:

    database = json.load(f)


# ============================================================
# 根据7位编号查找问题
# ============================================================

def find_question(qid):

    for item in database:

        if item["id"].lower() == qid.lower():

            return item

    return None


# ============================================================
# 首页
# ============================================================

@app.route(
    "/",
    methods=["GET", "POST"]
)
def index():

    result = None

    error = None


    if request.method == "POST":

        qid = request.form["qid"].strip()


        result = find_question(
            qid
        )


        if result is None:

            error = "沒有找到這個問題"


    return render_template(
        "index.html",
        result=result,
        error=error
    )


# ============================================================
# 启动 Flask
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )