# -*- coding: utf-8 -*-
"""PP课细化数据(8周)"""

PP3 = {
1: dict(
    basics=["C→Python映射：声明→动态/大括号→缩进/指针→引用",
            "引用语义：b=a后改b会动a(列表不拷贝)——应用：import copy; b=copy.deepcopy(a)——浅拷贝改b动a，深拷贝才安全",
            "列表append动态扩容；字典O(1)查找——应用：buffer.append(row); len(buffer)>=1000时批量写库——无需预分配",
            "try/except替代错误码层层上抛——应用：try:conn=connect() except TimeoutError as e:log(e);retry()——异常分层捕获不丢栈",
            "类=struct+函数指针的升级——应用：class Device: code=''; def start(self):...——数据+行为打包，比C的struct+函数指针更安全",
            "缩进统一4空格禁Tab混用——应用：见工单starter与教师参考实现"],
    skills=["双栏对照法完成语法迁移——应用：见工单starter与教师参考实现",
            "五题渐进练习全通过pytest断言——应用：见工单starter与教师参考实现",
            "异常保护文件读取——应用：见工单starter与教师参考实现",
            "编写C→Python迁移笔记——应用：见工单starter与教师参考实现"],
    abcd={
        "A": dict(goal="五题+测试用例+讲解", std="PEP8≥85%+笔记10条",
                 steps=["每题附3边界断言", "pytest全绿", "挑1条向全班讲解"]),
        "B": dict(goal="五题全对", std="PEP8≥85%",
                 steps=["完成题1-5", "过内置断言", "命名规范检查"]),
        "C": dict(goal="三题保底", std="题1-3正确",
                 steps=["换算器+方程+字典管理", "断言通过", "注释补全"]),
        "D": dict(goal="两题跟做", std="能运行出结果",
                 steps=["跟做题1/2", "改参数再跑", "记录一处差异"])},
    code=[("引用vs拷贝(C人必踩)",
"""a = [1, 2, 3]
b = a              # 引用!类似指针
b.append(4)        # a也变了
c = list(a)        # 真拷贝""",
           ),
          ("异常读取",
"""try:
    with open(path, encoding="utf-8") as f:
        return f.read()
except FileNotFoundError:
    return "FILE_NOT_FOUND\"""")],
    errors=[("b改a也变", "引用语义", "list(a)或a.copy()"),
             ("混用Tab", "跨编辑器报错", "统一4空格"),
             ("=当==", "条件失效", "比较用==")]),
2: dict(
    basics=["标准结构：src/tests/config/data/docs",
            "venv沙箱隔离；requirements.txt冻结",
            "Git五步：init/add/commit/branch/merge",
            "commit前缀：feat:/fix:/docs:",
            "pylint评分≥8.5；black格式化——应用：见工单starter与教师参考实现",
            "pytest自动发现test_函数——应用：def test_clean():assert...——文件名test_开头函数自动被pytest收集运行"],
    skills=["生成标准工程模板并推Git——应用：见工单starter与教师参考实现",
            "dev分支开发与规范合并——应用：见工单starter与教师参考实现",
            "配置检查工具与自动格式化——应用：见工单starter与教师参考实现",
            "编写第一个单元测试——应用：见工单starter与教师参考实现"],
    abcd={
        "A": dict(goal="CI/pre-commit", std="Actions绿钩",
                 steps=["GitHub Actions配置", "pre-commit钩子", "pylint 9+截图"]),
        "B": dict(goal="模板+工具链", std="pylint≥8.5+pytest过",
                 steps=["运行p12模板生成器", "flake8+black配置", "为题1写3断言"]),
        "C": dict(goal="基础模板", std="结构完整可运行",
                 steps=["生成模板目录", "git init+首次commit", "跑通main.py"]),
        "D": dict(goal="Git四关", std="init到merge走通",
                 steps=["闯关练习四关", "每步截图", "commit带说明"])},
    code=[("规范提交",
"""git checkout -b dev
git add src/
git commit -m "feat: 完成数据采集模块"
git checkout main && git merge dev""",
           )],
    errors=[("venv被提交", ".gitignore缺", "加venv/与__pycache__/"),
             ("全局py环境混乱", "没激活venv", "看终端前缀(venv)"),
             ("一次commit全部", "无说明", "小步提交带前缀")]),
3: dict(
    basics=["DataFrame二维表；shape/info/describe摸底",
            "dropna/fillna/interpolate三策略",
            "to_datetime(errors=coerce)多格式统一",
            "combine_first填补有效值——应用：df['vib'].combine_first(df['vib_backup'])——主列空用备列填，两列都不空取主",
            "IQR=Q3-Q1；1.5倍护栏——应用：q1,q3=df.vib.quantile([.25,.75]); fence=q3+1.5*(q3-q1); outliers=df[df.vib>fence]——比3σ对异常值更稳健",
            "业务阈值与统计法AND——应用：见工单starter与教师参考实现",
            "清洗顺序：类型→缺失→异常→去重——应用：见工单starter与教师参考实现"],
    skills=["七步管道构建与质量自测——应用：见工单starter与教师参考实现",
            "三格式时间戳统一——应用：见工单starter与教师参考实现",
            "IQR×业务阈值异常处理——应用：见工单starter与教师参考实现",
            "决策矩阵驱动策略选择——应用：见工单starter与教师参考实现"],
    abcd={
        "A": dict(goal="增量处理+质量90+", std="处理日志全留痕",
                 steps=["只清洗新增行", "质量冲90", "日志记录每步行数"]),
        "B": dict(goal="完整管道", std="质量≥88%",
                 steps=["类型转换+时间统一", "插值+IQR处理", "去重输出clean.csv"]),
        "C": dict(goal="基础清洗", std="质量≥85%",
                 steps=["to_numeric转NaN", "dropna简单处理", "输出评分"]),
        "D": dict(goal="--peek观察", std="能数出问题类型",
                 steps=["预览数据", "数缺失/类型错各几个", "记录到工单"])},
    code=[("三格式时间统一",
"""parts = [pd.to_datetime(df.ts, format=f, errors="coerce")
         for f in ("%Y-%m-%d %H:%M:%S", "%m/%d/%Y %H:%M",
                   "%Y%m%d%H%M%S")]
ts = parts[0]
for p in parts[1:]:
    ts = ts.combine_first(p)      # 依次填补
df["ts"] = ts""",
           ),
          ("IQR×业务",
"""q1, q3 = df.temp.quantile([.25, .75]); iqr = q3 - q1
mask = (df.temp < q1-1.5*iqr) | (df.temp > q3+1.5*iqr) | (df.temp > 120)
df = df[~mask]""")],
    errors=[("链式赋值警告", "视图上赋值", "用.loc或先copy()"),
             ("统计量被污染", "异常值前先归一化", "先清洗后缩放"),
             ("评分上不去", "时间列没转datetime", "统一格式后重评")]),
4: dict(
    basics=["ndarray同构多维数组；shape/dtype",
            "向量化：C级循环替代Python层for——应用：见工单starter与教师参考实现",
            "广播：形状对齐自动扩展——应用：见工单starter与教师参考实现",
            "rfft单边谱；幅值×2/n补偿——应用：见工单starter与教师参考实现",
            "主频=谱峰位置(频域指纹)——应用：见工单starter与教师参考实现",
            "峭度/偏度刻画冲击/偏斜——应用：见工单starter与教师参考实现",
            "标准化只fit训练集——应用：见工单starter与教师参考实现"],
    skills=["特征字典驱动补齐30维特征——应用：见工单starter与教师参考实现",
            "FFT频域特征计算——应用：见工单starter与教师参考实现",
            "计时基准测试(<100ms)——应用：见工单starter与教师参考实现",
            "箱线图可视化类别区分度——应用：见工单starter与教师参考实现"],
    abcd={
        "A": dict(goal="相关去冗余+性能", std="<50ms+字典完整",
                 steps=["相关矩阵热力图", "去|r|>0.95特征", "性能优化对比"]),
        "B": dict(goal="30维全实现", std="<100ms+向量化",
                 steps=["补时域10个", "补频域15个(FFT)", "标准化+箱线图"]),
        "C": dict(goal="15维保底", std="时域正确",
                 steps=["5示例+补10时域", "spectrum()单边谱", "矩阵形状断言"]),
        "D": dict(goal="示例研读", std="能讲5个示例含义",
                 steps=["跑通5示例特征", "改一个公式看数值", "抄写特征字典"])},
    code=[("FFT特征",
"""def spectrum(x, fs=100):
    amp = np.abs(np.fft.rfft(x)) * 2 / len(x)   # 单边+补偿
    return np.fft.rfftfreq(len(x), 1/fs), amp
freqs, amp = spectrum(sig)
dom_freq = freqs[amp.argmax()]     # 主频率""",
           ),
          ("峭度(冲击敏感)",
"""def kurtosis(x):
    return ((x-x.mean())**4).mean() / x.std()**4 - 3""")],
    errors=[("频域能量翻倍", "忘×2/n或没取单边", "rfft+补偿"),
             ("100ms超标", "用了apply/循环", "纯向量化重写"),
             ("公式口径混", "峭度定义版本不一", "字典里注明公式")]),
5: dict(
    basics=["Streamlit脚本式交互；sidebar筛选——应用：见工单starter与教师参考实现",
            "@st.cache_data缓存重计算——应用：见工单starter与教师参考实现",
            "st.metric指标卡(KPI)——应用：见工单starter与教师参考实现",
            "Plotly交互图表嵌入——应用：见工单starter与教师参考实现",
            "Jinja2模板{{变量}}渲染——应用：见工单starter与教师参考实现",
            "四段式日报结构——应用：见工单starter与教师参考实现"],
    skills=["搭建5+KPI仪表盘——应用：见工单starter与教师参考实现",
            "时间/设备联动筛选——应用：见工单starter与教师参考实现",
            "HTML+PDF双格式日报——应用：见工单starter与教师参考实现",
            "生成耗时基准(<2min)——应用：见工单starter与教师参考实现"],
    abcd={
        "A": dict(goal="钻取+定时", std="7指标+加载<2s",
                 steps=["点击钻取明细", "schedule定时生成", "移动端适配检查"]),
        "B": dict(goal="仪表盘+日报双交付", std="5KPI+四段PDF",
                 steps=["Streamlit五KPI", "筛选联动+缓存", "Jinja2+PDF日报"]),
        "C": dict(goal="二选一交付", std="仪表盘或日报达基线",
                 steps=["跑通starter", "完成5KPI版仪表", "或HTML日报"]),
        "D": dict(goal="starter跑通", std="页面能开",
                 steps=["streamlit run", "改一个KPI数值", "截图到工单"])},
    code=[("KPI指标卡",
"""c1, c2, c3, c4 = st.columns(4)
c1.metric("总产量", f"{int(df.output.sum()):,}")
c2.metric("平均良率", f"{df['yield'].mean():.1%}")
c3.metric("设备在线", f"{df.device_id.nunique()}/4")""",
           ),
          ("模板渲染",
"""from jinja2 import Template
html = Template(open("report.tpl").read()).render(
    total=total, yield_=y, anomalies=alerts)""")],
    errors=[("交互后变慢", "没缓存", "@st.cache_data"),
             ("Jinja2空白", "变量名不匹配", "对照模板逐个核"),
             ("f-string遇yield", "保留字", "df['yield']取列")]),
6: dict(
    basics=["线程并发；Queue线程安全传送带——应用：见工单starter与教师参考实现",
            "put/get超时防死等——应用：见工单starter与教师参考实现",
            "退避重试1→2→4s封顶——应用：见工单starter与教师参考实现",
            "daemon=True随主退出——应用：见工单starter与教师参考实现",
            "批量写库：50条或5秒flush——应用：见工单starter与教师参考实现",
            "对账：源计数=入库+异常+丢弃——应用：见工单starter与教师参考实现"],
    skills=["三线程骨架贯通(采集/订阅/处理)——应用：见工单starter与教师参考实现",
            "断线重连实测(2号PLC掉线)——应用：见工单starter与教师参考实现",
            "采集率统计与提升——应用：见工单starter与教师参考实现",
            "架构图绘制入工单——应用：见工单starter与教师参考实现"],
    abcd={
        "A": dict(goal="高可用演示", std="≥99.5%+监控",
                 steps=["主备采集切换", "实时统计小面板", "8小时稳定跑"]),
        "B": dict(goal="完整多源系统", std="≥95%+文档",
                 steps=["补全read_one+on_message", "断线重连调通", "10分钟统计截图"]),
        "C": dict(goal="单源贯通", std="数据能入库",
                 steps=["Modbus采集跑通", "Queue到Processor", "SQLite见记录"]),
        "D": dict(goal="架构观察", std="能画线程图",
                 steps=["跑演示notebook", "记录采集率", "手画三线程图"])},
    code=[("退避重连",
"""backoff = 1
while not stop.is_set():
    got = False
    for host, port in PLCS:
        if read_one(host, port): got = True; stat["ok"] += 1
        else: stat["fail"] += 1
    backoff = 1 if got else min(backoff*2, 4)
    time.sleep(0.5 if got else backoff)""",
           )],
    errors=[("Ctrl+C退不出", "没设daemon", "daemon=True"),
             ("Queue满卡死", "put无超时", "put(timeout=1)+丢弃计数"),
             ("线程日志混乱", "无名", "Thread(name='Modbus')")]),
7: dict(
    basics=["设备1-N测点1-N记录；告警挂设备——应用：见工单starter与教师参考实现",
            "外键=关系表达；数据字典逐字段——应用：见工单starter与教师参考实现",
            "ORM声明式+relationship——应用：见工单starter与教师参考实现",
            "bulk批量插入快10倍——应用：见工单starter与教师参考实现",
            "N+1陷阱→joinedload——应用：见工单starter与教师参考实现",
            "索引(device_id,ts)+EXPLAIN——应用：见工单starter与教师参考实现"],
    skills=["四表ER设计与ORM建模——应用：见工单starter与教师参考实现",
            "批量事务入库——应用：见工单starter与教师参考实现",
            "JOIN聚合统计查询——应用：见工单starter与教师参考实现",
            "索引优化前后对比取证——应用：见工单starter与教师参考实现"],
    abcd={
        "A": dict(goal="闭环演示+健康报告", std="EXPLAIN证据",
                 steps=["接P3仪表盘读库", "窗口函数环比", "慢查询Top3报告"]),
        "B": dict(goal="仓库+统计", std="溯源查询正确",
                 steps=["四表ORM建模", "bulk入库500条", "均值/Top3/时段聚合"]),
        "C": dict(goal="两表起步", std="能入库能查",
                 steps=["devices+records两表", "插入并查询", "打印统计"]),
        "D": dict(goal="ER观察", std="能画四表连线",
                 steps=["跑参考ER演示", "手绘关系图", "标主外键"])},
    code=[("ORM模型+查询",
"""class Rec(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    ts = Column(DateTime); vib = Column(Float)

print(s.execute(select(Dev.code, func.avg(Rec.vib))
      .join(Rec, Rec.device_id==Dev.id).group_by(Dev.code)).all())""",
           )],
    errors=[("N+1慢", "循环逐查关联", "joinedload一次带出"),
             ("连接泄漏", "session未关", "with Session()自动关"),
             ("索引不生效", "列序不对", "(device_id,ts)联合序")]),
8: dict(
    basics=["五步流：划分/训练/CV/调参/保存——应用：见工单starter与教师参考实现",
            "混淆矩阵对角=对；业务代价看漏检——应用：见工单starter与教师参考实现",
            "F1宏平均；交叉验证防偶然——应用：见工单starter与教师参考实现",
            "joblib保存+版本命名——应用：见工单starter与教师参考实现",
            "推理服务：POST JSON→预测→返回——应用：见工单starter与教师参考实现",
            "warmup后测p95延迟——应用：见工单starter与教师参考实现"],
    skills=["诊断模型训练与F1达标——应用：见工单starter与教师参考实现",
            "模型接入P5库联动——应用：见工单starter与教师参考实现",
            "推理服务封装与压测——应用：见工单starter与教师参考实现",
            "特征顺序对齐校验——应用：见工单starter与教师参考实现"],
    abcd={
        "A": dict(goal="ONNX对比+P7立项", std="延迟量化对比",
                 steps=["导出ONNX测延迟", "三模型对比报告", "P7综合项目立项书"]),
        "B": dict(goal="训练+服务", std="F1≥0.80+可调用",
                 steps=["五步流训练保存", "接入数据库联动", "curl测试/predict"]),
        "C": dict(goal="基线模型", std="F1达标能保存",
                 steps=["RF训练", "混淆矩阵输出", "joblib保存"]),
        "D": dict(goal="调用体验", std="能发请求",
                 steps=["加载预训练模型", "发一次预测请求", "看返回JSON"])},
    code=[("推理服务核心",
"""def do_POST(self):
    body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
    feats = body["features"]; assert len(feats) == 30
    pred = int(model.predict([feats])[0])
    self._send(200, {"prediction": pred,
                     "label": "磨损" if pred else "正常"})""",
           )],
    errors=[("预测恒同一类", "特征顺序错位", "feature_names.json对齐"),
             ("模型加载失败", "版本不匹配", "记录sklearn版本"),
             ("服务卡死", "单线程长阻塞", "教学够用/生产Litestar+Granian")]),
}


