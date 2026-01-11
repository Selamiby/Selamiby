from typing import Dict, Optional

import requests


class AIIntegration:
    def __init__(self, openai_key: Optional[str] = None, gemini_key: Optional[str] = None, claude_key: Optional[str] = None):
        self.openai_key = openai_key
        self.gemini_key = gemini_key
        self.claude_key = claude_key
        self.history = []

    def ask_openai(self, prompt: str) -> str:
        if not self.openai_key:
            return "OpenAI API anahtarı eksik."
        url = "https://api.openai.com/v1/completions"
        headers = {"Authorization": f"Bearer {self.openai_key}"}
        data = {
            "model": "gpt-3.5-turbo-instruct",
            "prompt": prompt,
            "max_tokens": 256
        }
        resp = requests.post(url, headers=headers, json=data)
        if resp.status_code == 200:
            return resp.json()["choices"][0]["text"].strip()
        return f"OpenAI API hatası: {resp.text}"

    def ask_gemini(self, prompt: str) -> str:
        if not self.gemini_key:
            return "Gemini API anahtarı eksik."
        # Gemini API örnek endpoint ve payload
        url = "https://api.gemini.com/v1/generate"
        headers = {"Authorization": f"Bearer {self.gemini_key}"}
        data = {"prompt": prompt}
        resp = requests.post(url, headers=headers, json=data)
        if resp.status_code == 200:
            return resp.json().get("result", "")
        return f"Gemini API hatası: {resp.text}"

    def ask_claude(self, prompt: str) -> str:
        if not self.claude_key:
            return "Claude API anahtarı eksik."
        url = "https://api.anthropic.com/v1/complete"
        headers = {"x-api-key": self.claude_key}
        data = {
            "prompt": prompt,
            "model": "claude-2",
            "max_tokens_to_sample": 256
        }
        resp = requests.post(url, headers=headers, json=data)
        if resp.status_code == 200:
            return resp.json().get("completion", "")
        return f"Claude API hatası: {resp.text}"

    def ask(self, prompt: str, provider: str = "openai") -> str:
        if provider == "openai":
            answer = self.ask_openai(prompt)
        elif provider == "gemini":
            answer = self.ask_gemini(prompt)
        elif provider == "claude":
            answer = self.ask_claude(prompt)
        else:
            answer = "Bilinmeyen AI sağlayıcı."
        self.history.append({"prompt": prompt, "answer": answer, "provider": provider})
        return answer
        self.history.append({"prompt": prompt, "answer": answer, "provider": provider})
        return answer
        self.history.append({"prompt": prompt, "answer": answer, "provider": provider})
        return answer
