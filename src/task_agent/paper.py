"""
Paper processing and management
"""

import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class Paper:
    """Represents a research paper"""
    title: str
    authors: List[str] = field(default_factory=list)
    year: Optional[int] = None
    abstract: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    filepath: Optional[str] = None
    url: Optional[str] = None
    summary: Optional[str] = None
    key_findings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert paper to dictionary"""
        return {
            'title': self.title,
            'authors': self.authors,
            'year': self.year,
            'abstract': self.abstract,
            'keywords': self.keywords,
            'filepath': self.filepath,
            'url': self.url,
            'summary': self.summary,
            'key_findings': self.key_findings,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Paper':
        """Create paper from dictionary"""
        return cls(**data)


class PaperManager:
    """Manage research papers"""
    
    def __init__(self, papers_dir: str = "output/papers"):
        """
        Initialize paper manager
        
        Args:
            papers_dir: Directory to store papers and metadata
        """
        self.papers_dir = Path(papers_dir)
        self.papers_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.papers_dir / "papers_metadata.json"
        self.papers: List[Paper] = []
        
        # Load existing papers
        self._load_metadata()
        logger.info(f"Initialized PaperManager with {len(self.papers)} papers")
    
    def _load_metadata(self):
        """Load papers metadata from JSON file"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.papers = [Paper.from_dict(p) for p in data]
                logger.info(f"Loaded {len(self.papers)} papers from metadata")
            except Exception as e:
                logger.error(f"Error loading papers metadata: {e}")
                self.papers = []
    
    def _save_metadata(self):
        """Save papers metadata to JSON file"""
        try:
            data = [paper.to_dict() for paper in self.papers]
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(self.papers)} papers to metadata")
        except Exception as e:
            logger.error(f"Error saving papers metadata: {e}")
    
    def add_paper(self, paper: Paper):
        """Add a paper to the collection"""
        self.papers.append(paper)
        self._save_metadata()
        logger.info(f"Added paper: {paper.title}")
    
    def add_paper_from_file(self, filepath: str, title: str, 
                           authors: List[str] = None, **kwargs) -> Paper:
        """
        Add a paper from a file
        
        Args:
            filepath: Path to paper file
            title: Paper title
            authors: List of authors
            **kwargs: Additional paper attributes
            
        Returns:
            Created Paper object
        """
        paper = Paper(
            title=title,
            authors=authors or [],
            filepath=filepath,
            **kwargs
        )
        self.add_paper(paper)
        return paper
    
    def get_paper_by_title(self, title: str) -> Optional[Paper]:
        """Get paper by title"""
        for paper in self.papers:
            if paper.title.lower() == title.lower():
                return paper
        return None
    
    def list_papers(self) -> List[Paper]:
        """Get all papers"""
        return self.papers
    
    def update_paper_summary(self, title: str, summary: str, key_findings: List[str] = None):
        """Update paper summary and key findings"""
        paper = self.get_paper_by_title(title)
        if paper:
            paper.summary = summary
            if key_findings:
                paper.key_findings = key_findings
            self._save_metadata()
            logger.info(f"Updated summary for paper: {title}")
    
    def generate_papers_summary(self) -> str:
        """Generate a summary of all papers"""
        if not self.papers:
            return "No papers available."
        
        summary = "# Papers Summary\n\n"
        
        for i, paper in enumerate(self.papers, 1):
            summary += f"## {i}. {paper.title}\n\n"
            
            if paper.authors:
                summary += f"**Authors:** {', '.join(paper.authors)}\n\n"
            
            if paper.year:
                summary += f"**Year:** {paper.year}\n\n"
            
            if paper.abstract:
                summary += f"**Abstract:** {paper.abstract}\n\n"
            
            if paper.summary:
                summary += f"**Summary:** {paper.summary}\n\n"
            
            if paper.key_findings:
                summary += "**Key Findings:**\n"
                for finding in paper.key_findings:
                    summary += f"- {finding}\n"
                summary += "\n"
            
            summary += "---\n\n"
        
        return summary
    
    def export_metadata(self, filepath: str):
        """Export papers metadata to a custom file"""
        data = [paper.to_dict() for paper in self.papers]
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Exported papers metadata to: {filepath}")
