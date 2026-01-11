#!/usr/bin/env python3
"""
NEXUS-ONE Web Navigator & Learning Agent
- Selenium-based browser automation
- Screenshot capture and visual learning
- Form interaction and navigation
- Content extraction and pattern learning
"""
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
    from PIL import Image
except Exception:
    Image = None

WORKSPACE = Path.cwd()
DATA_DIR = WORKSPACE / "nexus_data"
LOG_DIR = WORKSPACE / "nexus_logs"
SCREENSHOT_DIR = DATA_DIR / "screenshots"
LEARNING_DATA = DATA_DIR / "web_learning.json"
LOG_FILE = LOG_DIR / "web_navigator.log"

def log(msg: str):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{ts}] {msg}\n"
    try:
        LOG_DIR.mkdir(exist_ok=True)
        with LOG_FILE.open('a', encoding='utf-8') as f:
            f.write(line)
    except Exception:
        pass
    print(line.strip())


class WebNavigator:
    def __init__(self, headless=False):
        self.driver = None
        self.headless = headless
        self.learning_data = self.load_learning_data()
        SCREENSHOT_DIR.mkdir(exist_ok=True, parents=True)
        log("web_navigator_init")
    
    def load_learning_data(self):
        try:
            if LEARNING_DATA.exists():
                return json.loads(LEARNING_DATA.read_text(encoding='utf-8'))
        except Exception:
            pass
        return {"visited_urls": [], "learned_patterns": [], "interests": [], "code_snippets": []}
    
    def save_learning_data(self):
        try:
            LEARNING_DATA.write_text(json.dumps(self.learning_data, indent=2), encoding='utf-8')
        except Exception as e:
            log(f"save_learning_error: {e}")
    
    def start_browser(self):
        """Tarayıcıyı başlat - advanced options"""
        try:
            options = Options()
            if self.headless:
                options.add_argument('--headless')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            self.driver = webdriver.Chrome(options=options)
            self.driver.maximize_window()
            log("browser_started")
            return True
        except Exception as e:
            log(f"browser_start_error: {e}")
            return False
    
    def navigate_to(self, url):
        """Belirtilen URL'ye git ve öğren"""
        if not self.driver:
            if not self.start_browser():
                return "❌ Tarayıcı başlatılamadı"
        
        try:
            self.driver.get(url)
            log(f"navigate url={url}")
            self.learning_data["visited_urls"].append({"url": url, "time": datetime.now().isoformat()})
            self.save_learning_data()
            time.sleep(2)
            return f"🌐 {url} yüklendi"
        except Exception as e:
            log(f"navigate_error url={url} err={e}")
            return f"❌ Hata: {e}"
    
    def take_screenshot(self, name: str = None) -> Path | None:
        """Take screenshot and save"""
        if not self.driver:
            return None
        try:
            if not name:
                name = f"screen_{int(time.time())}.png"
            path = SCREENSHOT_DIR / name
            self.driver.save_screenshot(str(path))
            log(f"screenshot saved={path.name}")
            return path
        except Exception as e:
            log(f"screenshot_error: {e}")
            return None
    
    def extract_text(self) -> str:
        """Extract visible text from page"""
        if not self.driver:
            return ""
        try:
            text = self.driver.find_element(By.TAG_NAME, "body").text
            return text[:10000]  # Limit to 10k chars
        except Exception:
            return ""
    
    def find_links(self) -> list[str]:
        """Extract all links from page"""
        if not self.driver:
            return []
        try:
            links = self.driver.find_elements(By.TAG_NAME, "a")
            return [link.get_attribute("href") for link in links if link.get_attribute("href")][:100]
        except Exception:
            return []
    
    def search_google(self, query):
        """Google'da arama yap"""
        self.navigate_to("https://www.google.com")
        
        if not self.driver:
            return {"error": "Tarayıcı başlatılamadı"}

        search_box = self.driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        
        time.sleep(2)  # Sayfanın yüklenmesini bekle
        
        # Sonuçları al
        results = self.driver.find_elements(By.CSS_SELECTOR, "h3")
        top_results = [r.text for r in results[:5] if r.text]
        
        return {
            "query": query,
            "top_results": top_results,
            "result_count": len(results)
        }
    
    def scrape_github_trending(self):
        """GitHub trending'den veri çek"""
        self.navigate_to("https://github.com/trending")

        if not self.driver:
            return [] # Hata durumunda boş liste döndür
        
        repos = []
        
        # Repo isimlerini bul
        repo_elements = self.driver.find_elements(By.CSS_SELECTOR, "h2 a")
        for element in repo_elements[:10]:
            repo_name = element.text.strip()
            repo_url = element.get_attribute("href")
            
            if repo_name and repo_url:
                repos.append({
                    "name": repo_name,
                    "url": repo_url,
                    "description": self.get_repo_description(element)
                })
        
        return repos
    
    def get_repo_description(self, element):
        """Repo açıklamasını al"""
        try:
            # Açıklama elementi bul
            parent = element.find_element(By.XPATH, "../..")
            desc_element = parent.find_element(By.CSS_SELECTOR, "p")
            return desc_element.text.strip()
        except:
            return "Açıklama bulunamadı"
    
    def close(self):
        """Tarayıcıyı kapat"""
        if self.driver:
            self.driver.quit()
            self.driver = None
        return "✅ Tarayıcı kapatıldı"
