# Question Box · 58mm 热敏纸打印程序

第一版按照最终确认的视觉方案制作：

- 58mm 纸宽
- 203 DPI 默认值
- 魏碑字体
- 7位问题编号
- 一个问题一张纸
- 自动换行
- 自动计算纸张高度
- 上 / 中 / 下三组抽象装饰
- 不使用噪点
- 不使用纯方框
- 不连接真实打印机，只生成 PNG

## 1. 文件放置

项目结构：

Question box/
├── print_data.json
└── printer/
    ├── config.py
    ├── generate_prints.py
    ├── fonts/
    │   └── FZWeiBei-S03T.ttf
    └── output/

把你现有的 `FZWeiBei-S03T.ttf` 复制到：

`printer/fonts/FZWeiBei-S03T.ttf`

## 2. 安装 Pillow

在 Question box 根目录运行：

```bash
pip install pillow
```

如果你的电脑已经安装过 Pillow，可以直接跳过。

## 3. 先生成预览

打开：

`printer/config.py`

保持：

```python
PREVIEW_COUNT = 10
```

然后进入 printer：

```bash
cd printer
```

运行：

```bash
python generate_prints.py
```

程序会读取项目根目录的 `print_data.json`，并在：

`printer/output/`

生成前10张 PNG。

## 4. 确认版式

先不要批量打印。

重点检查：

- 魏碑在你的电脑上是否清楚
- 7位编号是否足够突出
- 问题字号是否合适
- 长问题换行是否自然
- 上中下三组装饰是否有足够留白
- 透明热敏纸实际打印时是否太黑/太淡

## 5. 全部生成

确认前10张没有问题后，把：

```python
PREVIEW_COUNT = 10
```

改成：

```python
PREVIEW_COUNT = 0
```

再次运行：

```bash
python generate_prints.py
```

就会生成全部问题。

## 6. 以后调整

所有主要参数都集中在：

`printer/config.py`

例如：

```python
CODE_FONT_SIZE = 30
QUESTION_FONT_SIZE = 20
QUESTION_LINE_SPACING = 9
```

不需要修改 `generate_prints.py`。

## 7. 重要

目前程序只负责：

`JSON → PNG`

暂时不直接控制打印机。

等你确定实际热敏打印机型号、连接方式和 DPI 后，再做：

`PNG / 排版 → 打印机`

的最终适配。

这样可以先通过少量实物测试确认版式，不会因为打印机差异返工全部570张。
