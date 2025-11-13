"""
Task Agent - AI-powered task decomposition and execution system
"""

__version__ = "1.0.0"
__author__ = "Task Agent Team"

from .agent import TaskAgent
from .task import Task, TaskStatus

__all__ = ['TaskAgent', 'Task', 'TaskStatus']
