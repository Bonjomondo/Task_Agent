#!/usr/bin/env python3
"""
Integration test demonstrating the complete workflow
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from task_agent import TaskAgent, Task, TaskStatus
from task_agent.paper import Paper
from task_agent.document import DocumentGenerator
import tempfile
import shutil


def test_complete_workflow():
    """Test complete literature review workflow"""
    print("=" * 70)
    print("Integration Test: Complete Workflow")
    print("=" * 70)
    print()
    
    # Create temporary directories
    temp_base = tempfile.mkdtemp()
    
    try:
        # Initialize agent with temp directories
        temp_output = os.path.join(temp_base, 'output')
        temp_papers = os.path.join(temp_base, 'papers')
        temp_generated = os.path.join(temp_base, 'generated')
        
        os.makedirs(temp_output, exist_ok=True)
        os.makedirs(temp_papers, exist_ok=True)
        os.makedirs(temp_generated, exist_ok=True)
        
        # Create agent without Gemini (for testing structure only)
        print("✓ Setting up test environment")
        
        # Test 1: Task decomposition structure
        print("\n1. Testing task decomposition structure...")
        from task_agent.task import Workflow
        
        workflow = Workflow(
            id="test_workflow",
            title="Test Literature Review",
            description="Test workflow for ML in Healthcare"
        )
        
        tasks = [
            Task(id="task_1", title="Collect Papers", description="Find relevant papers"),
            Task(id="task_2", title="Upload Papers", description="Upload papers", 
                 status=TaskStatus.WAITING_USER),
            Task(id="task_3", title="Analyze Papers", description="Analyze papers"),
            Task(id="task_4", title="Create Outline", description="Create outline"),
            Task(id="task_5", title="Write Review", description="Write full review"),
        ]
        
        for task in tasks:
            workflow.add_task(task)
        
        assert len(workflow.tasks) == 5
        print(f"   ✓ Created workflow with {len(workflow.tasks)} tasks")
        
        # Test 2: Paper management
        print("\n2. Testing paper management...")
        from task_agent.paper import PaperManager
        
        paper_manager = PaperManager(papers_dir=temp_papers)
        
        papers = [
            Paper(
                title="Deep Learning in Medical Imaging",
                authors=["Smith, J.", "Doe, A."],
                year=2023,
                abstract="A comprehensive review of deep learning applications in medical imaging.",
                keywords=["deep learning", "medical imaging"]
            ),
            Paper(
                title="AI in Clinical Decision Support",
                authors=["Johnson, M."],
                year=2022,
                abstract="Exploring AI applications in clinical decision making.",
                keywords=["AI", "clinical decision support"]
            )
        ]
        
        for paper in papers:
            paper_manager.add_paper(paper)
        
        assert len(paper_manager.list_papers()) == 2
        print(f"   ✓ Added {len(papers)} papers to collection")
        
        # Verify metadata file
        assert os.path.exists(os.path.join(temp_papers, "papers_metadata.json"))
        print("   ✓ Papers metadata saved to JSON")
        
        # Test 3: Document generation
        print("\n3. Testing document generation...")
        doc_gen = DocumentGenerator(output_dir=temp_generated)
        
        sample_content = """# Test Literature Review

## Introduction

This is a test literature review demonstrating the document generation capabilities.

## Background

Machine learning has revolutionized healthcare:

- Improved diagnosis accuracy
- Faster treatment planning
- Better patient outcomes

## Methods

We analyzed 10 papers using the following criteria:

1. Publication date (2020-2023)
2. Peer-reviewed journals
3. Focus on clinical applications

## Results

### Deep Learning Applications

Deep learning models showed significant improvements.

### Clinical Impact

The clinical impact was measured across multiple dimensions.

## Discussion

Our findings suggest that AI integration in healthcare is promising.

## Conclusion

This review demonstrates the potential of AI in healthcare.
"""
        
        files = doc_gen.generate_all_formats(sample_content, "test_review")
        
        assert os.path.exists(files['md'])
        assert os.path.exists(files['docx'])
        assert os.path.exists(files['pdf'])
        
        print("   ✓ Generated Markdown document")
        print("   ✓ Generated DOCX document")
        print("   ✓ Generated PDF document")
        
        # Test 4: Workflow state management
        print("\n4. Testing workflow state management...")
        
        workflow_file = os.path.join(temp_output, "test_workflow.json")
        workflow.save(workflow_file)
        
        assert os.path.exists(workflow_file)
        print("   ✓ Workflow saved to JSON")
        
        loaded_workflow = Workflow.load(workflow_file)
        assert loaded_workflow.id == workflow.id
        assert len(loaded_workflow.tasks) == len(workflow.tasks)
        print("   ✓ Workflow loaded from JSON")
        
        # Test 5: Task execution simulation
        print("\n5. Testing task execution simulation...")
        
        for i, task in enumerate(workflow.tasks):
            if task.status != TaskStatus.WAITING_USER:
                task.status = TaskStatus.IN_PROGRESS
                task.status = TaskStatus.COMPLETED
                task.result = f"Task {i+1} completed successfully"
        
        completed_tasks = sum(1 for t in workflow.tasks if t.status == TaskStatus.COMPLETED)
        print(f"   ✓ Executed {completed_tasks} automated tasks")
        
        # Test 6: Output structure verification
        print("\n6. Verifying output structure...")
        
        assert os.path.isdir(temp_papers)
        assert os.path.isdir(temp_generated)
        assert os.path.isdir(temp_output)
        
        print("   ✓ All output directories created")
        print("   ✓ Papers metadata stored in JSON")
        print("   ✓ Workflow state saved")
        print("   ✓ Documents generated in multiple formats")
        
        print()
        print("=" * 70)
        print("✓ Integration Test PASSED")
        print("=" * 70)
        print()
        print("Summary:")
        print(f"  - Workflow tasks: {len(workflow.tasks)}")
        print(f"  - Papers managed: {len(paper_manager.list_papers())}")
        print(f"  - Formats generated: 3 (MD, DOCX, PDF)")
        print(f"  - State files created: 2 (workflow, papers metadata)")
        print()
        
        return True
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Cleanup
        shutil.rmtree(temp_base, ignore_errors=True)


if __name__ == "__main__":
    success = test_complete_workflow()
    sys.exit(0 if success else 1)
