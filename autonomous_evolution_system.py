# autonomous_evolution_system.py
import asyncio
import json
import os
import threading
import time
from datetime import datetime

import schedule


class AutonomousEvolutionSystem:
    def __init__(self):
        self.cycles_completed = 0
        self.languages_learned = 0
        self.languages_created = 0
        self.data_collected = 0
        self.start_time = time.time()
        
        print("""
╔══════════════════════════════════════════════════════╗
║     🤖 OTONOM EVRİM SİSTEMİ v2.0                     ║
║     🌍 Tüm dillerden öğrenme                         ║
║     💻 Tüm kodlama dillerini bilme                   ║
║     🎨 Yeni kodlama dilleri üretme                   ║
╚══════════════════════════════════════════════════════╝
        """)
    
    async def cycle_1_data_collection(self):
        """Döngü 1: Evrensel veri toplama"""
        print(f"\n🌀 DÖNGÜ {self.cycles_completed + 1}.1: VERİ TOPLAMA")
        print("-"*50)
        
        try:
            # Universal data collector'u çalıştır
            import universal_data_collector
            from universal_data_collector import UniversalDataCollector
            
            collector = UniversalDataCollector()
            data, summary = await collector.collect_all_languages()
            
            self.data_collected += summary.get("total_code_blocks", 0)
            
            print(f"✅ Veri toplama tamam: {summary.get('total_code_blocks', 0):,} kod bloğu")
            return True
            
        except Exception as e:
            print(f"❌ Veri toplama hatası: {e}")
            return False
    
    def cycle_2_language_learning(self):
        """Döngü 2: Programlama dillerini öğrenme"""
        print(f"\n🌀 DÖNGÜ {self.cycles_completed + 1}.2: DİL ÖĞRENME")
        print("-"*50)
        
        try:
            # Programming language master'ı çalıştır
            import programming_language_master
            from programming_language_master import ProgrammingLanguageMaster
            
            master = ProgrammingLanguageMaster()
            results = master.learn_from_data()
            
            total_languages = len(results.get("language_distribution", {}))
            self.languages_learned = max(self.languages_learned, total_languages)
            
            print(f"✅ Dil öğrenme tamam: {total_languages} programlama dili")
            return True
            
        except Exception as e:
            print(f"❌ Dil öğrenme hatası: {e}")
            return False
    
    def cycle_3_language_generation(self):
        """Döngü 3: Yeni dil üretimi"""
        print(f"\n🌀 DÖNGÜ {self.cycles_completed + 1}.3: DİL ÜRETİMİ")
        print("-"*50)
        
        try:
            # Language generator'ı çalıştır
            import language_generator_ai
            from language_generator_ai import LanguageGeneratorAI
            
            generator = LanguageGeneratorAI()
            results = generator.generate_multiple_languages(2)
            
            languages_created = len(results)
            self.languages_created += languages_created
            
            print(f"✅ Dil üretimi tamam: {languages_created} yeni dil")
            return True
            
        except Exception as e:
            print(f"❌ Dil üretimi hatası: {e}")
            return False
    
    def cycle_4_analysis_and_improvement(self):
        """Döngü 4: Analiz ve iyileştirme"""
        print(f"\n🌀 DÖNGÜ {self.cycles_completed + 1}.4: ANALİZ")
        print("-"*50)
        
        try:
            # Sistem analizi
            print("📊 SİSTEM ANALİZİ:")
            
            stats = {
                "cycles_completed": self.cycles_completed,
                "languages_learned": self.languages_learned,
                "languages_created": self.languages_created,
                "data_collected": self.data_collected,
                "timestamp": datetime.now().isoformat()
            }
            
            # Dosyaya kaydet
            os.makedirs("evolution_logs", exist_ok=True)
            filename = f"evolution_logs/cycle_{self.cycles_completed + 1}.json"
            
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(stats, f, indent=2, ensure_ascii=False)
            
            print(f"   • Tamamlanan döngü: {stats['cycles_completed'] + 1}")
            print(f"   • Öğrenilen dil: {stats['languages_learned']}")
            print(f"   • Üretilen dil: {stats['languages_created']}")
            print(f"   • Toplanan veri: {stats['data_collected']:,} kod bloğu")
            print(f"   • Kayıt: {filename}")
            
            return True
            
        except Exception as e:
            print(f"❌ Analiz hatası: {e}")
            return False
    
    async def run_evolution_cycle(self):
        """Bir evrim döngüsü çalıştır"""
        print(f"\n{'='*80}")
        print(f"🚀 EVRİM DÖNGÜSÜ {self.cycles_completed + 1} BAŞLIYOR")
        print(f"{'='*80}")
        
        start_time = time.time()
        successes = 0
        
        # 1. Veri toplama
        if await self.cycle_1_data_collection():
            successes += 1
        
        # 2. Dil öğrenme
        if self.cycle_2_language_learning():
            successes += 1
        
        # 3. Dil üretimi
        if self.cycle_3_language_generation():
            successes += 1
        
        # 4. Analiz
        if self.cycle_4_analysis_and_improvement():
            successes += 1
        
        self.cycles_completed += 1
        elapsed_time = time.time() - start_time
        
        print(f"\n{'='*80}")
        print(f"✅ DÖNGÜ {self.cycles_completed} TAMAMLANDI")
        print(f"   • Başarılı adım: {successes}/4")
        print(f"   • Geçen süre: {elapsed_time:.1f} saniye")
        print(f"   • Toplam döngü: {self.cycles_completed}")
        print(f"{'='*80}")
        
        return successes == 4
    
    def schedule_hourly_evolution(self):
        """Saatlik evrim planla"""
        print("\n⏰ SAATLİK EVRİM PLANLANIYOR...")
        
        # Her saat başı evrim döngüsü
        schedule.every().hour.at(":00").do(
            lambda: asyncio.run(self.run_evolution_cycle())
        )
        
        # Her 6 saatte bir ek öğrenme
        schedule.every(6).hours.do(
            lambda: print(f"\n📚 Ek öğrenme modu: {datetime.now().strftime('%H:%M')}")
        )
        
        print(f"   • Plan: Her saat başı tam evrim döngüsü")
        print(f"   • Sonraki: {datetime.now().replace(minute=0, second=0, microsecond=0)}")
    
    async def run_continuous(self):
        """Sürekli çalışan evrim sistemi"""
        print("\n👁️  OTONOM EVRİM SİSTEMİ AKTİF")
        print("💤 Siz uyurken sistem evrimleşecek...")
        
        # İlk döngüyü hemen başlat
        await self.run_evolution_cycle()
        
        # Saatlik planlamayı başlat
        self.schedule_hourly_evolution()
        
        # Zamanlayıcı thread'i
        def schedule_runner():
            while True:
                schedule.run_pending()
                time.sleep(1)
        
        schedule_thread = threading.Thread(target=schedule_runner, daemon=True)
        schedule_thread.start()
        
        # Ana döngü
        try:
            while True:
                # Her dakika durum göster
                current_time = datetime.now().strftime("%H:%M:%S")
                print(f"\n[{current_time}] ⏳ Sistem aktif...")
                print(f"   • Döngü: {self.cycles_completed}")
                print(f"   • Öğrenilen: {self.languages_learned} dil")
                print(f"   • Üretilen: {self.languages_created} dil")
                
                await asyncio.sleep(60)  # 1 dakika bekle
                
        except KeyboardInterrupt:
            print(f"\n\n{'='*80}")
            print("🛑 EVRİM SİSTEMİ DURDURULUYOR...")
            
            final_stats = {
                "total_cycles": self.cycles_completed,
                "total_languages_learned": self.languages_learned,
                "total_languages_created": self.languages_created,
                "total_data_collected": self.data_collected,
                "total_runtime": time.time() - self.start_time,
                "end_time": datetime.now().isoformat()
            }
            
            print(f"📊 FİNAL İSTATİSTİKLER:")
            for key, value in final_stats.items():
                print(f"   • {key.replace('_', ' ').title()}: {value}")
            
            # Final raporu kaydet
            with open("evolution_logs/FINAL_REPORT.json", "w", encoding="utf-8") as f:
                json.dump(final_stats, f, indent=2, ensure_ascii=False)
            
            print(f"\n📁 Rapor kaydedildi: evolution_logs/FINAL_REPORT.json")
            print("✅ Otonom evrim sistemi kapatıldı")
            print(f"{'='*80}")
    
    def start(self):
        """Sistemi başlat"""
        # Gerekli klasörleri oluştur
        os.makedirs("data", exist_ok=True)
        os.makedirs("generated_languages", exist_ok=True)
        os.makedirs("evolution_logs", exist_ok=True)
        os.makedirs("new_languages", exist_ok=True)
        
        # Asenkron döngüyü başlat
        try:
            asyncio.run(self.run_continuous())
        except KeyboardInterrupt:
            print("\n✅ Sistem kapatıldı")

# Ana program
if __name__ == "__main__":
    evolution = AutonomousEvolutionSystem()
    evolution.start()
