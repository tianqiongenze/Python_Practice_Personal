# -*- coding: utf-8 -*-
"""M1-1b 特征设计与优化 starter（教学周2）：时域+频域双解造特征，用特征重要性证明设计值钱

运行: /opt/anaconda3/bin/python w2_feature_starter.py
数据: 合成泵振动（正常/轴承磨损两类，磨损类8Hz特征频率抬升——和工单剧情同源）
"""
import numpy as np
from sklearn.ensemble import RandomForestClassifier


def make_vib(n=400, seed=7):
    rng = np.random.RandomState(seed)
    t = np.linspace(0, 4, 400)
    x_norm = 0.3 * np.sin(2 * np.pi * 8 * t) + rng.randn(n) * 0.1
    x_wear = 0.3 * np.sin(2 * np.pi * 8 * t) + 0.25 * np.sin(2 * np.pi * 16 * t) + rng.randn(n) * 0.1
    return x_norm, x_wear


def feats_time(x):
    """解A 时域三件套：RMS / 峰峰值 / 峭度(尖锐度)"""
    # TODO-W2-1: 返回 [np.sqrt(np.mean(x**2)), np.ptp(x), float(((x-x.mean())**4).mean()/x.std()**4)]
    return []


def feats_freq(x):
    """解B 频域双特征：8Hz幅值 / 16Hz幅值（rfft取对应bin）"""
    # TODO-W2-2: rfft(x)的幅值谱，按频率分辨率找到8Hz与16Hz两个bin的幅值
    return []


def make_dataset():
    x_norm, x_wear = make_vib()
    X, y, names = [], [], ["rms", "ptp", "kurt", "a8", "a16"]
    for x, label in ((x_norm, 0), (x_wear, 1)):
        # 切4段各造一条样本（丰富样本量）
        for i in range(4):
            seg = x[i * 100:(i + 1) * 100]
            X.append(feats_time(seg) + feats_freq(seg))
            y.append(label)
    return np.array(X, dtype=float), np.array(y), names


if __name__ == "__main__":
    X, y, names = make_dataset()
    if X.shape[1] == len(names):
        clf = RandomForestClassifier(random_state=0).fit(X, y)
        order = np.argsort(clf.feature_importances_)[::-1]
        print("特征重要性排序:", [(names[i], round(clf.feature_importances_[i], 2)) for i in order])
        print("目标：正确挑出 a16（磨损的16Hz指纹）为Top1/Top2 —— 你的设计值钱了")
    else:
        print(f"先完成TODO-W2-1/2（当前特征{X.shape[1]}个/应5个）——教师参考见 教师参考/solutions.py")
