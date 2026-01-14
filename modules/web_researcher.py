"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:16
🚀 Status: ACTIVE / PRODUCTION
"""

"""
Otonom Web Araştırmacı - Akıllı İnternet Araştırma Ajanı
"""

import asyncio
import json
import re
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin, urlparse

import aiohttp
import requests
from bs4 import BeautifulSoup


@dataclass
class ResearchResult:
    """Araştırma sonucu"""

    query: str
    source: str
    title: str
    content: str
    url: str
    timestamp: datetime
    confidence: float
    tags: List[str]


class WebResearcher:
    """Otonom web araştırmacısı"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            }
        )

        self.search_engines = {
            "duckduckgo": "https://duckduckgo.com/html/?q=",
            "google": "https://www.google.com/search?q=",
            "bing": "https://www.bing.com/search?q=",
            "yandex": "https://yandex.com/search/?text=",
        }

        self.research_history: List[Dict[str, Any]] = []

    def search_web(
        self, query: str, engine: str = "duckduckgo", max_results: int = 10
    ) -> List[Dict]:
        """Web'de arama yap"""
        if engine not in self.search_engines:
            engine = "duckduckgo"

        search_url = self.search_engines[engine] + requests.utils.quote(query)

        try:
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            results: List[Dict[str, Any]] = []

            # DuckDuckGo result parsing
            if engine == "duckduckgo":
                for result in soup.find_all("a", class_="result__url", href=True):
                    if len(results) >= max_results:
                        break

                    title_elem = result.find_next("a", class_="result__title")
                    snippet_elem = result.find_next("a", class_="result__snippet")

                    if title_elem and snippet_elem:
                        results.append(
                            {
                                "title": title_elem.get_text(strip=True),
                                "url": result["href"],
                                "snippet": snippet_elem.get_text(strip=True)[:200],
                                "engine": engine,
                            }
                        )

            # Google result parsing
            elif engine == "google":
                for g in soup.find_all("div", class_="tF2Cxc"):
                    if len(results) >= max_results:
                        break

                    link = g.find("a", href=True)
                    title = g.find("h3")
                    snippet = g.find("div", class_="VwiC3b")

                    if link and title:
                        results.append(
                            {
                                "title": title.get_text(strip=True),
                                "url": link["href"],
                                "snippet": (
                                    snippet.get_text(strip=True)[:200]
                                    if snippet
                                    else ""
                                ),
                                "engine": engine,
                            }
                        )

            self.research_history.append(
                {
                    "query": query,
                    "engine": engine,
                    "results_count": len(results),
                    "timestamp": datetime.now().isoformat(),
                }
            )

            return results

        except Exception as e:
            print(f"Search error: {e}")
            return []

    def fetch_page_content(self, url: str, timeout: int = 10) -> Optional[Dict]:
        """Sayfa içeriğini getir"""
        try:
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            title = soup.title.string if soup.title else ""
            meta_desc = soup.find("meta", attrs={"name": "description"})
            description = meta_desc["content"] if meta_desc else ""

            content_tags = [
                "article",
                "main",
                "div#content",
                "div.content",
                "div.post-content",
            ]
            content = ""

            for tag in content_tags:
                if "#" in tag:
                    tag_name, tag_id = tag.split("#")
                    element = soup.find(tag_name, id=tag_id)
                elif "." in tag:
                    tag_name, tag_class = tag.split(".")
                    element = soup.find(tag_name, class_=tag_class)
                else:
                    element = soup.find(tag)

                if element:
                    content = element.get_text(strip=True)[:5000]
                    break

            if not content:
                paragraphs = soup.find_all("p")
                content = " ".join([p.get_text(strip=True) for p in paragraphs[:10]])[
                    :5000
                ]

            links = []
            for link in soup.find_all("a", href=True)[:20]:
                full_url = urljoin(url, link["href"])
                if urlparse(full_url).netloc:
                    links.append(
                        {"text": link.get_text(strip=True)[:100], "url": full_url}
                    )

            images = []
            for img in soup.find_all("img", src=True)[:10]:
                img_url = urljoin(url, img["src"])
                images.append(img_url)

            return {
                "url": url,
                "title": title[:200],
                "description": description[:500],
                "content": content,
                "word_count": len(content.split()),
                "links_count": len(links),
                "images_count": len(images),
                "links": links[:5],
                "images": images[:3],
                "timestamp": datetime.now().isoformat(),
                "status_code": response.status_code,
                "content_type": response.headers.get("content-type", ""),
            }

        except Exception as e:
            return {
                "url": url,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    async def async_fetch_multiple(self, urls: List[str]) -> List[Dict]:
        """Birden fazla URL'yi asenkron getir"""
        async with aiohttp.ClientSession() as session:
            tasks = [self._async_fetch_url(session, url) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            valid_results: List[Dict[str, Any]] = []
            for result in results:
                if isinstance(result, dict) and "error" not in result:
                    valid_results.append(result)

            return valid_results

    async def _async_fetch_url(self, session: aiohttp.ClientSession, url: str) -> Dict:
        """Asenkron URL fetch"""
        try:
            async with session.get(
                url, timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                text = await response.text()
                soup = BeautifulSoup(text, "html.parser")
                title = soup.title.string if soup.title else ""

                paragraphs = soup.find_all("p")
                content = " ".join([p.get_text(strip=True) for p in paragraphs[:5]])[
                    :1000
                ]

                return {
                    "url": url,
                    "title": title[:200],
                    "content": content,
                    "status": response.status,
                    "timestamp": datetime.now().isoformat(),
                }

        except Exception as e:
            return {
                "url": url,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def research_topic(self, topic: str, depth: int = 1) -> List[ResearchResult]:
        """Konu araştırması yap"""
        print(f"🔍 Researching: {topic}")

        search_results = self.search_web(topic, max_results=5)
        research_results: List[ResearchResult] = []
        visited_urls = set()

        for result in search_results:
            if depth > 0 and result["url"] not in visited_urls:
                visited_urls.add(result["url"])

                page_content = self.fetch_page_content(result["url"])

                if page_content and "error" not in page_content:
                    research_result = ResearchResult(
                        query=topic,
                        source=result["engine"],
                        title=result["title"],
                        content=page_content["content"][:1000],
                        url=result["url"],
                        timestamp=datetime.now(),
                        confidence=0.8,
                        tags=self._extract_tags(page_content["content"]),
                    )

                    research_results.append(research_result)

        return research_results

    def _extract_tags(self, text: str) -> List[str]:
        """Metinden tag'ları çıkar"""
        words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
        from collections import Counter

        word_freq = Counter(words)
        common_words = [word for word, count in word_freq.most_common(10)]
        return common_words[:5]

    def get_news(self, category: str = "technology", country: str = "tr") -> List[Dict]:
        """Haber getir (demo NewsAPI anahtarı ile)"""
        news_url = f"https://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey=demo"

        try:
            response = self.session.get(news_url, timeout=10)
            data = response.json()

            if data.get("status") == "ok":
                articles = data.get("articles", [])
                results = []
                for art in articles[:20]:
                    results.append(
                        {
                            "title": art.get("title", ""),
                            "description": art.get("description", ""),
                            "url": art.get("url", ""),
                            "published_at": art.get("publishedAt", ""),
                            "source": (art.get("source") or {}).get("name", ""),
                        }
                    )
                return results
            return []

        except Exception as e:
            print(f"News fetch error: {e}")
            return []


if __name__ == "__main__":
    researcher = WebResearcher()
    sample = researcher.search_web("latest AI research", max_results=3)
    print(json.dumps(sample, indent=2, ensure_ascii=False))
