"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:23
🚀 Status: ACTIVE / PRODUCTION
"""

import concurrent.futures
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

from nexus_sovereign_core import NexusSovereignCore


class NexusBrain:
    """
    NEXUS-ONE Deep Intelligence Layer.
    Now redirected to Sovereign Internal Logic.
    """
    def __init__(self):
        self.sovereign = NexusSovereignCore()
        # API Keys are no longer the primary source
        self.groq_key = os.getenv("GROQ_API_KEY")
        # ... other keys ...

    def think(self, prompt: str, system_prompt: str = ""):
        """
        Dış API bağımlılığını kesen yeni 'Egemen Düşünce' protokolü.
        """
        print(f"🧠 SOVEREIGN LOGIC: {prompt} işleniyor...")
        
        # Öncelikle kendi çekirdeğimizde çözmeyi dene
        internal_response = self.sovereign.execute_sovereign_task(prompt)
        
        # Eğer çok karmaşık bir yaratıcı metin gerekliyse (geçici hibrit mod)
        # ama hedef tamamen %100 otonomluk.
        return internal_response["response"]

        # Try models with exponential backoff / simple sleep for rate limits
        models = [
            ("DeepSeek", self._call_deepseek),
            ("Anthropic", self._call_anthropic),
            ("Gemini", self._call_gemini),
            ("Groq", self._call_groq),
            ("OpenAI", self._call_openai)
        ]

        for name, func in models:
            try:
                res = func(prompt, system_prompt)
                if res and "rate_limit" not in str(res).lower() and "error" not in str(res).lower():
                    return res
                if "rate_limit" in str(res).lower():
                    logger.warning(f"⚠️ {name} Rate Limited. Trying next...")
            except:
                continue

        return "NEXUS-CORE: Waiting for API cooldown. All layers throttled."

    def quantum_think(self, prompt: str, system_prompt: str):
        """
        🚀 QUANTUM REASONING V2: Parallel interference with Self-Correction (Metacognition).
        """
        logger.info("🌀 Quantum Reasoning Mode: Initiating Parallel Interference...")
        
        models_to_call = []
        if self.deepseek_key: models_to_call.append(self._call_deepseek)
        if self.groq_key: models_to_call.append(self._call_groq)
        if self.gemini_key: models_to_call.append(self._call_gemini)
        
        if not models_to_call:
            return self._call_gemini(prompt, system_prompt)

        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(models_to_call)) as executor:
            future_to_model = {executor.submit(m, prompt, system_prompt): m.__name__ for m in models_to_call}
            for future in concurrent.futures.as_completed(future_to_model):
                res = future.result()
                if res: results.append(res)
        
        if not results: return "Quantum Error: No valid interference patterns detected."
        
        if len(results) > 1:
            # METACOGNITION: Use the strongest model to evaluate and synthesize all results
            synthesis_prompt = f"Aşağıdaki farklı yapay zeka cevaplarını analiz et, hataları ayıkla ve en doğru, en kapsamlı nihai cevabı oluştur:\n\n"
            for i, r in enumerate(results):
                synthesis_prompt += f"--- CEVAP {i+1} ---\n{r}\n\n"
            
            logger.info("🧠 Metacognition: Synthesizing optimal response...")
            # Use Gemini as the 'Judge' for synthesis due to its large context window
            final_result = self._call_gemini(synthesis_prompt, "Sen NEXUS-SUPREME-JUDGE ajanısın. Diğer modellerin çıktılarını sentezleyip mükemmel hale getirirsin.")
            return final_result
        
        return results[0]

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
            # CORRECT ENDPOINTS FOR 2025/2026
            # We try the most stable ones first
            model_configs = [
                {"version": "v1beta", "model": "gemini-2.0-flash-exp"},
                {"version": "v1beta", "model": "gemini-1.5-flash"},
                {"version": "v1beta", "model": "gemini-1.5-pro"},
                {"version": "v1", "model": "gemini-1.5-flash"},
            ]
            
            error_log = []
            for cfg in model_configs:
                url = f"https://generativelanguage.googleapis.com/{cfg['version']}/models/{cfg['model']}:generateContent?key={self.gemini_key}"
                headers = {"Content-Type": "application/json"}
                data = {
                    "contents": [{
                        "parts": [{"text": f"System: {system_prompt}\nUser: {prompt}"}]
                    }]
                }
                try:
                    response = requests.post(url, headers=headers, json=data, timeout=15)
                    json_res = response.json()
                    if 'candidates' in json_res and len(json_res['candidates']) > 0:
                        return json_res['candidates'][0]['content']['parts'][0]['text']
                    error_log.append(f"{cfg['model']}: {json_res.get('error', {}).get('message', 'Unknown Error')}")
                except Exception as e:
                    error_log.append(f"{cfg['model']} Request Failed: {str(e)}")
            
            logger.error(f"Gemini API All Exhausted: {error_log}")
            return None
        except Exception as e:
            logger.error(f"Gemini Critical Error: {e}")
            return None

    def think_with_vision(self, prompt: str, image_path: str):
        """Gemini 1.5 Flash kullanarak gerçek zamanlı görsel analiz yapar."""
        # KEY VALIDATION & ENV CLEANING
        key = self.gemini_key.strip() if self.gemini_key else ""
        if not key or key == "..." or len(key) < 10:
            return "❌ Vision Hatası: Gemini API anahtarı (.env içerisindeki GOOGLE_AI_STUDIO_KEY) geçersiz veya eksik."
        
        try:
            import base64
            import mimetypes
            from pathlib import Path
            img_p = Path(image_path)
            if not img_p.exists():
                return f"❌ Vision Hatası: Dosya bulunamadı -> {image_path}"

            # Detect Mime Type
            mime_type, _ = mimetypes.guess_type(image_path)
            if not mime_type:
                mime_type = "image/png" # Default

            with open(img_p, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
            headers = {"Content-Type": "application/json"}
            data = {
                "contents": [{
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": mime_type,
                                "data": encoded_image
                            }
                        }
                    ]
                }]
            }
            response = requests.post(url, headers=headers, json=data, timeout=30)
            res_json = response.json()

            if 'candidates' in res_json and len(res_json['candidates']) > 0:
                text_out = res_json['candidates'][0]['content']['parts'][0]['text']
                logger.info("✅ Vision Analizi Başarılı.")
                return text_out
            
            # Detailed Error Parsing for the user
            if 'error' in res_json:
                error_code = res_json['error'].get('code', 'N/A')
                error_details = res_json['error'].get('message', 'Bilinmeyen API Hatası')
                logger.error(f"Gemini API Error ({error_code}): {error_details}")
                return f"⚠️ API Hatası ({error_code}): {error_details}"

            return "🔴 Görsel analiz edilemedi: API yanıtı beklenen formatta değil. Lütfen internet bağlantınızı veya API kotanızı kontrol edin."
        except Exception as e:
            logger.error(f"Vision Call Error: {e}")
            return f"❌ Kritik Hata: {str(e)}"

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
