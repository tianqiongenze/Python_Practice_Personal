# -*- coding: utf-8 -*-
"""生成28份可打印A4分层工单docx（每节课1份，含基础知识/技能点/ABCD四层/代码/错误表/评分）"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx import Document                       # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH    # noqa: E402
from docx.oxml.ns import qn                      # noqa: E402
from docx.shared import Cm, Pt, RGBColor         # noqa: E402

import meta3_ai, meta3_py, meta3_pp              # noqa: E402
import sessions_meta as SM                       # noqa: E402
import universe as UNI                           # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAT = os.path.join(BASE, "教学实施资料")
NAVY = RGBColor(0x01, 0x03, 0x28)
BLUE = RGBColor(0x05, 0x45, 0xE8)
ORANGE = RGBColor(0xC0, 0x4A, 0x0A)
GRAY = RGBColor(0x44, 0x54, 0x6A)

TASKS = []
AI_WONOS = ["M1.1", "M1.2", "M2.1", "M2.2", "M3.1", "M3.2", "M4.1", "M4.2"]
for i, w in enumerate(range(4, 12)):
    m = SM.AI_META[w]
    TASKS.append(("ai", w, meta3_ai.AI3[w], AI_WONOS[i],
                  m["woname"], "01-AI应用基础", "AI应用基础"))
PYW = {1: "0.1", 2: "0.2a", 3: "0.2b", 4: "0.3", 5: "0.4", 6: "0.5", 7: "1.1",
       8: "1.2", 9: "1.3", 10: "1.4", 11: "1.5", 12: "Z"}
PYN = {1: "设备参数初始化系统", 2: "工业实时告警系统Ⅰ", 3: "工业实时告警系统Ⅱ",
       4: "工业设备类设计", 5: "工业设备继承体系", 6: "健壮的工业数据采集程序",
       7: "工业数据格式转换工具", 8: "工业数据文件处理系统", 9: "工业故障分析报告生成系统",
       10: "工业图像处理与报告生成", 11: "工业互联网数据采集系统", 12: "综合项目数据处理系统"}
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

TIER_STYLE = {
    "A": ("A层·师傅(进阶拓展)", ORANGE),
    "B": ("B层·组长(标准达成)", BLUE),
    "C": ("C层·操作员(基础完成)", RGBColor(0x04, 0x75, 0xB6)),
    "D": ("D层·学徒(跟做保底)", GRAY),
}


def para(doc, text, size=10.5, bold=False, color=None, font="宋体",
         align=None, before=0, after=4):
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.name = "Times New Roman"
    r._element.rPr.rFonts.set(qn("w:eastAsia"), font)
    if color:
        r.font.color.rgb = color
    return p


def heading(doc, text, color=NAVY):
    p = para(doc, text, size=12, bold=True, color=color, font="黑体",
             before=10, after=4)
    pPr = p._p.get_or_add_pPr()
    from docx.oxml import OxmlElement
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "8")
    bottom.set(qn("w:color"), "0545E8")
    pBdr.append(bottom)
    pPr.append(pBdr)
    return p


def bullets(doc, items, prefix=""):
    for i, it in enumerate(items, 1):
        para(doc, f"{prefix}{i}. {it}", after=2)


def code_block(doc, title, code):
    para(doc, f"▍{title}", size=9.5, bold=True, color=BLUE, after=1)
    for line in code.splitlines():
        p = para(doc, line if line else " ", size=9, font="Consolas", after=0)
        p.paragraph_format.line_spacing = Pt(12)
        r = p.runs[0]
        r.font.name = "Consolas"
        r._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")
        sh = p._p.get_or_add_pPr()
        from docx.oxml import OxmlElement
        el = OxmlElement("w:shd")
        el.set(qn("w:val"), "clear")
        el.set(qn("w:fill"), "F3F6FD")
        sh.append(el)


def build(course_code, week, m3, wono, woname, folder, cname, meta):
    from env_tools import tool_for
    TOOL_PHRASE, _g = tool_for(course_code, week)
    doc = Document()
    sec = doc.sections[0]
    sec.top_margin = sec.bottom_margin = Cm(1.8)
    sec.left_margin = sec.right_margin = Cm(1.9)
    # 标题区
    para(doc, f"{cname} · 分层实训工单", size=9, color=GRAY, font="黑体",
         align=WD_ALIGN_PARAGRAPH.LEFT, after=0)
    para(doc, f"工单{wono}《{woname}》", size=16, bold=True, color=NAVY,
         font="黑体", align=WD_ALIGN_PARAGRAPH.CENTER, after=1)
    para(doc, f"第{week}周 · 2课时（80分钟） · 理实一体 · 难度见右栏",
         size=9.5, color=GRAY, align=WD_ALIGN_PARAGRAPH.CENTER, after=4)

    # 项目载体条（与PPT情境页同款集团条）
    dept = UNI.DEPTS.get(course_code, {}).get("name", "")
    scen = UNI.SCEN.get((course_code, week), "")
    strip = para(doc, f"◆ 项目载体：{UNI.GROUP['name']} · {dept}", size=10,
                 bold=True, color=RGBColor(0xFF, 0xFF, 0xFF), font="黑体",
                 align=WD_ALIGN_PARAGRAPH.CENTER, after=1)
    from docx.oxml import OxmlElement
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), "010328")
    strip._p.get_or_add_pPr().append(shd)
    if scen:
        para(doc, f"▍任务情境：{scen[:72]}{'……' if len(scen) > 72 else ''}",
             size=9, color=GRAY, font="楷体", align=WD_ALIGN_PARAGRAPH.LEFT,
             after=4)

    # 信息表
    t = doc.add_table(rows=2, cols=4)
    t.style = "Table Grid"
    info = [("工单号", wono), ("周次/课时", f"第{week}周/2课时"),
            ("地点", "双创中心302实训室"), ("角色层", "□A □B □C □D"),
            ("配套+工具", f"starter+Jupyter｜主用：{TOOL_PHRASE}"), ("提交命名", f"学号_姓名_{wono}"),
            ("评价", "D/C/B/A四级量表"), ("反馈", "24小时内")]
    for i, (k, v) in enumerate(info):
        cell = t.cell(i // 4, i % 4)
        cell.paragraphs[0].text = ""
        r1 = cell.paragraphs[0].add_run(f"{k}: ")
        r1.font.size = Pt(9)
        r1.font.bold = True
        r2 = cell.paragraphs[0].add_run(v)
        r2.font.size = Pt(9)

    heading(doc, "一、本课基础知识（课前资讯对应）")
    bullets(doc, m3["basics"])
    heading(doc, "二、本课技能点（做完你应该会）")
    bullets(doc, m3["skills"])

    heading(doc, "三、分层任务卡（按你的ABCD层执行；每4周动态升降）", ORANGE)
    for tier in "DCBA":
        name, color = TIER_STYLE[tier]
        d = m3["abcd"][tier]
        heading(doc, f"【{name}】目标：{d['goal']}", color)
        for i, s in enumerate(d["steps"], 1):
            para(doc, f"    步骤{i}: {s}", after=1)
        para(doc, f"    ✔ 达标标准: {d['std']}", size=10, bold=True,
             color=color, after=6)

    heading(doc, "四、关键代码参考")
    for title, code in m3["code"][:2]:
        code_block(doc, title, code)

    heading(doc, "五、常见错误速查")
    et = doc.add_table(rows=len(m3["errors"]) + 1, cols=3)
    et.style = "Table Grid"
    for ci, h in enumerate(("现象", "原因", "解决")):
        r = et.cell(0, ci).paragraphs[0].add_run(h)
        r.font.bold = True
        r.font.size = Pt(9)
    for ri, (a, b, c) in enumerate(m3["errors"], 1):
        for ci, v in enumerate((a, b, c)):
            r = et.cell(ri, ci).paragraphs[0].add_run(v)
            r.font.size = Pt(9)

    heading(doc, "六、提交物与评分")
    para(doc, "提交物: 程序/笔记本(含运行输出) + 本工单(勾选层与达标自评) + 过程记录",
         size=10)
    para(doc, "评分: 功能40% + 技术质量25% + 代码规范20% + 工程素养15%"
         "（D≥60 / C≥70 / B≥80 / A≥90，详见《工单评价通用量表》）", size=10)
    para(doc, "自评: 我完成了____层任务，最得意的一步是____________，"
         "卡壳最久的是____________。", size=10, color=GRAY)
    para(doc, "学号______ 姓名______ 组号____ 组长签字________",
         size=10, before=6)
    outdir = os.path.join(MAT, folder, "分层工单")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, f"W{week:02d}_{wono}_{woname[:10]}分层工单.docx")
    doc.save(path)
    return path


def get_meta(course, week):
    if course == "ai":
        return SM.AI_META[week]
    return {"py": SM.PY_META, "pp": SM.PP_META}[course][week]["tasks"][0]


if __name__ == "__main__":
    n = 0
    for code, w, m3, wo, nm, folder, cn in TASKS:
        build(code, w, m3, wo, nm, folder, cn, get_meta(code, w))
        n += 1
    print("生成分层工单:", n, "份")
