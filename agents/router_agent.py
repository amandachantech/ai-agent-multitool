# ai-agent-multitool/agents/router_agent.py
from typing import Dict, Any, Optional


class RouterAgent:
    def __init__(self, chat_agent: Any, pdf_agent: Optional[Any], csv_agent: Optional[Any]):
        
        self.chat_agent = chat_agent
        self.pdf_agent = pdf_agent
        self.csv_agent = csv_agent

        
        self.pdf_keywords = [
            "pdf", "document", "paper", "file", "section", "paragraph", "according to the document"
        ]
        self.csv_keywords = [
            "csv", "table", "dataset", "data", "chart", "plot", "bar", "line", "scatter",
            "trend"
        ]


    def _score(self, text: str, keywords: list[str]) -> int:
        t = (text or "").lower()
        return sum(1 for kw in keywords if kw in t)

    def route(self, user_query: str, resources: Dict[str, Any]) -> Dict[str, Any]:
        """
    
        resources:
          - has_pdf: bool
          - has_csv: bool
          - pdf_loaded: bool         
          - csv_df: Optional[DataFrame]
        return:
          {"tool": "chat"|"pdf"|"csv", "output": Any}
        """

        pdf_score = self._score(user_query, self.pdf_keywords)
        csv_score = self._score(user_query, self.csv_keywords)


        if not resources.get("has_pdf") or not resources.get("pdf_loaded"):
            pdf_score = 0
        if not resources.get("has_csv") or resources.get("csv_df") is None:
            csv_score = 0


        if pdf_score == 0 and csv_score == 0:
            tool = "chat"
        elif pdf_score >= csv_score:
            tool = "pdf"
        else:
            tool = "csv"


        if tool == "pdf" and self.pdf_agent is not None:
            result = self.pdf_agent.run(user_query)
            return {"tool": "pdf", "output": result}

        if tool == "csv" and self.csv_agent is not None:
            result = self.csv_agent.run(user_query)
            return {"tool": "csv", "output": result}

   
        if self.chat_agent is None:
            
            return {"tool": "chat", "output": "No available tools. Please provide an API key or upload resources."}
        reply = self.chat_agent.run(user_query)
        return {"tool": "chat", "output": reply}
