# -*- coding: utf-8 -*-
"""M3-1 迁移学习 starter（教学周7）：冻结特征提取器+只训分类头——零torch理解ResNet精髓

思想实验（离线CPU版）：
  "预训练模型" = 一个固定的随机投影(不训练) → 模拟"别人已学好的特征提取器"
  迁移 = 冻结它，只训练顶端的逻辑回归头（小样本也能成事）
  对照 = 不用预训练特征，直接用原始像素训头（小样本大概率崩）
真机版( torchvision ResNet18冻结实验 )见教师GPU演示——概念在本文件。
"""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score


def make_task(n_per_class=40, seed=7):
    """小样本任务：每类仅40张8×8"缺陷图"（digit风格合成）"""
    from sklearn.datasets import load_digits
    d = load_digits()
    rng = np.random.RandomState(seed)
    idx = rng.choice(len(d.data), n_per_class * 2, replace=False)
    X, y = d.data[idx], (d.target[idx] >= 5).astype(int)      # 二分类：小数字/大数字
    return X / 16.0, y


class FrozenExtractor:
    """'预训练特征提取器'：固定随机投影（种子固定=别人训练好的权重）"""

    def __init__(self, dim=64, seed=42):
        rng = np.random.RandomState(seed)
        self.W = rng.normal(0, 0.1, (64, dim))               # 64像素 → 64维特征

    def transform(self, X):
        # TODO-W7-1: 返回非线性特征 np.maximum(X @ self.W, 0)（ReLU——"层"的味道）
        return X


def main():
    X, y = make_task()
    ext = FrozenExtractor()
    # 对照组：原始像素直接训头
    s_raw = cross_val_score(LogisticRegression(max_iter=500), X, y, cv=5).mean()
    # 迁移组：冻结提取器特征 → 训头
    # TODO-W7-2: Xf = ext.transform(X) 后同样5折cv，得 s_transfer
    s_transfer = None
    print(f"对照(原始像素训头): cv={s_raw:.2f}")
    if s_transfer is not None:
        print(f"迁移(冻结特征+训头): cv={s_transfer:.2f}")
        print("目标：迁移组≥对照组 —— 这就是'站在巨人肩膀上'的量化证据（写进冻结/微调取舍实验）")
    else:
        print("完成TODO-W7-1/2看对比——两个TODO各一行")


if __name__ == "__main__":
    main()
