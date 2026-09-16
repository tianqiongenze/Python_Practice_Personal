# -*- coding: utf-8 -*-
"""Jupyter实训手册生成器: 28任务 × (学生版+教师版) = 56个ipynb
用 /opt/anaconda3/bin/python 运行本脚本。
结构(学生版): 工单信息/ABCD分层 → 资讯导学 → 环境与数据准备(可运行)
             → 任务与PRIMM引导 → starter分cell → 提交要求与避坑
结构(教师版): 简版说明 → 环境与数据准备 → 参考实现(inspect取源码) → 执行与验证
"""
import os
import sys

import nbformat as nbf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sessions_meta as SM          # noqa: E402
import sessions_meta2 as SM2        # noqa: E402

BASE = os.path.dirname(HERE)
MAT = os.path.join(BASE, "教学实施资料")

COURSES = {
    "ai": dict(folder="01-AI应用基础", name="AI应用基础", sol_file="教师参考/solutions.py",
               starter_dir="学生代码框架", sol_prefix="m", chk=SM.CHK_AI),
    "py": dict(folder="02-程序设计基础", name="Python编程基础", sol_file="教师参考/solutions.py",
               starter_dir="学生代码框架", sol_prefix="w", chk=SM.CHK_PY),
    "pp": dict(folder="03-Python程序设计-项目实战", name="Python程序设计（项目实战）",
               sol_file="教师参考/solutions.py", starter_dir="学生代码框架",
               sol_prefix="p", chk=SM.CHK_PP),
    "ai48": dict(folder="05-AI应用基础48课时版", name="AI应用基础（48课时版）",
                 sol_file="教师参考/solutions_multi_ai48.py", starter_dir="学生代码框架",
                 sol_prefix="w", chk=getattr(SM, "CHK_AI48", SM.CHK_AI)),
}

# (课程码, 周次, 任务码, 工单号, 工单名, starter文件, solutions函数名, 数据生成tag或None)
TASKS = [
    ("ai", 4, "m11", "M1.1", "泵类设备故障诊断系统", "m11_starter.py", "m11", "m1"),
    ("ai", 5, "m12", "M1.2", "特征工程优化的故障诊断系统", "m12_starter.py", "m12", None),
    ("ai", 6, "m21", "M2.1", "工业焊接缺陷检测系统", "m21_starter.py", "m21", "m2img"),
    ("ai", 7, "m22", "M2.2", "轴承寿命预测系统", "m22_starter.py", "m22", "m2rul"),
    ("ai", 8, "m31", "M3.1", "产品表面缺陷尺寸测量系统", "m31_starter.py", "m31", "m3"),
    ("ai", 9, "m32", "M3.2", "产线实时缺陷检测系统", "m32_starter.py", "m32", "m3yolo"),
    ("ai", 10, "m41", "M4.1", "工业故障报告自动分类系统", "m41_starter.py", "m41", "m4"),
    ("ai", 11, "m42", "M4.2", "工业智能决策助手系统", "m42_starter.py", "m42", "m4kb"),
]
PY_TASKS = [
    (1, "0.1", "设备参数初始化系统", "w01_device_init.py"),
    (2, "0.2a", "工业实时告警系统Ⅰ", "w02_alarm_if.py"),
    (3, "0.2b", "工业实时告警系统Ⅱ", "w03_alarm_loop.py"),
    (4, "0.3", "工业设备类设计", "w04_device_class.py"),
    (5, "0.4", "工业设备继承体系", "w05_inherit.py"),
    (6, "0.5", "健壮的工业数据采集程序", "w06_robust_collector.py"),
    (7, "1.1", "工业数据格式转换工具", "w07_parser.py"),
    (8, "1.2", "工业数据文件处理系统", "w08_fileio.py"),
    (9, "1.3", "工业故障分析报告生成系统", "w09_wordcloud_report.py"),
    (10, "1.4", "工业图像处理与报告生成", "w10_report_pdf.py"),
    (11, "1.5", "工业互联网数据采集系统", "w11_collector.py"),
    (12, "Z", "综合项目数据处理系统", "w12_project_template.py"),
]
for w, wo, nm, sf in PY_TASKS:
    TASKS.append(("py", w, f"w{w:02d}", wo, nm, sf, f"w{w:02d}", None))

