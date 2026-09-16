# -*- coding: utf-8 -*-
"""28张情境页手绘风插画（matplotlib xkcd抖动线+中文气泡）：每课取SCEN剧情台词画部门现场速写
输出: 教学实施资料/{课程包}/授课PPT/_场景插画/W{wk}_场景.png (800x600)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib                                   # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt                     # noqa: E402
from matplotlib import font_manager                 # noqa: E402
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Wedge  # noqa: E402

from make_videos_v2 import TASKS, MAT               # noqa: E402
import universe as UNI                              # noqa: E402



def _pick_font():
    import os
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cands = [os.path.join(base, "教学实施资料", "fonts", "SourceHanSansCN-Regular.otf"),
             os.path.join(os.path.dirname(os.path.abspath(__file__)), "_local_only", "ZH_Font.ttf"),
             "/System/Library/Fonts/PingFang.ttc"]
    for c in cands:
        if os.path.exists(c):
            return c
    raise FileNotFoundError("no CJK font: " + str(cands))

FP = _pick_font()
ZH = font_manager.FontProperties(fname=FP).get_name()
NAVY, ORANGE, BLUE = "#010328", "#F5670F", "#0545E8"


def quotes_of(scen):
    qs = re.findall(r"'([^'\"]{5,42})'", scen)
    if len(qs) >= 2:
        return qs[0], qs[1]
    parts = [p.strip() for p in scen.replace("——", "。").split("。") if len(p.strip()) >= 6]
    return (parts[0][:24], parts[1][:24] if len(parts) > 1 else parts[0][:24])


def wrap(t, n=10):
    return "\n".join(t[i:i + n] for i in range(0, len(t), n))


def stick(ax, x, y, label, hat=False, flip=False):
    ax.add_patch(Circle((x, y + .30), .055, fc="#F5D7B2", ec="k", lw=1.4))
    ax.plot([x, x], [y + .245, y], "k-", lw=1.6)                     # 身
    ax.plot([x - .09, x + .09], [y + .19, y + .19], "k-", lw=1.4)    # 臂
    ax.plot([x - .06, x + .06], [y, y], "k-", lw=1.4)                # 腿
    if hat:
        ax.add_patch(Wedge((x, y + .335), .075, 0, 180, fc=ORANGE, ec="k", lw=1.2))
        ax.plot([x - .1, x + .1], [y + .335, y + .335], "k-", lw=1.6)  # 安全帽
    ax.text(x + (.05 if not flip else -.05) * (1 if not flip else -1),
            y - .13, label, ha="center", fontsize=8.5, color=NAVY)


def bubble(ax, x, y, text, color=BLUE):
    ax.add_patch(FancyBboxPatch((x, y), .40, .16,
                                boxstyle="round,pad=0.02", fc="white",
                                ec=color, lw=1.6))
    ax.text(x + .20, y + .08, wrap(text, 9), ha="center", va="center",
            fontsize=7.8, color=NAVY)
    ax.plot([x + .06, x - .04], [y, y - .10], color=color, lw=1.4)
    ax.plot([x - .04, x - .10], [y - .10, y], color=color, lw=1.4)


def scene_ai(ax, q1, q2):
    for i, (x, r) in enumerate([(.14, .085), (.30, .065)]):          # 泵站两泵
        ax.add_patch(Circle((x, .30), r, fc="#DCE6FA", ec="k", lw=1.6))
        ax.add_patch(Circle((x, .30), r * .35, fc="white", ec="k", lw=1.2))
        ax.plot([x, x], [.30 + r, .52], "k-", lw=1.6)
    ax.add_patch(Polygon([(.52, .58), (.55, .63), (.58, .58)], closed=True,
                         fc="#FFE28A", ec="k", lw=1.4))               # 告警三角
    ax.text(.55, .595, "!", ha="center", fontsize=11, fontweight="bold")
    ax.plot([.60, .66, .72, .78], [.34, .42, .40, .50], "-o", color=ORANGE,
            lw=1.8, ms=3)                                             # 振动爬升
    ax.text(.70, .53, "振动↑", fontsize=8, color=ORANGE)
    stick(ax, .34, .18, "老周", hat=True)
    bubble(ax, .44, .52, q1, ORANGE)
    stick(ax, .78, .18, "林工", hat=True)
    bubble(ax, .60, .08, q2, BLUE)


def scene_py(ax, q1, q2):
    ax.add_patch(FancyBboxPatch((.10, .28), .38, .22, boxstyle="round,pad=0.01",
                                fc="#DCE6FA", ec="k", lw=1.6))        # 注塑机
    ax.add_patch(Polygon([(.18, .50), (.23, .60), (.28, .50)], closed=True,
                         fc="#C9D6F8", ec="k", lw=1.4))               # 料斗
    for i in range(4):                                                # 输送带
        ax.plot([.48, .74], [.33, .33], "k-", lw=2)
        ax.add_patch(Circle((.52 + i * .07, .30), .022, fc=ORANGE, ec="k", lw=.8))
    ax.plot([.60, .60], [.28, .12], "k-", lw=2)                       # 温度计
    ax.add_patch(Circle((.60, .10), .026, fc="#E23B3B", ec="k", lw=1))
    ax.plot([.60, .74], [.155, .155], "k--", lw=1)
    ax.text(.66, .17, "95℃警戒", fontsize=8, color="#C0392B")
    stick(ax, .20, .12, "王主任")
    bubble(ax, .06, .62, q1, BLUE)
    stick(ax, .82, .18, "李姐", flip=True)
    bubble(ax, .56, .60, q2, ORANGE)


def scene_pp(ax, q1, q2):
    for i, x in enumerate((.12, .28, .44)):                           # 三厂区
        ax.add_patch(FancyBboxPatch((x, .30), .11, .14, boxstyle="round,pad=0.008",
                                    fc="#DCE6FA", ec="k", lw=1.4))
        ax.text(x + .055, .37, f"{i+1}号", ha="center", fontsize=8, color=NAVY)
        ax.plot([x + .055, .63], [.44, .60], color=BLUE, lw=1.4, ls="->" if False else "-")
        ax.plot([x + .055, .63], [.44, .60], ".", color=BLUE, ms=3)
    ax.add_patch(Circle((.66, .66), .10, fc="white", ec=BLUE, lw=2))  # 数据中台云
    ax.text(.66, .66, "中台", ha="center", va="center", fontsize=9, color=BLUE)
    ax.add_patch(FancyBboxPatch((.60, .16), .26, .17, boxstyle="round,pad=0.01",
                                fc="#FDF0E6", ec="k", lw=1.5))        # 仪表盘屏
    ax.plot([.63, .68, .73, .83], [.24, .30, .22, .28], "-o", color=ORANGE, lw=1.6, ms=2.5)
    stick(ax, .16, .12, "方总监")
    bubble(ax, .04, .62, q1, BLUE)
    stick(ax, .40, .10, "吴工", hat=True)
    bubble(ax, .44, .60, q2, ORANGE)


SCENE = {"ai": scene_ai, "py": scene_py, "pp": scene_pp}


def main():
    with matplotlib.rc_context({"font.sans-serif": [ZH],
                                "axes.unicode_minus": False}):
        with plt.xkcd(scale=1.1, length=110, randomness=2):
            # 关键修复：xkcd会把字体族覆盖为Humor Sans等无CJK字体→中文变方框；
            # 在上下文内夺回字体设置（保留sketch抖线效果）
            plt.rcParams["font.family"] = "sans-serif"
            plt.rcParams["font.sans-serif"] = [ZH]
            for code, wk, _m3, _wo, _nm, folder, _cn in TASKS:
                if code == "ai48":
                    continue  # ai48插画由build_ai48_visual生成
                scen = UNI.SCEN.get((code, wk))
                if not scen:
                    continue
                q1, q2 = quotes_of(scen)
                fig, ax = plt.subplots(figsize=(8, 6), dpi=100)
                ax.set_xlim(0, 1)
                ax.set_ylim(0, .8)
                ax.axis("off")
                SCENE[code](ax, q1, q2)
                ax.text(.5, .775, f"W{wk:02d} 现场速写 · {UNI.DEPTS[code]['name']}",
                        ha="center", fontsize=10, color=NAVY, fontweight="bold")
                outdir = os.path.join(MAT, folder, "授课PPT", "_场景插画")
                os.makedirs(outdir, exist_ok=True)
                path = os.path.join(outdir, f"W{wk}_场景.png")
                fig.savefig(path, bbox_inches="tight", facecolor="white")
                plt.close(fig)
                print("saved:", os.path.relpath(path, MAT), flush=True)
    print("ILLUS DONE")


if __name__ == "__main__":
    main()
