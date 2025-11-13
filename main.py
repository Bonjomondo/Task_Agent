#!/usr/bin/env python3
"""
Main entry point for Task Agent
Example usage of the Task Agent for literature review
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from task_agent import TaskAgent


def main():
    """Main function demonstrating Task Agent usage"""
    
    print("=" * 70)
    print("Task Agent - AI-Powered Task Decomposition and Execution")
    print("=" * 70)
    print()
    
    # Initialize agent
    print("Initializing Task Agent...")
    try:
        agent = TaskAgent(config_path="config.yaml")
        print("✓ Agent initialized successfully")
        print()
    except Exception as e:
        print(f"✗ Error initializing agent: {e}")
        print("\nPlease ensure:")
        print("1. You have set GEMINI_API_KEY in .env file")
        print("2. All dependencies are installed (pip install -r requirements.txt)")
        return
    
    # Get topic from user
    print("=" * 70)
    print("Literature Review Generator")
    print("=" * 70)
    print()
    
    # Example topics
    example_topics = [
        "Machine Learning in Healthcare",
        "Quantum Computing Applications",
        "Climate Change Adaptation Strategies",
        "Blockchain Technology in Supply Chain"
    ]
    
    print("Example topics:")
    for i, topic in enumerate(example_topics, 1):
        print(f"  {i}. {topic}")
    print()
    
    # Get user input
    choice = input("Enter a number (1-4) or type your own topic: ").strip()
    
    if choice.isdigit() and 1 <= int(choice) <= 4:
        topic = example_topics[int(choice) - 1]
    else:
        topic = choice if choice else example_topics[0]
    
    print(f"\n✓ Selected topic: {topic}")
    print()
    
    # Create and run literature review workflow
    print("=" * 70)
    print("Starting Literature Review Workflow")
    print("=" * 70)
    print()
    
    try:
        success = agent.create_literature_review(topic)
        
        if success:
            print()
            print("=" * 70)
            print("✓ Literature Review Workflow Completed Successfully!")
            print("=" * 70)
            print()
            print("Generated files can be found in: output/generated/")
            print("Paper metadata: output/papers/papers_metadata.json")
            print("Execution log: output/logs/execution.log")
            print("=" * 70)
        else:
            print()
            print("=" * 70)
            print("✗ Workflow failed or was incomplete")
            print("=" * 70)
            print()
            print("Check output/logs/execution.log for details")
            
    except Exception as e:
        print(f"\n✗ Error during workflow execution: {e}")
        print("Check output/logs/execution.log for details")


if __name__ == "__main__":
    main()
