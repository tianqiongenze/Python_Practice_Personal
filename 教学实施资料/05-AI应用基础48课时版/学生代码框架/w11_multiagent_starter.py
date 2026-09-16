# -*- coding: utf-8 -*-
"""W11 多智能体检修调度 —— 学生starter（M5-1）
前置: python 工具/mini_sched_env.py  (自包含仿真, 无第三方依赖)
目标: 协调正确率≥75% + 奖励函数设计说明书(写入工单)
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "工具"))
from mini_sched_env import SchedEnv


def policy_random(env, s):
    import random
    return random.randint(0, 3)


def policy_alarm_first(env, s):
    """TODO-1: 规则策略——优先派检'告警且退化最高'的泵(无告警且无队列才等待)
    提示: s['degrade']与s['alarm']按泵站索引; 返回0=等待, 1-3=派检"""
    # === 你的代码 ===
    return 0


def main():
    env = SchedEnv(seed=42)
    s = env.reset(); total = 0.0
    for _ in range(200):
        a = policy_alarm_first(env, s)          # TODO-2: 换成你的策略对比(随机vs规则)
        s, r, done, info = env.step(a)
        total += r
        if done: break
    print(f"总奖励 {total:.1f} | 协调正确率 {env.accuracy():.1%} | 停机 {info['downtime']} 步")
    # TODO-3: 修改env的FIX_BENEFIT/IDLE_PENALTY做奖励敏感性实验, 表格入说明书
    # TODO-4(优秀): 包一层"感知-调度"两级agent: 感知预测下一告警泵, 调度提前派检


if __name__ == "__main__":
    main()
