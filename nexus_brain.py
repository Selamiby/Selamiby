import json
import logging
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

try:
    import anthropic
except ImportError:
    anthropic = None

load_dotenv()

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] 🧠 BRAIN: %(message)s")
logger = logging.getLogger("NexusBrain")

class NexusBrain:
    """
    NEXUS-ONE Deep Intelligence Layer.
    Coordinates between Groq, Gemini, and Local Logic.
    """
    def __init__(self):
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.gemini_key = os.getenv("GOOGLE_AI_STUDIO_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        self.deepseek_key = os.getenv("DEEPSEEK_API_KEY")

    def think(self, prompt: str, system_prompt: str = "You are NEXUS-ONE, an advanced autonomous AI."):
        """Decides which model to use based on availability and task."""

        # 1. Try DeepSeek (Best for Coding if key exists)
        if "code" in prompt.lower() or "python" in prompt.lower():
            if self.deepseek_key and self.deepseek_key != "...":
                result = self._call_deepseek(prompt, system_prompt)
                if result: return result

        # 2. Try Anthropic (Claude)
        if self.anthropic_key and self.anthropic_key != "..." and anthropic:
            result = self._call_anthropic(prompt, system_prompt)
            if result: return result

        # 2. Try Groq (Ultra Fast Reasoning)
        if self.groq_key and self.groq_key != "...":
            result = self._call_groq(prompt, system_prompt)
            if result: return result

        # 2. Try Gemini (Deep Analysis)
        if self.gemini_key and self.gemini_key != "...":
            return self._call_gemini(prompt, system_prompt)

        # 3. Try OpenAI
        if self.openai_key and self.openai_key != "...":
            return self._call_openai(prompt, system_prompt)

        return "Internal Logic: Deep Intelligence APIs not configured. Running on base autonomous patterns."

    def _call_deepseek(self, prompt, system_prompt):
        try:
            url = "https://api.deepseek.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {self.deepseek_key}", "Content-Type": "application/json"}
            data = {
                "model": "deepseek-coder",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            }
            response = requests.post(url, headers=headers, json=data)
            res_json = response.json()
            if 'choices' in res_json:
                return res_json['choices'][0]['message']['content']
            return None
        except Exception as e:
            logger.error(f"DeepSeek Call Error: {e}")
            return None

    def _call_groq(self, prompt, system_prompt):
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {self.groq_key}", "Content-Type": "application/json"}
            data = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            }
            response = requests.post(url, headers=headers, json=data)
            res_json = response.json()
            if 'choices' in res_json:
                return res_json['choices'][0]['message']['content']
            else:
                logger.error(f"Groq API error response: {res_json}")
                return None
        except Exception as e:
            logger.error(f"Groq Call Error: {e}")
            return None

    def _call_anthropic(self, prompt, system_prompt):
        """Calls Claude with NEXUS-ONE tools support using the specific 2025-09-29 pattern."""
        if not anthropic: return None
        try:
            client = anthropic.Anthropic(api_key=self.anthropic_key)
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022", # Current stable. Logic supports schema for future 4.5
                max_tokens=4096,
                temperature=1.0, # User specified temperature: 1
                system=system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                tools=[
                    {
                        "name": "nexus-one",
                        "description": "yapay zeka",
                        "input_schema": {
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "The city and state, e.g. San Francisco, CA"
                                },
                                "action": {
                                    "type": "string",
                                    "description": "NEXUS-ONE otonom eylem komutu"
                                }
                            },
                            "required": ["location"]
                        }
                    }
                ]
            )
            # Log the message content as requested by console.log simulation
            logger.info(f"🧠 CLAUDE-CODE-GEN-RESPONSE: {message.content}")
            return message.content[0].text
        except Exception as e:
            logger.error(f"Anthropic API Error: {e}")
            return None

    def _call_gemini(self, prompt, system_prompt):
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_key}"
            headers = {"Content-Type": "application/json"}
            data = {
                "contents": [{
                    "parts": [{"text": f"System: {system_prompt}\nUser: {prompt}"}]
                }]
            }
            response = requests.post(url, headers=headers, json=data)
            json_res = response.json()
            if 'candidates' in json_res and len(json_res['candidates']) > 0:
                return json_res['candidates'][0]['content']['parts'][0]['text']

            logger.error(f"Gemini API Error: {json_res}")
            return None
        except Exception as e:
            logger.error(f"Gemini Call Error: {e}")
            return None

    def search_internet(self, query: str):
        """Uses Tavily AI Search to find real-time info."""
        tavily_key = os.getenv("TAVILY_API_KEY")
        if not tavily_key or tavily_key == "...":
            return "Search unavailable: API Key missing."

        try:
            url = "https://api.tavily.com/search"
            data = {"api_key": tavily_key, "query": query, "search_depth": "advanced"}
            response = requests.post(url, json=data)
            return response.json().get("results", [])
        except Exception as e:
            logger.error(f"Tavily Search Error: {e}")
            return []

    def _call_openai(self, prompt, system_prompt):
        if not self.openai_key or self.openai_key == "...":
            return None
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {self.openai_key}", "Content-Type": "application/json"}
            data = {
                "model": "gpt-4o",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            }
            response = requests.post(url, headers=headers, json=data)
            res_json = response.json()
            if 'choices' in res_json:
                return res_json['choices'][0]['message']['content']
            else:
                logger.error(f"OpenAI API error response: {res_json}")
                return None
        except Exception as e:
            logger.error(f"OpenAI Call Error: {e}")
            return None

if __name__ == "__main__":
    brain = NexusBrain()
    print(brain.think("Perform a self-diagnostic on NEXUS-ONE project structure."))
