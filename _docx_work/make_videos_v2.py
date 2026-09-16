# -*- coding: utf-8 -*-
"""微课v3（配音版）：28课知识卡片 + 3部门剧场 = 31个mp4，全部带中文旁白
管线：macOS say(Eddy zh_CN)逐段合成 → 按音频时长定帧数（打字机自适应）→ matplotlib渲染 → ffmpeg合流
风格 = PPT模板DNA：藏青#010328/深蓝#0545E8/橙#F5670F，16:9 1280x720
无声回退：环境变量 NO_TTS=1 时退回纯动画
"""
import math
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib                                   # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt                     # noqa: E402
from matplotlib.animation import FuncAnimation      # noqa: E402
import matplotlib.animation as manim                # noqa: E402
from matplotlib import font_manager                 # noqa: E402
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle  # noqa: E402

import meta3_ai, meta3_py, meta3_pp            # noqa: E402
import sessions_meta as SM                      # noqa: E402
import universe as UNI                          # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAT = os.path.join(BASE, "教学实施资料")


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
font_manager.fontManager.addfont(FP)
plt.rcParams["font.sans-serif"] = [font_manager.FontProperties(fname=FP).get_name()]
plt.rcParams["axes.unicode_minus"] = False

NAVY, BLUE, ORANGE = "#010328", "#0545E8", "#F5670F"
SKY, GRAY, LIGHT = "#0475B6", "#44546A", "#F5F7FE"
FPS = 2
VOICE = "Eddy (Chinese (China mainland))"
NO_TTS = os.environ.get("NO_TTS") == "1"
TMPD = "/tmp/tts_segs"
os.makedirs(TMPD, exist_ok=True)

TASKS = []
AI_WONOS = ["M1.1", "M1.2", "M2.1", "M2.2", "M3.1", "M3.2", "M4.1", "M4.2"]
for i, w in enumerate(range(4, 12)):
    TASKS.append(("ai", w, meta3_ai.AI3[w], AI_WONOS[i],
                  SM.AI_META[w]["woname"], "01-AI应用基础", "AI应用基础"))
import meta3_ai48
A48W = [("M1-1a", "数据清洗与质量评估"), ("M1-1b", "特征设计与优化"),
        ("M2-1a", "传统分类：逻辑回归+决策树"), ("M2-2", "XGBoost参数调优"),
        ("M2-3a", "MLP神经网络"), ("M2-3b", "CNN或LSTM二选一"),
        ("M3-1", "ResNet迁移学习"), ("M3-2", "YOLO实时缺陷检测"),
        ("M4-1", "LLM故障诊断"), ("M4-2", "RAG知识库问答"),
        ("M5-1", "多智能体检修调度"), ("Z", "综合项目答辩")]
for i, w in enumerate(range(4, 16)):
    TASKS.append(("ai48", w, meta3_ai48.AI48[i + 1], A48W[i][0], A48W[i][1],
                  "05-AI应用基础48课时版", "AI应用基础（48课时版）"))
PYN = {1: "设备参数初始化系统", 2: "工业实时告警系统Ⅰ", 3: "工业实时告警系统Ⅱ",
       4: "工业设备类设计", 5: "工业设备继承体系", 6: "健壮的工业数据采集程序",
       7: "工业数据格式转换工具", 8: "工业数据文件处理系统",
       9: "工业故障分析报告生成系统", 10: "工业图像处理与报告生成",
       11: "工业互联网数据采集系统", 12: "综合项目数据处理系统"}
PYW = {1: "0.1", 2: "0.2a", 3: "0.2b", 4: "0.3", 5: "0.4", 6: "0.5", 7: "1.1",
       8: "1.2", 9: "1.3", 10: "1.4", 11: "1.5", 12: "Z"}
for w in range(1, 13):
    TASKS.append(("py", w, meta3_py.PY3[w], PYW[w], PYN[w], "02-程序设计基础",
                  "Python编程基础"))
PPW = {1: ("P1.1", "Python基础练习五题"), 2: ("P1.2", "标准Python工程模板"),
       3: ("P2.1", "Pandas数据处理管道"), 4: ("P2.2", "NumPy故障特征提取系统"),
       5: ("P3", "产线KPI仪表盘与自动日报"), 6: ("P4.1", "多源数据采集系统"),
       7: ("P5", "产线数据仓库与ORM"), 8: ("P6", "故障诊断模型与部署"),
       9: ("P7", "智能运维平台综合项目")}
