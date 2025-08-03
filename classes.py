from models import Article, Summary, GraphState
from typing import List, Dict
from langchain_core.messages import HumanMessage, SystemMessage
from datetime import datetime
from langchain_openai import ChatOpenAI
from tavily import TavilyClient
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url=os.getenv("OPENROUTER_BASE_URL"),
        model="openrouter/horizon-beta" 
)

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

class NewsSearcher:
    """
    Agent responsible for finding relevant Gen AI news articles
    using the Tavily search API
    """
    
    def search(self) -> List[Article]:
        """
        Performs news search with configured parameters
        
        Returns:
            List[Article]: Collection of found articles
        """
        response = tavily.search(
            query="Generative AI and Agentic AI news", 
            topic="news",
            time_period="1w",
            search_depth="advanced",
            max_results=5
        )
        
        articles = []
        for result in response['results']:
            articles.append(Article(
                title=result['title'],
                url=result['url'],
                content=result['content']
            ))
        
        return articles
    
class Summarizer:
    """
    Agent that processes articles and generates accessible summaries
    using an openrouter model
    """
    
    def __init__(self):
        self.system_prompt = """
        You are an AI expert who makes complex topics accessible 
        to general audiences. Summarize this article in 5 - 10 sentences, focusing on the key points 
        and explaining any technical terms simply.
        """
    
    def summarize(self, article: Article) -> str:
        """
        Generates an accessible summary of a single article
        
        Args:
            article (Article): Article to summarize
            
        Returns:
            str: Generated summary
        """
        response = llm.invoke([
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"Title: {article.title}\n\nContent: {article.content}")
        ])
        return response.content
    
class Publisher:
    """
    Agent that compiles summaries into a formatted report 
    and saves it to disk
    """
    
    def create_report(self, summaries: List[Dict]) -> str:
        """
        Creates and saves a formatted markdown report
        
        Args:
            summaries (List[Dict]): Collection of article summaries
            
        Returns:
            str: Generated report content
        """
        prompt = """
        Create a weekly Generative AI news report for the general public. 
        Format it with:
        1. A brief introduction
        2. The main news items with their summaries
        3. Links for further reading
        
        Make it engaging and accessible to non-technical readers.
        """
        
        # Format summaries for the LLM
        summaries_text = "\n\n".join([
            f"Title: {item['title']}\nSummary: {item['summary']}\nSource: {item['url']}"
            for item in summaries
        ])
        
        # Generate report
        response = llm.invoke([
            SystemMessage(content=prompt),
            HumanMessage(content=summaries_text)
        ])
        
        # Add metadata and save
        current_date = datetime.now().strftime("%Y-%m-%d")
        markdown_content = f"""
        Generated on: {current_date}

        {response.content}
        """
        
        filename = f"ai_news_report_{current_date}.md"
        with open(filename, 'w') as f:
            f.write(markdown_content)
        
        return response.content