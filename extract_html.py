#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os
import json
from bs4 import BeautifulSoup


INPUT_DIR = r"C:\Users\36175\OneDrive\Desktop\questionDetail\questionDetail"# 替換為實際文件路徑
OUTPUT_FILE = "qa_raw.json"


def clean_text(text):
    return (
        text
        .replace("\n", " ")
        .strip()
    )


def parse_html(filepath):

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as f:
        html = f.read()


    soup = BeautifulSoup(
        html,
        "html.parser"
    )


    text = soup.get_text(
        "\n",
        strip=True
    )


    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]


    conversation = []


    current_type = None
    buffer = []


    markers = {
        "提问": "question",
        "回答": "answer",
        "追问": "question",
        "追答": "answer"
    }


    for line in lines:


        if line in markers:

            # 保存上一段文字
            if current_type and buffer:

                conversation.append(
                    {
                        "type": current_type,
                        "text": clean_text(
                            " ".join(buffer)
                        )
                    }
                )


            current_type = markers[line]

            buffer = []


        else:

            if current_type:

                buffer.append(line)



    # 保存最后一段

    if current_type and buffer:

        conversation.append(
            {
                "type": current_type,
                "text": clean_text(
                    " ".join(buffer)
                )
            }
        )


    return conversation



results = []


files = sorted(
    [
        f for f in os.listdir(INPUT_DIR)
        if f.endswith(".html")
    ]
)



for index, filename in enumerate(files,1):

    path = os.path.join(
        INPUT_DIR,
        filename
    )


    conversation = parse_html(path)


    item = {

        "id": f"Q{index:03d}",

        "conversation": conversation,

        "source": filename

    }


    results.append(item)



with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        results,
        f,
        ensure_ascii=False,
        indent=4
    )


print(
    "完成:",
    len(results)
)


# In[ ]:




