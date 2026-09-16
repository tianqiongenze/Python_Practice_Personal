# -*- coding: utf-8 -*-
"""PPT v3 深度讲义版组装器: 每课约44-51页"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ppt_gen_v3 import DeckV3                       # noqa: E402
import sessions_meta as SM                          # noqa: E402
import sessions_meta2 as SM2                        # noqa: E402
import meta3_ai, meta3_py, meta3_pp                 # noqa: E402
import universe as UNI                              # noqa: E402
from build_ppts import (COURSES, MARK, cn_week,     # noqa: E402
                        split_sessions, group_items, lesson_title,
                        goals_of, next_prev_of)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAT = os.path.join(BASE, "教学实施资料")

M3 = {"ai": meta3_ai.AI3, "py": meta3_py.PY3, "pp": meta3_pp.PP3}

POSITION = {
    "ai": [("课程性质", "专业核心能力进阶课：无代码体验→轻代码实现→工业级应用"),
           ("面向岗位", "AI应用工程师、工业视觉开发、工业互联网数据分析"),
           ("对接证书", "AI应用实践（中级）、工业互联网平台运维、计算机视觉工程师"),
           ("课程衔接", "前：无Python先修（零基础入门） → 本课(第4-11周，与Python基础并行) → 后：项目实战")],
    "py": [("课程性质", "专业核心基础课：面向零基础新生的编程第一课"),
           ("面向岗位", "工业数据采集技术员、边缘计算运维、平台运维员"),
           ("对接证书", "Python开发（工信部）、AI应用实践、企业应用实施工程师"),
           ("课程衔接", "前：计算机文化基础 → 本课(第1-12周) → 后：AI应用基础")],
    "pp": [("课程性质", "自包含工程应用课：C语言底子直接上工业项目"),
           ("面向岗位", "数据工程师、数据分析、AI应用、采集技术员"),
           ("对接证书", "Python开发、数据应用与服务（1+X）、AI应用实践"),
           ("课程衔接", "前置仅需C语言 → 本课(第1-8周) → 后：毕业设计/平台实习")],
}


def flow_fig_for(course, four):
    if four:
        return ("课堂教法四步法（每课时40分钟）",
                ["讲10min", "演10min", "模仿10min", "练习10min"],
                "PRIMM融合：预测→运行→研究→修改→创造")
    return ("六步法课堂化（资讯计划课前完成）",
            ["资讯·计划", "决策10", "实施一30", "检查5", "实施二25", "评价10"],
            "时间单位: 分钟（除标注外）｜合计80分钟")


def build_course(c):
    mod = __import__(c["mod"])
    outdir = os.path.join(MAT, c["folder"], "授课PPT")
    os.makedirs(outdir, exist_ok=True)
    for f in os.listdir(outdir):
        fp = os.path.join(outdir, f)
        if os.path.isfile(fp):
            os.remove(fp)
    count = pages = 0
    for wi, week in enumerate(mod.WEEKS, 1):
        meta_key = wi + 3 if c["mod"] == "data_ai" else wi
        week_meta = c["meta"].get(meta_key)
        m3 = M3[c["code"]].get(meta_key)
        sessions = split_sessions(week)
        for si, (no, header, items) in enumerate(sessions):
            meta = week_meta if c["mod"] == "data_ai" else week_meta["tasks"][si]
            m2 = SM2.D.get((c["code"], meta_key, si), {})
            d = DeckV3()
            title = lesson_title(header, week)
            sub = f"第{cn_week(meta_key)}周 · 第{no}次课（2课时 · 80分钟）"
            illus = os.path.join(outdir, "_场景插画", f"W{meta_key}_场景.png")
            if not os.path.exists(illus):
                illus = None
            # ===== 第一部分 定位 =====
            from env_tools import tool_for
            _tp, _tg = tool_for(c["code"], meta_key)
            d.cover(c["name"], title, sub,
                    f"{c['place']}  ·  理实一体  ·  配套：分层工单+starter  ·  本课主用：{_tp}",
                    dept=UNI.DEPTS[c["code"]]["name"], illus=illus)
            # v9: 议程页（六部分+分钟归属，四步法周次换口径）
            four_agenda = wi in c["four_step_weeks"]
            AG = [("01", "课程定位", "课前已读", "性质·岗位·证书：为什么学这门课"),
                  ("02", "课堂流程", "约2′", "80分钟时间盒与ABCD分层节奏"),
                  ("03", "目标与资讯·情境", "约5′", "带着目标进课堂+两江智造本课剧情"),
                  ("04", "知识精讲", "约15′", "基础知识大卡+代码演示（先例后理）"),
                  ("05", "任务实施", "六步法核心", "工单发布·分层执行·避坑" ),
                  ("06", "检查与评价", "约15′", "三层质检·当堂评分·课后任务")]
            if four_agenda:
                AG = [("01", "课程定位", "课前已读", "性质·岗位·证书：为什么学这门课"),
                      ("02", "课堂流程", "约2′", "四步法节奏：讲-演-模仿-练习"),
                      ("03", "目标与资讯·情境", "约5′", "目标+两江智造本课剧情"),
                      ("04", "知识精讲", "讲10′+演10′", "基础知识大卡+现场演示"),
                      ("05", "模仿与练习", "10′+10′", "跟做保底→独立完成（工单分层）"),
                      ("06", "检查与评价", "约15′", "三层质检·当堂评分·课后任务")]
            d.note(f"开场30秒：本次课《{title}》，80分钟＝2课时×40分钟。"
                   "课前已发工单+starter+微课知识卡，资讯·计划线上完成。")
            d.agenda(AG, tail="资讯·计划已于课前线上完成——课堂从决策/演示直接开始")
            d.note("议程页30秒：指读六个部分的分钟归属，强调'资讯计划课前已完成'；"
                   "告诉学生'每次课都知道现在在哪一步、还剩多少时间'。")
            # 52号轮：本课目录（一页速览全课结构）
            d.content(22, "本课目录（结构速览）", [
                "①课程定位：定位/知识地图/课证赛岗——为什么学这门课",
                "②课堂流程：80分钟时间盒/分层节奏——今天怎么安排",
                "③目标与情境：三维目标/剧情拆解/随堂自测——学什么",
                "④知识精讲：知识卡×应用×深化×代码走读——怎么教",
                "⑤任务实施：工单/四层任务/避坑/核对清单——怎么做",
                "⑥检查评价+⑦拓展：质检/评分/工具箱/一图流——怎么收"])
            d.note("目录页：给学生'地图感'——翻到哪部分干什么，30秒。")
            d.section("01", "课程定位", "本课在课程体系中的位置（课程标准摘录）")
            d.note("过渡页：一句话点明本部分——先明确这门课'为什么学、学了去哪'。")
            d.positioning(c["name"], POSITION[c["code"]])
            d.note("念'课程性质'一行即可，重点指读'对接证书'与'课程衔接'，"
                   "让学生知道本课与前后课程的关系（30秒）。")
            d.mindmap(title[:8], [
                ("基础知识", m3["basics"][:2]),
                ("继续夯实", m3["basics"][2:4]),
                ("技能点", m3["skills"][:2]),
                ("分层任务", ["D跟做保底", "C基础完成", "B标准达成", "A进阶拓展"]),
                ("课堂评价", ["功能40%", "技术25%", "规范20%", "素养15%"]),
            ])
            d.note("知识地图：先见森林后见树木。指着四条分支预告本课路线，"
                   "不展开细讲（40秒）。")
            # 52号轮：图谱分支展开（每分支详解1页，共2页）
            d.content(1, "知识地图分支详解（一）", [
                f"基础知识线：{'；'.join(m3['basics'][:2])}",
                f"继续夯实线：{'；'.join(m3['basics'][2:4])}",
                "两条线的关系：先打地基（概念/类型），再上楼层（组合应用）",
                "学法提示：每条知识都配'车间例子'，先例后理"])
            d.note("分支详解一：基础两条线各点一个产线例子，说明'为什么先学这个'。")
            d.content(2, "知识地图分支详解（二）", [
                f"技能线：{'；'.join(m3['skills'][:2])}",
                "分层任务线：D跟做→C独立→B帮带→A拓展（每4周动态升降）",
                "课堂评价线：功能40%+技术25%+规范20%+素养15%",
                "三条线闭环：技能靠任务练，任务按评价收"])
            d.note("分支详解二：强调'技能=今天的验收口径'，评价权重即打分表。")
            # 52号轮：课证赛岗对照
            d.extend_page("岗课赛证对照（本课坐标）", [
                ("岗", UNI.DEPTS[c["code"]]["name"] + "：" + cs_posts(c["code"])),
                ("课", f"{meta['wono']}《{meta['woname']}》——本课工单即考核单元"),
                ("证", CERT_OF[c["code"]]),
                ("赛", "世界职业院校技能大赛（人工智能赛道）数据采集/处理赛项")])
            d.note("课证赛岗对照：说明本课工单在证书/竞赛中的对应考点，30秒。")
            d.recap("01", "课程定位", [
                f"本课在课程体系：{POSITION[c['code']][0][1][:36]}",
                "知识地图五分支：基础→夯实→技能→分层→评价",
                "岗课赛证四维坐标已明确，带着目标进课堂"])
            d.note("部分小结：三句话收束定位部分，转流程。")
            # ===== 第二部分 流程 =====
            d.section("02", "课堂流程", "80分钟时间盒与个人节奏")
            d.note("流程预告：强调'资讯·计划已在课前完成'，课堂从决策直接开始。")
            four = wi in c["four_step_weeks"]
            from sessions_meta import FOUR, SIX
            d.flow(FOUR if four else SIX,
                   "每课时40分钟 · 共80分钟（四步法）" if four
                   else "每课时40分钟 · 共80分钟（六步法课堂化）")
            d.note("讲10→演10→模仿10→练习10" if four else
                   "决策10→实施30→检查5→实施25→评价10；评价环节不压缩")
            d.pace()
            d.note("分层节奏：D层跟做保底、C层基础完成、B层标准达成、A层进阶拓展；"
                   "每人按工单勾选自己的层，每4周动态升降。")
            # 52号轮：产业数据卡+部分小结
            from pptx.dml.color import RGBColor as _RC2
            _ind = INDUSTRY_DATA[c["code"]]
            d.fig_bars("两江智造产线运营指标（虚拟产线月度数据）",
                       [(k, v, _RC2(0x05, 0x45, 0xE8)) for k, v in _ind],
                       note="数据来自虚拟产线五件套——你写的代码就在处理这些数据")
            d.note("产业数据卡：让学生看到'学的技能=产线的数字'，建立真实感。")
            d.recap("02", "课堂流程", [
                ("四步法：讲10→演10→模仿10→练习10" if four
                 else "六步法：决策10→实施30→检查5→实施25→评价10"),
                "分层节奏：D/C/B/A各就各位，每4周动态升降",
                "评价环节10分钟不压缩——当堂评分、24小时反馈"])
            d.note("部分小结：时间盒+分层节奏收束，转目标。")
            # ===== 第三部分 目标与资讯 =====
            d.section("03", "目标与资讯", "带着目标进课堂（Predict·预测）")
            d.note("PRIMM的Predict：先让学生猜，再揭晓。")
            d.goals(goals_of(week))
            d.note("目标解读：点读1-2个关键动词（能编写/能诊断/能部署），"
                   "说明这就是今天工单的验收口径。")
            # 52号轮：三维目标逐维页（知识/能力/素质各1页——怎么学怎么证）
            _g = goals_of(week)
            d.content(10, "知识目标：怎么学·怎么证", [
                f"目标：{_g[0][:56]}",
                "怎么学：知识卡先例后理→快查核对→应用页回到产线场景",
                "怎么证：课前quiz+随堂自测+工单'技术质量25%'项",
                "达标线：能复述定义+能说出产线例子=过关"])
            d.content(11, "能力目标：怎么练·怎么证", [
                f"目标：{_g[1][:56]}",
                "怎么练：starter跟做（D）→独立完成（C）→规范+帮带（B）→拓展（A）",
                "怎么证：工单'功能40%'全项+运行截图贴过程记录",
                "达标线：代码能跑+输出符合工单样例=过关"])
            d.content(12, "素质目标：怎么养·怎么证", [
                f"目标：{_g[2][:56]}",
                "怎么养：规范命名/及时提交/报错必究——每个工单都在练",
                "怎么证：Git提交历史（每周≥1次）+工单'素养15%'项",
                "达标线：提交记录连续+命名规范=过关"])
            d.review(meta["quiz"], c["chk"])
            d.note("课前测讲评：随机点2名学生说答案，只追问'为什么'，不展开讲；"
                   "错得多的题记到'检查'环节再回收。")
            # 52号轮：课前测逐题精讲（quiz题干实数据）
            d.content(18, "课前测逐题精讲（错得最多的那道）", [
                f"题目：{str(meta['quiz'])[:56]}",
                "正确思路：从'考哪个知识卡'入手——先定位再作答",
                "常见错误：背概念不看场景；看到代码就慌，先读注释",
                "本课回收：这道题的考点会在知识卡X和随堂自测中再次出现"])
            d.note("逐题精讲：只讲错得最多的题——其余对答案即可。")
            d.practice(1, meta["quiz"],
                       m2.get("cautions", ["先自己想30秒再讨论"])[0])
            d.note("快问快答：同桌互问30秒，举手表决；答案不公布，留到知识精讲验证。")
            scen = UNI.SCEN.get((c["code"], meta_key))
            if scen:
                d.scenario(scen, dept=UNI.DEPTS[c["code"]]["name"], illus=illus)
            else:
                d.scenario(meta["sc"] or title)
            d.note(f"情境说书（30秒，口头讲，不必逐字念）：{scen or meta['sc']}\n"
                   "讲完抛出问题：'如果是你，第一步先干什么？'——自然过渡到决策环节。")
            # 52号轮：情境连环（任务-冲突-决策三段拆解）
            _scen_txt = scen or meta.get("sc") or title
            d.content(3, "剧情拆解：任务 → 冲突 → 你的决策", [
                f"任务背景：{_scen_txt[:52]}",
                "冲突点：产线数据量大/格式杂/时限紧——手工做不完，必须编程",
                "决策点：先做什么再做什么？数据从哪来？输出给谁看？",
                "带着这三个问题进入知识精讲——每个知识点都是解药"])
            d.note("剧情拆解：把情境页的故事拆成三要素，让学生明确'解决什么'。")
            # 52号轮：目标-评价对照
            _g = goals_of(week)
            d.extend_page("三维目标 → 怎么算达标", [
                ("知识目标", _g[0][:56]),
                ("能力目标", _g[1][:56]),
                ("素质目标", _g[2][:56]),
                ("达标口径", f"对应工单{meta['wono']}评分：功能40%+技术25%+规范20%+素养15%")])
            d.note("目标对照页：逐维读目标，指读达标口径=评分表，目标可测可评。")
            # 52号轮：随堂自测（3题，题干来自quiz/errors/basics实数据）
            for qi, (qt, qa) in enumerate(quiz_of(meta, m3, c["code"]), 1):
                d.practice(qi + 2, qt, qa)
            d.note("随堂自测：先答后揭晓，答对记过程分——为目标达成做第一次探测。")
            d.recap("03", "目标与资讯·情境", [
                "三维目标已明确，达标口径=工单评分表",
                f"剧情任务：{_scen_txt[:32]}",
                "随堂自测完成第一次探测，带着问题进精讲"])
            d.note("部分小结：目标+剧情+自测收束，转知识精讲。")
            # ===== 第四部分 知识精讲 =====
            d.section("04", "知识精讲", "基础知识 → 详解 → 技能 → 代码")
            d.note("知识精讲开始：每条知识对应一张大卡，讲法'先例后理'。")
            b = m3["basics"]
            for bi, bt in enumerate(b, 1):
                d.basic_card(bi, bt)
                d.note(f"知识卡{bi}：{bt}\n"
                       "讲法：先给一个车间/产线的例子，再给定义；"
                       "讲完随机点1名学生用自己的话复述（每个30-60秒，控制节奏）。")
                # 52号轮：每条知识的应用页（有'——应用：'后缀的生成，先例后理）
                _main, _app = split_apply(bt)
                if _app:
                    _code_line = _app if any(ch in _app for ch in "=()[]{}:") else ""
                    d.apply_page(bi, _main[:22],
                                 f"{_main}。在两江智造产线上的用法：{_app[:86]}",
                                 _code_line[:200])
                    d.note(f"应用页{bi}：把知识点放回产线场景——先看代码输出，"
                           "再回看定义，强化'学以致用'。")
            d.quick_check(b[:5])
            d.note("快查核对：遮住左栏让学生说右栏含义；全对的小组加过程分。")
            if m2.get("kn"):
                d.knowledge(0, m2["kn"])
                d.note("深化讲解：面向A/B层的进阶理解，C/D层听懂结论即可。")
                # 52号轮：深化要点逐条展开（面向A层的费曼素材）
                _kns = m2["kn"] if isinstance(m2["kn"], list) else [m2["kn"]]
                d.content(4, "深化理解：逐条讲透（A层费曼素材）", [
                    f"要点{i+1}：{str(k)[:52]}" for i, k in enumerate(_kns[:4])] + [
                    "学法：A层用自己的话讲给D层听——讲得清才是真懂"])
                d.note("深化展开：每条要点配一个'为什么'，A层准备2分钟费曼讲解。")
            d.skills(m3["skills"])
            d.note("技能点＝今天'做完你应该会'，逐条对应工单步骤与评分点。")
            # 52号轮：技能点逐条展开（每条对应工单步骤与得分点）
            d.content(5, "技能点 → 工单步骤 → 得分点", [
                f"技能{i+1}：{sk[:44]} → 对应工单步骤{i+1}，占功能分"
                for i, sk in enumerate(m3["skills"][:4])] + [
                "提示：技能点全部来自工单评分点——练技能=挣分数"])
            d.note("技能展开：逐条读技能，指读工单对应步骤——把'学'和'考'对齐。")
            if c["code"] == "ai":
                d.metrics_card()
            groups = group_items(items)
            dcur, lines, slide_no = [], 0, 1

            def flush():
                nonlocal slide_no
                if dcur:
                    flat = [("· " + t) if sub else t for t, sub in dcur]
                    d.content(slide_no, f"{title}（{slide_no}）", flat)
                    slide_no += 1
                    d.note("实施内容清单：本页条目与工单步骤一一对应，"
                           "逐项过一遍即可，细节留到代码演示。")
            for parent, subs in groups:
                est = 1 + len(subs)
                if lines + est > 8 and dcur:
                    flush()
                    dcur, lines = [], 0
                dcur.append((parent, False))
                lines += 1
                for s_ in subs:
                    dcur.append((s_, True))
                    lines += 1
            flush()
            for ct, cc in m3["code"][:2]:
                d.code(ct, cc)
                d.note(f"现场演示《{ct}》：三步走——先整段跑通看结果，"
                       "再逐行讲关键语句，最后现场改一个参数看输出变化（演10分钟的核心素材）。")
                # 52号轮：代码走读页（逐段拆解——每段干什么/为什么这么写）
                _lines = [ln for ln in cc.splitlines() if ln.strip()][:5]
                d.content(17, f"代码走读：《{ct[:16]}》逐段拆解", [
                    f"行{i+1}：{ln.strip()[:52]}" for i, ln in enumerate(_lines)] + [
                    "读法：先看每行的输出→再问'为什么这么写'→最后改参数看变化"])
                d.note("代码走读：一页拆一段——学生跟着读，不是抄。")
            ft, fsteps, fnote = flow_fig_for(c["code"], four)
            d.fig_flow(ft, fsteps, fnote)
            d.note("流程图页：可快速带过，作为'我们现在在哪一步'的路标。")
            from pptx.dml.color import RGBColor as _RC
            d.fig_bars("80分钟时间盒分配（分钟）",
                       [("决策", 10, _RC(0x05, 0x45, 0xE8)),
                        ("实施一", 30, _RC(0x04, 0x75, 0xB6)),
                        ("检查", 5, _RC(0xF5, 0x67, 0x0F)),
                        ("实施二", 25, _RC(0x01, 0x75, 0x1F)),
                        ("评价", 10, _RC(0x44, 0x54, 0x6A))], ymax=30,
                       note="评价环节不压缩：10分钟当堂评分+24小时反馈")
            d.note("强调柱状图最右两根：实施二25分钟是冲优秀的时间，"
                   "评价10分钟不压缩——当堂评分、24小时内反馈。")
            if meta_key in (12, 8) and c["code"] == "py" or (c["code"] == "pp" and meta_key == 8):
                d.fig_arch("综合系统架构（分层）", [
                    ("展示层", ["仪表盘", "PDF报告"]),
                    ("分析层", ["阈值检测", "统计聚合"]),
                    ("数据层", ["清洗管道", "SQLite"]),
                    ("采集层", ["Modbus", "文件/模拟"])])
                d.note("架构分层讲解：自下而上过一遍数据流向，"
                       "答辩时按此图讲'系统架构'。")
            # ===== 第五部分 任务实施 =====
            d.section("05", "任务实施", "工单 · 分层 · 步骤 · 避坑")
            d.note("进入实施：先决策、再领工单、按层执行。")
            dec = meta["dec"]
            d.decision(dec["title"], dec["header"], dec["rows"],
                       dec.get("note", ""))
            d.note("决策矩阵用法（10分钟）：组内对备选方案打分→选型→把结论和理由"
                   "写进工单'决策记录'栏；教师抽查2组口头说理由（决策追责）。")
            # 52号轮：方案对比页（决策依据透明化）
            d.content(23, "决策怎么下：方案对比三问", [
                f"本课决策题：{dec['title'][:44]}",
                "问①可行吗——每个方案的实现路径走得通吗（技术风险）",
                "问②值吗——开发时间/运行速度/可维护性三角权衡（工程账）",
                "问③谁拍板——组内数据说话，理由写进工单（决策追责制）",
                "规则：没有记录的决策=没有决策——写下来才算数"])
            d.note("方案对比：三问框架通用——以后每个决策环节都用这三问。")
            d.task(meta["wono"], meta["woname"], meta["steps"],
                   meta["sp"], meta["sg"])
            d.note(f"工单发布话术：'{UNI.DEPTS[c['code']]['name']}发来工单"
                   f"{meta['wono']}《{meta['woname']}》，及格线是{meta['sp'][0]}，"
                   "优秀线看A层标准'——念完发starter。")
            extA = m2.get("extA", "在优秀基础上完成创新优化")
            tier_note = {
                "D": "D层·学徒：跟做保底。教师或屏幕领做，做完即达标，绝不留白。",
                "C": "C层·操作员：基础完成。按工单步骤独立完成，卡壳先查错误速查表。",
                "B": "B层·组长：标准达成。全部功能+规范，完成后帮带同组D/C层。",
                "A": "A层·师傅：进阶拓展。完成拓展任务并准备2分钟展示；费曼式讲给D层听。",
            }
            for tier in "DCBA":
                t = m3["abcd"][tier]
                d.tier_detail(tier, t["goal"], t["steps"], t["std"],
                              extA if tier == "A" else None)
                d.note(tier_note[tier])
                # 52号轮：每层步骤详解页（steps数据实展开）
                _tn = {"D": "学徒", "C": "操作员", "B": "组长", "A": "师傅"}[tier]
                d.content(13 + "DCBA".index(tier),
                          f"{tier}层·{_tn}：步骤怎么走", [
                              f"第{i+1}步：{str(st)[:50]}" for i, st in
                              enumerate(t["steps"][:4])] + [
                              f"达标自检：{t['std'][:44]}"])
                d.note(f"{tier}层步骤详解：逐条读步骤——D层照着做，A层做完讲给别人。")
            d.steps_caution(meta["steps"], m2.get("cautions",
                                                  ["按工单避坑清单执行"]))
            d.note("避坑清单：每条问'为什么会踩'，点名学生解释，"
                   "把'注意'变成'知道为什么注意'。")
            d.errors(m3["errors"])
            e0 = m3["errors"][0]
            d.note(f"错误速查：现场演示第一条——制造「{e0[0]}」，带着学生按'现象→原因→解决'三步排查。")
            d.practice(2, f"运行时出现「{e0[0]}」，你的排查顺序是？",
                       f"提示: 原因是{e0[1]}")
            d.note("先让学生说排查顺序再给提示：训练'看报错信息'的条件反射。")
            # 52号轮：ABCD四层总览（一页看全）
            d.content(6, "ABCD四层任务总览（先看全貌再领任务）", [
                f"D·学徒（≥60）：{m3['abcd']['D']['goal'][:40]}——跟做保底",
                f"C·操作员（≥70）：{m3['abcd']['C']['goal'][:40]}——基础完成",
                f"B·组长（≥80）：{m3['abcd']['B']['goal'][:40]}——标准达成+帮带",
                f"A·师傅（≥90）：{m3['abcd']['A']['goal'][:40]}——进阶拓展+费曼讲解",
                "规则：每人按工单勾选自己的层；每4周按达标情况动态升降"])
            d.note("四层总览：一页看全四层目标与达标线——学生选层前先看全局。")
            # 52号轮：操作核对清单（步骤逐条核）
            _steps = meta["steps"] if isinstance(meta.get("steps"), list) else []
            if _steps:
                d.content(7, "操作核对清单（做完一条勾一条）", [
                    f"□ 步骤{i+1}：{str(st)[:48]}" for i, st in enumerate(_steps[:5])] + [
                    "□ 全部勾完→同桌互查签字→提交工单"])
                d.note("核对清单：把工单步骤变成checklist，做完勾选——防漏做。")
                d.content(8, "提交前最后一查（90秒）", [
                    "□ 代码能从头跑到尾不报错（python xx.py再跑一遍）",
                    "□ 输出格式符合工单样例（对齐/单位/小数位）",
                    "□ 文件命名：学号_姓名_工单号.py（不对=扣规范分）",
                    "□ 运行截图已贴工单过程记录栏（过程性证据）",
                    f"□ conda环境正确（提示符显示({ENV_OF[c['code']]}）再运行"])
                d.note("最后一查：五项90秒自查——退回率最低的五个点。")
            d.recap("05", "任务实施", [
                f"工单{meta['wono']}已发布，四层任务各自认领",
                "避坑清单+错误速查在手，卡壳先自查再举手",
                "操作核对清单做完勾选，提交前90秒最后一查"])
            d.note("部分小结：实施收束，转检查评价。")
            # ===== 第六部分 检查评价 =====
            d.section("06", "检查与评价", "三层质检 · 评分 · 课后")
            d.note("收尾5分钟检查+10分钟评价。")
            d.check()
            d.note("三层质检组织：自查明细→同伴互查（签字）→教师抽查2组；"
                   "查出的缺陷当场修，修不完记入课后任务。")
            d.submission(meta["wono"])
            d.note("提交强调：文件命名'学号_姓名_工单号.zip'，24小时内教师在平台反馈评分。")
            d.closing_tasks(week["homework"], next_prev_of(week["homework"]))
            d.note("课后任务逐条念，说明下次课的衔接关系；预告下次课前微课与导学单。")
            # 37号轮：教材预习/检查知识点入演讲者备注（不占正文版面）
            _tb = week.get("textbook", [])
            if _tb:
                d.note("教材衔接：" + " | ".join(_tb))
            d.literacy(LITERACY[c["code"]])
            d.note("素养页：结合本课内容点一个真实案例（如数据脱敏、代码抄袭后果），30秒即可。")
            d.shot_placeholder()
            d.note("提醒：运行截图/实拍照片贴到工单过程记录栏，作为过程性考核证据。")
            # 52号轮：评分细则四级量表+FAQ+资源导航
            d.decision("工单评分细则（四级量表）",
                       ("等级", "达标线", "对应要求"),
                       [("A·师傅", "≥90分", "进阶拓展完成+2分钟费曼展示"),
                        ("B·组长", "≥80分", "全功能+代码规范+帮带D/C层"),
                        ("C·操作员", "≥70分", "基础功能完成+错误速查自查"),
                        ("D·学徒", "≥60分", "跟做完成核心步骤+达标自评")],
                       note="功能40%+技术质量25%+代码规范20%+工程素养15%")
            d.note("评分细则：四级量表逐行读——学生知道自己'到哪条线得多少分'。")
            d.extend_page("高频FAQ（先自查再举手）",
                          [(q, a) for q, a in FAQ_BANK[c["code"]]])
            d.note("FAQ三题：覆盖装包/启动/规范三大高频问题——贴在工单背面。")
            d.extend_page("资源导航（卡住时按顺序查）", [
                ("工单", f"{meta['wono']}任务书——步骤/及格线/评分细则都在里面"),
                ("starter", f"学生代码框架/——TODO注释即步骤提示，未填也能跑"),
                ("软件指南", "../软件操作指南/——PyCharm/Jupyter/Git/Anaconda六份图文"),
                ("Jupyter", "Jupyter实训/——本周notebook师生版，先跑教师版看答案"),
                ("Git提交", "做完按Ctrl+K提交推送——每周至少1次，工程素养分依据")])
            d.note("资源导航：五级求助顺序=工单→starter→指南→notebook→教师。")
            d.recap("06", "检查与评价", [
                "三层质检：自检→互查签字→教师抽查",
                "评分四级量表+四权重已明确，24小时内平台反馈",
                "课后任务+下次课预告形成学习闭环"])
            d.note("部分小结：评价收束。")
            # ===== 52号轮新增 第七部分 拓展与自测 =====
            d.section("07", "拓展与自测", "把今天的能力圈再画大一圈")
            d.note("拓展部分：A层必看，B层选看，C/D层课后看——差异化作业。")
            d.extend_page("产业应用案例（学这个能干什么）", [
                ("真实场景", INDUSTRY_CASE[c["code"]][0]),
                ("用什么解决", INDUSTRY_CASE[c["code"]][1]),
                ("本课对应", f"{meta['wono']}的技能点即其最小实现"),
                ("延伸方向", INDUSTRY_CASE[c["code"]][2])])
            d.note("产业案例：讲一个真实岗位场景，把课堂技能挂到职业坐标系。")
            # 52号轮：思政案例+学习策略+进阶路线+周回顾+预习+口袋书+好差对比
            d.extend_page("课程思政：如盐入水（30秒一个点）", [
                ("工匠精神", "报错必究——每个红色报错都是产线隐患的预演"),
                ("数据诚信", "指标不许造假——改数字骗过测试=产线事故的起点"),
                ("协作素养", "ABCD轮换履职——师傅带徒弟，贡献表如实填报"),
                ("职业底线", "代码抄作业=岗位上的'无证驾驶'，害人害己")])
            d.note("思政页：结合本课内容点一个真实案例，30秒即可，不贴标签。")
            d.extend_page("学习策略：这门课怎么学最有效", [
                ("先例后理", "先跑代码看结果，再回头懂原理——PRIMM教学法"),
                ("费曼技巧", "A层讲给D层听——讲得清才是真懂"),
                ("错题资产", "每个报错记入错误速查表——期末它是你的复习宝典"),
                ("提交习惯", "小步提交（每完成一步就commit）——回退不求人")])
            d.note("学习策略：四个方法贯穿全学期——第一周讲透，以后每周复用。")
            d.content(19, "进阶路线图（从今天的课往哪走）", [
                "本周：工单核心技能→下周：组合应用→期末：综合项目",
                "横向：本课技能在03课P项目链中的位置（工程化/全栈）",
                "纵向：证书线——初级操作题→中级工程题（1+X/工信部）",
                "竞赛线：校级选拔→世界职业院校技能大赛（人工智能赛道）",
                "岗位线：跟做学徒→独立操作→带组师傅→产线负责人"])
            d.note("进阶路线：把一门课放进三年坐标系——学完这周能走到哪。")
            from pptx.dml.color import RGBColor as _RC3
            d.fig_bars("本周各层达标预期（%）",
                       [("D层·跟做保底", 100, _RC3(0x44, 0x54, 0x6A)),
                        ("C层·基础完成", 80, _RC3(0x04, 0x75, 0xB6)),
                        ("B层·标准达成", 60, _RC3(0x05, 0x45, 0xE8)),
                        ("A层·进阶拓展", 30, _RC3(0xF5, 0x67, 0x0F))],
                       note="预期≠上限：动态升降制下人人可冲上一层")
            d.note("达标预期：四层的预期比例——D层100%保底是底线承诺。")
            d.content(20, "课前预习清单（下次课前完成）", [
                f"微课知识卡：{m3['skills'][0][:32]}（5分钟视频+导学单）",
                "Jupyter实训notebook：先跑教师版看答案，再试学生版",
                "预习快问：下次课quiz从微课与导学单出题——带着答案来",
                "Git推送本周工单：还没提交的课后补上（周达标率依据）"])
            d.note("预习清单：三项任务5-15分钟——闭环从课前开始。")
            d.content(21, "知识口袋书（本课概念速记）", [
                f"① {split_apply(m3['basics'][0])[0][:44]}" if m3["basics"] else "① 核心概念",
                f"② {split_apply(m3['basics'][1])[0][:44]}" if len(m3["basics"]) > 1 else "② 次要概念",
                f"③ {split_apply(m3['basics'][2])[0][:44]}" if len(m3["basics"]) > 2 else "③ 扩展概念",
                "用法：睡前30秒过一遍——口袋书越翻越薄，技能越练越厚"])
            d.note("口袋书：三条概念卡——期末汇总成全册，学生自查工具。")
            d.extend_page("输出对比：好的 vs 差的（规范从第一课开始）", [
                ("好的输出", "表头对齐·单位齐全·小数位统一·命名规范（snake_case）"),
                ("差的输出", "数字裸奔无单位·列不对齐·temp1/temp2乱命名·中文引号"),
                ("差多少分", "同样的功能——规范20%+素养15%两项就能差出35分"),
                ("为什么", "车间台账要给人看——读不懂的输出=没交付")])
            d.note("好差对比：两份同功能输出对比——规范分不是白给的。")
            d.extend_page("多解法一瞥（同一任务的不同打法）", [
                ("解法A·直白", "按工单步骤顺序实现——好懂好调试，D/C层路线"),
                ("解法B·工程", "函数封装+异常处理——可复用，B层路线"),
                ("解法C·进阶", "向量化/推导式/设计模式——性能优雅，A层路线"),
                ("怎么选", "先让它跑起来→再让它对→最后让它快（KISS原则）")])
            d.note("多解法页：同一工单三种深度——层不同，解法不同，都算对。")
            _qz = quiz_of(meta, m3, c["code"])
            if _qz:
                d.extend_page("自测答案与讲解", [
                    (q, a[:66]) for q, a in _qz] + [
                    ("错题怎么办", "回看对应知识卡+应用页，再跑一遍starter验证")])
                d.note("自测答案：逐题讲'为什么'——错题定位到知识卡编号。")
            d.content(9, "今日一图流总结（贴脑墙上）", [
                f"知识：{'；'.join(bt.split('——')[0][:20] for bt in m3['basics'][:3])}",
                f"技能：{'；'.join(m3['skills'][:2])}",
                f"交付：工单{meta['wono']}《{meta['woname']}》",
                "习惯：做完就Ctrl+K提交Git——每周至少1次",
                "明日：课前微课+导学单（下次课quiz从中出题）"])
            d.note("一图流总结：五句话收束全天——知识/技能/交付/习惯/明日。")
            # ===== 52号轮：学习工具箱（软件操作三页，48/49号轮指南浓缩） =====
            d.extend_page("工具箱①：Git提交四步（每周必做）", [
                ("第1步·暂存", "PyCharm按 Ctrl+K → 勾选改动文件"),
                ("第2步·提交", "Commit Message 按前缀写：feat:完成W%d工单核心" % meta_key),
                ("第3步·推送", "Ctrl+Shift+K 推送到 GitHub/Gitee——云端可查才算交"),
                ("第4步·验证", "网页刷新看到新提交=成功；每周≥1次，工程素养分依据")])
            d.note("Git工具箱：投屏演示一遍四步——学生跟着做一次就记住了。")
            d.extend_page("工具箱②：conda环境三命令（换课先切环境）", [
                ("激活", f"conda activate {ENV_OF[c['code']]}——提示符变({ENV_OF[c['code']]})才对"),
                ("装包", "激活后再 pip install——装错环境=白装"),
                ("核对", "python -c \"import sys; print(sys.executable)\" 路径含envs才对")])
            d.note("conda工具箱：三个命令一页——换课/换机先跑这三条。")
            d.extend_page("工具箱③：PyCharm效率五键", [
                ("Shift+F10", "运行当前文件（^R macOS）"),
                ("Shift+F9", "调试——断点停在红点行"),
                ("Ctrl+Alt+L", "格式化代码（⌘⌥L）——交作业前必按"),
                ("Ctrl+/", "注释/取消注释——调试好帮手"),
                ("Ctrl+`", "开关注册终端——跑服务/装包都在这")])
            d.note("PyCharm工具箱：五个键每天用——现场带练一遍。")
            d.thanks()
            d.note("下课提醒：关机→椅归位→带走工单；教师课后24h内完成反馈。")
            try:
                nw = c["meta"].get(meta_key + 1)
                nm3 = M3[c["code"]].get(meta_key + 1)
                if nw and nm3:
                    q = nw["quiz"] if c["mod"] == "data_ai" else nw["tasks"][0]["quiz"]
                    d.preview(next_title(c, meta_key + 1), q, meta_key + 1)
                    d.note("下次课预告：布置课前微课知识卡与导学单，形成学习闭环。")
            except Exception:
                pass
            from ppt_gen_v3 import _decorate
            _decorate(d, c["name"])
            fname = f"W{meta_key:02d}-第{no}次课-{title[:14]}.pptx"
            d.save(os.path.join(outdir, fname))
            count += 1
            pages += len(d.prs.slides._sldIdLst)
    print(f"{c['name']}: {count}个PPT, 平均{pages // max(count, 1)}页/课 → {outdir}")


LITERACY = {
    "ai": ["模型可解释与数据伦理：不迷信黑盒, 尊重隐私与合规红线",
           "工程化思维：从模型精度到系统可用, 版本可管理、结果可复现",
           "持续学习：追踪大模型前沿, 用工单沉淀个人知识资产"],
    "py": ["工匠精神：规范命名、及时保存、报错必究的编码习惯",
           "工程伦理：数据安全与隐私保护, 不抄代码、引用注明",
           "协作素养：ABCD角色轮换履职, 贡献表如实填报"],
    "pp": ["工程责任：代码可维护、文档完整、测试先行",
           "绿色计算：向量化省算力, 批量写入降开销",
           "职业规划：以项目档案袋对接岗位与竞赛"],
}


def next_title(c, wk):
    mod = __import__(c["mod"])
    m3 = M3[c["code"]].get(wk)
    if m3:
        return m3["skills"][0][:24]
    return "见下次课工单"


# ===== 52号轮：100页深度讲义扩展辅助 =====

def split_apply(bt):
    """basics条目拆分：主句 + '——应用：'后缀（40号轮扩充），无后缀返回(None, bt)"""
    if "——应用：" in bt:
        main, app = bt.split("——应用：", 1)
        return main.strip(), app.strip()
    return bt, None


def quiz_of(meta, m3, code):
    """随堂自测3题：课前quiz + 首条易错 + 首条知识（规则拼接，题干来自实数据）"""
    qs = []
    if meta.get("quiz"):
        qs.append(("课前快问", meta["quiz"][:60]))
    if m3.get("errors"):
        e0 = m3["errors"][0]
        qs.append((f"排错题：出现「{e0[0]}」", f"原因：{e0[1]}；解决：{e0[2]}"))
    b0 = m3["basics"][0] if m3.get("basics") else ""
    main, _ = split_apply(b0)
    if main:
        qs.append(("复述题：用自己的话说", main[:60]))
    return qs[:3]


INDUSTRY_DATA = {
    "py": [("设备接入数（台/月）", 42), ("告警响应达标率(%)", 96), ("台账电子化率(%)", 88)],
    "pp": [("清洗后数据可用率(%)", 95), ("仪表盘刷新延时(s)", 2), ("日报自动生成率(%)", 100)],
    "ai": [("模型准确率(%)", 92), ("推理耗时(ms/条)", 45), ("人工复核率(%)", 15)],
}

CERT_OF = {
    "py": "Python开发职业技能等级证书（工信部）——本课对应初级操作题",
    "pp": "Python开发职业技能等级证书（工信部）——工程模板/数据处理对应中级",
    "ai": "1+X AI应用实践（初级=M1-M3/中级=M4）——本课工单即考点",
}


def cs_posts(code):
    return {"py": "工业数据采集技术员、边缘计算运维员",
            "pp": "数据工程师、数据分析工程师",
            "ai": "AI应用工程师、工业视觉开发"}[code]


ENV_OF = {"py": "py02", "pp": "pp03", "ai": "ai01"}

INDUSTRY_CASE = {
    "py": ("车间设备台账还靠Excel手抄，格式天天错、查找靠肉眼",
           "Python变量+f-string+文件读写，30行代码生成规范台账卡",
           "下一步：把台账接到数据库（03课P5）/自动采集（02课W11）"),
    "pp": "三个系统的数据格式不统一，周报要人工合并两小时",
    "ai": "质检靠老师傅目检，漏检率高且疲劳",
}
INDUSTRY_CASE["pp"] = ("三个系统的数据格式不统一，周报要人工合并两小时",
                       "Pandas管道+Streamlit仪表盘，一键刷新自动出周报",
                       "下一步：模型预警（P6）/智能运维平台（P7选做）")
INDUSTRY_CASE["ai"] = ("质检靠老师傅目检，漏检率高且疲劳",
                       "分类模型+阈值规则，先自动化易判样本，人只复核疑难",
                       "下一步：视觉检测（M3）/大模型辅助诊断（M4）")


FAQ_BANK = {
    "py": [("pip装包很慢", "配清华镜像：pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple"),
           ("Jupyter启动不了", "先conda activate py02再jupyter notebook；看报错第一行"),
           ("代码能跑但不规范", "对照PEP 8卡：snake_case命名+4空格缩进+f-string")],
    "pp": [("pandas读取大CSV慢", "usecols选列+chunksize分块读，见W3微课"),
           ("Modbus连接拒绝", "先起plc_simulator再连5020；确认host是教师机IP"),
           ("streamlit页面不刷新", "改代码后浏览器右上Rerun或按R键")],
    "ai": [("torch安装失败", "用--index-url cpu官方源；确认在ai48环境里装"),
           ("模型指标波动大", "设random_state=42；数据先shuffle再划分"),
           ("ONNX推理结果不一致", "对齐预处理（同一scaler/归一化参数）")],
}


if __name__ == "__main__":
    for c in COURSES:
        build_course(c)


