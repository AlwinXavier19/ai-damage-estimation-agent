import json
import re
import requests

try:
    from estimation_agent.app.config import settings
except ImportError:
    from app.config import settings


class AzureOpenAIService:
    """
    Service wrapper for Azure OpenAI API.
    """

    def __init__(self):
        self.url = f"{settings.AZURE_OPENAI_ENDPOINT}/openai/deployments/{settings.AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version={settings.AZURE_OPENAI_API_VERSION}"
        self.headers = {
            "Content-Type": "application/json",
            "api-key": settings.AZURE_OPENAI_KEY
        }

    def chat_completion(self, messages: list) -> dict:
        """
        Sends a chat completion request to the Azure OpenAI endpoint.
        """
        payload = {
            "messages": messages,
            "temperature": settings.TEMPERATURE,
            "max_tokens": settings.MAX_TOKENS,
        }

        response = requests.post(
            self.url,
            headers=self.headers,
            json=payload,
            timeout=settings.REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response.json()

    def extract_content(self, response: dict) -> str:
        """
        Extracts the text content from the API response.
        """
        try:
            return response["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError):
            return ""

    def extract_json(self, response: dict) -> dict:
        """
        Extracts and parses a JSON object from the response content,
        handling optional markdown backticks (e.g. ```json ... ```).
        """
        content = self.extract_content(response)
        if not content:
            return {}

        # Clean markdown code block formatting
        match = re.search(r"```json\s*(.*?)\s*```", content, re.DOTALL)
        if match:
            content = match.group(1)
        else:
            match = re.search(r"```\s*(.*?)\s*```", content, re.DOTALL)
            if match:
                content = match.group(1)

        try:
            return json.loads(content.strip())
        except json.JSONDecodeError:
            return {}
