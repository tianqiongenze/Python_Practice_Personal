# VS Code 使用指南（课程版·备选）

![VSCode界面与五步](图/vscode.png)

> ⚠️ **本课程主用 PyCharm CE + Jupyter，VS Code 仅作备选**（42号轮起编辑器已迁移到 PyCharm CE）
> 统一用 conda 环境管理，不再使用 venv

## 一、它是什么

微软开源轻量编辑器：装上Python扩展≈小型IDE；**三课程备选编辑器**（主推 PyCharm CE）。

## 二、五步上手
1. code.visualstudio.com 下载安装；
2. 扩展(Ctrl+Shift+X)：装 Chinese(中文) + Python(ms-python)；
3. 文件→打开文件夹→选课程包；
4. 终端(Ctrl+`)：`conda activate 课程环境名`（如`py02`/`pp03`/`ai48`）激活环境→选解释器：Ctrl+Shift+P→Python: Select Interpreter→选 conda 环境；
5. 打开任一.py→右上▶运行。

## 三、高频快捷键
| 键 | 功能 |
|----|------|
| Ctrl+` | 开关终端 |
| Ctrl+P | 快速打开文件 |
| Ctrl+Shift+P | 命令面板 |
| Alt+↑/↓ | 整行上下移 |
| Ctrl+/ | 注释切换 |

## 四、Jupyter扩展
装Python扩展后直接点开.ipynb即可运行（等同Notebook）。

## 五、常见问题
- 运行用了系统Python：Ctrl+Shift+P→Select Interpreter→选 conda 环境（如`py02`）；
- 终端中文乱码：设置搜 terminal.integrated.profiles 按系统配置；
- Pylance报一堆波浪线：先跑一遍代码，真错误看终端。
