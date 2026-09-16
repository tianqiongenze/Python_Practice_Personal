# -*- coding: utf-8 -*-
"""生成3门课程的授课计划表与教学方案（共6个docx）"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gen_common import PlanBuilder, SchemeBuilder
import data_ai
import data_py
import data_pp

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T1 = os.path.join(BASE, "《工业互联网专业电气制图与CAD授课计划表》.docx")
T2 = os.path.join(BASE, "LS2.2工业电气制图CAD绘制教学方案（前五周）.docx")

# 简单校验：python-docx 版本输出位置
print("venv python:", sys.executable)


def build_course(mod, plan_name, scheme_name):
    # 授课计划表
    pb = PlanBuilder(T1)
    pb.build(mod.PLAN_INFO, mod.WEEKS,
             mod.PLAN_SUM["theory"], mod.PLAN_SUM["practice"],
             mod.PLAN_SUM["total"])
    out1 = os.path.join(BASE, plan_name)
    pb.save(out1)
    print("saved:", out1)

    # 教学方案
    sb = SchemeBuilder(T2)
    sb.build(mod.SCHEME_INFO, mod.BLOCKS)
    out2 = os.path.join(BASE, scheme_name)
    sb.save(out2)
    print("saved:", out2)


if __name__ == "__main__":
    # v3.0 版本：课时40分钟制（2课时=80分钟；v1.0/v2.0文件保留）
    build_course(
        data_ai,
        "工业互联网应用专业《AI应用基础》授课计划表v4.0.docx",
        "LS3.2工业智能应用AI系统开发教学方案（第4-11周）v4.0.docx",
    )
    build_course(
        data_py,
        "工业互联网应用专业《Python编程基础》授课计划表v3.0.docx",
        "LS3.1工业数据采集与处理程序开发教学方案（第1-12周）v3.0.docx",
    )
    build_course(
        data_pp,
        "工业互联网应用专业《Python程序设计（项目实战）》授课计划表v3.0.docx",
        "LS3.3工业互联网数据工程教学方案（第1-8周）v3.0.docx",
    )

