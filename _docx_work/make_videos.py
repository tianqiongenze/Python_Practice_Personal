# -*- coding: utf-8 -*-
"""原创动画微课生成(matplotlib+ffmpeg): 5个mp4"""
import os

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.animation as manim

matplotlib.use("Agg")
FP = "/Users/joelgong/Desktop/现代制造 1/Python编程实战/_docx_work/_local_only/ZH_Font.ttf"
from matplotlib import font_manager           # noqa: E402
font_manager.fontManager.addfont(FP)
zh = font_manager.FontProperties(fname=FP).get_name()
plt.rcParams["font.sans-serif"] = [zh]
plt.rcParams["axes.unicode_minus"] = False

MAT = "/Users/joelgong/Desktop/现代制造 1/Python编程实战/教学实施资料"
NAVY, BLUE, ORANGE = "#010328", "#0545E8", "#F5670F"


def save_mp4(anim, path, fps=8):
    path = os.path.abspath(path)
    anim.save(path, writer=manim.FFMpegWriter(fps=fps, bitrate=2400))
    print("saved:", path, os.path.getsize(path) // 1024, "KB")


# ============== 1) 六步法80分钟时间盒 ==============
def video_sixstep(path):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    segs = [("资讯·计划", 0, "课前"), ("决策", 10, "备选对比+矩阵"),
            ("实施一", 30, "骨架贯通"), ("检查", 5, "三层质检"),
            ("实施二", 25, "优化冲优"), ("评价", 10, "量表+反馈")]
    colors = [GRAYc := "#44546A", BLUE, "#0475B6", ORANGE, "#01751F", NAVY]

    def draw(k):
        ax.clear()
        left = 0
        for i, (name, val, note) in enumerate(segs):
            on = i <= k
            ax.barh(0, val if on else 0, left=left, height=0.55,
                    color=colors[i] if on else "#E7E9F0")
            if on:
                ax.text(left + val / 2, 0, f"{name}\n{val}min" if val else name,
                        ha="center", va="center", color="w", fontsize=10,
                        fontweight="bold")
                ax.text(left + val / 2, 0.42, note, ha="center", fontsize=8,
                        color=colors[i])
            left += val
        ax.set_xlim(0, 80)
        ax.set_yticks([])
        ax.set_xlabel("分钟（课堂80分钟 = 2课时×40分钟）")
        ax.set_title("六步法课堂时间盒" if k >= 0 else "", fontsize=13,
                     fontweight="bold")
        ax.spines[["top", "right", "left"]].set_visible(False)
    frames = list(range(-1, 7)) * 6 + [6] * 6
    ani = FuncAnimation(fig, draw, frames=frames, interval=900)
    save_mp4(ani, path, fps=3)
    plt.close(fig)


# ============== 2) 滑动窗口与RUL ==============
def video_window(path):
    rng = np.random.RandomState(7)
    t = np.arange(200)
    series = 0.6 + 2.2 * (t / 200) ** 1.6 + rng.normal(0, .1, 200)
    fig, ax = plt.subplots(figsize=(8, 4.5))

    def draw(k):
        ax.clear()
        start = 20 + k * 6
        ax.plot(t, series, lw=1.5, color=BLUE, label="振动信号")
        ax.axvspan(start, start + 20, color=ORANGE, alpha=.3)
        ax.axvspan(0, start + 20, color=NAVY, alpha=.06)
        ax.plot(t[start:start + 20], series[start:start + 20], color=ORANGE,
                lw=3, label="输入窗口X(20步)")
        ax.scatter([start + 20], [series[start + 20]], marker="*", s=180,
                   color=NAVY, zorder=5, label="标签y=RUL")
        ax.annotate(f"RUL={1 - (start + 20) / 199:.2f}",
                    (start + 20, series[start + 20]),
                    textcoords="offset points", xytext=(12, -6), fontsize=11,
                    color=NAVY, fontweight="bold")
        ax.set_title("滑动窗口造样本：看前20步 → 预测剩余寿命", fontsize=12,
                     fontweight="bold")
        ax.legend(loc="upper left", fontsize=9)
        ax.set_xlabel("时间步"); ax.set_ylabel("振动幅值")
    ani = FuncAnimation(fig, draw,
                        frames=list(range(24)) * 3 + [23] * 6, interval=500)
    save_mp4(ani, path, fps=2)
    plt.close(fig)


# ============== 3) 卷积滑动 ==============
def video_conv(path):
    rng = np.random.RandomState(3)
    img = np.zeros((12, 12))
    img[4:8, 3:9] = 1.0                      # 一条竖亮带
    img += rng.normal(0, .08, img.shape)
    ker = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])  # 垂直边缘核
    fig, axs = plt.subplots(1, 3, figsize=(10, 3.6))

    def draw(k):
        r, c = k // 6 + 3, k % 6 + 3
        for a in axs:
            a.clear()
        axs[0].imshow(img, cmap="Blues"); axs[0].set_title("输入图像", fontsize=11)
        from matplotlib.patches import Rectangle
        axs[0].add_patch(Rectangle((c - .5, r - .5), 3, 3,
                                   fill=False, edgecolor=ORANGE, lw=2.5))
        # 核
        axs[1].imshow(ker, cmap="RdBu_r", vmin=-1, vmax=1)
        axs[1].set_title("3×3卷积核\n(垂直边缘)", fontsize=10)
        # 输出累积
        out = np.zeros((10, 10))
        for i in range(10):
            for j in range(10):
                out[i, j] = np.abs((img[i:i + 3, j:j + 3] * ker).sum())
        mask = np.zeros((10, 10), bool)
        mask[:r - 2, :c - 2] = True
        disp = np.where(mask, out, np.nan)
        axs[2].imshow(disp, cmap="viridis")
        axs[2].set_title("输出特征图(已扫描)", fontsize=11)
        for a in axs:
            a.axis("off")
        fig.suptitle("卷积=局部加权求和：核扫过图像提取边缘", fontsize=12,
                     fontweight="bold")
    ani = FuncAnimation(fig, draw,
                        frames=list(range(36)) * 3 + [35] * 6, interval=420)
    save_mp4(ani, path, fps=3)
    plt.close(fig)


