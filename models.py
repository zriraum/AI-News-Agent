from pydantic import BaseModel
from typing import List, Optional, TypedDict

class Article(BaseModel):
    """
    Represents a single news article
    
    Attributes:
        title (str): Article headline
        url (str): Source URL
        content (str): Article content
    """
    title: str
    url: str
    content: str

class Summary(TypedDict):
    """
    Represents a processed article summary
    
    Attributes:
        title (str): Original article title
        summary (str): Generated summary
        url (str): Source URL for reference
    """
    title: str
    summary: str
    url: str

# This defines what information we can store and pass between nodes later
class GraphState(TypedDict):
    """
    Maintains workflow state between agents
    
    Attributes:
        articles (Optional[List[Article]]): Found articles
        summaries (Optional[List[Summary]]): Generated summaries
        report (Optional[str]): Final compiled report
    """
    articles: Optional[List[Article]] 
    summaries: Optional[List[Summary]] 
    report: Optional[str] 