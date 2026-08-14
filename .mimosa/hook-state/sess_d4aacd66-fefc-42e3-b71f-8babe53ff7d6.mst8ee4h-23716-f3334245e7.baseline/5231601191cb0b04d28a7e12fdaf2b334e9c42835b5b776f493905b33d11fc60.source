"""Build tiered skill-catalog.md from SKILL.md files."""
import os, re, json

skills_dir = 'paper-writer/skills'

# Read all skills
skills = {}
for name in sorted(os.listdir(skills_dir)):
    skill_md = os.path.join(skills_dir, name, 'SKILL.md')
    if not os.path.isfile(skill_md):
        continue
    with open(skill_md, encoding='utf-8') as f:
        content = f.read()
    m = re.search(r'description:\s*>?\s*\n?\s*(.+?)(?:\n[a-z]|\n---)', content, re.DOTALL)
    if m:
        desc = m.group(1).strip().replace('\n  ', ' ').replace('\n', ' ')
        desc = re.sub(r'\s+', ' ', desc)[:150]
    else:
        desc = '(no description)'
    skills[name] = desc

CORE = [
    'scientific-writing', 'citation-management', 'literature-review',
    'paper-lookup', 'peer-review', 'compiler', 'venue-templates',
    'database-lookup', 'research-lookup', 'scientific-brainstorming'
]

DOMAINS = {
    'ML/AI & Machine Learning': {
        'keywords': 'machine learning, deep learning, neural network, transformer, LLM, NLP, computer vision, reinforcement learning, fine-tuning, training, inference, AI, GPT, diffusion, RLHF, LoRA, quantization, PyTorch, RAG, agent',
        'subgroups': {
            'Training & Infrastructure': ['accelerate', 'awq', 'axolotl', 'bitsandbytes', 'deepspeed',
                'flash-attention', 'gptq', 'grpo-rl-training', 'hqq', 'knowledge-distillation',
                'litgpt', 'llama-factory', 'long-context', 'mamba', 'megatron-core', 'miles',
                'ml-training-recipes', 'model-merging', 'model-pruning', 'moe-training', 'nanogpt',
                'nemo-curator', 'openrlhf', 'peft', 'pytorch-fsdp2', 'pytorch-lightning', 'rwkv',
                'simpo', 'slime', 'speculative-decoding', 'tensorrt-llm', 'torchforge', 'torchtitan',
                'trl-fine-tuning', 'unsloth', 'verl', 'vllm'],
            'Evaluation & Interpretability': ['bigcode-evaluation-harness', 'lm-evaluation-harness',
                'nemo-evaluator', 'nnsight', 'pyvene', 'saelens', 'shap', 'transformer-lens'],
            'Applications & Models': ['aeon', 'audiocraft', 'blip-2', 'clip', 'cosmos-policy',
                'hugging-science', 'llava', 'openpi', 'openvla-oft', 'pufferlib', 'segment-anything',
                'stable-baselines3', 'stable-diffusion', 'timesfm-forecasting', 'torch-geometric', 'whisper'],
            'Tools & Agents': ['autogpt', 'crewai', 'dspy', 'guidance', 'huggingface-tokenizers',
                'instructor', 'langchain', 'langsmith', 'llama-cpp', 'llamaguard', 'llamaindex',
                'outlines', 'prompt-guard', 'sentence-transformers', 'sentencepiece', 'transformers'],
            'Infrastructure & Tracking': ['chroma', 'faiss', 'gguf', 'lambda-labs', 'mlflow', 'modal',
                'nemo-guardrails', 'phoenix', 'pinecone', 'qdrant', 'ray-data', 'ray-train', 'sglang',
                'skypilot', 'swanlab', 'tensorboard', 'weights-and-biases'],
            'ML Paper Writing': ['ml-paper-writing'],
            'Safety & Alignment': ['constitutional-ai'],
        }
    },
    'Biology & Bioinformatics': {
        'keywords': 'biology, bioinformatics, genomics, proteomics, RNA, DNA, gene, protein, cell, single-cell, phylogenetics, sequence, FASTA, CRISPR, metabolomics, omics',
        'skills': ['anndata', 'arboreto', 'benchling-integration', 'biopython', 'bioservices',
            'cellxgene-census', 'cobrapy', 'deeptools', 'dnanexus-integration', 'esm', 'etetoolkit',
            'flowio', 'geniml', 'gget', 'ginkgo-cloud-lab', 'glycoengineering', 'gtars', 'histolab',
            'labarchive-integration', 'lamindb', 'latchbio-integration', 'omero-integration',
            'opentrons-integration', 'phylogenetics', 'polars-bio', 'protocolsio-integration',
            'pylabrobot', 'pydeseq2', 'pysam', 'scanpy', 'scikit-bio', 'scvelo', 'scvi-tools',
            'tiledbvcf', 'zarr-python']
    },
    'Chemistry & Drug Discovery': {
        'keywords': 'chemistry, drug discovery, molecule, molecular, SMILES, docking, ADMET, toxicity, compound, mass spectrometry, medicinal chemistry, pharmaceutical',
        'skills': ['adaptyv', 'datamol', 'deepchem', 'diffdock', 'matchms', 'medchem', 'molfeat',
            'molecular-dynamics', 'pymatgen', 'pyopenms', 'pytdc', 'rdkit', 'rowan', 'torchdrug']
    },
    'Physics & Quantum Computing': {
        'keywords': 'physics, quantum, simulation, fluid dynamics, astrophysics, astronomy, quantum computing, qubit, thermodynamic',
        'skills': ['astropy', 'cirq', 'fluidsim', 'pennylane', 'qiskit', 'qutip', 'simpy']
    },
    'Medicine & Clinical': {
        'keywords': 'medical, clinical, healthcare, pathology, radiology, DICOM, treatment, diagnosis, EHR, patient, hospital, health',
        'skills': ['clinical-decision-support', 'clinical-reports', 'depmap', 'imaging-data-commons',
            'iso-13485-certification', 'pathml', 'primekg', 'pydicom', 'pyhealth', 'treatment-plans']
    },
    'Earth & Environmental Science': {
        'keywords': 'earth science, geospatial, GIS, remote sensing, climate, satellite, geography, environmental',
        'skills': ['geomaster', 'geopandas']
    },
    'Neuroscience': {
        'keywords': 'neuroscience, brain, EEG, ECG, neural recording, electrophysiology, biosignal, cognitive',
        'skills': ['neurokit2', 'neuropixels-analysis']
    },
    'Finance & Economics': {
        'keywords': 'finance, economics, market, fiscal, investment, financial, treasury, trading',
        'skills': ['market-research-reports', 'usfiscaldata']
    },
    'Writing Specializations': {
        'keywords': 'systems paper, grant, NSF, NIH, hypothesis, scholarly evaluation, research methodology, proposal',
        'skills': ['systems-paper-writing', 'hypothesis-generation', 'creative-thinking-for-research',
            'brainstorming-research-ideas', 'scholar-evaluation', 'rigor-reviewer', 'research-grants',
            'scientific-critical-thinking']
    },
}

