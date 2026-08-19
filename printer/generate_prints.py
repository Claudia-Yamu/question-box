# printer/generate_prints.py

"""
Question Box / 58mm / 304dpi 热敏纸批量排版程序

功能：
1. 读取项目根目录的 print_data.json
2. 每个 JSON 条目生成一张独立 PNG
3. 固定 58mm 纸宽
4. 304dpi
5. 问题区域自动换行
6. 使用魏碑字体
7. 上 / 中 / 下三组抽象装饰
8. 装饰随机组合
9. 不添加背景噪点
10. 按批次生成
11. 使用 print_data.json 中真实 ID 作为文件名
12. 自动生成 batch_001 / batch_002 ...
"""

from pathlib import Path
import json
import random

from PIL import Image, ImageDraw, ImageFont

from config import (
    PAPER_WIDTH_MM,
    DPI,
    MARGIN_LEFT_MM,
    MARGIN_RIGHT_MM,
    MARGIN_TOP_MM,
    MARGIN_BOTTOM_MM,
    CODE_FONT_SIZE,
    CODE_LETTER_SPACING,
    QUESTION_FONT_SIZE,
    QUESTION_LINE_SPACING,
    DECOR_TOP_GAP_MM,
    DECOR_MIDDLE_GAP_MM,
    DECOR_BOTTOM_GAP_MM,
    DECOR_HEIGHT_MM,
    QUESTION_TOP_GAP_MM,
    QUESTION_BOTTOM_GAP_MM,
    PREVIEW_COUNT,
    OUTPUT_DPI,
    SAFE_EDGE_PX,
    BATCH_SIZE,
    BATCH_START,
    GENERATE_ONE_BATCH,
)


# ============================================================
# 路径
# ============================================================

ROOT = Path(__file__).resolve().parent.parent
PRINTER_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = PRINTER_DIR / "output"

DATA_FILE = ROOT / "print_data.json"

FONT_FILE = (
    PRINTER_DIR
    / "fonts"
    / "FZWeiBei-S03T.ttf"
)


# ============================================================
# 颜色
# ============================================================

INK = (0, 0, 0, 255)
PAPER = (255, 255, 255, 255)


# ============================================================
# 单位转换
# ============================================================

def mm_to_px(mm: float) -> int:
    return max(
        1,
        round(mm * DPI / 25.4),
    )


# ============================================================
# 页面尺寸
# ============================================================

PAPER_WIDTH = mm_to_px(
    PAPER_WIDTH_MM
)

LEFT = mm_to_px(
    MARGIN_LEFT_MM
)

RIGHT = mm_to_px(
    MARGIN_RIGHT_MM
)

TOP = mm_to_px(
    MARGIN_TOP_MM
)

BOTTOM = mm_to_px(
    MARGIN_BOTTOM_MM
)

TEXT_WIDTH = (
    PAPER_WIDTH
    - LEFT
    - RIGHT
)


# ============================================================
# 字体
# ============================================================

def load_font(size: int):

    if not FONT_FILE.exists():

        raise FileNotFoundError(
            "\n没有找到魏碑字体：\n"
            f"{FONT_FILE}\n\n"
            "请把 FZWeiBei-S03T.ttf "
            "放进 printer/fonts/ 文件夹。"
        )

    return ImageFont.truetype(
        str(FONT_FILE),
        size=size,
    )


# ============================================================
# 文字尺寸
# ============================================================

def text_width(draw, text, font):

    bbox = draw.textbbox(
        (0, 0),
        text,
        font=font,
    )

    return (
        bbox[2]
        - bbox[0]
    )


def draw_letter_spaced_text(
    draw,
    xy,
    text,
    font,
    spacing,
    fill,
):

    x, y = xy

    for char in text:

        draw.text(
            (x, y),
            char,
            font=font,
            fill=fill,
        )

        width = text_width(
            draw,
            char,
            font,
        )

        x += (
            width
            + spacing
        )

    return x


# ============================================================
# 问题自动换行
# ============================================================

def wrap_question(
    draw,
    text,
    font,
    max_width,
):

    text = (
        str(text)
        .replace("\r\n", "\n")
        .replace("\r", "\n")
    )

    lines = []

    for paragraph in text.split("\n"):

        if not paragraph:

            lines.append("")

            continue

        current = ""

        for char in paragraph:

            candidate = (
                current
                + char
            )

            if (
                current
                and text_width(
                    draw,
                    candidate,
                    font,
                ) > max_width
            ):

                lines.append(
                    current
                )

                current = char

            else:

                current = candidate

        if current:

            lines.append(
                current
            )

    return lines or [""]


