# Task Agent - Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Task Agent System                        │
└─────────────────────────────────────────────────────────────────┘

                              User Interface
                                    │
                                    ▼
                    ┌───────────────────────────┐
                    │      main.py / API        │
                    │   (Entry Points)          │
                    └───────────────┬───────────┘
                                    │
                                    ▼
        ┌───────────────────────────────────────────────────┐
        │              TaskAgent (agent.py)                  │
        │  - Workflow Management                            │
        │  - Task Decomposition                             │
        │  - Task Execution Routing                         │
        └───┬────────┬───────────┬──────────┬──────────────┘
            │        │           │          │
            ▼        ▼           ▼          ▼
    ┌───────────┐ ┌─────────┐ ┌──────────┐ ┌──────────────┐
    │  Gemini   │ │  Paper  │ │ Document │ │    Task      │
    │  Client   │ │ Manager │ │Generator │ │  Workflow    │
    │           │ │         │ │          │ │  Manager     │
    └─────┬─────┘ └────┬────┘ └────┬─────┘ └──────┬───────┘
          │            │           │              │
          │            │           │              │
          ▼            ▼           ▼              ▼
    ┌─────────┐  ┌──────────┐ ┌────────┐   ┌──────────┐
    │ Gemini  │  │  Papers  │ │ Output │   │Workflow  │
    │   API   │  │Metadata  │ │  Files │   │  State   │
    │         │  │  (.json) │ │(.md/..) │   │ (.json)  │
    └─────────┘  └──────────┘ └────────┘   └──────────┘
```

## Component Breakdown

### 1. Core Components

#### TaskAgent (agent.py)
- **Purpose**: Main orchestrator
- **Responsibilities**:
  - Create and manage workflows
  - Decompose tasks using AI
  - Route task execution to appropriate handlers
  - Coordinate between all components
- **Key Methods**:
  - `create_workflow()`
  - `decompose_task()`
  - `execute_task()`
  - `run_workflow()`
  - `create_literature_review()`

#### GeminiClient (gemini_client.py)
- **Purpose**: AI integration layer
- **Responsibilities**:
  - Connect to Gemini API
  - Generate AI responses
  - Handle API errors and retries
- **Key Methods**:
  - `generate()` - Generate text from prompt
  - `chat()` - Multi-turn conversations

#### Task & Workflow (task.py)
- **Purpose**: Data structures
- **Responsibilities**:
  - Define task structure and status
  - Manage workflow state
  - Serialize/deserialize state
- **Key Classes**:
  - `Task` - Individual task
  - `Workflow` - Collection of tasks
  - `TaskStatus` - Task states (enum)

#### PaperManager (paper.py)
- **Purpose**: Research paper management
- **Responsibilities**:
  - Store paper metadata
  - Track paper analysis
  - Generate paper summaries
- **Key Methods**:
  - `add_paper()`
  - `list_papers()`
  - `update_paper_summary()`
  - `generate_papers_summary()`

#### DocumentGenerator (document.py)
- **Purpose**: Multi-format document generation
- **Responsibilities**:
  - Save Markdown files
  - Convert to DOCX
  - Convert to PDF
- **Key Methods**:
  - `save_markdown()`
  - `markdown_to_docx()`
  - `markdown_to_pdf()`
  - `generate_all_formats()`

### 2. Entry Points

#### main.py
- Interactive CLI for literature reviews
- Guides user through complete workflow
- Example topics provided

#### examples.py
- Advanced usage demonstrations
- Custom workflow examples
- Paper management examples
- Task decomposition examples

#### demo.py
- No-API-key demonstration
- Shows all features without AI
- Good for testing/understanding

### 3. Data Flow

```
User Input
    │
    ▼
Task Decomposition (AI)
    │
    ▼
Task Execution Loop
    │
    ├─→ Paper Collection (AI suggests)
    │       │
    │       ▼
    │   User Upload (Manual)
    │       │
    │       ▼
    │   Paper Analysis (AI)
    │       │
    │       ▼
    │   Outline Creation (AI)
    │       │
    │       ▼
    └─→ Document Writing (AI)
            │
            ▼
    Multi-Format Generation
            │
            ▼
    Output Files (MD, DOCX, PDF)
