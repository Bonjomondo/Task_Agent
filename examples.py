#!/usr/bin/env python3
"""
Advanced example showing custom workflow creation
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from task_agent import TaskAgent, Task, TaskStatus


def example_custom_workflow():
    """Example of creating a custom workflow"""
    
    print("Creating custom workflow...")
    
    # Initialize agent
    agent = TaskAgent()
    
    # Create custom workflow
    workflow = agent.create_workflow(
        title="Custom Research Review",
        description="Deep Learning in Natural Language Processing"
    )
    
    # Add custom tasks
    workflow.add_task(Task(
        id="task_1",
        title="Literature Search",
        description="Search for papers on deep learning NLP architectures"
    ))
    
    workflow.add_task(Task(
        id="task_2",
        title="Paper Collection",
        description="Collect 10-15 relevant papers",
        status=TaskStatus.WAITING_USER
    ))
    
    workflow.add_task(Task(
        id="task_3",
        title="Paper Analysis",
        description="Analyze papers and extract key contributions"
    ))
    
    workflow.add_task(Task(
        id="task_4",
        title="Outline Creation",
        description="Create comprehensive review outline"
    ))
    
    workflow.add_task(Task(
        id="task_5",
        title="Writing",
        description="Write full literature review"
    ))
    
    # Run workflow
    print(f"Running workflow: {workflow.title}")
    agent.run_workflow(workflow)


def example_add_papers():
    """Example of adding papers manually"""
    
    print("Adding papers manually...")
    
    agent = TaskAgent()
    
    # Add papers
    papers = [
        {
            'title': 'Attention Is All You Need',
            'authors': ['Vaswani, A.', 'Shazeer, N.', 'Parmar, N.'],
            'year': 2017,
            'abstract': 'The dominant sequence transduction models are based on complex recurrent or convolutional neural networks...',
            'keywords': ['transformer', 'attention', 'neural networks']
        },
        {
            'title': 'BERT: Pre-training of Deep Bidirectional Transformers',
            'authors': ['Devlin, J.', 'Chang, M.W.', 'Lee, K.'],
            'year': 2018,
            'abstract': 'We introduce a new language representation model called BERT...',
            'keywords': ['BERT', 'pre-training', 'transformers']
        }
    ]
    
    agent.add_papers(papers)
    print(f"Added {len(papers)} papers")
    
    # Generate papers summary
    summary = agent.paper_manager.generate_papers_summary()
    print("\nPapers Summary:")
    print(summary)


def example_task_decomposition():
    """Example of task decomposition"""
    
    print("Task Decomposition Example")
    
    agent = TaskAgent()
    
    # Decompose a complex task
    main_task = "Write a systematic review on the applications of artificial intelligence in medical diagnosis"
    
    print(f"\nMain Task: {main_task}\n")
    print("Decomposing into subtasks...")
    
    subtasks = agent.decompose_task(main_task)
    
    print(f"\nGenerated {len(subtasks)} subtasks:")
    for i, task in enumerate(subtasks, 1):
        print(f"\n{i}. {task.title}")
        print(f"   Description: {task.description}")
        print(f"   Status: {task.status.value}")


def main():
    """Main function with menu"""
    
    print("=" * 70)
    print("Task Agent - Advanced Examples")
    print("=" * 70)
    print()
    
    print("Select an example:")
    print("1. Custom Workflow")
    print("2. Add Papers Manually")
    print("3. Task Decomposition Demo")
    print()
    
    choice = input("Enter choice (1-3): ").strip()
    
    print()
    print("=" * 70)
    print()
    
    if choice == "1":
        example_custom_workflow()
    elif choice == "2":
        example_add_papers()
    elif choice == "3":
        example_task_decomposition()
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