# ============================================================
# 基础装饰元素
# ============================================================

def draw_dot(
    draw,
    x,
    y,
    r=3,
):

    draw.ellipse(
        (
            x - r,
            y - r,
            x + r,
            y + r,
        ),
        fill=INK,
    )


def draw_leaf(
    draw,
    x,
    y,
    direction=1,
    scale=1.0,
):

    length = (
        15 * scale
    )

    width = (
        5 * scale
    )

    points = [
        (x, y),

        (
            x
            + direction
            * length
            * 0.55,
            y - width,
        ),

        (
            x
            + direction
            * length,
            y,
        ),

        (
            x
            + direction
            * length
            * 0.55,
            y + width,
        ),
    ]

    draw.polygon(
        points,
        fill=INK,
    )


def draw_sun_symbol(
    draw,
    cx,
    cy,
    scale=1.0,
):

    r = (
        13 * scale
    )

    draw.ellipse(
        (
            cx - r,
            cy - r,
            cx + r,
            cy + r,
        ),
        outline=INK,
        width=max(
            2,
            round(
                2.5 * scale
            ),
        ),
    )

    draw_dot(
        draw,
        cx,
        cy,
        r=max(
            3,
            3.5 * scale,
        ),
    )


def draw_xia_symbol(
    draw,
    cx,
    cy,
    scale=1.0,
):

    s = (
        14 * scale
    )

    width = max(
        2,
        round(
            2.8 * scale
        ),
    )

    draw.line(
        (
            cx,
            cy - s,
            cx,
            cy + s * 0.55,
        ),
        fill=INK,
        width=width,
    )

    draw.line(
        (
            cx - s,
            cy + s * 0.05,
            cx - 2.0 * s,
            cy + s * 0.95,
        ),
        fill=INK,
        width=width,
    )

    draw.line(
        (
            cx + s,
            cy + s * 0.05,
            cx + 2.0 * s,
            cy + s * 0.95,
        ),
        fill=INK,
        width=width,
    )


def draw_wen_symbol(
    draw,
    cx,
    cy,
    scale=1.0,
):

    s = (
        16 * scale
    )

    width = max(
        2,
        round(
            2.8 * scale
        ),
    )

    draw_dot(
        draw,
        cx,
        cy - s * 0.65,
        r=max(
            3,
            3.2 * scale,
        ),
    )

    draw.arc(
        (
            cx - s,
            cy - s * 0.25,
            cx + s,
            cy + s * 1.1,
        ),
        20,
        160,
        fill=INK,
        width=width,
    )

    draw.line(
        (
            cx - s * 0.9,
            cy + s * 0.25,
            cx + s * 0.9,
            cy + s * 0.25,
        ),
        fill=INK,
        width=width,
    )


# ============================================================
# 随机连接符
# ============================================================

def draw_connector(
    draw,
    x1,
    y,
    x2,
):

    if x2 <= x1:
        return

    mid = (
        x1 + x2
    ) / 2

    width = max(
        2,
        round(
            DPI / 120
        ),
    )

    # 随机连接方式
    mode = random.choice(
        [
            "dot",
            "double_dot",
            "leaf",
            "center_dot",
        ]
    )

    # 两侧短线
    draw.line(
        (
            x1,
            y,
            x1
            + (mid - x1)
            * 0.42,
            y,
        ),
        fill=INK,
        width=width,
    )

    draw.line(
        (
            x2
            - (x2 - mid)
            * 0.42,
            y,
            x2,
            y,
        ),
        fill=INK,
        width=width,
    )

    gap = (
        x2 - x1
    ) * 0.12

    if mode == "dot":

        draw_dot(
            draw,
            mid,
            y,
            r=4,
        )

    elif mode == "double_dot":

        draw_dot(
            draw,
            mid - gap,
            y,
            r=3,
        )

        draw_dot(
            draw,
            mid + gap,
            y,
            r=3,
        )

    elif mode == "leaf":

        draw_leaf(
            draw,
            mid,
            y,
            random.choice(
                [-1, 1]
            ),
            0.85,
        )

    elif mode == "center_dot":

        draw_dot(
            draw,
            mid - gap,
            y,
            r=2.5,
        )

        draw_dot(
            draw,
            mid,
            y,
            r=4,
        )

        draw_dot(
            draw,
            mid + gap,
            y,
            r=2.5,
        )


# ============================================================
# 随机绘制一个象征字符
# ============================================================

