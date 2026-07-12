#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import os


DATA_FILE = "qa_raw.json"



def load_database():

    with open(
        DATA_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



def find_question(data, qid):

    for item in data:

        if item["id"].lower() == qid.lower():

            return item

    return None



def clear_screen():

    os.system(
        "cls" if os.name == "nt" else "clear"
    )



def show_home():

    clear_screen()

    print("=" * 50)

    print(
        "      問答展示系統"
    )

    print()

    print(
        "請輸入問題ID"
    )

    print(
        "例如：Q001"
    )

    print("=" * 50)



def display(item):

    clear_screen()


    print("=" * 50)


    for turn in item["conversation"]:


        if turn["type"] == "question":

            print("\n提問：")

        else:

            print("\n回答：")


        print(
            turn["text"]
        )


    print("\n")
    print("=" * 50)



    # 自動返回入口

    input(
        "\n按 Enter 返回"
    )



def main():

    database = load_database()


    while True:


        show_home()


        qid = input(
            "\nID > "
        ).strip()



        item = find_question(
            database,
            qid
        )


        if item:

            display(item)


        else:

            print(
                "\n沒有找到這個問題"
            )

            input(
                "\n按 Enter 返回"
            )



if __name__ == "__main__":

    main()


# In[ ]:





# In[ ]:




