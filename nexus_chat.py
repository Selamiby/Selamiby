"""
NEXUS-ONE Chat Assistant
Lightweight background chat interface - Low CPU usage
"""
import asyncio
import sys
from datetime import datetime
from typing import Optional










class ChatAssistant:
    """Hafif sohbet asistanı"""

    def __init__(self):
        self.name = "NEXUS-ONE Chat"
        self.version = "1.0.0"
        self.running = False
        self.chat_history = []
        self.max_history = 50  # Bellekten tasarruf

    def start_chat(self):
        """Sohbeti başlat"""
        self.running = True
        print("\n" + "="*60)
        print("💬 NEXUS-ONE CHAT ASSISTANT")
        print("="*60)
        print("Merhaba! Ben NEXUS-ONE Chat Asistanı.")
        print("Sana her zaman yardımcı olmaya hazırım.")
        print("('exit' veya 'quit' yazarak çıkabilirsin)")
        print("="*60 + "\n")

    async def process_message(self, user_input: str) -> str:
        """Mesajı işle (hafif işlem)"""

        if user_input.lower() in ['exit', 'quit', 'çık']:
            self.running = False
            return "👋 Hoşça kalın!"

        # Hafif yanıtlar - CPU tasarrufu
        responses = {
            "merhaba": "Merhaba! 👋 Nasılsın?",
            "nasılsın": "İyiyim, teşekkür ederim! 😊 Sen nasılsın?",
            "yardım": "🤖 Seni çeşitli konularda yardımcı olabilirim:\n   • Dosya işlemleri\n   • Sistem bilgisi\n   • Görev planlama\n   • Web araştırması",
            "nedir": "Ben NEXUS-ONE Chat Asistanı. Seni her konuda desteklemek için buradayım!",
            "saat": f"🕐 Şu anki saat: {datetime.now().strftime('%H:%M:%S')}",
            "tarih": f"📅 Bugünün tarihi: {datetime.now().strftime('%Y-%m-%d')}",
            "ön": "🚀 NEXUS-ONE v1.0.0 - Autonomous AI Operating System",
            "teşekkür": "Çok hoş! 😊 Seni yardımcı olmaktan mutlu edebilmiş oluşturdum.",
            "thanks": "You're welcome! 😊",
            "hello": "Hello! 👋 Nice to see you!",
        }

        # Yanıt ara
        for keyword, response in responses.items():
            if keyword in user_input.lower():
                return response

        # Varsayılan yanıt
        return f"🤔 '{user_input}' hakkında daha fazla bilgi verebilir misin?"

    async def run_chat_loop(self):
        """Sohbet döngüsü (hafif)"""
        self.start_chat()

        while self.running:
            try:
                user_input = input("👤 Sen: ").strip()

                if not user_input:
                    continue

                # Mesajı işle
                response = await self.process_message(user_input)

                # Hafif gecikmeli yanıt
                await asyncio.sleep(0.1)

                print(f"🤖 NEXUS: {response}\n")

                # Chat geçmişine ekle
                self.chat_history.append({
                    "time": datetime.now().isoformat(),
                    "user": user_input,
                    "nexus": response
                })

                # Bellek optimizasyonu
                if len(self.chat_history) > self.max_history:
                    self.chat_history = self.chat_history[-self.max_history:]

            except KeyboardInterrupt:
                print("\n⚠️ Sohbet kesildi.")
                self.running = False
                break
            except Exception as e:
                print(f"❌ Hata: {e}")
                await asyncio.sleep(0.5)

    def get_chat_summary(self) -> dict:
        """Sohbet özeti al"""
        return {
            "total_messages": len(self.chat_history),
            "start_time": self.chat_history[0]["time"] if self.chat_history else None,
            "last_message": self.chat_history[-1] if self.chat_history else None
        }

async def start_lightweight_chat():
    """Hafif sohbeti başlat"""
    chat = ChatAssistant()
    await chat.run_chat_loop()

    # Özet göster
    summary = chat.get_chat_summary()
    if summary["total_messages"] > 0:
        print("\n" + "="*60)
        print("📊 Sohbet Özeti")
        print("="*60)
        print(f"📝 Toplam Mesaj: {summary['total_messages']}")
        print(f"⏰ Başlama Saati: {summary['start_time'][:19]}")
        print("="*60 + "\n")

if __name__ == "__main__":
    try:
        # Windows encoding fix
        if sys.platform == "win32":
            import os
            os.system("chcp 65001 > nul")

        # Start chat
        asyncio.run(start_lightweight_chat())

    except KeyboardInterrupt:
        print("\n👋 Chat terminated.")
    except Exception as e:
        print(f"🚨 Error: {e}")
        import traceback
        traceback.print_exc()