for w in range(1, 10):
    TASKS.append(("pp", w, meta3_pp.PP3[w], PPW[w][0], PPW[w][1],
                  "03-Python程序设计-项目实战", "Python程序设计（项目实战）"))


# ---------------- TTS / 音视频工具 ----------------
def _dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", path], capture_output=True, text=True)
    return float(r.stdout.strip())


def tts(text, name):
    """合成一段旁白 → (m4a路径, 时长秒)。首尾留白使节奏自然。"""
    aiff = os.path.join(TMPD, name + ".aiff")
    m4a = os.path.join(TMPD, name + ".m4a")
    subprocess.run(["say", "-v", VOICE, "-r", "182", "-o", aiff, text], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", aiff,
                    "-af", "adelay=150,apad=pad_dur=0.5",
                    "-ar", "44100", "-ac", "1", "-c:a", "aac", "-b:a", "128k",
                    m4a], check=True)
    return m4a, _dur(m4a)


def concat_audio(files, out):
    lst = out + ".txt"
    with open(lst, "w") as f:
        for p in files:
            f.write(f"file '{p}'\n")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", lst, "-c", "copy", out], check=True)
    return _dur(out)


def mux(video, audio, out):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", video, "-i", audio,
                    "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "copy",
                    "-shortest", "-movflags", "+faststart", out], check=True)


def wrap(t, n=26):
    return "\n".join(t[i:i + n] for i in range(0, len(t), n))


def new_fig():
    fig = plt.figure(figsize=(12.8, 7.2), dpi=100)
    fig.patch.set_facecolor(NAVY)
    return fig


def clear(fig):
    fig.texts.clear()
    for ax in list(fig.axes):
        ax.remove()


def chip(fig, x, y, text, fc=ORANGE, fs=13):
    fig.text(x, y, f" {text} ", fontsize=fs, color="white", fontweight="bold",
             ha="left", va="center",
             bbox=dict(boxstyle="round,pad=0.45", fc=fc, ec="none"))


def speak_bars(fig, x, y, k):
    """旁白播放指示：三根随帧跳动的声波条"""
    for i in range(3):
        h = 0.012 + 0.010 * abs(math.sin(k * 0.9 + i * 1.3))
        fig.patches.append(Rectangle((x + i * 0.012, y), 0.007, h,
                                     transform=fig.transFigure,
                                     fc=ORANGE, ec="none"))


def footer(fig, cname, week):
    fig.text(0.045, 0.045, f"两江智造集团 · {cname}", fontsize=11, color=GRAY)
    fig.text(0.955, 0.045, f"W{week:02d} 知识卡" if week else "部门剧场",
             fontsize=11, color=GRAY, ha="right")


def card_bg(fig):
    fig.patch.set_facecolor(LIGHT)
    fig.add_artist(Rectangle((0, 0.92), 1, 0.08, fc=NAVY, ec="none",
                             transform=fig.transFigure, zorder=0))


def frames_for(dur, minimum=5):
    return max(minimum, math.ceil((dur + 0.1) * FPS))


