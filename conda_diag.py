#!/usr/bin/env python3
"""诊断 conda EnvironmentNameNotFound: py02 问题 - 只读探测,不改任何状态"""
import os, glob, shutil, subprocess, json

HOME = os.path.expanduser("~")
report = []

def sec(title):
    report.append(f"\n===== {title} =====")

# 1. 当前进程环境变量中的 conda 线索
sec("1. 当前进程环境变量 (conda 相关)")
for k in sorted(os.environ):
    if "CONDA" in k.upper() or k in ("PATH", "VIRTUAL_ENV", "SHELL", "HOME", "ZSH_VERSION"):
        v = os.environ[k]
        if k == "PATH":
            v = " | ".join(v.split(":"))
        report.append(f"{k} = {v}")

# 2. 所有 conda 安装候选
sec("2. 本机 conda 安装目录探测")
candidates = [
    f"{HOME}/anaconda3", f"{HOME}/miniconda3",
    f"{HOME}/opt/anaconda3", f"{HOME}/opt/miniconda3",
    "/opt/anaconda3", "/opt/miniconda3",
    "/usr/local/anaconda3", "/usr/local/miniconda3",
    "/usr/local/Caskroom/miniconda/base", "/usr/local/Caskroom/miniforge/base",
    "/usr/local/Caskroom/miniconda", "/usr/local/Caskroom/anaconda",
]
found_installs = []
for c in candidates:
    if os.path.isdir(c):
        found_installs.append(c)
        report.append(f"[存在] {c}")
# Homebrew 下更深的 base
for pat in ("/usr/local/Caskroom/*/*/base", "/opt/homebrew/Caskroom/*/*/base", "/opt/homebrew/Caskroom/miniforge/base"):
    for p in glob.glob(pat):
        if os.path.isdir(p):
            found_installs.append(p)
            report.append(f"[存在] {p}")
# which conda 指向
wc = shutil.which("conda")
report.append(f"shutil.which('conda') = {wc}")

