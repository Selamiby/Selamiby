import asyncio
"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:15
🚀 Status: ACTIVE / PRODUCTION
"""

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
import random
import sys
import time
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import nexus_multimodal as mm
from nexus_learning_tracker import record_event

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
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}\n"
    try:
        LOG_DIR.mkdir(exist_ok=True)
        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass
    print(line.strip())


class WebNavigator:
    def __init__(self, headless=False, use_profile=False):
        self.driver = None
        self.headless = headless
        self.use_profile = use_profile
        self.learning_data = self.load_learning_data()
        SCREENSHOT_DIR.mkdir(exist_ok=True, parents=True)
        log(f"web_navigator_init headless={headless} use_profile={use_profile}")

    def load_learning_data(self):
        try:
            if LEARNING_DATA.exists():
                return json.loads(LEARNING_DATA.read_text(encoding="utf-8"))
        except Exception:
            pass
        return {
            "visited_urls": [],
            "learned_patterns": [],
            "interests": [],
            "code_snippets": [],
        }

    def save_learning_data(self):
        try:
            LEARNING_DATA.write_text(
                json.dumps(self.learning_data, indent=2), encoding="utf-8"
            )
        except Exception as e:
            log(f"save_learning_error: {e}")

    def start_browser(self):
        """Tarayıcıyı başlat - advanced options"""
        try:
            options = Options()
            if self.headless:
                options.add_argument("--headless")
            
            # Anti-detection & Efficiency
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-software-rasterizer")
            options.add_argument("--remote-debugging-port=9222")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)
            
            # User Agent for Human Look
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

            # Persistent Profile Support
            if self.use_profile:
                # Use a dedicated profile in the workspace to avoid locking issues with personal Chrome
                nexus_profile_path = WORKSPACE / "nexus_chrome_profile"
                nexus_profile_path.mkdir(exist_ok=True)
                options.add_argument(f"user-data-dir={nexus_profile_path.absolute()}")
                log(f"using_nexus_profile={nexus_profile_path}")

            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager
            
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            
            # Remove automation flag
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            log("browser_started_successfully")
            return True
        except Exception as e:
            log(f"browser_start_error: {e}")
            self.driver = None
            return False

    def human_click(self, element):
        """ActionChains ile rastgele ofsetli ve insansı tıklama"""
        try:
            from selenium.webdriver.common.action_chains import ActionChains
            actions = ActionChains(self.driver)
            
            # Rastgele ofset (merkezden +-3px)
            off_x = random.randint(-3, 3)
            off_y = random.randint(-3, 3)
            
            actions.move_to_element_with_offset(element, off_x, off_y)
            actions.pause(random.uniform(0.1, 0.3))
            actions.click()
            actions.perform()
            log(f"human_click offset=({off_x},{off_y})")
        except Exception as e:
            log(f"human_click_error: {e}")
            element.click() # Fallback

    def human_type(self, element, text):
        """Harf harf, rastgele hızda yazma"""
        try:
            for char in text:
                element.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            log(f"human_typed text_len={len(text)}")
        except Exception as e:
            log(f"human_type_error: {e}")
            element.send_keys(text) # Fallback

    def human_scroll_to(self, element):
        """Yavaşça öğeye kaydır"""
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(random.uniform(1, 2))
        except Exception:
            pass

    def navigate_to(self, url):
        """Güvenli ve insansı şekilde bir URL'ye gider"""
        if not self.driver: return
        log(f"navigating_to: {url}")
        try:
            self.driver.get(url)
            time.sleep(random.uniform(2, 4)) # Sayfanın yüklenmesini bekle
        except Exception as e:
            log(f"navigation_error: {e}")

    def take_screenshot(self, filename="last_frame.png"):
        """Ekranda o an ne varsa yakalar - Vision için"""
        if not self.driver: return
        try:
            path = Path(filename)
            path.parent.mkdir(exist_ok=True, parents=True)
            self.driver.save_screenshot(str(path))
            log(f"screenshot_saved: {filename}")
        except Exception as e:
            log(f"screenshot_error: {e}")

    def human_type(self, element, text):
        """İnsansı yazma hareketi - Değişken hız ve rastgele duraklamalar"""
        for char in text:
            element.send_keys(char)
            # Rastgele yazı hızı (bazı harflerde daha hızlı, bazılarında yavaş)
            time.sleep(random.uniform(0.02, 0.15))
            if random.random() < 0.1: # %10 ihtimalle kısa bir düşünme molası
                time.sleep(random.uniform(0.3, 0.8))

    def human_click(self, element):
        """İnsansı tıklama - Önce üzerine gel, bekle, sonra rastgele koordinata tıkla"""
        try:
            from selenium.webdriver.common.action_chains import ActionChains
            actions = ActionChains(self.driver)
            
            # Elementin üzerine yumuşak geçiş simülasyonu
            actions.move_to_element(element).perform()
            time.sleep(random.uniform(0.2, 0.6))
            
            # Tam merkeze değil, rastgele bir piksel ofsetiyle tıkla (fiziksel gerçeklik)
            actions.move_to_element_with_offset(element, random.randint(-5, 5), random.randint(-5, 5)).click().perform()
            log("human_click_performed")
        except Exception as e:
            log(f"click_error: {e}")
            element.click()

    def human_scroll_to(self, element):
        """Elemente yumuşak bir şekilde kaydırarak odaklan"""
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        time.sleep(random.uniform(0.8, 1.5))
        """Belirtilen URL'ye git ve öğren"""
        if not self.driver:
            if not self.start_browser():
                return "❌ Tarayıcı başlatılamadı"

        try:
            self.driver.get(url)
            log(f"navigate url={url}")
            self.learning_data["visited_urls"].append(
                {"url": url, "time": datetime.now().isoformat()}
            )
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
            # Optional vision analysis + tracking
            try:
                info = mm.analyze_image(path)
                if info.get("ok"):
                    record_event(source="vision", vision_events=1)
                    log(
                        f"vision_analysis size={info.get('size')} ocr_len={len(info.get('ocr_text',''))}"
                    )
            except Exception:
                pass
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
            return [
                link.get_attribute("href")
                for link in links
                if link.get_attribute("href")
            ][:100]
        except Exception:
            return []

    def search_google(self, query):
        """Google'da arama yap ve öğren"""
        self.navigate_to("https://www.google.com")

        if not self.driver:
            return {"error": "Tarayıcı başlatılamadı"}

        try:
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            time.sleep(2)

            # Screenshot results
            self.take_screenshot(f"search_{query.replace(' ', '_')[:30]}.png")

            # Extract results
            results = self.driver.find_elements(By.CSS_SELECTOR, "h3")
            top_results = [r.text for r in results[:10] if r.text]

            # Learn from search
            self.learning_data["learned_patterns"].append(
                {
                    "type": "search",
                    "query": query,
                    "results_count": len(top_results),
                    "time": datetime.now().isoformat(),
                }
            )
            self.save_learning_data()
            try:
                record_event(source="web_search", web_sessions=1)
            except Exception:
                pass

            log(f"search_complete query={query} results={len(top_results)}")
            return {
                "query": query,
                "top_results": top_results,
                "result_count": len(results),
            }
        except Exception as e:
            log(f"search_error: {e}")
            return {"error": str(e)}

    def learn_from_youtube(self, video_url: str, duration_sec: int = 30):
        """YouTube videosunu izle ve öğren"""
        self.navigate_to(video_url)

        if not self.driver:
            return {"error": "Tarayıcı başlatılamadı"}

        try:
            log(f"youtube_learning duration={duration_sec}s url={video_url}")
            start = time.time()
            screenshots = []

            # Capture frames periodically
            while time.time() - start < duration_sec:
                path = self.take_screenshot(f"yt_{int(time.time())}.png")
                if path:
                    screenshots.append(str(path.name))
                time.sleep(5)

            # Extract title and description
            title = ""
            try:
                title_el = self.driver.find_element(
                    By.CSS_SELECTOR, "h1.ytd-video-primary-info-renderer"
                )
                title = title_el.text
            except Exception:
                pass

            self.learning_data["learned_patterns"].append(
                {
                    "type": "youtube",
                    "url": video_url,
                    "title": title,
                    "duration": duration_sec,
                    "screenshots": len(screenshots),
                    "time": datetime.now().isoformat(),
                }
            )
            self.save_learning_data()
            try:
                record_event(
                    source="web_youtube", web_sessions=1, vision_events=len(screenshots)
                )
            except Exception:
                pass

            log(f"youtube_learning_complete screenshots={len(screenshots)}")
            return {
                "title": title,
                "screenshots": len(screenshots),
                "duration": duration_sec,
            }
        except Exception as e:
            log(f"youtube_error: {e}")
            return {"error": str(e)}

    def learn_from_code_repo(self, repo_url: str):
        """GitHub repo'dan kod öğren"""
        self.navigate_to(repo_url)

        if not self.driver:
            return {"error": "Tarayıcı başlatılamadı"}

        try:
            # Get repo name
            repo_name = ""
            try:
                repo_name = self.driver.find_element(
                    By.CSS_SELECTOR, "[itemprop='name']"
                ).text
            except Exception:
                pass

            # Find code files
            time.sleep(2)
            code_links = []
            try:
                file_elements = self.driver.find_elements(
                    By.CSS_SELECTOR, "a.Link--primary"
                )
                for el in file_elements[:20]:
                    href = el.get_attribute("href")
                    if href and (".py" in href or ".js" in href or ".ts" in href):
                        code_links.append(href)
            except Exception:
                pass

            self.learning_data["code_snippets"].append(
                {
                    "repo": repo_url,
                    "repo_name": repo_name,
                    "files_found": len(code_links),
                    "time": datetime.now().isoformat(),
                }
            )
            self.save_learning_data()
            try:
                record_event(source="web_repo", web_sessions=1)
            except Exception:
                pass

            log(f"code_learning repo={repo_name} files={len(code_links)}")
            return {
                "repo_name": repo_name,
                "code_files": len(code_links),
                "sample_files": code_links[:5],
            }
        except Exception as e:
            log(f"code_learning_error: {e}")
            return {"error": str(e)}

    def scrape_github_trending(self):
        """GitHub trending'den veri çek ve öğren"""
        self.navigate_to("https://github.com/trending")

        if not self.driver:
            return []

        repos = []
        try:
            repo_elements = self.driver.find_elements(By.CSS_SELECTOR, "h2 a")
            for element in repo_elements[:10]:
                repo_name = element.text.strip()
                repo_url = element.get_attribute("href")

                if repo_name and repo_url:
                    repos.append({"name": repo_name, "url": repo_url})

            log(f"github_trending_scraped repos={len(repos)}")
            return repos
        except Exception as e:
            log(f"github_trending_error: {e}")
            return []

    def close(self):
        """Close browser"""
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
                log("browser_closed")
            except Exception:
                pass


def demo_web_learning():
    """Demo: Search, navigate, learn"""
    nav = WebNavigator(headless=False)
    try:
        # Search for programming tutorials
        nav.search_google("Python machine learning tutorial")
        time.sleep(3)

        # Navigate to Python docs
        nav.navigate_to("https://docs.python.org/3/tutorial/")
        nav.take_screenshot("python_docs.png")

        log("demo_complete")
    finally:
        nav.close()


if __name__ == "__main__":
    demo_web_learning()
