import json
import secrets
from pathlib import Path


# ============================================================
# 基础设置
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = BASE_DIR / "qa_raw.json"

OUTPUT_QA_FILE = BASE_DIR / "qa_raw_new.json"
OUTPUT_ANSWERS_FILE = BASE_DIR / "answers_new.json"
OUTPUT_PRINT_FILE = BASE_DIR / "print_data.json"
OUTPUT_MAPPING_FILE = BASE_DIR / "id_mapping.json"


# ============================================================
# 编号设置
# ============================================================

ID_LENGTH = 7


# 为了避免观众看错，排除：
# 0 / O
# 1 / I / L

LETTERS = "ABCDEFGHJKMNPQRSTUVWXYZ"
NUMBERS = "23456789"

ALL_CHARACTERS = LETTERS + NUMBERS


# ============================================================
# 生成一个新的7位编号
# ============================================================

def generate_id():
    """
    生成一个7位、大小写不敏感、字母数字混合的编号。

    每一位随机决定使用字母还是数字，
    不固定字母/数字的位置。
    """

    while True:

        characters = []

        for _ in range(ID_LENGTH):

            # 随机决定这一位使用字母还是数字
            if secrets.randbelow(2) == 0:
                characters.append(
                    secrets.choice(LETTERS)
                )
            else:
                characters.append(
                    secrets.choice(NUMBERS)
                )

        new_id = "".join(characters)

        # 至少包含一个字母
        has_letter = any(
            char in LETTERS
            for char in new_id
        )

        # 至少包含一个数字
        has_number = any(
            char in NUMBERS
            for char in new_id
        )

        if not has_letter or not has_number:
            continue

        return new_id


# ============================================================
# 生成570个唯一编号
# ============================================================

def generate_unique_ids(count):

    ids = set()

    while len(ids) < count:

        new_id = generate_id()

        if new_id not in ids:
            ids.add(new_id)

    return list(ids)


# ============================================================
# 提取第一个问题
# ============================================================

def get_first_question(conversation):

    for item in conversation:

        if item.get("type") == "question":

            return item.get("text", "")

    return ""


# ============================================================
# 主程序
# ============================================================

def main():

    print()
    print("=" * 60)
    print("Question Box 编号生成与数据转换程序")
    print("=" * 60)
    print()

    # --------------------------------------------------------
    # 读取原始数据
    # --------------------------------------------------------

    if not INPUT_FILE.exists():

        print("错误：找不到 qa_raw.json")
        print()
        print(f"应该位于：{INPUT_FILE}")
        return

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        database = json.load(f)


    print(f"读取到问题数量：{len(database)}")
    print()


    # --------------------------------------------------------
    # 检查数据
    # --------------------------------------------------------

    if not isinstance(database, list):

        print("错误：qa_raw.json 顶层结构不是列表。")
        return


    for item in database:

        if "id" not in item:
            print("错误：发现记录没有 id。")
            print(item)
            return

        if "conversation" not in item:
            print("错误：发现记录没有 conversation。")
            print(item)
            return


    # --------------------------------------------------------
    # 生成新的编号
    # --------------------------------------------------------

    new_ids = generate_unique_ids(
        len(database)
    )


    # --------------------------------------------------------
    # 创建新的数据
    # --------------------------------------------------------

    new_database = []

    answers_database = {}

    print_database = []

    mapping_database = []


    for index, item in enumerate(database):

        old_id = item["id"]

        new_id = new_ids[index]

        conversation = item["conversation"]


        # ================================================
        # 新的完整 QA 数据
        # ================================================

        new_item = {

            "id": new_id,

            "conversation": conversation,

            "source": item.get(
                "source",
                ""
            )

        }

        new_database.append(
            new_item
        )


        # ================================================
        # 网页查询用 answers.json
        #
        # {
        #   "K7M4X2P": [
        #       ...
        #   ]
        # }
        # ================================================

        answers_database[new_id] = conversation


        # ================================================
        # 打印用数据
        #
        # 只取第一个 question
        # ================================================

        first_question = get_first_question(
            conversation
        )

        print_database.append({

            "id": new_id,

            "question": first_question

        })


        # ================================================
        # 编号映射
        #
        # 方便之后检查和追溯
        # ================================================

        mapping_database.append({

            "old_id": old_id,

            "new_id": new_id,

            "question": first_question

        })


    # --------------------------------------------------------
    # 写入 qa_raw_new.json
    # --------------------------------------------------------

    with open(
        OUTPUT_QA_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            new_database,
            f,
            ensure_ascii=False,
            indent=2
        )


    # --------------------------------------------------------
    # 写入 answers_new.json
    # --------------------------------------------------------

    with open(
        OUTPUT_ANSWERS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            answers_database,
            f,
            ensure_ascii=False,
            indent=2
        )


    # --------------------------------------------------------
    # 写入 print_data.json
    # --------------------------------------------------------

    with open(
        OUTPUT_PRINT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            print_database,
            f,
            ensure_ascii=False,
            indent=2
        )


    # --------------------------------------------------------
    # 写入 id_mapping.json
    # --------------------------------------------------------

    with open(
        OUTPUT_MAPPING_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            mapping_database,
            f,
            ensure_ascii=False,
            indent=2
        )


    # --------------------------------------------------------
    # 完成
    # --------------------------------------------------------

    print("转换完成。")
    print()

    print("生成文件：")
    print()

    print("1. qa_raw_new.json")
    print("   完整的新 QA 数据")
    print()

    print("2. answers_new.json")
    print("   网页查询使用")
    print()

    print("3. print_data.json")
    print("   后续热敏纸打印程序使用")
    print()

    print("4. id_mapping.json")
    print("   原编号 → 新编号的对应关系")
    print()

    print("=" * 60)
    print("原问题数量：", len(database))
    print("新编号数量：", len(new_database))
    print("=" * 60)
    print()

    # --------------------------------------------------------
    # 显示前10条
    # --------------------------------------------------------

    print("前10条编号预览：")
    print()

    for item in mapping_database[:10]:

        print(
            f"{item['old_id']}  →  {item['new_id']}"
        )

    print()

    print("请先检查生成结果。")
    print("确认无误后，再进行网页和打印系统的替换。")
    print()


if __name__ == "__main__":
    main()