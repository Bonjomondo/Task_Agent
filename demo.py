#!/usr/bin/env python3
"""
Demo script that shows Task Agent functionality without requiring API key
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from task_agent.task import Task, TaskStatus, Workflow
from task_agent.paper import Paper, PaperManager
from task_agent.document import DocumentGenerator


def demo_task_decomposition():
    """Demo task decomposition structure"""
    print("=" * 70)
    print("Demo: Task Decomposition")
    print("=" * 70)
    print()
    
    # Simulated task decomposition
    main_task = "Write a literature review on Machine Learning in Healthcare"
    print(f"Main Task: {main_task}")
    print()
    print("Agent decomposes this into subtasks:")
    print()
    
    tasks = [
        Task(id="task_1", title="Collect Relevant Papers", 
             description="Search and identify relevant research papers"),
        Task(id="task_2", title="Upload Papers", 
             description="Download and upload papers to the system",
             status=TaskStatus.WAITING_USER),
        Task(id="task_3", title="Analyze Papers", 
             description="Read and extract key findings from papers"),
        Task(id="task_4", title="Create Outline", 
             description="Generate comprehensive outline for review"),
        Task(id="task_5", title="Write Review", 
             description="Write complete literature review section by section"),
    ]
    
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task.title}")
        print(f"   Description: {task.description}")
        print(f"   Status: {task.status.value}")
        print()


def demo_paper_management():
    """Demo paper management"""
    print("=" * 70)
    print("Demo: Paper Management")
    print("=" * 70)
    print()
    
    paper_manager = PaperManager(papers_dir="output/papers")
    
    # Add sample papers
    papers = [
        Paper(
            title="Deep Learning for Medical Image Analysis",
            authors=["Smith, J.", "Johnson, A."],
            year=2022,
            abstract="This paper presents a comprehensive review of deep learning techniques for medical imaging.",
            keywords=["deep learning", "medical imaging", "CNN"]
        ),
        Paper(
            title="Machine Learning in Clinical Decision Support",
            authors=["Brown, M.", "Davis, R."],
            year=2023,
            abstract="An exploration of machine learning applications in clinical decision support systems.",
            keywords=["machine learning", "clinical decision", "healthcare AI"]
        ),
        Paper(
            title="Natural Language Processing for Electronic Health Records",
            authors=["Wilson, K.", "Taylor, L."],
            year=2021,
            abstract="Review of NLP techniques for extracting information from EHRs.",
            keywords=["NLP", "EHR", "information extraction"]
        )
    ]
    
    for paper in papers:
        paper_manager.add_paper(paper)
    
    print(f"Added {len(papers)} papers to the collection")
    print()
    print("Paper Collection Summary:")
    print()
    
    for i, paper in enumerate(paper_manager.list_papers(), 1):
        print(f"{i}. {paper.title}")
        print(f"   Authors: {', '.join(paper.authors)}")
        print(f"   Year: {paper.year}")
        print(f"   Keywords: {', '.join(paper.keywords)}")
        print()


def demo_document_generation():
    """Demo document generation"""
    print("=" * 70)
    print("Demo: Document Generation")
    print("=" * 70)
    print()
    
    doc_gen = DocumentGenerator(output_dir="output/generated")
    
    # Sample content
    content = """# Machine Learning in Healthcare: A Literature Review

## Abstract

This literature review examines the applications of machine learning in healthcare, 
focusing on recent advances in medical imaging, clinical decision support, and 
electronic health record analysis.

## Introduction

Machine learning has revolutionized many aspects of healthcare delivery and medical research.
This review synthesizes recent findings from the literature to provide a comprehensive 
overview of the field.

## Medical Imaging

Deep learning techniques, particularly convolutional neural networks (CNNs), have shown 
remarkable success in medical image analysis. Key applications include:

- Automated disease detection
- Image segmentation
- Diagnostic assistance

### Deep Learning Architectures

Recent studies have demonstrated that advanced architectures such as ResNet, U-Net, 
and Vision Transformers achieve high accuracy in various medical imaging tasks.

## Clinical Decision Support

Machine learning models are increasingly used to support clinical decision-making:

1. Risk prediction models
2. Treatment recommendation systems
3. Patient monitoring and alerts

## Natural Language Processing

NLP techniques extract valuable information from unstructured clinical text:

- Named entity recognition for medical concepts
- Clinical note summarization
- Automated coding and billing

## Discussion

The integration of machine learning in healthcare shows promising results but faces 
challenges including data privacy, model interpretability, and clinical validation.

## Conclusion

Machine learning continues to transform healthcare, offering new opportunities for 
improved patient outcomes and operational efficiency. Future research should focus 
on addressing current limitations and ensuring equitable access to these technologies.

## References

1. Smith, J. & Johnson, A. (2022). Deep Learning for Medical Image Analysis.
2. Brown, M. & Davis, R. (2023). Machine Learning in Clinical Decision Support.
3. Wilson, K. & Taylor, L. (2021). Natural Language Processing for Electronic Health Records.
"""
    
    # Generate all formats
    print("Generating documents in multiple formats...")
    print()
    
    filename = "demo_literature_review"
    files = doc_gen.generate_all_formats(content, filename)
    
    print("Generated files:")
    for format_type, filepath in files.items():
        print(f"  - {format_type.upper()}: {filepath}")
    
    print()
    print("You can find these files in the output/generated/ directory")


def demo_workflow_execution():
    """Demo workflow execution"""
    print("=" * 70)
    print("Demo: Workflow Execution")
    print("=" * 70)
    print()
    
    workflow = Workflow(
        id="demo_workflow",
        title="Literature Review Workflow",
        description="Demo workflow for literature review creation"
    )
    
    # Add tasks
    tasks = [
        Task(id="task_1", title="Research Planning", description="Define research scope"),
        Task(id="task_2", title="Paper Collection", description="Gather relevant papers"),
        Task(id="task_3", title="Analysis", description="Analyze collected papers"),
        Task(id="task_4", title="Writing", description="Write the review"),
    ]
    
    for task in tasks:
        workflow.add_task(task)
    
    print(f"Workflow: {workflow.title}")
    print()
    print("Tasks:")
    
    # Simulate execution
    for i, task in enumerate(workflow.tasks, 1):
        print(f"\n{i}. {task.title}")
        print(f"   Status: {task.status.value} → ", end="")
        
        # Simulate execution
        task.status = TaskStatus.IN_PROGRESS
        print(f"{task.status.value} → ", end="")
        
        task.status = TaskStatus.COMPLETED
        print(f"{task.status.value}")
    
    print()
    print(f"Workflow Status: {'Complete' if workflow.is_complete() else 'In Progress'}")
    
    # Save workflow
    workflow.save("output/demo_workflow.json")
    print(f"\nWorkflow saved to: output/demo_workflow.json")


def main():
    """Run all demos"""
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "Task Agent - Feature Demonstration" + " " * 19 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    demos = [
        ("Task Decomposition", demo_task_decomposition),
        ("Paper Management", demo_paper_management),
        ("Document Generation", demo_document_generation),
        ("Workflow Execution", demo_workflow_execution),
    ]
    
    for i, (name, demo_func) in enumerate(demos, 1):
        if i > 1:
            input("\nPress Enter to continue to next demo...")
            print()
        
        demo_func()
    
    print()
    print("=" * 70)
    print("Demo Complete!")
    print("=" * 70)
    print()
    print("To use the full agent with AI capabilities:")
    print("1. Set up your Gemini API key in .env file")
    print("2. Run: python main.py")
    print()


if __name__ == "__main__":
    main()
