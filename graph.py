from classes import NewsSearcher, Summarizer, Publisher
from models import Article, Summary, GraphState
from langgraph.graph import StateGraph
from typing import Dict, Any

def search_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node for article search
    
    Args:
        state (Dict[str, Any]): Current workflow state
        
    Returns:
        Dict[str, Any]: Updated state with found articles
    """
    searcher = NewsSearcher()
    state['articles'] = searcher.search() 
    return state

def summarize_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node for article summarization
    
    Args:
        state (Dict[str, Any]): Current workflow state
        
    Returns:
        Dict[str, Any]: Updated state with summaries
    """
    summarizer = Summarizer()
    state['summaries'] = []
    
    for article in state['articles']: # Uses articles from previous node
        summary = summarizer.summarize(article)
        state['summaries'].append({
            'title': article.title,
            'summary': summary,
            'url': article.url
        })
    return state

def publish_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Node for report generation
    
    Args:
        state (Dict[str, Any]): Current workflow state
        
    Returns:
        Dict[str, Any]: Updated state with final report
    """
    publisher = Publisher()
    report_content = publisher.create_report(state['summaries'])
    state['report'] = report_content
    return state


def create_workflow() -> StateGraph:
    """
    Constructs and configures the workflow graph
    search -> summarize -> publish
    
    Returns:
        StateGraph: Compiled workflow ready for execution
    """
    
    # Create a workflow (graph) initialized with our state schema
    workflow = StateGraph(state_schema=GraphState)
    
    # Add processing nodes that we will flow between
    workflow.add_node("search", search_node)
    workflow.add_node("summarize", summarize_node)
    workflow.add_node("publish", publish_node)
    
    # Define the flow with edges
    workflow.add_edge("search", "summarize") # search results flow to summarizer
    workflow.add_edge("summarize", "publish") # summaries flow to publisher
    
    # Set where to start
    workflow.set_entry_point("search")
    
    return workflow.compile()








