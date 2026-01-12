import os

import requests
from dotenv import load_dotenv

# .env dosyasındaki ortam değişkenlerini yükle
load_dotenv()

# Ortam değişkenlerinden API anahtarlarını al
github_api_key = os.getenv("GITHUB_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")
google_ai_studio_key = os.getenv("GOOGLE_AI_STUDIO_KEY")
hugging_face_api_key = os.getenv("HUGGING_FACE_API_KEY")
cohere_api_key = os.getenv("COHERE_API_KEY")
infura_api_key = os.getenv("INFURA_API_KEY")
moralis_api_key = os.getenv("MORALIS_API_KEY")
chainlink_api_key = os.getenv("CHAINLINK_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
render_api_key = os.getenv("RENDER_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
fireworks_api_key = os.getenv("FIREWORKS_API_KEY")
twilio_api_key = os.getenv("TWILIO_API_KEY")
firebase_api_key = os.getenv("FIREBASE_API_KEY")
supabase_api_key = os.getenv("SUPABASE_API_KEY")
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
fal_ai_api_key = os.getenv("FAL_AI_API_KEY")
poe_api_key = os.getenv("POE_API_KEY")
serpapi_api_key = os.getenv("SERPAPI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

# Anahtarların varlığını kontrol et
print("API Anahtar Durumları:")
print("-" * 30)

key_map = {
    "GITHUB_API_KEY": (github_api_key, "GitHub"),
    "GOOGLE_API_KEY": (google_api_key, "Google (YouTube)"),
    "GOOGLE_AI_STUDIO_KEY": (google_ai_studio_key, "Google AI Studio (Gemini)"),
    "HUGGING_FACE_API_KEY": (hugging_face_api_key, "Hugging Face"),
    "COHERE_API_KEY": (cohere_api_key, "Cohere"),
    "INFURA_API_KEY": (infura_api_key, "Infura (Blockchain)"),
    "MORALIS_API_KEY": (moralis_api_key, "Moralis (Blockchain)"),
    "CHAINLINK_API_KEY": (chainlink_api_key, "Chainlink (Blockchain)"),
    "OPENAI_API_KEY": (openai_api_key, "OpenAI"),
    "RENDER_API_KEY": (render_api_key, "Render (Cloud)"),
    "GROQ_API_KEY": (groq_api_key, "Groq (LLM)"),
    "OPENROUTER_API_KEY": (openrouter_api_key, "OpenRouter (LLM)"),
    "FIREWORKS_API_KEY": (fireworks_api_key, "Fireworks AI (LLM)"),
    "TWILIO_API_KEY": (twilio_api_key, "Twilio (Communications)"),
    "FIREBASE_API_KEY": (firebase_api_key, "Firebase (BaaS)"),
    "SUPABASE_API_KEY": (supabase_api_key, "Supabase (BaaS)"),
    "DEEPSEEK_API_KEY": (deepseek_api_key, "DeepSeek (LLM)"),
    "FAL_AI_API_KEY": (fal_ai_api_key, "Fal.ai (AI Models)"),
    "POE_API_KEY": (poe_api_key, "Poe (LLM)"),
    "SERPAPI_API_KEY": (serpapi_api_key, "SerpApi (Search)"),
    "TAVILY_API_KEY": (tavily_api_key, "Tavily (Search)"),
}

all_keys_found = True
for key_name, (key_value, key_desc) in key_map.items():
    if key_value:
        print(f"✅ {key_desc} ({key_name}) başarıyla yüklendi.")
    else:
        print(f"❌ Hata: {key_desc} ({key_name}) ortam değişkeni bulunamadı.")
        all_keys_found = False

print("-" * 30)

# Sadece GitHub anahtarı varsa API isteği yap
if github_api_key:
    # Kimliği doğrulanmış bir istek için başlıkları (headers) hazırla
    headers = {
        "Authorization": f"token {github_api_key}",
        "Accept": "application/vnd.github.v3+json",
    }

    # GitHub API'sine kimliği doğrulanmış kullanıcı bilgilerini almak için bir istek gönder
    url = "https://api.github.com/user"

    try:
        print("\nGitHub API'si test ediliyor...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Olası HTTP hatalarını kontrol et (4xx veya 5xx)

        # Yanıtı işle
        user_data = response.json()
        print(f"✅ GitHub API bağlantısı başarılı! Hoş geldin, {user_data['login']}!")

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            print(
                "❌ Hata: GitHub kimlik doğrulama başarısız. API anahtarınız geçersiz veya süresi dolmuş olabilir."
            )
        else:
            print(f"❌ HTTP Hatası: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"❌ Bağlantı Hatası: {req_err}")

# OpenAI API'sini test et
if openai_api_key:
    try:
        print("\nOpenAI API'si test ediliyor...")
        # Bu kısım, 'openai' kütüphanesinin kurulu olmasını gerektirir.
        # pip install openai
        from openai import OpenAI

        client = OpenAI(api_key=openai_api_key)

        # Modelleri listelemek gibi basit bir istek yapalım
        models = client.models.list()
        print(f"✅ OpenAI API bağlantısı başarılı! {len(models.data)} model bulundu.")

    except ImportError:
        print(
            "⚠️ Uyarı: 'openai' kütüphanesi kurulu değil. 'pip install openai' komutu ile kurabilirsiniz."
        )
    except Exception as e:
        print(f"❌ Hata: OpenAI API bağlantısı kurulamadı. Detay: {e}")


if all_keys_found:
    print("\n🎉 Tüm API anahtarları başarıyla yüklendi ve doğrulandı!")
else:
    print("\n⚠️ Bazı API anahtarları eksik. Lütfen yukarıdaki listeyi kontrol edin.")
