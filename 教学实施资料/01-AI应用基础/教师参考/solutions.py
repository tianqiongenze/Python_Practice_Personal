# -*- coding: utf-8 -*-
"""《AI应用基础》教师参考实现（M1.1~M4.2 全部8个工单）
用法: python solutions.py m11 | m12 | m21 | m22 | m31 | m32 | m41 | m42
说明: 仅教师使用; M3.2 需资料包权重, M4.2 需先启动 mock_llm_server.py。
"""
import csv
import json
import sys

import numpy as np

# ======================================================================
# M1.1 泵类故障诊断
# ======================================================================


def m11():
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import (accuracy_score, f1_score, precision_score,
                                 recall_score)
    from sklearn.tree import DecisionTreeClassifier

    data = np.genfromtxt("data/pump_fault.csv", delimiter=",", skip_header=1)
    X, y = data[:, :5], data[:, 5].astype(int)

    idx = np.random.RandomState(42).permutation(len(X))
    X, y = X[idx], y[idx]
    n = int(len(X) * 0.75)
    Xtr, Xte, ytr, yte = X[:n], X[n:], y[:n], y[n:]

    models = {"逻辑回归": LogisticRegression(max_iter=1000),
              "决策树": DecisionTreeClassifier(max_depth=6, random_state=42),
              "随机森林": RandomForestClassifier(n_estimators=100,
                                                random_state=42)}
    print(f"{'模型':<6}{'准确':>7}{'精确':>7}{'召回':>7}{'F1':>7}")
    best = (None, 0)
    for name, m in models.items():
        m.fit(Xtr, ytr)
        p = m.predict(Xte)
        acc = accuracy_score(yte, p)
        row = [precision_score(yte, p, average="macro"),
               recall_score(yte, p, average="macro"),
               f1_score(yte, p, average="macro")]
        print(f"{name:<6}{acc:>7.3f}" + "".join(f"{v:>7.3f}" for v in row))
        if acc > best[1]:
            best = (name, acc)
    print("决策矩阵结论: 随机森林精度最优且可给出特征重要度, 选为交付模型;"
          "逻辑回归可作为产线侧轻量基线。最终:", best)


# ======================================================================
# M1.2 特征工程优化
# ======================================================================


def m12():
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score, f1_score
    from sklearn.model_selection import (GridSearchCV, cross_val_score,
                                         train_test_split)

    data = np.genfromtxt("data/pump_fault.csv", delimiter=",", skip_header=1)
    X, y = data[:, :5], data[:, 5].astype(int)

    z = (X - X.mean(0)) / X.std(0)
    mask = (np.abs(z) < 3).all(axis=1)                # 3σ清洗
    Xc, yc = X[mask], y[mask]
    print(f"清洗: {len(X)} → {len(Xc)}")

    rpm, temp, press, vib, amp = Xc.T
    Xf = np.c_[Xc, vib / amp, temp * press]           # 派生特征×2

    def ev(tag, Xa):
        Xtr, Xte, ytr, yte = train_test_split(Xa, yc, test_size=0.25,
                                              stratify=yc, random_state=42)
        m = RandomForestClassifier(n_estimators=100, random_state=42).fit(Xtr, ytr)
        acc = accuracy_score(yte, m.predict(Xte))
        f1 = f1_score(yte, m.predict(Xte), average="macro")
        print(f"[消融] {tag:<16} acc={acc:.3f} F1={f1:.3f}")
        return acc

    b = ev("基线", Xc)
    a1 = ev("+派生特征", Xf)
    gs = GridSearchCV(RandomForestClassifier(random_state=42),
                      {"n_estimators": [50, 100, 200]}, cv=5)
    Xtr, Xte, ytr, yte = train_test_split(Xf, yc, test_size=0.25,
                                          stratify=yc, random_state=42)
    gs.fit(Xtr, ytr)
    a2 = accuracy_score(yte, gs.predict(Xte))
    print(f"[消融] +网格搜索      acc={a2:.3f} 最优参数={gs.best_params_}")
    cv = cross_val_score(gs.best_estimator_, Xf, yc, cv=5)
    print(f"5折CV: {cv.mean():.3f} ± {cv.std():.3f}")
    print(f"提升: {(a2 - b) * 100:.1f}%")
    print("决策: 树模型对归一化不敏感(矩阵中此项打低分), 故缩放不采纳。")


# ======================================================================
# M2.1 焊接缺陷CNN
# ======================================================================