# ============ 1) 每课基础知识卡片（配音版） ============
def video_cards(code, week, cname, woname, basics, folder):
    dept = UNI.DEPTS[code]["name"]
    n = len(basics)
    audios, durs, steps = [], [], [3] * n
    if not NO_TTS:
        segs = [(f"t{code}{week}",
                 f"{UNI.GROUP['name']}，{dept}。第{week}周，{cname}：{woname}。"
                 f"课前知识卡，一共{n}条，请边看边记。")]
        for i, b in enumerate(basics):
            segs.append((f"b{code}{week}_{i}", f"第{i + 1}条。{b}"))
        segs.append((f"o{code}{week}",
                     f"达标自测：合上视频想一想，这{n}条，你能各用一句话说清楚吗？"
                     "记下最模糊的一条，课堂决策环节优先提问。"
                     "带着卡片进课堂，实施环节直接用在分层工单上。"))
        for name, text in segs:
            m4a, d = tts(text, name)
            audios.append(m4a)
            durs.append(d)
        for i in range(n):
            steps[i] = max(3, math.ceil(len(basics[i]) / durs[i + 1] / FPS))
    states = ([("title", 0)] * frames_for(durs[0] if durs else 3)
              + [("card", i, c)
                 for i in range(n)
                 for c in range(frames_for(durs[i + 1] if durs else 4, 5))]
              + [("outro", 0)] * frames_for(durs[-1] if durs else 4))
    fig = new_fig()

    def draw(state):
        clear(fig)
        for r in list(fig.artists):
            r.remove()
        if state[0] == "title":
            fig.patch.set_facecolor(NAVY)
            chip(fig, 0.045, 0.86, f"◆ {UNI.GROUP['name']} · {dept}", fs=14)
            fig.text(0.5, 0.55, f"W{week:02d} · {woname}", fontsize=30,
                     color="white", fontweight="bold", ha="center")
            fig.text(0.5, 0.38, f"课前微课 · 基础知识卡（{n}条）", fontsize=17,
                     color="#9DB8F5", ha="center")
            fig.text(0.5, 0.24, "看完这张卡，课堂上的分层工单就不慌了",
                     fontsize=13, color=GRAY, ha="center")
            fig.text(0.5, 0.06, UNI.GROUP["logo_text"], fontsize=12,
                     color="#33477A", ha="center")
        elif state[0] == "card":
            _, i, c = state
            card_bg(fig)
            fig.text(0.045, 0.955, cname, fontsize=13, color="white",
                     fontweight="bold")
            fig.text(0.955, 0.955, f"第{i + 1} / {n} 条", fontsize=12,
                     color="white", ha="right")
            fig.patches.append(FancyBboxPatch(
                (0.10, 0.60), 0.80, 0.24,
                boxstyle="round,pad=0.02", fc="white", ec="#D8E0F5",
                transform=fig.transFigure, lw=1.5, zorder=1))
            chip(fig, 0.135, 0.72, f"B{i + 1:02d}", fs=17)
            txt = basics[i][:max(0, (c + 1) * steps[i])]
            fig.text(0.26, 0.72, wrap(txt, 30), fontsize=18, color=NAVY,
                     va="center", zorder=2)
            speak_bars(fig, 0.135, 0.625, c)
            for d in range(n):
                fig.patches.append(Circle((0.10 + d * 0.03, 0.50), 0.008,
                                          transform=fig.transFigure,
                                          fc=ORANGE if d <= i else "#C9D3E8"))
            fig.text(0.10, 0.42, "用你自己的话，向同桌复述一遍", fontsize=13,
                     color=GRAY)
            footer(fig, cname, week)
        else:
            fig.patch.set_facecolor(NAVY)
            chip(fig, 0.045, 0.80, "课前达标自检", fs=15)
            fig.text(0.10, 0.62,
                     f"□  这{n}条卡，我能各用一句话说清楚吗？",
                     fontsize=17, color="white")
            fig.text(0.10, 0.50, "□  记下最模糊的一条，课堂“决策”环节优先问",
                     fontsize=17, color="white")
            fig.text(0.10, 0.38, "□  带着卡进课堂：实施环节直接用在分层工单上",
                     fontsize=17, color="white")
            fig.text(0.5, 0.16, f"—— {UNI.GROUP['name']} · {dept} ——",
                     fontsize=13, color="#9DB8F5", ha="center")
        return []

    outdir = os.path.join(MAT, folder, "微课视频")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, f"W{week:02d}_知识卡片_{woname[:12]}.mp4")
    ani = FuncAnimation(fig, draw, frames=states, interval=500)
    if NO_TTS:
        ani.save(path, writer=manim.FFMpegWriter(fps=FPS, bitrate=2000))
    else:
        tmp = path.replace(".mp4", ".silent.mp4")
        ani.save(tmp, writer=manim.FFMpegWriter(fps=FPS, bitrate=2000))
        track = os.path.join(TMPD, f"track_{code}{week}.m4a")
        concat_audio(audios, track)
        mux(tmp, track, path)
        os.remove(tmp)
    plt.close(fig)
    print("saved:", os.path.basename(path), os.path.getsize(path) // 1024, "KB",
          round(_dur(path), 1), "s", flush=True)


