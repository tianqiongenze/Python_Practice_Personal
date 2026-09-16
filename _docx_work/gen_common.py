# -*- coding: utf-8 -*-
"""
模板克隆法 docx 生成器：
以参考模板 docx 为基底，深拷贝原型元素并替换文本，
保证字体、字号、边框、行高、节设置、页脚等格式与模板完全一致。
"""
import copy
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn

W = qn  # namespace helper


# ---------- 基础工具 ----------

def q(tag):
    return qn(tag)


def para_text(p):
    return "".join(t.text or "" for t in p.iter(q("w:t")))


def set_para_text(p, text):
    """将段落文本整体替换：保留第一个 run 的 rPr，删除其余 run 的 w:t 内容。
    若段落无 run，则依据段落标记属性（pPr/rPr）新建 run 以保持字体一致。"""
    runs = p.findall(q("w:r"))
    if not runs:
        first = p.makeelement(q("w:r"), {})
        pPr = p.find(q("w:pPr"))
        mark_rPr = pPr.find(q("w:rPr")) if pPr is not None else None
        if mark_rPr is not None:
            first.append(copy.deepcopy(mark_rPr))
        if pPr is not None:
            pPr.addnext(first)
        else:
            p.insert(0, first)
        runs = [first]
    first = runs[0]
    # 删除第一个 run 中除 rPr 外的所有子元素
    for child in list(first):
        if child.tag != q("w:rPr"):
            first.remove(child)
    t = first.makeelement(q("w:t"), {})
    t.text = text
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    first.append(t)
    # 其余 run 删除
    for r in runs[1:]:
        p.remove(r)


def set_para_jc(p, jc):
    """设置段落对齐；jc in (left, center, right, both)"""
    pPr = p.find(q("w:pPr"))
    if pPr is None:
        pPr = p.makeelement(q("w:pPr"), {})
        p.insert(0, pPr)
    jcEl = pPr.find(q("w:jc"))
    if jcEl is None:
        jcEl = pPr.makeelement(q("w:jc"), {})
        pPr.append(jcEl)
    jcEl.set(q("w:val"), jc)


def fill_para_list(proto_p, texts, jc=None):
    """由原型段落生成一组段落元素（list of w:p），texts 为字符串列表。"""
    out = []
    for txt in texts:
        np = copy.deepcopy(proto_p)
        set_para_text(np, txt)
        if jc:
            set_para_jc(np, jc)
        out.append(np)
    return out


def cell_paras(tc):
    return tc.findall(q("w:p"))


def fill_cell(tc, texts, jc=None):
    """填充单元格：以格内第一段为原型，生成 len(texts) 段。
    texts 为字符串列表。"""
    ps = cell_paras(tc)
    proto = ps[0]
    new_ps = fill_para_list(proto, texts, jc=jc)
    # 移除原有全部段落，追加新段（表格单元格至少要有一个 w:p）
    for p in ps:
        tc.remove(p)
    for p in new_ps:
        tc.append(p)


def table_rows(tbl):
    return tbl.findall(q("w:tr"))


def row_cells(tr):
    return tr.findall(q("w:tc"))


def clone(el):
    return copy.deepcopy(el)


def set_tr_texts(tr, texts_per_cell, jc_map=None):
    """按单元格顺序填充一行。texts_per_cell: list[list[str]]。
    jc_map: {cell_index: jc} 可选对齐覆盖。"""
    cells = row_cells(tr)
    assert len(cells) == len(texts_per_cell), \
        f"cell count mismatch: {len(cells)} vs {len(texts_per_cell)}"
    for i, tc in enumerate(cells):
        jc = jc_map.get(i) if jc_map else None
        fill_cell(tc, texts_per_cell[i], jc=jc)


# ---------- 授课计划表（模板1结构） ----------

