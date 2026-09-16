# 工业互联网应用专业《AI应用基础》课程标准

## 目录

- [一、课程概述](#一课程概述)
- [二、教学目标](#二教学目标)
- [三、教学内容](#三教学内容)
- [四、课程实施保障条件](#四课程实施保障条件)
- [五、学习评价](#五学习评价)

---

## 一、课程概述

### （一）课程基本信息

| 项目           | 内容                                        |
| ------------ | ----------------------------------------- |
| **课程代码**     | B46021002                                 |
| **开课学院**     | 智能控制学院                                    |
| **课程名称**     | AI应用基础                                    |
| **面向的职业及岗位** | 工业数据采集技术员、边缘计算运维员、工业网络实施与运维工程师、工业互联网平台运维员 |
| **学分**       | 3                                         |
| **总学时**      | 48                                        |
| **理论学时**     | 24                                        |
| **实习（训）学时**  | 24                                        |
| **授课周数**     | 12周                                       |
| **周学时**      | 4课时/周                                     |
| **先修课程**     | 《Python编程基础》建议完成前6周内容                     |

### （二）课程性质与定位

《AI应用基础》是工业互联网应用专业的核心课程，面向专科一年级新生开设。本课程建立在《Python编程基础》基础之上，以工业实际应用为驱动，通过**传统机器学习→深度学习→大模型与智能体→强化学习→多模态AI**的递进路径，培养学生的AI应用能力。特别强调图像识别、自然语言处理、语音处理、大模型集成、智能体编程等在工业中的实际应用。

**课程定位**：

1. **职业面向**：适配工业互联网四大核心岗位的AI应用需求
2. **知识结构**：ML基础 → 深度学习与神经网络 → 计算机视觉 → **大模型原理与应用 → 智能体系统设计** → NLP与语音 → 强化学习与AI优化
3. **实践取向**：以工业视觉检测、大模型故障诊断、多智能体协调、故障预测、设备优化为真实场景
4. **技术前沿**：涵盖当前AI领域的主流技术与实际应用，特别是生成式AI与大模型应用

（三）课程与其他课程的关系

| 序号  | 前续课程         | 相互衔接和关联的知识点、技能点、软硬件工具、标准规范                              |
| --- | ------------ | ------------------------------------------------------- |
| 1   | 《Python编程基础》 | 知识点：Python语法、数据结构、异常处理 / 技能点：代码编写、调试、模块化设计 / 工具：IDE、Git |
| 2   | 数学基础         | 知识点：线性代数、概率统计、微积分基础 / 技能点：数学建模、统计分析                     |
| 3   | 计算机网络基础      | 知识点：数据格式、网络协议、API调用                                     |

| 序号  | 后续课程           | 相互衔接和关联的知识点、技能点、软硬件工具、标准规范             |
| --- | -------------- | -------------------------------------- |
| 1   | 工业互联网应用集成      | 知识点：模型部署、边缘计算、系统架构 / 技能点：模型服务化、性能优化    |
| 2   | 深度学习与计算机视觉（选修） | 知识点：神经网络、卷积神经网络 / 库：TensorFlow、PyTorch |
| 3   | 工业互联网平台运维      | 知识点：大数据处理、数据治理 / 工具：Spark、Flink（流处理）   |

### （四）对接"1+X"证书

- **数据分析职业技能等级证书**（初/中/高级）
- **AI应用实践证书**（工业互联网相关）
- **机器学习工程师认证**（阶段性）

### （五）课程基本教学理念

1. **工业问题导向**：围绕真实的工业场景（设备故障预测、性能优化、异常检测）设计教学
2. **"数据→模型→决策"完整链条**：从数据采集、清洗、特征工程，到模型训练、评估、部署
3. **理解优于记忆**：重视模型原理理解与可解释性，而非盲目调参
4. **工程实践先行**：优先解决实际问题，再深入理论推导
5. **轻量级模型优先**：考虑边缘计算环境，优先使用部署友好的算法（决策树、XGBoost等）

---

## 二、教学目标

### （一）知识目标

1. **传统机器学习**（回顾）
   
   - 分类、回归、时间序列的基本模型
   - 特征工程与超参数调优

2. **深度学习与神经网络**
   
   - 理解神经网络的结构与前向传播、反向传播
   - 掌握卷积神经网络（CNN）的基本原理
   - 了解循环神经网络（RNN、LSTM）的时间序列能力
   - **理解Transformer架构与自注意力机制**
   - **理解大模型的预训练与微调原理**

3. **计算机视觉**
   
   - 掌握图像分类、物体检测的方法
   - 理解缺陷检测的工业应用原理
   - 了解迁移学习在工业视觉中的应用
   - **掌握多模态视觉大模型的使用**

4. **自然语言处理与大模型**
   
   - 掌握文本表示与词向量（Word2Vec、BERT）
   - 理解文本分类与情感分析方法
   - **理解大语言模型（LLM）的基本原理与能力**
   - **掌握Prompt工程的核心概念与技巧**
   - **了解RAG（检索增强生成）的工作原理**
   - **理解思维链（Chain-of-Thought）推理方法**

5. **语音处理**
   
   - 理解语音信号处理基础
   - 掌握语音识别与语音合成的基本应用
   - **了解语音大模型的工业应用**
   - 了解多模态（音频+文本+视觉）的融合应用

6. **智能体与多智能体系统**
   
   - **理解智能体的基本架构与工作流**
   - **掌握工具调用（Tool Use）与Function Calling机制**
   - **理解多智能体的通信与协调机制**
   - **了解多智能体在工业中的应用场景**

7. **强化学习与优化**
   
   - 理解马尔可夫决策过程（MDP）与值函数
   - 掌握Q-Learning算法基础
   - 了解策略梯度与Actor-Critic方法
   - **理解深度强化学习与智能体训练**
   - 理解在工业优化中的应用

### （二）能力目标

1. **深度学习开发能力**
   
   - 能够使用TensorFlow/PyTorch搭建神经网络
   - 能够进行模型训练、验证、测试的完整流程
   - 能够进行模型诊断与超参数优化

2. **计算机视觉应用能力**
   
   - 能够进行图像数据的预处理与增强
   - 能够使用预训练模型进行图像分类
   - 能够进行工业缺陷检测与定位
   - **能够使用多模态视觉大模型进行零样本检测**

3. **NLP与大模型应用能力**
   
   - 能够进行文本预处理与向量化
   - 能够训练文本分类模型
   - **能够调用大模型API（ChatGPT、Claude等）解决工业问题**
   - **能够设计和优化Prompt工程以提高任务准确率**
   - **能够实现RAG系统用于技术文档问答**
   - **能够使用思维链（CoT）进行复杂推理**

4. **语音处理与多模态能力**
   
   - 能够进行语音信号的基本处理
   - 能够调用语音识别API进行实时转录
   - **能够使用语音大模型进行工业指令理解**
   - **能够融合音频、文本、图像等多模态信息进行综合分析**

5. **智能体编程与设计能力**
   
   - **能够理解智能体的基本架构（感知-推理-执行）**
   - **能够使用LLM框架（如LangChain、AutoGPT框架）构建智能体**
   - **能够设计工具接口（Tool Use）供智能体调用**
   - **能够实现多智能体系统的通信与协调机制**
   - **能够验证智能体的决策过程与可靠性**

6. **强化学习与智能体优化能力**
   
   - 能够建模工业优化问题为MDP
   - 能够实现基本的强化学习算法
   - **能够结合大模型与强化学习进行智能体训练**
   - **能够进行智能体的评估与改进**

### （三）素质目标

1. **AI伦理与责任意识**
   
   - 理解AI在工业应用中的伦理问题
   - **理解大模型的局限性与幻觉问题**
   - **树立"AI为人服务"与"以人为中心"的意识**
   - 关注数据隐私、模型解释性、智能体决策可追溯

2. **创新意识**
   
   - 鼓励学生探索AI在工业新应用
   - 培养"技术 + 工业领域知识"的交叉思维
   - **培养"大模型+工业知识"的创新思维**

3. **工程化思维**
   
   - 理解从研究到生产环境的差异
   - 掌握模型部署、监控、迭代的完整流程
   - **理解智能体在实际工业系统中的集成方式**

---

## 三、教学内容

### （一）教学方式

#### 1. 理实一体教学

通过案例讲解算法原理，结合Jupyter Notebook/Python脚本演示代码实现，学生实时跟进修改参数、观察模型效果变化，形成"理解→编码→实验→优化"的闭环。

**实现方式**：

- 讲解阶段（15分钟）：讲解算法原理、超参数含义、应用场景
- 演示阶段（15分钟）：使用真实工业数据演示模型训练与评估
- 实践阶段（25分钟）：学生改变超参数、数据预处理方式，观察效果变化

**案例融合**：每堂课都围绕真实工业问题设计，例如：

- "分类模型" → 设备故障分类预测
- "时间序列" → 生产线产量预测
- "异常检测" → 传感器数据异常识别

#### 2. 项目驱动学习

将课程内容组织为若干个递进式、任务化的"AI工单项目"，每个工单都是完整的、可评估的、有业务价值的AI应用。

**工单特征**：

- 规模：200-500行代码 + Jupyter Notebook + 模型文件
- 产出：完整的.py模型库 + .ipynb探索记录 + 模型评估报告
- 场景：模拟真实的工业AI应用（预测、诊断、优化）
- 评价：按模型性能、代码规范、文档完整性评分

**工单层级**：

- L1（入门）：单个算法的直接应用与调参
- L2（进阶）：多个算法的对比与集成
- L3（挑战）：创新特征工程或新算法的探索

#### 3. 数据驱动的迭代学习

使用真实或仿真的工业数据集，让学生在数据探索、特征工程、模型训练、结果分析的过程中不断迭代改进。

**数据集支持**：

- 工业传感器采样数据（温度、压力、振动等）
- 设备故障历史数据（标记故障类型与发生时间）
- 生产线产量与质量数据
- 仿真数据生成脚本（OpenAI Gym、自定义生成器）

#### 4. 模型对标与评估

强调模型选择的科学性，通过实验对比不同算法在同一任务上的表现，帮助学生理解"没有最好的算法，只有最合适的算法"。

**对标方式**：

- 同一数据集上多个模型的性能对比
- 不同超参数下的性能曲线分析
- 模型复杂度与准确率的权衡

### （二）教学内容与进度

### （一）模块M1：数据处理与特征工程（第1-2周，8课时）

**学习内容**：Pandas数据处理、EDA分析、特征工程、特征选择

**工单项目**：工业设备采样数据清洗与分析

---

### （二）模块M2：传统ML与深度学习基础（第3-6周，16课时）

#### **任务M2.1：分类模型与XGBoost（第3-4周，8课时）**

**学习内容**：分类评估指标、决策树、随机森林、XGBoost

**工单项目**：工业设备故障多分类预测模型

#### **任务M2.2：深度学习与神经网络（第5-6周，8课时）**

**学习目标**：

- 知识：理解神经网络结构、卷积神经网络、循环神经网络、**Transformer与大模型基础**
- 能力：能够使用TensorFlow/PyTorch搭建深度学习模型
- 素质：培养对AI底层原理的理解

**学习流程**：

**第一部分：神经网络基础（2课时）**

- 神经元、激活函数、损失函数的基本概念
- 前向传播与反向传播算法
- 梯度下降与优化方法（SGD、Adam）

**第二部分：卷积神经网络（CNN）— 工业视觉基础（2课时）**

- CNN基本原理：卷积层、池化层、全连接层
- 经典架构：AlexNet、VGG、ResNet
- 迁移学习与预训练模型
- 工业应用：产品质量检测、设备故障图像识别

**第三部分：Transformer与大模型基础（2.5课时）**

- **Transformer架构的自注意力机制**
- **大模型的预训练与微调**
- **大模型尺度对性能的影响**
- **理解GPT、BERT等大模型的基本原理**

**第四部分：循环神经网络（RNN/LSTM）— 工业时间序列深化（1.5课时）**

- RNN与LSTM基本原理
- 双向LSTM与Attention机制
- 工业应用：设备性能预测、故障预警

**标准与规范**：TensorFlow/PyTorch官方文档

**工单项目M2.2**：

- 项目名称：工业设备故障深度学习预测模型
- 需求：使用CNN+LSTM混合模型进行多特征故障预测
- 验收标准：分类准确率≥80%、RMSE≤15%、代码规范率≥90%

---

### （三）模块M3：计算机视觉与多模态大模型（第7-9周，12课时）

**学习目标**：

- 知识：掌握图像分类、物体检测、**多模态大模型应用**
- 能力：能够进行工业图像检测和缺陷定位、**使用视觉大模型进行零样本检测**
- 素质：培养工业AI视觉应用的认知

**学习流程**：

**第一部分：图像预处理与特征提取（1.5课时）**

- 图像颜色空间转换与归一化
- 图像增强、特征金字塔、多尺度特征

**第二部分：图像分类与迁移学习（2课时）**

- 使用预训练模型（ResNet、MobileNet）
- 工业应用案例：产品分类、设备状态识别

**第三部分：物体检测与缺陷定位（2课时）**

- 物体检测基础：YOLO、Faster R-CNN
- 工业缺陷检测工作流
- 代码实践与结果可视化

**第四部分：多模态视觉大模型应用（2课时）** ✨ **v3.0新增**

- **GPT-4V、LLaVA等视觉大模型原理**

- **零样本图像分类与理解**

- **利用视觉大模型进行故障图片分析与诊断**

- **代码实践**：
  
  ```python
  # 使用GPT-4V进行工业图像分析
  from openai import OpenAI
  import base64
  
  client = OpenAI(api_key='your-api-key')
  
  # 编码图像
  with open('equipment_fault.jpg', 'rb') as f:
      image_data = base64.standard_b64encode(f.read()).decode()
  
  # 调用视觉大模型进行故障诊断
  response = client.chat.completions.create(
      model='gpt-4-vision-preview',
      messages=[
          {
              'role': 'user',
              'content': [
                  {'type': 'text', 'text': '这是一张工业设备的图片，请分析可能存在的故障'},
                  {'type': 'image_url', 'image_url': {'url': f'data:image/jpeg;base64,{image_data}'}}
              ]
          }
      ]
  )
  
  print(response.choices[0].message.content)
  ```

**软硬件工具**：OpenCV、TensorFlow、YOLO、OpenAI API、Hugging Face模型

**工单项目M3**：

- 项目名称：工业产品多模态缺陷检测系统
- 需求：结合YOLO物体检测与视觉大模型进行缺陷分析
- 验收标准：mAP≥0.70、缺陷诊断准确率≥80%、代码规范率≥90%

---

### （四）模块M4：自然语言处理、大模型与智能体基础（第9-11周，12课时）

**学习目标**：

- 知识：掌握NLP、**LLM原理、Prompt工程、RAG、思维链、智能体架构**
- 能力：能够调用大模型API、**设计Prompt、实现RAG系统、构建简单智能体**
- 素质：培养大模型时代的AI应用思维

**学习流程**：

**第一部分：NLP基础与文本分类（2课时）**

1. 文本向量化方法：TF-IDF、Word2Vec、BERT
2. 文本分类应用：故障类型分类、工单优先级
3. 代码实践与模型评估

**第二部分：大语言模型原理与应用（2.5课时）** ✨ **v3.0新增核心内容**

1. **LLM基础概念**
   
   - Transformer架构在大模型中的应用
   - Token化与位置编码
   - 自注意力机制如何实现上下文理解
   - 大模型的涌现能力（Emergent Abilities）

2. **主流大模型介绍**
   
   - GPT系列（GPT-3.5、GPT-4）的能力与限制
   - Claude系列的特点与应用
   - 开源模型：Llama、Mistral等
   - 行业特定模型：代码模型、医疗模型等

3. **调用大模型API**
   
   ```python
   from openai import OpenAI
   
   client = OpenAI(api_key='your-api-key')
   
   # 基础对话
   response = client.chat.completions.create(
       model='gpt-4',
       messages=[
           {'role': 'system', 'content': '你是一个工业设备故障诊断专家'},
           {'role': 'user', 'content': '轴承温度异常升高，可能是什么原因？'}
       ],
       temperature=0.7,
       max_tokens=500
   )
   
   print(response.choices[0].message.content)
   ```

**第三部分：Prompt工程（提示词优化）（2课时）** ✨ **v3.0新增核心内容**

1. **Prompt工程的核心技巧**
   
   - 角色设定（Role Prompt）：定义大模型的身份
   - 上下文定义（Context）：提供必要的背景信息
   - 任务明确化（Task）：清楚地说明要求
   - 输出格式指定（Output Format）：JSON、表格等
   - 例子示范（Few-shot Learning）：提供示例

2. **工业应用中的Prompt设计**
   
   *示例1：故障诊断Prompt*
   
   ```
   你是一个资深的工业设备维修工程师。
   
   背景信息：
   - 设备型号：重型加工中心CNC-2000
   - 运行时长：12000小时
   - 环境温度：25°C
   
   故障现象：
   - 加工精度下降2mm
   - 主轴振动增加
   - 温度传感器读数：+8°C异常升高
   
   请按以下格式分析故障原因：
   {
       "可能原因":[
           {"原因":"...","置信度":"高/中/低","验证方法":"..."}
       ],
       "建议维修方案":[
           {"方案":"...","预计成本":"...","完成时间":"..."}
       ],
       "紧急程度":"高/中/低"
   }
   ```
   
   *示例2：生成维护报告Prompt*
   
   ```
   根据以下设备运行数据生成一份简明的周维护报告：
   
   数据：[提供JSON格式的设备数据]
   
   要求：
   1. 总结本周设备运行状况
   2. 识别关键性能指标（KPI）的异常
   3. 列出建议的维护措施
   4. 预估下周可能的故障风险
   
   输出格式：Markdown表格
   ```

3. **提示词优化技巧**
   
   - 迭代与测试：测试不同的Prompt版本
   - 模板化：为常见任务建立Prompt模板
   - 链式提示：多步骤的Prompt设计

4. **代码实践：Prompt管理系统**
   
   ```python
   class PromptManager:
       def __init__(self):
           self.prompts = {}
   
       def add_prompt(self, name, template):
           """注册一个Prompt模板"""
           self.prompts[name] = template
   
       def format_prompt(self, name, **kwargs):
           """格式化Prompt并填充参数"""
           return self.prompts[name].format(**kwargs)
   
   # 使用示例
   manager = PromptManager()
   manager.add_prompt('fault_diagnosis', 
       '你是工业设备诊断专家。设备: {device}\n症状: {symptom}\n请诊断故障原因。')
   
   prompt = manager.format_prompt('fault_diagnosis', 
       device='水泵', symptom='异常噪声')
   ```

**第四部分：RAG（检索增强生成）系统（2课时）** ✨ **v3.0新增核心内容**

1. **RAG的基本原理**
   
   - 问题：大模型的知识可能过时、幻觉问题
   - 解决方案：从外部知识库检索相关信息，增强生成
   - 工作流：查询→检索→增强→生成

2. **RAG在工业中的应用**
   
   - 技术文档问答系统
   - 设备故障排查助手
   - 工业规范查询系统

3. **RAG实现（使用LangChain）**
   
   ```python
   from langchain.vectorstores import FAISS
   from langchain.embeddings.openai import OpenAIEmbeddings
   from langchain.chat_models import ChatOpenAI
   from langchain.chains import RetrievalQA
   from langchain.document_loaders import PDFLoader
   from langchain.text_splitter import CharacterTextSplitter
   
   # 加载技术文档
   loader = PDFLoader('equipment_manual.pdf')
   documents = loader.load()
   
   # 文本分割
   text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
   docs = text_splitter.split_documents(documents)
   
   # 创建向量存储
   embeddings = OpenAIEmbeddings()
   vectorstore = FAISS.from_documents(docs, embeddings)
   
   # 构建RAG链
   llm = ChatOpenAI(model='gpt-4', temperature=0)
   qa = RetrievalQA.from_chain_type(
       llm=llm,
       chain_type='stuff',
       retriever=vectorstore.as_retriever()
   )
   
   # 查询
   result = qa.run('如何更换水泵的密封圈？')
   print(result)
   ```

**第五部分：思维链（Chain-of-Thought）与多步推理（1.5课时）** ✨ **v3.0新增核心内容**

1. **思维链的基本概念**
   
   - CoT提示："让我们一步一步思考..."
   - 自洽性（Self-Consistency）：多次生成取多数
   - 改进的CoT：结构化推理过程

2. **工业应用中的多步推理**
   
   ```
   任务：根据多个传感器数据诊断故障
   
   Prompt示例：
   "让我们按以下步骤分析这个故障：
   1. 首先，分析温度传感器的异常模式
   2. 其次，关联压力传感器的变化
   3. 然后，检查时间序列的相关性
   4. 最后，综合判断最可能的故障类型
   
   请逐步分析并给出最终诊断。"
   ```

3. **代码实践：多步推理系统**
   
   ```python
   def multi_step_diagnosis(sensor_data):
       steps = [
           '分析温度异常',
           '分析压力波动',
           '检查时间关联',
           '综合诊断'
       ]
   
       for step in steps:
           prompt = f"考虑到{step}，请分析: {sensor_data}"
           response = call_llm(prompt)
           print(f"步骤: {step}\n结果: {response}\n")
   ```

**第六部分：智能体基础与工具调用（2.5课时）** ✨ **v3.0新增核心内容**

1. **智能体的基本架构**
   
   - 感知层：获取环境信息
   - 推理层：LLM进行决策
   - 执行层：调用工具完成任务
   - 记忆层：维护上下文与历史

2. **工具调用（Tool Use / Function Calling）**
   
   *定义工具接口*：
   
   ```python
   tools = [
       {
           'type': 'function',
           'function': {
               'name': 'query_sensor_data',
               'description': '查询指定设备的实时传感器数据',
               'parameters': {
                   'type': 'object',
                   'properties': {
                       'device_id': {'type': 'string', 'description': '设备ID'},
                       'sensor_type': {'type': 'string', 'enum': ['temperature', 'pressure', 'vibration']}
                   },
                   'required': ['device_id', 'sensor_type']
               }
           }
       },
       {
           'type': 'function',
           'function': {
               'name': 'trigger_maintenance_alert',
               'description': '触发维护告警',
               'parameters': {
                   'type': 'object',
                   'properties': {
                       'device_id': {'type': 'string'},
                       'alert_level': {'type': 'string', 'enum': ['low', 'medium', 'high']},
                       'reason': {'type': 'string'}
                   },
                   'required': ['device_id', 'alert_level', 'reason']
               }
           }
       }
   ]
   ```
   
   *智能体调用工具*：
   
   ```python
   from openai import OpenAI
   import json
   
   client = OpenAI()
   
   def run_agent(user_query):
       messages = [{'role': 'user', 'content': user_query}]
   
       while True:
           response = client.chat.completions.create(
               model='gpt-4',
               messages=messages,
               tools=tools,
               tool_choice='auto'
           )
   
           # 检查是否需要调用工具
           if response.choices[0].finish_reason == 'tool_calls':
               for tool_call in response.choices[0].message.tool_calls:
                   # 执行工具
                   result = execute_tool(tool_call.function.name, 
                                       json.loads(tool_call.function.arguments))
   
                   # 添加工具结果到消息
                   messages.append({
                       'role': 'assistant',
                       'content': response.choices[0].message.content,
                       'tool_calls': [tool_call]
                   })
                   messages.append({
                       'role': 'tool',
                       'tool_call_id': tool_call.id,
                       'content': str(result)
                   })
           else:
               # 智能体完成任务
               return response.choices[0].message.content
   
   # 使用示例
   result = run_agent('检查设备001的温度传感器，如果异常则触发告警')
   print(result)
   ```

3. **工业应用中的智能体**
   
   - 故障诊断智能体：自动查询传感器→分析故障→建议维修
   - 生产调度智能体：查询设备状态→优化调度→下达指令
   - 文档查询智能体：理解用户问题→检索文档→生成答案

**软硬件工具**：

- OpenAI API、Claude API、Hugging Face推理
- LangChain、LlamaIndex（用于RAG）
- LangChain Agent（用于智能体）

**工单项目M4**：

- 项目名称：工业设备多模态诊断与智能体系统
- 需求描述：
  1. 使用Prompt工程优化故障诊断准确率
  2. 构建RAG系统查询技术文档
  3. 实现工具调用（查询传感器、触发告警）
  4. 集成智能体进行多步诊断
- 验收标准：
  - 文本分类准确率≥80%
  - Prompt优化后诊断准确率提升≥20%
  - RAG检索准确率≥85%
  - 智能体能正确调用≥3个工具
  - 代码规范率≥90%

---

### （五）模块M5：多智能体系统与强化学习（第11-12周，8课时）

**学习目标**：

- 知识：理解多智能体架构、通信机制、强化学习与智能体训练
- 能力：能够设计多智能体系统、实现智能体训练
- 素质：培养系统级AI应用的思维

**学习流程**：

**第一部分：多智能体系统设计（2课时）** ✨ **v3.0新增核心内容**

1. **多智能体的核心问题**
   
   - 通信机制：智能体之间如何交互
   - 协调机制：如何解决冲突与实现合作
   - 学习机制：集中式 vs 分布式学习

2. **经典多智能体场景**
   
   - 生产调度：多台设备的任务分配
   - 流程优化：多个工序的协调
   - 故障诊断：多个诊断智能体的投票

3. **多智能体实现示例**
   
   ```python
   class IndustrialAgent:
       def __init__(self, agent_id, role):
           self.agent_id = agent_id
           self.role = role  # 'sensor', 'analyzer', 'executor'
           self.state = {}
           self.message_queue = []
   
       def perceive(self, sensor_data):
           """感知环境"""
           self.state['sensor_data'] = sensor_data
   
       def reason(self, llm_client):
           """使用LLM进行推理"""
           prompt = f"基于以下数据进行{self.role}分析: {self.state}"
           result = llm_client.chat.completions.create(
               model='gpt-4',
               messages=[{'role': 'user', 'content': prompt}]
           )
           return result.choices[0].message.content
   
       def act(self, action):
           """执行行动"""
           return f"Agent {self.agent_id} 执行: {action}"
   
       def communicate(self, other_agents, message):
           """与其他智能体通信"""
           for agent in other_agents:
               agent.receive_message(self.agent_id, message)
   
       def receive_message(self, from_agent, message):
           """接收来自其他智能体的消息"""
           self.message_queue.append((from_agent, message))
   
   # 多智能体协调示例
   class MultiAgentSystem:
       def __init__(self):
           self.agents = []
   
       def add_agent(self, agent):
           self.agents.append(agent)
   
       def run_coordination(self, sensor_data, llm_client):
           """运行多智能体协调"""
           # 1. 所有智能体感知环境
           for agent in self.agents:
               agent.perceive(sensor_data)
   
           # 2. 每个智能体进行推理
           results = {}
           for agent in self.agents:
               results[agent.agent_id] = agent.reason(llm_client)
   
           # 3. 智能体之间通信与协调
           # 例如：诊断智能体将诊断结果发送给执行智能体
           if 'analyzer' in [a.role for a in self.agents]:
               analyzer = [a for a in self.agents if a.role == 'analyzer'][0]
               diagnosis = results[analyzer.agent_id]
               for agent in self.agents:
                   if agent.role == 'executor':
                       analyzer.communicate([agent], diagnosis)
   
           return results
   ```

**第二部分：强化学习与智能体训练（2课时）**

1. **强化学习基础（回顾）**
   
   - MDP、值函数、Q-Learning
   - 策略梯度与Actor-Critic

2. **深度强化学习（DQN）**
   
   - 经验回放机制
   - 目标网络的作用
   - 工业应用：设备参数优化

3. **代码实践：简单的设备优化问题**
   
   ```python
   import numpy as np
   from collections import deque
   
   class DQNAgent:
       def __init__(self, state_size, action_size):
           self.state_size = state_size
           self.action_size = action_size
           self.memory = deque(maxlen=2000)
           self.gamma = 0.95
           self.epsilon = 1.0
           self.epsilon_decay = 0.995
           self.learning_rate = 0.001
   
           # 构建DQN网络
           self.q_network = self.build_network()
           self.target_network = self.build_network()
   
       def build_network(self):
           """构建深度Q网络"""
           import tensorflow as tf
           model = tf.keras.Sequential([
               tf.keras.layers.Dense(64, activation='relu', input_shape=(self.state_size,)),
               tf.keras.layers.Dense(64, activation='relu'),
               tf.keras.layers.Dense(self.action_size, activation='linear')
           ])
           model.compile(optimizer='adam', loss='mse')
           return model
   
       def remember(self, state, action, reward, next_state, done):
           """存储经验"""
           self.memory.append((state, action, reward, next_state, done))
   
       def replay(self, batch_size):
           """经验回放"""
           if len(self.memory) < batch_size:
               return
   
           batch = np.random.choice(len(self.memory), batch_size, replace=False)
           for idx in batch:
               state, action, reward, next_state, done = self.memory[idx]
   
               # 计算目标Q值
               if done:
                   target = reward
               else:
                   target = reward + self.gamma * np.max(
                       self.target_network.predict(np.array([next_state]))[0]
                   )
   
               # 更新Q网络
               target_f = self.q_network.predict(np.array([state]))
               target_f[0][action] = target
               self.q_network.fit(np.array([state]), target_f, epochs=1, verbose=0)
   
       def update_target_network(self):
           """更新目标网络"""
           self.target_network.set_weights(self.q_network.get_weights())
   ```

**第三部分：综合项目准备（2课时）**

- 复习多智能体系统设计要点
- 综合项目选题与需求分析
- 项目架构设计与技术路线

**软硬件工具**：

- TensorFlow / PyTorch（强化学习）
- Stable-Baselines3（强化学习库）
- Ray RLlib（分布式强化学习）
- 工业模拟环境

**工单项目M5**：

- 项目名称：工业生产多智能体调度与优化系统
- 需求描述：
  1. 设计3个或以上的智能体（感知、诊断、执行）
  2. 实现智能体间的通信与协调
  3. 使用强化学习优化调度策略
  4. 与单智能体方案对比
- 验收标准：
  - 正确定义MDP问题
  - 多智能体协调正确率≥80%
  - 与基准策略相比改进≥30%
  - 代码规范率≥90%
  - 包含系统交互流程图

---

### （六）综合项目（第12周完成）

**综合项目选题**：

**选项1：完整的工业AI决策支持系统**（推荐）✨

- 功能集成：视觉检测 + 文本/语音多模态分析 + 大模型诊断 + 多智能体协调
- 涉及知识点：CNN、NLP、LLM、RAG、多智能体、工具调用
- 工作量：2000+行代码

**选项2：设备故障诊断与预测维护智能体系统**✨

- 功能集成：故障图像识别 + 文本诊断 + 大模型推理 + 智能体决策
- 涉及知识点：LSTM、YOLO、LLM、Prompt工程、多智能体
- 工作量：1800+行代码

**选项3：生产流程智能优化系统**✨

- 功能集成：生产调度 + 质量检测 + 多智能体优化 + 强化学习
- 涉及知识点：强化学习、计算机视觉、多智能体、系统优化
- 工作量：1600+行代码

**选项4：工业知识库问答与多模态诊断智能体**✨ **新增 - 大模型重点应用**

- 功能集成：RAG文档检索 + 大模型问答 + 图像分析 + 多步推理
- 涉及知识点：RAG、LLM、Prompt工程、多模态、思维链
- 工作量：1400+行代码

---

### （七）教学进度表

| 周次  | 课时  | 模块  | 学习内容                      | 工单项目        | 考核方式    |
| --- | --- | --- | ------------------------- | ----------- | ------- |
| 1   | 4   | M1  | 数据清洗、EDA                  | 数据清洗分析      | 代码演示+工单 |
| 2   | 4   | M1  | 特征工程、特征选择                 | 特征库设计       | 代码演示+工单 |
| 3   | 4   | M2  | 分类模型、评估指标                 | 故障分类预测      | 代码演示+工单 |
| 4   | 4   | M2  | XGBoost、集成学习              | 故障分类预测      | 代码演示+工单 |
| 5   | 4   | M2  | 神经网络、CNN基础、Transformer基础  | 深度学习模型      | 代码演示+工单 |
| 6   | 4   | M2  | LSTM、大模型原理                | 深度学习模型      | 代码演示+工单 |
| 7   | 4   | M3  | 图像分类、迁移学习                 | 缺陷检测系统      | 代码演示+工单 |
| 8   | 4   | M3  | 物体检测、视觉大模型                | 缺陷检测系统      | 代码演示+工单 |
| 9   | 4   | M4  | NLP基础、LLM调用               | 多模态分析系统     | 代码演示+工单 |
| 10  | 4   | M4  | **Prompt工程、RAG系统、多智能体基础** | **多模态分析系统** | 代码演示+工单 |
| 11  | 4   | M5  | **多智能体设计、强化学习、智能体训练**     | **智能体系统**   | 代码演示+工单 |
| 12  | 4   | M5  | 综合项目答辩、系统集成               | 综合项目答辩      | 项目演示+答辩 |

---

## 四、课程实施保障条件

### （一）实训条件

1. **硬件配置**
   
   - CPU：i7+ / Ryzen 7+（推荐）
   - 内存：16GB+
   - GPU：NVIDIA RTX 2060+ 或 A100（用于深度学习加速）
   - 网络：100Mbps+（用于调用云端LLM API）

2. **软件环境**
   
   - Python 3.9+
   - TensorFlow 2.10+ 或 PyTorch 2.0+
   - 库：scikit-learn、xgboost、opencv、librosa、transformers、langchain、openai等
   - IDE：Jupyter Lab（推荐用于深度学习与大模型实验）

3. **数据与模型资源**
   
   - 工业图像数据集（产品、缺陷等）
   - 预训练模型（ResNet、YOLO、BERT、LLM等）
   - LLM API密钥（OpenAI、Claude、Hugging Face等）
   - 技术文档库（用于RAG系统训练）

### （二）教学团队

1. **教师要求**
   
   - 教学经验：≥3年深度学习或AI实战经验
   - 技能：精通TensorFlow/PyTorch、计算机视觉、NLP、**大模型应用、多智能体系统**
   - 工业背景：理解工业应用场景
   - **大模型经验**：有实际调用LLM API、Prompt工程、RAG系统开发经验

2. **企业导师**
   
   - AI算法工程师参与案例设计
   - 大模型应用经验分享
   - 工业AI系统集成经验

### （三）学习资源

1. **在线平台**
   
   - TensorFlow/PyTorch官方教程
   - Hugging Face模型库与文档
   - **OpenAI API文档与最佳实践**
   - **LangChain文档（RAG与智能体框架）**
   - Kaggle数据竞赛与解决方案

2. **工业数据集**
   
   - 开源：MIT-BIH心电图、工业故障数据集等
   - 公司数据：脱敏后的真实工业数据

---

## 五、学习评价

### （一）过程性评价（80%）

| 评价维度     | 权重  | 满分     | 评价标准                                                   |
| -------- | --- | ------ | ------------------------------------------------------ |
| **出勤率**  | 10% | 100    | 缺课≤10%为满分                                              |
| **课中表现** | 15% | 100    | 积极参与、能解释模型、代码演示清晰、**能解释大模型决策**                         |
| **工单任务** | 55% | 100/任务 | 功能完整≥80%、代码规范≥90% PEP8、**模型性能达基准值**、文档完整、**展示大模型应用价值** |

### （二）终结性评价（20%）

| 评价方式     | 权重   | 满分  | 评价标准                               |
| -------- | ---- | --- | ---------------------------------- |
| **综合项目** | 100% | 100 | 需求分析、模型设计、**智能体架构**、性能指标、文档与答辩、创新性 |

### （三）模型性能基准值

| 工单项目           | 评估指标       | 合格线       | 良好线       | 优秀线       |
| -------------- | ---------- | --------- | --------- | --------- |
| M2.1 分类        | F1分数       | ≥0.70     | ≥0.80     | ≥0.90     |
| M2.2 CNN       | 精确度        | ≥0.75     | ≥0.85     | ≥0.95     |
| M2.2 LSTM      | RMSE相对误差   | ≤15%      | ≤10%      | ≤5%       |
| M3 缺陷检测        | mAP        | ≥0.65     | ≥0.75     | ≥0.85     |
| **M3 视觉大模型**   | **零样本准确率** | **≥0.70** | **≥0.80** | **≥0.90** |
| M4 文本分类        | 精确度        | ≥0.75     | ≥0.85     | ≥0.95     |
| **M4 RAG系统**   | **检索准确率**  | **≥0.75** | **≥0.85** | **≥0.95** |
| **M4 智能体工具调用** | **正确率**    | **≥0.80** | **≥0.90** | **≥0.98** |
| M4 语音识别        | 字错率        | ≤20%      | ≤15%      | ≤10%      |
| M5 强化学习        | 改进率        | ≥30%      | ≥50%      | ≥70%      |
| **M5 多智能体**    | **协调正确率**  | **≥0.75** | **≥0.85** | **≥0.95** |

### （四）通过标准

**及格（60分）**：

- 缺课≤10%
- ≥70%工单完成度≥60%
- 至少2个工单达到模型性能合格线
- **至少1个工单涉及大模型或智能体应用**
- 综合成绩≥60分

**良好（80-89分）**：

- 缺课≤5%
- ≥80%工单完成度≥80%
- 至少3个工单达到模型性能良好线
- **至少2个工单涉及大模型、Prompt、RAG或多智能体应用，性能良好**
- 综合成绩≥80分

**优秀（90分及以上）**：

- 全勤或缺课≤1次
- 100%工单完成度≥85%
- ≥4个工单达到模型性能优秀线
- **综合项目创新性强，展现深度的大模型与多智能体应用**
- **综合项目中至少涉及RAG、Prompt工程、多智能体协调中的两项**
- 综合成绩≥90分

---

**文档版本**：3.0（v3.0 融合大模型与智能体版本）
**最后更新**：2026年8月
**核心新增**：

- ✨ 大模型（LLM）原理与应用
- ✨ Prompt工程与提示词优化
- ✨ RAG（检索增强生成）系统
- ✨ 思维链（Chain-of-Thought）推理
- ✨ 智能体架构与工具调用
- ✨ 多智能体系统设计
- ✨ 多模态视觉大模型应用
- ✨ 语音大模型应用
- ✨ 工业决策支持系统