# AI48: 12周×师生版notebook
AI48_TASKS = [
    (1, "M1-1a", "数据清洗与质量评估", "w1_clean_starter.py", "m11a"),
    (2, "M1-1b", "特征设计与优化", "w2_feature_starter.py", "m11b"),
    (3, "M2-1a", "传统分类逻辑回归与决策树", "w3_classify_starter.py", "m21a"),
    (4, "M2-2", "XGBoost参数调优", "w4_tuning_starter.py", "m22"),
    (5, "M2-3a", "MLP神经网络", "w5_mlp_starter.py", "m23a"),
    (6, "M2-3b", "CNN或LSTM二选一竞标", "w6_bidding_starter.py", "m23b"),
    (7, "M3-1", "ResNet迁移学习", "w7_transfer_starter.py", "m31"),
    (8, "M3-2", "YOLO实时缺陷检测", "w8_detect_starter.py", "m32"),
    (9, "M4-1", "LLM故障诊断Prompt工程", "w9_prompt_starter.py", "m41"),
    (10, "M4-2", "RAG知识库问答", "w10_rag_starter.py", "m42"),
    (11, "M5-1", "多智能体检修调度", "w11_multiagent_starter.py", "m51"),
    (12, "Z", "综合项目答辩", "w12_defense_starter.py", "z"),
]
for w, wo, nm, sf, fn in AI48_TASKS:
    TASKS.append(("ai48", w, f"W{w}", wo, nm, sf, fn, None))

PPD = [("p11", 1, "P1.1", "Python基础练习五题", "p11_exercises.py", "p11"),
       ("p12", 2, "P1.2", "标准Python工程模板", "p12_template.py", "p12"),
       ("p21", 3, "P2.1", "Pandas数据处理管道", "p21_pipeline.py", "p21"),
       ("p22", 4, "P2.2", "NumPy故障特征提取系统", "p22_features.py", "p22"),
       ("p33", 5, "P3", "产线KPI仪表盘与自动日报", "p33_dashboard.py", "p33"),
       ("p41", 6, "P4.1", "多源数据采集系统", "p41_collector.py", "P41DEMO"),
       ("p55", 7, "P5", "产线数据仓库与ORM", "p55_warehouse.py", "p55"),
       ("p66", 8, "P6", "故障诊断模型与部署", "p66_ml_service.py", "p66")]
for code, w, wo, nm, sf, fn in PPD:
    TASKS.append(("pp", w, code, wo, nm, sf, fn, None))

PREP_AI = '''\
# --- 环境与数据准备(勿改, 运行即可) ---
import os, sys, subprocess
os.chdir(os.path.abspath("../"))          # 切到课程包根目录(data/所在处)
print("工作目录:", os.getcwd())
'''
PREP_PY = PREP_AI
PREP_PP = PREP_AI


def prep_cell(course, tag):
    extra = ""
    if course == "ai" and tag:
        extra = f'\nsubprocess.run([sys.executable, "数据与工具/generate_data.py", "{tag}"], check=True)\nprint("数据已生成: data/")'
    return ("ai" and PREP_AI) + extra


