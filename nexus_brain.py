import json
import logging
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

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
        
    def think(self, prompt: str, system_prompt: str = "You are NEXUS-ONE, an advanced autonomous AI."):
        """Decides which model to use based on availability and task."""
        
        # 1. Try Groq (Ultra Fast Reasoning) - Currently checking if '...'
        if self.groq_key and self.groq_key != "...":
            return self._call_groq(prompt, system_prompt)
        
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

    def _call_gemini(self, prompt, system_prompt):
        # Placeholder for Gemini API call
        return "Gemini Analysis Active (Connection Ready)"

    def _call_openai(self, prompt, system_prompt):
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
