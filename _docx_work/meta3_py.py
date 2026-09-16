# -*- coding: utf-8 -*-
"""PY课细化数据(12周)：每课基础6条/技能4条/ABCD/代码片段/常见错误"""

PY3 = {
1: dict(
    basics=["变量=给值贴标签；动态类型随值走——应用：dev_code='PUMP-03'; temp=78.5; print(type(temp))→<class 'float'>，同一变量可随时换类型",
            "四种基本类型：int/float/str/bool",
            "type()查看类型；int('36')显式转换——应用：isinstance(temp,float)做类型守卫防传入字符串温度",
            "f-string格式化：f\"温度{t:.1f}℃\"",
            "单位换算公式：F=C*9/5+32；MPa=kPa/1000",
            "PEP 8启蒙：snake_case命名+4空格缩进"],
    skills=["安装Python与PyCharm CE并运行首程序——应用：见工单starter与教师参考实现",
            "定义多类型变量并格式化输出台账卡——应用：见工单starter与教师参考实现",
            "完成单位换算并保留小数——应用：见工单starter与教师参考实现",
            "按规范命名并添加关键注释——应用：见工单starter与教师参考实现"],
    abcd={
        "A": dict(goal="输入校验+多行台账", std="8变量4类型+校验",
                 steps=["input录入并校验范围", "循环输出多设备台账卡", "加单位换算双项"]),
        "B": dict(goal="完整台账卡", std="8变量+2处换算",
                 steps=["定义8个变量覆盖4类型", "f-string对齐输出", "完成℃→℉与kPa→MPa"]),
        "C": dict(goal="基础台账", std="6变量3类型",
                 steps=["定义6个变量", "print逐项输出", "完成1处换算"]),
        "D": dict(goal="首程序仪式", std="Hello World跑通",
                 steps=["运行w01示例", "改一个变量值再跑", "截图打卡"])},
    code=[("台账卡输出",
"""device_id = "DEV-2026-001"; name = "智能注塑机"
temp = 56.5; press_kpa = 450.0
print(f"编号:{device_id}\\n名称:{name}")
print(f"温度:{temp:.1f}℃ ({temp*9/5+32:.1f}℉)")
print(f"压力:{press_kpa/1000:.2f}MPa")""")],
    errors=[("SyntaxError", "中文标点/冒号", "全用英文标点"),
             ("NameError", "拼写不一致", "搜索变量名核对大小写"),
             ("f-string原样输出", "少了f前缀", "加f前缀")]),
2: dict(
    basics=["if/elif/else分支；缩进即语法——应用：见工单starter与教师参考实现",
            "比较运算==/!=/>=/<=；=是赋值——应用：见工单starter与教师参考实现",
            "and/or/not组合条件(加括号)——应用：if temp>=80 and vib>4.5: 报警——两个条件同时满足才触发",
            "嵌套判断：先危险后预警的顺序——应用：先if level=='alarm'再if device=='PUMP'——先筛高危再定位设备",
            "边界值：79.9/80/80.1三测法——应用：见工单starter与教师参考实现",
            "告警分级：提示/警告/停机三级——应用：见工单starter与教师参考实现"],
    skills=["编写多级阈值判断逻辑——应用：见工单starter与教师参考实现",
            "设计alarm告警函数——应用：见工单starter与教师参考实现",
            "边界五组全覆盖测试——应用：见工单starter与教师参考实现",
            "用流程图先行梳理分支——应用：见工单starter与教师参考实现"],
    abcd={
        "A": dict(goal="三级告警+去重", std="边界全对+日志",
                 steps=["温度压力同时超限升紧急", "同设备同级10秒去重", "告警写alarm.log"]),
        "B": dict(goal="两级判断完整", std="边界五组通过",
                 steps=["80/95双阈值判断", "alarm函数封装", "五组边界测试输出"]),
        "C": dict(goal="单级判断", std="两组边界通过",
                 steps=["温度≥80判断", "输出告警信息", "测试79.9/80"]),
        "D": dict(goal="跟做改值", std="能改阈值再跑",
                 steps=["运行示例", "把80改成75", "观察输出变化"])},
    code=[("两级判断",
"""if temp >= 95:
    alarm(3, f"温度{temp}℃超危险线，停机！")
elif temp >= 80:
    alarm(2, f"温度{temp}℃超预警线")
else:
    alarm(1, "运行正常")""",
           )],
    errors=[("95分支永不执行", "elif顺序反了", "先判危险再预警"),
             ("=用在条件里", "语法错误", "改=="),
             ("边界80落错分支", "用了>而非>=", "按需求选>=/>")]),
3: dict(
    basics=["for+range遍历；while满足条件循环——应用：见工单starter与教师参考实现",
            "break跳出一层/continue跳过本轮——应用：见工单starter与教师参考实现",
            "循环三要素：初始化/条件/更新——应用：for i in range(10):读设备[i]——初始化i/条件i<10/更新i+=1三件缺一不可",
            "random.uniform(a,b)随机浮点；seed固定",
            "函数：def+参数+return；作用域隔离——应用：见工单starter与教师参考实现",
            "列表存设备序列、字典存键值属性——应用：devs=['PUMP-03','FAN-02']; devs.append('MOTOR-01')——动态扩容无需预声明大小"],
    skills=["双层循环模拟多设备多周期——应用：见工单starter与教师参考实现",
            "封装check_device/alarm两函数——应用：见工单starter与教师参考实现",
            "统计各设备各级告警次数——应用：见工单starter与教师参考实现",
            "固定seed保证结果可复现——应用：见工单starter与教师参考实现"],
    abcd={
        "A": dict(goal="防抖动+while版", std="统计准确+无死循环",
                 steps=["连续3次≥95才停机", "while版持续监测", "重构对比说明收益"]),
        "B": dict(goal="循环+统计完整", std="报告正确",
                 steps=["3设备×10周期循环", "两函数封装", "告警统计报告"]),
        "C": dict(goal="单循环跑通", std="能出10轮结果",
                 steps=["一设备10周期", "调用check函数", "打印每轮状态"]),
        "D": dict(goal="跟做循环", std="能改周期数",
                 steps=["运行示例", "range(10)改5", "看输出减半"])},
    code=[("双层循环+统计",
"""stats = {d["id"]: {2:0, 3:0} for d in devices}
for d in devices:
    for _ in range(10):
        t = d["base"] + random.uniform(-8, 15)
        lv = check_device(d, t)
        if lv: stats[d["id"]][lv] += 1; alarm(d, lv, t)""",
           )],
    errors=[("死循环", "while条件永真", "补更新语句+Ctrl+C"),
             ("KeyError", "统计键未初始化", "先建{2:0,3:0}"),
             ("函数内改不了外面变量", "作用域", "用return传值")]),
4: dict(
    basics=["类=图纸；实例=按图纸造的产品——应用：见工单starter与教师参考实现",
            "__init__构造方法；self=实例自身——应用：见工单starter与教师参考实现",
            "实例属性写__init__内(独立内存)——应用：见工单starter与教师参考实现",
            "方法=类内函数；d.start()即调用——应用：见工单starter与教师参考实现",
            "__str__让print(对象)可读——应用：见工单starter与教师参考实现",
            "状态校验：非法迁移要拒绝——应用：见工单starter与教师参考实现"],
    skills=["设计Device类(属性+方法)——应用：见工单starter与教师参考实现",
            "创建多实例并演示属性隔离——应用：见工单starter与教师参考实现",
            "实现启停状态校验逻辑——应用：见工单starter与教师参考实现",
            "用id()观察对象独立性——应用：见工单starter与教师参考实现"],
    abcd={
        "A": dict(goal="__str__+运行时长", std="3属性3方法+docstring",
                 steps=["实现__str__", "start/stop时间差统计", "输出设备报表"]),
        "B": dict(goal="标准设备类", std="2属性2方法2实例",
                 steps=["完成Device类", "创建2实例调用", "get_status输出"]),
        "C": dict(goal="最小类", std="1属性1方法",
                 steps=["补全__init__", "实现start", "创建1实例调用"]),
        "D": dict(goal="对象体验", std="能调用方法",
                 steps=["运行示例", "再建一个对象", "观察互不影响"])},
    code=[("设备类骨架",
"""class Device:
    def __init__(self, dev_id, name, temp=25.0):
        self.dev_id, self.name, self.temp = dev_id, name, temp
        self.status = "停止"
    def start(self):
        if self.status == "运行":
            print(f"{self.name}已在运行"); return
        self.status = "运行"; print(f"{self.name}启动成功")""",
           )],
    errors=[("漏self", "调用报参数多一个", "方法第一参数写self"),
             ("属性被共享", "属性写在类体", "移入__init__"),
             ("d.start无输出", "少了括号", "d.start()才调用")]),
5: dict(
    basics=["继承：子类复用父类成员(is-a关系)——应用：见工单starter与教师参考实现",
            "super().__init__()先完成父类初始化",
            "覆盖：子类同名方法优先执行——应用：见工单starter与教师参考实现",
            "多态：统一接口、不同行为——应用：见工单starter与教师参考实现",
            "isinstance/issubclass类型判断",
            "docstring：类与方法一行说明——应用：见工单starter与教师参考实现"],
    skills=["构建基类+两子类继承体系——应用：见工单starter与教师参考实现",
            "覆盖start并调用super协作——应用：见工单starter与教师参考实现",
            "循环统一调用演示多态——应用：见工单starter与教师参考实现",
            "绘制继承体系类图——应用：见工单starter与教师参考实现"],
    abcd={
        "A": dict(goal="三子类+类图", std="多态清晰+is-a判断",
                 steps=["加Sensor子类calibrate", "总控台统一启停", "类图绘制"]),
        "B": dict(goal="两子类覆盖", std="docstring齐全",
                 steps=["PLC子类+scan_ms", "覆盖start带扫描周期", "循环调用看多态"]),
        "C": dict(goal="单子类继承", std="继承与super正确",
                 steps=["PLC继承Device", "super().__init__", "新增一个属性"]),
        "D": dict(goal="继承体验", std="能复述is-a",
                 steps=["运行多态示例", "换一种设备再跑", "口述谁继承谁"])},
    code=[("继承+覆盖",
"""class PLC(Device):
    def __init__(self, dev_id, name, scan_ms=10):
        super().__init__(dev_id, name)   # 父类先初始化!
        self.scan_ms = scan_ms
    def start(self):                     # 覆盖
        super().start()
        print(f"  扫描周期:{self.scan_ms}ms")""",
           )],
    errors=[("父类属性丢失", "忘调super().__init__", "补上super调用"),
             ("多态失效", "方法名大小写不一致", "与父类完全同名"),
             ("为继承而继承", "车间不是设备", "is-a不成立就不继承")]),
6: dict(
    basics=["异常=运行时错误对象；类型即线索——应用：见工单starter与教师参考实现",
            "try/except/else/finally四段结构",
            "精确捕获：FileNotFoundError/ValueError",
            "禁止裸except(吞Ctrl+C)——应用：见工单starter与教师参考实现",
            "logging三级：INFO/WARNING/ERROR",
            "finally放收尾：关资源/写统计——应用：见工单starter与教师参考实现"],
    skills=["配置双输出日志(控制台+文件)——应用：见工单starter与教师参考实现",
            "捕获多类型异常并分级记录——应用：见工单starter与教师参考实现",
            "输出采集统计(成功/跳过/失败)——应用：见工单starter与教师参考实现",
            "脏数据写入bad_records备查——应用：见工单starter与教师参考实现"],
    abcd={
        "A": dict(goal="断点续采+bad_records", std="3异常+可定位日志",
                 steps=["脏数据写csv备查", "异常后从断点继续", "日志带行号定位"]),
        "B": dict(goal="完整健壮程序", std="3异常+finally",
                 steps=["日志双输出配置", "try/except/finally完整", "统计输出"]),
        "C": dict(goal="基础捕获", std="2异常+基本日志",
                 steps=["捕获文件缺失", "捕获转换错误", "WARNING记录跳过"]),
        "D": dict(goal="故障注入体验", std="能读日志定位",
                 steps=["删数据文件触发异常", "看日志ERROR行", "恢复文件再跑"])},
    code=[("健壮读取",
"""try:
    t, p = line.split(","); float(t); float(p)
    log.info("第%d条成功:%s", i, line); ok += 1
except ValueError:
    log.warning("脏数据跳过:%r", line); skip += 1
finally:
    pass                       # 收尾:写统计/关资源""",
           )],
    errors=[("裸except吞异常", "连Ctrl+C都拦", "写明异常类型"),
             ("日志中文乱码", "编码缺省", "FileHandler(encoding='utf-8')"),
             ("except里pass", "错误被掩盖", "至少log.error记录")]),
7: dict(
    basics=["列表有序可重复；字典键值O(1)查——应用：见工单starter与教师参考实现",
            "集合自动去重；元组不可变——应用：见工单starter与教师参考实现",
            "正则八积木：\\d \\w + * [] ()",
            "re.match/findall/search三方法",
            "r前缀防转义：r'DEV-\\d+'",
            "统一schema：多源输入→标准字典——应用：见工单starter与教师参考实现"],
    skills=["正则解析报文键值对——应用：见工单starter与教师参考实现",
            "CSV/JSON双格式解析——应用：见工单starter与教师参考实现",
            "三格式统一映射标准结构——应用：见工单starter与教师参考实现",
            "按决策矩阵完成容器选型——应用：见工单starter与教师参考实现"],
    abcd={
        "A": dict(goal="容错解析器+批量", std="3格式+成功率统计",
                 steps=["缺字段置None容错", "批量转换文件", "输出成功率统计"]),
        "B": dict(goal="三格式全通", std="结构统一无错",
                 steps=["报文正则解析", "CSV/JSON解析", "统一{device_id,metrics}"]),
        "C": dict(goal="双格式解析", std="能出标准字典",
                 steps=["报文解析", "JSON解析", "打印对照"]),
        "D": dict(goal="正则体验", std="能改模式匹配",
                 steps=["运行示例", "\\d+改\\d{2}", "观察匹配变化"])},
    code=[("报文正则解析",
"""import re
msg = "DEV-01:temp=56.3C;press=0.45MPa;status=RUN"
dev = re.match(r"([A-Z]+-\\d+):", msg).group(1)
kv = re.findall(r"(\\w+)=([\\d.]+|\\w+)", msg)
metrics = {k: float(v) if re.fullmatch(r"[\\d.]+", v) else v
           for k, v in kv}""",
           )],
    errors=[("正则把整行吞了", "贪婪.*", "用[\\d.]+限定"),
             ("键名带空格", "没strip", "切分后strip()"),
             ("str当float用", "忘了转换", "数值字段float()")]),
8: dict(
    basics=["with open自动关闭；encoding='utf-8'防乱码",
            "csv.DictReader按表头取列——应用：见工单starter与教师参考实现",
            "json.loads/dumps解析与序列化——应用：见工单starter与教师参考实现",
            "三维验证：缺失/类型/范围——应用：见工单starter与教师参考实现",
            "问题行策略：跳过+记录可追溯——应用：见工单starter与教师参考实现",
            "newline=''防CSV空行——应用：见工单starter与教师参考实现"],
    skills=["with读写CSV与JSON——应用：见工单starter与教师参考实现",
            "实现三维数据验证——应用：见工单starter与教师参考实现",
            "bad_records错误留痕——应用：见工单starter与教师参考实现",
            "输出清洗报告与标准化数据——应用：见工单starter与教师参考实现"],
    abcd={
        "A": dict(goal="体检脚本+参数化", std="三维统计报表",
                 steps=["缺失/类型/范围统计脚本", "--input参数支持", "135℃业务决策记录"]),
        "B": dict(goal="完整清洗管线", std="报告+bad_records",
                 steps=["读取CSV三维验证", "问题行写bad_records.csv", "输出清洗报告"]),
        "C": dict(goal="基础清洗", std="能出clean.csv",
                 steps=["读取CSV", "过滤空值行", "输出clean.csv"]),
        "D": dict(goal="脏数据观察", std="能数出问题行",
                 steps=["--peek预览", "找3个问题行", "口述维度归类"])},
    code=[("三维验证",
"""def validate(row):
    t = row["temp"]
    if t in ("", None): return "缺失"
    try: t = float(t)
    except ValueError: return "类型"
    return None if 0 <= t <= 120 else "范围\"""",
           )],
    errors=[("float('err')崩", "未预判", "try转换或errors处理"),
             ("CSV多空行", "缺newline=''", "open(...,newline='')"),
             ("路径找不到", "IDE与命令行cwd不同", "按脚本目录拼路径")]),
9: dict(
    basics=["pip安装与离线whl安装——应用：见工单starter与教师参考实现",
            "jieba.cut精确分词——应用：见工单starter与教师参考实现",
            "停用词过滤提升信噪比——应用：见工单starter与教师参考实现",
            "Counter词频统计most_common——应用：见工单starter与教师参考实现",
            "TF-IDF关键词：专属词升权——应用：见工单starter与教师参考实现",
            "wordcloud需font_path指定中文字体"],
    skills=["完成分词+停用词管线——应用：见工单starter与教师参考实现",
            "生成词云与Top10柱状图——应用：见工单starter与教师参考实现",
            "extract_tags提取关键词——应用：见工单starter与教师参考实现",
            "撰写数据支撑的故障洞察——应用：见工单starter与教师参考实现"],
    abcd={
        "A": dict(goal="分组对比词云", std="洞察有数字支撑",
                 steps=["按系统分组两朵词云", "对比Top词差异", "150字洞察结论"]),
        "B": dict(goal="词云+词频+关键词", std="三件产出齐全",
                 steps=["分词停用词管线", "词云+柱状图", "extract_tags Top20"]),
        "C": dict(goal="词云生成", std="能出cloud.png",
                 steps=["jieba分词", "Counter统计", "wordcloud出图"]),
        "D": dict(goal="分词观察", std="能读Top10",
                 steps=["运行分词示例", "加停用词再跑", "对比两次Top词"])},
    code=[("词云核心",
"""words = [w for t in texts for w in jieba.cut(t)
         if w not in STOP and len(w) > 1]
from wordcloud import WordCloud
wc = WordCloud(font_path="../教学实施资料/fonts/SourceHanSansCN-Regular.otf", width=800,
               height=400, background_color="white")
wc.generate(" ".join(words)); wc.to_file("cloud.png")""",
           )],
    errors=[("中文变方块", "没指定字体", "font_path必填"),
             ("Top10全是虚词", "停用词未滤", "扩STOP表"),
             ("frequencies用错", "传参类型错", "generate吃文本串")]),
10: dict(
    basics=["Pillow：open/copy/resize/draw",
            "rectangle画框[x1,y1,x2,y2]——应用：见工单starter与教师参考实现",
            "reportlab三件：Paragraph/Image/Table",
            "中文字体注册TTFont后setFont——应用：见工单starter与教师参考实现",
            "四段式日报：概览/分析/异常/附表——应用：见工单starter与教师参考实现",
            "信息层级：结论先行——应用：见工单starter与教师参考实现"],
    skills=["图像缩放与缺陷框标注——应用：见工单starter与教师参考实现",
            "PDF图文表混排生成——应用：见工单starter与教师参考实现",
            "中文字体注册与使用——应用：见工单starter与教师参考实现",
            "按读者视角组织报告层级——应用：见工单starter与教师参考实现"],
    abcd={
        "A": dict(goal="封面+多页报告", std="可直接上交水准",
                 steps=["自绘封面页", "概览+明细双页", "耗时<2min记录"]),
        "B": dict(goal="图文表三要素", std="排版规范",
                 steps=["标注缺陷图", "PDF标题+结论+图+表", "生成并检查"]),
        "C": dict(goal="图+PDF", std="PDF能打开",
                 steps=["画框标注", "最简PDF输出", "确认中文正常"]),
        "D": dict(goal="标注体验", std="能改框位置",
                 steps=["运行示例", "改坐标再画", "观察标注变化"])},
    code=[("标注+PDF",
"""d = ImageDraw.Draw(img.copy())
d.rectangle([120,80,210,120], outline=(255,0,0), width=3)
d.text((120,66), "scratch 9.0mm", fill=(255,0,0))
pdfmetrics.registerFont(TTFont("ZH", "fonts/ZH_Font.ttf"))
doc.build([Paragraph("设备质量日报", st),
           RLImage("marked.png", width=120*mm, height=90*mm)])""",
           )],
    errors=[("PDF中文空白", "字体未注册", "registerFont+setFont"),
             ("文字压住框", "y坐标不当", "画在框上方y-14"),
             ("图变形", "宽高没等比", "按原始比例设宽高")]),
11: dict(
    basics=["Modbus寄存器：40001-40005五测点——应用：见工单starter与教师参考实现",
            "数值×10定点存储：678=67.8℃——应用：见工单starter与教师参考实现",
            "pymodbus：read_holding_registers",
            "MQTT主题：device/1/status路由——应用：见工单starter与教师参考实现",
            "JSON消息含ts时间戳——应用：见工单starter与教师参考实现",
            "排错三步：ping通→端口通→代码通——应用：见工单starter与教师参考实现"],
    skills=["连接虚拟PLC读取寄存器——应用：见工单starter与教师参考实现",
            "paho-mqtt发布JSON消息——应用：见工单starter与教师参考实现",
            "异常重试与日志记录——应用：见工单starter与教师参考实现",
            "订阅回环验证消息到达——应用：见工单starter与教师参考实现"],
    abcd={
        "A": dict(goal="回环验证+重连", std="规范率≥90%",
                 steps=["订阅自己主题打印回执", "断线重试逻辑", "消息结构优化"]),
        "B": dict(goal="五轮采集上报", std="JSON结构规范",
                 steps=["读5寄存器÷10还原", "5轮循环采集", "MQTT发布JSON"]),
        "C": dict(goal="单次采集", std="能读出数值",
                 steps=["连PLC读一次", "打印还原值", "单条MQTT发布"]),
        "D": dict(goal="模拟器体验", std="能改端口",
                 steps=["--check连通", "换5021再读", "记录两台数据"])},
    code=[("采集+上报",
"""rr = c.read_holding_registers(address=0, count=5)
vals = rr.registers
data = {n: v/10 for n, v in zip(NAMES[:4], vals[:4])}
payload = json.dumps({"device_id":"DEV-1",
    "ts": time.strftime("%H:%M:%S"), "metrics":data},
    ensure_ascii=False)
mq.publish("device/1/status", payload)""",
           )],
    errors=[("连不上PLC", "模拟器没启动", "先跑虚拟产线--check"),
             ("数值大10倍", "忘了÷10", "寄存器定点换算"),
             ("publish后无消息", "立刻退出", "sleep 0.3再退")]),
12: dict(
    basics=["checklist三清单：功能/规范/演示——应用：见工单starter与教师参考实现",
            "答辩结构：1分工+5演示+2总结——应用：见工单starter与教师参考实现",
            "bad-case预案：评委必点脏数据——应用：见工单starter与教师参考实现",
            "贡献表与Git交叉核对——应用：见工单starter与教师参考实现",
            "每人必答1题(个人问责)——应用：见工单starter与教师参考实现",
            ">6组切换5+3分钟制——应用：见工单starter与教师参考实现"],
    skills=["按checklist完成终验自查——应用：见工单starter与教师参考实现",
            "组内预答辩互问热身——应用：见工单starter与教师参考实现",
            "限时演示与规范表达——应用：见工单starter与教师参考实现",
            "提交物齐套打包——应用：见工单starter与教师参考实现"],
    abcd={
        "A": dict(goal="脱稿架构讲解", std="2分钟讲清",
                 steps=["画架构图脱稿讲", "bad-case演示准备", "创新点陈述"]),
        "B": dict(goal="答辩主力", std="答问准确",
                 steps=["8分钟演示彩排", "必答题准备", "分工说明"]),
        "C": dict(goal="模块讲解", std="讲清自己模块",
                 steps=["负责模块演示", "答1个模块问题", "过程记录提交"]),
        "D": dict(goal="参与汇报", std="能答基础问题",
                 steps=["说清自己做了什么", "回答1基础题", "反思一页纸"])},
    code=[("项目骨架(四类分工)",
"""class Collector:      # A: 采集(Modbus/文件)
    def collect(self): ...
class Cleaner:        # B: 清洗(三维验证)
    def clean(self, rows): ...
class Analyzer:       # C: 分析(阈值+统计)
    def analyze(self, rows): ...
class Reporter:       # D: 文档(PDF报告)
    def build(self, stats): ...""",
           )],
    errors=[("现场装依赖", "没提前试跑", "答辩机预演"),
             ("只讲不演示", "空谈", "必须现场运行"),
             ("超时", "没掐表", "按5+3彩排两遍")]),
}
