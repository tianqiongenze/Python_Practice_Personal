# -*- coding: utf-8 -*-
"""AI48 每次课元数据（24次课）：由12任务块派生——第1次课重知识与基础实现，第2次课重优化与检查评价"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data_ai48 as D
import meta3_ai48 as _M3

SESSIONS = []  # (week, no, wono, woname, focus, quiz[2], steps, sp, sg, dec, sc)

for i, b in enumerate(D.BLOCKS, 1):
    wk = i + 3
    wono = b["no"]
    base = b["title"]
    m3 = _M3.AI48[i]
    q = [f"W{i+3}课前测①：本课工单{wono}的及格线是什么？（答：{b['sp'][0]}）",
         f"W{i+3}课前测②：'{b['keypts'][0]}'用一句话说说你的理解"]
    steps_a = ["回顾预习卡与微课", "知识精讲（先例后理）", "演示代码骨架", "基础实现（D/C层保底）", "小结+布置第2次课"]
    steps_b = ["错误速查复盘", "优化冲刺（B/A层）", "三层质检互查", "当堂评分与反馈", "下次课预告+微课"]
    sp, sg = b["sp"], b["sg"]
    dec = dict(title=f"{base}：备选方案决策矩阵",
               header=["备选方案", "可行性", "达标概率", "工时", "结论"],
               rows=[["方案A：按工单主线（starter起步）", "高", "高", "适中", "推荐主干"],
                     ["方案B：自选技术路线", "中", "中", "多", "A层可选"],
                     ["方案C：直接改现成项目", "低（无过程分）", "低", "少", "不建议"]],
               note="组内打分3分钟，结论与理由写入工单决策记录")
    scen_hook = b["desc"][0][-60:]
    SESSIONS.append(dict(week=wk, no=i * 2 - 1, wono=wono, woname=base + "（上）：基础实现",
                         focus="A", quiz=q, steps=steps_a, sp=sp, sg=sg, dec=dec, sc=scen_hook))
    SESSIONS.append(dict(week=wk, no=i * 2, wono=wono, woname=base + "（下）：优化与评价",
                         focus="B", quiz=[f"W{i+3}课中查①：'{m3['errors'][0][0]}'这个报错怎么排查？",
                                          f"W{i+3}课中查②：优秀线{sg[0]}你打算怎么冲？"],
                         steps=steps_b, sp=sp, sg=sg, dec=dec, sc=scen_hook))

assert len(SESSIONS) == 24
