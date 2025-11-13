# Task Agent - AI-Powered Task Decomposition and Execution

An intelligent AI agent that breaks down complex tasks into manageable subtasks and executes them step-by-step. Particularly designed for creating literature reviews and research syntheses.

## Features

- 🤖 **AI-Powered Task Decomposition**: Automatically breaks down complex tasks into actionable subtasks using Gemini AI
- 📚 **Literature Review Workflow**: Specialized workflow for academic literature reviews
- 📄 **Multiple Output Formats**: Generate documents in Markdown (.md), Word (.docx), and PDF formats
- 📊 **Paper Management**: Track and manage research papers with metadata
- 📝 **Execution Logging**: Automatic logging of all execution steps
- 🔄 **State Management**: Save and resume workflows
- 🎯 **Step-by-Step Execution**: Execute tasks one at a time with clear progress tracking

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Bonjomondo/Task_Agent.git
cd Task_Agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Gemini API key:
```bash
cp .env.example .env
# Edit .env and add your Gemini API key
```

## Quick Start

### Basic Usage

```python
from task_agent import TaskAgent

# Initialize the agent
agent = TaskAgent()

# Create a literature review
agent.create_literature_review("Machine Learning in Healthcare")
```

### Run the Main Script

```bash
python main.py
```

This will guide you through creating a literature review with an interactive interface.

## Workflow Example

For a literature review, the agent automatically creates these steps:

1. **Collect Relevant Papers** - AI suggests relevant papers to review
2. **Upload Papers** - User downloads and uploads papers (manual step)
3. **Analyze Papers** - AI analyzes each paper and extracts key findings
4. **Create Outline** - AI generates a comprehensive outline
5. **Write Review** - AI writes the complete literature review section by section

## Output Structure

```
output/
├── generated/              # Generated documents (.md, .docx, .pdf)
├── logs/
│   └── execution.log      # Execution logs
├── papers/
│   └── papers_metadata.json  # Paper metadata
└── workflow_*.json        # Workflow state files
```

## Configuration

Edit `config.yaml` to customize:

- AI model settings (temperature, max tokens)
- Output directories
- Logging configuration
- Task execution parameters

## Advanced Usage

### Custom Workflow

```python
from task_agent import TaskAgent, Task, Workflow

agent = TaskAgent()

# Create custom workflow
workflow = agent.create_workflow(
    title="Custom Research Task",
    description="Your task description"
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

### Manual Paper Management

```python
# Add papers manually
agent.add_papers([
    {
        'title': 'Paper Title',
        'authors': ['Author 1', 'Author 2'],
        'year': 2023,
        'abstract': 'Paper abstract...',
        'keywords': ['keyword1', 'keyword2']
    }
])

# Generate papers summary
summary = agent.paper_manager.generate_papers_summary()
```

### Task Decomposition Only

```python
# Decompose a task without executing
tasks = agent.decompose_task("Write a systematic review on AI in education")

for task in tasks:
    print(f"- {task.title}: {task.description}")
```

## Examples

Run the examples script to see different use cases:

```bash
python examples.py
```

Available examples:
1. Custom workflow creation
2. Manual paper management
3. Task decomposition demo

## API Reference

### TaskAgent

Main class for task management and execution.

**Methods:**
- `create_workflow(title, description)` - Create a new workflow
- `decompose_task(main_task)` - Break down a task into subtasks
- `execute_task(task)` - Execute a single task
- `run_workflow(workflow)` - Run a complete workflow
- `create_literature_review(topic)` - Create and run a literature review
- `add_papers(papers_info)` - Add papers to the collection

### Task

Represents a single task.

**Attributes:**
- `id` - Unique task identifier
- `title` - Task title
- `description` - Task description
- `status` - Current status (PENDING, IN_PROGRESS, COMPLETED, FAILED, WAITING_USER)
- `result` - Task execution result
- `metadata` - Additional task metadata

### DocumentGenerator

Generate documents in multiple formats.

**Methods:**
- `save_markdown(content, filename)` - Save as Markdown
- `markdown_to_docx(content, filename)` - Convert to Word
- `markdown_to_pdf(content, filename)` - Convert to PDF
- `generate_all_formats(content, filename)` - Generate all formats

### PaperManager

Manage research papers.

**Methods:**
- `add_paper(paper)` - Add a paper
- `list_papers()` - Get all papers
- `get_paper_by_title(title)` - Find paper by title
- `update_paper_summary(title, summary, key_findings)` - Update paper analysis
- `generate_papers_summary()` - Generate summary of all papers

## Requirements

- Python 3.8+
- Gemini API key (get from [Google AI Studio](https://makersuite.google.com/app/apikey))

## Dependencies

- `google-generativeai` - Gemini AI API
- `python-docx` - Word document generation
- `reportlab` - PDF generation
- `pyyaml` - Configuration management
- `python-dotenv` - Environment variable management

## Project Structure

```
Task_Agent/
├── src/
│   └── task_agent/
│       ├── __init__.py          # Package initialization
│       ├── agent.py             # Main TaskAgent class
│       ├── gemini_client.py     # Gemini API client
│       ├── task.py              # Task data structures
│       ├── document.py          # Document generation
│       └── paper.py             # Paper management
├── output/                      # Generated outputs (git-ignored)
├── main.py                      # Main entry point
├── examples.py                  # Usage examples
├── config.yaml                  # Configuration
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

## Logging

All execution is automatically logged to `output/logs/execution.log` with:
- Timestamp
- Component name
- Log level
- Message

## Troubleshooting

### API Key Issues
```
Error: Gemini API key not provided
```
**Solution**: Set `GEMINI_API_KEY` in `.env` file

### Import Errors
```
ModuleNotFoundError: No module named 'google.generativeai'
```
**Solution**: Install dependencies with `pip install -r requirements.txt`

### Permission Errors
```
PermissionError: [Errno 13] Permission denied: 'output/logs/execution.log'
```
**Solution**: Ensure output directories are writable

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Author

Task Agent Team

## Acknowledgments

- Built with Google's Gemini AI
- Inspired by autonomous agent frameworks