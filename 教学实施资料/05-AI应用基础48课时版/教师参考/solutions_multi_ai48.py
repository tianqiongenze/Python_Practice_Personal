# -*- coding: utf-8 -*-
"""AI应用基础（48课时版）教师版·多解法互验（合成数据、全离线、秒级）
运行: /opt/anaconda3/bin/python solutions_multi_ai48.py → ALL PASS 才算数
完整解法地图见同目录《多解法手册.md》；M4-2 RAG双解复用 01包/教师参考/rag_chroma_demo.py
"""
import numpy as np

RESULTS = []


def check(name, fn, expect):
    got = fn()
    ok = got == expect
    RESULTS.append((name, ok))
    print(("✓" if ok else "✗"), name, "→", got)


def vib(n=2000, seed=7):
    t = np.linspace(0, 60, n)
    x = 4.0 + 0.6 * np.sin(2 * np.pi * 8 * t) + np.random.RandomState(seed).randn(n) * 0.3
    x[1500:1700] += np.linspace(0, 9, 200)     # 尾段异常抬升
    return t, x


# ===== M1-1a 异常检测双解：3σ vs IQR——同据零误报，且IQR对"污染数据"更稳健 =====
def m11a():
    _, x = vib()                                             # 尾段异常本身抬高了σ
    sig = (x > x.mean() + 3 * x.std())                        # 解A 3σ（σ被异常值拖大）
    q1, q3 = np.percentile(x, [25, 75])
    iqr = (x > q3 + 1.5 * (q3 - q1))                          # 解B IQR（四分位稳健）
    hit_sig = sig[1550:1700].mean()
    hit_iqr = iqr[1550:1700].mean()
    fp = sig[:1400].mean() + iqr[:1400].mean()                # 两解正常段都零误报
    return fp <= 0.02 and hit_iqr >= hit_sig and hit_iqr >= 0.9   # 结论: IQR≥3σ


# ===== M1-1b 特征双解：时域(RMS/峭度) vs 频域(主频FFT)——各证其明 =====
def m11b():
    t, x = vib()
    rms = float(np.sqrt(np.mean(x ** 2)))                     # 解A 时域
    from scipy.fft import rfft, rfftfreq
    xd = np.diff(x)                                           # 解B 频域：一阶差分去趋势
    freqs = rfftfreq(len(xd), t[1] - t[0])                    # (尾段斜坡的低频能量会淹没主频,
    main_f = float(freqs[np.argmax(np.abs(rfft(xd)))])        #  线性detrend去不掉局部斜坡)
    return round(rms, 1) >= 4.0 and abs(main_f - 8.0) < 0.5


# ===== M2-1a 分类双解：LR vs DT——同据F1齐达标、一致率≥0.85 =====
def m21a():
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import f1_score
    from sklearn.model_selection import train_test_split
    from sklearn.tree import DecisionTreeClassifier
    rng = np.random.RandomState(7)
    X = rng.normal(0, 1, (800, 5))
    y = rng.binomial(1, 0.4, 800)
    X[y == 1, :3] += 1.6
    Xtr, Xte, ytr, yte = train_test_split(X, y, stratify=y, random_state=42)
    lr = LogisticRegression(max_iter=500).fit(Xtr, ytr)
    dt = DecisionTreeClassifier(max_depth=8, random_state=0).fit(Xtr, ytr)
    f_lr = f1_score(yte, lr.predict(Xte))
    f_dt = f1_score(yte, dt.predict(Xte))
    agree = (lr.predict(Xte) == dt.predict(Xte)).mean()
    return f_lr >= 0.85 and f_dt >= 0.82 and agree >= 0.85


# ===== M2-2 调优双解：GridSearch(穷举) vs 随机搜索(预算)——小空间穷举胜/大空间省时 =====
def m22():
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, train_test_split
    rng = np.random.RandomState(7)
    X = rng.normal(0, 1, (500, 5))
    y = rng.binomial(1, 0.5, 500)
    X[y == 1, :3] += 1.4
    Xtr, Xte, ytr, yte = train_test_split(X, y, stratify=y, random_state=1)
    grid = {"n_estimators": [50, 100], "max_depth": [4, 6, 8]}
    gs = GridSearchCV(RandomForestClassifier(random_state=0), grid, cv=3).fit(Xtr, ytr)
    rs = RandomizedSearchCV(RandomForestClassifier(random_state=0), grid, n_iter=4,
                            random_state=0, cv=3).fit(Xtr, ytr)
    from sklearn.metrics import f1_score
    return (f1_score(yte, gs.predict(Xte)) >= 0.8
            and f1_score(yte, rs.predict(Xte)) >= 0.8
            and gs.best_score_ >= rs.best_score_ - 0.03)


# ===== M5-1 调度双解：FIFO vs WSPT价值密度贪心——加权流时间更优（奖励=管理哲学） =====
def m51():
    rng = np.random.RandomState(7)
    jobs = [{"id": i, "dur": rng.uniform(1, 9), "crit": rng.uniform(0.1, 1)} for i in range(30)]

    def weighted_flow(order):
        """关键设备越早处理越好：Σ完成时刻×关键度（WSPT经典规则）"""
        t = cost = 0.0
        for j in order:
            t += j["dur"]
            cost += t * j["crit"]
        return cost

    fifo = weighted_flow(jobs)                               # 解A 先来先做
    wspt = weighted_flow(sorted(jobs, key=lambda j: -j["crit"] / j["dur"]))  # 解B WSPT
    return wspt < fifo * 0.8                                 # 显著优于FIFO(>20%)


if __name__ == "__main__":
    check("M1-1a 异常双解(3σ/IQR)零误报且IQR更稳健", m11a, True)
    check("M1-1b 特征双解(时域RMS/频域主频)各证其明", m11b, True)
    check("M2-1a 分类双解(LR/DT)一致率≥0.85", m21a, True)
    check("M2-2 调优双解(穷举/随机)同档", m22, True)
    check("M5-1 调度双解(FIFO/WSPT)加权流时间省20%+", m51, True)
    bad = [n for n, ok in RESULTS if not ok]
    print(f"\n{len(RESULTS)}项多解互验：{'ALL PASS ✅' if not bad else 'FAIL ❌ ' + str(bad)}")
    print("M4-2 RAG双解 → 运行 ../../01-AI应用基础/教师参考/rag_chroma_demo.py")