```

### 4. File Organization

```
Task_Agent/
│
├── src/task_agent/          # Core library
│   ├── agent.py            # Main controller
│   ├── gemini_client.py    # AI client
│   ├── task.py             # Data structures
│   ├── paper.py            # Paper management
│   └── document.py         # Document generation
│
├── test/                    # Test suite
│   ├── test_basic.py       # Unit tests
│   └── test_integration.py # Integration tests
│
├── output/                  # Generated outputs
│   ├── generated/          # Documents
│   ├── papers/             # Paper metadata
│   └── logs/               # Execution logs
│
├── main.py                  # Main entry point
├── examples.py              # Advanced examples
├── demo.py                  # Demo script
│
├── config.yaml              # Configuration
├── requirements.txt         # Dependencies
│
└── docs/                    # Documentation
    ├── README.md           # Main docs
    ├── USAGE.md            # Usage guide
    └── SUMMARY.md          # Project summary
```

## Workflow State Machine

```
Task Status Transitions:

    PENDING
       │
       ▼ execute_task()
  IN_PROGRESS
       │
       ├─→ Success ──→ COMPLETED
       │
       ├─→ Failure ──→ FAILED
       │
       └─→ User Action ──→ WAITING_USER
                               │
                               ▼ User completes
                           COMPLETED
```

## Literature Review Workflow

```
1. Collect Papers
   └─→ AI generates paper suggestions
       └─→ Papers stored in task metadata

2. Upload Papers (WAITING_USER)
   └─→ User downloads & uploads
       └─→ Papers registered in PaperManager
           └─→ Metadata saved to JSON

3. Analyze Papers
   └─→ AI analyzes each paper
       └─→ Extracts key findings
           └─→ Updates paper metadata

4. Create Outline
   └─→ AI generates review outline
       └─→ Considers all papers
           └─→ Saves to workflow metadata

5. Write Review
   └─→ AI writes complete review
       └─→ Uses outline + papers
           └─→ Generates all formats
               └─→ MD + DOCX + PDF
```

## Technology Stack

```
┌─────────────────────────────────────┐
│         Application Layer            │
│  - TaskAgent                         │
│  - Workflow Management               │
│  - Task Execution                    │
└──────────────┬──────────────────────┘
               │
┌──────────────┴──────────────────────┐
│         Service Layer                │
│  - GeminiClient (AI)                 │
│  - PaperManager (Data)               │
│  - DocumentGenerator (Output)        │
└──────────────┬──────────────────────┘
               │
┌──────────────┴──────────────────────┐
│         External Services            │
│  - Gemini API (Google)               │
└──────────────┬──────────────────────┘
               │
┌──────────────┴──────────────────────┐
│         Libraries                    │
│  - google-generativeai               │
│  - python-docx                       │
│  - reportlab                         │
│  - pyyaml                           │
└─────────────────────────────────────┘
```

## Error Handling Strategy

```
Level 1: Task Execution
    │
    ├─→ Catch task-specific errors
    ├─→ Mark task as FAILED
    └─→ Log error details

Level 2: Workflow Execution
    │
    ├─→ Catch workflow errors
    ├─→ Save workflow state
    └─→ Allow resume

Level 3: Component Errors
    │
    ├─→ API errors (retry)
    ├─→ File I/O errors (log)
    └─→ Data validation errors (report)

Level 4: System Errors
    │
    ├─→ Log to execution.log
    ├─→ Preserve state
    └─→ Graceful shutdown
```

## Configuration Management

```
Environment Variables (.env)
    │
    ├─→ GEMINI_API_KEY
    └─→ GEMINI_MODEL

Configuration File (config.yaml)
    │
    ├─→ AI Settings
    │   ├─→ model
    │   ├─→ temperature
    │   └─→ max_tokens
    │
    ├─→ Output Settings
    │   ├─→ base_dir
    │   ├─→ logs_dir
    │   ├─→ papers_dir
    │   └─→ generated_dir
    │
    └─→ Logging Settings
        ├─→ level
        ├─→ format
        └─→ file
```

## Extensibility Points

1. **New Task Types**
   - Add handler method in TaskAgent
   - Implement custom logic
   - Register in execute_task()

2. **New AI Models**
   - Create new client (like gemini_client.py)
   - Implement same interface
   - Update configuration

3. **New Output Formats**
   - Add method to DocumentGenerator
   - Implement conversion logic
   - Update generate_all_formats()

4. **Custom Workflows**
   - Create Workflow instance
   - Add Task objects
   - Run with agent.run_workflow()

## Performance Considerations

- **API Rate Limits**: Gemini API has rate limits
- **Token Limits**: Max 4096 tokens per request
- **File Size**: Large documents may need chunking
- **Memory**: Paper metadata stored in memory
- **Disk Space**: Generated files can be large

## Security Considerations

✅ **API Key Management**: Stored in .env (git-ignored)
✅ **Input Validation**: User inputs sanitized
✅ **File Permissions**: Output files properly secured
✅ **Error Messages**: No sensitive data in logs
✅ **CodeQL Scan**: 0 vulnerabilities found
