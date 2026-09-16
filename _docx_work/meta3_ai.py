# -*- coding: utf-8 -*-
"""AI课细化数据(每课): basics基础知识6条/skills技能4条/abcd四层任务/code代码片段/errors常见错误"""

AI3 = {
4: dict(
    basics=["监督学习：从带标签历史数据学习\u201c特征→类别\u201d映射",
            "分类vs回归：离散类别vs连续数值；故障三态判别属分类",
            "逻辑回归：线性边界+sigmoid概率，可解释强、速度快的基线模型",
            "决策树：if-else树状切分，可读性最好，易过拟合需限深",
            "随机森林：多棵树投票，精度稳定性佳，可输出特征重要度",
            "四项指标：准确率(总体)、精确率(报准)、召回率(抓全)、F1(调和)",
            "分层划分：train/test类别比例一致，小数据集必用"],
    skills=["用NumPy读写CSV并切分X/y",
            "调用sklearn三分类器并fit/predict",
            "计算并解读四项评估指标(宏平均)",
            "按决策矩阵选择交付模型并说明理由"],
    abcd={
        "A": dict(goal="三模型对比+决策矩阵+错误样本分析", std="准确率≥0.85且决策答辩流畅",
                 steps=["三模型同台对比并记录指标表", "选2个错判样本分析共性", "填写决策矩阵并准备1分钟讲解"]),
        "B": dict(goal="完成三分类器训练与评估", std="准确率≥0.80",
                 steps=["加载pump_fault.csv并分层划分", "训练LR/DT/RF三模型", "输出四指标对照表"]),
        "C": dict(goal="完成单模型基线", std="准确率≥0.75",
                 steps=["加载CSV并划分数据", "训练随机森林", "计算准确率与F1"]),
        "D": dict(goal="跑通模型调用五步模板", std="程序出结果+口述指标含义",
                 steps=["运行starter示例单元", "把模型换成决策树再跑一次", "记录两轮准确率"])},
    code=[("五步模板(核心骨架)",
"""from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import numpy as np

data = np.genfromtxt("data/pump_fault.csv", delimiter=",", skip_header=1)
X, y = data[:, :5], data[:, 5].astype(int)
Xtr, Xte, ytr, yte = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=42)   # 分层!
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(Xtr, ytr)
print("准确率:", (model.predict(Xte) == yte).mean())"""),
          ("四指标一次算齐",
"""from sklearn.metrics import (accuracy_score, precision_score,
                             recall_score, f1_score)
p = model.predict(Xte)
print(f"准确率{accuracy_score(yte,p):.3f} 精确率{precision_score(yte,p,average='macro'):.3f}"
      f" 召回率{recall_score(yte,p,average='macro'):.3f} F1{f1_score(yte,p,average='macro'):.3f}")""")],
    errors=[("准确率忽高忽低", "未固定random_state/未分层划分", "加random_state=42与stratify=y"),
             ("漏检轴承磨损严重但指标尚可", "只看了准确率", "漏报代价高→重点核查召回率"),
             ("predict报维度错误", "训练时X含标签列", "切X=data[:,:5]勿带第6列")]),
5: dict(
    basics=["特征构建：由原始列派生新列(比值/乘积/统计量)",
            "归一化Min-Max：压到[0,1]，受极值影响",
            "标准化Z-score：均值0方差1，更适合近似正态",
            "树模型对单调缩放不敏感——决策矩阵要体现",
            "3σ清洗：|x-μ|>3σ视为异常并剔除",
            "交叉验证：5折轮换验证，评估稳定性",
            "网格搜索：GridSearchCV穷举超参组合选优"],
    skills=["派生≥2个物理含义明确的特征",
            "实现消融实验并记录每步指标",
            "使用GridSearchCV调参(仅训练集)",
            "用5折交叉验证输出均值±方差"],
    abcd={
        "A": dict(goal="≥3种优化组合+交叉验证报告", std="提升≥10%且F1≥0.80",
                 steps=["清洗+2特征+缩放+调参全链路", "消融表逐步留痕", "CV稳定性报告+生产推荐配置"]),
        "B": dict(goal="完成特征工程全流程", std="提升≥7%",
                 steps=["3σ清洗并记录条数", "构建振动/电流比等2特征", "网格搜索n_estimators"]),
        "C": dict(goal="完成清洗+1个新特征", std="提升≥5%",
                 steps=["3σ清洗", "加1个派生特征", "前后准确率对比"]),
        "D": dict(goal="跑通消融演示", std="能复述每步指标变化",
                 steps=["运行starter消融循环", "把fillna改成dropna观察差异", "记录两版结果"])},
    code=[("消融实验循环",
"""ABLATION = []
def evaluate(tag, Xa):
    m = RandomForestClassifier(random_state=42).fit(Xtr2, ytr2)
    acc = (m.predict(Xte2) == yte2).mean()
    ABLATION.append((tag, acc))
    print(f"[消融]{tag:<14} acc={acc:.3f}")""",
           ),
          ("派生特征+网格搜索",
"""Xf = np.c_[Xc, Xc[:,3]/Xc[:,4]]           # 振动/电流比
from sklearn.model_selection import GridSearchCV
gs = GridSearchCV(RandomForestClassifier(random_state=42),
                  {"n_estimators":[50,100,200]}, cv=5)
gs.fit(Xtr, ytr)      # 只用训练集!
print(gs.best_params_, gs.best_score_)""")],
    errors=[("调参后测试指标反降", "在全量数据上调参(泄漏)", "严格train上调、test只看一次"),
             ("归一化后树模型无变化", "树对单调缩放不敏感", "正常现象，矩阵中写明"),
             ("消融表数字对不上", "一次改多处", "每步只加一个变量并即时记录")]),
6: dict(
    basics=["神经元：加权求和+非线性激活(ReLU)",
            "网络=层堆叠：Input→Conv→Pool→FC→Output",
            "卷积核3×3扫图做局部加权→提取边缘/纹理",
            "池化2×2取最大→尺寸减半、保留显著特征",
            "形状追踪：(N,1,64,64)→conv→pool→…→(N,4)",
            "归一化/255：把像素压到0-1，加速收敛",
            "数据增强：翻转/平移扩充样本防过拟合"],
    skills=["完成TinyCNN的forward前向传播",
            "编写batch训练循环并打印loss",
            "用张量形状追踪法定位维度错误",
            "对测试图输出预测+softmax置信度"],
    abcd={
        "A": dict(goal="数据增强对比+loss曲线+混淆矩阵", std="准确率≥0.88",
                 steps=["加随机水平翻转增强", "绘制loss/acc曲线", "混淆矩阵分析1个误判样本"]),
        "B": dict(goal="完整训练评估流程", std="准确率≥0.85",
                 steps=["补全forward与训练循环(6轮)", "记录每轮loss与测试acc", "输出形状追踪表"]),
        "C": dict(goal="跑通训练", std="准确率≥0.80",
                 steps=["加载npy数据并归一化", "完成forward", "训练6轮看acc"]),
        "D": dict(goal="推理体验", std="能读懂形状表",
                 steps=["加载预训练权重仅推理", "上传图片看预测", "抄写形状追踪表"])},
    code=[("TinyCNN前向(填空核心)",
"""class TinyCNN(nn.Module):
    def forward(self, x):                  # (N,1,64,64)
        x = self.pool(torch.relu(self.conv1(x)))  # →(N,8,31,31)
        x = self.pool(torch.relu(self.conv2(x)))  # →(N,16,14,14)
        x = x.flatten(1)                   # →(N,3136)
        return self.fc2(torch.relu(self.fc1(x)))  # →(N,4)"""),
          ("训练循环骨架",
"""for i in range(0, len(Xtr), 32):
    b = perm[i:i+32]
    opt.zero_grad()
    loss = lossf(model(Xtr[b]), ytr[b])
    loss.backward(); opt.step()""")],
    errors=[("loss停在1.386不动", "忘记/255归一化", "X=X.astype('float32')/255.0"),
             ("尺寸不匹配报错", "通道序/flatten位置错", "逐步打印x.shape定位"),
             ("训练慢", "batch太小/full-batch", "batch=32并只训6轮")]),
7: dict(
    basics=["时间序列：按时间顺序记录的序列数据",
            "滑动窗口：前w步作输入、第w+1步作标签",
            "RNN缺陷：长序列梯度消失→LSTM引入门控",
            "LSTM三门：遗忘/输入/输出控制记忆读写",
            "RUL剩余寿命：归一化1→0表示健康→失效",
            "回归指标：MSE/RMSE/MAE越小越好",
            "早停：验证loss不再下降即停，防过拟合"],
    skills=["可视化窗口-标签对应关系(--viz)",
            "构建LSTM回归模型并训练",
            "计算MSE/RMSE/MAE三指标",
            "绘制真实vs预测RUL曲线并业务解读"],
    abcd={
        "A": dict(goal="LSTMvs线性基线对比+敏感性实验", std="MSE<0.10",
                 steps=["训练线性回归基线", "对比两模型误差曲线", "改窗口长度w=10/20/30看影响"]),
        "B": dict(goal="完整LSTM预测流程", std="MSE≤0.12",
                 steps=["跑--viz核对窗口对齐", "训练RULNet(≤60轮)", "三指标+预测曲线"]),
        "C": dict(goal="跑通训练与评估", std="MSE<0.15",
                 steps=["加载bearing_rul.npz", "训练60轮", "算MSE并画曲线"]),
        "D": dict(goal="窗口可视化理解", std="能讲清输入标签",
                 steps=["运行--viz出图", "换一个样本i再看", "口头解释RUL含义"])},
    code=[("LSTM模型定义",
"""class RULNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(1, 32, batch_first=True)
        self.fc = nn.Linear(32, 1)
    def forward(self, x):              # (N,20,1)
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :]).squeeze(-1)  # 取最后时刻"""),
          ("三指标计算",
"""p = model(Xte).detach().numpy()
mse = ((p - yte.numpy())**2).mean()
print(f"MSE={mse:.4f} RMSE={mse**0.5:.4f} MAE={abs(p-yte.numpy()).mean():.4f}")""")],
    errors=[("MSE降后回升", "过拟合", "减轮数/加早停观察验证loss"),
             ("预测全是一条直线", "学习率过大或特征未归一化", "lr=1e-3并检查输入尺度"),
             ("X/y错位", "窗口切分标签取错位", "用--viz图核对t..t+19→t+20")]),
8: dict(
    basics=["数字图像=二维矩阵；灰度图单通道0-255",
            "色彩空间：GRAY/RGB/HSV及转换",
            "高斯滤波：抑制噪声、平滑图像",
            "阈值分割：灰度差→二值前景/背景",
            "形态学开运算：先腐蚀后膨胀去噪点",
            "轮廓：连通边界曲线；contourArea算面积",
            "像素当量：标定1px=0.1mm，面积要平方换算"],
    skills=["构建预处理链条并可视化中间图",
            "阈值策略对比实验(全局/Otsu/自适应)",
            "findContours提取并过滤轮廓",
            "缺陷判型+尺寸换算+画框标注输出"],
    abcd={
        "A": dict(goal="多缺陷全检出+误检归零分析", std="误差<5%",
                 steps=["三种阈值策略各测5件", "多缺陷件逐一检出", "每个误检写成因分析"]),
        "B": dict(goal="完整测量链路", std="误差<8%",
                 steps=["预处理→分割→轮廓", "划痕长度/凹坑面积换算", "标注图输出"]),
        "C": dict(goal="单缺陷测量", std="误差<10%",
                 steps=["跑通预处理链条", "测一个缺陷尺寸", "输出标注图"]),
        "D": dict(goal="阈值实验体验", std="能说出参数影响",
                 steps=["改阈值100→80→120看结果", "记录检出变化", "口述当量换算公式"])},
    code=[("测量链路核心",
"""blur = cv2.GaussianBlur(img, (5,5), 0)
_, bw = cv2.threshold(blur, 0, 255,
                      cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
cnts, _ = cv2.findContours(bw, cv2.RETR_EXTERNAL,
                           cv2.CHAIN_APPROX_SIMPLE)
for c in cnts:
    if cv2.contourArea(c) < 15: continue     # 滤噪
    w, h = sorted(cv2.minAreaRect(c)[1])
    length_mm = w * 0.1                      # 当量换算"""),
          ("面积换算(平方!)",
"""area_px = cv2.contourArea(c)
area_mm2 = area_px * 0.1 ** 2     # 350px²→3.5mm²""")],
    errors=[("面积大10倍", "当量没平方", "×0.1²而不是×0.1"),
             ("轮廓重复计数", "用了RETR_TREE", "改RETR_EXTERNAL只要外轮廓"),
             ("阈值后全黑/全白", "方向反了", "暗缺陷用BINARY_INV")]),
9: dict(
    basics=["YOLO：整图一次前向输出全部候选框",
            "输出张量(84,8400)：0-3行xywh、4-83行80类分数",
            "置信度过滤+NMS去重叠框",
            "imgsz输入尺寸：大→准但慢",
            "FPS衡量实时性；产线节拍是硬约束",
            "训练/推理分离：GPU训练、CPU推理",
            "微调：预训练权重+自有数据继续训练"],
    skills=["加载本地权重执行CPU推理",
            "解析(84,8400)输出并画框",
            "conf阈值实验与imgsz三档FPS测试",
            "输出精度-速度权衡决策矩阵"],
    abcd={
        "A": dict(goal="推理优化量化提速", std="较默认提速≥50%",
                 steps=["batch推理/输入裁剪实验", "量化前后FPS对比", "写权衡结论入工单"]),
        "B": dict(goal="完整推理+双实验", std="检出稳定+实验记录全",
                 steps=["推理20张并可视化", "conf四档阈值实验", "imgsz三档FPS测试"]),
        "C": dict(goal="推理与可视化", std="能出标注图",
                 steps=["加载yolov8n权重", "推理5张出结果图", "记录检出数"]),
        "D": dict(goal="零检出观察讨论", std="能说为何需微调",
                 steps=["实物照推理看检出", "缺陷图推理看零检出", "讨论原因写两句"])},
    code=[("ONNX解析(84,8400)",
"""out = sess.run(None, {"images": x})[0][0]   # (84,8400)
cls = out[4:]                               # (80,8400)
conf, cid = cls.max(0), cls.argmax(0)
keep = np.where(conf > 0.4)[0]              # 阈值过滤
boxes = out[:4, keep].T                      # cx,cy,w,h @640"""),
          ("FPS计时(warmup后)",
"""for _ in range(3): model.predict(img, imgsz=sz, verbose=False)  # warmup
t0 = time.time()
for _ in range(10): model.predict(img, imgsz=sz, verbose=False)
print(f"FPS={10/(time.time()-t0):.1f}")""")],
    errors=[("在线下载权重失败", "机房无外网", "用data/weights离线加载"),
             ("框画错位置", "640坐标没还原原图", "按缩放比换算回原尺寸"),
             ("FPS忽小", "把IO也计进去了", "只计predict段并warmup")]),
10: dict(
    basics=["NLP：让机器处理自然语言文本",
            "分词：jieba精确模式切词",
            "停用词：的/了等无信息词需过滤",
            "词袋模型：文本→词频向量",
            "TF-IDF：常见词降权、专属词升权",
            "文本分类：向量→类别标签",
            "数据泄漏：向量化只能fit训练集"],
    skills=["jieba分词+停用词过滤管线",
            "TF-IDF向量化(Pipeline防泄漏)",
            "NB与LR双分类器对比评估",
            "输出Top关键词并解释贡献"],
    abcd={
        "A": dict(goal="混淆矩阵+词典调优", std="准确率≥0.85",
                 steps=["混淆矩阵找易混两类", "加自定义词典或ngram", "解释关键词贡献"]),
        "B": dict(goal="双分类器完整对比", std="准确率≥0.80",
                 steps=["分词+停用词过滤", "Pipeline(NB/LR)训练对比", "预测自收集新文本"]),
        "C": dict(goal="单分类器管线", std="准确率≥0.75",
                 steps=["完成分词", "TF-IDF+NB训练", "预测3条新文本"]),
        "D": dict(goal="分词体验", std="能看懂词云",
                 steps=["jieba.cut两句故障描述", "对比去停用词前后", "看Top10词表"])},
    code=[("文本分类管线",
"""from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
def cut(t): return " ".join(w for w in jieba.cut(t)
                            if w not in STOP and len(w)>1)
pipe = make_pipeline(TfidfVectorizer(max_features=2000),
                     LogisticRegression(max_iter=1000))
pipe.fit([cut(t) for t in texts_train], labels_train)""",
           ),
          ("Top关键词",
"""import jieba.analyse
print(jieba.analyse.extract_tags(" ".join(all_texts), topK=10,
                                  withWeight=True))""")],
    errors=[("Top10全是虚词", "停用词没滤", "扩充STOP表再统计"),
             ("测试指标虚高", "向量化fit了全量(泄漏)", "Pipeline只在训练集fit"),
             ("中文乱码", "编码不一致", "统一encoding='utf-8'")]),
11: dict(
    basics=["LLM大语言模型：生成式文本能力",
            "Prompt工程：角色设定/上下文/示例引导",
            "RAG=检索+生成：知识库TopK注入Prompt",
            "Agent：LLM+工具调用+多步规划",
            "幻觉：无依据生成→需检索锚定与校验",
            "数据合规：企业数据不出域、脱敏前置",
            "容错三招：超时/重试/降级话术"],
    skills=["三版Prompt对比实验",
            "KnowledgeBase检索注入CONTEXT（检索双解：重合度打分→Chroma向量库）",
            "Agent两步推理(判断→工具→汇总)",
            "requests容错( timeout/重试/降级)"],
    abcd={
        "A": dict(goal="多轮对话+容错实测", std="≥10问且过程清晰",
                 steps=["加对话历史拼接", "HALLUCINATE=1容错实测", "RAG前后对比记录"]),
        "B": dict(goal="RAG链路+Prompt对比", std="≥7问有依据回答",
                 steps=["三版Prompt实验", "检索注入CONTEXT再生成", "记录是否grounded"]),
        "C": dict(goal="基础问答", std="≥5问正确回答",
                 steps=["调用本地LLM", "优化一次Prompt", "记录5组问答"]),
        "D": dict(goal="调用体验", std="能复述容错逻辑",
                 steps=["跑通一次问答", "把Prompt改得更具体", "观察回答变化"])},
    code=[("带容错的调用",
"""def chat(msgs, retries=2):
    for i in range(retries+1):
        try:
            r = requests.post(URL, json={"messages":msgs}, timeout=5)
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
        except requests.RequestException: pass
    return "[降级]服务暂不可用，已转人工工单。\"""",
           ),
          ("RAG注入",
"""ctx = "\\n".join(kb.retrieve(question, topk=2))
answer = chat([{"role":"system","content":"CONTEXT:"+ctx},
               {"role":"user","content":question}])""")],
    errors=[("回答无依据", "没接知识库", "检索结果注入CONTEXT前缀"),
             ("程序卡死", "无timeout", "requests加timeout=5"),
             ("真实API被叫", "合规红线", "课内只用本地模拟LLM")]),
}