# ============== 4) 阈值分割对比 ==============
def video_threshold(path):
    rng = np.random.RandomState(5)
    x = np.linspace(0, 10, 240)
    y = np.linspace(0, 6, 180)
    X, Y = np.meshgrid(x, y)
    img = 0.45 + 0.1 * np.sin(X) + rng.normal(0, .05, X.shape)
    img[70:110, 90:150] = 0.9                 # 亮缺陷块
    img[130:150, 40:70] = 0.88
    fig, axs = plt.subplots(1, 3, figsize=(10, 3.4))
    ths = [0.5, 0.62, 0.75]

    def draw(k):
        for i, a in enumerate(axs):
            a.clear(); a.axis("off")
        axs[0].imshow(img, cmap="gray")
        axs[0].set_title("原图(含两处亮缺陷)", fontsize=11)
        th = ths[k % 3]
        bw = img > th
        axs[1].imshow(bw, cmap="gray")
        axs[1].set_title(f"全局阈值 th={th}", fontsize=11)
        n = int(bw.sum())
        axs[2].barh([0], [n], color=ORANGE)
        axs[2].barh([1], [int((img > 0.5).sum())], color=BLUE, alpha=.4)
        axs[2].set_yticks([0, 1]); axs[2].set_yticklabels(["当前检出px", "基准px"])
        axs[2].set_title(f"检出像素数 = {n}", fontsize=11)
        for sp in ["top", "right", "left"]:
            axs[2].spines[sp].set_visible(False)
        fig.suptitle("阈值决定检出与误检的平衡", fontsize=12, fontweight="bold")
    ani = FuncAnimation(fig, draw, frames=list(range(9)) * 4 + [8] * 5,
                        interval=900)
    save_mp4(ani, path, fps=1.5)
    plt.close(fig)


# ============== 5) 向量化加速赛跑 ==============
def video_vectorize(path):
    fig, ax = plt.subplots(figsize=(8, 4.5))

    def draw(k):
        ax.clear()
        rows = [("for循环", k * 0.9, "#44546A"), ("向量化", k * 4.2, ORANGE)]
        for i, (name, v, c) in enumerate(rows):
            ax.barh(i, min(v, 100), color=c, height=.5)
            ax.text(min(v, 100) + 1, i, f"{min(v,100):.0f}%",
                    va="center", fontsize=11, color=c, fontweight="bold")
        ax.set_yticks([0, 1]); ax.set_yticklabels(
            [f"{n}(慢)" if i == 0 else f"{n}(快100倍)" for i, n in
             enumerate(["for循环", "向量化"])])
        ax.set_xlim(0, 115); ax.set_xticks([])
        ax.set_title("同样求10万个平方：进度条赛跑", fontsize=12,
                     fontweight="bold")
        ax.spines[["top", "right"]].set_visible(False)
    ani = FuncAnimation(fig, draw,
                        frames=list(range(25)) * 3 + [24] * 6, interval=400)
    save_mp4(ani, path, fps=3)
    plt.close(fig)


if __name__ == "__main__":
    os.makedirs(f"{MAT}/01-AI应用基础/微课视频", exist_ok=True)
    os.makedirs(f"{MAT}/03-Python程序设计-项目实战/微课视频", exist_ok=True)
    os.makedirs(f"{MAT}/04-教学管理工具包/微课视频", exist_ok=True)
    video_sixstep(f"{MAT}/04-教学管理工具包/微课视频/六步法80分钟时间盒.mp4")
    video_window(f"{MAT}/01-AI应用基础/微课视频/滑动窗口与RUL预测.mp4")
    video_conv(f"{MAT}/01-AI应用基础/微课视频/卷积滑动演示.mp4")
    video_threshold(f"{MAT}/01-AI应用基础/微课视频/阈值分割对比.mp4")
    video_vectorize(f"{MAT}/03-Python程序设计-项目实战/微课视频/向量化加速赛跑.mp4")
    print("全部微课生成完成")
