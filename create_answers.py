import json
import os


INPUT = "qa_raw.json"

OUTPUT = "visual/answers.json"


os.makedirs(
    "visual",
    exist_ok=True
)



with open(
    INPUT,
    "r",
    encoding="utf-8"
) as f:

    data = json.load(f)



answers = {}



for item in data:


    qid = item["id"]


    answers[qid] = item["conversation"]




with open(
    OUTPUT,
    "w",
    encoding="utf-8"
) as f:


    json.dump(
        answers,
        f,
        ensure_ascii=False,
        indent=2
    )


print(
    "生成完成:",
    len(answers)
)