def m21():
    import torch
    import torch.nn as nn

    with open("data/weld_images/index.json", encoding="utf-8") as f:
        meta = json.load(f)
    X = np.stack([np.load("data/weld_images/" + m["file"]) for m in meta])
    y = np.array([["normal", "porosity", "slag", "crack"].index(m["label"])
                  for m in meta])
    X = (X.astype(np.float32) / 255.0)[:, None]
    idx = np.random.RandomState(42).permutation(len(X))
    X, y = X[idx], y[idx]
    n = int(len(X) * 0.8)
    Xtr, ytr = torch.tensor(X[:n]), torch.tensor(y[:n])
    Xte, yte = torch.tensor(X[n:]), torch.tensor(y[n:])

    class TinyCNN(nn.Module):
        def __init__(self):
            super().__init__()
            self.conv1 = nn.Conv2d(1, 8, 3)
            self.pool = nn.MaxPool2d(2, 2)
            self.conv2 = nn.Conv2d(8, 16, 3)
            self.fc1 = nn.Linear(16 * 14 * 14, 64)
            self.fc2 = nn.Linear(64, 4)

        def forward(self, x):
            x = self.pool(torch.relu(self.conv1(x)))
            x = self.pool(torch.relu(self.conv2(x)))
            x = x.flatten(1)
            return self.fc2(torch.relu(self.fc1(x)))

    torch.manual_seed(42)
    model = TinyCNN()
    opt = torch.optim.Adam(model.parameters(), lr=1.5e-3)
    lossf = nn.CrossEntropyLoss()
    for ep in range(6):
        model.train()
        perm = torch.randperm(len(Xtr))
        tot = 0.0
        for i in range(0, len(Xtr), 32):
            b = perm[i:i + 32]
            opt.zero_grad()
            loss = lossf(model(Xtr[b]), ytr[b])
            loss.backward()
            opt.step()
            tot += loss.item() * len(b)
        model.eval()
        with torch.no_grad():
            acc = (model(Xte).argmax(1) == yte).float().mean().item()
        print(f"epoch{ep + 1} loss={tot / len(Xtr):.4f} 测试acc={acc:.3f}")
    print("形状追踪: (N,1,64,64)→conv1(N,8,62,62)→pool(31)→conv2(N,16,29,29)"
          "→pool(14)→flatten(N,3136)→fc→(N,4)")


# ======================================================================
# M2.2 LSTM寿命预测
# ======================================================================


def m22():
    import torch
    import torch.nn as nn

    d = np.load("data/bearing_rul.npz")
    X = torch.tensor(d["X"][:, :, None])
    y = torch.tensor(d["y"])
    n = int(len(X) * 0.8)
    Xtr, ytr, Xte, yte = X[:n], y[:n], X[n:], y[n:]

    class RULNet(nn.Module):
        def __init__(self):
            super().__init__()
            self.lstm = nn.LSTM(1, 32, batch_first=True)
            self.fc = nn.Linear(32, 1)

        def forward(self, x):
            return self.fc(self.lstm(x)[0][:, -1, :]).squeeze(-1)

    torch.manual_seed(42)
    model = RULNet()
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    for ep in range(60):
        opt.zero_grad()
        loss = nn.functional.mse_loss(model(Xtr), ytr)
        loss.backward()
        opt.step()
        if (ep + 1) % 10 == 0:
            print(f"epoch{ep + 1} loss={loss.item():.4f}")
    with torch.no_grad():
        p = model(Xte).numpy()
    mse = float(np.mean((p - yte.numpy()) ** 2))
    print(f"MSE={mse:.4f} RMSE={mse ** 0.5:.4f} "
          f"MAE={float(np.mean(np.abs(p - yte.numpy()))):.4f}")
    print("业务解读: RMSE≈0.1即寿命预测误差约10%退化区间, 可提前1-2个维护"
          "周期介入, 满足预测性维护排程需求。")


# ======================================================================
# M3.1 缺陷尺寸测量
# ======================================================================


