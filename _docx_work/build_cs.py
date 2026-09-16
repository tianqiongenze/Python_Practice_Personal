# -*- coding: utf-8 -*-
"""课程标准docx生成器 —— 严格复刻《电气制图与CAD》课程标准.docx 版式
封面(宋体36pt标题/黑体18pt信息/黑体16pt编印) + 目录 + 五章正文
(一级标题方正黑体_GBK16pt / 二级方正楷体_GBK16pt / 正文方正仿宋_GBK16pt 行距594exact)
+ 课程基本信息五列表 + 页脚页码
"""
from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor, Twips

S = "style-ish constants"
F_HEI = "方正黑体_GBK"
F_KAI = "方正楷体_GBK"
F_FS = "方正仿宋_GBK"


def set_run(run, font_ea, size_pt, bold=False, color=None):
    run.font.name = "Times New Roman"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), font_ea)
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    if color:
        run.font.color.rgb = color


def para(doc, text, font=F_FS, size=16, bold=False, align=None,
         line_exact=594, indent_chars=0, before_lines=0, space_after=0):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    if align is not None:
        pf.alignment = align
    pf.line_spacing = Pt(line_exact / 20)
    pf.space_before = Pt(before_lines * 12)
    pf.space_after = Pt(space_after)
    if indent_chars:
        pf.first_line_indent = Pt(size * indent_chars)
    r = p.add_run(text)
    set_run(r, font, size, bold)
    return p


def add_page_number_footer(section):
    footer = section.footer
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p.add_run("- ")
    set_run(r1, "宋体", 14)
    r = p.add_run()
    set_run(r, "宋体", 14)
    fld1, instr, fld2 = OxmlElement("w:fldChar"), OxmlElement("w:instrText"), OxmlElement("w:fldChar")
    fld1.set(qn("w:fldCharType"), "begin")
    instr.set(qn("xml:space"), "preserve")
    instr.text = r" PAGE \* MERGEFORMAT "
    fld2.set(qn("w:fldCharType"), "end")
    r._element.append(fld1)
    r._element.append(instr)
    r._element.append(fld2)
    r2 = p.add_run(" -")
    set_run(r2, "宋体", 14)


def toc_field(doc):
    p = doc.add_paragraph()
    r = p.add_run()
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), r'TOC \o "1-2" \h \z \u')
    tip = OxmlElement("w:r")
    t = OxmlElement("w:t")
    t.text = "（目录域：请在Word中右键“更新域”生成带页码目录）"
    tip.append(t)
    fld.append(tip)
    p._p.append(fld)


