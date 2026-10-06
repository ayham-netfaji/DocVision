import httpx
import json
from app.core.config import settings

class AIService:
    def __init__(self):
        self.api_key = settings.openrouter_api_key
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = "nvidia/nemotron-3-ultra-550b-a55b:free"
        
    async def _call_openrouter(self, messages: list) -> str:
        if not self.api_key:
            return "Error: OPENROUTER_API_KEY is not configured."
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "reasoning": {"enabled": True}
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=60.0
                )
                data = response.json()
                if 'error' in data:
                    error_msg = data['error'].get('message', 'Unknown API Error')
                    return f"OpenRouter API Error: {error_msg}"
                return data['choices'][0]['message'].get('content', '')
            except Exception as e:
                return f"AI Processing Error: {str(e)}"

    async def summarize_text(self, text: str) -> str:
        if not text or not text.strip():
            return "No text provided for summarization."
            
        messages = [
            {"role": "system", "content": "You are a helpful assistant that summarizes documents concisely."},
            {"role": "user", "content": f"Please provide a concise summary of the following text:\n\n{text}"}
        ]
        return await self._call_openrouter(messages)
        
    async def classify_document(self, text: str) -> str:
        if not text or not text.strip():
            return "Unknown"
            
        messages = [
            {"role": "system", "content": "You are a document classifier. Classify the document into exactly one of these categories: Invoice, Receipt, ID Card, Contract, Letter, Academic Paper, Form, Other. Output ONLY the category name."},
            {"role": "user", "content": f"Classify the following text:\n\n{text}"}
        ]
        return await self._call_openrouter(messages)

ai_service = AIService()