UTILITIES = {
    'Visualization & Figures': {
        'trigger': '需要图表、示意图、海报、幻灯片、数据可视化',
        'trigger_en': 'need charts, figures, diagrams, schematics, posters, slides',
        'skills': ['academic-plotting', 'generate-image', 'infographics', 'latex-posters', 'matplotlib',
            'pptx-posters', 'scientific-schematics', 'scientific-slides', 'scientific-visualization',
            'seaborn', 'umap-learn', 'presenting-conference-talks']
    },
    'Data & Statistics': {
        'trigger': '需要数据分析、统计建模、机器学习、数值计算',
        'trigger_en': 'need data analysis, statistics, ML modeling, optimization, numerical computing',
        'skills': ['dask', 'exploratory-data-analysis', 'matlab', 'networkx', 'optimize-for-gpu',
            'polars', 'pymc', 'pymoo', 'scikit-learn', 'scikit-survival', 'statistical-analysis',
            'statsmodels', 'sympy', 'vaex']
    },
    'Document Processing': {
        'trigger': '需要读写 PDF、DOCX、PPTX、XLSX 或格式转换',
        'trigger_en': 'need to read/write PDF, DOCX, PPTX, XLSX or convert formats',
        'skills': ['docx', 'markdown-mermaid-writing', 'markitdown', 'parallel-web', 'pdf', 'pptx', 'xlsx']
    },
    'Research Automation': {
        'trigger': '需要自主研究、假设生成、What-If 分析、论文编译',
        'trigger_en': 'need autonomous research, hypothesis generation, what-if analysis',
        'skills': ['0-autoresearch-skill', 'a-evolve', 'autoskill', 'consciousness-council',
            'dhdna-profiler', 'hypogenic', 'open-notebook', 'paper-2-web', 'paperzilla', 'what-if-oracle']
    },
    'Infrastructure & Resources': {
        'trigger': '需要资源检测、文献管理、数据溯源',
        'trigger_en': 'need resource detection, reference management, data provenance',
        'skills': ['bgpt-paper-search', 'get-available-resources', 'pyzotero', 'research-manager']
    },
}

