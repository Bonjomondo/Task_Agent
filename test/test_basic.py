"""
Basic tests for Task Agent
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from task_agent.task import Task, TaskStatus, Workflow
from task_agent.paper import Paper, PaperManager
import tempfile
import shutil


def test_task_creation():
    """Test task creation and manipulation"""
    print("Testing task creation...")
    
    task = Task(
        id="test_1",
        title="Test Task",
        description="This is a test task"
    )
    
    assert task.id == "test_1"
    assert task.title == "Test Task"
    assert task.status == TaskStatus.PENDING
    
    # Test status change
    task.status = TaskStatus.IN_PROGRESS
    assert task.status == TaskStatus.IN_PROGRESS
    
    # Test dict conversion
    task_dict = task.to_dict()
    assert task_dict['id'] == "test_1"
    assert task_dict['status'] == "in_progress"
    
    print("✓ Task creation test passed")


def test_workflow():
    """Test workflow creation and management"""
    print("Testing workflow...")
    
    workflow = Workflow(
        id="test_workflow",
        title="Test Workflow",
        description="Testing workflow functionality"
    )
    
    # Add tasks
    task1 = Task(id="t1", title="Task 1", description="First task")
    task2 = Task(id="t2", title="Task 2", description="Second task")
    
    workflow.add_task(task1)
    workflow.add_task(task2)
    
    assert len(workflow.tasks) == 2
    
    # Test current task
    current = workflow.get_current_task()
    assert current.id == "t1"
    
    # Move to next task
    assert workflow.next_task() == True
    current = workflow.get_current_task()
    assert current.id == "t2"
    
    # Try to move beyond last task
    assert workflow.next_task() == False
    
    print("✓ Workflow test passed")


def test_paper_management():
    """Test paper management"""
    print("Testing paper management...")
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        paper_manager = PaperManager(papers_dir=temp_dir)
        
        # Add paper
        paper = Paper(
            title="Test Paper",
            authors=["Author 1", "Author 2"],
            year=2023,
            abstract="Test abstract"
        )
        
        paper_manager.add_paper(paper)
        
        # Verify paper was added
        papers = paper_manager.list_papers()
        assert len(papers) == 1
        assert papers[0].title == "Test Paper"
        
        # Test finding paper
        found = paper_manager.get_paper_by_title("Test Paper")
        assert found is not None
        assert found.year == 2023
        
        print("✓ Paper management test passed")
        
    finally:
        # Cleanup
        shutil.rmtree(temp_dir)


def test_workflow_serialization():
    """Test workflow save/load"""
    print("Testing workflow serialization...")
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        workflow = Workflow(
            id="test_wf",
            title="Test Workflow",
            description="Test"
        )
        
        task = Task(id="t1", title="Task 1", description="Test task")
        workflow.add_task(task)
        
        # Save workflow
        filepath = os.path.join(temp_dir, "workflow.json")
        workflow.save(filepath)
        
        # Load workflow
        loaded_workflow = Workflow.load(filepath)
        
        assert loaded_workflow.id == workflow.id
        assert loaded_workflow.title == workflow.title
        assert len(loaded_workflow.tasks) == 1
        assert loaded_workflow.tasks[0].id == "t1"
        
        print("✓ Workflow serialization test passed")
        
    finally:
        shutil.rmtree(temp_dir)


def run_all_tests():
    """Run all tests"""
    print("=" * 70)
    print("Running Task Agent Tests")
    print("=" * 70)
    print()
    
    try:
        test_task_creation()
        test_workflow()
        test_paper_management()
        test_workflow_serialization()
        
        print()
        print("=" * 70)
        print("✓ All tests passed!")
        print("=" * 70)
        return True
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