def draw_symbol(
    draw,
    symbol,
    cx,
    cy,
):

    if symbol == "sun":

        draw_sun_symbol(
            draw,
            cx,
            cy,
            random.choice(
                [
                    1.15,
                    1.25,
                    1.35,
                ]
            ),
        )

    elif symbol == "xia":

        draw_xia_symbol(
            draw,
            cx,
            cy,
            random.choice(
                [
                    1.10,
                    1.20,
                    1.30,
                ]
            ),
        )

    elif symbol == "wen":

        draw_wen_symbol(
            draw,
            cx,
            cy,
            random.choice(
                [
                    1.10,
                    1.20,
                    1.30,
                ]
            ),
        )


# ============================================================
# 随机顶部装饰
# ============================================================

def draw_top_decor(
    draw,
    y,
):

    cy = (
        y
        + mm_to_px(
            DECOR_HEIGHT_MM
        ) // 2
    )

    margin = mm_to_px(5)

    positions = [

        margin,

        PAPER_WIDTH // 2
        - mm_to_px(10),

        PAPER_WIDTH // 2
        + mm_to_px(10),

        PAPER_WIDTH - margin,
    ]

    # 随机选择四个符号
    symbols = random.choice(
        [
            ["sun", "xia", "wen", "sun"],
            ["wen", "sun", "xia", "wen"],
            ["xia", "wen", "sun", "xia"],
            ["sun", "wen", "xia", "sun"],
            ["wen", "xia", "sun", "wen"],
            ["xia", "sun", "wen", "xia"],
        ]
    )

    for symbol, x in zip(
        symbols,
        positions,
    ):

        draw_symbol(
            draw,
            symbol,
            x,
            cy,
        )

    # 三段连接符全部独立随机
    draw_connector(
        draw,
        positions[0]
        + mm_to_px(6),
        cy,
        positions[1]
        - mm_to_px(6),
    )

    draw_connector(
        draw,
        positions[1]
        + mm_to_px(6),
        cy,
        positions[2]
        - mm_to_px(6),
    )

    draw_connector(
        draw,
        positions[2]
        + mm_to_px(6),
        cy,
        positions[3]
        - mm_to_px(6),
    )

    # 两侧残笔随机
    if random.random() < 0.8:

        draw_leaf(
            draw,
            margin - 2,
            cy - random.choice(
                [7, 9, 11]
            ),
            random.choice(
                [-1, 1]
            ),
            random.choice(
                [0.55, 0.65, 0.75]
            ),
        )

    if random.random() < 0.8:

        draw_leaf(
            draw,
            PAPER_WIDTH
            - margin
            + 2,
            cy + random.choice(
                [7, 9, 11]
            ),
            random.choice(
                [-1, 1]
            ),
            random.choice(
                [0.55, 0.65, 0.75]
            ),
        )


# ============================================================
# 随机中间装饰
# ============================================================

def draw_middle_decor(
    draw,
    y,
):

    cy = (
        y
        + mm_to_px(
            DECOR_HEIGHT_MM
        ) // 2
    )

    center = (
        PAPER_WIDTH // 2
    )

    half = random.choice(
        [
            mm_to_px(16),
            mm_to_px(18),
            mm_to_px(20),
        ]
    )

    line_width = max(
        2,
        round(
            DPI / 120
        ),
    )

    # 左右线长度随机
    left_gap = random.choice(
        [
            mm_to_px(4),
            mm_to_px(5),
            mm_to_px(6),
        ]
    )

    right_gap = left_gap

    draw.line(
        (
            center - half,
            cy,
            center - left_gap,
            cy,
        ),
        fill=INK,
        width=line_width,
    )

    draw.line(
        (
            center + right_gap,
            cy,
            center + half,
            cy,
        ),
        fill=INK,
        width=line_width,
    )

    mode = random.choice(
        [
            "single",
            "triple",
            "leaf",
        ]
    )

    if mode == "single":

        draw_dot(
            draw,
            center,
            cy,
            r=random.choice(
                [3, 4, 5]
            ),
        )

    elif mode == "triple":

        gap = mm_to_px(2.5)

        draw_dot(
            draw,
            center - gap,
            cy,
            r=2.5,
        )

        draw_dot(
            draw,
            center,
            cy,
            r=4,
        )

        draw_dot(
            draw,
            center + gap,
            cy,
            r=2.5,
        )

    else:

        draw_leaf(
            draw,
            center,
            cy,
            random.choice(
                [-1, 1]
            ),
            random.choice(
                [0.65, 0.75, 0.85]
            ),
        )

    # 两端残笔随机
    if random.random() < 0.75:

        draw_leaf(
            draw,
            center - half - mm_to_px(2),
            cy,
            random.choice(
                [-1, 1]
            ),
            random.choice(
                [0.45, 0.55, 0.65]
            ),
        )

    if random.random() < 0.75:

        draw_leaf(
            draw,
            center + half + mm_to_px(2),
            cy,
            random.choice(
                [-1, 1]
            ),
            random.choice(
                [0.45, 0.55, 0.65]
            ),
        )


