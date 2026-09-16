# -*- coding: utf-8 -*-
"""三课15分钟整体说课PPT生成器：02/03/05各1个，说课九段逻辑
结构（每课15-16页，1页/分钟）：封面→说课框架agenda→定位→学情→目标→内容结构
→教学设计(六步法+ABCD)→载体剧情→资源→评价→特色(岗课赛证创+思政)→成效诊改→结束
数据源=cs_data.py课标字典+meta3_*.py+universe.py——与课标/工单/PPT自动同步
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ppt_gen_v3 import DeckV3, _decorate   # noqa: E402
import cs_data                              # noqa: E402
import meta3_py, meta3_pp, meta3_ai48      # noqa: E402
import sessions_ai48 as S48                # noqa: E402
import universe as UNI                     # noqa: E402
from gen_common import PlanBuilder          # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAT = os.path.join(BASE, "教学实施资料")
OUT = os.path.join(MAT, "说课PPT")
os.makedirs(OUT, exist_ok=True)

AGENDA = [("01", "课程定位", "约2′", "性质·岗位·证书·衔接"),
          ("02", "学情分析", "约1′", "起点·差异·对策"),
          ("03", "课程目标", "约2′", "知识·能力·素质三维"),
          ("04", "内容与结构", "约3′", "模块化·剧情递进"),
          ("05", "教学设计", "约3′", "六步法·ABCD分层·理实一体"),
          ("06", "教学资源", "约1′", "五层资料·虚拟产线"),
          ("07", "考核评价", "约2′", "过程80%·三级质检"),
          ("08", "特色与成效", "约1′", "岗课赛证创·诊改闭环")]

# 说课口吻标题替换（组件内置标题是授课口吻"本次课/本课"→说课口吻"课程/教学"）
TITLE_FIX = [("本次课议程（六部分 · 80分钟）", "说课框架（八环节 · 15分钟）"),
             ("学习目标", "课程目标（三维可测可评）"),
             ("本次课流程（80分钟时间盒）", "教学流程设计（80分钟时间盒）")]


def _shuoke_agenda(deck, items):
    """说课框架页：3列×3行大卡（8环节+1汇总徽章格）——52号轮结构重设计
    视觉目标：卡片更大更透气（3行×1500000高），字号全面放大（编号24/名称17/分钟12/一句话11.5）"""
    from pptx.enum.text import PP_ALIGN
    from ppt_gen_v3 import box, text, LIGHT
    from ppt_gen import NAVY, BLUE, GRAY, CBLUE, WHITE
    from pptx.util import Emu
    s = deck.add()
    deck._header(s, "说课框架（八环节 · 15分钟）")
    x0, y0 = Emu(536000), Emu(1720000)
    cw, ch, gx, gy = Emu(3520000), Emu(1500000), Emu(280000), Emu(200000)
    for i, (no, name, mins, note) in enumerate(items):
        x = x0 + (i % 3) * (cw + gx)
        y = y0 + (i // 3) * (ch + gy)
        box(s, x, y, cw, ch, LIGHT, line=BLUE)
        box(s, x, y, cw, Emu(380000), NAVY)
        text(s, x + Emu(160000), y + Emu(40000), Emu(1300000), Emu(320000),
             [[(no, 24, WHITE, True)]])
        text(s, x + Emu(1500000), y + Emu(80000), Emu(1900000), Emu(280000),
             [[(mins, 12, WHITE, True)]], PP_ALIGN.RIGHT)
        text(s, x + Emu(160000), y + Emu(450000), Emu(3220000), Emu(420000),
             [[(name, 17, NAVY, True)]])
        text(s, x + Emu(160000), y + Emu(880000), Emu(3220000), Emu(540000),
             [[(note, 11.5, GRAY, False)]], line_spacing=1.18)
    # 第9格：汇总徽章卡（NAVY全底）
    x9 = x0 + 2 * (cw + gx)
    y9 = y0 + 2 * (ch + gy)
    box(s, x9, y9, cw, ch, NAVY)
    text(s, x9 + Emu(140000), y9 + Emu(180000), Emu(3240000), Emu(420000),
         [[("15分钟 · 八环节", 19, WHITE, True)]], PP_ALIGN.CENTER)
    text(s, x9 + Emu(140000), y9 + Emu(640000), Emu(3240000), Emu(700000),
         [[("定位→学情→目标→内容→", 11.5, CBLUE, False)],
          [("设计→资源→评价→特色成效", 11.5, CBLUE, False)]],
         PP_ALIGN.CENTER, line_spacing=1.25)


def _shuoke_xq(deck, lines):
    """学情三问页：3行横条完整展示（mindmap的[:28]截断会丢失内容，弃用）"""
    from ppt_gen_v3 import box, text, LIGHT
    from ppt_gen import NAVY, BLUE, ORANGE, CBLUE, WHITE
    from pptx.util import Emu
    chips = [("起点", NAVY), ("差异", ORANGE), ("对策", CBLUE)]
    s = deck.add()
    deck._header(s, "学情分析：起点 · 差异 · 对策")
    y = Emu(1900000)
    for (chip, color), body in zip(chips, lines):
        box(s, Emu(760000), y, Emu(10900000), Emu(950000), LIGHT, line=BLUE)
        box(s, Emu(760000), y, Emu(1500000), Emu(950000), color)
        text(s, Emu(820000), y + Emu(260000), Emu(1380000), Emu(460000),
             [[(chip, 15, WHITE, True)]])
        text(s, Emu(2500000), y, Emu(9000000), Emu(950000),
             [[(body, 13.5, NAVY, False)]])
        y += Emu(1100000)
    text(s, Emu(760000), Emu(5350000), Emu(10900000), Emu(400000),
         [[("→ 下一页：入学摸底分层数据，ABCD四层动态升降就是为此设计", 12.5, CBLUE, True)]])


def _fix_titles(deck):
    for sl in deck.prs.slides:
        for sh in sl.shapes:
            if not sh.has_text_frame:
                continue
            for para in sh.text_frame.paragraphs:
                for run in para.runs:
                    for old, new in TITLE_FIX:
                        if old in run.text:
                            run.text = run.text.replace(old, new)


def _nature_brief(txt):
    """说课定位页：课程性质长文提炼为'首句+定位关键词'（147字压到约75字2行内）"""
    if len(txt) <= 88:
        return txt
    head = txt.split("：")[0]
    tail = txt.split("——")[-1].split("；") if "——" in txt else []
    kws = "、".join(k.split("（")[0].replace("。", "") for k in tail) if tail else txt[:40]
    return head + "：四大核心定位——" + kws if tail else head + "。"


def shuoke(key, folder, cname, sub, meta3, tasks_note, resource_note,
           design_extra, feature_extra, effect_note):
    """key: cs_data里的课标字典键/py|pp或传入dict；meta3: {周: {basics, skills,...}}"""
    cs = cs_data.__dict__[key] if isinstance(key, str) else key
    info = cs["info"]
    weeks = sorted(int(w) for w in meta3.keys())
    w0, w1 = weeks[0], weeks[-1]

    d = DeckV3()
    # 封面
    d.cover(cname, "课程整体说课", f"{sub} · 说课时长15分钟",
            f"说课人：专业教学团队 · 依据：课程标准+授课计划+48学时实施方案 · 载体：{UNI.GROUP['name']}",
            dept=UNI.DEPTS.get("py" if key == "PY" else ("pp" if key == "PP" else "ai48"), {}).get("name", ""))
    d.note("开场30秒：报课程名+学时+面向岗位，说明说课八个环节。")
    _shuoke_agenda(d, AGENDA)
    d.note("框架页30秒：指读八环节与分钟归属，评委可对照打分表。")

    # 01 定位
    d.section("01", "课程定位", "为什么开这门课")
    d.note("过渡：从专业人才培养方案说起。")
    pos = [("课程性质", _nature_brief(cs["性质定位"][0])),
           ("面向岗位", info["岗位"]),
           ("学时学分", f"{info['总学时']}学时（理论{info['理论']}+实训{info['实训']}）· {info['学分']}学分 · {info['开课时间']}"),
           ("对接证书", cs["x证书"][0]),
           ("课程衔接", f"{info.get('前续', [('', '')])[0][0]} → 本课 → {info.get('后续', [('', '')])[0][0]}")]
    d.positioning(cname, pos)
    d.note("定位页90秒：念性质定位一句，指读岗位链与证书衔接。")

    # 02 学情
    d.section("02", "学情分析", "学生是谁·差异在哪")
    d.note("学情：起点/差异/对策三段，40秒。")
    xq = {"PY": ["起点：大一新生，多数零Python基础（W4-11零基础口径），有C语言或Office经验",
                 "差异：入学摸底分四档，ABCD分层动态升降（每4周）",
                 "对策：starter防挫败+微课课前预习+双师带教"],
          "PP": ["起点：大二，已修Python编程基础48学时，会Pandas/NumPy基础操作",
                 "差异：工程化经验分化大——会用库≠会做项目",
                 "对策：Git+Gitee五步工作流规范协作，P7选做多模存储全栈挑战"],
          "ai48": ["起点：大二，Python开课4周后即第5周开课，有Pandas/NumPy基础",
                   "差异：ML/DL/大模型经验两极分化，GPU资源有限",
                   "对策：CPU优先全流程可跑+ABCD分层+虚拟产线零硬件门槛"]}[key if isinstance(key, str) else "ai48"]
    _shuoke_xq(d, xq)
    d.note("学情三问：先讲共性起点，再讲差异，落到对策。")
    d.fig_bars("入学摸底分层占比（%）· ABCD每4周动态升降",
               [("D层·学徒", 25, None), ("C层·操作员", 40, None),
                ("B层·组长", 25, None), ("A层·师傅", 10, None)], ymax=40,
               note="分层依据：入学摸底+第2周课堂观察；动态升降保公平")
    d.note("摸底数据卡：25%跟做保底、40%基础完成、25%标准达成、10%进阶拓展——ABCD分层就是为此设计。")

    # 03 目标
    d.section("03", "课程目标", "三维目标·可测可评")
    d.goals([f"{cs['知识目标'][0][:50]}…（共{len(cs['知识目标'])}条，对应工单验收口径）",
             f"{cs['能力目标'][0][:50]}…（共{len(cs['能力目标'])}条，对应周工单+代码审查）",
             f"{cs['素质目标'][0] if isinstance(cs['素质目标'][0], str) else cs['素质目标'][0][0]}（课程思政如盐入水）"])
    d.note("目标页90秒：点读关键动词（掌握/能/养成），对应工单验收口径。")

    # 04 内容与结构
    d.section("04", "内容与结构", "教什么·怎么编排")
    d.note("内容：模块化+剧情递进，2分钟。")
    trows = cs["任务"]
    if len(trows) <= 2:
        # PY式大模块（2行）：行高加大+列宽重分配+内容60字
        rows = [(t[0].split("\n")[0], t[1].replace("\n", " · "), t[2][:50]) for t in trows]
        d.decision("模块化任务结构（岗课赛证融通）",
                   ("模块", "周次·学时", "任务内容"), rows,
                   note=tasks_note, rowh=1100000, colw=[3200000, 2200000, 4400000])
    else:
        # 6-7行模块表：7行时上移起始纵坐标防溢出（7×620000+表头+note>页面底）
        y0v = 1700000 if len(trows) >= 7 else 1900000
        rows = [(t[0].split("\n")[0][:14], t[1].replace("\n", " · ")[:16], t[2][:44]) for t in trows]
        d.decision("模块化任务结构（岗课赛证融通）",
                   ("模块", "周次·学时", "任务内容"), rows,
                   note="" if len(trows) >= 7 else tasks_note,
                   y0_emu=y0v, colw=[3200000, 2200000, 4400000])
        if len(trows) >= 7:
            d.note("模块表：" + tasks_note)
    d.note("模块表：自上而下讲剧情递进，每个模块挂接两江智造剧情线。")
    d.fig_arch("课程内容架构（自下而上）", {
        "ai48": [("智能体层", ["多智能体调度(W11)", "综合答辩(W12)"]),
                 ("大模型层", ["LLM故障诊断(W9)", "RAG知识库(W10)"]),
                 ("视觉层", ["ResNet迁移(W7)", "YOLO检测(W8)"]),
                 ("模型层", ["分类/XGBoost(W3-4)", "MLP/CNN竞标(W5-6)"]),
                 ("数据层", ["清洗与特征(W1-2)", "泵站日志/缺陷图"])],
        "PY": [("综合应用层", ["工业互联网采集(W11)", "综合项目(W12)"]),
               ("报告与文档层", ["故障分析报告(W9)", "图像处理报告(W10)"]),
               ("数据进阶层", ["格式转换(W7)", "文件处理(W8)"]),
               ("面向对象层", ["类设计(W4)", "继承体系(W5)", "健壮采集(W6)"]),
               ("语法基础层", ["变量与初始化(W1)", "分支循环告警(W2-3)"])],
        "PP": [("部署与模型层", ["故障诊断模型与部署(W8)"]),
                ("数据仓库层", ["产线数据仓库与ORM(W7)"]),
                ("采集与看板层", ["多源数据采集(W6)", "KPI仪表盘(W5)"]),
                ("数据处理层", ["Pandas管道(W3)", "NumPy特征(W4)"]),
                ("工程基础层", ["Python基础五题(W1)", "标准工程模板(W2)"])]}[key if isinstance(key, str) else "ai48"])
    d.note("架构图：自下而上讲'数据→模型→应用'的递进逻辑，每个方块对应一周工单。")

    # 05 教学设计
    d.section("05", "教学设计", "怎么教·怎么学")
    d.note("设计：六步法+ABCD+理实一体，90秒。")
    d.flow([("资讯", "课前线上", "微课+预习快问"),
            ("计划", "10′", "决策矩阵·组内定方案"),
            ("决策", "10′", "方案理由入工单"),
            ("实施", "40′", "分层做任务·双师巡诊"),
            ("检查", "10′", "自检+互查签字"),
            ("评价", "10′", "当堂评分+24h反馈")],
           "80分钟时间盒（4课时周两次课分摊）· 完整六步法课堂化", note_emu=6600000)
    d.note("六步法：资讯计划课前线上完成——课堂从决策直接开始，实施占比50%。")
    d.mindmap("教学设计四支柱", [
        ("理实一体", ["双创中心302实训室", "讲演做一体化"]),
        ("ABCD分层", ["D跟做保底", "A进阶拓展费曼带徒"]),
        ("剧情载体", [f"{UNI.GROUP['name']}12周剧情", "真实生产关切"]),
        ("数字赋能", ["虚拟产线五件套", "微课+notebook预习"])], title="教学设计四支柱")
    d.note("四支柱：逐个点读——理实一体是形，ABCD是序，剧情是魂，数字化是翼。")
    scen_first = UNI.SCEN.get(("ai48" if key == "ai48" or not isinstance(key, str) else ("py" if key == "PY" else "pp"),
                               w0), "")
    d.scenario(f"剧情载体示例（第{w0}周）：{scen_first[:130]}", dept=UNI.DEPTS.get("py" if key == "PY" else ("pp" if key == "PP" else "ai48"), {}).get("name", ""))
    d.note("情境说书60秒：以第{}周为例讲剧情如何驱动任务。抛问'如果是你，第一步干什么？'".format(w0))

    # 06 资源
    d.section("06", "教学资源", "用什么教")
    d.note("资源：五层资料+虚拟产线，40秒。")
    d.mindmap("教学资源五层", [
        ("课程文件", ["课程标准+授课计划", "教学方案+分层工单"]),
        ("课堂资料", ["授课PPT每页讲稿", "starter代码框架"]),
        ("线上资源", ["微课知识卡+数字人版", "Jupyter实训notebook"]),
        ("实训环境", ["虚拟产线五件套", "软件指南照做版"]),
        ("教材", ["任越美《Python程序设计", "项目化教程》活页式" if key != "ai48" else "程显毅《人工智能应用", "基础项目式教程》"])], title="教学资源五层导览")
    d.note("资源页40秒：" + resource_note)

    # 07 评价
    d.section("07", "考核评价", "怎么考·怎么反馈")
    d.note("评价：过程80+结果20，90秒。")
    d.fig_bars("评价权重（%）", [("过程性·周工单", 50, None), ("代码审查", 20, None),
                                ("学习投入", 10, None), ("期末综合", 20, None)], ymax=50)
    d.note("权重：过程性80%——每周工单即考；期末20%综合答辩。")
    d.decision("工单评分细则（四级量表）",
               ("等级", "达标线", "对应要求"),
               [("A层·师傅", "≥90分", "进阶拓展+2分钟费曼展示"),
                ("B层·组长", "≥80分", "全功能+代码规范+帮带D/C"),
                ("C层·操作员", "≥70分", "基础功能完成+错误速查自查"),
                ("D层·学徒", "≥60分", "跟做完成核心步骤+达标自评")],
               note="功能40%+技术质量25%+代码规范20%+工程素养15%")
    d.note("评分细则：四级量表对应ABCD分层，每个等级有明确达标线。")
    d.content(2, "三级质检与诊改闭环",
              ["自检：工单达标自评（勾选ABCD层）",
               "互查：组长签字——讲得清才算会",
               "抽查：教师按ABCD分层抽人答辩",
               "反馈：24小时内工单批注退回",
               "诊改：周达标率连续两次<70%触发台账"])
    d.note("三级质检：强调'讲得清才算会'——防抄防混。")

    # 08 特色
    d.section("08", "特色与成效", "可复制亮点·量化成果")
    d.note("特色：60秒收束。")
    base_feat = [
        f"岗课赛证创五维融通：{(cs['五维融通'][2][1] if len(cs['五维融通']) > 2 else cs['五维融通'][0][-1])[:70]}…",
        f"课程思政如盐入水：{cs['思政'][0][:70]}…",
        "零硬件虚拟产线：数据生成/故障模拟/缺陷库/知识库/生产模拟五件套离线可跑",
        "ABCD四层动态升降：每4周评一次，保底不封顶"]
    d.content(3, "课程特色（可复制可推广）", base_feat + [feature_extra])
    d.note("特色页：点读岗课赛证创+思政+虚拟产线+分层四个亮点。")
    d.fig_bars("课程资源建设成果（份）",
               [("分层工单", 41, None), ("授课PPT", 72, None),
                ("Jupyter实训", 64, None), ("微课视频", 35, None)], ymax=72,
               note="全部与工单/课标同源自动同步——改一处全链更新")
    d.note("成果数据卡：41份工单+72个PPT+64个notebook+35个微课，全部可再生成。")

    # 成效
    d.content(4, "教学成效与持续改进", [
        effect_note,
        "三级闭环：学生评教+督导听课+企业反馈",
        "学习投入：课前微课观看率≥85%，实训任务当堂完成率≥90%",
        "课证赛贯通：1+X证书考核对标课内工单，W6竞标/W12答辩对标技能大赛规程",
        "课程标准年度修订：对齐1+X大纲与载体案例库",
        "四层教学文件开课前交叉校验（课标/计划/方案/工单）"])
    d.note("成效页：报达标率与诊改机制，回扣定位一句话收束。")
    d.thanks()
    d.note("结束：感谢评委，恳请指导。")

    _fix_titles(d)
    _decorate(d, cname)
    fname = f"{cname}-课程整体说课（15分钟）.pptx"
    p = os.path.join(OUT, fname)
    d.save(p)
    return p, len(d.prs.slides._sldIdLst)


if __name__ == "__main__":
    # 02-Python编程基础
    p1, n1 = shuoke("PY", "02-程序设计基础", "Python编程基础",
                    "48学时 · 大一新生 · 第1-12周", meta3_py.PY3,
                    "12周剧情递进：告警系统→设备类→健壮采集→数据报告→综合项目，每周1工单",
                    "24个notebook+12个微课+12份工单+12个starter全覆盖12周",
                    "starter防挫败：TODO未填也能跑通占位流程",
                    "配套资料与工单/PPT同源自动同步，改一处全链更新",
                    "周达标率≥90%，期末综合项目一次通过率≥85%")
    print(f"02说课PPT: {n1}页 → {os.path.basename(p1)}")
    # 03-Python程序设计（项目实战）
    p2, n2 = shuoke("PP", "03-Python程序设计-项目实战", "Python程序设计（项目实战）",
                    "32学时 · 大二 · 第1-8周（扩展9周选做）", meta3_pp.PP3,
                    "8周工程递进：基础→Pandas/NumPy→仪表盘→采集→仓库→模型部署，P7选做多模存储",
                    "16个notebook+10个微课+8份工单+P7智能运维平台可部署",
                    "Git+Gitee五步工作流：branch→commit→push→PR→merge真实协作",
                    "P7智能运维平台：Litestar+五库全栈，verify.sh 9断言可复现",
                    "代码审查合格率≥90%，8份工单全员按时提交率≥95%")
    print(f"03说课PPT: {n2}页 → {os.path.basename(p2)}")
    # 05-AI应用基础（48课时版）
    ai48_cs = dict(性质定位=["专业核心课程扩展版：48课时覆盖'数据处理→机器学习→深度学习→视觉→大模型→智能体'全谱系"],
                   info=dict(岗位="AI应用工程师、工业视觉开发、工业互联网数据分析",
                             总学时="48", 学分="3", 理论="24", 实训="24",
                             开课时间="第5-16周（12周×4课时，Python开课4周后即第5周开课）"),
                   x证书=["1+X AI应用实践（初级=M1-M3/中级=M4/高级=M5）"],
                   知识目标=["掌握数据清洗与特征工程方法，掌握分类/集成/神经网络原理与调优"],
                   能力目标=["能独立完成12个工单的端到端实现与评估，能做参数级工程权衡并留痕"],
                   素质目标=["数据诚信与工程纪律"],
                   任务=[("M1 数据处理与特征工程", "第1-2周·8课时", "M1-1a清洗质检；M1-1b特征优化"),
                         ("M2 机器学习与神经网络", "第3-6周·16课时", "分类/XGBoost/MLP/CNN竞标"),
                         ("M3 视觉与迁移学习", "第7-8周·8课时", "ResNet小样本；YOLO实时检测"),
                         ("M4 NLP与大模型", "第9-10周·8课时", "LLM故障诊断；RAG知识库问答"),
                         ("M5 多智能体", "第11周·8课时", "多智能体检修调度"),
                         ("综合答辩", "第12周·4课时", "综合项目答辩（预答辩+正式）")],
                   五维融通=[["赛（竞赛）", "W6竞标答辩制对标竞赛评审；W12答辩对标技能大赛'人工智能应用'赛项"]],
                   思政=["总目标：可信AI与制造强国——模型要有据可查，指标不许造假"])
    p3, n3 = shuoke(ai48_cs, "05-AI应用基础48课时版", "AI应用基础（48课时版）",
                    "48学时 · 大二 · 第5-16周（12周×4课时）",
                    {w: m for w, m in meta3_ai48.AI48.items()},
                    "12周全谱系递进：数据→ML→DL→视觉→大模型→智能体→答辩，M1-1a至Z共12工单",
                    "24个notebook+13个微课+12份工单+12个starter+虚拟产线五件套",
                    "CPU优先全流程可跑：GPU仅作可选加速，30台16GB机房即可开课",
                    "mock LLM本地化：不联网也能教大模型应用（Prompt+RAG可信问答）",
                    "12工单全员D级以上达标率≥90%，答辩优秀率≥35%（扩展班口径）")
    print(f"05说课PPT: {n3}页 → {os.path.basename(p3)}")
