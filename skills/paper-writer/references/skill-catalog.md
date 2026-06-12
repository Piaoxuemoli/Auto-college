# Skill Catalog

> 233 skills organized by tier for efficient retrieval
> Tier 1 (Core): always loaded | Tier 2 (Domain): topic-matched | Tier 3 (Utility): need-matched

---

## TIER 1: CORE SKILLS (Always Loaded)

These skills are loaded for **every** paper-writing task regardless of topic.

| Skill | Description | Path |
|-------|-------------|------|
| scientific-writing | Core skill for the deep research and writing tool. Write scientific manuscripts in full paragraphs (never bullet points). Use two-stage process with ( | `skills/scientific-writing/SKILL.md` |
| citation-management | Comprehensive citation management for academic research. Search Google Scholar and PubMed for papers, extract accurate metadata, validate citations, a | `skills/citation-management/SKILL.md` |
| literature-review | Conduct comprehensive, systematic literature reviews using multiple academic databases (PubMed, arXiv, bioRxiv, Semantic Scholar, etc.). This skill sh | `skills/literature-review/SKILL.md` |
| paper-lookup | Search 10 academic paper databases via REST APIs for research papers, preprints, and scholarly articles. Covers PubMed, PMC (full text), bioRxiv, medR | `skills/paper-lookup/SKILL.md` |
| peer-review | Structured manuscript/grant review with checklist-based evaluation. Use when writing formal peer reviews with specific criteria methodology assessment | `skills/peer-review/SKILL.md` |
| compiler | Compiles any research input — PDF papers, GitHub repositories, experiment logs, code directories, or raw notes — into a complete Agent-Native Research | `skills/compiler/SKILL.md` |
| venue-templates | Access comprehensive LaTeX templates, formatting requirements, and submission guidelines for major scientific publication venues (Nature, Science, PLO | `skills/venue-templates/SKILL.md` |
| database-lookup | Search 78 public scientific, biomedical, materials science, and economic databases via REST APIs. Covers physics/astronomy (NASA, NIST, SDSS, SIMBAD), | `skills/database-lookup/SKILL.md` |
| research-lookup | Look up current research information using parallel-cli search (primary, fast web search), the Parallel Chat API (deep research), or Perplexity sonar- | `skills/research-lookup/SKILL.md` |
| scientific-brainstorming | Creative research ideation and exploration. Use for open-ended brainstorming sessions, exploring interdisciplinary connections, challenging assumption | `skills/scientific-brainstorming/SKILL.md` |

---

## TIER 2: DOMAIN SKILLS (Topic-Matched)

Match the paper topic against domain keywords. Load ALL skills from matching domain(s).
A paper may match multiple domains (e.g. "deep learning for protein structure" matches both ML/AI and Biology).

### ML/AI & Machine Learning
**Keywords:** machine learning, deep learning, neural network, transformer, LLM, NLP, computer vision, reinforcement learning, fine-tuning, training, inference, AI, GPT, diffusion, RLHF, LoRA, quantization, PyTorch, RAG, agent
**Count:** 96

#### Training & Infrastructure (37)
| Skill | Description | Path |
|-------|-------------|------|
| accelerate | Simplest distributed training API. 4 lines to add distributed support to any PyTorch script. Unified API for DeepSpeed/FSDP/Megatron/DDP. Automatic de | `skills/accelerate/SKILL.md` |
| awq | Activation-aware weight quantization for 4-bit LLM compression with 3x speedup and minimal accuracy loss. Use when deploying large models (7B-70B) on  | `skills/awq/SKILL.md` |
| axolotl | Expert guidance for fine-tuning LLMs with Axolotl - YAML configs, 100+ models, LoRA/QLoRA, DPO/KTO/ORPO/GRPO, multimodal support | `skills/axolotl/SKILL.md` |
| bitsandbytes | Quantizes LLMs to 8-bit or 4-bit for 50-75% memory reduction with minimal accuracy loss. Use when GPU memory is limited, need to fit larger models, or | `skills/bitsandbytes/SKILL.md` |
| deepspeed | Expert guidance for distributed training with DeepSpeed - ZeRO optimization stages, pipeline parallelism, FP16/BF16/FP8, 1-bit Adam, sparse attention | `skills/deepspeed/SKILL.md` |
| flash-attention | Optimizes transformer attention with Flash Attention for 2-4x speedup and 10-20x memory reduction. Use when training/running transformers with long se | `skills/flash-attention/SKILL.md` |
| gptq | Post-training 4-bit quantization for LLMs with minimal accuracy loss. Use for deploying large models (70B, 405B) on consumer GPUs, when you need 4× me | `skills/gptq/SKILL.md` |
| grpo-rl-training | Expert guidance for GRPO/RL fine-tuning with TRL for reasoning and task-specific model training | `skills/grpo-rl-training/SKILL.md` |
| hqq | Half-Quadratic Quantization for LLMs without calibration data. Use when quantizing models to 4/3/2-bit precision without needing calibration datasets, | `skills/hqq/SKILL.md` |
| knowledge-distillation | Compress large language models using knowledge distillation from teacher to student models. Use when deploying smaller models with retained performanc | `skills/knowledge-distillation/SKILL.md` |
| litgpt | Implements and trains LLMs using Lightning AI's LitGPT with 20+ pretrained architectures (Llama, Gemma, Phi, Qwen, Mistral). Use when need clean model | `skills/litgpt/SKILL.md` |
| llama-factory | Expert guidance for fine-tuning LLMs with LLaMA-Factory - WebUI no-code, 100+ models, 2/3/4/5/6/8-bit QLoRA, multimodal support | `skills/llama-factory/SKILL.md` |
| long-context | Extend context windows of transformer models using RoPE, YaRN, ALiBi, and position interpolation techniques. Use when processing long documents (32k-1 | `skills/long-context/SKILL.md` |
| mamba | State-space model with O(n) complexity vs Transformers' O(n²). 5× faster inference, million-token sequences, no KV cache. Selective SSM with hardware- | `skills/mamba/SKILL.md` |
| megatron-core | Trains large language models (2B-462B parameters) using NVIDIA Megatron-Core with advanced parallelism strategies. Use when training models >1B parame | `skills/megatron-core/SKILL.md` |
| miles | Provides guidance for enterprise-grade RL training using miles, a production-ready fork of slime. Use when training large MoE models with FP8/INT4, ne | `skills/miles/SKILL.md` |
| ml-training-recipes | Battle-tested PyTorch training recipes for all domains — LLMs, vision, diffusion, medical imaging, protein/drug discovery, spatial omics, genomics. Co | `skills/ml-training-recipes/SKILL.md` |
| model-merging | Merge multiple fine-tuned models using mergekit to combine capabilities without retraining. Use when creating specialized models by blending domain-sp | `skills/model-merging/SKILL.md` |
| model-pruning | Reduce LLM size and accelerate inference using pruning techniques like Wanda and SparseGPT. Use when compressing models without retraining, achieving  | `skills/model-pruning/SKILL.md` |
| moe-training | Train Mixture of Experts (MoE) models using DeepSpeed or HuggingFace. Use when training large-scale models with limited compute (5× cost reduction vs  | `skills/moe-training/SKILL.md` |
| nanogpt | Educational GPT implementation in ~300 lines. Reproduces GPT-2 (124M) on OpenWebText. Clean, hackable code for learning transformers. By Andrej Karpat | `skills/nanogpt/SKILL.md` |
| nemo-curator | GPU-accelerated data curation for LLM training. Supports text/image/video/audio. Features fuzzy deduplication (16× faster), quality filtering (30+ heu | `skills/nemo-curator/SKILL.md` |
| openrlhf | High-performance RLHF framework with Ray+vLLM acceleration. Use for PPO, GRPO, RLOO, DPO training of large models (7B-70B+). Built on Ray, vLLM, ZeRO- | `skills/openrlhf/SKILL.md` |
| peft | Parameter-efficient fine-tuning for LLMs using LoRA, QLoRA, and 25+ methods. Use when fine-tuning large models (7B-70B) with limited GPU memory, when  | `skills/peft/SKILL.md` |
| pytorch-fsdp2 | Adds PyTorch FSDP2 (fully_shard) to training scripts with correct init, sharding, mixed precision/offload config, and distributed checkpointing. Use w | `skills/pytorch-fsdp2/SKILL.md` |
| pytorch-lightning | Deep learning framework (PyTorch Lightning). Organize PyTorch code into LightningModules, configure Trainers for multi-GPU/TPU, implement data pipelin | `skills/pytorch-lightning/SKILL.md` |
| rwkv | RNN+Transformer hybrid with O(n) inference. Linear time, infinite context, no KV cache. Train like GPT (parallel), infer like RNN (sequential). Linux  | `skills/rwkv/SKILL.md` |
| simpo | Simple Preference Optimization for LLM alignment. Reference-free alternative to DPO with better performance (+6.4 points on AlpacaEval 2.0). No refere | `skills/simpo/SKILL.md` |
| slime | Provides guidance for LLM post-training with RL using slime, a Megatron+SGLang framework. Use when training GLM models, implementing custom data gener | `skills/slime/SKILL.md` |
| speculative-decoding | Accelerate LLM inference using speculative decoding, Medusa multiple heads, and lookahead decoding techniques. Use when optimizing inference speed (1. | `skills/speculative-decoding/SKILL.md` |
| tensorrt-llm | Optimizes LLM inference with NVIDIA TensorRT for maximum throughput and lowest latency. Use for production deployment on NVIDIA GPUs (A100/H100), when | `skills/tensorrt-llm/SKILL.md` |
| torchforge | Provides guidance for PyTorch-native agentic RL using torchforge, Meta's library separating infra from algorithms. Use when you want clean RL abstract | `skills/torchforge/SKILL.md` |
| torchtitan | Provides PyTorch-native distributed LLM pretraining using torchtitan with 4D parallelism (FSDP2, TP, PP, CP). Use when pretraining Llama 3.1, DeepSeek | `skills/torchtitan/SKILL.md` |
| trl-fine-tuning | Fine-tune LLMs using reinforcement learning with TRL - SFT for instruction tuning, DPO for preference alignment, PPO/GRPO for reward optimization, and | `skills/trl-fine-tuning/SKILL.md` |
| unsloth | Expert guidance for fast fine-tuning with Unsloth - 2-5x faster training, 50-80% less memory, LoRA/QLoRA optimization | `skills/unsloth/SKILL.md` |
| verl | Provides guidance for training LLMs with reinforcement learning using verl (Volcano Engine RL). Use when implementing RLHF, GRPO, PPO, or other RL alg | `skills/verl/SKILL.md` |
| vllm | Serves LLMs with high throughput using vLLM's PagedAttention and continuous batching. Use when deploying production LLM APIs, optimizing inference lat | `skills/vllm/SKILL.md` |

#### Evaluation & Interpretability (8)
| Skill | Description | Path |
|-------|-------------|------|
| bigcode-evaluation-harness | Evaluates code generation models across HumanEval, MBPP, MultiPL-E, and 15+ benchmarks with pass@k metrics. Use when benchmarking code models, compari | `skills/bigcode-evaluation-harness/SKILL.md` |
| lm-evaluation-harness | Evaluates LLMs across 60+ academic benchmarks (MMLU, HumanEval, GSM8K, TruthfulQA, HellaSwag). Use when benchmarking model quality, comparing models,  | `skills/lm-evaluation-harness/SKILL.md` |
| nemo-evaluator | Evaluates LLMs across 100+ benchmarks from 18+ harnesses (MMLU, HumanEval, GSM8K, safety, VLM) with multi-backend execution. Use when needing scalable | `skills/nemo-evaluator/SKILL.md` |
| nnsight | Provides guidance for interpreting and manipulating neural network internals using nnsight with optional NDIF remote execution. Use when needing to ru | `skills/nnsight/SKILL.md` |
| pyvene | Provides guidance for performing causal interventions on PyTorch models using pyvene's declarative intervention framework. Use when conducting causal  | `skills/pyvene/SKILL.md` |
| saelens | Provides guidance for training and analyzing Sparse Autoencoders (SAEs) using SAELens to decompose neural network activations into interpretable featu | `skills/saelens/SKILL.md` |
| shap | Model interpretability and explainability using SHAP (SHapley Additive exPlanations). Use this skill when explaining machine learning model prediction | `skills/shap/SKILL.md` |
| transformer-lens | Provides guidance for mechanistic interpretability research using TransformerLens to inspect and manipulate transformer internals via HookPoints and a | `skills/transformer-lens/SKILL.md` |

#### Applications & Models (16)
| Skill | Description | Path |
|-------|-------------|------|
| aeon | This skill should be used for time series machine learning tasks including classification, regression, clustering, forecasting, anomaly detection, seg | `skills/aeon/SKILL.md` |
| audiocraft | PyTorch library for audio generation including text-to-music (MusicGen) and text-to-sound (AudioGen). Use when you need to generate music from text de | `skills/audiocraft/SKILL.md` |
| blip-2 | Vision-language pre-training framework bridging frozen image encoders and LLMs. Use when you need image captioning, visual question answering, image-t | `skills/blip-2/SKILL.md` |
| clip | OpenAI's model connecting vision and language. Enables zero-shot image classification, image-text matching, and cross-modal retrieval. Trained on 400M | `skills/clip/SKILL.md` |
| cosmos-policy | Evaluates NVIDIA Cosmos Policy on LIBERO and RoboCasa simulation environments. Use when setting up cosmos-policy for robot manipulation evaluation, ru | `skills/cosmos-policy/SKILL.md` |
| hugging-science | Use when the user is doing AI/ML work in a scientific domain — biology, chemistry, physics, astronomy, climate, genomics, materials science, medicine, | `skills/hugging-science/SKILL.md` |
| llava | Large Language and Vision Assistant. Enables visual instruction tuning and image-based conversations. Combines CLIP vision encoder with Vicuna/LLaMA l | `skills/llava/SKILL.md` |
| openpi | Fine-tune and serve Physical Intelligence OpenPI models (pi0, pi0-fast, pi0.5) using JAX or PyTorch backends for robot policy inference across ALOHA,  | `skills/openpi/SKILL.md` |
| openvla-oft | Fine-tunes and evaluates OpenVLA-OFT and OpenVLA-OFT+ policies for robot action generation with continuous action heads, LoRA adaptation, and FiLM con | `skills/openvla-oft/SKILL.md` |
| pufferlib | High-performance reinforcement learning framework optimized for speed and scale. Use when you need fast parallel training, vectorized environments, mu | `skills/pufferlib/SKILL.md` |
| segment-anything | Foundation model for image segmentation with zero-shot transfer. Use when you need to segment any object in images using points, boxes, or masks as pr | `skills/segment-anything/SKILL.md` |
| stable-baselines3 | Production-ready reinforcement learning algorithms (PPO, SAC, DQN, TD3, DDPG, A2C) with scikit-learn-like API. Use for standard RL experiments, quick  | `skills/stable-baselines3/SKILL.md` |
| stable-diffusion | State-of-the-art text-to-image generation with Stable Diffusion models via HuggingFace Diffusers. Use when generating images from text prompts, perfor | `skills/stable-diffusion/SKILL.md` |
| timesfm-forecasting | Zero-shot time series forecasting with Google's TimesFM foundation model. Use for any univariate time series (sales, sensors, energy, vitals, weather) | `skills/timesfm-forecasting/SKILL.md` |
| torch-geometric | "Guide for building Graph Neural Networks with PyTorch Geometric (PyG). Use this skill whenever the user asks about graph neural networks, GNNs, node  | `skills/torch-geometric/SKILL.md` |
| whisper | OpenAI's general-purpose speech recognition model. Supports 99 languages, transcription, translation to English, and language identification. Six mode | `skills/whisper/SKILL.md` |

#### Tools & Agents (16)
| Skill | Description | Path |
|-------|-------------|------|
| autogpt | Autonomous AI agent platform for building and deploying continuous agents. Use when creating visual workflow agents, deploying persistent autonomous a | `skills/autogpt/SKILL.md` |
| crewai | Multi-agent orchestration framework for autonomous AI collaboration. Use when building teams of specialized agents working together on complex tasks,  | `skills/crewai/SKILL.md` |
| dspy | Build complex AI systems with declarative programming, optimize prompts automatically, create modular RAG systems and agents with DSPy - Stanford NLP' | `skills/dspy/SKILL.md` |
| guidance | Control LLM output with regex and grammars, guarantee valid JSON/XML/code generation, enforce structured formats, and build multi-step workflows with  | `skills/guidance/SKILL.md` |
| huggingface-tokenizers | Fast tokenizers optimized for research and production. Rust-based implementation tokenizes 1GB in <20 seconds. Supports BPE, WordPiece, and Unigram al | `skills/huggingface-tokenizers/SKILL.md` |
| instructor | Extract structured data from LLM responses with Pydantic validation, retry failed extractions automatically, parse complex JSON with type safety, and  | `skills/instructor/SKILL.md` |
| langchain | Framework for building LLM-powered applications with agents, chains, and RAG. Supports multiple providers (OpenAI, Anthropic, Google), 500+ integratio | `skills/langchain/SKILL.md` |
| langsmith | LLM observability platform for tracing, evaluation, and monitoring. Use when debugging LLM applications, evaluating model outputs against datasets, mo | `skills/langsmith/SKILL.md` |
| llama-cpp | Runs LLM inference on CPU, Apple Silicon, and consumer GPUs without NVIDIA hardware. Use for edge deployment, M1/M2/M3 Macs, AMD/Intel GPUs, or when C | `skills/llama-cpp/SKILL.md` |
| llamaguard | Meta's 7-8B specialized moderation model for LLM input/output filtering. 6 safety categories - violence/hate, sexual content, weapons, substances, sel | `skills/llamaguard/SKILL.md` |
| llamaindex | Data framework for building LLM applications with RAG. Specializes in document ingestion (300+ connectors), indexing, and querying. Features vector in | `skills/llamaindex/SKILL.md` |
| outlines | Guarantee valid JSON/XML/code structure during generation, use Pydantic models for type-safe outputs, support local models (Transformers, vLLM), and m | `skills/outlines/SKILL.md` |
| prompt-guard | Meta's 86M prompt injection and jailbreak detector. Filters malicious prompts and third-party data for LLM apps. 99%+ TPR, <1% FPR. Fast (<2ms GPU). M | `skills/prompt-guard/SKILL.md` |
| sentence-transformers | Framework for state-of-the-art sentence, text, and image embeddings. Provides 5000+ pre-trained models for semantic similarity, clustering, and retrie | `skills/sentence-transformers/SKILL.md` |
| sentencepiece | Language-independent tokenizer treating text as raw Unicode. Supports BPE and Unigram algorithms. Fast (50k sentences/sec), lightweight (6MB memory),  | `skills/sentencepiece/SKILL.md` |
| transformers | This skill should be used when working with pre-trained transformer models for natural language processing, computer vision, audio, or multimodal task | `skills/transformers/SKILL.md` |

#### Infrastructure & Tracking (17)
| Skill | Description | Path |
|-------|-------------|------|
| chroma | Open-source embedding database for AI applications. Store embeddings and metadata, perform vector and full-text search, filter by metadata. Simple 4-f | `skills/chroma/SKILL.md` |
| faiss | Facebook's library for efficient similarity search and clustering of dense vectors. Supports billions of vectors, GPU acceleration, and various index  | `skills/faiss/SKILL.md` |
| gguf | GGUF format and llama.cpp quantization for efficient CPU/GPU inference. Use when deploying models on consumer hardware, Apple Silicon, or when needing | `skills/gguf/SKILL.md` |
| lambda-labs | Reserved and on-demand GPU cloud instances for ML training and inference. Use when you need dedicated GPU instances with simple SSH access, persistent | `skills/lambda-labs/SKILL.md` |
| mlflow | Track ML experiments, manage model registry with versioning, deploy models to production, and reproduce experiments with MLflow - framework-agnostic M | `skills/mlflow/SKILL.md` |
| modal | Cloud computing platform for running Python on GPUs and serverless infrastructure. Use when deploying AI/ML models, running GPU-accelerated workloads, | `skills/modal/SKILL.md` |
| nemo-guardrails | NVIDIA's runtime safety framework for LLM applications. Features jailbreak detection, input/output validation, fact-checking, hallucination detection, | `skills/nemo-guardrails/SKILL.md` |
| phoenix | Open-source AI observability platform for LLM tracing, evaluation, and monitoring. Use when debugging LLM applications with detailed traces, running e | `skills/phoenix/SKILL.md` |
| pinecone | Managed vector database for production AI applications. Fully managed, auto-scaling, with hybrid search (dense + sparse), metadata filtering, and name | `skills/pinecone/SKILL.md` |
| qdrant | High-performance vector similarity search engine for RAG and semantic search. Use when building production RAG systems requiring fast nearest neighbor | `skills/qdrant/SKILL.md` |
| ray-data | Scalable data processing for ML workloads. Streaming execution across CPU/GPU, supports Parquet/CSV/JSON/images. Integrates with Ray Train, PyTorch, T | `skills/ray-data/SKILL.md` |
| ray-train | Distributed training orchestration across clusters. Scales PyTorch/TensorFlow/HuggingFace from laptop to 1000s of nodes. Built-in hyperparameter tunin | `skills/ray-train/SKILL.md` |
| sglang | Fast structured generation and serving for LLMs with RadixAttention prefix caching. Use for JSON/regex outputs, constrained decoding, agentic workflow | `skills/sglang/SKILL.md` |
| skypilot | Multi-cloud orchestration for ML workloads with automatic cost optimization. Use when you need to run training or batch jobs across multiple clouds, l | `skills/skypilot/SKILL.md` |
| swanlab | Provides guidance for experiment tracking with SwanLab. Use when you need open-source run tracking, local or self-hosted dashboards, and lightweight m | `skills/swanlab/SKILL.md` |
| tensorboard | Visualize training metrics, debug models with histograms, compare experiments, visualize model graphs, and profile performance with TensorBoard - Goog | `skills/tensorboard/SKILL.md` |
| weights-and-biases | Track ML experiments with automatic logging, visualize training in real-time, optimize hyperparameters with sweeps, and manage model registry with W&B | `skills/weights-and-biases/SKILL.md` |

#### ML Paper Writing (1)
| Skill | Description | Path |
|-------|-------------|------|
| ml-paper-writing | Write publication-ready ML/AI papers for NeurIPS, ICML, ICLR, ACL, AAAI, COLM. Use when drafting papers from research repos, structuring arguments, ve | `skills/ml-paper-writing/SKILL.md` |

#### Safety & Alignment (1)
| Skill | Description | Path |
|-------|-------------|------|
| constitutional-ai | Anthropic's method for training harmless AI through self-improvement. Two-phase approach - supervised learning with self-critique/revision, then RLAIF | `skills/constitutional-ai/SKILL.md` |

### Biology & Bioinformatics
**Keywords:** biology, bioinformatics, genomics, proteomics, RNA, DNA, gene, protein, cell, single-cell, phylogenetics, sequence, FASTA, CRISPR, metabolomics, omics
**Count:** 35

| Skill | Description | Path |
|-------|-------------|------|
| anndata | Data structure for annotated matrices in single-cell analysis. Use when working with .h5ad files or integrating with the scverse ecosystem. This is th | `skills/anndata/SKILL.md` |
| arboreto | Infer gene regulatory networks (GRNs) from gene expression data using scalable algorithms (GRNBoost2, GENIE3). Use when analyzing transcriptomics data | `skills/arboreto/SKILL.md` |
| benchling-integration | Benchling R&D platform integration. Access registry (DNA, proteins), inventory, ELN entries, workflows via API, build Benchling Apps, query Data Wareh | `skills/benchling-integration/SKILL.md` |
| biopython | Comprehensive molecular biology toolkit. Use for sequence manipulation, file parsing (FASTA/GenBank/PDB), phylogenetics, and programmatic NCBI/PubMed  | `skills/biopython/SKILL.md` |
| bioservices | Unified Python interface to 40+ bioinformatics services. Use when querying multiple databases (UniProt, KEGG, ChEMBL, Reactome) in a single workflow w | `skills/bioservices/SKILL.md` |
| cellxgene-census | Query the CELLxGENE Census (61M+ cells) programmatically. Use when you need expression data across tissues, diseases, or cell types from the largest c | `skills/cellxgene-census/SKILL.md` |
| cobrapy | Constraint-based metabolic modeling (COBRA). FBA, FVA, gene knockouts, flux sampling, SBML models, for systems biology and metabolic engineering analy | `skills/cobrapy/SKILL.md` |
| deeptools | NGS analysis toolkit. BAM to bigWig conversion, QC (correlation, PCA, fingerprints), heatmaps/profiles (TSS, peaks), for ChIP-seq, RNA-seq, ATAC-seq v | `skills/deeptools/SKILL.md` |
| dnanexus-integration | DNAnexus cloud genomics platform. Build apps/applets, manage data (upload/download), dxpy Python SDK, run workflows, FASTQ/BAM/VCF, for genomics pipel | `skills/dnanexus-integration/SKILL.md` |
| esm | Comprehensive toolkit for protein language models including ESM3 (generative multimodal protein design across sequence, structure, and function) and E | `skills/esm/SKILL.md` |
| etetoolkit | Phylogenetic tree toolkit (ETE). Tree manipulation (Newick/NHX), evolutionary event detection, orthology/paralogy, NCBI taxonomy, visualization (PDF/S | `skills/etetoolkit/SKILL.md` |
| flowio | Parse FCS (Flow Cytometry Standard) files v2.0-3.1. Extract events as NumPy arrays, read metadata/channels, convert to CSV/DataFrame, for flow cytomet | `skills/flowio/SKILL.md` |
| geniml | This skill should be used when working with genomic interval data (BED files) for machine learning tasks. Use for training region embeddings (Region2V | `skills/geniml/SKILL.md` |
| gget | "Fast CLI/Python queries to 20+ bioinformatics databases. Use for quick lookups: gene info, BLAST searches, AlphaFold structures, enrichment analysis. | `skills/gget/SKILL.md` |
| ginkgo-cloud-lab | Submit and manage protocols on Ginkgo Bioworks Cloud Lab (cloud.ginkgo.bio), a web-based interface for autonomous lab execution on Reconfigurable Auto | `skills/ginkgo-cloud-lab/SKILL.md` |
| glycoengineering | Analyze and engineer protein glycosylation. Scan sequences for N-glycosylation sequons (N-X-S/T), predict O-glycosylation hotspots, and access curated | `skills/glycoengineering/SKILL.md` |
| gtars | High-performance toolkit for genomic interval analysis in Rust with Python bindings. Use when working with genomic regions, BED files, coverage tracks | `skills/gtars/SKILL.md` |
| histolab | Lightweight WSI tile extraction and preprocessing. Use for basic slide processing tissue detection, tile extraction, stain normalization for H&E image | `skills/histolab/SKILL.md` |
| labarchive-integration | Electronic lab notebook API integration. Access notebooks, manage entries/attachments, backup notebooks, integrate with Protocols.io/Jupyter/REDCap, f | `skills/labarchive-integration/SKILL.md` |
| lamindb | This skill should be used when working with LaminDB, an open-source data framework for biology that makes data queryable, traceable, reproducible, and | `skills/lamindb/SKILL.md` |
| latchbio-integration | Latch platform for bioinformatics workflows. Build pipelines with Latch SDK, @workflow/@task decorators, deploy serverless workflows, LatchFile/LatchD | `skills/latchbio-integration/SKILL.md` |
| omero-integration | Microscopy data management platform. Access images via Python, retrieve datasets, analyze pixels, manage ROIs/annotations, batch processing, for high- | `skills/omero-integration/SKILL.md` |
| opentrons-integration | Official Opentrons Protocol API for OT-2 and Flex robots. Use when writing protocols specifically for Opentrons hardware with full access to Protocol  | `skills/opentrons-integration/SKILL.md` |
| phylogenetics | Build and analyze phylogenetic trees using MAFFT (multiple alignment), IQ-TREE 2 (maximum likelihood), and FastTree (fast NJ/ML). Visualize with ETE3  | `skills/phylogenetics/SKILL.md` |
| polars-bio | High-performance genomic interval operations and bioinformatics file I/O on Polars DataFrames. Overlap, nearest, merge, coverage, complement, subtract | `skills/polars-bio/SKILL.md` |
| protocolsio-integration | Integration with protocols.io API for managing scientific protocols. This skill should be used when working with protocols.io to search, create, updat | `skills/protocolsio-integration/SKILL.md` |
| pylabrobot | Vendor-agnostic lab automation framework. Use when controlling multiple equipment types (Hamilton, Tecan, Opentrons, plate readers, pumps) or needing  | `skills/pylabrobot/SKILL.md` |
| pydeseq2 | Differential gene expression analysis (Python DESeq2). Identify DE genes from bulk RNA-seq counts, Wald tests, FDR correction, volcano/MA plots, for R | `skills/pydeseq2/SKILL.md` |
| pysam | Genomic file toolkit. Read/write SAM/BAM/CRAM alignments, VCF/BCF variants, FASTA/FASTQ sequences, extract regions, calculate coverage, for NGS data p | `skills/pysam/SKILL.md` |
| scanpy | Standard single-cell RNA-seq analysis pipeline. Use for QC, normalization, dimensionality reduction (PCA/UMAP/t-SNE), clustering, differential express | `skills/scanpy/SKILL.md` |
| scikit-bio | Biological data toolkit. Sequence analysis, alignments, phylogenetic trees, diversity metrics (alpha/beta, UniFrac), ordination (PCoA), PERMANOVA, FAS | `skills/scikit-bio/SKILL.md` |
| scvelo | RNA velocity analysis with scVelo. Estimate cell state transitions from unspliced/spliced mRNA dynamics, infer trajectory directions, compute latent t | `skills/scvelo/SKILL.md` |
| scvi-tools | Deep generative models for single-cell omics. Use when you need probabilistic batch correction (scVI), transfer learning, differential expression with | `skills/scvi-tools/SKILL.md` |
| tiledbvcf | Efficient storage and retrieval of genomic variant data using TileDB. Scalable VCF/BCF ingestion, incremental sample addition, compressed storage, par | `skills/tiledbvcf/SKILL.md` |
| zarr-python | Chunked N-D arrays for cloud storage. Compressed arrays, parallel I/O, S3/GCS integration, NumPy/Dask/Xarray compatible, for large-scale scientific co | `skills/zarr-python/SKILL.md` |

### Chemistry & Drug Discovery
**Keywords:** chemistry, drug discovery, molecule, molecular, SMILES, docking, ADMET, toxicity, compound, mass spectrometry, medicinal chemistry, pharmaceutical
**Count:** 14

| Skill | Description | Path |
|-------|-------------|------|
| adaptyv | "How to use the Adaptyv Bio Foundry API and Python SDK for protein experiment design, submission, and results retrieval. Use this skill whenever the u | `skills/adaptyv/SKILL.md` |
| datamol | Pythonic wrapper around RDKit with simplified interface and sensible defaults. Preferred for standard drug discovery including SMILES parsing, standar | `skills/datamol/SKILL.md` |
| deepchem | Molecular ML with diverse featurizers and pre-built datasets. Use for property prediction (ADMET, toxicity) with traditional ML or GNNs when you want  | `skills/deepchem/SKILL.md` |
| diffdock | Diffusion-based molecular docking. Predict protein-ligand binding poses from PDB/SMILES, confidence scores, virtual screening, for structure-based dru | `skills/diffdock/SKILL.md` |
| matchms | Spectral similarity and compound identification for metabolomics. Use for comparing mass spectra, computing similarity scores (cosine, modified cosine | `skills/matchms/SKILL.md` |
| medchem | Medicinal chemistry filters. Apply drug-likeness rules (Lipinski, Veber), PAINS filters, structural alerts, complexity metrics, for compound prioritiz | `skills/medchem/SKILL.md` |
| molfeat | Molecular featurization for ML (100+ featurizers). ECFP, MACCS, descriptors, pretrained models (ChemBERTa), convert SMILES to features, for QSAR and m | `skills/molfeat/SKILL.md` |
| molecular-dynamics | Run and analyze molecular dynamics simulations with OpenMM and MDAnalysis. Set up protein/small molecule systems, define force fields, run energy mini | `skills/molecular-dynamics/SKILL.md` |
| pymatgen | Materials science toolkit. Crystal structures (CIF, POSCAR), phase diagrams, band structure, DOS, Materials Project integration, format conversion, fo | `skills/pymatgen/SKILL.md` |
| pyopenms | Complete mass spectrometry analysis platform. Use for proteomics workflows feature detection, peptide identification, protein quantification, and comp | `skills/pyopenms/SKILL.md` |
| pytdc | Therapeutics Data Commons. AI-ready drug discovery datasets (ADME, toxicity, DTI), benchmarks, scaffold splits, molecular oracles, for therapeutic ML  | `skills/pytdc/SKILL.md` |
| rdkit | Cheminformatics toolkit for fine-grained molecular control. SMILES/SDF parsing, descriptors (MW, LogP, TPSA), fingerprints, substructure search, 2D/3D | `skills/rdkit/SKILL.md` |
| rowan | Rowan is a cloud-native molecular modeling and medicinal-chemistry workflow platform with a Python API. Use for pKa and macropKa prediction, conformer | `skills/rowan/SKILL.md` |
| torchdrug | PyTorch-native graph neural networks for molecules and proteins. Use when building custom GNN architectures for drug discovery, protein modeling, or k | `skills/torchdrug/SKILL.md` |

### Physics & Quantum Computing
**Keywords:** physics, quantum, simulation, fluid dynamics, astrophysics, astronomy, quantum computing, qubit, thermodynamic
**Count:** 7

| Skill | Description | Path |
|-------|-------------|------|
| astropy | Comprehensive Python library for astronomy and astrophysics. This skill should be used when working with astronomical data including celestial coordin | `skills/astropy/SKILL.md` |
| cirq | Google quantum computing framework. Use when targeting Google Quantum AI hardware, designing noise-aware circuits, or running quantum characterization | `skills/cirq/SKILL.md` |
| fluidsim | Framework for computational fluid dynamics simulations using Python. Use when running fluid dynamics simulations including Navier-Stokes equations (2D | `skills/fluidsim/SKILL.md` |
| pennylane | Hardware-agnostic quantum ML framework with automatic differentiation. Use when training quantum circuits via gradients, building hybrid quantum-class | `skills/pennylane/SKILL.md` |
| qiskit | IBM quantum computing framework. Use when targeting IBM Quantum hardware, working with Qiskit Runtime for production workloads, or needing IBM optimiz | `skills/qiskit/SKILL.md` |
| qutip | Quantum physics simulation library for open quantum systems. Use when studying master equations, Lindblad dynamics, decoherence, quantum optics, or ca | `skills/qutip/SKILL.md` |
| simpy | Process-based discrete-event simulation framework in Python. Use this skill when building simulations of systems with processes, queues, resources, an | `skills/simpy/SKILL.md` |

### Medicine & Clinical
**Keywords:** medical, clinical, healthcare, pathology, radiology, DICOM, treatment, diagnosis, EHR, patient, hospital, health
**Count:** 10

| Skill | Description | Path |
|-------|-------------|------|
| clinical-decision-support | Generate professional clinical decision support (CDS) documents for pharmaceutical and clinical research settings, including patient cohort analyses ( | `skills/clinical-decision-support/SKILL.md` |
| clinical-reports | Write comprehensive clinical reports including case reports (CARE guidelines), diagnostic reports (radiology/pathology/lab), clinical trial reports (I | `skills/clinical-reports/SKILL.md` |
| depmap | Query the Cancer Dependency Map (DepMap) for cancer cell line gene dependency scores (CRISPR Chronos), drug sensitivity data, and gene effect profiles | `skills/depmap/SKILL.md` |
| imaging-data-commons | Query and download public cancer imaging data from NCI Imaging Data Commons using idc-index. Use for accessing large-scale radiology (CT, MR, PET) and | `skills/imaging-data-commons/SKILL.md` |
| iso-13485-certification | Comprehensive toolkit for preparing ISO 13485 certification documentation for medical device Quality Management Systems. Use when users need help with | `skills/iso-13485-certification/SKILL.md` |
| pathml | Full-featured computational pathology toolkit. Use for advanced WSI analysis including multiplexed immunofluorescence (CODEX, Vectra), nucleus segment | `skills/pathml/SKILL.md` |
| primekg | Query the Precision Medicine Knowledge Graph (PrimeKG) for multiscale biological data including genes, drugs, diseases, phenotypes, and more. | `skills/primekg/SKILL.md` |
| pydicom | Python library for working with DICOM (Digital Imaging and Communications in Medicine) files. Use this skill when reading, writing, or modifying medic | `skills/pydicom/SKILL.md` |
| pyhealth | Build clinical/healthcare deep-learning pipelines with PyHealth — loading EHR/signal/imaging datasets (MIMIC-III/IV, eICU, OMOP, SleepEDF, ChestXray14 | `skills/pyhealth/SKILL.md` |
| treatment-plans | Generate concise (3-4 page), focused medical treatment plans in LaTeX/PDF format for all clinical specialties. Supports general medical treatment, reh | `skills/treatment-plans/SKILL.md` |

### Earth & Environmental Science
**Keywords:** earth science, geospatial, GIS, remote sensing, climate, satellite, geography, environmental
**Count:** 2

| Skill | Description | Path |
|-------|-------------|------|
| geomaster | Comprehensive geospatial science skill covering remote sensing, GIS, spatial analysis, machine learning for earth observation, and 30+ scientific doma | `skills/geomaster/SKILL.md` |
| geopandas | Python library for working with geospatial vector data including shapefiles, GeoJSON, and GeoPackage files. Use when working with geographic data for  | `skills/geopandas/SKILL.md` |

### Neuroscience
**Keywords:** neuroscience, brain, EEG, ECG, neural recording, electrophysiology, biosignal, cognitive
**Count:** 2

| Skill | Description | Path |
|-------|-------------|------|
| neurokit2 | Comprehensive biosignal processing toolkit for analyzing physiological data including ECG, EEG, EDA, RSP, PPG, EMG, and EOG signals. Use this skill wh | `skills/neurokit2/SKILL.md` |
| neuropixels-analysis | Neuropixels neural recording analysis. Load SpikeGLX/OpenEphys data, preprocess, motion correction, Kilosort4 spike sorting, quality metrics, Allen/IB | `skills/neuropixels-analysis/SKILL.md` |

### Finance & Economics
**Keywords:** finance, economics, market, fiscal, investment, financial, treasury, trading
**Count:** 2

| Skill | Description | Path |
|-------|-------------|------|
| market-research-reports | Generate comprehensive market research reports (50+ pages) in the style of top consulting firms (McKinsey, BCG, Gartner). Features professional LaTeX  | `skills/market-research-reports/SKILL.md` |
| usfiscaldata | Query the U.S. Treasury Fiscal Data API for federal financial data including national debt, government spending, revenue, interest rates, exchange rat | `skills/usfiscaldata/SKILL.md` |

### Writing Specializations
**Keywords:** systems paper, grant, NSF, NIH, hypothesis, scholarly evaluation, research methodology, proposal
**Count:** 8

| Skill | Description | Path |
|-------|-------------|------|
| systems-paper-writing | Comprehensive guide for writing systems papers targeting OSDI, SOSP, ASPLOS, NSDI, and EuroSys. Provides paragraph-level structural blueprints, writin | `skills/systems-paper-writing/SKILL.md` |
| hypothesis-generation | Structured hypothesis formulation from observations. Use when you have experimental observations or data and need to formulate testable hypotheses wit | `skills/hypothesis-generation/SKILL.md` |
| creative-thinking-for-research | Applies cognitive science frameworks for creative thinking to CS and AI research ideation. Use when seeking genuinely novel research directions by lev | `skills/creative-thinking-for-research/SKILL.md` |
| brainstorming-research-ideas | Guides researchers through structured ideation frameworks to discover high-impact research directions. Use when exploring new problem spaces, pivoting | `skills/brainstorming-research-ideas/SKILL.md` |
| scholar-evaluation | Systematically evaluate scholarly work using the ScholarEval framework, providing structured assessment across research quality dimensions including p | `skills/scholar-evaluation/SKILL.md` |
| rigor-reviewer | Performs ARA Seal Level 2 semantic epistemic review on Agent-Native Research Artifacts, scoring six dimensions (evidence relevance, falsifiability, sc | `skills/rigor-reviewer/SKILL.md` |
| research-grants | Write competitive research proposals for NSF, NIH, DOE, DARPA, and Taiwan NSTC. Agency-specific formatting, review criteria, budget preparation, broad | `skills/research-grants/SKILL.md` |
| scientific-critical-thinking | Evaluate scientific claims and evidence quality. Use for assessing experimental design validity, identifying biases and confounders, applying evidence | `skills/scientific-critical-thinking/SKILL.md` |

---

## TIER 3: UTILITY SKILLS (Need-Matched)

Select based on specific task requirements, not paper topic.

### Visualization & Figures
**Trigger (zh):** 需要图表、示意图、海报、幻灯片、数据可视化
**Trigger (en):** need charts, figures, diagrams, schematics, posters, slides
**Count:** 13

| Skill | Description | Path |
|-------|-------------|------|
| academic-plotting | Generates publication-quality figures for ML papers from research context. Given a paper section or description, extracts system components and relati | `skills/academic-plotting/SKILL.md` |
| generate-image | Generate or edit images using AI models (FLUX, Nano Banana 2). Use for general-purpose image generation including photos, illustrations, artwork, visu | `skills/generate-image/SKILL.md` |
| infographics | "Create professional infographics using Nano Banana Pro AI with smart iterative refinement. Uses Gemini 3 Pro for quality review. Integrates research- | `skills/infographics/SKILL.md` |
| latex-posters | "Create professional research posters in LaTeX using beamerposter, tikzposter, or baposter. Support for conference presentations, academic posters, an | `skills/latex-posters/SKILL.md` |
| markdown-mermaid-writing | Comprehensive markdown and Mermaid diagram writing skill. Use when creating any scientific document, report, analysis, or visualization. Establishes t | `skills/markdown-mermaid-writing/SKILL.md` |
| matplotlib | Low-level plotting library for full customization. Use when you need fine-grained control over every plot element, creating novel plot types, or integ | `skills/matplotlib/SKILL.md` |
| pptx-posters | Create research posters using HTML/CSS that can be exported to PDF or PPTX. Use this skill ONLY when the user explicitly requests PowerPoint/PPTX post | `skills/pptx-posters/SKILL.md` |
| scientific-schematics | Create publication-quality scientific diagrams using Nano Banana 2 AI with smart iterative refinement. Uses Gemini 3.1 Pro Preview for quality review. | `skills/scientific-schematics/SKILL.md` |
| scientific-slides | Build slide decks and presentations for research talks. Use this for making PowerPoint slides, conference presentations, seminar talks, research prese | `skills/scientific-slides/SKILL.md` |
| scientific-visualization | Meta-skill for publication-ready figures. Use when creating journal submission figures requiring multi-panel layouts, significance annotations, error  | `skills/scientific-visualization/SKILL.md` |
| seaborn | Statistical visualization with pandas integration. Use for quick exploration of distributions, relationships, and categorical comparisons with attract | `skills/seaborn/SKILL.md` |
| umap-learn | UMAP dimensionality reduction. Fast nonlinear manifold learning for 2D/3D visualization, clustering preprocessing (HDBSCAN), supervised/parametric UMA | `skills/umap-learn/SKILL.md` |
| presenting-conference-talks | Generates conference presentation slides (Beamer LaTeX PDF and editable PPTX) from a compiled paper with speaker notes and talk script. Use when prepa | `skills/presenting-conference-talks/SKILL.md` |

### Data & Statistics
**Trigger (zh):** 需要数据分析、统计建模、机器学习、数值计算
**Trigger (en):** need data analysis, statistics, ML modeling, optimization, numerical computing
**Count:** 14

| Skill | Description | Path |
|-------|-------------|------|
| dask | Distributed computing for larger-than-RAM pandas/NumPy workflows. Use when you need to scale existing pandas/NumPy code beyond memory or across cluste | `skills/dask/SKILL.md` |
| exploratory-data-analysis | Perform comprehensive exploratory data analysis on scientific data files across 200+ file formats. This skill should be used when analyzing any scient | `skills/exploratory-data-analysis/SKILL.md` |
| matlab | MATLAB and GNU Octave numerical computing for matrix operations, data analysis, visualization, and scientific computing. Use when writing MATLAB/Octav | `skills/matlab/SKILL.md` |
| networkx | Comprehensive toolkit for creating, analyzing, and visualizing complex networks and graphs in Python. Use when working with network/graph data structu | `skills/networkx/SKILL.md` |
| optimize-for-gpu | "GPU-accelerate Python code using CuPy, Numba CUDA, Warp, cuDF, cuML, cuGraph, KvikIO, cuCIM, cuxfilter, cuVS, cuSpatial, and RAFT. Use whenever the u | `skills/optimize-for-gpu/SKILL.md` |
| polars | Fast in-memory DataFrame library for datasets that fit in RAM. Use when pandas is too slow but data still fits in memory. Lazy evaluation, parallel ex | `skills/polars/SKILL.md` |
| pymc | Bayesian modeling with PyMC. Build hierarchical models, MCMC (NUTS), variational inference, LOO/WAIC comparison, posterior checks, for probabilistic p | `skills/pymc/SKILL.md` |
| pymoo | Multi-objective optimization framework. NSGA-II, NSGA-III, MOEA/D, Pareto fronts, constraint handling, benchmarks (ZDT, DTLZ), for engineering design  | `skills/pymoo/SKILL.md` |
| scikit-learn | Machine learning in Python with scikit-learn. Use when working with supervised learning (classification, regression), unsupervised learning (clusterin | `skills/scikit-learn/SKILL.md` |
| scikit-survival | Comprehensive toolkit for survival analysis and time-to-event modeling in Python using scikit-survival. Use this skill when working with censored surv | `skills/scikit-survival/SKILL.md` |
| statistical-analysis | Guided statistical analysis with test selection and reporting. Use when you need help choosing appropriate tests for your data, assumption checking, p | `skills/statistical-analysis/SKILL.md` |
| statsmodels | Statistical models library for Python. Use when you need specific model classes (OLS, GLM, mixed models, ARIMA) with detailed diagnostics, residuals,  | `skills/statsmodels/SKILL.md` |
| sympy | Use this skill when working with symbolic mathematics in Python. This skill should be used for symbolic computation tasks including solving equations  | `skills/sympy/SKILL.md` |
| vaex | Use this skill for processing and analyzing large tabular datasets (billions of rows) that exceed available RAM. Vaex excels at out-of-core DataFrame  | `skills/vaex/SKILL.md` |

### Document Processing
**Trigger (zh):** 需要读写 PDF、DOCX、PPTX、XLSX 或格式转换
**Trigger (en):** need to read/write PDF, DOCX, PPTX, XLSX or convert formats
**Count:** 7

| Skill | Description | Path |
|-------|-------------|------|
| docx | "Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers include: any mention of 'Word doc' | `skills/docx/SKILL.md` |
| markdown-mermaid-writing | Comprehensive markdown and Mermaid diagram writing skill. Use when creating any scientific document, report, analysis, or visualization. Establishes t | `skills/markdown-mermaid-writing/SKILL.md` |
| markitdown | Convert files and office documents to Markdown. Supports PDF, DOCX, PPTX, XLSX, images (with OCR), audio (with transcription), HTML, CSV, JSON, XML, Z | `skills/markitdown/SKILL.md` |
| parallel-web | "All-in-one web toolkit powered by parallel-cli, with a strong emphasis on academic and scientific sources. Use this skill whenever the user needs to  | `skills/parallel-web/SKILL.md` |
| pdf | Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging  | `skills/pdf/SKILL.md` |
| pptx | "Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or present | `skills/pptx/SKILL.md` |
| xlsx | "Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an e | `skills/xlsx/SKILL.md` |

### Research Automation
**Trigger (zh):** 需要自主研究、假设生成、What-If 分析、论文编译
**Trigger (en):** need autonomous research, hypothesis generation, what-if analysis
**Count:** 10

| Skill | Description | Path |
|-------|-------------|------|
| 0-autoresearch-skill | Orchestrates end-to-end autonomous AI research projects using a two-loop architecture. The inner loop runs rapid experiment iterations with clear opti | `skills/0-autoresearch-skill/SKILL.md` |
| a-evolve | Provides guidance for automatically evolving and optimizing AI agents across any domain using LLM-driven evolution algorithms. Use when building self- | `skills/a-evolve/SKILL.md` |
| autoskill | Observe the user's screen via screenpipe, detect repeated research workflows, match them against existing scientific-agent-skills, and draft new skill | `skills/autoskill/SKILL.md` |
| consciousness-council | Run a multi-perspective Mind Council deliberation on any question, decision, or creative challenge. Use this skill whenever the user wants diverse vie | `skills/consciousness-council/SKILL.md` |
| dhdna-profiler | Extract cognitive patterns and thinking fingerprints from any text. Use this skill when the user wants to analyze how someone thinks, understand cogni | `skills/dhdna-profiler/SKILL.md` |
| hypogenic | Automated LLM-driven hypothesis generation and testing on tabular datasets. Use when you want to systematically explore hypotheses about patterns in e | `skills/hypogenic/SKILL.md` |
| open-notebook | Self-hosted, open-source alternative to Google NotebookLM for AI-powered research and document analysis. Use when organizing research materials into n | `skills/open-notebook/SKILL.md` |
| paper-2-web | This skill should be used when converting academic papers into promotional and presentation formats including interactive websites (Paper2Web), presen | `skills/paper-2-web/SKILL.md` |
| paperzilla | Chat with your agent about projects, recommendations, and canonical papers in Paperzilla. Use when users ask for recent project recommendations, canon | `skills/paperzilla/SKILL.md` |
| what-if-oracle | Run structured What-If scenario analysis with multi-branch possibility exploration. Use this skill when the user asks speculative questions like "what | `skills/what-if-oracle/SKILL.md` |

### Infrastructure & Resources
**Trigger (zh):** 需要资源检测、文献管理、数据溯源
**Trigger (en):** need resource detection, reference management, data provenance
**Count:** 4

| Skill | Description | Path |
|-------|-------------|------|
| bgpt-paper-search | Search scientific papers and retrieve structured experimental data extracted from full-text studies via the BGPT MCP server. Returns 25+ fields per pa | `skills/bgpt-paper-search/SKILL.md` |
| get-available-resources | This skill should be used at the start of any computationally intensive scientific task to detect and report available system resources (CPU cores, GP | `skills/get-available-resources/SKILL.md` |
| pyzotero | Interact with Zotero reference management libraries using the pyzotero Python client. Retrieve, create, update, and delete items, collections, tags, a | `skills/pyzotero/SKILL.md` |
| research-manager | Records research provenance as a post-task epilogue, scanning conversation history at the end of a coding or research session to extract decisions, ex | `skills/research-manager/SKILL.md` |
