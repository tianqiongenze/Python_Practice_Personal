# -*- coding: utf-8 -*-
"""AI48 视觉层：12张手绘插画 + 24个授课PPT（DeckV3 v9风格+每页讲稿）+ 元数据"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib                                   # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt                     # noqa: E402
from matplotlib import font_manager                 # noqa: E402
from matplotlib.patches import Circle, FancyBboxPatch, Wedge, Polygon  # noqa: E402

from gen_illustrations import stick, bubble, scene_ai, quotes_of  # noqa: E402
import sessions_ai48 as S                           # noqa: E402
import meta3_ai48 as M3                             # noqa: E402
import data_ai48 as D                               # noqa: E402
import universe as UNI                              # noqa: E402
from ppt_gen_v3 import DeckV3, _decorate            # noqa: E402
from sessions_meta import SIX                       # noqa: E402
from pptx.dml.color import RGBColor as _RC          # noqa: E402

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
ZH = font_manager.FontProperties(fname=FP).get_name()
NAVY, ORANGE = "#010328", "#F5670F"

OUTDIR = os.path.join(MAT, "05-AI应用基础48课时版")
PPTDIR = os.path.join(OUTDIR, "授课PPT")
ILLDIR = os.path.join(PPTDIR, "_场景插画")
os.makedirs(ILLDIR, exist_ok=True)

POSITION = [("课程性质", "专业核心课扩展版：48课时全谱系（数据→ML→DL→视觉→大模型→智能体）"),
            ("面向岗位", "AI应用工程师、工业视觉开发、工业互联网数据分析"),
            ("对接证书", "1+X AI应用实践（初级=M1-M3/中级=M4/高级=M5）"),
            ("课程衔接", "前：无Python先修（零基础·并行开设） → 本课(第4-15周·12周×4课时) → 后：项目实战/毕设")]
LITERACY = ["可信AI：模型要有据可查，指标不许造假",
            "工程纪律：限时调参与过程留痕",
            "团队与档案：竞标协作，档案袋沉淀三年资产"]


def gen_illus():
    with matplotlib.rc_context({"font.sans-serif": [ZH],
                                "axes.unicode_minus": False}):
        with plt.xkcd(scale=1.1, length=110, randomness=2):
            plt.rcParams["font.family"] = "sans-serif"
            plt.rcParams["font.sans-serif"] = [ZH]
            for w in range(4, 16):
                scen = UNI.SCEN.get(("ai48", w))
                if not scen:
                    continue
                q1, q2 = quotes_of(scen)
                fig, ax = plt.subplots(figsize=(8, 6), dpi=100)
                ax.set_xlim(0, 1); ax.set_ylim(0, .8); ax.axis("off")
                scene_ai(ax, q1, q2)
                ax.text(.5, .775, f"W{w:02d} 现场速写 · {UNI.DEPTS['ai48']['name']}",
                        ha="center", fontsize=10, color=NAVY, fontweight="bold")
                fig.savefig(os.path.join(ILLDIR, f"W{w}_场景.png"),
                            bbox_inches="tight", facecolor="white")
                plt.close(fig)
    print("illus: 12")


def build_ppts():
    count = pages = 0
    for s in S.SESSIONS:
        w, no = s["week"], s["no"]
        m3 = M3.AI48[w - 3]
        title = f"{s['woname']}"
        sub = f"第{w}周 · 第{no}次课（2课时 · 80分钟）"
        d = DeckV3()
        illus = os.path.join(ILLDIR, f"W{w}_场景.png")
        from env_tools import tool_for
        _tp, _ = tool_for("ai48", w)
        d.cover("AI应用基础（48课时版）", title[:20], sub,
                f"双创中心302实训室 · 理实一体 · 配套：分层工单+starter · 本课主用：{_tp}",
                dept=UNI.DEPTS["ai48"]["name"], illus=illus if os.path.exists(illus) else None)
        d.note(f"开场30秒：《{title}》，80分钟=2课时×40分钟。课前已发工单+微课知识卡。")
        AG = [("01", "课程定位", "课前已读", "性质·岗位·证书"),
              ("02", "课堂流程", "约2′", "80分钟时间盒与ABCD分层"),
              ("03", "目标与资讯·情境", "约5′", "目标+本课剧情"),
              ("04", "知识精讲", "约15′", "基础知识大卡+代码演示"),
              ("05", "任务实施", "六步法核心", "工单·分层·避坑"),
              ("06", "检查与评价", "约15′", "三层质检·当堂评分")]
        d.agenda(AG, tail="资讯·计划已课前线上完成——课堂从决策直接开始")
        d.note("议程页30秒：指读分钟归属，强调课前已完成资讯计划。")
        d.section("01", "课程定位", "本课在课程体系中的位置")
        d.note("过渡页：一句话点明为什么学、学了去哪。")
        d.positioning("AI应用基础（48课时版）", POSITION)
        d.note("念课程性质一行，指读证书衔接（30秒）。")
        d.mindmap(title[:8], [
            ("基础知识", m3["basics"][:2]),
            ("继续夯实", m3["basics"][2:4]),
            ("技能点", m3["skills"][:2]),
            ("分层任务", ["D跟做保底", "C基础完成", "B标准达成", "A进阶拓展"]),
            ("课堂评价", ["功能40%", "技术25%", "规范20%", "素养15%"])])
        d.note("知识地图：先见森林（40秒）。")
        d.section("02", "课堂流程", "80分钟时间盒")
        d.note("流程预告。")
        d.flow(SIX, "每课时40分钟 · 共80分钟（六步法课堂化）")
        d.note("决策10→实施40→检查10→实施30→评价10口径（4课时周两次课分摊）。")
        d.pace()
        d.note("ABCD分层节奏提醒。")
        d.section("03", "目标与资讯", "带着目标进课堂")
        d.note("PRIMM之Predict。")
        d.goals(["知识：" + m3["basics"][0],
                 "能力：" + m3["skills"][0],
                 "素质：数据诚信与工程纪律（课程思政）"])
        d.note("点读关键动词，对应工单验收口径。")
        d.review(s["quiz"][0], s["quiz"][1])
        d.note("课前测：点2人说答案，只追问为什么。")
        scen = UNI.SCEN.get(("ai48", w), "")
        d.scenario(scen, dept=UNI.DEPTS["ai48"]["name"],
                   illus=illus if os.path.exists(illus) else None)
        d.note(f"情境说书30秒：{scen[:60]}…\n抛问：'如果是你，第一步干什么？'")
        d.section("04", "知识精讲", "基础知识 → 技能 → 代码")
        d.note("先例后理。")
        for bi, bt in enumerate(m3["basics"][:6], 1):
            d.basic_card(bi, bt)
            d.note(f"知识卡{bi}：{bt[:30]}… 讲法：例子→定义→点1人复述。")
        d.quick_check(m3["basics"][:6])
        d.note("快查核对：遮左说右。")
        d.skills(m3["skills"])
        d.note("技能点=做完你应该会。")
        d.content(1, f"{title}（实施要点）",
                  [("· " + st) for st in s["steps"]])
        d.note("步骤清单与工单一一对应。")
        for ct, cc in m3["code"][:2]:
            d.code(ct, cc)
            d.note(f"演示《{ct}》：跑通→逐行→改参数（演的核心素材）。")
        d.fig_bars("80分钟时间盒分配（分钟）",
                   [("决策", 10, _RC(0x05, 0x45, 0xE8)),
                    ("实施一", 40, _RC(0x04, 0x75, 0xB6)),
                    ("检查", 10, _RC(0xF5, 0x67, 0x0F)),
                    ("实施二", 30, _RC(0x01, 0x75, 0x1F)),
                    ("评价", 10, _RC(0x44, 0x54, 0x6A))], ymax=40,
                   note="评价环节不压缩")
        d.note("强调时间盒纪律。")
        d.section("05", "任务实施", "工单 · 分层 · 避坑")
        d.note("先决策再领工单。")
        dec = s["dec"]
        d.decision(dec["title"], dec["header"], dec["rows"], dec.get("note", ""))
        d.note("决策矩阵：组内3分钟打分，结论理由入工单。")
        sp0 = s["sp"][0] if isinstance(s["sp"], list) else s["sp"]
        sg0 = s["sg"][0] if isinstance(s["sg"], list) else s["sg"]
        d.task(s["wono"], s["woname"], s["steps"], sp0, sg0)
        d.note(f"工单发布：'{UNI.DEPTS['ai48']['name']}工单{s['wono']}'——及格线{s['sp'][0]}。")
        tier_note = {"D": "D层跟做保底，领做做完即达标。",
                     "C": "C层独立完成，卡壳先查错误速查表。",
                     "B": "B层全功能+规范，帮带D/C。",
                     "A": "A层进阶拓展+2分钟展示（费曼带徒）。"}
        for tier in "DCBA":
            t = m3["abcd"][tier]
            d.tier_detail(tier, t["goal"], t["steps"], t["std"], None)
            d.note(tier_note[tier])
        d.errors(m3["errors"])
        e0 = m3["errors"][0]
        d.note(f"错误速查：现场制造「{e0[0]}」带学生三步排查。")
        if w == 15:
            d.fig_arch("12周成果综合链路（答辩一图贯通）", [
                ("智能体层", ["RAG问答(W13)", "调度决策(W14)"]),
                ("服务层", ["推理服务(W11)", "一键run"]),
                ("模型层", ["ML/CNN/ResNet", "YOLO/LLM"]),
                ("特征层", ["特征字典(W5)", "清洗质检(W4)"]),
                ("数据层", ["泵站日志", "缺陷图/知识库"])])
            d.note("答辩导航图：自下而上讲'数据→特征→模型→服务→智能体'，"
                   "每个方块对应一周工单——这就是'链路完整性'。")
        d.section("06", "检查与评价", "三层质检 · 评分 · 课后")
        d.note("收尾：检查+评价。")
        d.check()
        d.note("自检→互查签字→教师抽查。")
        d.submission(s["wono"])
        d.note("命名'学号_姓名_工单号.zip'，24h反馈。")
        d.literacy(LITERACY)
        d.note("素养页：点1个真实案例（30秒）。")
        d.thanks()
        d.note("下课：关机归位；课后微课+导学单。")
        # 37号轮：教材预习/检查知识点入演讲者备注
        _tb = D.WEEKS[s["week"] - 4].get("textbook", []) if hasattr(D, "WEEKS") else []
        if _tb:
            d.note("教材衔接：" + " | ".join(_tb))
        if w < 15:
            nxt = M3.AI48[w - 2]
            d.preview(nxt["skills"][0][:24], s["quiz"][0], w + 1)
            d.note("下次课预告：布置微课与导学单。")
        _decorate(d, "AI应用基础48课时版")
        fname = f"W{w:02d}-第{no}次课-{title[:12]}.pptx"
        d.save(os.path.join(PPTDIR, fname))
        count += 1
        pages += len(d.prs.slides._sldIdLst)
    print(f"PPT: {count}个, 平均{pages // max(count, 1)}页")


def metadata():
    import glob
    import datetime
    from pptx import Presentation
    NOW = datetime.datetime(2026, 9, 9)
    n = 0
    for p in glob.glob(os.path.join(PPTDIR, "*.pptx")):
        prs = Presentation(p)
        cp = prs.core_properties
        cp.title = os.path.basename(p)[:-5]
        cp.author = "工业互联网应用专业教学资源库"
        cp.subject = "AI48授课PPT（v9风格+讲稿）"
        cp.keywords = "两江智造;AI48;岗课赛证创;课程思政;双创中心302"
        cp.category = "高职高专教学文件"
        cp.comments = "48课时扩展版·每页备注为教师讲稿"
        cp.created = cp.modified = NOW
        prs.save(p)
        n += 1
    print("pptx metadata:", n)


if __name__ == "__main__":
    gen_illus()
    build_ppts()
    metadata()
