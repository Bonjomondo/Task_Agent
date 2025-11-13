"""
Main Task Agent - AI-powered task decomposition and execution
"""

import os
import logging
import yaml
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
import json

from .gemini_client import GeminiClient
from .task import Task, TaskStatus, Workflow
from .document import DocumentGenerator
from .paper import PaperManager, Paper

# Setup logging
def setup_logging(log_file: str = "output/logs/execution.log"):
    """Setup logging configuration"""
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

setup_logging()
logger = logging.getLogger(__name__)


class TaskAgent:
    """Main agent for task decomposition and execution"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize Task Agent
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        
        # Initialize components
        self.gemini = GeminiClient(
            model=self.config.get('ai', {}).get('model', 'gemini-pro')
        )
        
        output_dir = self.config.get('output', {}).get('generated_dir', 'output/generated')
        self.doc_generator = DocumentGenerator(output_dir)
        
        papers_dir = self.config.get('output', {}).get('papers_dir', 'output/papers')
        self.paper_manager = PaperManager(papers_dir)
        
        self.current_workflow: Optional[Workflow] = None
        
        logger.info("TaskAgent initialized successfully")
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            logger.info(f"Loaded configuration from {config_path}")
            return config
        except Exception as e:
            logger.warning(f"Could not load config file: {e}. Using defaults.")
            return {}
    
    def create_workflow(self, title: str, description: str) -> Workflow:
        """
        Create a new workflow
        
        Args:
            title: Workflow title
            description: Workflow description
            
        Returns:
            Created workflow
        """
        workflow = Workflow(
            id=f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            title=title,
            description=description
        )
        
        self.current_workflow = workflow
        logger.info(f"Created workflow: {title}")
        return workflow
    
    def decompose_task(self, main_task: str) -> List[Task]:
        """
        Decompose a main task into subtasks using AI
        
        Args:
            main_task: Main task description
            
        Returns:
            List of subtasks
        """
        logger.info(f"Decomposing task: {main_task}")
        
        prompt = f"""You are a task planning expert. Break down the following task into clear, actionable subtasks.

Main Task: {main_task}

For a literature review task, typical steps include:
1. Collect relevant papers (search and identify)
2. Wait for user to download and upload papers
3. Read and analyze uploaded papers
4. Create an outline/structure
5. Write sections one by one
6. Review and refine

Provide a numbered list of subtasks in the following format:
1. [Task Title]: [Detailed description]
2. [Task Title]: [Detailed description]
...

Keep each subtask focused and actionable."""

        try:
            response = self.gemini.generate(prompt, temperature=0.7)
            tasks = self._parse_subtasks(response)
            logger.info(f"Decomposed into {len(tasks)} subtasks")
            return tasks
        except Exception as e:
            logger.error(f"Error decomposing task: {e}")
            # Return default subtasks for literature review
            return self._get_default_review_tasks()
    
    def _parse_subtasks(self, response: str) -> List[Task]:
        """Parse AI response into Task objects"""
        tasks = []
        lines = response.strip().split('\n')
        
        task_num = 1
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Try to parse numbered items
            if line[0].isdigit() and ('. ' in line or ') ' in line):
                # Remove number prefix
                parts = line.split(': ', 1)
                if len(parts) == 2:
                    title = parts[0].split('. ', 1)[-1].split(') ', 1)[-1]
                    description = parts[1]
                else:
                    # No colon, use whole line as title
                    title = line.split('. ', 1)[-1].split(') ', 1)[-1]
                    description = title
                
                task = Task(
                    id=f"task_{task_num}",
                    title=title,
                    description=description
                )
                tasks.append(task)
                task_num += 1
        
        return tasks if tasks else self._get_default_review_tasks()
    
    def _get_default_review_tasks(self) -> List[Task]:
        """Get default tasks for literature review"""
        return [
            Task(id="task_1", title="Collect Relevant Papers", 
                 description="Search and identify relevant research papers for the review"),
            Task(id="task_2", title="Upload Papers", 
                 description="Download identified papers and upload them to the system",
                 status=TaskStatus.WAITING_USER),
            Task(id="task_3", title="Analyze Papers", 
                 description="Read and analyze the uploaded papers, extract key findings"),
            Task(id="task_4", title="Create Outline", 
                 description="Create a comprehensive outline for the literature review"),
            Task(id="task_5", title="Write Literature Review", 
                 description="Write the complete literature review section by section"),
        ]
    
    def execute_task(self, task: Task) -> bool:
        """
        Execute a single task
        
        Args:
            task: Task to execute
            
        Returns:
            True if task completed successfully
        """
        logger.info(f"Executing task: {task.title}")
        task.status = TaskStatus.IN_PROGRESS
        
        try:
            # Route to appropriate handler based on task type
            if "collect" in task.title.lower() or "search" in task.title.lower():
                result = self._handle_paper_collection(task)
            elif "upload" in task.title.lower() or "download" in task.title.lower():
                result = self._handle_paper_upload(task)
            elif "analyze" in task.title.lower() or "read" in task.title.lower():
                result = self._handle_paper_analysis(task)
            elif "outline" in task.title.lower() or "structure" in task.title.lower():
                result = self._handle_outline_creation(task)
            elif "write" in task.title.lower() or "review" in task.title.lower():
                result = self._handle_writing(task)
            else:
                # Generic task execution
                result = self._handle_generic_task(task)
            
            task.result = result
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            logger.info(f"Task completed: {task.title}")
            return True
            
        except Exception as e:
            logger.error(f"Error executing task {task.title}: {e}")
            task.status = TaskStatus.FAILED
            task.result = f"Error: {str(e)}"
            return False
    
    def _handle_paper_collection(self, task: Task) -> str:
        """Handle paper collection task"""
        logger.info("Handling paper collection")
        
        # Get topic from workflow description
        topic = self.current_workflow.description if self.current_workflow else "the topic"
        
        prompt = f"""Generate a list of important research papers for a literature review on: {topic}

