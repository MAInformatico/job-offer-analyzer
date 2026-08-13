import os
import json
import yaml
from groq import Groq
from dotenv import load_dotenv
from app.services.llm.base import LLMBase

load_dotenv()

def load_config() -> dict:
    config_path = "config.yaml"
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            "config.yaml not found. Copy config.example.yaml to config.yaml and customize it."
        )
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


class GroqClient(LLMBase):
    
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"
        self.config = load_config()
    
    def _build_prompt(self, offer_text: str) -> str:
        criteria = self.config["criteria"]
        
        excluded = ", ".join(criteria.get("excluded_company_types", []))
        required_stack = ", ".join(criteria.get("required_stack", []))
        
        return f"""
        Analyze this job offer and determine if it's worth applying to.
        
        Evaluation criteria:
        - Work mode: {criteria.get("work_mode")}
        - Minimum salary: {criteria.get("min_salary")} EUR or equivalent
        - Contract type: {criteria.get("contract_type")}
        - Required stack: {required_stack}
        - Additional notes: {criteria.get("additional_notes")}
        
        Excluded company types: {excluded}
        
        IMPORTANT - Signs that indicate a consultancy or staffing agency (automatic disqualification):
        - Phrases like "top global clients", "project success rate", "we work for clients"
        - Mentions of "relocation program" as a selling point
        - "service partner", "outsourcing", "staffing"
        - No clear product of their own mentioned
        
        Job offer:
        {offer_text}
        
        Respond in JSON format:
        {{
            "should_apply": true/false,
            "reasons": ["reason1", "reason2"],
            "summary": "brief summary of the offer",
            "red_flags": ["flag1", "flag2"],
            "salary_info": "salary info if mentioned or null"
        }}
        
        Respond ONLY with the JSON, no additional text.
        """
    
    def analyze(self, offer_text: str) -> dict:
        prompt = self._build_prompt(offer_text)
        
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
        )
        
        content = response.choices[0].message.content.strip()
        
        # Extraer JSON aunque haya texto alrededor
        import re
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if not json_match:
            raise ValueError(f"No JSON found in LLM response: {content}")
        
        return json.loads(json_match.group())

    def complete(self, prompt: str) -> dict:
        import re
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
        )
        
        content = response.choices[0].message.content.strip()
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if not json_match:
            raise ValueError(f"No JSON found in LLM response: {content}")
        
        return json.loads(json_match.group())