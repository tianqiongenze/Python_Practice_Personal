# -*- coding: utf-8 -*-
"""6份软件操作指南配图：界面线框图+操作流程图(matplotlib绘制)"""
import os

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

matplotlib.use("Agg")
FP = "/Users/joelgong/Desktop/现代制造 1/Python编程实战/_docx_work/_local_only/ZH_Font.ttf"
from matplotlib import font_manager                     # noqa: E402
font_manager.fontManager.addfont(FP)
plt.rcParams["font.sans-serif"] = [font_manager.FontProperties(fname=FP).get_name()]
plt.rcParams["axes.unicode_minus"] = False

OUT = "/Users/joelgong/Desktop/现代制造 1/Python编程实战/教学实施资料/软件操作指南/图"
os.makedirs(OUT, exist_ok=True)
NAVY, BLUE, ORANGE, GRAY, LIGHT = "#010328", "#0545E8", "#F5670F", "#44546A", "#F3F6FD"


def frame(ax, title):
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.add_patch(Rectangle((0.2, 0.2), 15.6, 9.3, fill=False, ec=NAVY, lw=2))
    ax.add_patch(Rectangle((0.2, 8.6), 15.6, 0.9, fc=NAVY, ec=NAVY))
    ax.text(8, 9.0, title, ha="center", va="center", color="w",
            fontsize=12, fontweight="bold")


def block(ax, x, y, w, h, label, fc=LIGHT, ec=BLUE, fs=8.5, tc=NAVY, bold=False):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=1.2))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
            fontsize=fs, color=tc, fontweight="bold" if bold else "normal")


def arrow(ax, x1, y1, x2, y2, text=""):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=14, color=ORANGE, lw=1.6))
    if text:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + .25, text, ha="center",
                fontsize=8, color=ORANGE)


# ============ 1 Anaconda Navigator ============
fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.6, 4.4))
frame(a1, "Anaconda Navigator 界面线框")
for i, m in enumerate(["Home", "Environments", "Learning", "Community"]):
    block(a1, 0.5, 7.6 - i * 1.1, 3.2, 0.9, m,
          fc=NAVY if i == 1 else LIGHT, tc="w" if i == 1 else NAVY, bold=(i == 1))
block(a1, 4.2, 6.4, 7.0, 2.0, "环境列表\nbase (root)  ▼\n课程环境 py310", fs=9)
block(a1, 11.5, 6.4, 4.0, 2.0, "操作按钮\nCreate / Clone / Remove", fs=8.5)
block(a1, 4.2, 3.2, 11.3, 2.8, "包列表(Channels: defaults)\nnumpy ✓   pandas ✓   jieba ✗ → 勾选后 Apply 安装", fs=9)
block(a1, 4.2, 1.0, 11.3, 1.8, "搜索框: 输入包名过滤（例: scikit-learn）", fs=9)
frame(a2, "安装与建环境流程")
steps = ["官网下载 Anaconda3", "安装(勾选 Add to PATH)", "打开 Navigator",
         "Environments→Create 新建 py310", "搜索并安装课程依赖", "Home 启动 Jupyter"]
for i, s_ in enumerate(steps):
    y = 8.0 - i * 1.35
    block(a2, 1.0, y - 0.5, 6.0, 0.85, f"{i+1}. {s_}",
          fc=NAVY if i in (0, 3) else LIGHT, tc="w" if i in (0, 3) else NAVY)
    if i < 5:
        arrow(a2, 4.0, y - 0.55, 4.0, y - 1.15)
plt.tight_layout()
plt.savefig(f"{OUT}/anaconda.png", dpi=150)
plt.close()

# ============ 2 Jupyter Notebook ============
fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.6, 4.4))
frame(a1, "Jupyter Notebook 界面线框")
block(a1, 0.5, 7.4, 15.0, 0.8, "菜单栏: File Edit View Insert Cell Kernel Help   |   ▶ Run | ■ Stop | ▷▷ Restart", fs=8)
block(a1, 0.5, 6.2, 15.0, 0.7, "工具栏: ＋ 代码单元  ▶ 运行  ■ 中断  保存  Cell类型[Code▼]", fs=8)
block(a1, 0.5, 4.4, 15.0, 1.5, "In [1]:  print(\"环境OK\")", fs=9.5)
block(a1, 0.5, 2.6, 15.0, 1.5, "Out[1]: 环境OK", fc="#E8F1E8", ec="#01751F")
block(a1, 0.5, 0.8, 15.0, 1.4, "In [2]: |   ← 光标在此, Shift+Enter 运行并新建", fs=9.5)
frame(a2, "单元操作核心流程")
steps = ["新建 notebook(New→Python3)", "Markdown单元写标题", "Code单元写代码",
         "Shift+Enter 运行", "Kernel→Restart清空重跑", "File→下载ipynb提交"]
for i, s_ in enumerate(steps):
    y = 8.0 - i * 1.35
    block(a2, 1.0, y - 0.5, 6.2, 0.85, f"{i+1}. {s_}",
          fc=BLUE if i == 3 else LIGHT, tc="w" if i == 3 else NAVY)
    if i < 5:
        arrow(a2, 4.1, y - 0.55, 4.1, y - 1.15)