Provide 5-10 relevant paper suggestions with:
- Title
- Authors (if known)
- Year
- Brief description of relevance

Format as a numbered list."""

        response = self.gemini.generate(prompt)
        task.metadata['suggested_papers'] = response
        
        return f"Generated paper suggestions:\n\n{response}\n\nNote: User needs to download and upload these papers."
    
    def _handle_paper_upload(self, task: Task) -> str:
        """Handle paper upload task (requires user action)"""
        logger.info("Handling paper upload - waiting for user")
        task.status = TaskStatus.WAITING_USER
        
        papers_dir = self.paper_manager.papers_dir
        
        return f"""Papers should be uploaded to: {papers_dir}

Instructions:
1. Download the suggested papers
2. Save them in the papers directory: {papers_dir}
3. Register them using the add_papers() method

Once papers are uploaded, continue to the next task."""
    
    def _handle_paper_analysis(self, task: Task) -> str:
        """Handle paper analysis task"""
        logger.info("Handling paper analysis")
        
        papers = self.paper_manager.list_papers()
        
        if not papers:
            return "No papers available for analysis. Please upload papers first."
        
        # Analyze each paper
        analysis_results = []
        
        for paper in papers:
            prompt = f"""Analyze the following research paper and provide:
1. A brief summary (2-3 sentences)
2. Key findings (3-5 bullet points)
3. Relevance to the literature review

Paper Title: {paper.title}
Authors: {', '.join(paper.authors) if paper.authors else 'Unknown'}
Abstract: {paper.abstract if paper.abstract else 'Not available'}

Provide a concise analysis."""

            try:
                analysis = self.gemini.generate(prompt)
                analysis_results.append(f"### {paper.title}\n\n{analysis}")
                
                # Update paper with analysis
                # Extract key findings from analysis
                key_findings = [line.strip('- ').strip() 
                               for line in analysis.split('\n') 
                               if line.strip().startswith('-')]
                
                self.paper_manager.update_paper_summary(
                    paper.title,
                    analysis,
                    key_findings[:5]
                )
                
            except Exception as e:
                logger.error(f"Error analyzing paper {paper.title}: {e}")
                analysis_results.append(f"### {paper.title}\n\nError analyzing paper: {e}")
        
        full_analysis = "\n\n".join(analysis_results)
        
        # Save analysis to metadata
        task.metadata['paper_analysis'] = full_analysis
        
        return f"Analyzed {len(papers)} papers.\n\n{full_analysis}"
    
    def _handle_outline_creation(self, task: Task) -> str:
        """Handle outline creation task"""
        logger.info("Handling outline creation")
        
        papers = self.paper_manager.list_papers()
        topic = self.current_workflow.description if self.current_workflow else "the topic"
        
        # Prepare papers summary for context
        papers_context = ""
        if papers:
            papers_context = "Available papers:\n"
            for paper in papers:
                papers_context += f"- {paper.title}"
                if paper.summary:
                    papers_context += f": {paper.summary[:200]}..."
                papers_context += "\n"
        
        prompt = f"""Create a comprehensive outline for a literature review on: {topic}

{papers_context}

The outline should include:
1. Introduction
2. Background/Context
3. Main themes/sections (3-5 major sections)
4. Discussion
5. Conclusion
6. References

For each section, provide:
- Section title
- 2-3 key points to cover
- Relevant papers to cite (if applicable)

