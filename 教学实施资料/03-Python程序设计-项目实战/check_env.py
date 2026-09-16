# -*- coding: utf-8 -*-
"""《Python程序设计（项目实战）》 环境一键自检（python check_env.py [--deep]）"""
import sys

DEEP = "--deep" in sys.argv

def imp(mod):
    def f():
        import importlib
        m = importlib.import_module(mod)
        return getattr(m, "__version__", "ok")
    return f

def font(path):
    def f():
        import os
        assert os.path.exists(path), "缺少字体: " + path
        return "OK"
    return f

def fileexists(path):
    def f():
        import os
        assert os.path.exists(path), "缺少: " + path
        return ""
    return f

def port(host, p):
    def f():
        import socket
        s = socket.create_connection((host, p), timeout=2); s.close()
        return f"port {p} ✓"
    return f


ok = warn = fail = 0

def check(name, need, fn):
    global ok, warn, fail
    try:
        extra = fn() or ""
        print(f"[PASS] {name} {extra}")
        ok += 1
    except Exception as e:
        if need:
            print(f"[FAIL] {name} —— {e}")
            fail += 1
        else:
            print(f"[WARN] {name}（按周可选）—— {e}")
            warn += 1

check("Python≥3.12", True, lambda: (__import__("sys").version_info >= (3, 12) and "v%d.%d" % sys.version_info[:2]) or (_ for _ in ()).throw(RuntimeError(sys.version.split()[0])))
check("Git", True, lambda: __import__("subprocess").run(["git", "--version"], capture_output=True, text=True).stdout.strip())
check("conda环境(需先conda activate pp03)", True, lambda: ("conda" in sys.executable or "envs" in sys.executable) or (_ for _ in ()).throw(RuntimeError(f"当前Python路径不含conda/envs: {sys.executable}（需conda activate pp03后再运行）")))
check("pandas", True, imp("pandas"))
check("numpy", True, imp("numpy"))
check("matplotlib", False, imp("matplotlib"))
check("scikit-learn", False, imp("sklearn"))
check("joblib", False, imp("joblib"))
check("sqlalchemy", False, imp("sqlalchemy"))
check("PLC三口启动器", True, fileexists("工具/plc_simulator.py"))
if DEEP:
    for p in (5020, 5021, 5022):
        check(f"PLC:{p}", False, port("127.0.0.1", p))
print("-" * 46)
# ===== P7扩展周新栈自检（32号轮，全部离线） =====
def check_p7():
    print("\n[P7扩展周] 多模数据库+异步服务栈")
    for mod, tip in [("litestar", "pip install litestar"), ("granian", "pip install granian"),
                     ("kuzu", "图数据库"), ("duckdb", "时序OLAP"), ("chromadb", "向量库"),
                     ("diskcache", "缓存回退"), ("sklearn", "诊断模型")]:
        try:
            __import__(mod)
            print(f"[PASS] {mod} 可用")
        except ImportError:
            print(f"[WARN] {mod} 缺失 → {tip}（选做周，不装不影响P1-P6）")
    try:
        import redis
        redis.Redis.from_url("redis://127.0.0.1:6399/0", socket_connect_timeout=1).ping()
        print("[PASS] Redis服务在线(6399) → KV后端=redis")
    except Exception:
        print("[WARN] Redis不可达 → 平台自动回退diskcache（功能等价）")



check_p7()

print(f"结果: PASS {ok} | WARN {warn} | FAIL {fail}")
print("开课口径: 必需项FAIL=0 即可开课" + ("；--deep已含服务/数据连通" if DEEP else "（--deep 检查服务与数据）"))
sys.exit(1 if fail else 0)
