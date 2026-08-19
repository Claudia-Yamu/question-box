# printer/config.py
# 58mm / 304dpi 热敏纸大字版排版参数

PAPER_WIDTH_MM = 58
DPI = 304

# 左右边距大幅缩小，让正文真正利用纸张宽度
MARGIN_LEFT_MM = 2.0
MARGIN_RIGHT_MM = 2.0

# 上下边距缩小
MARGIN_TOP_MM = 2.0
MARGIN_BOTTOM_MM = 2.0

# 编号
# 原来 30 → 现在 78
CODE_FONT_SIZE = 78
CODE_LETTER_SPACING = 3

# 问题正文
# 原来 20 → 现在 60
QUESTION_FONT_SIZE = 60

# 行间距
QUESTION_LINE_SPACING = 12

# 装饰之间的空间
DECOR_TOP_GAP_MM = 1.5
DECOR_MIDDLE_GAP_MM = 1.5
DECOR_BOTTOM_GAP_MM = 1.5

# 装饰区域高度
DECOR_HEIGHT_MM = 8.0

# 问题上下空间
QUESTION_TOP_GAP_MM = 2.5
QUESTION_BOTTOM_GAP_MM = 2.5

# 预览数量
# 0 = 不限制
# 注意：真正批量打印时建议使用 BATCH_SIZE 控制每批数量
PREVIEW_COUNT = 0

# ============================================================
# 批量生成设置
# ============================================================

# 每批生成多少张
# 例如 50：
#
# batch_001 → 第 1～50 条
# batch_002 → 第 51～100 条
# batch_003 → 第 101～150 条
#
# 最后一批不足 50 张也会正常生成。
BATCH_SIZE = 50

# 从第几条开始生成
#
# 1 = 从第一条开始
# 51 = 从第51条开始
# 101 = 从第101条开始
#
# 注意：
# 这里按照 print_data.json 中的“顺序”计算，
# 与问题 ID 的具体格式无关。
BATCH_START = 1

# 是否只生成一个批次
#
# True：
#     只生成 BATCH_START 所在的一个批次
#
# False：
#     从 BATCH_START 开始一直生成到最后。
#
# 实际打印时建议 True，
# 一批一批生成、传手机、打印。
GENERATE_ONE_BATCH = False

# 输出分辨率
OUTPUT_DPI = DPI

# 边缘安全空间
SAFE_EDGE_PX = 2