# all_ai_integration.py
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from typing import Any, Dict, Optional

import requests


class AllAIIntegration:
    def __init__(self):
        self.ai_models = {
            "openai": {
                "models": ["gpt-4", "gpt-3.5-turbo", "dall-e-3", "whisper", "claude"],
                "api_base": "https://api.openai.com/v1",
                "capabilities": ["text", "image", "audio", "code"]
            },
            "anthropic": {
                "models": ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"],
                "api_base": "https://api.anthropic.com/v1",
                "capabilities": ["text", "reasoning"]
            },
            "google": {
                "models": ["gemini-pro", "gemini-ultra", "palm-2"],
                "api_base": "https://generativelanguage.googleapis.com/v1",
                "capabilities": ["text", "multimodal", "code"]
            },
            "meta": {
                "models": ["llama-2", "llama-3", "code-llama"],
                "api_base": "https://api.meta.ai/v1",
                "capabilities": ["text", "code", "open_source"]
            },
            "microsoft": {
                "models": ["copilot", "bing-chat", "orion"],
                "api_base": "https://api.copilot.microsoft.com/v1",
                "capabilities": ["text", "code", "search"]
            },
            "stability": {
                "models": ["stable-diffusion-3", "stable-video"],
                "api_base": "https://api.stability.ai/v1",
                "capabilities": ["image", "video"]
            },
            "elevenlabs": {
                "models": ["eleven-monolingual", "eleven-multilingual"],
                "api_base": "https://api.elevenlabs.io/v1",
                "capabilities": ["speech", "voice_clone"]
            },
            "huggingface": {
                "models": ["thousands_of_models"],
                "api_base": "https://api-inference.huggingface.co/models",
                "capabilities": ["text", "image", "audio", "custom"]
            },
            "local": {
                "models": ["llama.cpp", "ollama", "text-generation-webui"],
                "api_base": "http://localhost:8080",
                "capabilities": ["text", "offline", "private"]
            }
        }
        
        print("""
╔══════════════════════════════════════════════════════╗
║     🤖 ALL AI INTEGRATION SYSTEM v2.0                ║
║     Tüm AI modelleri tek sistemde                    ║
║     Offline + Online + Yerel + Bulut                 ║
╚══════════════════════════════════════════════════════╝
        """)
    
    def setup_environment(self):
        """AI ortamını kur"""
        print("\n📦 AI ORTAMI KURULUYOR...")
        
        requirements = [
            "openai>=1.0.0", 
            "anthropic>=0.8.0",
            "google-generativeai>=0.3.0",
            "transformers>=4.35.0",
            "diffusers>=0.24.0",
            "torch>=2.1.0",
            "langchain>=0.1.0",
            "crewai>=0.1.0",
            "llama-index>=0.9.0",
            "autogen>=0.2.0",
            "elevenlabs>=0.2.0",
            "stability-sdk>=0.4.0"
        ]
        
        installed = []
        failed = []
        
        for package in requirements:
            try:
                print(f"   ⏳ {package.split('>=')[0]} yükleniyor...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package.split('>=')[0], "--quiet"])
                installed.append(package.split('>=')[0])
                print(f"   ✅ {package.split('>=')[0]}")
                time.sleep(1)  # Rate limiting için
            except Exception as e:
                print(f"   ⚠️ {package.split('>=')[0]} yüklenemedi: {str(e)[:50]}")
                failed.append(package.split('>=')[0])
        
        print(f"\n📊 KURULUM SONUÇLARI:")
        print(f"   • Başarılı: {len(installed)}")
        print(f"   • Başarısız: {len(failed)}")
        if failed:
            print(f"   • Başarısız olanlar: {', '.join(failed)}")
        
        # Environment kontrolü
        print("\n🔍 ORTAM KONTROLÜ:")
        try:
            import openai
            print("   ✅ OpenAI: Hazır")
        except ImportError:
            print("   ❌ OpenAI: Kurulu değil")
        
        try:
            import google.generativeai as genai
            print("   ✅ Google AI: Hazır")
        except ImportError:
            print("   ❌ Google AI: Kurulu değil")
        
        try:
            from transformers import pipeline
            print("   ✅ Transformers: Hazır")
        except ImportError:
            print("   ❌ Transformers: Kurulu değil")
        
        return {
            "installed": installed,
            "failed": failed,
            "total": len(requirements)
        }
    
    def create_unified_api(self):
        """Birleşik AI API'si oluştur"""
        print("\n🔗 BİRLEŞİK AI API'Sİ OLUŞTURULUYOR...")
        
        api_code = '''# unified_ai_api.py
import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

class UnifiedAIApi:
    """Tüm AI servislerini birleştiren API"""
    
    def __init__(self, config_path: str = None):
        self.providers = {}
        self.config = self.load_config(config_path)
        self.setup_providers()
        
        print(f"🤖 Unified AI API Başlatıldı")
        print(f"   • Aktif Provider: {len(self.providers)}")
        print(f"   • Mod: {self.config.get('mode', 'mixed')}")
    
    def load_config(self, config_path: str = None) -> Dict:
        """Config dosyasını yükle"""
        default_config = {
            "mode": "mixed",  # online, offline, mixed
            "default_provider": "openai",
            "fallback_chain": ["openai", "google", "local"],
            "timeout": 30,
            "max_retries": 3,
            "cost_optimization": True,
            "cache_responses": True,
            "log_level": "info"
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except:
                print(f"⚠️ Config dosyası okunamadı: {config_path}")
        
        return default_config
    
    def setup_providers(self):
        """AI provider'ları kur"""
        # 1. OpenAI
        try:
            import openai
            if os.getenv("OPENAI_API_KEY"):
                self.providers["openai"] = {
                    "client": openai.OpenAI(),
                    "models": ["gpt-4", "gpt-3.5-turbo", "gpt-4-vision-preview"],
                    "capabilities": ["text", "vision", "code"],
                    "cost_per_1k": 0.03  # USD
                }
                print("   ✅ OpenAI: Aktif")
        except Exception as e:
            print(f"   ❌ OpenAI: {str(e)[:50]}")
        
        # 2. Google Gemini
        try:
            import google.generativeai as genai
            if os.getenv("GOOGLE_API_KEY"):
                genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
                self.providers["google"] = {
                    "client": genai,
                    "models": ["gemini-pro", "gemini-pro-vision"],
                    "capabilities": ["text", "vision", "multimodal"],
                    "cost_per_1k": 0.0  # Ücretsiz (sınırlı)
                }
                print("   ✅ Google AI: Aktif")
        except Exception as e:
            print(f"   ❌ Google AI: {str(e)[:50]}")
        
        # 3. Anthropic Claude
        try:
            import anthropic
            if os.getenv("ANTHROPIC_API_KEY"):
                self.providers["anthropic"] = {
                    "client": anthropic.Anthropic(),
                    "models": ["claude-3-opus-20240229", "claude-3-sonnet-20240229"],
                    "capabilities": ["text", "reasoning", "long_context"],
                    "cost_per_1k": 0.015
                }
                print("   ✅ Anthropic: Aktif")
        except Exception as e:
            print(f"   ❌ Anthropic: {str(e)[:50]}")
        
        # 4. Yerel Modeller (Transformers)
        try:
            from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
            import torch
            
            # Hafif bir model pipeline'ı
            self.providers["local"] = {
                "text": None,  # Lazy loading
                "models": ["gpt2", "distilgpt2", "microsoft/DialoGPT-small"],
                "capabilities": ["text", "offline", "free"],
                "cost_per_1k": 0.0
            }
            print("   ✅ Local Models: Hazır (lazy load)")
        except Exception as e:
            print(f"   ❌ Local Models: {str(e)[:50]}")
        
        # 5. Hugging Face Inference API
        try:
            import requests
            if os.getenv("HUGGINGFACE_TOKEN"):
                self.providers["huggingface"] = {
                    "client": requests,
                    "models": ["gpt2", "bert", "distilbert"],
                    "capabilities": ["text", "free_tier"],
                    "cost_per_1k": 0.0
                }
                print("   ✅ Hugging Face: Aktif")
        except:
            print("   ❌ Hugging Face: Token bulunamadı")
    
    def load_local_model(self):
        """Yerel modeli lazy load et"""
        if "local" in self.providers and self.providers["local"]["text"] is None:
            try:
                print("   ⏳ Yerel model yükleniyor...")
                from transformers import pipeline
                self.providers["local"]["text"] = pipeline(
                    "text-generation",
                    model="gpt2",
                    device=-1,  # CPU
                    max_length=200
                )
                print("   ✅ Yerel model yüklendi")
            except Exception as e:
                print(f"   ❌ Yerel model yüklenemedi: {e}")
    
    def smart_router(self, prompt: str, context: Dict = None) -> Dict[str, Any]:
        """Akıllı router - en iyi AI'yı seç"""
        if context is None:
            context = {}
        
        # Prompt analizi
        prompt_lower = prompt.lower()
        task_analysis = {
            "requires_vision": any(word in prompt_lower for word in ["resim", "görsel", "image", "photo", "fotoğraf"]),
            "requires_code": any(word in prompt_lower for word in ["kod", "code", "program", "function", "yazılım"]),
            "requires_reasoning": any(word in prompt_lower for word in ["analiz", "reason", "think", "solve", "problem"]),
            "requires_creativity": any(word in prompt_lower for word in ["yarat", "creative", "imagine", "story", "hikaye"]),
            "requires_technical": any(word in prompt_lower for word in ["tekn", "tech", "mühendis", "engineer"]),
            "requires_speed": len(prompt) < 100 and "local" in self.providers,
            "sensitive": any(word in prompt_lower for word in ["gizli", "secret", "private", "şifre", "password"])
        }
        
        # Provider skorlaması
        provider_scores = {}
        
        for provider_name, provider_info in self.providers.items():
            score = 0
            
            # Uygunluk puanı
            if task_analysis["requires_vision"] and "vision" in provider_info.get("capabilities", []):
                score += 10
            if task_analysis["requires_code"] and "code" in provider_info.get("capabilities", []):
                score += 8
            if task_analysis["requires_reasoning"] and "reasoning" in provider_info.get("capabilities", []):
                score += 7
            if task_analysis["requires_speed"] and provider_name == "local":
                score += 5
            if task_analysis["sensitive"] and "offline" in provider_info.get("capabilities", []):
                score += 20  # Hassas veriler için offline öncelik
            
            # Maliyet puanı (düşük maliyet yüksek puan)
            cost = provider_info.get("cost_per_1k", 1.0)
            if cost == 0:
                score += 3
            elif cost < 0.01:
                score += 2
            elif cost < 0.05:
                score += 1
            
            provider_scores[provider_name] = score
        
        # En yüksek puanlı provider'ı seç
        if provider_scores:
            selected = max(provider_scores.items(), key=lambda x: x[1])[0]
        else:
            selected = None
        
        return {
            "selected_provider": selected,
            "provider_scores": provider_scores,
            "task_analysis": task_analysis,
            "confidence": provider_scores.get(selected, 0) / 50 if selected else 0
        }
    
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Birleşik AI çağrısı"""
        start_time = datetime.now()
        
        # Router'ı kullan
        routing = self.smart_router(prompt, kwargs.get("context"))
        provider_name = routing["selected_provider"]
        
        if not provider_name:
            return {
                "error": "No AI provider available",
                "routing": routing,
                "timestamp": start_time.isoformat()
            }
        
        provider_info = self.providers.get(provider_name)
        if not provider_info:
            return {
                "error": f"Provider {provider_name} not configured",
                "routing": routing,
                "timestamp": start_time.isoformat()
            }
        
        try:
            result = None
            
            if provider_name == "openai":
                response = provider_info["client"].chat.completions.create(
                    model=kwargs.get("model", "gpt-3.5-turbo"),
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=kwargs.get("max_tokens", 500),
                    temperature=kwargs.get("temperature", 0.7)
                )
                
                result = {
                    "provider": "openai",
                    "content": response.choices[0].message.content,
                    "model": response.model,
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens,
                        "estimated_cost": (response.usage.total_tokens / 1000) * provider_info["cost_per_1k"]
                    }
                }
            
            elif provider_name == "google":
                model = provider_info["client"].GenerativeModel(
                    kwargs.get("model", "gemini-pro")
                )
                response = model.generate_content(
                    prompt,
                    generation_config={
                        "max_output_tokens": kwargs.get("max_tokens", 500),
                        "temperature": kwargs.get("temperature", 0.7)
                    }
                )
                
                result = {
                    "provider": "google",
                    "content": response.text,
                    "model": kwargs.get("model", "gemini-pro"),
                    "usage": {
                        "estimated_cost": 0.0  # Ücretsiz tier
                    }
                }
            
            elif provider_name == "anthropic":
                response = provider_info["client"].messages.create(
                    model=kwargs.get("model", "claude-3-sonnet-20240229"),
                    max_tokens=kwargs.get("max_tokens", 500),
                    temperature=kwargs.get("temperature", 0.7),
                    messages=[{"role": "user", "content": prompt}]
                )
                
                result = {
                    "provider": "anthropic",
                    "content": response.content[0].text,
                    "model": response.model,
                    "usage": {
                        "input_tokens": response.usage.input_tokens,
                        "output_tokens": response.usage.output_tokens,
                        "estimated_cost": ((response.usage.input_tokens + response.usage.output_tokens) / 1000) * provider_info["cost_per_1k"]
                    }
                }
            
            elif provider_name == "local":
                # Lazy load
                self.load_local_model()
                
                if self.providers["local"]["text"]:
                    response = self.providers["local"]["text"](
                        prompt,
                        max_length=kwargs.get("max_tokens", 200) + len(prompt),
                        temperature=kwargs.get("temperature", 0.7),
                        do_sample=True
                    )
                    
                    result = {
                        "provider": "local",
                        "content": response[0]["generated_text"],
                        "model": "gpt2",
                        "usage": {
                            "estimated_cost": 0.0,
                            "device": "CPU",
                            "offline": True
                        }
                    }
                else:
                    result = {
                        "error": "Local model not loaded",
                        "provider": "local"
                    }
            
            elif provider_name == "huggingface":
                API_URL = f"https://api-inference.huggingface.co/models/gpt2"
                headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_TOKEN')}"}
                
                response = provider_info["client"].post(
                    API_URL,
                    headers=headers,
                    json={"inputs": prompt, "parameters": {"max_length": kwargs.get("max_tokens", 200)}}
                )
                
                if response.status_code == 200:
                    result_data = response.json()
                    result = {
                        "provider": "huggingface",
                        "content": result_data[0]["generated_text"],
                        "model": "gpt2",
                        "usage": {
                            "estimated_cost": 0.0,
                            "api_status": "success"
                        }
                    }
                else:
                    result = {
                        "error": f"Hugging Face API error: {response.status_code}",
                        "provider": "huggingface"
                    }
            
            else:
                result = {
                    "error": f"Provider {provider_name} not implemented",
                    "provider": provider_name
                }
            
            # Ortak metadata ekle
            if result and "error" not in result:
                result.update({
                    "timestamp": datetime.now().isoformat(),
                    "processing_time": (datetime.now() - start_time).total_seconds(),
                    "routing": routing,
                    "success": True
                })
            else:
                result.update({
                    "timestamp": datetime.now().isoformat(),
                    "processing_time": (datetime.now() - start_time).total_seconds(),
                    "routing": routing,
                    "success": False
                })
            
            return result
            
        except Exception as e:
            return {
                "error": str(e),
                "provider": provider_name,
                "routing": routing,
                "timestamp": datetime.now().isoformat(),
                "processing_time": (datetime.now() - start_time).total_seconds(),
                "success": False
            }
    
    def multi_provider_vote(self, prompt: str, providers: List[str] = None) -> Dict[str, Any]:
        """Çoklu provider oylaması - en iyi yanıtı seç"""
        if providers is None:
            providers = list(self.providers.keys())
        
        responses = []
        start_time = datetime.now()
        
        # Paralel olması için thread pool kullanılabilir, şimdilik sıralı
        for provider in providers[:3]:  # İlk 3 provider
            try:
                result = self.generate(prompt, context={"multi_vote": True})
                
                if result.get("success") and "error" not in result:
                    responses.append({
                        "provider": provider,
                        "response": result.get("content", ""),
                        "confidence": result.get("routing", {}).get("confidence", 0.5),
                        "processing_time": result.get("processing_time", 0),
                        "cost": result.get("usage", {}).get("estimated_cost", 0)
                    })
            except Exception as e:
                print(f"   ⚠️ {provider} oylamada hata: {str(e)[:50]}")
        
        # En iyi yanıtı seç
        if responses:
            # Çoklu kriter: uzunluk + güven + hız - maliyet
            def response_score(r):
                length_score = len(r["response"]) / 1000  # Uzunluk
                confidence_score = r["confidence"] * 2    # Güven
                speed_score = 1 / (r["processing_time"] + 1)  # Hız
                cost_penalty = r["cost"] * 100  # Maliyet cezası
                return length_score + confidence_score + speed_score - cost_penalty
            
            best_response = max(responses, key=response_score)
            
            return {
                "best_response": best_response,
                "all_responses": responses,
                "total_time": (datetime.now() - start_time).total_seconds(),
                "consensus": len(responses) > 1,
                "vote_count": len(responses)
            }
        
        return {
            "error": "No responses received",
            "total_time": (datetime.now() - start_time).total_seconds(),
            "vote_count": 0
        }
    
    def create_agent_swarm(self, task: str, agent_count: int = 3) -> Dict[str, Any]:
        """AI agent swarm oluştur"""
        print(f"\n👥 AI AGENT SWARM OLUŞTURULUYOR ({agent_count} agent)...")
        
        agents = []
        
        # Farklı uzmanlıklarda agent'lar
        agent_specializations = [
            {"role": "Analist", "focus": "problem analysis", "provider": "openai"},
            {"role": "Kod Uzmanı", "focus": "code generation", "provider": "google"},
            {"role": "Stratejist", "focus": "planning", "provider": "anthropic"},
            {"role": "Yaratıcı", "focus": "creative solutions", "provider": "local"},
            {"role": "Eleştirmen", "focus": "critical review", "provider": "huggingface"}
        ]
        
        for i in range(min(agent_count, len(agent_specializations))):
            spec = agent_specializations[i]
            
            agent_prompt = f"""
            Sen {spec['role']} agentsın. Uzmanlık alanın: {spec['focus']}.
            
            Görev: {task}
            
            Lütfen uzmanlık alanına göre analiz yap ve önerilerde bulun.
            """
            
            result = self.generate(agent_prompt, context={"agent_role": spec['role']})
            
            if result.get("success"):
                agents.append({
                    "id": i + 1,
                    "role": spec['role'],
                    "focus": spec['focus'],
                    "provider": spec['provider'],
                    "response": result.get("content", "")[:500],
                    "analysis_time": result.get("processing_time", 0)
                })
        
        # Swarm sonuçlarını birleştir
        if agents:
            combined_prompt = f"""
            {len(agents)} AI agent'ın analizini birleştir:
            
            Görev: {task}
            
            Agent Analizleri:
            {json.dumps([{"role": a['role'], "analysis": a['response']} for a in agents], indent=2)}
            
            Lütfen tüm analizleri sentezleyerek nihai bir öneri oluştur.
            """
            
            final_result = self.generate(combined_prompt, context={"swarm_synthesis": True})
            
            return {
                "agents": agents,
                "final_synthesis": final_result.get("content", "") if final_result.get("success") else "Sentez oluşturulamadı",
                "total_agents": len(agents),
                "total_time": sum(a['analysis_time'] for a in agents) + final_result.get("processing_time", 0)
            }
        
        return {
            "error": "No agents created",
            "agents": [],
            "total_agents": 0
        }

# Kullanım örneği
if __name__ == "__main__":
    # Environment değişkenlerini kontrol et
    print("🔑 API KEY KONTROLÜ:")
    keys_to_check = ["OPENAI_API_KEY", "GOOGLE_API_KEY", "ANTHROPIC_API_KEY", "HUGGINGFACE_TOKEN"]
    
    for key in keys_to_check:
        if os.getenv(key):
            print(f"   ✅ {key}: ***{os.getenv(key)[-4:] if len(os.getenv(key)) > 4 else '***'}")
        else:
            print(f"   ❌ {key}: Bulunamadı (isteğe bağlı)")
    
    # API'yi başlat
    ai = UnifiedAIApi()
    
    print("\n🧪 TEST SÜRÜŞÜ:")
    
    # Test 1: Basit soru
    print("\n1. Basit soru:")
    result1 = ai.generate("Python'da fibonacci serisi nasıl yazılır?")
    if result1.get("success"):
        print(f"   Provider: {result1.get('provider')}")
        print(f"   Yanıt: {result1.get('content', '')[:100]}...")
    else:
        print(f"   Hata: {result1.get('error', 'Bilinmeyen hata')}")
    
    # Test 2: Çoklu oylama
    print("\n2. Çoklu oylama:")
    vote_result = ai.multi_provider_vote("AI'nın geleceği nedir?")
    if "best_response" in vote_result:
        best = vote_result["best_response"]
        print(f"   En iyi: {best['provider']} (güven: %{int(best['confidence']*100)})")
        print(f"   Özet: {best['response'][:150]}...")
    else:
        print(f"   Hata: {vote_result.get('error', 'Oylama yapılamadı')}")
    
    # Test 3: Agent swarm
    print("\n3. Agent swarm testi:")
    swarm_result = ai.create_agent_swarm("Yeni bir programlama dili nasıl tasarlanır?", agent_count=2)
    if "agents" in swarm_result and swarm_result["agents"]:
        print(f"   Oluşturulan agent: {len(swarm_result['agents'])}")
        print(f"   Final özet: {swarm_result.get('final_synthesis', '')[:200]}...")
    else:
        print("   Agent swarm oluşturulamadı")
    
    print("\n" + "="*80)
    print("✅ UNIFIED AI API TESTİ TAMAMLANDI!")
    print(f"   • Toplam provider: {len(ai.providers)}")
    print(f"   • Mod: {ai.config.get('mode')}")
    print(f"   • Cache: {'Aktif' if ai.config.get('cache_responses') else 'Pasif'}")
    print("="*80)
'''
        
        # Dosyaya yaz
        os.makedirs("ai_integration", exist_ok=True)
        with open("ai_integration/unified_ai_api.py", "w", encoding="utf-8") as f:
            f.write(api_code)
        
        print("   ✅ Birleşik API oluşturuldu: ai_integration/unified_ai_api.py")
        
        return "ai_integration/unified_ai_api.py"
    
    def integrate_local_models(self):
        """Yerel AI modellerini kur"""
        print("\n💻 YEREL AI MODELLERİ KURULUYOR...")
        
        local_models = {
            "llama": {
                "size": "7B",
                "format": "GGUF",
                "use_case": "General purpose",
                "ram_required": "8GB",
                "download_size": "4.2GB"
            },
            "mistral": {
                "size": "7B",
                "format": "GGUF",
                "use_case": "Coding & reasoning",
                "ram_required": "8GB",
                "download_size": "4.1GB"
            },
            "codellama": {
                "size": "7B",
                "format": "GGUF",
                "use_case": "Programming",
                "ram_required": "8GB",
                "download_size": "4.3GB"
            },
            "stable_diffusion": {
                "size": "4GB",
                "format": "safetensors",
                "use_case": "Image generation",
                "ram_required": "6GB",
                "download_size": "2.1GB"
            },
            "whisper": {
                "size": "1.5GB",
                "format": "pytorch",
                "use_case": "Speech recognition",
                "ram_required": "2GB",
                "download_size": "1.5GB"
            },
            "gpt2": {
                "size": "500MB",
                "format": "pytorch",
                "use_case": "Text generation (lightweight)",
                "ram_required": "2GB",
                "download_size": "500MB"
            }
        }
        
        # Model config dosyası oluştur
        config = {
            "local_models": local_models,
            "download_links": {
                "llama": "https://huggingface.co/TheBloke/Llama-2-7B-GGUF/resolve/main/llama-2-7b.Q4_K_M.gguf",
                "mistral": "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
                "codellama": "https://huggingface.co/TheBloke/CodeLlama-7B-GGUF/resolve/main/codellama-7b.Q4_K_M.gguf",
                "stable_diffusion": "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors",
                "whisper": "https://huggingface.co/openai/whisper-medium/resolve/main/pytorch_model.bin",
                "gpt2": "https://huggingface.co/gpt2/resolve/main/pytorch_model.bin"
            },
            "setup_commands": [
                "# Transformer modelleri için",
                "pip install transformers torch diffusers accelerate",
                
                "# GGUF modelleri için (llama.cpp)",
                "pip install llama-cpp-python",
                
                "# Audio işleme için",
                "pip install whisper openai-whisper",
                
                "# GPU desteği için (opsiyonel)",
                "pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118"
            ],
            "inference_examples": {
                "text_generation": '''
from transformers import pipeline
generator = pipeline('text-generation', model='gpt2')
result = generator("Hello, how are you?", max_length=50)
print(result[0]['generated_text'])
''',
                "image_generation": '''
from diffusers import StableDiffusionPipeline
import torch

model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

image = pipe("a beautiful sunset over mountains").images[0]
image.save("sunset.png")
''',
                "speech_recognition": '''
import whisper

model = whisper.load_model("medium")
result = model.transcribe("audio.mp3")
print(result["text"])
'''
            }
        }
        
        with open("ai_integration/local_models_config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"   ✅ {len(local_models)} yerel model konfigüre edildi")
        
        # Download script'i oluştur
        download_script = '''# download_local_models.py
import requests
import os
from tqdm import tqdm
import json

def download_file(url, filename):
    """Dosya indirme"""
    print(f"📥 İndiriliyor: {filename}")
    
    # Stream ile indirme
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(filename, 'wb') as f, tqdm(
        desc=filename,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = f.write(data)
            bar.update(size)
    
    print(f"✅ İndirme tamamlandı: {filename}")
    return True

def download_model(model_name, url, save_dir="models"):
    """Model indirme"""
    os.makedirs(save_dir, exist_ok=True)
    
    filename = os.path.join(save_dir, url.split("/")[-1])
    
    if os.path.exists(filename):
        print(f"📁 {model_name} zaten var: {filename}")
        return True
    
    try:
        return download_file(url, filename)
    except Exception as e:
        print(f"❌ {model_name} indirilemedi: {e}")
        return False

def main():
    """Ana indirme fonksiyonu"""
    print("🤖 YEREL AI MODELLERİ İNDİRİLİYOR")
    print("="*50)
    
    # Config dosyasını yükle
    with open("ai_integration/local_models_config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    
    models_to_download = {
        "gpt2": config["download_links"]["gpt2"],
        # Diğer modelleri isteğe bağlı indir
        # "llama": config["download_links"]["llama"],
        # "stable_diffusion": config["download_links"]["stable_diffusion"],
    }
    
    successful = 0
    total = len(models_to_download)
    
    for model_name, url in models_to_download.items():
        if download_model(model_name, url):
            successful += 1
    
    print(f"\\n📊 İNDİRME SONUÇLARI:")
    print(f"   • Başarılı: {successful}/{total}")
    print(f"   • Klasör: models/")
    
    if successful > 0:
        print(f"\\n🚀 MODELLER HAZIR!")
        print(f"   Örnek kullanım için:")
        print(f"   python ai_integration/test_local_models.py")
    
    return successful == total

if __name__ == "__main__":
    main()
'''
        
        with open("ai_integration/download_local_models.py", "w", encoding="utf-8") as f:
            f.write(download_script)
        
        # Test script'i oluştur
        test_script = '''# test_local_models.py
import os
import sys

def test_gpt2():
    """GPT-2 model testi"""
    print("🧪 GPT-2 TESTİ...")
    
    try:
        from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
        import torch
        
        print("   Model yükleniyor...")
        
        # Küçük model (hızlı test için)
        model_name = "gpt2"
        
        # Tokenizer ve model
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        
        # Pipeline
        generator = pipeline('text-generation', model=model, tokenizer=tokenizer)
        
        # Test
        prompt = "Python programlama dili"
        result = generator(prompt, max_length=100, num_return_sequences=1)
        
        print(f"   ✅ GPT-2 çalışıyor!")
        print(f"   Prompt: {prompt}")
        print(f"   Üretilen: {result[0]['generated_text'][:200]}...")
        
        return True
        
    except Exception as e:
        print(f"   ❌ GPT-2 test hatası: {e}")
        return False

def test_simple_inference():
    """Basit inference testi"""
    print("\\n🧪 BASİT INFERENCE TESTİ...")
    
    try:
        # CPU'da çalışabilen küçük model
        from transformers import pipeline
        
        # Text classification (küçük model)
        classifier = pipeline("sentiment-analysis")
        
        result = classifier("I love using AI models!")
        
        print(f"   ✅ Inference çalışıyor!")
        print(f"   Sonuç: {result}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Inference hatası: {e}")
        return False

def main():
    """Ana test fonksiyonu"""
    print("🤖 YEREL MODELLER TEST SÜRÜŞÜ")
    print("="*50)
    
    tests = [
        ("GPT-2 Model", test_gpt2),
        ("Basit Inference", test_simple_inference),
    ]
    
    successful = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                successful += 1
        except Exception as e:
            print(f"❌ {test_name} hatası: {e}")
    
    print(f"\\n📊 TEST SONUÇLARI:")
    print(f"   • Başarılı: {successful}/{len(tests)}")
    
    if successful == len(tests):
        print("\\n🎉 TÜM TESTLER BAŞARILI!")
        print("   Yerel AI modelleri hazır!")
    else:
        print("\\n⚠️ BAZI TESTLER BAŞARISIZ")
        print("   Dependencies kontrol edin: pip install transformers torch")
    
    return successful == len(tests)

if __name__ == "__main__":
    main()
'''
        
        with open("ai_integration/test_local_models.py", "w", encoding="utf-8") as f:
            f.write(test_script)
        
        print(f"   📁 Script'ler oluşturuldu:")
        print(f"     • ai_integration/download_local_models.py")
        print(f"     • ai_integration/test_local_models.py")
        
        return {
            "config": "ai_integration/local_models_config.json",
            "download_script": "ai_integration/download_local_models.py",
            "test_script": "ai_integration/test_local_models.py",
            "total_models": len(local_models)
        }
    
    def create_orchestration_system(self):
        """AI orkestrasyon sistemi oluştur"""
        print("\n🎵 AI ORKESTRASYON SİSTEMİ OLUŞTURULUYOR...")
        
        orchestration_code = '''# ai_orchestrator.py
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor
import hashlib

class AIOrchestrator:
    """AI servislerini orkestre eden sistem"""
    
    def __init__(self, config_path: str = None):
        self.tasks_queue = asyncio.Queue()
        self.results_cache = {}
        self.worker_pool = ThreadPoolExecutor(max_workers=5)
        self.load_config(config_path)
        
        print(f"🎵 AI Orkestratör Başlatıldı")
        print(f"   • Worker: {self.config['max_workers']}")
        print(f"   • Queue size: {self.config['max_queue_size']}")
        print(f"   • Cache: {'Aktif' if self.config['enable_cache'] else 'Pasif'}")
    
    def load_config(self, config_path: str = None):
        """Config yükle"""
        default_config = {
            "max_workers": 5,
            "max_queue_size": 100,
            "timeout": 60,
            "retry_attempts": 3,
            "enable_cache": True,
            "cache_ttl": 3600,  # 1 saat
            "load_balancing": "round_robin",
            "fallback_strategy": "cascade",
            "monitoring": True,
            "log_level": "info"
        }
        
        self.config = default_config
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    self.config.update(user_config)
            except:
                print(f"⚠️ Config dosyası okunamadı: {config_path}")
    
    def get_task_hash(self, prompt: str, provider: str) -> str:
        """Task için hash oluştur (cache için)"""
        task_str = f"{prompt}:{provider}:{datetime.now().strftime('%Y%m%d%H')}"
        return hashlib.md5(task_str.encode()).hexdigest()
    
    async def orchestrate_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Task'ı orkestre et"""
        task_id = task.get("id", "unknown")
        prompt = task.get("prompt", "")
        provider = task.get("provider", "auto")
        priority = task.get("priority", "normal")
        
        print(f"   🎼 Orkestrasyon: {task_id} ({priority})")
        
        # Cache kontrolü
        if self.config["enable_cache"]:
            cache_key = self.get_task_hash(prompt, provider)
            if cache_key in self.results_cache:
                cached = self.results_cache[cache_key]
                # TTL kontrolü
                if (datetime.now() - cached["timestamp"]).seconds < self.config["cache_ttl"]:
                    print(f"     ⚡ Cache'ten: {task_id}")
                    return {**cached["result"], "cached": True, "cache_key": cache_key}
        
        # Task processing
        try:
            # Unified API'yi kullan
            from unified_ai_api import UnifiedAIApi
            ai = UnifiedAIApi()
            
            # Provider seçimi
            if provider == "auto":
                routing = ai.smart_router(prompt)
                provider = routing["selected_provider"]
            
            # Task execution
            result = await asyncio.get_event_loop().run_in_executor(
                self.worker_pool,
                lambda: ai.generate(prompt, context={"orchestrated": True, "task_id": task_id})
            )
            
            # Cache'e kaydet
            if self.config["enable_cache"] and result.get("success"):
                cache_key = self.get_task_hash(prompt, provider)
                self.results_cache[cache_key] = {
                    "result": result,
                    "timestamp": datetime.now(),
                    "hits": 1
                }
            
            return {**result, "orchestrated": True, "task_id": task_id}
            
        except Exception as e:
            return {
                "error": str(e),
                "task_id": task_id,
                "success": False,
                "orchestrated": True
            }
    
    async def parallel_orchestration(self, tasks: List[Dict]) -> Dict[str, Any]:
        """Paralel orkestrasyon"""
        print(f"🎵 PARALEL ORKESTRASYON: {len(tasks)} task")
        
        # Task'ları kuyruğa ekle
        for task in tasks:
            await self.tasks_queue.put(task)
        
        results = []
        
        # Worker'ları başlat
        async def worker(worker_id: int):
            while not self.tasks_queue.empty():
                try:
                    task = await self.tasks_queue.get()
                    print(f"   👷 Worker {worker_id}: {task.get('id', 'unknown')}")
                    
                    result = await self.orchestrate_task(task)
                    results.append(result)
                    
                    self.tasks_queue.task_done()
                    
                except Exception as e:
                    print(f"   ❌ Worker {worker_id} hatası: {e}")
        
        # Worker pool oluştur
        worker_tasks = []
        for i in range(min(self.config["max_workers"], len(tasks))):
            worker_tasks.append(asyncio.create_task(worker(i + 1)))
        
        # Tüm task'ların bitmesini bekle
        await self.tasks_queue.join()
        
        # Worker'ları durdur
        for task in worker_tasks:
            task.cancel()
        
        # Sonuçları analiz et
        successful = sum(1 for r in results if r.get("success"))
        failed = len(results) - successful
        cached = sum(1 for r in results if r.get("cached", False))
        
        return {
            "total_tasks": len(tasks),
            "successful": successful,
            "failed": failed,
            "cached_responses": cached,
            "results": results,
            "summary": {
                "success_rate": successful / len(tasks) if tasks else 0,
                "cache_hit_rate": cached / len(tasks) if tasks else 0,
                "avg_processing_time": sum(r.get("processing_time", 0) for r in results) / len(results) if results else 0
            }
        }
    
    def create_pipeline(self, steps: List[Dict]) -> Dict[str, Any]:
        """AI pipeline oluştur"""
        print(f"🔄 AI PIPELINE OLUŞTURULUYOR: {len(steps)} adım")
        
        pipeline_results = []
        
        for i, step in enumerate(steps, 1):
            print(f"   🔧 Adım {i}/{len(steps)}: {step.get('name', 'Unnamed')}")
            
            # Önceki adımların sonuçlarını kullan
            context = {}
            if i > 1:
                context = {"previous_steps": pipeline_results}
            
            # Step execution
            try:
                from unified_ai_api import UnifiedAIApi
                ai = UnifiedAIApi()
                
                prompt = step.get("prompt", "")
                if context:
                    # Context'i prompt'a ekle
                    prompt = f"{prompt}\\n\\nContext: {json.dumps(context, indent=2)}"
                
                result = ai.generate(prompt, context={**context, "pipeline_step": i})
                
                pipeline_results.append({
                    "step": i,
                    "name": step.get("name"),
                    "result": result,
                    "success": result.get("success", False)
                })
                
                if result.get("success"):
                    print(f"     ✅ Adım {i} tamamlandı")
                else:
                    print(f"     ❌ Adım {i} başarısız: {result.get('error', 'Unknown')}")
                    
            except Exception as e:
                print(f"     ❌ Adım {i} hatası: {e}")
                pipeline_results.append({
                    "step": i,
                    "name": step.get("name"),
                    "error": str(e),
                    "success": False
                })
        
        # Pipeline sonucu
        successful_steps = sum(1 for r in pipeline_results if r.get("success"))
        
        return {
            "total_steps": len(steps),
            "successful_steps": successful_steps,
            "pipeline_results": pipeline_results,
            "pipeline_success": successful_steps == len(steps),
            "final_output": pipeline_results[-1]["result"] if pipeline_results else None
        }

# Kullanım örneği
async def example_usage():
    """Örnek kullanım"""
    print("🎵 AI ORKESTRASYON ÖRNEĞİ")
    print("="*50)
    
    orchestrator = AIOrchestrator()
    
    # Örnek task'lar
    tasks = [
        {
            "id": "task_1",
            "prompt": "Python'da fibonacci fonksiyonu yaz",
            "provider": "auto",
            "priority": "high"
        },
        {
            "id": "task_2", 
            "prompt": "AI etiği hakkında 100 kelime yaz",
            "provider": "auto",
            "priority": "normal"
        },
        {
            "id": "task_3",
            "prompt": "Robotik sistemlerin geleceği nedir?",
            "provider": "auto", 
            "priority": "low"
        }
    ]
    
    # Paralel orkestrasyon
    print("\\n1. PARALEL ORKESTRASYON:")
    parallel_result = await orchestrator.parallel_orchestration(tasks)
    
    print(f"\\n📊 PARALEL SONUÇLAR:")
    print(f"   • Toplam task: {parallel_result['total_tasks']}")
    print(f"   • Başarılı: {parallel_result['successful']}")
    print(f"   • Cache hit: {parallel_result['cached_responses']}")
    
    # Pipeline örneği
    print("\\n2. AI PIPELINE:")
    pipeline_steps = [
        {
            "name": "Problem Analizi",
            "prompt": "Küresel ısınma problemini analiz et"
        },
        {
            "name": "Çözüm Önerileri",
            "prompt": "Küresel ısınma için teknolojik çözümler öner"
        },
        {
            "name": "Uygulama Planı",
            "prompt": "Bu çözümlerin uygulama planını oluştur"
        }
    ]
    
    pipeline_result = orchestrator.create_pipeline(pipeline_steps)
    
    print(f"\\n📊 PIPELINE SONUÇLARI:")
    print(f"   • Toplam adım: {pipeline_result['total_steps']}")
    print(f"   • Başarılı adım: {pipeline_result['successful_steps']}")
    print(f"   • Pipeline başarı: {pipeline_result['pipeline_success']}")
    
    if pipeline_result['final_output'] and pipeline_result['final_output'].get('success'):
        final_content = pipeline_result['final_output'].get('content', '')
        print(f"\\n🎯 FİNAL ÇIKTI (ilk 200 karakter):")
        print(f"{final_content[:200]}...")
    
    return {
        "parallel": parallel_result,
        "pipeline": pipeline_result
    }

if __name__ == "__main__":
    # Asenkron fonksiyonu çalıştır
    import asyncio
    results = asyncio.run(example_usage())
    
    print("\\n" + "="*50)
    print("✅ AI ORKESTRASYON TESTİ TAMAMLANDI!")
    print("="*50)
'''
        
        with open("ai_integration/ai_orchestrator.py", "w", encoding="utf-8") as f:
            f.write(orchestration_code)
        
        print("   ✅ Orkestrasyon sistemi oluşturuldu: ai_integration/ai_orchestrator.py")
        
        return "ai_integration/ai_orchestrator.py"
    
    def create_monitoring_dashboard(self):
        """AI monitoring dashboard oluştur"""
        print("\n📊 AI MONITORING DASHBOARD OLUŞTURULUYOR...")
        
        dashboard_code = '''# ai_monitor.py
import json
import time
from datetime import datetime, timedelta
from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict, List, Any
import os

class AIMonitor:
    """AI sistemlerini izleme dashboard'ı"""
    
    def __init__(self, log_dir: str = "ai_logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        
        self.metrics = {
            "requests": defaultdict(list),
            "responses": defaultdict(list),
            "errors": defaultdict(list),
            "latency": defaultdict(list),
            "costs": defaultdict(float)
        }
        
        print(f"📊 AI Monitor Başlatıldı")
        print(f"   • Log dizini: {log_dir}")
        print(f"   • Metrikler: {len(self.metrics)} kategori")
    
    def log_request(self, provider: str, prompt: str, timestamp: datetime = None):
        """Request log'u"""
        if timestamp is None:
            timestamp = datetime.now()
        
        log_entry = {
            "provider": provider,
            "prompt_length": len(prompt),
            "timestamp": timestamp.isoformat(),
            "hour": timestamp.hour
        }
        
        self.metrics["requests"][provider].append(log_entry)
        
        # Dosyaya log
        self._save_log("requests", log_entry)
    
    def log_response(self, provider: str, result: Dict, timestamp: datetime = None):
        """Response log'u"""
        if timestamp is None:
            timestamp = datetime.now()
        
        success = result.get("success", False)
        processing_time = result.get("processing_time", 0)
        token_usage = result.get("usage", {}).get("total_tokens", 0)
        estimated_cost = result.get("usage", {}).get("estimated_cost", 0)
        
        log_entry = {
            "provider": provider,
            "success": success,
            "processing_time": processing_time,
            "tokens": token_usage,
            "estimated_cost": estimated_cost,
            "timestamp": timestamp.isoformat()
        }
        
        self.metrics["responses"][provider].append(log_entry)
        
        if estimated_cost > 0:
            self.metrics["costs"][provider] += estimated_cost
        
        # Dosyaya log
        self._save_log("responses", log_entry)
        
        # Latency metrik
        self.metrics["latency"][provider].append(processing_time)
    
    def log_error(self, provider: str, error: str, timestamp: datetime = None):
        """Error log'u"""
        if timestamp is None:
            timestamp = datetime.now()
        
        log_entry = {
            "provider": provider,
            "error": error,
            "timestamp": timestamp.isoformat()
        }
        
        self.metrics["errors"][provider].append(log_entry)
        
        # Dosyaya log
        self._save_log("errors", log_entry)
    
    def _save_log(self, log_type: str, entry: Dict):
        """Log'u dosyaya kaydet"""
        date_str = datetime.now().strftime("%Y%m%d")
        log_file = os.path.join(self.log_dir, f"{log_type}_{date_str}.jsonl")
        
        try:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\\n")
        except Exception as e:
            print(f"⚠️ Log kaydetme hatası: {e}")
    
    def get_stats(self, hours: int = 24) -> Dict[str, Any]:
        """Son X saatlik istatistikleri getir"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        stats = {
            "total_requests": 0,
            "total_responses": 0,
            "total_errors": 0,
            "success_rate": 0,
            "avg_latency": 0,
            "total_cost": 0,
            "by_provider": {},
            "hourly_traffic": defaultdict(int)
        }
        
        # Tüm metrikleri filtrele
        for provider in self.metrics["requests"]:
            provider_stats = {
                "requests": 0,
                "responses": 0,
                "errors": 0,
                "success_rate": 0,
                "avg_latency": 0,
                "total_cost": 0
            }
            
            # Requests
            provider_requests = [
                r for r in self.metrics["requests"][provider]
                if datetime.fromisoformat(r["timestamp"]) > cutoff_time
            ]
            provider_stats["requests"] = len(provider_requests)
            
            # Responses
            provider_responses = [
                r for r in self.metrics["responses"][provider]
                if datetime.fromisoformat(r["timestamp"]) > cutoff_time
            ]
            provider_stats["responses"] = len(provider_responses)
            
            # Errors
            provider_errors = [
                e for e in self.metrics["errors"][provider]
                if datetime.fromisoformat(e["timestamp"]) > cutoff_time
            ]
            provider_stats["errors"] = len(provider_errors)
            
            # Success rate
            if provider_responses:
                successful = sum(1 for r in provider_responses if r.get("success", False))
                provider_stats["success_rate"] = successful / len(provider_responses)
            
            # Average latency
            latencies = [
                r["processing_time"] for r in provider_responses
                if "processing_time" in r
            ]
            if latencies:
                provider_stats["avg_latency"] = sum(latencies) / len(latencies)
            
            # Total cost
            provider_stats["total_cost"] = self.metrics["costs"].get(provider, 0)
            
            stats["by_provider"][provider] = provider_stats
            
            # Toplamlara ekle
            stats["total_requests"] += provider_stats["requests"]
            stats["total_responses"] += provider_stats["responses"]
            stats["total_errors"] += provider_stats["errors"]
            stats["total_cost"] += provider_stats["total_cost"]
            
            # Hourly traffic
            for request in provider_requests:
                hour = datetime.fromisoformat(request["timestamp"]).strftime("%H:00")
                stats["hourly_traffic"][hour] += 1
        
        # Genel success rate
        if stats["total_responses"] > 0:
            stats["success_rate"] = sum(
                p["success_rate"] * p["responses"] for p in stats["by_provider"].values()
            ) / stats["total_responses"]
        
        # Average latency
        all_latencies = []
        for provider_data in stats["by_provider"].values():
            if provider_data["avg_latency"] > 0:
                all_latencies.append(provider_data["avg_latency"])
        
        if all_latencies:
            stats["avg_latency"] = sum(all_latencies) / len(all_latencies)
        
        return stats
    
    def generate_report(self, hours: int = 24) -> str:
        """Rapor oluştur"""
        stats = self.get_stats(hours)
        
        report = f"""
🤖 AI SİSTEM MONITORING RAPORU
{'='*60}
Zaman Aralığı: Son {hours} saat
Rapor Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 GENEL İSTATİSTİKLER:
   • Toplam İstek: {stats['total_requests']:,}
   • Toplam Yanıt: {stats['total_responses']:,}
   • Toplam Hata: {stats['total_errors']:,}
   • Başarı Oranı: %{stats['success_rate']*100:.1f}
   • Ortalama Gecikme: {stats['avg_latency']:.2f}s
   • Toplam Maliyet: ${stats['total_cost']:.4f}

🔧 PROVIDER BAZINDA:
"""
        
        for provider, provider_stats in stats["by_provider"].items():
            report += f"""
   {provider.upper()}:
     • İstek: {provider_stats['requests']:,}
     • Yanıt: {provider_stats['responses']:,}
     • Hata: {provider_stats['errors']:,}
     • Başarı: %{provider_stats['success_rate']*100:.1f}
     • Gecikme: {provider_stats['avg_latency']:.2f}s
     • Maliyet: ${provider_stats['total_cost']:.4f}
"""
        
        # Hourly traffic
        if stats["hourly_traffic"]:
            report += f"""
⏰ SAATLİK TRAFİK:
"""
            for hour in sorted(stats["hourly_traffic"].keys()):
                report += f"   • {hour}: {stats['hourly_traffic'][hour]:,} istek\\n"
        
        report += f"""
{'='*60}
⚠️ ÖNERİLER:
"""
        
        # Öneriler
        if stats["total_errors"] > stats["total_requests"] * 0.1:  # %10'dan fazla hata
            report += "   • Hata oranı yüksek! Provider bağlantılarını kontrol edin.\\n"
        
        if stats["avg_latency"] > 5:  # 5 saniyeden fazla
            report += "   • Gecikme yüksek! Yerel modelleri düşünün.\\n"
        
        if stats["total_cost"] > 10:  # $10'dan fazla
            report += "   • Maliyet yüksek! Ücretsiz tier veya yerel modellere geçin.\\n"
        
        if len(stats["by_provider"]) == 1:
            report += "   • Sadece 1 provider kullanıyorsunuz. Çeşitlendirmeyi düşünün.\\n"
        
        report += f"{'='*60}"
        
        return report
    
    def plot_metrics(self, save_path: str = "ai_metrics.png"):
        """Metrikleri görselleştir"""
        try:
            stats = self.get_stats(24)
            
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            fig.suptitle('🤖 AI Sistem Metrikleri', fontsize=16)
            
            # 1. Provider bazında istekler
            providers = list(stats["by_provider"].keys())
            requests = [stats["by_provider"][p]["requests"] for p in providers]
            
            axes[0, 0].bar(providers, requests, color='skyblue')
            axes[0, 0].set_title('Provider Bazında İstekler')
            axes[0, 0].set_ylabel('İstek Sayısı')
            axes[0, 0].tick_params(axis='x', rotation=45)
            
            # 2. Başarı oranları
            success_rates = [stats["by_provider"][p]["success_rate"] * 100 for p in providers]
            
            axes[0, 1].bar(providers, success_rates, color='lightgreen')
            axes[0, 1].set_title('Başarı Oranları (%)')
            axes[0, 1].set_ylabel('Başarı Oranı %')
            axes[0, 1].tick_params(axis='x', rotation=45)
            axes[0, 1].set_ylim(0, 100)
            
            # 3. Ortalama gecikme
            latencies = [stats["by_provider"][p]["avg_latency"] for p in providers]
            
            axes[1, 0].bar(providers, latencies, color='lightcoral')
            axes[1, 0].set_title('Ortalama Gecikme (saniye)')
            axes[1, 0].set_ylabel('Gecikme (s)')
            axes[1, 0].tick_params(axis='x', rotation=45)
            
            # 4. Maliyet
            costs = [stats["by_provider"][p]["total_cost"] for p in providers]
            
            axes[1, 1].bar(providers, costs, color='gold')
            axes[1, 1].set_title('Toplam Maliyet ($)')
            axes[1, 1].set_ylabel('Maliyet ($)')
            axes[1, 1].tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"📈 Grafik oluşturuldu: {save_path}")
            return save_path
            
        except Exception as e:
            print(f"⚠️ Grafik oluşturma hatası: {e}")
            return None

# Kullanım örneği
def example_monitoring():
    """Örnek monitoring"""
    print("📊 AI MONITORING ÖRNEĞİ")
    print("="*50)
    
    monitor = AIMonitor()
    
    # Örnek log'lar ekle
    test_time = datetime.now()
    
    # Request log'ları
    monitor.log_request("openai", "Python fibonacci kodu", test_time - timedelta(hours=1))
    monitor.log_request("google", "AI etiği makalesi", test_time - timedelta(minutes=30))
    monitor.log_request("local", "Test prompt", test_time - timedelta(minutes=15))
    
    # Response log'ları
    monitor.log_response("openai", {
        "success": True,
        "processing_time": 1.5,
        "usage": {"total_tokens": 150, "estimated_cost": 0.0045}
    }, test_time - timedelta(hours=1, minutes=5))
    
    monitor.log_response("google", {
        "success": True,
        "processing_time": 2.1,
        "usage": {"total_tokens": 200, "estimated_cost": 0.0}
    }, test_time - timedelta(minutes=25))
    
    monitor.log_response("local", {
        "success": False,
        "processing_time": 0.8,
        "usage": {"total_tokens": 0, "estimated_cost": 0.0}
    }, test_time - timedelta(minutes=10))
    
    # Error log'ları
    monitor.log_error("local", "Model yüklenemedi", test_time - timedelta(minutes=10))
    
    # Rapor oluştur
    print("\\n📄 24 SAATLİK RAPOR:")
    report = monitor.generate_report(24)
    print(report)
    
    # Grafik oluştur
    chart_path = monitor.plot_metrics("ai_metrics_example.png")
    if chart_path:
        print(f"\\n📈 Grafik kaydedildi: {chart_path}")
    
    # Detaylı istatistikler
    stats = monitor.get_stats(24)
    print(f"\\n📊 DETAYLI İSTATİSTİKLER:")
    print(f"   • Toplam Provider: {len(stats['by_provider'])}")
    print(f"   • Saatlik trafik kayıt: {len(stats['hourly_traffic'])}")
    
    return {
        "report": report,
        "chart": chart_path,
        "stats": stats
    }

if __name__ == "__main__":
    results = example_monitoring()
    
    print("\\n" + "="*50)
    print("✅ AI MONITORING TESTİ TAMAMLANDI!")
    print("="*50)
'''
        
        with open("ai_integration/ai_monitor.py", "w", encoding="utf-8") as f:
            f.write(dashboard_code)
        
        print("   ✅ Monitoring dashboard oluşturuldu: ai_integration/ai_monitor.py")
        
        return "ai_integration/ai_monitor.py"
    
    def create_main_integration(self):
        """Ana entegrasyon script'i oluştur"""
        print("\n🚀 ANA ENTEGRASYON SCRIPT'I OLUŞTURULUYOR...")
        
        main_code = '''# main_ai_integration.py
#!/usr/bin/env python3
"""
🤖 ALL AI INTEGRATION SYSTEM - Ana Script
Tüm AI sistemlerini başlatır ve entegre eder.
"""

import os
import sys
import json
from datetime import datetime

def print_header():
    """Başlık yazdır"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║     🤖 ALL AI INTEGRATION SYSTEM v2.0                        ║
║     Tüm AI modelleri tek sistemde                            ║
║     Offline + Online + Yerel + Bulut + Orkestrasyon          ║
╚══════════════════════════════════════════════════════════════╝
    """)

def check_environment():
    """Ortam kontrolü"""
    print("🔍 ORTAM KONTROLÜ:")
    
    # Python versiyonu
    python_version = sys.version_info
    print(f"   • Python: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Gerekli klasörler
    required_dirs = ["ai_integration", "models", "ai_logs"]
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
            print(f"   📁 {dir_name}: Oluşturuldu")
        else:
            print(f"   📁 {dir_name}: Mevcut")
    
    # API Key kontrolü (opsiyonel)
    print("\\n🔑 API KEY DURUMU (Opsiyonel):")
    api_keys = {
        "OPENAI_API_KEY": "OpenAI GPT/DALL-E",
        "GOOGLE_API_KEY": "Google Gemini",
        "ANTHROPIC_API_KEY": "Anthropic Claude", 
        "HUGGINGFACE_TOKEN": "Hugging Face",
        "STABILITY_API_KEY": "Stable Diffusion"
    }
    
    for env_var, service in api_keys.items():
        if os.getenv(env_var):
            print(f"   ✅ {service}: Mevcut")
        else:
            print(f"   ⚠️ {service}: Bulunamadı (isteğe bağlı)")

def setup_system():
    """Sistemi kur"""
    print("\\n📦 SİSTEM KURULUMU:")
    
    try:
        # AI Integration sistemini başlat
        from all_ai_integration import AllAIIntegration
        
        integrator = AllAIIntegration()
        
        # 1. Ortamı kur
        print("\\n1. AI Ortamı Kuruluyor...")
        env_result = integrator.setup_environment()
        
        # 2. Birleşik API oluştur
        print("\\n2. Birleşik API Oluşturuluyor...")
        api_path = integrator.create_unified_api()
        
        # 3. Yerel modelleri kur
        print("\\n3. Yerel Modeller Konfigüre Ediliyor...")
        local_models = integrator.integrate_local_models()
        
        # 4. Orkestrasyon sistemi
        print("\\n4. Orkestrasyon Sistemi Oluşturuluyor...")
        orchestration_path = integrator.create_orchestration_system()
        
        # 5. Monitoring dashboard
        print("\\n5. Monitoring Dashboard Oluşturuluyor...")
        monitor_path = integrator.create_monitoring_dashboard()
        
        return {
            "success": True,
            "environment": env_result,
            "api_path": api_path,
            "local_models": local_models,
            "orchestration_path": orchestration_path,
            "monitor_path": monitor_path,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"❌ Sistem kurulumu başarısız: {e}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

def quick_test():
    """Hızlı test"""
    print("\\n🧪 HIZLI TEST:")
    
    try:
        # Unified API test
        print("1. Unified API Testi...")
        sys.path.append("ai_integration")
        from unified_ai_api import UnifiedAIApi
        
        ai = UnifiedAIApi()
        
        # Basit test
        result = ai.generate("Merhaba, nasılsın?")
        if result.get("success"):
            print(f"   ✅ API çalışıyor: {result.get('provider')}")
            print(f"   Yanıt: {result.get('content', '')[:50]}...")
        else:
            print(f"   ❌ API hatası: {result.get('error', 'Bilinmeyen')}")
        
        # Multi-provider test
        print("\\n2. Multi-Provider Testi...")
        vote_result = ai.multi_provider_vote("Python neden popüler?", providers=["openai", "google", "local"])
        
        if "best_response" in vote_result:
            best = vote_result["best_response"]
            print(f"   ✅ En iyi yanıt: {best['provider']}")
            print(f"   Güven: %{int(best['confidence']*100)}")
        else:
            print(f"   ❌ Multi-provider hatası: {vote_result.get('error', 'Bilinmeyen')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test başarısız: {e}")
        return False

def show_menu():
    """Menü göster"""
    print("\\n📋 ANA MENÜ:")
    print("   1. 🚀 Tüm sistemi başlat")
    print("   2. 🤖 Unified AI API kullan")
    print("   3. 💻 Yerel modelleri test et")
    print("   4. 🎵 Orkestrasyon sistemi")
    print("   5. 📊 Monitoring dashboard")
    print("   6. 📥 Modelleri indir")
    print("   7. 🧪 Tam test sürüşü")
    print("   8. ❌ Çıkış")
    
    try:
        choice = input("\\nSeçiminiz (1-8): ").strip()
        return choice
    except KeyboardInterrupt:
        return "8"

def handle_choice(choice):
    """Seçimi işle"""
    if choice == "1":
        # Tüm sistemi başlat
        print("\\n🚀 TÜM SİSTEM BAŞLATILIYOR...")
        result = setup_system()
        
        if result["success"]:
            print("\\n✅ SİSTEM BAŞARIYLA KURULDU!")
            print(f"   • API: {result.get('api_path', 'N/A')}")
            print(f"   • Yerel Model: {result.get('local_models', {}).get('total_models', 0)}")
            print(f"   • Orkestrasyon: {result.get('orchestration_path', 'N/A')}")
            print(f"   • Monitor: {result.get('monitor_path', 'N/A')}")
            
            # Config dosyasını kaydet
            config_file = "ai_integration/system_config.json"
            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"\\n📁 Konfigürasyon kaydedildi: {config_file}")
        else:
            print(f"\\n❌ Sistem kurulumu başarısız: {result.get('error', 'Bilinmeyen')}")
    
    elif choice == "2":
        # Unified API
        print("\\n🤖 UNIFIED AI API")
        print("="*50)
        
        try:
            sys.path.append("ai_integration")
            from unified_ai_api import UnifiedAIApi
            
            ai = UnifiedAIApi()
            
            while True:
                prompt = input("\\nSoru (çıkmak için 'exit'): ")
                if prompt.lower() == 'exit':
                    break
                
                result = ai.generate(prompt)
                
                if result.get("success"):
                    print(f"\\n✅ {result.get('provider', 'Unknown')}:")
                    print(f"{result.get('content', '')}")
                    print(f"\\n📊 İstatistikler:")
                    print(f"   • İşlem süresi: {result.get('processing_time', 0):.2f}s")
                    print(f"   • Model: {result.get('model', 'Unknown')}")
                    if 'usage' in result:
                        usage = result['usage']
                        if 'estimated_cost' in usage and usage['estimated_cost'] > 0:
                            print(f"   • Tahmini maliyet: ${usage['estimated_cost']:.6f}")
                else:
                    print(f"\\n❌ Hata: {result.get('error', 'Bilinmeyen')}")
        
        except Exception as e:
            print(f"❌ API hatası: {e}")
    
    elif choice == "3":
        # Yerel modeller
        print("\\n💻 YEREL MODELLER TESTİ")
        print("="*50)
        
        try:
            # Download script'ini çalıştır
            print("1. Modeller indiriliyor...")
            os.system("python ai_integration/download_local_models.py")
            
            print("\\n2. Modeller test ediliyor...")
            os.system("python ai_integration/test_local_models.py")
            
        except Exception as e:
            print(f"❌ Yerel model hatası: {e}")
    
    elif choice == "4":
        # Orkestrasyon
        print("\\n🎵 AI ORKESTRASYON SİSTEMİ")
        print("="*50)
        
        try:
            import asyncio
            sys.path.append("ai_integration")
            from ai_orchestrator import example_usage
            
            print("Orkestrasyon testi çalıştırılıyor...")
            results = asyncio.run(example_usage())
            
            print("\\n✅ Orkestrasyon testi tamamlandı!")
            
        except Exception as e:
            print(f"❌ Orkestrasyon hatası: {e}")
    
    elif choice == "5":
        # Monitoring
        print("\\n📊 MONITORING DASHBOARD")
        print("="*50)
        
        try:
            sys.path.append("ai_integration")
            from ai_monitor import example_monitoring
            
            results = example_monitoring()
            
            print("\\n✅ Monitoring testi tamamlandı!")
            print(f"   • Rapor: ai_logs/ klasörü")
            print(f"   • Grafik: ai_metrics_example.png")
            
        except Exception as e:
            print(f"❌ Monitoring hatası: {e}")
    
    elif choice == "6":
        # Model download
        print("\\n📥 MODELLERİ İNDİR")
        print("="*50)
        
        try:
            print("Modeller indiriliyor...")
            import subprocess
            result = subprocess.run(
                [sys.executable, "ai_integration/download_local_models.py"],
                capture_output=True,
                text=True
            )
            
            print(result.stdout)
            if result.stderr:
                print(f"Hata: {result.stderr}")
            
        except Exception as e:
            print(f"❌ İndirme hatası: {e}")
    
    elif choice == "7":
        # Tam test
        print("\\n🧪 TAM TEST SÜRÜŞÜ")
        print("="*50)
        
        success = quick_test()
        
        if success:
            print("\\n🎉 TÜM TESTLER BAŞARILI!")
            print("   Sistem tamamen çalışır durumda!")
        else:
            print("\\n⚠️ BAZI TESTLER BAŞARISIZ")
            print("   Lütfen kurulumu kontrol edin.")
    
    elif choice == "8":
        # Çıkış
        print("\\n👋 GÜLE GÜLE!")
        sys.exit(0)
    
    else:
        print("\\n❌ Geçersiz seçim! Lütfen 1-8 arası bir sayı girin.")

def main():
    """Ana fonksiyon"""
    print_header()
    check_environment()
    
    print(f"\\n⏰ Başlangıç Zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    while True:
        choice = show_menu()
        handle_choice(choice)
        
        # Menüden sonra devam et
        input("\\nDevam etmek için Enter'a basın...")
        print("\\n" + "="*80)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\\n\\n👋 Program kapatılıyor...")
        sys.exit(0)
    except Exception as e:
        print(f"\\n❌ Beklenmeyen hata: {e}")
        sys.exit(1)
'''
        
        with open("main_ai_integration.py", "w", encoding="utf-8") as f:
            f.write(main_code)
        
        print("   ✅ Ana entegrasyon script'i oluşturuldu: main_ai_integration.py")
        
        # CHMOD (Unix/Linux için)
        if os.name != 'nt':  # Windows değilse
            os.chmod("main_ai_integration.py", 0o755)
        
        return "main_ai_integration.py"
    
    def run_full_integration(self):
        """Tam entegrasyonu çalıştır"""
        print("\n" + "="*80)
        print("🚀 TAM AI ENTEGRASYON BAŞLATILIYOR")
        print("="*80)
        
        results: Dict[str, Optional[Any]] = {
            "environment": None,
            "api": None,
            "local_models": None,
            "orchestration": None,
            "monitoring": None,
            "main_script": None
        }
        
        try:
            # 1. Ortam kurulumu
            print("\n1. 📦 ORTAM KURULUMU...")
            results["environment"] = self.setup_environment()
            
            # 2. Birleşik API
            print("\n2. 🔗 BİRLEŞİK API...")
            results["api"] = self.create_unified_api()
            
            # 3. Yerel modeller
            print("\n3. 💻 YEREL MODELLER...")
            results["local_models"] = self.integrate_local_models()
            
            # 4. Orkestrasyon
            print("\n4. 🎵 ORKESTRASYON...")
            results["orchestration"] = self.create_orchestration_system()
            
            # 5. Monitoring
            print("\n5. 📊 MONITORING...")
            results["monitoring"] = self.create_monitoring_dashboard()
            
            # 6. Ana script
            print("\n6. 🚀 ANA SCRIPT...")
            results["main_script"] = self.create_main_integration()
            
            print("\n" + "="*80)
            print("✅ TAM ENTEGRASYON TAMAMLANDI!")
            print("="*80)
            
            # Sonuç özeti
            print(f"""
📊 ENTEGRASYON SONUÇLARI:
   • Ortam: {len(results['environment']['installed'])}/{results['environment']['total']} paket
   • API: {results['api']}
   • Yerel Model: {results['local_models']['total_models']}
   • Orkestrasyon: {results['orchestration']}
   • Monitoring: {results['monitoring']}
   • Ana Script: {results['main_script']}

🚀 ÇALIŞTIRMAK İÇİN:
   python main_ai_integration.py

📁 OLUŞTURULAN DOSYALAR:
   • ai_integration/ - Tüm AI modülleri
   • models/ - İndirilen modeller
   • ai_logs/ - Monitoring log'ları

💡 ÖRNEK KULLANIM:
   1. Ana menüden "1" seçerek tüm sistemi başlat
   2. "2" seçerek AI sohbeti başlat
   3. "7" seçerek tam test yap

⚠️ NOT: API key'lerinizi .env dosyasına eklemeyi unutmayın:
   OPENAI_API_KEY=sk-...
   GOOGLE_API_KEY=...
   ANTHROPIC_API_KEY=...
            """)
            
            return {
                "success": True,
                "results": results,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"\n❌ ENTEGRASYON HATASI: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

def main():
    """Ana fonksiyon"""
    integrator = AllAIIntegration()
    
    # Tam entegrasyonu çalıştır
    result = integrator.run_full_integration()
    
    if result["success"]:
        print("\n🎉 ALL AI INTEGRATION SİSTEMİ HAZIR!")
        print("Artık tüm AI modellerini tek sistemde kullanabilirsiniz!")
    else:
        print(f"\n❌ Sistem kurulumunda hata: {result['error']}")
        print("Lütfen bağımlılıkları kontrol edin ve tekrar deneyin.")
    
    return result

if __name__ == "__main__":
    main()
if __name__ == "__main__":
    main()
if __name__ == "__main__":
    main()
