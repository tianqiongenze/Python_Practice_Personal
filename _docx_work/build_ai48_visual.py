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
        # 52号轮扩展：目录+图谱分支+课证对照+小结
        d.content(22, "本课目录（结构速览）", [
            "①课程定位：定位/知识地图/课证赛岗——为什么学这门课",
            "②课堂流程：80分钟时间盒/分层节奏——今天怎么安排",
            "③目标与情境：三维目标/剧情拆解/随堂自测——学什么",
            "④知识精讲：知识卡×应用×深化×代码走读——怎么教",
            "⑤任务实施：工单/四层任务/避坑/核对清单——怎么做",
            "⑥检查评价+⑦拓展：质检/评分/工具箱/一图流——怎么收"])
        d.note("目录页：给学生'地图感'，30秒。")
        d.content(28, "怎么用好这套PPT（使用说明）", [
            "课前：只看①②③——定位/流程/目标，带问题来",
            "课中：跟着④⑤走——知识卡打地基，工单练技能",
            "卡住：查⑤避坑+错误速查，再举手",
            "课后：⑦拓展自测+预习清单——闭环从课后开始",
            "这份PPT=教材+工单说明书+复习提纲三合一"])
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
        d.content(1, "知识地图分支详解（一）", [
            f"基础知识线：{'；'.join(m3['basics'][:2])}",
            f"继续夯实线：{'；'.join(m3['basics'][2:4])}",
            "两条线的关系：先打地基（概念），再上楼层（组合应用）",
            "学法提示：每条知识都配'产线例子'，先例后理"])
        d.content(2, "知识地图分支详解（二）", [
            f"技能线：{'；'.join(m3['skills'][:2])}",
            "分层任务线：D跟做→C独立→B帮带→A拓展（每4周动态升降）",
            "课堂评价线：功能40%+技术25%+规范20%+素养15%",
            "三条线闭环：技能靠任务练，任务按评价收"])
        d.extend_page("岗课赛证对照（本课坐标）", [
            ("岗", UNI.DEPTS["ai48"]["name"] + "：AI应用工程师、工业视觉开发"),
            ("课", f"{s['wono']}《{s['woname']}》——本课工单即考核单元"),
            ("证", "1+X AI应用实践（初级=M1-M3/中级=M4）——本课工单即考点"),
            ("赛", "世界职业院校技能大赛（人工智能赛道）——数据处理/模型赛项")])
        d.recap("01", "课程定位", [
            "本课在M1-M5全谱系中的位置已明确",
            "知识地图五分支：基础→夯实→技能→分层→评价",
            "岗课赛证四维坐标——带着目标进课堂"])
        d.section("02", "课堂流程", "80分钟时间盒")
        d.note("流程预告。")
        d.flow(SIX, "每课时40分钟 · 共80分钟（六步法课堂化）")
        d.note("决策10→实施40→检查10→实施30→评价10口径（4课时周两次课分摊）。")
        d.pace()
        d.note("ABCD分层节奏提醒。")
        # 52号轮：产业数据+小结
        d.fig_bars("两江智造产线运营指标（虚拟产线月度数据）",
                   [("模型准确率(%)", 92, _RC(0x05, 0x45, 0xE8)),
                    ("推理耗时(ms/条)", 45, _RC(0x04, 0x75, 0xB6)),
                    ("人工复核率(%)", 15, _RC(0xF5, 0x67, 0x0F))],
                   note="数据来自虚拟产线——你训的模型就在处理这些数据")
        d.note("产业数据卡：学的技能=产线的数字。")
        d.recap("02", "课堂流程", [
            "六步法：决策10→实施40→检查10→实施30→评价10",
            "分层节奏：D/C/B/A各就各位，每4周动态升降",
            "评价10分钟不压缩——当堂评分、24小时反馈"])
        d.section("03", "目标与资讯", "带着目标进课堂")
        d.note("PRIMM之Predict。")
        d.goals(["知识：" + m3["basics"][0],
                 "能力：" + m3["skills"][0],
                 "素质：数据诚信与工程纪律（课程思政）"])
        d.note("点读关键动词，对应工单验收口径。")
        d.review(s["quiz"][0], s["quiz"][1])
        d.note("课前测：点2人说答案，只追问为什么。")
        # 52号轮：逐题精讲+目标三维页
        d.content(18, "课前测逐题精讲（错得最多的那道）", [
            f"题目：{str(s['quiz'][0])[:56]}",
            "正确思路：从'考哪个知识卡'入手——先定位再作答",
            "常见错误：背概念不看场景；模型题不看数据分布先猜",
            "本课回收：考点会在知识卡与随堂自测中再次出现"])
        d.content(10, "知识目标：怎么学·怎么证", [
            f"目标：{m3['basics'][0][:56]}",
            "怎么学：知识卡先例后理→快查核对→应用页回到产线场景",
            "怎么证：课前quiz+随堂自测+工单'技术质量25%'项",
            "达标线：能复述定义+能说出产线例子=过关"])
        d.content(11, "能力目标：怎么练·怎么证", [
            f"目标：{m3['skills'][0][:56]}",
            "怎么练：starter跟做（D）→独立完成（C）→规范+帮带（B）→拓展（A）",
            "怎么证：工单'功能40%'全项+指标达标+运行截图贴过程记录",
            "达标线：代码能跑+指标达工单线=过关"])
        d.content(12, "素质目标：怎么养·怎么证", [
            "目标：数据诚信与工程纪律（课程思政融入）",
            "怎么养：指标不造假/随机种子可复现/调参留痕——每个工单都在练",
            "怎么证：Git提交历史（每周≥1次）+工单'素养15%'项",
            "达标线：实验可复现+提交记录连续=过关"])
        scen = UNI.SCEN.get(("ai48", w), "")
        d.scenario(scen, dept=UNI.DEPTS["ai48"]["name"],
                   illus=illus if os.path.exists(illus) else None)
        d.note(f"情境说书30秒：{scen[:60]}…\n抛问：'如果是你，第一步干什么？'")
        # 52号轮：剧情拆解+目标对照+随堂自测+小结
        d.content(3, "剧情拆解：任务 → 冲突 → 你的决策", [
            f"任务背景：{scen[:52] or s['woname']}",
            "冲突点：数据量/模型选型/算力时限——手工做不完，必须建模",
            "决策点：用什么模型？怎么验证？指标线定多少？",
            "带着这三个问题进知识精讲——每个知识点都是解药"])
        d.practice(4, str(s["quiz"][0])[:52], str(s["quiz"][1])[:52])
        d.practice(5, f"出现「{m3['errors'][0][0]}」，你的排查顺序是？",
                   f"提示: 原因是{m3['errors'][0][1]}")
        d.practice(6, f"复述：{m3['basics'][0][:44]}", "用自己的话讲给同桌——讲得清才算懂")
        d.note("随堂自测三题：先答后揭晓，答对记过程分。")
        d.recap("03", "目标与资讯·情境", [
            "三维目标已明确，达标口径=工单评分表",
            f"剧情任务：{scen[:32] or s['woname']}",
            "随堂自测完成第一次探测，带着问题进精讲"])
        d.section("04", "知识精讲", "基础知识 → 技能 → 代码")
        d.note("先例后理。")
        for bi, bt in enumerate(m3["basics"][:6], 1):
            d.basic_card(bi, bt)
            d.note(f"知识卡{bi}：{bt[:30]}… 讲法：例子→定义→点1人复述。")
            # 52号轮：应用页
            _main, _app = (bt.split("——应用：", 1) + [None])[:2] if "——应用：" in bt else (bt, None)
            if _app:
                _code_line = _app if any(ch in _app for ch in "=()[]{}:") else ""
                d.apply_page(bi, _main.strip()[:22],
                             f"{_main.strip()}。在两江智造产线上的用法：{_app.strip()[:86]}",
                             _code_line[:200])
                d.note(f"应用页{bi}：知识点放回产线场景——先看输出再看定义。")
        d.quick_check(m3["basics"][:6])
        d.note("快查核对：遮左说右。")
        d.content(4, "深化理解：逐条讲透（A层费曼素材）", [
            f"要点1：{m3['basics'][0][:52]}",
            f"要点2：{m3['basics'][1][:52]}" if len(m3["basics"]) > 1 else "要点2：见微课深化",
            f"要点3：{m3['basics'][2][:52]}" if len(m3["basics"]) > 2 else "要点3：见多解法手册",
            "学法：A层用自己的话讲给D层听——讲得清才是真懂"])
        d.skills(m3["skills"])
        d.note("技能点=做完你应该会。")
        d.content(5, "技能点 → 工单步骤 → 得分点", [
            f"技能{i+1}：{sk[:44]} → 对应工单步骤，占功能分"
            for i, sk in enumerate(m3["skills"][:4])] + [
            "提示：技能点全部来自工单评分点——练技能=挣分数"])
        d.content(1, f"{title}（实施要点）",
                  [("· " + st) for st in s["steps"]])
        d.note("步骤清单与工单一一对应。")
        for ct, cc in m3["code"][:2]:
            d.code(ct, cc)
            d.note(f"演示《{ct}》：跑通→逐行→改参数（演的核心素材）。")
            # 52号轮：代码走读
            _lines = [ln for ln in cc.splitlines() if ln.strip()][:5]
            d.content(17, f"代码走读：《{ct[:16]}》逐段拆解", [
                f"行{i+1}：{ln.strip()[:52]}" for i, ln in enumerate(_lines)] + [
                "读法：先看每行的输出→再问'为什么这么写'→最后改参数看变化"])
        d.fig_flow("本次课六步法流程", [
            "决策：定方案·选模型", "实施一：数据+建模",
            "检查：自检互查", "实施二：调优+拓展",
            "评价：当堂评分", "课后：微课预习"],
            "六步法课堂化——每次课都知道现在在哪一步")
        d.note("流程图页：作为'我们现在在哪一步'的路标。")
        d.fig_bars("80分钟时间盒分配（分钟）",
                   [("决策", 10, _RC(0x05, 0x45, 0xE8)),
                    ("实施一", 40, _RC(0x04, 0x75, 0xB6)),
                    ("检查", 10, _RC(0xF5, 0x67, 0x0F)),
                    ("实施二", 30, _RC(0x01, 0x75, 0x1F)),
                    ("评价", 10, _RC(0x44, 0x54, 0x6A))], ymax=40,
                   note="评价环节不压缩")
        d.note("强调时间盒纪律。")
        d.content(26, "本课术语表（听不懂时查这里）", [
            f"术语①：{m3['basics'][0].split('：')[0][:24]}——{m3['basics'][0].split('：')[1][:40] if '：' in m3['basics'][0] else m3['basics'][0][:44]}",
            f"术语②：{m3['basics'][1][:52]}" if len(m3["basics"]) > 1 else "术语②：见微课",
            f"术语③：{m3['skills'][0][:52]}",
            "用法：教师说术语→学生查表——第一周建立'术语-含义'反射"])
        d.section("05", "任务实施", "工单 · 分层 · 避坑")
        d.note("先决策再领工单。")
        dec = s["dec"]
        d.decision(dec["title"], dec["header"], dec["rows"], dec.get("note", ""))
        d.note("决策矩阵：组内3分钟打分，结论理由入工单。")
        d.content(23, "决策怎么下：方案对比三问", [
            f"本课决策题：{dec['title'][:44]}",
            "问①可行吗——每个方案的实现路径走得通吗（技术风险）",
            "问②值吗——精度/耗时/可复现性三角权衡（工程账）",
            "问③谁拍板——组内数据说话，理由写进工单（决策追责制）",
            "规则：没有记录的决策=没有决策——写下来才算数"])
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
            # 52号轮：每层步骤详解
            _tn = {"D": "学徒", "C": "操作员", "B": "组长", "A": "师傅"}[tier]
            d.content(13 + "DCBA".index(tier),
                      f"{tier}层·{_tn}：步骤怎么走", [
                          f"第{i+1}步：{str(st)[:50]}" for i, st in
                          enumerate(t["steps"][:4])] + [
                          f"达标自检：{t['std'][:44]}"])
        d.errors(m3["errors"])
        e0 = m3["errors"][0]
        d.note(f"错误速查：现场制造「{e0[0]}」带学生三步排查。")
        d.practice(2, f"运行时出现「{e0[0]}」，你的排查顺序是？",
                   f"提示: 原因是{e0[1]}")
        d.steps_caution(s["steps"], [f"步骤{i+1}先看工单样例再动手" for i in range(min(3, len(s["steps"])))])
        d.note("避坑清单：每条问'为什么会踩'——把'注意'变成'知道为什么注意'。")
        # 52号轮：四层总览+核对清单+小结
        d.content(6, "ABCD四层任务总览（先看全貌再领任务）", [
            f"D·学徒（≥60）：{m3['abcd']['D']['goal'][:40]}——跟做保底",
            f"C·操作员（≥70）：{m3['abcd']['C']['goal'][:40]}——基础完成",
            f"B·组长（≥80）：{m3['abcd']['B']['goal'][:40]}——标准达成+帮带",
            f"A·师傅（≥90）：{m3['abcd']['A']['goal'][:40]}——进阶拓展+费曼讲解",
            "规则：每人按工单勾选自己的层；每4周动态升降"])
        d.content(7, "操作核对清单（做完一条勾一条）", [
            f"□ 步骤{i+1}：{str(st)[:48]}" for i, st in enumerate(s["steps"][:5])] + [
            "□ 全部勾完→同桌互查签字→提交工单"])
        d.content(8, "提交前最后一查（90秒）", [
            "□ 代码能从头跑到尾不报错（python xx.py再跑一遍）",
            "□ 指标达标：准确率/F1/耗时对齐工单及格线",
            "□ 随机种子已固定（random_state=42）——结果可复现",
            "□ 文件命名：学号_姓名_工单号.py+模型文件",
            "□ conda环境正确（提示符显示(ai48)）再运行"])
        d.recap("05", "任务实施", [
            f"工单{s['wono']}已发布，四层任务各自认领",
            "避坑清单+错误速查在手，卡壳先自查再举手",
            "操作核对清单做完勾选，提交前90秒最后一查"])
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
        d.extend_page("A层加餐：原理深挖（选读）", [
            ("为什么有效", f"{m3['basics'][0][:40]}——背后是统计/优化原理"),
            ("怎么验证", "改一个参数跑对比实验——用数据说话，不凭感觉"),
            ("边界在哪", "什么场景会失效？——数据漂移/样本不平衡/泄漏"),
            ("延伸阅读", "微课深化版+多解法手册——A层自己挖")])
        d.literacy(LITERACY)
        d.note("素养页：点1个真实案例（30秒）。")
        # 52号轮：评分细则+FAQ+资源+小结
        d.decision("工单评分细则（四级量表）",
                   ("等级", "达标线", "对应要求"),
                   [("A·师傅", "≥90分", "进阶拓展完成+2分钟费曼展示"),
                    ("B·组长", "≥80分", "全功能+代码规范+帮带D/C层"),
                    ("C·操作员", "≥70分", "基础功能完成+错误速查自查"),
                    ("D·学徒", "≥60分", "跟做完成核心步骤+达标自评")],
                   note="功能40%+技术质量25%+代码规范20%+工程素养15%")
        d.extend_page("高频FAQ（先自查再举手）", [
            ("torch安装失败", "用--index-url cpu官方源；确认在ai48环境里装"),
            ("模型指标波动大", "设random_state=42；数据先shuffle再划分"),
            ("ONNX推理不一致", "对齐预处理——同一scaler/归一化参数")])
        d.extend_page("资源导航（卡住时按顺序查）", [
            ("工单", f"{s['wono']}任务书——步骤/及格线/评分细则都在里面"),
            ("starter", f"学生代码框架/w{w-3}_xxx_starter.py——TODO注释即步骤提示"),
            ("软件指南", "../软件操作指南/——PyCharm/Jupyter/Git/Anaconda六份图文"),
            ("Jupyter", "Jupyter实训/——本周notebook师生版"),
            ("Git提交", "做完按Ctrl+K提交推送——每周至少1次")])
        d.recap("06", "检查与评价", [
            "三层质检：自检→互查签字→教师抽查",
            "评分四级量表+四权重已明确，24小时内反馈",
            "课后任务+下次课预告形成学习闭环"])
        # ===== 52号轮 第七部分 拓展与自测 =====
        d.section("07", "拓展与自测", "把今天的能力圈再画大一圈")
        d.extend_page("产业应用案例（学这个能干什么）", [
            ("真实场景", "质检靠老师傅目检，漏检率高且疲劳"),
            ("用什么解决", "分类模型+阈值规则——先自动化易判样本，人只复核疑难"),
            ("本课对应", f"{s['wono']}的技能点即其最小实现"),
            ("延伸方向", "视觉检测（M3）/大模型辅助诊断（M4）")])
        d.extend_page("多解法一瞥（同一任务的不同打法）", [
            ("解法A·直白", "按工单步骤顺序实现——好懂好调试，D/C层路线"),
            ("解法B·工程", "函数封装+管道化——可复用，B层路线"),
            ("解法C·进阶", "集成/调参/特征工程组合拳——冲指标，A层路线"),
            ("怎么选", "先让它跑起来→再让它对→最后让它准（KISS原则）")])
        d.extend_page("课程思政：如盐入水（30秒一个点）", [
            ("数据诚信", "指标不许造假——改数字骗过测试=产线事故的起点"),
            ("可解释性", "不迷信黑盒——每个预测能说出'为什么'才敢上线"),
            ("算力节约", "CPU优先调优——绿色计算从课堂开始"),
            ("职业底线", "模型抄袭=岗位上的'无证驾驶'")])
        d.extend_page("学习策略：这门课怎么学最有效", [
            ("先例后理", "先跑代码看结果，再回头懂原理——PRIMM教学法"),
            ("费曼技巧", "A层讲给D层听——讲得清才是真懂"),
            ("错题资产", "每个报错记入错误速查表——期末它是复习宝典"),
            ("提交习惯", "小步提交——调参每进一步就commit，回退不求人")])
        d.content(19, "进阶路线图（从今天的课往哪走）", [
            "本周：单点技能→下周：组合应用→W15：综合链路答辩",
            "横向：M1数据→M2模型→M3视觉→M4大模型→M5智能体（全谱系）",
            "纵向：证书线——1+X初级（M1-M3）→中级（M4）",
            "竞赛线：校级选拔→世界职业院校技能大赛（人工智能赛道）",
            "岗位线：跟做学徒→独立调参→带组师傅→AI应用工程师"])
        d.fig_bars("本周各层达标预期（%）",
                   [("D层·跟做保底", 100, _RC(0x44, 0x54, 0x6A)),
                    ("C层·基础完成", 80, _RC(0x04, 0x75, 0xB6)),
                    ("B层·标准达成", 60, _RC(0x05, 0x45, 0xE8)),
                    ("A层·进阶拓展", 30, _RC(0xF5, 0x67, 0x0F))],
                   note="预期≠上限：动态升降制下人人可冲上一层")
        d.content(20, "课前预习清单（下次课前完成）", [
            f"微课知识卡：{m3['skills'][0][:32]}（5分钟视频+导学单）",
            "Jupyter实训notebook：先跑教师版看答案，再试学生版",
            "预习快问：下次课quiz从微课与导学单出题——带着答案来",
            "Git推送本周工单：还没提交的课后补上"])
        d.content(21, "知识口袋书（本课概念速记）", [
            f"① {(m3['basics'][0].split('——')[0])[:44]}",
            f"② {(m3['basics'][1].split('——')[0])[:44]}" if len(m3["basics"]) > 1 else "② 见微课",
            f"③ {(m3['basics'][2].split('——')[0])[:44]}" if len(m3["basics"]) > 2 else "③ 见多解法",
            "用法：睡前30秒过一遍——口袋书越翻越薄，技能越练越厚"])
        d.extend_page("输出对比：好的 vs 差的（规范从第一课开始）", [
            ("好的输出", "指标+阈值结论+随机种子——三件套齐全可复现"),
            ("差的输出", "只报一个准确率——无种子无阈值，跑第二遍就对不上"),
            ("差多少分", "技术25%+素养15%两项就能差出40分"),
            ("为什么", "工业模型要给人信——复现不了的指标=没交付")])
        d.mindmap(title[:8], [
            ("知识回顾", m3["basics"][:2]),
            ("技能回顾", m3["skills"][:2]),
            ("易错回顾", [e[0] for e in m3["errors"][:2]] if len(m3["errors"]) >= 2 else ["见错误速查表"]),
            ("交付物", [f"工单{s['wono']}"])],
            title="全课知识图谱回顾（一图收束）")
        d.extend_page("常见场景应对（卡住了怎么办）", [
            ("场景①代码报错", "读报错最后一行→查错误速查表→举手（附截图）"),
            ("场景②不知道做啥", "回看操作核对清单□——第一个没勾的就是下一步"),
            ("场景③做完了", "90秒最后一查→Git提交→帮同组D/C层"),
            ("场景④提前全完成", "A层拓展→费曼准备→预习下次课微课")])
        d.extend_page("微课与自学资源（课后补弱/拓强）", [
            ("微课知识卡", f"本周主题：{m3['skills'][0][:32]}"),
            ("数字人版", "同内容数字人讲解——喜欢听的换着看"),
            ("Jupyter师生版", "教师版有完整答案——先看懂再独立做"),
            ("多解法手册", "教师参考/——同一任务三种深度解法")])
        d.content(24, "答辩预演（期末综合链路的彩排）", [
            "①30秒讲需求：这个模型解决什么问题、部署在哪",
            "②60秒讲链路：数据→特征→模型→评估→部署（五段式）",
            "③60秒讲亮点：我踩过的坑+怎么爬出来（错误速查表就是素材）",
            "④答辩礼仪：指着屏幕讲不念稿；被问住就说'课后验证'",
            "从本周开始练——W15答辩=12周彩排的总和"])
        d.content(25, "课堂实录清单（过程性考核证据）", [
            "□ 运行截图：训练日志+指标输出同框",
            "□ 工单过程栏：步骤勾选+调参记录+自查记录",
            "□ Git提交：本次课至少1条commit",
            "□ 同伴签字：互查通过后签名",
            "四项齐全=过程分满分；缺一项课后24小时内补齐"])
        d.content(9, "今日一图流总结（贴脑墙上）", [
            f"知识：{'；'.join(bt.split('——')[0][:20] for bt in m3['basics'][:3])}",
            f"技能：{'；'.join(m3['skills'][:2])}",
            f"交付：工单{s['wono']}《{s['woname']}》",
            "习惯：调参每进一步就commit——每周至少1次",
            "明日：课前微课+导学单（下次课quiz从中出题）"])
        d.content(27, "睡前自查三问（30秒）", [
            "问①今天的核心概念能一句话说清吗？——说不清回看知识卡",
            "问②工单步骤全部勾完了吗？——没勾的明早第一件事",
            "问③Git推送今天做了吗？——每周至少1次，工程素养分依据",
            "三问通过=今天闭环；明天从微课开始"])
        # 52号轮：学习工具箱三页
        d.extend_page("工具箱①：Git提交四步（每周必做）", [
            ("第1步·暂存", "PyCharm按 Ctrl+K → 勾选改动文件"),
            ("第2步·提交", "Commit Message 按前缀写：feat:完成W%d工单" % w),
            ("第3步·推送", "Ctrl+Shift+K 推送——云端可查才算交"),
            ("第4步·验证", "网页刷新看到新提交=成功；每周≥1次")])
        d.extend_page("工具箱②：conda环境三命令", [
            ("激活", "conda activate ai48——提示符变(ai48)才对"),
            ("装包", "激活后再 pip install——装错环境=白装"),
            ("核对", "python -c \"import sys; print(sys.executable)\" 路径含envs")])
        d.extend_page("工具箱③：PyCharm效率五键", [
            ("Shift+F10", "运行当前文件（^R macOS）"),
            ("Shift+F9", "调试——断点停在红点行"),
            ("Ctrl+Alt+L", "格式化代码——交作业前必按"),
            ("Ctrl+/", "注释/取消注释"),
            ("Ctrl+`", "开关注册终端")])
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
