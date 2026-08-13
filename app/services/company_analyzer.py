import json
import re
from app.services.llm.base import LLMBase
from app.services.search.base import WebSearchBase


class CompanyAnalyzer:

    def __init__(self, llm_client: LLMBase, search_client: WebSearchBase):
        self.llm = llm_client
        self.search = search_client

    def analyze(self, company_name: str) -> dict:
        search_results = self.search.search(
            f"{company_name} company reviews employees culture glassdoor",
            max_results=5
        )

        context = "\n\n".join([
            f"Source: {r['url']}\nTitle: {r['title']}\n{r['snippet']}"
            for r in search_results
        ])

        sources = [r['url'] for r in search_results]

        prompt = f"""
        Based on the following search results, analyze the reputation of the company "{company_name}".
        
        Search results:
        {context}
        
        Respond in JSON format:
        {{
            "company_name": "{company_name}",
            "reputation_score": "positive/neutral/negative/unknown",
            "summary": "brief summary of company reputation",
            "red_flags": ["flag1", "flag2"],
            "positive_signals": ["signal1", "signal2"],
            "sources_consulted": {json.dumps(sources)}
        }}
        
        Respond ONLY with the JSON, no additional text.
        """

        response = self.llm.complete(prompt)
        
        if isinstance(response, dict):
            response["sources_consulted"] = sources
            return response
        
        json_match = re.search(r'\{{.*\}}', str(response), re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            result["sources_consulted"] = sources
            return result
            
        return {
            "company_name": company_name,
            "reputation_score": "unknown",
            "summary": "Could not analyze company reputation",
            "red_flags": [],
            "positive_signals": [],
            "sources_consulted": sources
        }