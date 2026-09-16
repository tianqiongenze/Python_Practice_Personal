# -*- coding: utf-8 -*-
"""P7 智能运维平台 专属授课PPT（扩展第9周·选做·第17次课，DeckV3 v9风格+每页讲稿）"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import meta3_pp
import universe as UNI
from ppt_gen_v3 import DeckV3, _decorate
from sessions_meta import SIX
from pptx.dml.color import RGBColor as _RC

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PPTDIR = os.path.join(BASE, "教学实施资料", "03-Python程序设计-项目实战", "授课PPT")
ILL = os.path.join(PPTDIR, "_场景插画", "W9_场景.png")

m3 = meta3_pp.PP3[9]
SCEN = UNI.SCEN[("pp", 9)]
POS = [("课程性质", "综合项目课（扩展第9周·选做）：12周数据资产的工业化集成"),
       ("面向岗位", "工业互联网应用开发/智能运维平台开发工程师"),
       ("对接证书", "1+X数据应用与服务、AI应用实践（系统设计模块）"),
       ("课程衔接", "前：P6模型与部署 → 本课(五库+缓存+智能体+异步服务) → 后：毕业设计/实习")]
LIT = ["工程决策留痕：每个选型写'为什么'",
       "离线可跑：机房无外网也能ALL PASS",
       "可验证交付：verify.sh全绿才上线"]

d = DeckV3()
title = "智能运维平台：多模存储×智能体×异步服务"
d.cover("Python程序设计（项目实战）", "P7 智能运维平台综合项目",
        "第9周 · 第17次课（4课时 · 选做扩展）",
        "双创中心302实训室 · 理实一体 · 配套：分层工单+starter+verify.sh · 本课主用：Litestar+Granian+五库",
        dept=UNI.DEPTS["pp"]["name"], illus=ILL if os.path.exists(ILL) else None)
d.note("开场30秒：方总监验收P6后的新工单——把数据资产变成不睡觉的运维平台。")
d.agenda([("01", "课程定位", "课前已读", "综合项目定位与岗位价值"),
          ("02", "架构总览", "约10′", "五库选型决策矩阵"),
          ("03", "情境与任务", "约5′", "两江智造P7剧情+工单发布"),
          ("04", "技术精讲", "约20′", "Litestar/Granian/ReAct要点"),
          ("05", "任务实施", "六步法核心", "TODO-P7×5分层执行+verify.sh"),
          ("06", "检查与评价", "约15′", "端到端断言·当堂评分")],
         tail="资讯·计划已课前线上完成——课堂从架构决策直接开始")
d.section("01", "课程定位", "综合项目在本课程体系中的位置")
d.positioning("Python程序设计（项目实战）", POS)
d.note("指读课程衔接：P7把P2特征/P4采集/P5仓库/P6模型全部串起来（30秒）。")
d.mindmap("P7平台", [("五库", ["SQLite/DuckDB/Kùzu/Chroma/Redis"]),
                     ("服务", ["Litestar全异步", "Granian Rust运行时"]),
                     ("智能体", ["ReAct六步取证", "OpenAI协议工具"]),
                     ("缓存", ["TTL缓存命中", "INCR原子限流"]),
                     ("交付", ["verify.sh全绿", "决策矩阵留痕"])])
d.section("02", "架构总览", "为什么这么选——每个选型都要留痕")
d.content(1, "五库选型决策矩阵（摘自p77 README）", [
    "· 关系SQLite(WAL)：零运维台账；JSON列兼顾文档场景",
    "· 时序DuckDB：ASOF对齐+窗口降采样，一条SQL",
    "· 图Kùzu：嵌入式Cypher查拓扑影响路径（免Neo4j服务）",
    "· 向量Chroma：案例语义检索，哈希嵌入离线零下载",
    "· KV Redis：TTL缓存+原子INCR限流；无Redis回退diskcache"])
d.note("逐行问'淘汰了谁、为什么'——这就是决策矩阵的课堂形态。")
d.fig_bars("granian vs http.server 吞吐量级（课堂实测示意）",
           [("http.server", 1.0, _RC(0x44, 0x54, 0x6A)),
            ("uvicorn", 6, _RC(0x04, 0x75, 0xB6)),
            ("granian×2w", 12, _RC(0x05, 0x45, 0xE8))], ymax=14,
           note="B层作业：ab实测并把真实QPS填回本图")
d.section("03", "目标与资讯·情境", "带着目标进平台")
d.goals(["知识：" + m3["basics"][0][:26],
         "能力：" + m3["skills"][0][:26],
         "素质：工程决策留痕+可验证交付（课程思政）"])
d.review("课前测①：为什么时序数据不用SQLite逐行扫？",
         "课前测②：'泵停→主机联锁'用什么库查最快？")
d.scenario(SCEN, dept=UNI.DEPTS["pp"]["name"],
           illus=ILL if os.path.exists(ILL) else None)
d.note(f"情境说书30秒：{SCEN[:60]}…\n抛问：'五份数据五种库，还是一库走天下？'")
d.section("04", "技术精讲", "三个新姿势")
for i, b in enumerate(m3["basics"][:5], 1):
    d.basic_card(i, b)
    d.note(f"知识卡{i}：{b[:30]}… 讲法：例子→定义→点1人复述。")
d.quick_check(m3["basics"][:5])
d.skills(m3["skills"])
for ct, cc in m3["code"][:2]:
    d.code(ct, cc)
    d.note(f"演示《{ct}》：现场跑通一遍。")
d.section("05", "任务实施", "TODO-P7×5 · 分层 · verify.sh")
d.task("P7", "智能运维平台综合项目", m3["abcd"]["B"]["steps"],
       "verify.sh ALL PASS（五库+4API全绿）",
       "压测调优报告+bge嵌入对比（A层）")
tier_note = {"D": "D层deploy/run.sh一键起，截图live→cache。",
             "C": "C层补3个查询TODO，五库段全绿。",
             "B": "B层补Cypher与ReAct，ALL PASS。",
             "A": "A层压测+容器部署+嵌入升级。"}
for tier in "DCBA":
    t = m3["abcd"][tier]
    d.tier_detail(tier, t["goal"], t["steps"], t["std"], None)
    d.note(tier_note[tier])
d.errors(m3["errors"])
d.note("错误速查：现场制造'duckdb STRUCT报错'带学生三步排查。")
d.section("06", "检查与评价", "端到端断言 · 评分 · 展示")
d.check()
d.submission("P7")
d.literacy(LIT)
d.thanks()
d.preview("扩展阅读：bge嵌入/ONNX推理/消息队列", "课前测①答案：ASOF与列式聚合", 10)
d.note("P7为选做收官：作品直通毕业设计与企业实习答辩。")
_decorate(d, "Python程序设计（项目实战）")
out = os.path.join(PPTDIR, "W09-第17次课-P7智能运维平台.pptx")
d.save(out)
print("saved:", out, len(d.prs.slides._sldIdLst), "页")