# ============ 2) 部门剧场（配音版） ============
def video_theater(code, cname, folder, items):
    dept = UNI.DEPTS[code]
    P = (len(items) + 5) // 6
    audios, durs = [], []
    if not NO_TTS:
        segs = [("g" + code, UNI.GROUP["intro"]),
                ("o" + code,
                 "集团下设三大事业部：设备智能运维中心，对应AI应用基础课程；"
                 "精密制造事业部，对应Python编程基础课程；"
                 "数字化转型办公室，对应Python程序设计项目实战课程。"
                 f"本课程的使命是：{dept['mission']}"),
                ("p" + code, "本课程主要人物：" + dept["people"]),
                ("a" + code, "你将打交道的设备资产：" + dept.get("assets", ""))]
        for p in range(P):
            part = items[p * 6:(p + 1) * 6]
            segs.append((f"c{code}_{p}",
                         "剧情线，第" + "一二三四五"[p] + "部分。" +
                         "。".join(f"工单{wo}，第{w}周，{nm}" for wo, nm, w in part)))
        segs.append(("e" + code,
                     f"入职手续办理完毕。下一站：{dept['name']}，"
                     f"先完成工单{items[0][0]}。{dept['mission']}"))
        for name, text in segs:
            m4a, d = tts(text, name)
            audios.append(m4a)
            durs.append(d)
    kinds = ["group", "org", "people", "assets"] + ["arc"] * P + ["end"]
    counts = ([frames_for(d, 6) for d in durs] if durs else [6] * len(kinds))
    states = []
    for kind, cnt in zip(kinds, counts):
        if kind == "arc":
            p = len([s for s in states if s[0] == "arc"])
            states += [("arc", p)] * cnt
        else:
            states += [(kind, 0)] * cnt
    fig = new_fig()

    def draw(state):
        clear(fig)
        kind = state[0]
        if kind == "group":
            fig.patch.set_facecolor(NAVY)
            fig.text(0.5, 0.74, UNI.GROUP["name"], fontsize=38, color="white",
                     fontweight="bold", ha="center")
            fig.text(0.5, 0.62, UNI.GROUP["logo_text"], fontsize=15,
                     color=ORANGE, ha="center")
            fig.text(0.5, 0.40, wrap(UNI.GROUP["intro"], 30), fontsize=15,
                     color="#C9D6F8", ha="center", va="center")
            fig.text(0.5, 0.10, f"《{cname}》项目载体 · 开篇剧场", fontsize=12,
                     color=GRAY, ha="center")
        elif kind == "org":
            fig.patch.set_facecolor(LIGHT)
            fig.text(0.5, 0.90, "集团组织架构 · 三事业部", fontsize=20,
                     color=NAVY, fontweight="bold", ha="center")
            fig.patches.append(FancyBboxPatch(
                (0.36, 0.68), 0.28, 0.11, boxstyle="round,pad=0.015",
                fc=NAVY, ec="none", transform=fig.transFigure))
            fig.text(0.5, 0.735, UNI.GROUP["name"], fontsize=15, color="white",
                     ha="center", va="center")
            for k, (xx, dd) in enumerate([(0.08, "ai"), (0.395, "py"), (0.71, "pp")]):
                hot = dd == code
                fig.patches.append(FancyBboxPatch(
                    (xx, 0.38), 0.21, 0.20, boxstyle="round,pad=0.015",
                    fc=ORANGE if hot else "#DDE4F2", ec="none",
                    transform=fig.transFigure))
                fig.text(xx + 0.105, 0.52, UNI.DEPTS[dd]["name"], fontsize=12.5,
                         color="white" if hot else NAVY, ha="center",
                         fontweight="bold" if hot else "normal")
                fig.text(xx + 0.105, 0.44, ["AI应用基础", "Python编程基础",
                                             "Python项目实战"][k], fontsize=11,
                         color="white" if hot else GRAY, ha="center")
            fig.add_artist(plt.Line2D([0.5, 0.5], [0.68, 0.63], color="#B9C4DC",
                                      lw=1.6, transform=fig.transFigure))
            fig.add_artist(plt.Line2D([0.185, 0.815], [0.63, 0.63],
                                      color="#B9C4DC", lw=1.6,
                                      transform=fig.transFigure))
            for xx, hot in [(0.08, code == "ai"), (0.395, code == "py"),
                            (0.71, code == "pp")]:
                fig.add_artist(plt.Line2D([xx + 0.105, xx + 0.105],
                                          [0.63, 0.58],
                                          color=ORANGE if hot else "#B9C4DC",
                                          lw=2.5 if hot else 1.6,
                                          transform=fig.transFigure))
            fig.text(0.5, 0.28, wrap("本课程使命：" + dept["mission"], 34),
                     fontsize=14, color=NAVY, ha="center", va="center")
            fig.text(0.5, 0.12, "你将以“小郑”的身份在这里入职、闯关、交付",
                     fontsize=13, color=ORANGE, ha="center")
        elif kind == "people":
            fig.patch.set_facecolor(LIGHT)
            chip(fig, 0.045, 0.86, "主要人物（剧情贯穿全课程）", fs=15)
            fig.patches.append(FancyBboxPatch(
                (0.07, 0.30), 0.86, 0.46, boxstyle="round,pad=0.02", fc="white",
                ec="#D8E0F5", transform=fig.transFigure, lw=1.5))
            fig.text(0.11, 0.53, wrap(dept["people"], 40), fontsize=17,
                     color=NAVY, va="center")
            for i, (nm, desc) in enumerate(UNI.PEOPLE_CARD[:3]):
                fig.text(0.11 + i * 0.30, 0.38, f"· {nm}", fontsize=12,
                         color=GRAY)
            footer(fig, cname, None)
        elif kind == "assets":
            fig.patch.set_facecolor(LIGHT)
            chip(fig, 0.045, 0.86, "你将打交道的设备资产", fs=15, fc=SKY)
            fig.patches.append(FancyBboxPatch(
                (0.07, 0.42), 0.86, 0.30, boxstyle="round,pad=0.02", fc="white",
                ec="#D8E0F5", transform=fig.transFigure, lw=1.5))
            fig.text(0.11, 0.57, wrap(dept.get("assets", ""), 44), fontsize=17,
                     color=NAVY, va="center")
            fig.text(0.5, 0.22, "数据都来自这些设备——工单里的每一行代码都作用于此",
                     fontsize=13, color=GRAY, ha="center")
            footer(fig, cname, None)
        elif kind == "arc":
            p = state[1]
            fig.patch.set_facecolor(NAVY)
            chip(fig, 0.045, 0.88,
                 f"剧情线 · 工单闯关（{p + 1}/{(len(items) + 5) // 6}）", fs=15)
            for j, (wo, nm, wk) in enumerate(items[p * 6:(p + 1) * 6]):
                y = 0.74 - j * 0.115
                fig.patches.append(FancyBboxPatch(
                    (0.07, y - 0.035), 0.10, 0.075, boxstyle="round,pad=0.008",
                    fc=ORANGE, ec="none", transform=fig.transFigure))
                fig.text(0.12, y, wo, fontsize=13, color="white", ha="center",
                         va="center", fontweight="bold")
                fig.text(0.20, y, f"W{wk:02d}  {nm}", fontsize=14.5,
                         color="white", va="center")
            footer(fig, cname, None)
        else:
            fig.patch.set_facecolor(NAVY)
            fig.text(0.5, 0.66, "入职手续办理完毕", fontsize=26, color="white",
                     fontweight="bold", ha="center")
            fig.text(0.5, 0.50, f"下一站：{dept['name']} · 工单{items[0][0]}",
                     fontsize=18, color=ORANGE, ha="center")
            fig.text(0.5, 0.34, wrap(dept["mission"], 34), fontsize=14,
                     color="#C9D6F8", ha="center", va="center")
            fig.text(0.5, 0.12, UNI.GROUP["logo_text"], fontsize=12,
                     color="#33477A", ha="center")
        return []

    outdir = os.path.join(MAT, folder, "微课视频")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, f"部门剧场_{dept['name']}.mp4")
    ani = FuncAnimation(fig, draw, frames=states, interval=500)
    if NO_TTS:
        ani.save(path, writer=manim.FFMpegWriter(fps=FPS, bitrate=2000))
    else:
        tmp = path.replace(".mp4", ".silent.mp4")
        ani.save(tmp, writer=manim.FFMpegWriter(fps=FPS, bitrate=2000))
        track = os.path.join(TMPD, f"track_t{code}.m4a")
        concat_audio(audios, track)
        mux(tmp, track, path)
        os.remove(tmp)
    plt.close(fig)
    print("saved:", os.path.basename(path), os.path.getsize(path) // 1024, "KB",
          round(_dur(path), 1), "s", flush=True)


if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for code, w, m3, wo, nm, folder, cn in TASKS:
        if only and only != code:
            continue
        video_cards(code, w, cn, nm, m3["basics"], folder)
    if not only or only == "theater":
        for code, folder, cn in [("ai", "01-AI应用基础", "AI应用基础"),
                                 ("py", "02-程序设计基础", "Python编程基础"),
                                 ("pp", "03-Python程序设计-项目实战",
                                  "Python程序设计（项目实战）"),
                                 ("ai48", "05-AI应用基础48课时版",
                                  "AI应用基础（48课时版）")]:
            items = [(wo, nm, w) for c, w, _m, wo, nm, _f, _n in TASKS if c == code]
            video_theater(code, cn, folder, items)
    print("ALL DONE")