def get_meta(course, week, sidx):
    if course == "ai48":
        import meta3_ai48 as _M3A48, sessions_ai48 as _S48
        m3 = _M3A48.AI48.get(week)
        if not m3:
            return None, {}
        s = _S48.SESSIONS[week - 1] if week <= len(_S48.SESSIONS) else {}
        _sp = s.get("sp", [""])
        _sg = s.get("sg", [""])
        meta = {"basics": m3["basics"], "skills": m3["skills"], "abcd": m3["abcd"],
                "code": m3.get("code", []), "errors": m3.get("errors", []),
                "quiz": s.get("quiz", ["", ""]),
                "sp": _sp[0] if isinstance(_sp, list) else _sp,
                "sg": _sg[0] if isinstance(_sg, list) else _sg,
                "woname": s.get("woname", ""), "wono": s.get("wono", ""),
                "steps": s.get("steps", [])}
        return meta, {}
    if course == "ai":
        return SM.AI_META.get(week), SM2.D.get((course, week, 0), {})
    m = {"py": SM.PY_META, "pp": SM.PP_META}[course].get(week)
    return (m["tasks"][sidx] if m else None), SM2.D.get((course, week, sidx), {})


def md_authors_meta(course, week, meta, m2, wo, wname, teacher=False):
    c = COURSES[course]
    tier = f"""
| 层 | 任务定位 | 达标要求 |
|----|---------|---------|
| **A 师傅** | 进阶拓展 | {m2.get('extA','创新优化')}；示范讲解 |
| **B 组长** | 标准达成 | {meta['sg']} |
| **C 操作员** | 基础完成 | {meta['sp']} |
| **D 学徒** | 跟做保底 | 跟做示例跑通TODO-1, 程序出结果 |
> 每4周按工单成绩动态升降层（连续2次≥B升一层）
"""
    head = f"""# {c['name']} · 工单{wo}《{wname}》
**第{week}周 | 2课时(80分钟) | 理实一体**  {'| 教师参考版' if teacher else '| 学生实训版'}
""" + ("" if teacher else tier)
    return head


def build_student(course, week, sidx, wo, wname, starter_file, tag):
    c = COURSES[course]
    meta, m2 = get_meta(course, week, sidx)
    nb = nbf.v4.new_notebook()
    cells = []
    cells.append(nbf.v4.new_markdown_cell(
        md_authors_meta(course, week, meta, m2, wo, wname)))
    cells.append(nbf.v4.new_markdown_cell(
        f"""## 一、课前资讯（Predict·预测）
> **预习快问**：{meta['quiz']}

> **课前检查**：{c['chk']}

## 二、PRIMM五步法（先读后写）
本工单按国际编程教学法 **PRIMM** 组织：
1. **Predict 预测**——先运行下方示例，猜输出再验证；
2. **Run 运行**——跑通环境与数据；
3. **Investigate 研究**——读懂starter每段在做什么；
4. **Modify 修改**——完成TODO改造；
5. **Make 创造**——独立完成工单任务。
"""))
    cells.append(nbf.v4.new_code_cell(prep_cell(course, tag)))
    cells.append(nbf.v4.new_markdown_cell(
        f"""## 三、任务要求（Make）
**实施步骤**
""" + "\n".join(f"{i+1}. {s}" for i, s in enumerate(meta["steps"])) +
        f"""

**验收标准**：及格(D)=`{meta['sp']}` ；优秀(B+)=`{meta['sg']}`
"""))
    # starter 分cell
    sp = os.path.join(MAT, c["folder"], c["starter_dir"], starter_file)
    if os.path.exists(sp):
        src = open(sp, encoding="utf-8").read()
        parts = [p.strip() for p in src.split("\n\n\n") if p.strip()]
        for i, part in enumerate(parts):
            title = part.splitlines()[0].strip()[:46]
            cells.append(nbf.v4.new_markdown_cell(
                f"### Starter {i+1}：`{title}`\n（Investigate: 读代码→Modify: 补全TODO）"))
            cells.append(nbf.v4.new_code_cell(part))
    else:
        cells.append(nbf.v4.new_markdown_cell("> starter文件缺失, 见学生代码框架目录"))
    cells.append(nbf.v4.new_markdown_cell(
        f"""## 四、提交要求与避坑
- 提交: `学号_姓名_{wo}.py` 或本notebook(含输出)
""" + "\n".join(f"- ⚠ {x}" for x in m2.get("cautions", []))))
    nb["cells"] = cells
    nb["metadata"]["kernelspec"] = {"name": "python3", "display_name": "Python 3"}
    return nb


