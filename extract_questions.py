import json
import os

INPUT = "qa_raw.json"
OUTPUT = "visual/questions.json"


with open(
    INPUT,
    "r",
    encoding="utf-8"
) as f:

    data = json.load(f)



questions = []


for item in data:

    for turn in item["conversation"]:

        if turn["type"] == "question":

            questions.append(
                turn["text"]
            )

            break



with open(
    OUTPUT,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        questions,
        f,
        ensure_ascii=False,
        indent=2
    )


print(
    "生成完成，共",
    len(questions),
    "个问题"
)