Format as a structured markdown outline."""

        outline = self.gemini.generate(prompt, temperature=0.7, max_tokens=2048)
        
        # Save outline to workflow metadata
        if self.current_workflow:
            self.current_workflow.metadata['outline'] = outline
        
        task.metadata['outline'] = outline
        
        return outline
    
    def _handle_writing(self, task: Task) -> str:
        """Handle writing task - write the full review"""
        logger.info("Handling writing task")
        
        outline = ""
        if self.current_workflow and 'outline' in self.current_workflow.metadata:
            outline = self.current_workflow.metadata['outline']
        elif 'outline' in task.metadata:
            outline = task.metadata['outline']
        
        # Get papers context
        papers_summary = self.paper_manager.generate_papers_summary()
        topic = self.current_workflow.description if self.current_workflow else "the topic"
        
        # Generate the full review section by section
        prompt = f"""Write a comprehensive literature review on: {topic}

Use the following outline:
{outline}

Papers available for citation:
{papers_summary}

Write a complete, well-structured literature review with:
- Clear introduction
- Thorough analysis of the literature
- Proper flow between sections
- Insightful discussion
- Strong conclusion

Format in Markdown with proper headings and citations."""

        review_content = self.gemini.generate(prompt, temperature=0.7, max_tokens=4096)
        
        # Save the review
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"literature_review_{timestamp}"
        
        # Generate all formats
        output_files = self.doc_generator.generate_all_formats(review_content, filename)
        
        task.metadata['output_files'] = output_files
        task.metadata['review_content'] = review_content
        
        result = f"Literature review completed!\n\n"
        result += f"Generated files:\n"
        for format_type, filepath in output_files.items():
            result += f"- {format_type.upper()}: {filepath}\n"
        
        return result
    
    def _handle_generic_task(self, task: Task) -> str:
        """Handle generic task execution"""
        logger.info(f"Handling generic task: {task.title}")
        
        prompt = f"""Execute the following task:

Task: {task.title}
Description: {task.description}

Provide a detailed response on how to complete this task or the results of completing it."""

        result = self.gemini.generate(prompt)
        return result
    
    def run_workflow(self, workflow: Workflow) -> bool:
        """
        Run a complete workflow
        
        Args:
            workflow: Workflow to execute
            
        Returns:
            True if workflow completed successfully
        """
        logger.info(f"Starting workflow: {workflow.title}")
        self.current_workflow = workflow
        
        for i, task in enumerate(workflow.tasks):
            logger.info(f"Task {i+1}/{len(workflow.tasks)}: {task.title}")
            
            if task.status == TaskStatus.WAITING_USER:
                logger.info(f"Task requires user action: {task.title}")
                print(f"\n{'='*60}")
                print(f"USER ACTION REQUIRED: {task.title}")
                print(f"{task.description}")
                print(f"{'='*60}\n")
                
                # Wait for user to indicate completion
                input("Press Enter when ready to continue...")
                task.status = TaskStatus.COMPLETED
                task.completed_at = datetime.now()
                continue
            
            success = self.execute_task(task)
            
            if not success:
                logger.error(f"Workflow failed at task: {task.title}")
                return False
            
            # Print task result
            print(f"\n{'='*60}")
            print(f"TASK COMPLETED: {task.title}")
            print(f"{'='*60}")
            if task.result:
                print(task.result[:500])  # Print first 500 chars
                if len(task.result) > 500:
                    print("...")
            print(f"{'='*60}\n")
        
        logger.info(f"Workflow completed: {workflow.title}")
        
        # Save workflow state
        self._save_workflow(workflow)
        
        return True
    
    def _save_workflow(self, workflow: Workflow):
        """Save workflow state to file"""
        output_dir = Path(self.config.get('output', {}).get('base_dir', 'output'))
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = output_dir / f"{workflow.id}.json"
        workflow.save(str(filepath))
        logger.info(f"Saved workflow to: {filepath}")
    
    def create_literature_review(self, topic: str) -> bool:
        """
        Convenience method to create and run a literature review workflow
        
        Args:
            topic: Literature review topic
            
        Returns:
            True if successful
        """
        logger.info(f"Creating literature review workflow for: {topic}")
        
        # Create workflow
        workflow = self.create_workflow(
            title=f"Literature Review: {topic}",
            description=topic
        )
        
        # Decompose task
        tasks = self.decompose_task(f"Write a comprehensive literature review on {topic}")
        
        for task in tasks:
            workflow.add_task(task)
        
        # Run workflow
        return self.run_workflow(workflow)
    
    def add_papers(self, papers_info: List[Dict[str, Any]]):
        """
        Add papers to the paper manager
        
        Args:
            papers_info: List of paper dictionaries with title, authors, etc.
        """
        for info in papers_info:
            paper = Paper(
                title=info.get('title', ''),
                authors=info.get('authors', []),
                year=info.get('year'),
                abstract=info.get('abstract'),
                keywords=info.get('keywords', []),
                filepath=info.get('filepath'),
                url=info.get('url')
            )
            self.paper_manager.add_paper(paper)
        
        logger.info(f"Added {len(papers_info)} papers")
