# -*- coding: utf-8 -*-
"""虚拟讲师"小郑"出镜层：绘制带透明通道的说话循环动画(prores4444)，叠加到36个微课右下角
口型随节奏开合+周期眨眼+安全帽/耳麦工装形象；不改变原视频内容与音轨。
输出: 各课程包/微课视频/数字人版/<原文件名>（原版保留）
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib                                   # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt                     # noqa: E402
from matplotlib import font_manager                 # noqa: E402
from matplotlib.patches import Circle, FancyBboxPatch, Wedge, Polygon  # noqa: E402

MAT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "教学实施资料")
FP = os.path.join(MAT, "fonts", "SourceHanSansCN-Regular.otf")
try:
    import matplotlib.font_manager as _fm
    _fm.fontManager.addfont(FP)
except Exception:
    pass
ZH = font_manager.FontProperties(fname=FP).get_name()
font_manager.fontManager.addfont(FP) if FP.endswith((".ttf", ".otf")) and not any(
    f.fname == FP for f in font_manager.fontManager.ttflist) else None
plt.rcParams["font.sans-serif"] = [ZH]
plt.rcParams["axes.unicode_minus"] = False

NAVY, ORANGE, BLUE = "#010328", "#F5670F", "#0545E8"
SKIN = "#F5D0A9"
FPS = 12
N = 60  # 5秒循环

MOUTH = [1, 4, 8, 5, 2, 6, 3, 7, 2, 5, 1, 4, 6, 2, 3]  # 口型开合序列(px)


def draw_avatar(frame_i, path):
    fig = plt.figure(figsize=(4.0, 3.0), dpi=100)
    fig.patch.set_alpha(0.0)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 4.0)
    ax.set_ylim(0, 3.0)
    ax.axis("off")
    t = frame_i % N
    blink = 18 <= (frame_i % N) <= 19 or 48 <= (frame_i % N) <= 49
    # ---- 定位：右下角 (x 10.1-12.4, y 0.35-2.35) ----
    cx, cy = 2.0, 1.35          # 头心（局部画布）
    # 阴影底座
    ax.add_patch(FancyBboxPatch((10.05, 0.30), 2.35, 2.05,
                                boxstyle="round,pad=0.06",
                                fc="white", ec="none", alpha=0.0))
    ax.add_patch(Circle((cx, 0.62), 0.95, fc=NAVY, ec="none", alpha=0.18))
    # 肩身（工装背心）
    ax.add_patch(Polygon([(cx - .92, .45), (cx + .92, .45), (cx + .62, 1.02),
                          (cx - .62, 1.02)], closed=True,
                         fc=BLUE, ec="white", lw=2))
    ax.plot([cx - .5, cx + .5], [.90, .90], color=ORANGE, lw=3)
    # 头
    ax.add_patch(Circle((cx, cy + .28), .50, fc=SKIN, ec=NAVY, lw=2))
    # 头发
    ax.add_patch(Wedge((cx, cy + .42), .50, 25, 155, fc="#3A2E22", ec="none"))
    # 安全帽
    ax.add_patch(Wedge((cx, cy + .48), .58, 0, 180, fc=ORANGE, ec=NAVY, lw=2))
    ax.add_patch(FancyBboxPatch((cx - .72, cy + .42), 1.44, .10,
                                boxstyle="round,pad=0.01", fc=ORANGE,
                                ec=NAVY, lw=1.5))
    # 耳麦
    ax.plot([cx - .58, cx - .58], [cy + .42, cy + .05], color=NAVY, lw=3)
    ax.add_patch(Circle((cx - .58, cy + .05), .08, fc=NAVY, ec="none"))
    ax.plot([cx - .58, cx - .30], [cy + .05, cy - .06], color=NAVY, lw=2)
    # 眼睛（眨眼=横线）
    if blink:
        ax.plot([cx - .26, cx - .10], [cy + .38, cy + .38], color=NAVY, lw=2)
        ax.plot([cx + .10, cx + .26], [cy + .38, cy + .38], color=NAVY, lw=2)
    else:
        ax.add_patch(Circle((cx - .18, cy + .38), .05, fc=NAVY, ec="none"))
        ax.add_patch(Circle((cx + .18, cy + .38), .05, fc=NAVY, ec="none"))
    # 口型（随序列开合）
    mh = MOUTH[t % len(MOUTH)] * 0.012
    ax.add_patch(FancyBboxPatch((cx - .13, cy + .10 - mh / 2), 0.26, mh,
                                boxstyle="round,pad=0.01", fc="#8C4A3A",
                                ec=NAVY, lw=1))
    # 头顶声波点（说话指示）
    for i in range(3):
        h = 0.06 + 0.05 * abs((t * 1.7 + i * 2) % 7 - 3.5) / 3.5 * 2
        ax.add_patch(FancyBboxPatch((cx + .45 + i * .16, cy + .78), .07, h,
                                    boxstyle="round,pad=0.005", fc=ORANGE,
                                    ec="none"))
    # 名牌
    ax.add_patch(FancyBboxPatch((cx - .55, .26), 1.10, .22,
                                boxstyle="round,pad=0.02", fc=NAVY, ec="none"))
    ax.text(cx, .37, "小郑 · 虚拟讲师", ha="center", va="center",
            fontsize=8.5, color="white", fontweight="bold")
    fig.savefig(path, transparent=True)
    plt.close(fig)


def build_avatar_mov(out_mov):
    tmp = "/tmp/avatar_frames"
    os.makedirs(tmp, exist_ok=True)
    for i in range(N):
        draw_avatar(i, os.path.join(tmp, f"a_{i:03d}.png"))
        print("frame", i, flush=True)
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i",
         f"{tmp}/a_%03d.png", "-frames:v", str(N), "-c:v", "prores_ks",
         "-profile:v", "4444", "-pix_fmt", "yuva444p10le", out_mov],
        check=True)
    print("avatar mov:", out_mov, os.path.getsize(out_mov) // 1024, "KB")


def overlay_all():
    mov = "/tmp/avatar_talk.mov"
    if not os.path.exists(mov):
        build_avatar_mov(mov)
    courses = ["01-AI应用基础", "02-程序设计基础",
               "03-Python程序设计-项目实战", "04-教学管理工具包"]
    n = 0
    for c in courses:
        srcd = os.path.join(MAT, c, "微课视频")
        outd = os.path.join(srcd, "数字人版")
        os.makedirs(outd, exist_ok=True)
        for f in sorted(os.listdir(srcd)):
            if not f.endswith(".mp4"):
                continue
            out = os.path.join(outd, f)
            subprocess.run(
                ["ffmpeg", "-y", "-v", "error",
                 "-i", os.path.join(srcd, f),
                 "-stream_loop", "-1", "-i", mov,
                 "-filter_complex",
                 "[1:v]overlay=x=W-w-30:y=H-h-120:shortest=1",
                 "-map", "0:v", "-map", "0:a?", "-c:v", "libx264",
                 "-preset", "medium", "-crf", "21", "-c:a", "copy",
                 "-movflags", "+faststart", out],
                check=True)
            n += 1
            print("overlay:", c, f, flush=True)
    print("OVERLAY DONE:", n)


if __name__ == "__main__":
    overlay_all()
