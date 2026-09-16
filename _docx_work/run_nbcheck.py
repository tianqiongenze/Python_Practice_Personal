# -*- coding: utf-8 -*-
"""用本地Anaconda Jupyter执行验证全部教师版notebook"""
import glob
import os
import subprocess
import sys
import time, functools
print = functools.partial(print, flush=True)

MAT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "教学实施资料")
files = sorted(glob.glob(os.path.join(MAT, "0*", "Jupyter实训", "*_教师版.ipynb")))
print("待验证:", len(files), "个")
ok, fail = [], []
for f in files:
    t0 = time.time()
    r = subprocess.run(
        ["/opt/anaconda3/bin/jupyter", "nbconvert", "--to", "notebook",
         "--execute", "--inplace", "--ExecutePreprocessor.timeout=300", f],
        capture_output=True, text=True, cwd=os.path.dirname(f))
    dt = time.time() - t0
    name = "/".join(f.split("/")[-3:])
    if r.returncode == 0:
        ok.append(name)
        print(f"PASS {name} ({dt:.0f}s)")
    else:
        fail.append((name, r.stderr[-500:]))
        print(f"FAIL {name} ({dt:.0f}s)")
print(f"\n===== 结果: {len(ok)} PASS / {len(fail)} FAIL =====")
for n, e in fail:
    print("----", n, "----\n", e[-400:])
