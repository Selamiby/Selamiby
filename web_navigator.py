# web_navigator.py
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class WebNavigator:
    def __init__(self):
        self.driver = None
        print("🌐 AI WEB TARAYICI HAZIR")
    
    def start_browser(self):
        """Tarayıcıyı başlat"""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Görünmez mod
        options.add_argument('--no-sandbox')
        
        self.driver = webdriver.Chrome(options=options)
        return "✅ Tarayıcı başlatıldı"
    
    def navigate_to(self, url):
        """Belirtilen URL'ye git"""
        if not self.driver:
            self.start_browser()
        
        if self.driver:
            self.driver.get(url)
            return f"🌐 {url} yüklendi"
        return "❌ Tarayıcı başlatılamadı"
    
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