class PlanBuilder:
    """基于《工业互联网专业电气制图与CAD授课计划表》模板生成授课计划表。"""

    # 模板 body 顶层元素索引
    IDX_TITLE1, IDX_TITLE2 = 0, 1
    IDX_INFO_TBL = 2
    IDX_SECT_BREAK = 3          # 纵向节结束段（含 sectPr）
    IDX_BIG_TBL = 4             # 横向 8 列大表
    IDX_EMPTY = 5
    IDX_SIGN1, IDX_SIGN2 = 6, 7
    IDX_FINAL_SECT = 8

    def __init__(self, template_path):
        self.doc = Document(template_path)
        body = self.doc.element.body
        self.body = body
        ch = list(body)
        self.proto = ch
        # v2 动态定位
        from docx.oxml.ns import qn as _qn
        _texts = [c for c in ch if c.tag == _qn("w:p") and "".join(c.itertext()).strip()]
        _tbls = [c for c in ch if c.tag == _qn("w:tbl")]
        assert len(_tbls) >= 2, "方案模板缺表格"
        self.e_title1, self.e_title2 = _texts[0], _texts[1]
        self.e_info = _tbls[0]
        self.e_pagebreak = None
        for c in ch:
            if c.tag == _qn("w:p") and c.findall(".//" + _qn("w:br")):
                for br in c.findall(".//" + _qn("w:br")):
                    if br.get(_qn("w:type")) == "page":
                        self.e_pagebreak = c
        self.e_block_title = next((c for c in _texts if "学习情境" in "".join(c.itertext())), _texts[2])
        self.e_block_tbl = next((t for t in _tbls if len(table_rows(t)) >= 20), _tbls[1])
        _i_blk = ch.index(self.e_block_tbl)
        _empt = [c for c in ch[_i_blk:] if c.tag == _qn("w:p") and not "".join(c.itertext()).strip()]
        self.e_filler = _empt[0] if _empt else None
        # v2 动态定位（模板空段顺序无关）：两标题段/两张表/签字两段/末元素
        texts = [c for c in ch if c.tag == qn("w:p") and "".join(c.itertext()).strip()]
        tbls = [c for c in ch if c.tag == qn("w:tbl")]
        assert len(tbls) >= 2, "模板缺表格"
        self.e_title1, self.e_title2 = texts[0], texts[1]
        self.e_info, self.big_tbl_el = tbls[0], tbls[1]
        big = tbls[1]
        i_big = ch.index(big)
        empties = [c for c in ch[:i_big] if c.tag == qn("w:p") and not "".join(c.itertext()).strip()]
        self.e_sect = empties[-1] if empties else ch[i_big - 1]
        tail_empty = [c for c in ch[i_big:] if c.tag == qn("w:p") and not "".join(c.itertext()).strip()]
        self.e_empty = tail_empty[0] if tail_empty else None
        sign = [c for c in ch if c.tag == qn("w:p") and "签字" in "".join(c.itertext())]
        self.e_sign1, self.e_sign2 = (sign + sign[-1:] * 2)[:2] if sign else (None, None)
        self.e_final = ch[-1]
        rows = table_rows(big)
        self.big_rows = rows
        assert len(rows) >= 17, f"大表行数{len(rows)}"
        self.proto_merge_head = rows[0]    # 教学内容与学时分配
        self.proto_col_head = rows[1]      # 列头
        self.proto_data = rows[2]          # 数据行
        self.proto_sum = rows[14]          # 合计
        self.proto_total = rows[15]        # 总计
        self.proto_note = rows[16]         # 说明

    def build(self, info_rows, week_rows, sum_theory, sum_practice, total):
        """
        info_rows: list of (label, [value_paras], jc) 长度 9，顺序：
            开课学院/授课教师/课程名称/课程类型/授课学期/授课专业及班级/教学方式/考核方式/周学时总学时
        week_rows: list of dict(week, content[list], theory, practice,
                                objectives[list], keypoints[list],
                                measures[list], homework[list])
        """
        body = self.body
        for child in list(body):
            body.remove(child)

        # 标题
        body.append(clone(self.e_title1))
        body.append(clone(self.e_title2))

        # 信息表：以模板 9 行为原型逐行替换
        info_tbl = clone(self.e_info)
        rows = table_rows(info_tbl)
        assert len(rows) == len(info_rows), f"info rows {len(rows)} vs {len(info_rows)}"
        for tr, (label, values, jc) in zip(rows, info_rows):
            cells = row_cells(tr)
            fill_cell(cells[0], [label], jc="center")
            fill_cell(cells[1], values, jc=jc)
        body.append(info_tbl)

        # 纵向节结束段
        body.append(clone(self.e_sect))

        # 大表
        big = clone(self.big_tbl_el)
        # 清空模板行
        for tr in table_rows(big):
            big.remove(tr)
        big.append(clone(self.proto_merge_head))
        big.append(clone(self.proto_col_head))
        for wk in week_rows:
            tr = clone(self.proto_data)
            cells = row_cells(tr)
            fill_cell(cells[0], [wk["week"]], jc="center")
            _cnt = list(wk["content"]) + wk.get("textbook", [])
            fill_cell(cells[1], _cnt)
            fill_cell(cells[2], [str(wk["theory"])], jc="center")
            fill_cell(cells[3], [str(wk["practice"])], jc="center")
            fill_cell(cells[4], wk["objectives"])
            fill_cell(cells[5], wk["keypoints"])
            fill_cell(cells[6], wk["measures"])
            fill_cell(cells[7], wk["homework"])
            big.append(tr)
        # 合计
        tr_sum = clone(self.proto_sum)
        cells = row_cells(tr_sum)
        fill_cell(cells[2], [str(sum_theory)], jc="center")
        fill_cell(cells[3], [str(sum_practice)], jc="center")
        big.append(tr_sum)
        # 总计
        tr_total = clone(self.proto_total)
        cells = row_cells(tr_total)
        fill_cell(cells[2], [str(total)], jc="center")
        big.append(tr_total)
        # 说明（固定文本，原样克隆）
        big.append(clone(self.proto_note))
        body.append(big)

        # 空段 + 签字 + 尾部 sectPr
        if self.e_empty is not None:
            body.append(clone(self.e_empty))
        if self.e_sign1 is not None:
            body.append(clone(self.e_sign1))
        if self.e_sign2 is not None:
            body.append(clone(self.e_sign2))
        body.append(clone(self.e_final))

    def save(self, path):
        self.doc.save(path)