# 3. environments.txt - 所有曾登记的环境真实路径
sec("3. ~/.conda/environments.txt (历史环境登记)")
envtxt = os.path.join(HOME, ".conda", "environments.txt")
py02_paths = []
if os.path.exists(envtxt):
    with open(envtxt, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            exists = os.path.isdir(line)
            report.append(f"{'[存在]' if exists else '[缺失]'} {line}")
            if os.path.basename(line) == "py02" or line.endswith("/py02"):
                py02_paths.append(line)
else:
    report.append("(文件不存在)")

# 4. 全盘搜索 py02 环境
sec("4. 全盘搜索 py02 环境目录")
search_roots = [HOME, "/opt", "/usr/local"]
seen = set()
for root in search_roots:
    if not os.path.isdir(root):
        continue
    try:
        for dirpath, dirnames, _ in os.walk(root):
            # 剪枝:跳过明显无关/巨大的目录
            dirnames[:] = [d for d in dirnames if d not in (
                ".Trash", "Library", "node_modules", ".git", ".svn",
                "__pycache__", ".venv", "venv", "site-packages",
            ) and not d.startswith(".npm")]
            depth = dirpath[len(root):].count(os.sep)
            if depth >= 6:
                dirnames[:] = []
                continue
            if os.path.basename(dirpath) == "py02":
                # 判断是否真的是 conda env(有 conda-meta)
                is_env = os.path.isdir(os.path.join(dirpath, "conda-meta"))
                if dirpath not in seen:
                    seen.add(dirpath)
                    report.append(f"[找到] {dirpath}  (conda-env={is_env})")
                    if is_env:
                        py02_paths.append(dirpath)
    except (PermissionError, OSError) as e:
        report.append(f"(跳过 {root}: {e})")
if not seen:
    report.append("(未找到任何名为 py02 的目录)")

# 5. py02 环境内容验证(若找到)
sec("5. py02 环境内容验证")
for p in dict.fromkeys(py02_paths):
    report.append(f"-- {p}")
    cm = os.path.join(p, "conda-meta")
    if os.path.isdir(cm):
        py = os.path.join(p, "bin", "python3")
        if os.path.exists(py):
            report.append(f"   bin/python3 存在: {py}")
            ver = os.path.join(p, "conda-meta", "python-3.")
            hits = [f for f in os.listdir(cm) if f.startswith("python-3.")]
            report.append(f"   conda-meta python 包: {hits}")
        else:
            report.append(f"   [警告] bin/python3 不存在,环境可能损坏")

# 6. 各安装自己的 envs 目录
sec("6. 各 conda 安装的 envs/ 目录内容")
for inst in dict.fromkeys(found_installs + ([os.path.dirname(wc).rsplit("/",2)[0]] if wc and "/bin/" in wc else [])):
    envs_dir = os.path.join(inst, "envs")
    if os.path.isdir(envs_dir):
        try:
            report.append(f"{envs_dir}: {sorted(os.listdir(envs_dir))}")
        except OSError as e:
            report.append(f"{envs_dir}: (无法读取: {e})")

# 7. shell 配置文件中的 conda init 块
sec("7. shell 配置文件 conda init 块")
for rc in (".zshrc", ".zprofile", ".zshenv", ".bash_profile", ".bashrc", ".profile"):
    p = os.path.join(HOME, rc)
    if not os.path.exists(p):
        continue
    try:
        with open(p, encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except OSError as e:
        report.append(f"{rc}: (无法读取: {e})")
        continue
    hits = [(i+1, l.rstrip()) for i, l in enumerate(lines) if "conda" in l.lower()]
    if hits:
        report.append(f"-- ~/{rc} ({len(hits)} 行命中):")
        for n, l in hits[:30]:
            report.append(f"   {n}: {l}")

# 8. VS Code 设置
sec("8. VS Code 用户设置 (conda/python 相关)")
vscode_settings = os.path.join(HOME, "Library/Application Support/Code/User/settings.json")
if os.path.exists(vscode_settings):
    try:
        with open(vscode_settings, encoding="utf-8", errors="replace") as f:
            content = f.read()
        hits = [l.strip() for l in content.splitlines() if ("conda" in l.lower() or "python" in l.lower())]
        for h in hits[:20]:
            report.append(f"   {h}")
    except OSError as e:
        report.append(f"(无法读取: {e})")
else:
    report.append("(文件不存在)")

# 9. 尝试运行 conda 命令(当前 PATH 环境)
sec("9. 运行 conda 命令复现")
conda_exe = wc
if conda_exe:
    for args in (["--version"], ["info", "--base"], ["env", "list"]):
        try:
            r = subprocess.run([conda_exe] + args, capture_output=True, text=True, timeout=60)
            report.append(f"$ conda {' '.join(args)}\n{r.stdout.strip() or r.stderr.strip()}")
        except Exception as e:
            report.append(f"$ conda {' '.join(args)} -> 异常: {e}")
else:
    report.append("PATH 中无 conda 可执行文件(仅 shell 函数)")

# 10. 尝试激活 py02 复现原始异常
sec("10. 复现 conda activate py02")
if conda_exe:
    script = f'source "{os.path.dirname(os.path.dirname(conda_exe))}/etc/profile.d/conda.sh" 2>/dev/null; conda activate py02 2>&1; echo "exit=$?"'
    for shell in ("/bin/zsh", "/bin/bash"):
        try:
            r = subprocess.run([shell, "-c", script], capture_output=True, text=True, timeout=60)
            report.append(f"[{shell}] {r.stdout.strip()} {r.stderr.strip()}")
        except Exception as e:
            report.append(f"[{shell}] 异常: {e}")

out = "\n".join(report)
print(out)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "conda-diag-report.txt"), "w", encoding="utf-8") as f:
    f.write(out)
print("\n[报告已落盘 conda-diag-report.txt]")
