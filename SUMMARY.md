# Task Agent - Project Summary

## 项目概述 / Project Overview

### 中文

Task Agent 是一个智能AI代理系统，专门用于将复杂任务分解为可管理的子任务并逐步执行。该系统特别适合创建学术文献综述，但也可以扩展到其他任务类型。

**核心功能：**
- 使用 Gemini AI 进行智能任务分解
- 专门的文献综述工作流程
- 多格式文档生成（Markdown、Word、PDF）
- 论文管理和元数据跟踪
- 自动执行日志记录
- 工作流状态管理

### English

Task Agent is an intelligent AI agent system designed to decompose complex tasks into manageable subtasks and execute them step-by-step. The system is particularly suited for creating academic literature reviews but can be extended to other task types.

**Core Features:**
- Intelligent task decomposition using Gemini AI
- Specialized literature review workflow
- Multi-format document generation (Markdown, Word, PDF)
- Paper management and metadata tracking
- Automatic execution logging
- Workflow state management

---

## 实现的功能 / Implemented Features

### ✅ 任务分解 / Task Decomposition
- AI 自动分解复杂任务
- 支持自定义任务创建
- 任务状态管理（待处理、进行中、完成、失败、等待用户）

### ✅ 文献综述工作流 / Literature Review Workflow
1. **收集论文** - AI 建议相关论文
2. **上传论文** - 用户手动操作（标记为等待用户状态）
3. **分析论文** - AI 分析并提取关键发现
4. **创建大纲** - AI 生成综合性大纲
5. **撰写综述** - AI 逐段撰写完整综述

### ✅ 输出格式 / Output Formats
- **主要格式：** Markdown (.md)
- **辅助格式：** DOCX (.docx) + PDF (.pdf)
- **执行日志：** output/logs/execution.log
- **元数据：** JSON 格式（论文信息、大纲结构）

### ✅ 论文管理 / Paper Management
- 添加和跟踪研究论文
- 存储论文元数据（标题、作者、年份、摘要、关键词）
- JSON 格式持久化存储
- 自动生成论文摘要

### ✅ 文档生成 / Document Generation
- Markdown 到 DOCX 转换
- Markdown 到 PDF 转换
- 支持标题、列表、段落等格式
- 一键生成所有格式

---

## 项目结构 / Project Structure

```
Task_Agent/
├── src/task_agent/              # 核心源代码
│   ├── __init__.py             # 包初始化
│   ├── agent.py                # 主 Agent 控制器
│   ├── gemini_client.py        # Gemini API 客户端
│   ├── task.py                 # 任务数据结构
│   ├── paper.py                # 论文管理
│   └── document.py             # 文档生成
├── test/                        # 测试文件
│   ├── test_basic.py           # 基础单元测试
│   └── test_integration.py     # 集成测试
├── output/                      # 输出目录
│   ├── generated/              # 生成的文档
│   ├── papers/                 # 论文和元数据
│   └── logs/                   # 执行日志
├── main.py                      # 主程序入口
├── demo.py                      # 功能演示（无需 API key）
├── examples.py                  # 高级示例
├── config.yaml                  # 配置文件
├── requirements.txt             # 依赖项
├── README.md                    # 项目文档
├── USAGE.md                     # 使用指南（双语）
└── SUMMARY.md                   # 本文件
```

---

## 技术栈 / Technology Stack

### AI/ML
- **Gemini API** - Google 的生成式 AI 模型
- **google-generativeai** - Python SDK

### 文档处理 / Document Processing
- **python-docx** - Word 文档生成
- **reportlab** - PDF 生成
- **markdown** - Markdown 处理

### 其他 / Others
- **pyyaml** - 配置管理
- **python-dotenv** - 环境变量管理

---

## 使用示例 / Usage Examples

### 基础使用 / Basic Usage

```python
from task_agent import TaskAgent

# 初始化 / Initialize
agent = TaskAgent()

# 创建文献综述 / Create literature review
agent.create_literature_review("Machine Learning in Healthcare")
```

### 自定义工作流 / Custom Workflow

```python
from task_agent import TaskAgent, Task, Workflow

agent = TaskAgent()

workflow = agent.create_workflow(
    title="Custom Research Task",
    description="Your description"
)

workflow.add_task(Task(
    id="task_1",
    title="Research Phase",
    description="Conduct research"
))

agent.run_workflow(workflow)
```

### 添加论文 / Add Papers

```python
agent.add_papers([
    {
        'title': 'Paper Title',
        'authors': ['Author 1'],
        'year': 2023,
        'abstract': 'Abstract...'
    }
])
```

---

## 测试覆盖 / Test Coverage

### 基础测试 / Basic Tests
- ✅ 任务创建和状态管理
- ✅ 工作流创建和导航
- ✅ 论文管理
- ✅ 工作流序列化/反序列化

### 集成测试 / Integration Tests
- ✅ 完整工作流程
- ✅ 论文管理和元数据
- ✅ 文档生成（所有格式）
- ✅ 状态持久化

### 安全检查 / Security
- ✅ CodeQL 扫描通过（0 漏洞）

---

## 快速开始 / Quick Start