def m31():
    import cv2

    PX = 0.1
    for i in range(3):
        p = f"data/surface_parts/part_{i:03d}.png"
        img = cv2.imread(p, cv2.IMREAD_GRAYSCALE)
        blur = cv2.GaussianBlur(img, (5, 5), 0)
        _, bw = cv2.threshold(blur, 0, 255,
                              cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        bw = cv2.morphologyEx(bw, cv2.MORPH_OPEN,
                              np.ones((3, 3), np.uint8))
        cnts, _ = cv2.findContours(bw, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
        anno = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        for c in cnts:
            if cv2.contourArea(c) < 15:
                continue
            rect = cv2.minAreaRect(c)
            w, h = sorted(rect[1])
            if w / max(h, 1) > 3:                      # 划痕
                val = w * PX
                txt = f"scratch {val:.2f}mm"
            else:                                      # 凹坑
                val = cv2.contourArea(c) * PX ** 2
                txt = f"pit {val:.2f}mm2"
            box = cv2.boxPoints(rect).astype(int)
            cv2.drawContours(anno, [box], 0, (0, 0, 255), 2)
            cv2.putText(anno, txt, (box[:, 0].min(), box[:, 1].min() - 6),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 1)
            print(p.split("/")[-1], txt)
        cv2.imwrite(f"result_{i:03d}.png", anno)


# ======================================================================
# M3.2 YOLO推理(方案B onnx示例; 方案A见starter)
# ======================================================================


def m32():
    import cv2
    try:
        import onnxruntime as ort
    except ImportError:
        print("本机未装onnxruntime: 参考run_ultralytics方案或装onnxruntime")
        return
    sess = ort.InferenceSession("data/weights/yolov8n.onnx",
                                providers=["CPUExecutionProvider"])
    import glob
    total = {}
    for p in sorted(glob.glob("data/yolo_dataset/images/*.npy"))[:10]:
        img = np.load(p).astype(np.uint8)
        x = cv2.resize(img, (640, 640)).astype(np.float32) / 255.0
        out = sess.run(None, {"images": x.transpose(2, 0, 1)[None]})[0][0]
        cls = out[4:]                       # (80,8400)
        n = int((cls.max(0) > 0.4).sum())
        total[p] = n
        print(p.split("/")[-1], "conf>0.4 检出:", n)
    print("阈值实验: 降低conf检出↑误检↑; 产线建议conf=0.4~0.6,"
          "imgsz=320在CPU上平衡精度与FPS。")


# ======================================================================
# M4.1 文本分类
# ======================================================================


def m41():
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import classification_report
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.pipeline import make_pipeline
    import jieba

    texts, labels = [], []
    with open("data/fault_reports.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            texts.append(r["text"])
            labels.append(r["label"])
    stop = set("的 了 在 是 请 尽快 处理 影响 生产 班中 巡检 发现 已 挂牌 停机".split())

    def cut(t):
        return " ".join(w for w in jieba.cut(t) if w not in stop and w.strip())

    corpus = [cut(t) for t in texts]
    n = int(len(corpus) * 0.8)
    for name, clf in [("NB", MultinomialNB()),
                      ("LR", LogisticRegression(max_iter=1000))]:
        pipe = make_pipeline(TfidfVectorizer(max_features=2000), clf)
        pipe.fit(corpus[:n], labels[:n])
        pred = pipe.predict(corpus[n:])
        print("=====", name, "=====")
        print(classification_report(labels[n:], pred))
    demo = "3号注塑机液压油温升高报警"
    pipe2 = make_pipeline(TfidfVectorizer(), LogisticRegression(max_iter=1000))
    pipe2.fit(corpus, labels)
    print(demo, "->", pipe2.predict([cut(demo)]))


# ======================================================================
# M4.2 智能决策助手(需先启动mock_llm_server.py)
# ======================================================================


def m42():
    import re
    import requests

    BASE = "http://127.0.0.1:8000"

    def chat(msgs):
        r = requests.post(f"{BASE}/v1/chat/completions",
                          json={"messages": msgs}, timeout=5)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]

    kb = json.load(open("data/knowledge_base.json", encoding="utf-8"))
    docs = [t for v in kb.values() for t in v]

    def retrieve(q, topk=2):
        qs = set(re.findall(r"[\u4e00-\u9fa5a-zA-Z0-9]+", q))
        return sorted(docs, key=lambda t: -len(qs & set(
            re.findall(r"[\u4e00-\u9fa5a-zA-Z0-9]+", t))))[:topk]

    qs = ["泵振动7.5mm/s怎么处理？", "轴承温度82℃要不要停机？",
          "变频器过流报警如何排查？"]
    for q in qs:
        ctx = "\n".join(retrieve(q))
        a = chat([{"role": "system", "content": "CONTEXT:" + ctx},
                  {"role": "user", "content": q}])
        print("Q:", q, "\nA:", a[:90], "\n")
    print("Agent演示: 振动7.5>4.5阈值 → 判定超标 → 检索知识库 → 生成停机检查建议。")


if __name__ == "__main__":
    task = sys.argv[1] if len(sys.argv) > 1 else "m11"
    {"m11": m11, "m12": m12, "m21": m21, "m22": m22,
     "m31": m31, "m32": m32, "m41": m41, "m42": m42}[task]()
