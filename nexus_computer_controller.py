import asyncio
"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:16
🚀 Status: ACTIVE / PRODUCTION
"""

import logging
import os
import subprocess
import time
from pathlib import Path

import pyautogui
from PIL import Image

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] 🖥️ COMPUTER-CONTROLLER: %(message)s")
logger = logging.getLogger("ComputerController")

class ComputerController:
    """
    NEXUS-ONE Fiziksel Bilgisayar Kullanım Birimi.
    Bilgisayarı bir insan gibi kontrol eder ve GÖRÜR.
    """
    def __init__(self):
        pyautogui.FAILSAFE = True  # Fareyi sol üste çekmek işlemi durdurur
        self.workspace = Path("c:/Users/selam/NEXUS-ONE")
        self.logs_dir = self.workspace / "nexus_logs"
        self.logs_dir.mkdir(exist_ok=True)

    def execute_action(self, action_description: str):
        """Doğal dilden gelen komutu fiziksel eyleme dönüştürür."""
        logger.info(f"Komut Alındı: {action_description}")
        
        ad = action_description.lower()

        if "visual studio" in ad or "code" in ad or "editör" in ad:
            return self.open_vscode()
        elif "chrome" in ad:
            return self.open_specific_browser("chrome")
        elif "edge" in ad:
            return self.open_specific_browser("msedge")
        elif "firefox" in ad:
            return self.open_specific_browser("firefox")
        elif "tarayıcı" in ad:
            return self.open_browser()
        elif "masaüstü" in ad and "göster" in ad:
            pyautogui.hotkey('win', 'd')
            return "Masaüstü gösterildi."
        elif "başlat" in ad or "çalıştır" in ad:
            # Örn: 'Not defteri çalıştır' veya 'calculator başlat'
            app_name = ad.replace("başlat", "").replace("çalıştır", "").strip()
            return self.run_any_app(app_name)
        elif "ekranı gör" in ad or "ne görüyorsun" in ad:
            return self.see_and_analyze()
        elif "indir" in ad or "yükle" in ad or "install" in ad:
            # Örn: 'vlc indir' veya 'python yükle'
            target = ad.replace("indir", "").replace("yükle", "").replace("install", "").strip()
            return self.download_and_install(target)
        elif "yaz" in ad:
            # Örn: 'NEXUS yaz'
            text = action_description.split("yaz")[-1].strip()
            pyautogui.write(text, interval=0.1)
            return f"'{text}' yazıldı."
        
        return "Komut anlaşıldı ancak henüz fiziksel karşılığı tanımlanmadı."

    def open_vscode(self):
        logger.info("Visual Studio Code açılıyor...")
        try:
            subprocess.Popen(["code", "."], shell=True, cwd=self.workspace)
            time.sleep(3)
            return "Visual Studio Code başarıyla açıldı."
        except Exception as e:
            return f"VS Code açılırken hata: {e}"

    def open_browser(self):
        logger.info("Varsayılan tarayıcı açılıyor...")
        try:
            subprocess.Popen(["start", "https://www.google.com"], shell=True)
            return "Varsayılan tarayıcı açıldı."
        except Exception as e:
            return f"Tarayıcı hatası: {e}"

    def open_specific_browser(self, browser_name):
        logger.info(f"{browser_name} açılıyor...")
        try:
            # Windows'ta 'start' komutu uygulama ismiyle çalışabilir
            subprocess.Popen(["start", browser_name, "https://www.google.com"], shell=True)
            return f"{browser_name} başarıyla başlatıldı."
        except Exception as e:
            return f"{browser_name} açılırken hata oluştu: {e}"

    def run_any_app(self, app_name):
        logger.info(f"Sistemde uygulama aranıyor: {app_name}")
        try:
            # Windows 'start' komutu ile PATH üzerindeki her şeyi dener
            subprocess.Popen(f"start {app_name}", shell=True)
            return f"'{app_name}' başlatma komutu gönderildi."
        except Exception as e:
            return f"Uygulama başlatılamadı: {e}"

    def see_and_analyze(self):
        """Ekran görüntüsü alır ve NEXUS-Brain (Vision) ile analiz eder."""
        logger.info("📸 Ekran görüntüsü alınıyor...")
        screenshot_path = self.logs_dir / "current_screen.png"
        
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_path)
            
            from nexus_brain import NexusBrain
            brain = NexusBrain()
            
            # Vision analizi için Gemini 1.5 Flash kullanımı (Görüntü desteği var)
            analysis = brain.think_with_vision(
                "Şu an bilgisayar ekranında ne görüyorsun? Açık olan pencereleri ve önemli detayları Türkçe özetle.",
                str(screenshot_path)
            )
            return f"👁️ Ekran Analizi: {analysis}"
        except Exception as e:
            return f"Görüntüleme hatası: {e}"

    def download_and_install(self, target):
        """Winget veya Pip kullanarak uygulama/paket indirir ve kurar."""
        logger.info(f"İndirme ve kurulum talebi: {target}")
        
        # 1. Python paketi mi?
        if any(pkg in target for pkg in ["python", "pip", "library", "kütüphane", "modül"]):
            clean_target = target.replace("python", "").replace("pip", "").replace("kütüphane", "").replace("modül", "").strip()
            try:
                subprocess.Popen(f"pip install {clean_target}", shell=True)
                return f"Python kütüphanesi kuruluyor: {clean_target}"
            except Exception as e:
                return f"Pip hatası: {e}"

        # 2. Özel Araç Setleri (ffmpeg, git vb)
        if "ffmpeg" in target.lower():
            subprocess.Popen("winget install ffmpeg --silent", shell=True)
            return "Video işleme motoru (FFmpeg) kuruluyor..."

        # 3. Genel Windows Uygulaması (Winget)
        try:
            logger.info(f"Winget üzerinden aranıyor: {target}")
            # winget install --silent komutu arka planda kurar
            process = subprocess.Popen(f"winget install {target} --silent --accept-source-agreements --accept-package-agreements", shell=True)
            return f"'{target}' kurulumu Winget üzerinden arka planda başlatıldı."
        except Exception as e:
            return f"Kurulum hatası (Winget bulunamadı mı?): {e}"

    def plan_and_execute_project(self, project_description: str):
        """Karmaşık bir görev için gerekli araçları belirler ve kurar."""
        from nexus_brain import NexusBrain
        brain = NexusBrain()
        
        planner_prompt = (
            f"Görev: '{project_description}'\n"
            "Sen bir sistem mimarısın. Bu görevi tamamlamak için hangi Windows uygulamaları veya Python kütüphaneleri kurulmalı? "
            "Sadece kurulması gereken araçların isimlerini aralarında virgül olacak şekilde liste olarak döndür. "
            "Örn: 'ffmpeg, opencv-python, moviepy, pillow'"
        )
        
        tools_list = brain.think(planner_prompt, "Sen sadece araç isimleri dönen bir robotsun.")
        if tools_list:
            tools = [t.strip() for t in tools_list.split(",")]
            results = []
            for tool in tools:
                res = self.download_and_install(tool)
                results.append(res)
            return f"Proje Planı oluşturuldu. Şu araçlar kuruluyor: {', '.join(tools)}"
        return "Proje planlanamadı."

    def type_and_enter(self, text):
        pyautogui.write(text)
        pyautogui.press('enter')

if __name__ == "__main__":
    # Test
    cc = ComputerController()
    print(cc.execute_action("Visual Studio Code aç"))