# ============================================================
# 随机底部装饰
# ============================================================

def draw_bottom_decor(
    draw,
    y,
):

    cy = (
        y
        + mm_to_px(
            DECOR_HEIGHT_MM
        ) // 2
    )

    margin = mm_to_px(5)

    positions = [

        margin,

        PAPER_WIDTH // 2
        - mm_to_px(10),

        PAPER_WIDTH // 2
        + mm_to_px(10),

        PAPER_WIDTH - margin,
    ]

    symbols = random.choice(
        [
            ["wen", "xia", "sun", "wen"],
            ["sun", "wen", "xia", "sun"],
            ["xia", "sun", "wen", "xia"],
            ["wen", "sun", "xia", "wen"],
            ["sun", "xia", "wen", "sun"],
            ["xia", "wen", "sun", "xia"],
        ]
    )

    for symbol, x in zip(
        symbols,
        positions,
    ):

        draw_symbol(
            draw,
            symbol,
            x,
            cy,
        )

    draw_connector(
        draw,
        positions[0]
        + mm_to_px(6),
        cy,
        positions[1]
        - mm_to_px(6),
    )

    draw_connector(
        draw,
        positions[1]
        + mm_to_px(6),
        cy,
        positions[2]
        - mm_to_px(6),
    )

    draw_connector(
        draw,
        positions[2]
        + mm_to_px(6),
        cy,
        positions[3]
        - mm_to_px(6),
    )

    if random.random() < 0.8:

        draw_leaf(
            draw,
            margin - 2,
            cy - random.choice(
                [7, 9, 11]
            ),
            random.choice(
                [-1, 1]
            ),
            random.choice(
                [0.55, 0.65, 0.75]
            ),
        )

    if random.random() < 0.8:

        draw_leaf(
            draw,
            PAPER_WIDTH
            - margin
            + 2,
            cy + random.choice(
                [7, 9, 11]
            ),
            random.choice(
                [-1, 1]
            ),
            random.choice(
                [0.55, 0.65, 0.75]
            ),
        )


# ============================================================
# 布局计算
# ============================================================

def calculate_layout(
    question,
):

    dummy = Image.new(
        "RGBA",
        (
            PAPER_WIDTH,
            100,
        ),
        PAPER,
    )

    draw = ImageDraw.Draw(
        dummy
    )

    code_font = load_font(
        CODE_FONT_SIZE
    )

    question_font = load_font(
        QUESTION_FONT_SIZE
    )

    lines = wrap_question(
        draw,
        question,
        question_font,
        TEXT_WIDTH,
    )

    bbox = question_font.getbbox(
        "国"
    )

    line_height = (
        bbox[3]
        - bbox[1]
    ) + QUESTION_LINE_SPACING

    question_height = (
        len(lines)
        * line_height
    )

    decor_height = mm_to_px(
        DECOR_HEIGHT_MM
    )

    code_bbox = code_font.getbbox(
        "8"
    )

    code_height = (
        code_bbox[3]
        - code_bbox[1]
    )

    total_height = (

        TOP

        + decor_height

        + mm_to_px(
            DECOR_TOP_GAP_MM
        )

        + code_height

        + mm_to_px(
            DECOR_MIDDLE_GAP_MM
        )

        + decor_height

        + mm_to_px(
            QUESTION_TOP_GAP_MM
        )

        + question_height

        + mm_to_px(
            QUESTION_BOTTOM_GAP_MM
        )

        + decor_height

        + BOTTOM
    )

    return {
        "lines": lines,
        "line_height": line_height,
        "question_height": question_height,
        "total_height": max(
            total_height,
            mm_to_px(45),
        ),
    }


# ============================================================
# 创建单张打印图
# ============================================================

