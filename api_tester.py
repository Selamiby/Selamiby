"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:18
🚀 Status: ACTIVE / PRODUCTION
"""

import os

from dotenv import load_dotenv

from nexus_brain import NexusBrain


def test_api_keys():
    load_dotenv()
    brain = NexusBrain()

    print("--- NEXUS-ONE API KEY TEST MERKEZİ ---")

    # 1. OpenAI Test
    print("\n[1] OpenAI Test Ediliyor...")
    openai_res = brain._call_openai("Merhaba!", "Test asistanı.")
    if openai_res:
        print(f"✅ OpenAI ÇALIŞIYOR: {openai_res[:50]}...")
    else:
        print("❌ OpenAI HATALI veya KEY GEÇERSİZ.")

    # 2. Groq Test
    print("\n[2] Groq Test Ediliyor...")
    groq_res = brain._call_groq("Hello!", "Test assistant.")
    if groq_res:
        print(f"✅ Groq ÇALIŞIYOR: {groq_res[:50]}...")
    else:
        print("❌ Groq HATALI veya KEY GEÇERSİZ (Şu an .env'de '...' olabilir).")

    # 3. Gemini Test
    print("\n[3] Gemini Test Ediliyor...")
    gemini_res = brain._call_gemini("Test", "Test")
    if gemini_res and "Error" not in gemini_res:
        print(f"✅ Gemini ÇALIŞIYOR: {gemini_res[:50]}...")
    else:
        print("❌ Gemini HATALI veya KEY GEÇERSİZ.")

    # 4. Vision Test
    print("\n[4] Gemini Vision Test Ediliyor...")
    # nexus_logs/current_screen.png varsa onu kullan
    from pathlib import Path
    img_path = Path("nexus_logs/current_screen.png")
    if img_path.exists():
        vision_res = brain.think_with_vision("Bu resimde ne var?", str(img_path))
        print(f"👁️ Vision Sonucu: {vision_res}")
    else:
        print("⚠️ Vision Testi Atlandı: nexus_logs/current_screen.png bulunamadı.")

if __name__ == "__main__":
    test_api_keys()
