# Task Agent - 使用指南 / Usage Guide

## 中文说明

### 简介

Task Agent 是一个智能AI代理，可以将复杂任务分解为可管理的子任务并逐步执行。特别适合创建文献综述和研究综合。

### 主要功能

- 🤖 **AI驱动的任务分解**：使用Gemini AI自动将复杂任务分解为可执行的子任务
- 📚 **文献综述工作流**：专为学术文献综述设计的工作流
- 📄 **多种输出格式**：生成Markdown (.md)、Word (.docx) 和 PDF 格式的文档
- 📊 **论文管理**：跟踪和管理研究论文及其元数据
- 📝 **执行日志**：自动记录所有执行步骤到 output/logs/execution.log
- 🔄 **状态管理**：保存和恢复工作流
- 🎯 **分步执行**：清晰的进度跟踪，一次执行一个任务

### 快速开始

1. **安装依赖**
```bash
pip install -r requirements.txt
```

2. **配置API密钥**
```bash
cp .env.example .env
# 编辑 .env 文件并添加你的 Gemini API 密钥
```

3. **运行示例**
```bash
# 运行演示（不需要API密钥）
python demo.py

# 运行完整的文献综述生成器
python main.py

# 运行高级示例
python examples.py
```

### 工作流程示例

对于文献综述任务，Agent会自动创建以下步骤：

1. **收集相关论文** - AI建议相关论文
2. **上传论文** - 用户下载并上传论文（手动步骤）
3. **分析论文** - AI分析每篇论文并提取关键发现
4. **创建大纲** - AI生成综合大纲
5. **撰写综述** - AI逐段撰写完整的文献综述

### 输出结构

```
output/
├── generated/              # 生成的文档 (.md, .docx, .pdf)
├── logs/
│   └── execution.log      # 执行日志
├── papers/
│   └── papers_metadata.json  # 论文元数据
└── workflow_*.json        # 工作流状态文件
```

### 代码示例

```python
from task_agent import TaskAgent

# 初始化Agent
agent = TaskAgent()

# 创建文献综述
agent.create_literature_review("机器学习在医疗保健中的应用")
```

### 自定义工作流

```python
from task_agent import TaskAgent, Task, Workflow

agent = TaskAgent()

# 创建自定义工作流
workflow = agent.create_workflow(
    title="自定义研究任务",
    description="任务描述"
)

# 添加自定义任务
workflow.add_task(Task(
    id="task_1",
    title="研究阶段",
    description="进行初步研究"
))

# 运行工作流
agent.run_workflow(workflow)
```

### 手动添加论文

```python
agent.add_papers([
    {
        'title': '论文标题',
        'authors': ['作者1', '作者2'],
        'year': 2023,
        'abstract': '摘要内容...',
        'keywords': ['关键词1', '关键词2']
    }
])
```

---

## English Guide

### Introduction

Task Agent is an intelligent AI agent that breaks down complex tasks into manageable subtasks and executes them step-by-step. Particularly designed for creating literature reviews and research syntheses.

### Key Features

- 🤖 **AI-Powered Task Decomposition**: Automatically breaks down complex tasks using Gemini AI
- 📚 **Literature Review Workflow**: Specialized workflow for academic literature reviews
- 📄 **Multiple Output Formats**: Generate Markdown (.md), Word (.docx), and PDF documents
- 📊 **Paper Management**: Track and manage research papers with metadata
- 📝 **Execution Logging**: Automatic logging to output/logs/execution.log
- 🔄 **State Management**: Save and resume workflows
- 🎯 **Step-by-Step Execution**: Clear progress tracking

### Quick Start

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Configure API Key**
```bash
cp .env.example .env
# Edit .env file and add your Gemini API key
```

3. **Run Examples**
```bash
# Run demo (no API key required)
python demo.py

# Run full literature review generator
python main.py

# Run advanced examples
python examples.py
```

### Workflow Example

For literature review tasks, the Agent automatically creates:

1. **Collect Relevant Papers** - AI suggests relevant papers
2. **Upload Papers** - User downloads and uploads papers (manual step)
3. **Analyze Papers** - AI analyzes each paper and extracts key findings
4. **Create Outline** - AI generates comprehensive outline
5. **Write Review** - AI writes complete literature review section by section

### Output Structure

```
output/
├── generated/              # Generated documents (.md, .docx, .pdf)
├── logs/
│   └── execution.log      # Execution logs
├── papers/
│   └── papers_metadata.json  # Paper metadata
└── workflow_*.json        # Workflow state files
```

### Code Examples

```python
from task_agent import TaskAgent

# Initialize Agent
agent = TaskAgent()

# Create literature review
agent.create_literature_review("Machine Learning in Healthcare")
```

### Custom Workflow

```python
from task_agent import TaskAgent, Task, Workflow

agent = TaskAgent()

# Create custom workflow
workflow = agent.create_workflow(
    title="Custom Research Task",
    description="Task description"
)

# Add custom tasks
workflow.add_task(Task(
    id="task_1",
    title="Research Phase",
    description="Conduct initial research"
))

# Run workflow
agent.run_workflow(workflow)
```

### Manually Add Papers

```python
agent.add_papers([
    {
        'title': 'Paper Title',
        'authors': ['Author 1', 'Author 2'],
        'year': 2023,
        'abstract': 'Abstract content...',
        'keywords': ['keyword1', 'keyword2']
    }
])
```

### API Reference

See README.md for complete API reference.

### Troubleshooting

**API Key Error:**
```
Error: Gemini API key not provided
```
Solution: Set `GEMINI_API_KEY` in `.env` file

**Module Not Found:**
```
ModuleNotFoundError: No module named 'google.generativeai'
```
Solution: Run `pip install -r requirements.txt`

### Getting Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key to your `.env` file

### Support

For issues and questions, please visit the GitHub repository.
