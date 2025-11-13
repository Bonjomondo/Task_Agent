"""
Task data structures and state management
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
import json


class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    WAITING_USER = "waiting_user"


@dataclass
class Task:
    """Represents a single task in the workflow"""
    id: str
    title: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status.value,
            'result': self.result,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Create task from dictionary"""
        data['status'] = TaskStatus(data['status'])
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        if data['completed_at']:
            data['completed_at'] = datetime.fromisoformat(data['completed_at'])
        return cls(**data)


@dataclass
class Workflow:
    """Represents a complete workflow with multiple tasks"""
    id: str
    title: str
    description: str
    tasks: List[Task] = field(default_factory=list)
    current_task_index: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_task(self, task: Task):
        """Add a task to the workflow"""
        self.tasks.append(task)
    
    def get_current_task(self) -> Optional[Task]:
        """Get the current task"""
        if 0 <= self.current_task_index < len(self.tasks):
            return self.tasks[self.current_task_index]
        return None
    
    def next_task(self) -> bool:
        """Move to next task, return True if successful"""
        if self.current_task_index < len(self.tasks) - 1:
            self.current_task_index += 1
            return True
        return False
    
    def is_complete(self) -> bool:
        """Check if all tasks are completed"""
        return all(task.status == TaskStatus.COMPLETED for task in self.tasks)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert workflow to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'tasks': [task.to_dict() for task in self.tasks],
            'current_task_index': self.current_task_index,
            'created_at': self.created_at.isoformat(),
            'metadata': self.metadata
        }
    
    def save(self, filepath: str):
        """Save workflow to JSON file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load(cls, filepath: str) -> 'Workflow':
        """Load workflow from JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['tasks'] = [Task.from_dict(task_data) for task_data in data['tasks']]
        return cls(**data)
