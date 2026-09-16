# -*- coding: utf-8 -*-
"""AI48 文档层构建：授课计划表 + 教学方案 + 课程标准docx/PDF + 12份分层工单 + 元数据"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_common import PlanBuilder, SchemeBuilder
import data_ai48 as D
from build_worksheets import build as ws_build, TIER_STYLE  # noqa: F401
import meta3_ai48 as M3
import universe as UNI
from cs_data import COVER as _C  # 复用封面版式

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T1 = os.path.join(BASE, "《工业互联网专业电气制图与CAD授课计划表》.docx")
T2 = os.path.join(BASE, "LS2.2工业电气制图CAD绘制教学方案（前五周）.docx")
OUTDIR = os.path.join(BASE, "教学实施资料", "05-AI应用基础48课时版")
os.makedirs(OUTDIR, exist_ok=True)

if __name__ == "__main__":
    # 1) 授课计划表
    pb = PlanBuilder(T1)
    pb.build(D.PLAN_INFO, D.WEEKS, D.PLAN_SUM["theory"], D.PLAN_SUM["practice"],
             D.PLAN_SUM["total"])
    p_plan = os.path.join(BASE, "工业互联网应用专业《AI应用基础（48课时版）》授课计划表v2.0.docx")
    pb.save(p_plan)
    # 2) 教学方案
    sb = SchemeBuilder(T2)
    sb.build(D.SCHEME_INFO, D.BLOCKS)
    p_scheme = os.path.join(BASE, "LS3.2X工业智能应用AI系统开发教学方案（48课时版·第4-15周）v2.0.docx")
    sb.save(p_scheme)
    print("docs saved")

    # 3) 课程标准（build_standard 通用渲染）
    import datetime
    from build_cs import build_standard, extract_toc
    AI48 = dict(
        name="AI应用基础（48课时版）",
        cover_info=["部    门： 智能控制学院        ",
                    "编制依据： 本专业人才培养方案；职业教育国家教学标准体系（含2025年修订版专业教学标准）；《职业院校人工智能应用指引（2026版）》        ",
                    "制    订： 工业互联网应用专业教学团队        ",
                    "课程负责人：                    ",
                    "二级学院院长：                    ",
                    "制订时间： 2026  年 8 月"],
        info=dict(代码="B46010304X", 学院="智能控制学院", 名称="AI应用基础（48课时版）",
                  岗位="AI应用工程师、智能系统设计员、工业视觉系统开发员、工业互联网数据分析师",
                  学分="3", 总学时="48", 理论="24", 实训="24",
                  开课时间="第4-15周（12周×4课时，自第4周与《Python编程基础》并行开课）",
                  教材=("人工智能应用基础项目式教程", "程显毅 陈凤妹 王岩 编著", "978-7-111-77382-5", "机械工业出版社", "2025年4月", "高职本科新形态系列教材"),
                  前续=[("无Python先修要求", "自第4周与《Python编程基础》并行开设，不设Python先修门槛；课内以'Python速成箱'随任务内嵌最小语法（当堂10分钟速成+填空式脚手架），首月Pandas用法随工单即学即用"),],
                  后续=[("《Python程序设计（项目实战）》", "工程化落地"), ("毕业设计", "课题延续")]),
        性质定位=["专业核心课程扩展版：48课时完整覆盖'数据处理→机器学习→深度学习→视觉→大模型→多智能体'全谱系",
                 "以'不睡觉的运维中心'为总目标，12周剧情递进（两江智造集团·设备智能运维中心载体）",
                 "CPU优先全流程可跑，GPU仅作可选加速"],
        理念=["工程实践优于理论：先跑通再深究",
              "递进设计（W=教学周，学期周=教学周+3）：初级（W1-4夯实ML）→中级（W5-8深度与视觉）→高级（W9-12大模型与智能体）",
              "难度自适应：必修周工单保底+选修进阶挑战",
              "零硬件虚拟产线：数据生成器/故障模拟器/缺陷库/知识库/生产模拟器五件套",
              "可信AI：可解释、有出处、不造假"],
        五维融通=[
            ["岗（岗位）", "AI应用工程师/视觉开发/数据分析——运维中心'数据→特征→模型→智能体'全链岗位任务"],
            ["课（课程）", "M1-1a至Z共12个工单即课程主线，挂接两江智造12周连续剧情"],
            ["赛（竞赛）", "教学周W6竞标答辩制对标竞赛评审；W12答辩对标技能大赛'人工智能应用'赛项展示环节"],
            ["证（证书）", "考核点覆盖1+X AI应用实践（初级=M1-M3，中级=M4，高级=M5）"],
            ["创（创新）", "奖励函数设计/Prompt模板/业务洞察特征等成果入个人项目档案袋，可孵化双创项目"],
        ],
        思政=[
            "总目标：可信AI与制造强国——模型要有据可查，指标不许造假",
            "设计融入：12周剧情全部源自真实生产关切（漏报要命→生命至上；小样本→珍惜每一次标注）",
            "环节融入：限时调参守工程纪律；竞标答辩讲诚信；RAG引用标注即学术规范前置",
            "流程融入：素养计入工单评分；2号泵站'神仙数据'案例贯穿数据诚信教育",
            "案例映射：W4工时账→职业操守；W9脱敏红线→数据伦理；W11奖励漏洞→制度设计者的责任",
        ],
        x证书=["AI应用实践职业技能等级证书（初级/中级分级对标模块M1-M3/M4）",
               "工业互联网平台运维职业技能等级证书",
               "计算机视觉应用工程师（企业认证）"],
        知识目标=["掌握数据清洗与特征工程方法（M1）",
                  "掌握分类/集成/神经网络原理与调优（M2）",
                  "掌握迁移学习与目标检测应用（M3）",
                  "掌握LLM调用、Prompt工程与RAG（M4）",
                  "理解强化学习与多智能体协调（M5）"],
        能力目标=["能独立完成12个工单的端到端实现与评估",
                  "能做参数/方案级的工程权衡并留痕",
                  "能用本地LLM/RAG搭建可信问答",
                  "能完成综合项目答辩表达"],
        素质目标=["数据诚信与工程纪律", "团队竞标与协作", "持续学习与档案沉淀"],
        研究创新=["特征工程/Prompt/奖励函数三处微创新点",
                  "优秀档案袋可推荐参赛或孵化"],
        可持续=["向量化与早停的算力节约意识", "模型版本与知识库迭代管理"],
        教学方式=["讲演做+完整六步法（资讯·计划课前线上）；周次口径：本课程第4周开课，学期周=教学周+3",
                  "虚拟产线五件套（数据生成/故障模拟/缺陷库/知识库/生产模拟）",
                  "大一适配（34号轮）：面向大一下学期扩展班——全部实训CPU/离线；starter填空式脚手架12/12全覆盖（难度分级见包README）；先校园场景后工业场景（campus_skills→运维智能体同构迁移）",
                  "工单难度梯度⭐~⭐⭐⭐⭐⭐ + ABCD分层",
                  "竞标答辩与同伴学习"],
        任务=[[m[0], m[1], m[2]] for m in [
            ("M1 数据处理与特征工程", "第4-5周(教学周1-2)·8课时", "M1-1a数据清洗与质量评估；M1-1b特征设计与优化（工单含及格/优秀双线）"),
            ("M2 机器学习与神经网络", "第6-9周(教学周3-6)·16课时", "M2-1传统分类；M2-2 XGBoost调优；M2-3a MLP；M2-3b CNN/LSTM竞标"),
            ("M3 计算机视觉与迁移学习", "第10-11周(教学周7-8)·8课时", "M3-1 ResNet小样本；M3-2 YOLO实时检测"),
            ("M4 NLP与大模型应用", "第12-13周(教学周9-10)·8课时", "M4-1 LLM故障诊断；M4-2 RAG知识库问答"),
            ("M5 多智能体与强化学习", "第14周(教学周11)·8课时", "M5-1多智能体检修调度（gym-industrial）"),
            ("综合答辩", "第15周(教学周12)·4课时", "综合项目答辩（第23次预答辩/第24次正式）")]],
        实训条件=["双创中心302实训室：30台≥16GB内存计算机",
                  "软件：Python3.12+/PyTorch或TF/ONNX/本地mock LLM/gym-industrial",
                  "虚拟产线工具包随课程包提供（离线可跑）"],
        团队=["主讲1名（ML/DL工业应用3年+）", "实训指导1名", "企业导师线上答疑（可选）"],
        资源=["24个授课PPT（每页讲稿备注）",
              "12份分层工单 + starter全覆盖12/12（每工单一个~40行填空式starter：合成数据自带、离线CPU、含w1纯Py/Pandas双解、w6竞标双线基线、w7迁移思想实验、w8手搓检测器、w12答辩提纲生成）",
              "12个配音微课知识卡", "Jupyter实训（复用01包16个notebook+映射表）",
              "校园生活智能体（M4拓展实训）：工具/campus_skills（课表/DDL/专注计划3个Skill，OpenAI协议不限平台，verify_skills自检ALL PASS）+学生TODO版3处填空",
              "教师版《多解法手册》+solutions_multi_ai48.py（12工单×2解工程权衡，5项互验ALL PASS：IQR稳健性/WSPT调度/FFT差分去趋势）"],
        课程评价=["过程性评价80%：周工单50%+代码审查20%+学习投入10%",
                  "期末20%：第15周（第12教学周）综合项目答辩",
                  "每周24小时内反馈，第5周中期诊断"],
        通过标准=["各周工单达D级及以上；综合成绩≥60分",
                  "及格率目标≥90%，优秀率≥35%（扩展班口径）"],
        质量保障=[
            "三级闭环：学生评教+督导听课（'授课计划完整规范''内容符合课程标准'）+企业反馈",
            "周达标率连续两次<70%触发诊改台账",
            "课程标准年度修订（对齐1+X大纲与载体案例库）",
            "四层教学文件（课标/计划/方案/工单）开课前交叉校验",
        ],
    )
    import cs_data  # noqa: F401 确保模块可用
    p_cs = os.path.join(BASE, "工业互联网专业《AI应用基础（48课时版）》课程标准.docx")
    os.makedirs("/tmp/cs_pass", exist_ok=True)
    build_standard(AI48, "/tmp/cs_pass/pass48.docx")
    import subprocess
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir",
                    "/tmp/cs_pass", "/tmp/cs_pass/pass48.docx"], capture_output=True)
    build_standard(AI48, p_cs, toc_entries=extract_toc("/tmp/cs_pass/pass48.pdf"))
    pdfdir = os.path.join(BASE, "教学实施资料", "课标PDF版")
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir",
                    pdfdir, p_cs], capture_output=True)
    print("cs saved")

    # 4) 12份分层工单（复用 build_worksheets.build）
    n = 0
    for i, b in enumerate(D.BLOCKS, 1):
        wk = i + 3
        m3 = M3.AI48[i]
        fake_meta = dict()  # build()仅用参数，不需meta
        path = ws_build("ai48", wk, m3, b["no"], b["title"],
                        "05-AI应用基础48课时版", "AI应用基础（48课时版）", fake_meta)
        n += 1
    print("worksheets:", n)

    # 5) 元数据回写（本次全部产物）
    from docx import Document
    NOW = datetime.datetime(2026, 9, 9)
    AUTH = "工业互联网应用专业教学资源库"
    KW = "两江智造;项目载体;岗课赛证创;课程思政;六步法;ABCD分层;双创中心302;AI48"
    import glob
    files = [p_plan, p_scheme, p_cs] + glob.glob(
        os.path.join(OUTDIR, "分层工单", "*.docx"))
    for f in files:
        d = Document(f); cp = d.core_properties
        cp.title = os.path.basename(f)[:-5]; cp.author = AUTH
        cp.keywords = KW; cp.category = "高职高专教学文件"
        cp.created = cp.modified = NOW; d.save(f)
    print("metadata:", len(files))