def build_standard(course, path, toc_entries=None):
    doc = Document()
    # 页面设置
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Twips(11906), Twips(16838)
    for a in ("top_margin", "bottom_margin", "left_margin", "right_margin"):
        setattr(sec, a, Twips(1411))

    # ============ 封面（首页无页码：titlePg） ============
    para(doc, f"《{course['name']}》", font="宋体", size=36,
         align=WD_ALIGN_PARAGRAPH.CENTER, before_lines=6)
    para(doc, "课程标准", font="宋体", size=36,
         align=WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, "")
    for line in course["cover_info"]:
        para(doc, line, font="黑体", size=18, before_lines=2)
    para(doc, "")
    para(doc, "重庆现代制造职业学院 编印", font="黑体", size=16,
         align=WD_ALIGN_PARAGRAPH.CENTER, before_lines=8)

    # ============ 新节(目录+正文), 页码从1重计 ============
    from docx.enum.section import WD_SECTION
    body_sec = doc.add_section(WD_SECTION.NEW_PAGE)
    body_sec.page_width, body_sec.page_height = Twips(11906), Twips(16838)
    for a in ("top_margin", "bottom_margin", "left_margin", "right_margin"):
        setattr(body_sec, a, Twips(1411))
    body_sec.footer.is_linked_to_previous = False

    # ============ 目录(静态页码, 无需更新域) ============
    para(doc, "目  录", font="黑体", size=16, bold=True,
         align=WD_ALIGN_PARAGRAPH.CENTER)
    if toc_entries:
        from docx.enum.text import WD_TAB_ALIGNMENT, WD_TAB_LEADER
        for level, text, page in toc_entries:
            p = doc.add_paragraph()
            pf = p.paragraph_format
            pf.line_spacing = Pt(24)
            pf.left_indent = Pt(0 if level == 1 else 24)
            pf.tab_stops.add_tab_stop(Twips(9070), WD_TAB_ALIGNMENT.RIGHT,
                                      WD_TAB_LEADER.DOTS)
            r = p.add_run(text + "\t" + str(page))
            set_run(r, "方正仿宋_GBK", 14, bold=(level == 1))
    else:
        toc_field(doc)   # 无页码数据时回退为目录域
    from docx.enum.text import WD_BREAK
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    add_page_number_footer(body_sec)

    H1 = lambda t: para(doc, t, font=F_HEI, size=16, before_lines=1)
    H2 = lambda t: para(doc, t, font=F_KAI, size=16)
    BODY = lambda t, n=2: para(doc, t, size=16, indent_chars=n)
    LIST = lambda items: [BODY(x) for x in items]

    # ============ 一、课程概述 ============
    H1("一、课程概述")
    H2("（一）课程基本信息")
    info = course["info"]

    def table(rows, widths, header_shade=None, fill="EDEDED"):
        t = doc.add_table(rows=len(rows), cols=len(widths))
        t.style = "Table Grid"
        t.autofit = False
        for ri, row in enumerate(rows):
            for ci, val in enumerate(row):
                cell = t.cell(ri, ci)
                cell.width = Cm(widths[ci] / 567)
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                p = cell.paragraphs[0]
                p.paragraph_format.line_spacing = Pt(18)
                r = p.add_run(str(val))
                set_run(r, F_FS, 12)
                if header_shade and ri in header_shade:
                    sh = OxmlElement("w:shd")
                    sh.set(qn("w:val"), "clear")
                    sh.set(qn("w:fill"), fill)
                    cell._tc.get_or_add_tcPr().append(sh)
        return t

    # 单行表（课程代码…实训学时）参照模板首表
    _tb = info.get("教材", ("", "", "", "", "", ""))
    table([["课程代码", info["代码"], "开课学院", info["学院"]],
           ["课程名称", info["名称"], "", ""],
           ["面向的职业及岗位", info["岗位"], "", ""],
           ["学分", info["学分"], "总学时", info["总学时"]],
           ["理论学时", info["理论"], "实习（训）学时", info["实训"]],
           ["课时标准", "每课时40分钟", "开课时间", info["开课时间"]],
           ["使用教材", _tb[0] + "（" + _tb[1] + "）ISBN " + _tb[2] + " | " + _tb[3] + " | " + _tb[4] + " | " + _tb[5], "", ""]],
          widths=[2450, 2400, 2450, 2400], header_shade={1, 2})
    # 合并课程名称/岗位值格
    doc_ = doc.tables[-1]
    doc_.cell(1, 1).merge(doc_.cell(1, 3))
    doc_.cell(2, 1).merge(doc_.cell(2, 3))
    doc_.cell(6, 1).merge(doc_.cell(6, 3))
    para(doc, "")

    H2("（二）本课程与其他课程的关系")
    para(doc, "本课程与其它课程的关系", size=14, align=WD_ALIGN_PARAGRAPH.CENTER)
    rel_rows = [["序号", "前续课程", "相互衔接和关联的知识点、技能点、软硬件工具、标准规范"]]
    rel_rows += [[str(i + 1), a, b] for i, (a, b) in enumerate(info["前续"])]
    rel_rows += [["序号", "后续课程", "相互衔接和关联的知识点、技能点、软硬件工具、标准规范"]]
    rel_rows += [[str(i + 1), a, b] for i, (a, b) in enumerate(info["后续"])]
    table(rel_rows, widths=[1100, 3100, 6500], header_shade={0, 1 + len(info["前续"])})
    para(doc, "")

    H2("（三）课程性质与定位")
    LIST(course["性质定位"])
    H2("（四）课程基本教学理念")
    LIST(course["理念"])
    H2("（五）\u201c岗课赛证创\u201d五维融通")
    rows = [["维度", "对接内容与落地载体"]]
    rows += [list(r) for r in course["五维融通"]]
    table(rows, widths=[2100, 8800], header_shade={0})
    para(doc, "")
    para(doc, "证书对接细则：", font="黑体", size=12, bold=True)
    LIST(course["x证书"])
    H2("（六）课程思政设计（三融入）")
    LIST(course["思政"])

    # ============ 二、教学目标 ============
    H1("二、教学目标")
    H2("（一）知识目标")
    LIST(course["知识目标"])
    H2("（二）能力目标")
    LIST(course["能力目标"])
    H2("（三）素质目标")
    LIST(course["素质目标"])
    H2("（四）研究与创新")
    LIST(course["研究创新"])
    H2("（五）可持续发展")
    LIST(course["可持续"])

    # ============ 三、教学内容 ============
    H1("三、教学内容")
    H2("（一）教学方式")
    LIST(course["教学方式"])
    H2("（二）教学任务与工作内容")
    task_rows = [["模块/任务", "周次·学时", "学习内容与工单项目"]]
    for m in course["任务"]:
        task_rows.append([m[0], m[1], m[2]])
    table(task_rows, widths=[2600, 1900, 6200], header_shade={0})
    para(doc, "")

    # ============ 四、课程实施保障条件 ============
    H1("四、课程实施保障条件")
    H2("（一）实训（实习）条件")
    LIST(course["实训条件"])
    H2("（二）教学团队")
    LIST(course["团队"])
    H2("（三）学习资源")
    LIST(course["资源"])

    # ============ 五、学习评价 ============
    H1("五、学习评价")
    H2("（一）课程评价")
    LIST(course["课程评价"])
    H2("（二）通过标准")
    LIST(course["通过标准"])
    H2("（三）质量保障与持续改进")
    LIST(course["质量保障"])

    doc.save(path)
    print("saved:", path)


