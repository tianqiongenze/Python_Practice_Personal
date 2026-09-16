# -*- coding: utf-8 -*-
"""《Python编程基础》 环境一键自检（python check_env.py [--deep]）"""
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
check("jieba", False, imp("jieba"))
check("wordcloud", False, imp("wordcloud"))
check("Pillow", False, imp("PIL"))
check("reportlab", False, imp("reportlab"))
check("pymodbus(3.x)", False, imp("pymodbus"))
check("paho-mqtt", False, imp("paho.mqtt"))
check("思源字体", True, font("../fonts/SourceHanSansCN-Regular.otf"))
check("虚拟PLC脚本", True, fileexists("虚拟产线/mini_modbus_server.py"))
check("虚拟MQTT脚本", True, fileexists("虚拟产线/mini_mqtt_broker.py"))
if DEEP:
    check("PLC服务:5020", False, port("127.0.0.1", 5020))
    check("MQTT代理:1883", False, port("127.0.0.1", 1883))
print("-" * 46)
print(f"结果: PASS {ok} | WARN {warn} | FAIL {fail}")
print("开课口径: 必需项FAIL=0 即可开课" + ("；--deep已含服务/数据连通" if DEEP else "（--deep 检查服务与数据）"))
sys.exit(1 if fail else 0)
