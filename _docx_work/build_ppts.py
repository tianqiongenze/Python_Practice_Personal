# -*- coding: utf-8 -*-
"""批量生成48个授课PPT（每2课时一次课=1个PPT，80分钟）"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pptx.util import Emu
from ppt_gen import Deck
import sessions_meta as SM
import sessions_meta2 as SM2
FOUR, SIX = SM.FOUR, SM.SIX

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAT = os.path.join(BASE, "教学实施资料")

MARK = re.compile(r"^第(\d+)次课")

COURSES = [
    dict(mod="data_ai", code="ai", folder="01-AI应用基础", name="AI应用基础",
         meta=SM.AI_META, chk=SM.CHK_AI, place="双创中心302实训室",
         four_step_weeks=()),
    dict(mod="data_py", code="py", folder="02-程序设计基础", name="Python编程基础",
         meta=SM.PY_META, chk=SM.CHK_PY, place="双创中心302实训室",
         four_step_weeks=set(range(1, 7))),
    dict(mod="data_pp", code="pp", folder="03-Python程序设计-项目实战",
         name="Python程序设计（项目实战）", meta=SM.PP_META, chk=SM.CHK_PP,
         place="双创中心302实训室", four_step_weeks=()),
]

CN = "一二三四五六七八九十"


def cn_week(i):
    s = ""
    if i <= 10:
        return CN[i - 1] if i < 10 else "十"
    if i < 20:
        return "十" + CN[i - 11]
    return "二十" + (CN[i - 21] if i > 20 else "")


def split_sessions(week):
    """按'第N次课'标记切分一周内容 → [(no, header, [items])]"""
    out, cur = [], None
    for it in week["content"]:
        m = MARK.match(it)
        if m:
            if cur:
                out.append(cur)
            cur = (int(m.group(1)), it, [])
        elif cur is not None:
            cur[2].append(it)
    if cur:
        out.append(cur)
    return out


def group_items(items):
    """'1. x' 顶级 / '（1）y' 子级 → [(parent, [subs])]"""
    groups, cur = [], None
    for it in items:
        if re.match(r"^\d+[\.、]\s*", it):
            if cur:
                groups.append(cur)
            cur = (re.sub(r"^\d+[\.、]\s*", "", it), [])
        elif re.match(r"^[（(]\d+[)）]", it) and cur:
            cur[1].append(re.sub(r"^[（(]\d+[)）]", "", it))
        elif cur and it.strip():
            cur[1].append(it)
    if cur:
        groups.append(cur)
    return groups


def lesson_title(header, week):
    m = re.search(r"\u201c(.+?)\u201d", header)
    if m:
        return m.group(1)
    m = re.search(r"《(.+?)》", header)
    if m:
        return m.group(1)
    theme = next((x for x in week["content"] if x.startswith("本周主题")), "")
    return theme.replace("本周主题：", "")[:20] or "综合实训"


def goals_of(week):
    gs = []
    for ob in week["objectives"]:
        gs.append(re.sub(r"^\d+\.\s*", "", ob))
    while len(gs) < 3:
        gs.append("见工单任务书")
    # 压缩：去掉"1. 知识目标：" 前缀词后超长截断
    return [re.sub(r"^(知识目标|能力目标|素质目标)[:：]\s*", "", g)[:90] for g in gs[:3]]


def next_prev_of(homework):
    for h in homework:
        if h.startswith("预习"):
            return h
    return "见下次课工单任务书"


def build_course(c):
    mod = __import__(c["mod"])
    outdir = os.path.join(MAT, c["folder"], "授课PPT")
    os.makedirs(outdir, exist_ok=True)
    count = 0
    for wi, week in enumerate(mod.WEEKS, 1):
        week_no = None
        m = re.match(r"第([一二三四五六七八九十]+)周", week["week"])
        if m:
            week_no = m.group(1)
        sessions = split_sessions(week)
        # AI_META按实际周次(6-13)索引, PY/PP按第1周起索引
        meta_key = wi + 4 if c["mod"] == "data_ai" else wi
        week_meta = c["meta"].get(meta_key)
        for si, (no, header, items) in enumerate(sessions):
            meta = week_meta if c["mod"] == "data_ai" else week_meta["tasks"][si]
            d = Deck()
            title = lesson_title(header, week)
            sub = (f"第{week_no or cn_week(wi)}周 · 第{no}次课"
                   f"（2课时 · 80分钟）")
            d.cover(c["name"], f"{title}", sub,
                    f"{c['place']}  ·  理实一体  ·  配套工单与starter随堂发放")
            # 流程页
            flow = FOUR if wi in c["four_step_weeks"] else SIX
            note = ("每课时40分钟 · 本次课2课时共80分钟（四步法筑基）"
                    if wi in c["four_step_weeks"] else
                    "每课时40分钟 · 本次课2课时共80分钟（六步法课堂化）")
            d.flow(flow, note)
            d.goals(goals_of(week))
            d.review(meta["quiz"], c["chk"])
            d.scenario(meta["sc"] if meta["sc"] else
                       next((x for x in week["content"] if "项目" in x or "模块" in x), title))
            m2 = SM2.D.get((c["code"], meta_key, si), {})
            if m2.get("kn"):
                d.knowledge(0, m2["kn"])
            # 内容页（分组切块, v2压缩至≤2页）
            groups = group_items(items)
            bullets, slide_no = [], 1
            dcur = []          # (text, is_sub)
            def flush():
                nonlocal slide_no
                if dcur:
                    flat = []
                    for t, is_sub in dcur:
                        flat.append(("· " + t) if is_sub else t)
                    d.content(slide_no, f"{title}（{slide_no}）", flat)
                    slide_no += 1
            lines = 0
            for parent, subs in groups:
                est = 1 + len(subs)
                if lines + est > 9 and dcur:
                    flush()
                    dcur, lines = [], 0
                dcur.append((parent, False))
                lines += 1
                for s_ in subs:
                    dcur.append((s_, True))
                    lines += 1
            flush()
            # 决策/教法
            dec = meta["dec"]
            d.decision(dec["title"], dec["header"], dec["rows"], dec.get("note", ""))
            # 实施工单
            d.task(meta["wono"], meta["woname"], meta["steps"], meta["sp"], meta["sg"])
            d.tiers(meta["wono"], meta["sp"], meta["sg"],
                    m2.get("extA", "在优秀基础上完成创新优化"))
            d.steps_caution(meta["steps"], m2.get("cautions", ["按工单避坑清单执行"]))
            d.check()
            d.closing_tasks(week["homework"], next_prev_of(week["homework"]))
            d.shot_placeholder()
            d.thanks()
            fname = f"W{meta_key:02d}-第{no}次课-{title[:14]}.pptx"
            d.save(os.path.join(outdir, fname))
            count += 1
    print(c["name"], "生成PPT:", count, "个 →", outdir)


if __name__ == "__main__":
    for c in COURSES:
        build_course(c)