def build_teacher(course, week, sidx, wo, wname, sol_fn, tag):
    import inspect
    import importlib.util
    c = COURSES[course]
    meta, m2 = get_meta(course, week, sidx)
    nb = nbf.v4.new_notebook()
    cells = [nbf.v4.new_markdown_cell(
        f"# {c['name']} · 工单{wo}《{wname}》 — 教师参考版\n"
        f"第{week}周 | 参考实现可直接运行验证 | 答案请勿下发学生")]
    cells.append(nbf.v4.new_code_cell(prep_cell(course, tag)))
    # 参考实现源码
    spec = importlib.util.spec_from_file_location(
        "sol", os.path.join(MAT, c["folder"], c["sol_file"]))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    fn = getattr(mod, sol_fn, None) if sol_fn else None
    # 模块级imports前置(修复函数源码脱离原模块后np等未定义)
    import re as _re
    sol_src = open(os.path.join(MAT, c["folder"], c["sol_file"]), encoding="utf-8").read()
    imp_lines = [l for l in sol_src.splitlines()
                 if _re.match(r"^(import |from )", l) and "solutions" not in l]
    imp_cell = "\n".join(imp_lines) + "\nimport numpy as np  # 通用科学计算\n"
    if fn is None and course == "pp" and sol_fn == "P41DEMO":
        cells.append(nbf.v4.new_markdown_cell(
            "## 最小三线程采集演示（完整版见 starter p41_collector.py）"))
        cells.append(nbf.v4.new_code_cell(P41_DEMO))
    elif fn is None:
        cells.append(nbf.v4.new_markdown_cell(
            "> 本任务参考实现见对应starter/独立脚本, 见工单说明。"))
        cells.append(nbf.v4.new_code_cell("print('参考实现见: 学生代码框架/ 与 教师参考/solutions.py')"))
    else:
        src = inspect.getsource(fn)
        cells.append(nbf.v4.new_markdown_cell(f"## 参考实现 `{sol_fn}`（含依赖导入）"))
        cells.append(nbf.v4.new_code_cell(imp_cell + "\n\n" + src))
        pre, post = runner(course, code := sol_fn)
        if pre:
            cells.append(nbf.v4.new_markdown_cell("## 运行环境(如需)"))
            cells.append(nbf.v4.new_code_cell(pre))
        cells.append(nbf.v4.new_markdown_cell("## 执行与验证"))
        cells.append(nbf.v4.new_code_cell(post.format(fn=code)))
    nb["cells"] = cells
    nb["metadata"]["kernelspec"] = {"name": "python3", "display_name": "Python 3"}
    return nb