def create_ticket(
    code,
    question,
):

    layout = calculate_layout(
        question
    )

    img = Image.new(
        "RGBA",
        (
            PAPER_WIDTH,
            layout["total_height"],
        ),
        PAPER,
    )

    draw = ImageDraw.Draw(
        img
    )

    # --------------------------------------------------------
    # 顶部装饰
    # --------------------------------------------------------

    draw_top_decor(
        draw,
        TOP,
    )

    y = (
        TOP
        + mm_to_px(
            DECOR_HEIGHT_MM
        )
        + mm_to_px(
            DECOR_TOP_GAP_MM
        )
    )

    # --------------------------------------------------------
    # 编号
    # --------------------------------------------------------

    code_font = load_font(
        CODE_FONT_SIZE
    )

    code_bbox = draw.textbbox(
        (0, 0),
        code,
        font=code_font,
    )

    code_width = (
        sum(
            text_width(
                draw,
                char,
                code_font,
            )
            for char in code
        )
        + CODE_LETTER_SPACING
        * max(
            0,
            len(code) - 1,
        )
    )

    code_x = (
        PAPER_WIDTH
        - code_width
    ) // 2

    draw_letter_spaced_text(
        draw,
        (
            code_x,
            y,
        ),
        code,
        code_font,
        CODE_LETTER_SPACING,
        INK,
    )

    y += (
        code_bbox[3]
        - code_bbox[1]
        + mm_to_px(
            DECOR_MIDDLE_GAP_MM
        )
    )

    # --------------------------------------------------------
    # 中间装饰
    # --------------------------------------------------------

    draw_middle_decor(
        draw,
        y,
    )

    y += (
        mm_to_px(
            DECOR_HEIGHT_MM
        )
        + mm_to_px(
            QUESTION_TOP_GAP_MM
        )
    )

    # --------------------------------------------------------
    # 问题正文
    # --------------------------------------------------------

    question_font = load_font(
        QUESTION_FONT_SIZE
    )

    line_height = layout[
        "line_height"
    ]

    for index, line in enumerate(
        layout["lines"]
    ):

        bbox = draw.textbbox(
            (0, 0),
            line,
            font=question_font,
        )

        line_width = (
            bbox[2]
            - bbox[0]
        )

        x = (
            PAPER_WIDTH
            - line_width
        ) // 2

        draw.text(
            (
                x,
                y
                + index * line_height,
            ),
            line,
            font=question_font,
            fill=INK,
        )

    y += (
        layout["question_height"]
        + mm_to_px(
            QUESTION_BOTTOM_GAP_MM
        )
    )

    # --------------------------------------------------------
    # 底部装饰
    # --------------------------------------------------------

    draw_bottom_decor(
        draw,
        y,
    )

    return img.convert(
        "RGB"
    )


# ============================================================
# 读取数据
# ============================================================

def load_data():

    if not DATA_FILE.exists():

        raise FileNotFoundError(
            f"\n没有找到 print_data.json：\n"
            f"{DATA_FILE}\n\n"
            "请把 print_data.json 放在 "
            "Question box 项目根目录。"
        )

    with DATA_FILE.open(
        "r",
        encoding="utf-8",
    ) as f:

        data = json.load(f)

    if not isinstance(
        data,
        list,
    ):

        raise ValueError(
            "print_data.json 必须是 JSON 数组。"
        )

    valid = []

    for index, item in enumerate(
        data,
        start=1,
    ):

        if not isinstance(
            item,
            dict,
        ):

            print(
                f"跳过第 {index} 条：不是对象。"
            )

            continue

        code = str(
            item.get(
                "id",
                "",
            )
        ).strip()

        question = str(
            item.get(
                "question",
                "",
            )
        ).strip()

        if not code or not question:

            print(
                f"跳过第 {index} 条："
                "缺少 id 或 question。"
            )

            continue

        valid.append(
            (
                code,
                question,
            )
        )

    return valid


# ============================================================
# 计算批次
# ============================================================

def calculate_batches(
    total_count,
):

    if total_count <= 0:
        return []

    if BATCH_SIZE <= 0:
        raise ValueError(
            "BATCH_SIZE 必须大于 0。"
        )

    if BATCH_START < 1:
        raise ValueError(
            "BATCH_START 必须从 1 开始。"
        )

    if BATCH_START > total_count:
        raise ValueError(
            f"BATCH_START={BATCH_START} "
            f"超过数据总数 {total_count}。"
        )

    start_index = (
        BATCH_START - 1
    )

    batches = []

    if GENERATE_ONE_BATCH:

        batch_number = (
            start_index
            // BATCH_SIZE
        )

        end_index = min(
            start_index
            + BATCH_SIZE,
            total_count,
        )

        batches.append(
            (
                batch_number + 1,
                start_index,
                end_index,
            )
        )

    else:

        current = start_index

        batch_number = (
            current
            // BATCH_SIZE
        )

        while current < total_count:

            end_index = min(
                current
                + BATCH_SIZE,
                total_count,
            )

            batches.append(
                (
                    batch_number + 1,
                    current,
                    end_index,
                )
            )

            current = end_index

            batch_number += 1

    return batches