# Verify coverage
all_categorized = set(CORE)
for d, info in DOMAINS.items():
    if 'skills' in info:
        all_categorized.update(info['skills'])
    if 'subgroups' in info:
        for sg, sg_skills in info['subgroups'].items():
            all_categorized.update(sg_skills)
for u, info in UTILITIES.items():
    all_categorized.update(info['skills'])

missing = set(skills.keys()) - all_categorized
extra = all_categorized - set(skills.keys())
if missing:
    print(f'WARNING: {len(missing)} skills not categorized: {sorted(missing)}')
if extra:
    print(f'WARNING: {len(extra)} categorized but not in skills dir: {sorted(extra)}')
print(f'Total: {len(skills)}, Categorized: {len(all_categorized)}, Missing: {len(missing)}, Extra: {len(extra)}')

# Generate catalog
lines = []
lines.append('# Skill Catalog')
lines.append('')
lines.append(f'> {len(skills)} skills organized by tier for efficient retrieval')
lines.append('> Tier 1 (Core): always loaded | Tier 2 (Domain): topic-matched | Tier 3 (Utility): need-matched')
lines.append('')

# Tier 1
lines.append('---')
lines.append('')
lines.append('## TIER 1: CORE SKILLS (Always Loaded)')
lines.append('')
lines.append('These skills are loaded for **every** paper-writing task regardless of topic.')
lines.append('')
lines.append('| Skill | Description | Path |')
lines.append('|-------|-------------|------|')
for name in CORE:
    desc = skills.get(name, '(no description)')
    lines.append(f'| {name} | {desc} | `skills/{name}/SKILL.md` |')
lines.append('')

# Tier 2
lines.append('---')
lines.append('')
lines.append('## TIER 2: DOMAIN SKILLS (Topic-Matched)')
lines.append('')
lines.append('Match the paper topic against domain keywords. Load ALL skills from matching domain(s).')
lines.append('A paper may match multiple domains (e.g. "deep learning for protein structure" matches both ML/AI and Biology).')
lines.append('')

for domain, info in DOMAINS.items():
    count = 0
    if 'skills' in info:
        count += len(info['skills'])
    if 'subgroups' in info:
        for sg_skills in info['subgroups'].values():
            count += len(sg_skills)

    lines.append(f'### {domain}')
    lines.append(f'**Keywords:** {info["keywords"]}')
    lines.append(f'**Count:** {count}')
    lines.append('')

    if 'subgroups' in info:
        for sg_name, sg_skills in info['subgroups'].items():
            lines.append(f'#### {sg_name} ({len(sg_skills)})')
            lines.append('| Skill | Description | Path |')
            lines.append('|-------|-------------|------|')
            for name in sg_skills:
                desc = skills.get(name, '(no description)')
                lines.append(f'| {name} | {desc} | `skills/{name}/SKILL.md` |')
            lines.append('')
    elif 'skills' in info:
        lines.append('| Skill | Description | Path |')
        lines.append('|-------|-------------|------|')
        for name in info['skills']:
            desc = skills.get(name, '(no description)')
            lines.append(f'| {name} | {desc} | `skills/{name}/SKILL.md` |')
        lines.append('')

# Tier 3
lines.append('---')
lines.append('')
lines.append('## TIER 3: UTILITY SKILLS (Need-Matched)')
lines.append('')
lines.append('Select based on specific task requirements, not paper topic.')
lines.append('')

for util, info in UTILITIES.items():
    lines.append(f'### {util}')
    lines.append(f'**Trigger (zh):** {info["trigger"]}')
    lines.append(f'**Trigger (en):** {info["trigger_en"]}')
    lines.append(f'**Count:** {len(info["skills"])}')
    lines.append('')
    lines.append('| Skill | Description | Path |')
    lines.append('|-------|-------------|------|')
    for name in info['skills']:
        desc = skills.get(name, '(no description)')
        lines.append(f'| {name} | {desc} | `skills/{name}/SKILL.md` |')
    lines.append('')

# Write
out_path = 'paper-writer/references/skill-catalog.md'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f'Written to {out_path}: {len(lines)} lines')