# ===== P7 智能运维平台（扩展第9周·选做，32号轮新增） =====
PP3[9] = dict(
    basics=["多模存储各就各位：关系SQLite / 时序DuckDB / 图Kùzu / 向量Chroma / KV缓存Redis",
            "Litestar全异步框架+Granian(Rust)运行时：替代单线程http.server的部署新范式",
            "ReAct智能体：思考→选工具→观察→结论，六步取证输出结构化诊断工单",
            "缓存三问：什么值得缓存？TTL多长？失效策略？(缓存穿透/雪崩一句带过)",
            "端到端验证思维：verify.sh断言全绿才可交付上线"],
    skills=["会按场景选存储引擎并写决策矩阵留痕——应用：见工单starter与教师参考实现",
            "会把模型/查询包成OpenAI协议工具给智能体调用",
            "会用granian多worker部署并用ab压测对比QPS"],
    abcd=dict(
        D=dict(goal="跑通平台", steps=["bash deploy/run.sh 一键播种+启动",
                                     "curl /health 与 /api/device/PUMP-03 各一次",
                                     "截图live→cache两次响应差异"], std="4个API全部返回200"),
        C=dict(goal="补齐学生版TODO", steps=["完成TODO-P7-1 关系查询", "完成TODO-P7-2 时序窗口",
                                          "完成TODO-P7-4 向量检索"], std="verify.sh 五库段全绿"),
        B=dict(goal="智能体+图路径", steps=["完成TODO-P7-3 Cypher影响路径",
                                          "完成TODO-P7-5 ReAct循环",
                                          "agent/ask 问题换成FAN-02再测一轮"], std="verify.sh ALL PASS"),
        A=dict(goal="上线级优化", steps=["哈希嵌入换bge-small-zh对比召回",
                                       "ab -n 1000 -c 50 压测并调workers",
                                       "docker compose up 真容器部署"], std="写出选型+压测对比报告"),
    ),
    code=[("granian部署", "# Rust运行时拉满多核\ngranian --interface asgi service.app:app \\\
  --host 0.0.0.0 --port 8900 --workers 4"),
          ("智能体调用链", "# engineer.investigate(question)\n# → 台账→时序→图谱→案例→模型 → 诊断工单JSON")],
    errors=[("granian起不来", "模块路径不对", "cd到p77_smart_ops再启动"),
            ("duckdb参数报错STRUCT", "把dict整个传给了标量参数", "绑定a['device']再传"),
            ("kuzu重复主键", "CREATE边时又建了节点", "边要MATCH双端再CREATE"),
            ("chroma首次卡住", "默认嵌入要联网下载", "用自定义HashEmbedding离线跑")],
)
