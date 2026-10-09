# 文献、网站、引用和精读

## 常用入口与用途

| 来源 | 用途 |
| --- | --- |
| [arXiv](https://arxiv.org/) | 前沿预印本、版本、公开全文；发表状态另外核实 |
| [GitHub](https://github.com/) | 官方实现、数据处理、配置与提交版本 |
| [OpenReview](https://openreview.net/) | 投稿版本、会议状态、公开评审与讨论 |
| [DOI](https://doi.org/) | 稳定标识与出版社落地页 |
| [ResearchGate](https://www.researchgate.net/) | 全文线索；关键元数据回到原出版来源核实 |
| [ScienceDirect](https://www.sciencedirect.com/) | 期刊原文与正式元数据 |
| [Hugging Face](https://huggingface.co/) | 模型、数据集卡、版本与使用说明 |
| [Springer](https://link.springer.com/) | 原出版页与论文全文 |
| [DBLP](https://dblp.org/) | 计算机论文的作者、会议与出版记录 |
| [Nature](https://www.nature.com/) | 原文、补充与科学图表参照 |
| [IEEE Xplore](https://ieeexplore.ieee.org/) | 通信、雷达、卫星、生医工原出版记录 |
| [PMLR](https://proceedings.mlr.press/) | 机器学习会议正式论文与补充材料 |
| [CVF Open Access](https://openaccess.thecvf.com/) | 计算机视觉会议原文与视觉参照 |
| [Zenodo](https://zenodo.org/) | 数据、代码与版本记录 |
| [ACL Anthology](https://aclanthology.org/) | NLP/LLM 原文、会议与元数据 |
| [NeurIPS Proceedings](https://proceedings.neurips.cc/) | 正式论文与补充 |
| [MOABB](https://moabb.neurotechx.com/) | EEG 数据集、协议与基线实现 |
| [TorchEEG 文档](https://torcheeg.readthedocs.io/) | EEG 数据适配与模型接口 |

其他可用来源包括 PubMed/PMC、alphaXiv、SciSpace、papers.cool、DeepSig、IEEE DataPort。用于发现后回到原论文、官方数据页与代码；不要把自动总结当作已读原文。

补充工具：Crossref/OpenAlex/Semantic Scholar 可用于元数据、引用网络或批量发现。

## 检索策略

先写问题实体、任务、数据类型、约束、机制和评价量，组合关键词。并行搜索问题名、近义词、机制、最近邻作者和指定 venue；经典奠基、最近两三年进展、公开数据/代码分别查，再交叉回引与前向被引。

Google Scholar 支持标题引号检索、作者检索、相关论文/被引与引用导出；用它发现记录，关键引用对回原出版来源。[官方检索帮助](https://scholar.google.com/intl/en/scholar/help.html)。出现验证码或访问限制不循环硬刷；记录不可访问并换官方出版页、DBLP 或元数据接口。替代检索不冒称完成了 Scholar 核查。

建立最近邻矩阵：问题、机制、输入输出、数据、协议、关键结论、条件、代码、与你的重叠、真正未解决的缺口。相关性优先，高引与最新可靠论文互补；不能因为没找到就宣布“首个”。结果饱和到足以决策后推进实验，不无止境搜索。

## 引用逐条核对

核对标题、作者顺序、年份、正式 venue、卷期页码或文章号、DOI、预印本版本和撤稿/更正情况。出版年与 online-first 年可能不同；没有 DOI 的真实文献保留可靠入口，不造 DOI。Crossref REST API 可检索出版元数据，返回内容还要与实际引用版本核对。[官方接口说明](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)。

每条记录保存 cite key、主来源 URL、核实日期、状态、版本、验证笔记路径。状态为 `verified / partial / unresolved / excluded`。verified 要有实际核查笔记，不能只写一个布尔值。某篇存在不代表它支持当前句子：额外记录支撑的段落、图号、页码及适用条件。

替换虚构或不相关引用时，检查整句是否仍被新文献支持；必要时重写主张。引用要承担论证功能，删掉“引用了但没用”的条目。缺 PDF 先找作者主页、arXiv、机构仓储和开放出版版本，保存版本说明，不能把未读摘要当全文。

## Zotero 和论文网

按问题/系统节点/方法建立分类，条目可有多个标签。避免预印本与正式版变成两篇统计；建立版本关系。用 DOI、arXiv ID、标题与作者联合去重；元数据模糊匹配只产生待确认候选。

条目笔记包含问题、输入输出、核心机制、关键公式、数据协议、图表索引、复现入口、适用边界和先修论文。架构图节点关联“系统问题 → 核心模块 → 必读/先修论文 → 可复现切入点”。需要时导出 BibTeX、清单和离线 HTML，验证迁移后仍能定位来源。

Zotero 可通过本地工具或 Web API 读取管理条目，写权限由当前环境授权；API 密钥与账户由使用者自行配置，不随本 skill 打包。[官方 Web API 文档](https://www.zotero.org/support/dev/web_api/v3/)。没有 Zotero 就用本地 BibTeX/JSONL 与笔记，不因此停下科研。

## 论文与代码精读格式

逐段提取原文主张、你的通俗解释和证据位置，明确作者结果、你复现的结果、推断与设想。重点回答：解决什么问题，旧方法为何不够，为什么这样设计，什么条件成立，什么证据真正支撑。

代码对照必须做到：原始数据 → 划分 → 预处理 → 张量形状/单位 → 每层操作 → 损失 → 优化 → checkpoint 选择 → 指标。网络解释追到实际 kernel、stride、padding、reshape、残差、归一化和梯度路径；不要只报层名字。公式说明所有变量、维度与假设，必要时用小输入手算。

复现核对 commit、配置、环境、数据版本、split、seed、运行命令、预处理与原始日志。源码发现的问题只支持“当前公开实现存在问题”；若没有生成论文数字的确切版本，不能断言论文全部结果同样有误。