### 1. 安装 / Installation

```bash
pip install -r requirements.txt
```

### 2. 配置 / Configuration

```bash
cp .env.example .env
# 编辑 .env 添加 Gemini API key
# Edit .env to add Gemini API key
```

### 3. 运行 / Run

```bash
# 演示（无需 API key）/ Demo (no API key needed)
python demo.py

# 完整系统 / Full system
python main.py

# 测试 / Tests
python test/test_basic.py
python test/test_integration.py
```

---

## 输出示例 / Output Examples

### 生成的文件 / Generated Files

```
output/
├── generated/
│   ├── literature_review_20231113_123456.md
│   ├── literature_review_20231113_123456.docx
│   └── literature_review_20231113_123456.pdf
├── papers/
│   └── papers_metadata.json
├── logs/
│   └── execution.log
└── workflow_20231113_123456.json
```

### 论文元数据示例 / Paper Metadata Example

```json
{
  "title": "Deep Learning for Medical Imaging",
  "authors": ["Smith, J.", "Johnson, A."],
  "year": 2023,
  "abstract": "This paper presents...",
  "keywords": ["deep learning", "medical imaging"],
  "summary": "AI-generated summary...",
  "key_findings": [
    "Finding 1",
    "Finding 2"
  ]
}
```

---

## 主要类和方法 / Main Classes and Methods

### TaskAgent
- `create_workflow(title, description)` - 创建工作流
- `decompose_task(main_task)` - 分解任务
- `execute_task(task)` - 执行任务
- `run_workflow(workflow)` - 运行工作流
- `create_literature_review(topic)` - 创建文献综述
- `add_papers(papers_info)` - 添加论文

### Task
- 任务数据结构，包含 ID、标题、描述、状态、结果等

### Workflow
- 工作流管理，包含多个任务和当前状态

### PaperManager
- `add_paper(paper)` - 添加论文
- `list_papers()` - 列出所有论文
- `generate_papers_summary()` - 生成摘要

### DocumentGenerator
- `save_markdown(content, filename)` - 保存 Markdown
- `markdown_to_docx(content, filename)` - 转换为 DOCX
- `markdown_to_pdf(content, filename)` - 转换为 PDF
- `generate_all_formats(content, filename)` - 生成所有格式

---

## 配置选项 / Configuration Options

### config.yaml

```yaml
ai:
  model: "gemini-pro"
  temperature: 0.7
  max_tokens: 4096

output:
  base_dir: "output"
  logs_dir: "output/logs"
  papers_dir: "output/papers"
  generated_dir: "output/generated"

logging:
  level: "INFO"
  file: "output/logs/execution.log"
```

---

## 日志记录 / Logging

所有操作都会自动记录到 `output/logs/execution.log`：
All operations are automatically logged to `output/logs/execution.log`:

```
2023-11-13 12:34:56 - task_agent.agent - INFO - TaskAgent initialized
2023-11-13 12:35:01 - task_agent.agent - INFO - Created workflow: Literature Review
2023-11-13 12:35:02 - task_agent.agent - INFO - Decomposing task...
2023-11-13 12:35:15 - task_agent.paper - INFO - Added paper: Paper Title
2023-11-13 12:35:30 - task_agent.document - INFO - Generated all formats
```

---

## 扩展性 / Extensibility

系统设计为可扩展的：
The system is designed to be extensible:

### 添加新的任务类型 / Add New Task Types

```python
def _handle_custom_task(self, task: Task) -> str:
    """Handle custom task type"""
    # Your implementation
    return result
```

### 自定义文档格式 / Custom Document Formats

```python
def custom_format(self, content: str, filename: str) -> str:
    """Generate custom format"""
    # Your implementation
    return filepath
```

### 集成其他 AI 模型 / Integrate Other AI Models

修改 `gemini_client.py` 以支持其他 AI 提供商
Modify `gemini_client.py` to support other AI providers

---

## 限制和注意事项 / Limitations and Notes

1. **API 依赖** - 需要 Gemini API key
2. **语言支持** - 主要支持英文和中文
3. **论文上传** - 需要用户手动下载和上传论文
4. **网络连接** - 需要互联网连接以访问 AI API

---

## 未来改进 / Future Improvements

- [ ] 支持更多 AI 模型（OpenAI, Claude 等）
- [ ] 自动论文下载和 OCR
- [ ] Web 界面
- [ ] 更多输出格式（LaTeX, HTML）
- [ ] 协作功能
- [ ] 模板系统

---

## 贡献指南 / Contributing

欢迎贡献！请：
Contributions welcome! Please:

1. Fork 项目 / Fork the project
2. 创建特性分支 / Create feature branch
3. 提交更改 / Commit changes
4. 推送到分支 / Push to branch
5. 创建 Pull Request

---

## 许可证 / License

MIT License

---

## 支持 / Support

如有问题或建议，请在 GitHub 上提交 Issue。
For questions or suggestions, please submit an Issue on GitHub.

---

## 致谢 / Acknowledgments

- Google Gemini AI
- Python 开源社区 / Python Open Source Community
- 所有贡献者 / All Contributors
