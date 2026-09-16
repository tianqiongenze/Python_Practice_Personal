# -*- coding: utf-8 -*-
"""每门课每周的"主用工具"标识（供工单/PPT/任务书统一注入；与各包《课程软件与环境配置完全指南》零节地图同源）"""

# 通用指南文件名（供跳转）——51号轮：VS Code指南已归档（编辑器统一PyCharm CE+Jupyter）
GUIDE = {
    "jupyter": "02-Jupyter Notebook使用指南.md",
    "anaconda": "01-Anaconda安装与使用指南.md",
    "git": "03-Git与GitHub-Gitee使用指南.md",
    "processon": "04-ProcessOn绘图指南.md",
    "pycharm": "05-PyCharm使用指南.md",
}


def tool_for(code, week):
    """返回 (主用工具短语, 指南文件名列表)
    所有课程第1周/开课周起即使用Git+GitHub/Gitee每周提交（48号轮：从选做升级为必用）
    """
    if code == "ai":
        return "Jupyter（实训/演示）+ PyCharm CE（编码）+ Git/GitHub（每周提交）", [GUIDE["jupyter"], GUIDE["pycharm"], GUIDE["git"]]
    if code == "py":
        if week >= 8:
            return "PyCharm CE（编码）+ Jupyter（Pandas数据实验）+ Git/GitHub（每周提交）", [GUIDE["pycharm"], GUIDE["jupyter"], GUIDE["git"]]
        return "PyCharm CE（全程主编辑器）+ Jupyter（每周notebook）+ Git/GitHub（每周提交）", [GUIDE["pycharm"], GUIDE["jupyter"], GUIDE["git"]]
    if code == "pp":
        if week == 2:
            return "PyCharm CE + Git/GitHub（工程模板核心·五步工作流）", [GUIDE["pycharm"], GUIDE["git"]]
        if week == 7:
            return "PyCharm CE + ProcessOn（ER图设计）+ Git/GitHub（每周提交）", [GUIDE["pycharm"], GUIDE["processon"], GUIDE["git"]]
        if week >= 3 and week <= 4:
            return "PyCharm CE（编码）+ Jupyter（Pandas/NumPy数据探索）+ Git/GitHub（每周提交）", [GUIDE["pycharm"], GUIDE["jupyter"], GUIDE["git"]]
        return "PyCharm CE + conda环境(pp03) + Git/GitHub（每周提交）", [GUIDE["pycharm"], GUIDE["git"]]
    if code == "ai48":
        if week == 9:  # 第9学期周=课程第6周M2-3b分组竞标
            return "Jupyter（全程实训）+ PyCharm CE + ProcessOn（竞标书）+ Git/GitHub（每周提交）", [GUIDE["jupyter"], GUIDE["processon"], GUIDE["git"]]
        return "Jupyter（全程实训）+ PyCharm CE（starter编码）+ Git/GitHub（每周提交）", [GUIDE["jupyter"], GUIDE["pycharm"], GUIDE["git"]]
    return "", []