# ---------- 教学方案（模板2结构） ----------

class SchemeBuilder:
    """基于《LS2.2工业电气制图CAD绘制教学方案》模板生成教学方案文档。"""

    IDX_TITLE1, IDX_TITLE2 = 0, 1
    IDX_INFO_TBL = 2
    IDX_PAGEBREAK = 3           # 含 w:br type=page 的段落
    IDX_BLOCK_TITLE = 5         # 块标题段
    IDX_BLOCK_TBL = 6           # 27 行块表
    IDX_FILLER = 8              # 空段

    def __init__(self, template_path):
        self.doc = Document(template_path)
        body = self.doc.element.body
        self.body = body
        ch = list(body)
        self.proto = ch
        # v2 动态定位（模板空段顺序无关）
        from docx.oxml.ns import qn as _qn
        _texts = [c for c in ch if c.tag == _qn("w:p") and "".join(c.itertext()).strip()]
        _tbls = [c for c in ch if c.tag == _qn("w:tbl")]
        assert len(_tbls) >= 2, "方案模板缺表格"
        self.e_title1, self.e_title2 = _texts[0], _texts[1]
        self.e_info = _tbls[0]
        self.e_pagebreak = None
        for c in ch:
            if c.tag == _qn("w:p"):
                for br in c.findall(".//" + _qn("w:br")):
                    if br.get(_qn("w:type")) == "page":
                        self.e_pagebreak = c
        self.e_block_title = next(
            (c for c in _texts if "学习情境" in "".join(c.itertext())), _texts[2])
        self.e_block_tbl = next(
            (t for t in _tbls if len(table_rows(t)) >= 20), _tbls[1])
        _i_blk = ch.index(self.e_block_tbl)
        _empt = [c for c in ch[_i_blk:]
                 if c.tag == _qn("w:p") and not "".join(c.itertext()).strip()]
        self.e_filler = _empt[0] if _empt else None
        self.block_rows = table_rows(self.e_block_tbl)

    def _pb(self):
        if self.e_pagebreak is not None:
            self.body.append(clone(self.e_pagebreak))

    def build(self, info_rows, blocks):
        """
        info_rows: list of (label, [value_paras], jc) 长度 9
        blocks: list of dict(title,
            form, hours, place, time,
            desc[list], learners[list], keypts[list], diffpts[list],
            resources[list], methods[list], key_measures[list], diff_measures[list],
            pre_teach, pre_stu, pre_goal,
            lead_teach, lead_stu, lead_goal, lead_time,
            r1_teach, r1_stu, r1_goal, r1_time,
            r1rv_teach, r1rv_stu, r1rv_goal, r1rv_time,
            r2_teach, r2_stu, r2_goal, r2_time,
            sum_teach, sum_stu, sum_goal, sum_time,
            ext_teach, ext_stu, ext_goal,
            effect[list], improve[list])
            其中 *_teach/*_stu/*_goal 为 list[str]，*_time 为 str
        """
        body = self.body
        for child in list(body):
            body.remove(child)

        # 标题（固定文本，原样克隆）
        body.append(clone(self.e_title1))
        body.append(clone(self.e_title2))

        # 信息表
        info_tbl = clone(self.e_info)
        rows = table_rows(info_tbl)
        assert len(rows) == len(info_rows), f"info rows {len(rows)} vs {len(info_rows)}"
        for tr, (label, values, jc) in zip(rows, info_rows):
            cells = row_cells(tr)
            fill_cell(cells[0], [label], jc="center")
            fill_cell(cells[1], values, jc=jc)
        body.append(info_tbl)

        # 各任务块
        first = True
        for blk in blocks:
            if first:
                self._pb()

                first = False
            else:
                # 块间分页：克隆分页段
                self._pb()
            # 块标题
            t = clone(self.proto[self.IDX_BLOCK_TITLE])
            set_para_text(t, blk["title"])
            body.append(t)
            # 块表
            tbl = clone(self.e_block_tbl)
            rows = table_rows(tbl)
            self._fill_block(rows, blk)
            body.append(tbl)
            # 教材衔接段（37号轮：教材预习/检查知识点独立渲染，不挤在desc格内）
            tb_lines = blk.get("textbook_lines", [])
            if tb_lines:
                from docx.oxml.ns import qn as _qn2
                from docx.oxml import OxmlElement as _OE
                _p = self.doc.add_paragraph()
                _r = _p.add_run("教材衔接与预习检查")
                _r.font.bold = True
                _r.font.size = Pt(11)
                body.append(_p._p)
                for ln in tb_lines:
                    _pp = self.doc.add_paragraph()
                    _rr = _pp.add_run(ln)
                    _rr.font.size = Pt(9.5)
                    body.append(_pp._p)
            # 块后收尾空段（保持与模板一致）
            if self.e_filler is not None:
                body.append(clone(self.e_filler))

        # 尾部 sectPr
        body.append(clone(self.proto[-1]))

    def _fill_block(self, rows, blk):
        R = lambda i: rows[i]

        def put(ri, ci, texts, jc=None):
            fill_cell(row_cells(R(ri))[ci], texts, jc=jc)

        # r0 一、任务分析（固定）
        # r1: 形式|理实一体|课时|X|地点|XX|时间|XX
        put(1, 1, [blk["form"]])
        put(1, 3, [blk["hours"]])
        put(1, 5, [blk["place"]])
        put(1, 7, [blk["time"]])
        # r2-r5
        put(2, 1, blk["desc"])
        put(3, 1, blk["learners"])
        put(4, 1, blk["keypts"])
        put(5, 1, blk["diffpts"])
        # r7-r10
        put(7, 1, blk["resources"])
        put(8, 1, blk["methods"])
        put(9, 1, blk["key_measures"])
        put(10, 1, blk["diff_measures"])
        # r13 课前准备, r14 任务导入
        put(13, 1, blk["pre_teach"]);  put(13, 2, blk["pre_stu"]);  put(13, 3, blk["pre_goal"]);  put(13, 4, [blk["pre_time"]])
        put(14, 1, blk["lead_teach"]); put(14, 2, blk["lead_stu"]); put(14, 3, blk["lead_goal"]); put(14, 4, [blk["lead_time"]])
        # r16 第一轮实施, r17 复盘
        put(16, 1, blk["r1_teach"]); put(16, 2, blk["r1_stu"]); put(16, 3, blk["r1_goal"]); put(16, 4, [blk["r1_time"]])
        put(17, 1, blk["r1rv_teach"]); put(17, 2, blk["r1rv_stu"]); put(17, 3, blk["r1rv_goal"]); put(17, 4, [blk["r1rv_time"]])
        # r19 第二轮实施, r20 总结
        put(19, 1, blk["r2_teach"]); put(19, 2, blk["r2_stu"]); put(19, 3, blk["r2_goal"]); put(19, 4, [blk["r2_time"]])
        put(20, 1, blk["sum_teach"]); put(20, 2, blk["sum_stu"]); put(20, 3, blk["sum_goal"]); put(20, 4, [blk["sum_time"]])
        # r23 课后拓展
        put(23, 1, blk["ext_teach"]); put(23, 2, blk["ext_stu"]); put(23, 3, blk["ext_goal"]); put(23, 4, [blk["ext_time"]])
        # r25-r26
        put(25, 1, blk["effect"])
        put(26, 1, blk["improve"])

    def save(self, path):
        self.doc.save(path)