plt.tight_layout()
plt.savefig(f"{OUT}/jupyter.png", dpi=150)
plt.close()

# ============ 3 GitHub/Gitee ============
fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.6, 4.4))
frame(a1, "Gitee/GitHub 仓库页线框")
block(a1, 0.5, 7.3, 15.0, 0.8, "仓库名/工业互联网课程  ★Star  ⑂Fork   [绿色Code▼按钮]", fs=8.5)
block(a1, 0.5, 5.6, 9.6, 1.4, "文件列表\nsrc/   tests/   README.md   requirements.txt", fs=9)
block(a1, 10.4, 5.6, 5.1, 1.4, "About\n分支 main/dev\n提交 32", fs=8.5)
block(a1, 0.5, 3.8, 15.0, 1.4, "点击 Code → 复制 HTTPS 地址 (https://gitee.com/xxx/xxx.git)", fc="#FDF0E6", ec=ORANGE)
block(a1, 0.5, 1.0, 15.0, 2.4, "提交历史 commits —— 每次feat:/fix:一条记录(评审证据)", fs=9)
frame(a2, "Git 五步工作流")
for i, s_ in enumerate(["git clone 地址", "git checkout -b dev", "改代码+git add .",
                        "git commit -m \"feat: xxx\"", "git push origin dev"]):
    y = 8.0 - i * 1.6
    block(a2, 0.8, y - 0.55, 7.2, 0.95, s_, fc=NAVY if i % 2 == 0 else BLUE,
          tc="w", fs=9, bold=True)
    if i < 4:
        arrow(a2, 4.4, y - 0.6, 4.4, y - 1.0)
plt.tight_layout()
plt.savefig(f"{OUT}/git.png", dpi=150)
plt.close()

# ============ 4 ProcessOn ============
fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.6, 4.4))
frame(a1, "ProcessOn 界面线框")
block(a1, 0.5, 7.4, 3.0, 1.6, "图形库\n流程图/架构图\nER图/UML", fs=8.5)
block(a1, 3.9, 7.4, 8.2, 1.6, "画布：拖入图形→双击改名→连线（自动吸附）", fs=9)
block(a1, 12.4, 7.4, 3.1, 1.6, "属性栏\n填充/边框/字号", fs=8.5)
for i in range(3):
    block(a1, 3.9 + i * 2.9, 4.6, 2.2, 1.2,
          ["开始", "处理", "判断"][i], fc=LIGHT, fs=9)
    if i < 2:
        arrow(a1, 6.1, 5.2, 6.8, 5.2)
block(a1, 3.9, 1.0, 11.6, 2.6, "顶部：文件→导出(PNG/PDF/POS)   模板社区搜索\"流程图\"", fs=9)
frame(a2, "绘制流程图四步")
for i, s_ in enumerate(["新建→流程图", "拖图形到画布", "双击改文字/连线",
                        "导出PNG插入工单"]):
    y = 7.8 - i * 1.7
    block(a2, 1.2, y - 0.5, 6.2, 0.95, f"{i+1}. {s_}",
          fc=ORANGE if i == 3 else LIGHT, tc="w" if i == 3 else NAVY)
    if i < 3:
        arrow(a2, 4.3, y - 0.55, 4.3, y - 1.1)
plt.tight_layout()
plt.savefig(f"{OUT}/processon.png", dpi=150)
plt.close()

# ============ 5 PyCharm ============
fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.6, 4.4))
frame(a1, "PyCharm 界面线框")
block(a1, 0.5, 7.4, 15.0, 0.8, "菜单: File Edit View Run Git Tools   |   运行▶ 调试(()=> 终端Terminal", fs=8)
block(a1, 0.5, 3.4, 3.4, 3.8, "Project 项目树\nsrc/\n  main.py\n  utils.py\ntests/", fs=8.5)
block(a1, 4.2, 5.4, 8.2, 1.8, "编辑器: 代码+智能提示(Tab补全)\n行号断点(点击行号旁)", fs=9)
block(a1, 12.7, 5.4, 2.8, 1.8, "结构栏\n类/函数", fs=8.5)
block(a1, 4.2, 3.4, 11.3, 1.6, "Run 窗口: 程序输出 / 调试变量", fc="#E8F1E8", ec="#01751F", fs=9)
block(a1, 0.5, 1.0, 15.0, 2.0, "底部 Terminal: 可直接跑 git / pytest / pip", fs=9)
frame(a2, "首次配置三步")
for i, s_ in enumerate(["New Project→选venv", "Settings→解释器选venv",
                        "Run→运行main.py"]):
    y = 7.6 - i * 1.9
    block(a2, 1.2, y - 0.5, 6.4, 1.0, f"{i+1}. {s_}", fc=BLUE, tc="w", fs=9.5)
    if i < 2:
        arrow(a2, 4.4, y - 0.55, 4.4, y - 1.3)
plt.tight_layout()
plt.savefig(f"{OUT}/pycharm.png", dpi=150)
plt.close()

print("5张指南配图已生成 →", OUT)