# ============================================================
# 写入批次信息
# ============================================================

def write_batch_info(
    batch_dir,
    batch_number,
    start_index,
    end_index,
    data,
):

    first_code = data[
        start_index
    ][0]

    last_code = data[
        end_index - 1
    ][0]

    count = (
        end_index
        - start_index
    )

    info_file = (
        batch_dir
        / "batch_info.txt"
    )

    with info_file.open(
        "w",
        encoding="utf-8",
    ) as f:

        f.write(
            "Question Box · 打印批次信息\n"
        )

        f.write(
            "=" * 40
            + "\n\n"
        )

        f.write(
            f"批次：batch_{batch_number:03d}\n"
        )

        f.write(
            f"数量：{count} 张\n"
        )

        f.write(
            f"数据序号："
            f"{start_index + 1}"
            f" - "
            f"{end_index}\n"
        )

        f.write(
            f"第一张：{first_code}\n"
        )

        f.write(
            f"最后一张：{last_code}\n\n"
        )

        f.write(
            "文件列表：\n"
        )

        for index in range(
            start_index,
            end_index,
        ):

            code = data[
                index
            ][0]

            f.write(
                f"{index + 1:03d}  "
                f"{code}.png\n"
            )


# ============================================================
# 生成一个批次
# ============================================================

def generate_batch(
    batch_number,
    start_index,
    end_index,
    data,
):

    batch_dir = (
        OUTPUT_DIR
        / f"batch_{batch_number:03d}"
    )

    batch_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    print()
    print(
        "-" * 58
    )

    print(
        f"批次："
        f"batch_{batch_number:03d}"
    )

    print(
        f"范围："
        f"第 {start_index + 1}"
        f" ～ "
        f"{end_index} 条"
    )

    print(
        f"编号："
        f"{data[start_index][0]}"
        f" → "
        f"{data[end_index - 1][0]}"
    )

    print(
        f"数量："
        f"{end_index - start_index} 张"
    )

    print(
        "-" * 58
    )

    # 清理当前批次旧 PNG
    for path in batch_dir.glob(
        "*.png"
    ):

        path.unlink()

    # 生成图片
    for local_index, index in enumerate(
        range(
            start_index,
            end_index,
        ),
        start=1,
    ):

        code, question = data[
            index
        ]

        image = create_ticket(
            code,
            question,
        )

        output = (
            batch_dir
            / f"{code}.png"
        )

        image.save(
            output,
            format="PNG",
            dpi=(
                OUTPUT_DPI,
                OUTPUT_DPI,
            ),
        )

        print(
            f"[{local_index:>3}/"
            f"{end_index - start_index}] "
            f"{code} "
            f"-> "
            f"{output.name}"
        )

    write_batch_info(
        batch_dir,
        batch_number,
        start_index,
        end_index,
        data,
    )

    print()
    print(
        f"批次完成："
        f"batch_{batch_number:03d}"
    )

    print(
        f"输出目录："
        f"{batch_dir}"
    )


# ============================================================
# 主程序
# ============================================================

def main():

    print("=" * 58)

    print(
        "Question Box · "
        "58mm / 304dpi · "
        "大字版"
    )

    print(
        "随机装饰 + 批次生成模式"
    )

    print("=" * 58)

    data = load_data()

    total_count = len(data)

    print(
        f"数据总数："
        f"{total_count}"
    )

    print(
        f"每批数量："
        f"{BATCH_SIZE}"
    )

    print(
        f"起始位置："
        f"第 {BATCH_START} 条"
    )

    batches = calculate_batches(
        total_count
    )

    print(
        f"本次生成批次："
        f"{len(batches)}"
    )

    for (
        batch_number,
        start_index,
        end_index,
    ) in batches:

        generate_batch(
            batch_number,
            start_index,
            end_index,
            data,
        )

    print()
    print("=" * 58)

    print(
        "生成完成。"
    )

    print(
        f"输出目录："
        f"{OUTPUT_DIR}"
    )

    print("=" * 58)


if __name__ == "__main__":
    main()