def runner(course, fn):
    """特殊任务的运行前置/调用(模拟器/LLM/缩短时长)"""
    if course == "py" and fn == "w11":
        return ("""# 启动虚拟产线(离线模拟器, 5轮采集约15秒)
import subprocess, sys, time, atexit
p1 = subprocess.Popen([sys.executable, "虚拟产线/mini_modbus_server.py", "5020", "1"])
p2 = subprocess.Popen([sys.executable, "虚拟产线/mini_mqtt_broker.py", "1883"])
atexit.register(lambda: (p1.terminate(), p2.terminate()))
time.sleep(1.2)
print("模拟器就绪: PLC@5020 / MQTT@1883")""",
                "w11()")
    if course == "ai" and fn == "m42":
        return ("""# 本地模拟LLM服务(后台线程)
import threading, sys, importlib.util
spec = importlib.util.spec_from_file_location("mock", "数据与工具/mock_llm_server.py")
mock = importlib.util.module_from_spec(spec); spec.loader.exec_module(mock)
srv = mock.ThreadingHTTPServer(("127.0.0.1", 8000), mock.Handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()
print("mock LLM on :8000")""",
                "results = {fn}()")
    if course == "py" and fn == "w12":
        return (None,
                "import importlib.util as iu\n"
                "sp = iu.spec_from_file_location('sol', '教师参考/solutions.py')\n"
                "m = iu.module_from_spec(sp); sp.loader.exec_module(m)\n"
                "m.w12()")
    if course == "pp" and fn == "p21":
        return ("import subprocess, sys\n"
                "subprocess.run([sys.executable, '学生代码框架/p21_pipeline.py', '--peek'], check=True)\n"
                "print('样例脏数据已生成: p21_raw.csv')",
                "p21()")
    if course == "pp" and fn == "p41":
        return ("""# 启动三台PLC模拟器
import subprocess, sys, time, atexit
ps = [subprocess.Popen([sys.executable, "../02-程序设计基础/虚拟产线/mini_modbus_server.py",
                        str(p), str(u)]) for p, u in [(5020,1),(5021,2),(5022,3)]]
atexit.register(lambda: [p.terminate() for p in ps])
time.sleep(1.2)
print("3台PLC就绪")""",
                "from pymodbus.client import ModbusTcpClient as C\n"
                "c = C(host='127.0.0.1', port=5020); c.connect()\n"
                "rr = c.read_holding_registers(address=0, count=5)\n"
                "print('PLC1读数:', rr.registers)\nc.close()\n"
                "print('完整三线程系统见 学生代码框架/p41_collector.py; 教师演示可运行之')")
    return None, f"{fn}()"



P41_DEMO = """
# --- P4.1 最小三线程演示: 采集→Queue→处理→统计(运行约10秒) ---
import subprocess, sys, time, atexit, queue, threading
ps = [subprocess.Popen([sys.executable,
        "../02-程序设计基础/虚拟产线/mini_modbus_server.py", str(p), str(u)])
      for p, u in [(5020, 1), (5021, 2), (5022, 3)]]
atexit.register(lambda: [p.terminate() for p in ps])
time.sleep(1.2)
from pymodbus.client import ModbusTcpClient

q = queue.Queue(maxsize=1000)
stat = {"ok": 0, "fail": 0, "got": 0}
stop = threading.Event()

def collect():
    clients = [ModbusTcpClient(host="127.0.0.1", port=p) for p in (5020, 5021, 5022)]
    [c.connect() for c in clients]
    while not stop.is_set():
        for c in clients:
            try:
                rr = c.read_holding_registers(address=0, count=5)
                q.put(rr.registers, timeout=1); stat["ok"] += 1
            except Exception:
                stat["fail"] += 1
        time.sleep(0.5)

def process():
    while not stop.is_set() or not q.empty():
        try:
            rows = q.get(timeout=1); stat["got"] += 1
        except queue.Empty:
            pass

t1, t2 = threading.Thread(target=collect), threading.Thread(target=process)
t1.start(); t2.start(); time.sleep(8); stop.set(); t1.join(); t2.join()
total = stat["ok"] + stat["fail"]
print(f"采集率: {stat['ok']}/{total} = {stat['ok']/max(total,1):.1%} | 入队处理 {stat['got']} 条")
[p.terminate() for p in ps]
print("演示完成; 完整三线程系统(断线重连/入库)见 学生代码框架/p41_collector.py")
"""


if __name__ == "__main__":
    made = 0
    for course, week, code, wo, wname, starter, sol_fn, tag in TASKS:
        c = COURSES[course]
        outdir = os.path.join(MAT, c["folder"], "Jupyter实训")
        os.makedirs(outdir, exist_ok=True)
        sidx = 0 if course == "ai" else 0    # 每任务的第1次课meta
        stu = build_student(course, week, sidx, wo, wname, starter, tag)
        nbf.write(stu, os.path.join(outdir, f"{code}_{wo}_{wname[:8]}_学生版.ipynb"))
        tea = build_teacher(course, week, sidx, wo, wname, sol_fn, tag)
        nbf.write(tea, os.path.join(outdir, f"{code}_{wo}_{wname[:8]}_教师版.ipynb"))
        made += 2
    print("生成notebook:", made, "个")