def extract_toc(pdf_path):
    """从第一遍PDF提取各标题页码(正文节页码 = PDF页 - 2)"""
    import subprocess
    titles_h1 = ["一、课程概述", "二、教学目标", "三、教学内容",
                 "四、课程实施保障条件", "五、学习评价"]
    titles_h2 = ["（一）", "（二）", "（三）", "（四）", "（五）"]
    out = subprocess.run(["pdftotext", "-layout", pdf_path, "-"],
                         capture_output=True, text=True).stdout
    pages = out.split("\f")
    found = {}
    for pi, page in enumerate(pages, 1):
        for line in page.splitlines():
            t = line.strip()
            for h in titles_h1:
                if t.startswith(h) and h not in found and pi > 2:
                    found[h] = pi - 2
            for h in titles_h2:
                if t.startswith(h):
                    key = (pi, t[:14])
                    if not any(k[1] == t[:14] for k in found if isinstance(k, tuple)):
                        found[key] = pi - 2
    entries = []
    seen = set()
    for pi in range(3, len(pages) + 1):
        for line in pages[pi - 1].splitlines():
            t = line.strip()
            if not t:
                continue
            is_h1 = any(t.startswith(h) and len(t) < 16 for h in titles_h1)
            is_h2 = any(t.startswith(h) and len(t) < 16 for h in titles_h2)
            if (is_h1 or is_h2) and t not in seen:
                seen.add(t)
                entries.append((1 if is_h1 else 2, t, pi - 2))
    return entries
