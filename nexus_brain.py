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

    def think(self, prompt: str, system_prompt: str = "You are NEXUS-ONE, an advanced autonomous AI."):
        """Decides which model to use based on availability and task."""
        
        # 1. Try Anthropic (Claude) - Highest Priority if available
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

    def _call_groq(self, prompt, system_prompt):
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {self.groq_key}", "Content-Type": "application/json"}
            data = {
                "model": "llama3-70b-8192",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            }
            response = requests.post(url, headers=headers, json=data)
            return response.json()['choices'][0]['message']['content']
        except:
            return None

    def _call_anthropic(self, prompt, system_prompt):
        """Calls Claude with NEXUS-ONE tools support."""
        if not anthropic: return None
        try:
            client = anthropic.Anthropic(api_key=self.anthropic_key)
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022", # Latest stable sonnet
                max_tokens=4096,
                temperature=0.7,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                tools=[
                    {
                        "name": "nexus_one_action",
                        "description": "NEXUS-ONE otonom eylem gerçekleştirir.",
                        "input_schema": {
                            "type": "object",
                            "properties": {
                                "action_type": {"type": "string", "description": "Eylem türü (optimize, fix, learn)"},
                                "target": {"type": "string", "description": "Hedef dosya veya konu"}
                            },
                            "required": ["action_type", "target"]
                        }
                    }
                ]
            )
            return message.content[0].text
        except Exception as e:
            logger.error(f"Anthropic API Error: {e}")
            return None

    def _call_gemini(self, prompt, system_prompt):
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={self.gemini_key}"
            headers = {"Content-Type": "application/json"}
            data = {
                "contents": [{
                    "parts": [{"text": f"System: {system_prompt}\nUser: {prompt}"}]
                }]
            }
            response = requests.post(url, headers=headers, json=data)
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            logger.error(f"Gemini API Error: {e}")
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
            return response.json()['choices'][0]['message']['content']
        except:
            return None

if __name__ == "__main__":
    brain = NexusBrain()
    print(brain.think("Perform a self-diagnostic on NEXUS-ONE project structure."))
