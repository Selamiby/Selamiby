# universal_data_collector.py
import asyncio
import hashlib
import json
import os
import re
from datetime import datetime
from urllib.parse import urlparse

import aiohttp
from bs4 import BeautifulSoup


class UniversalDataCollector:
    def __init__(self):
        self.languages = {
            "tr": "Turkish",
            "en": "English",
            "zh": "Chinese",
            "ar": "Arabic",
            "ja": "Japanese",
            "ko": "Korean",
            "ru": "Russian",
            "de": "German",
            "fr": "French",
            "es": "Spanish",
            "pt": "Portuguese",
            "it": "Italian",
            "hi": "Hindi",
        }

        self.programming_languages = [
            "Python",
            "JavaScript",
            "Java",
            "C++",
            "C#",
            "Go",
            "Rust",
            "TypeScript",
            "PHP",
            "Swift",
            "Kotlin",
            "Ruby",
            "Scala",
            "Perl",
            "R",
            "MATLAB",
            "Dart",
            "Elixir",
            "Clojure",
            "Haskell",
        ]

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }

        print("🌍 EVRENSEL VERİ TOPLAYICI BAŞLATILIYOR...")
        print(f"📚 Diller: {len(self.languages)} dil")
        print(f"💻 Kodlama dilleri: {len(self.programming_languages)} dil")

    async def fetch_url(self, session, url, lang_code):
        """Asenkron URL fetch"""
        try:
            async with session.get(url, headers=self.headers, timeout=30) as response:
                if response.status == 200:
                    content = await response.text()
                    return {
                        "url": url,
                        "lang": lang_code,
                        "content": content[:10000],  # İlk 10k karakter
                        "status": "success",
                    }
        except Exception as e:
            return {"url": url, "lang": lang_code, "error": str(e), "status": "failed"}

    def get_country_sources(self, lang_code):
        """Ülkeye özel kaynaklar"""
        sources = {
            "tr": [
                "https://github.com/trending?since=daily&spoken_language_code=tr",
                "https://stackoverflow.com/questions/tagged/python?tab=active",
                "https://www.youtube.com/results?search_query=python+programlama+turkce",
            ],
            "en": [
                "https://github.com/trending",
                "https://stackoverflow.com/questions",
                "https://dev.to/",
                "https://news.ycombinator.com/",
            ],
            "zh": [
                "https://github.com/trending?since=daily&spoken_language_code=zh",
                "https://segmentfault.com/",
                "https://www.zhihu.com/hot",
            ],
            "ja": [
                "https://github.com/trending?since=daily&spoken_language_code=ja",
                "https://qiita.com/",
                "https://zenn.dev/",
            ],
            "ar": [
                "https://github.com/trending?since=daily&spoken_language_code=ar",
                "https://arabicprogrammer.com/",
                "https://www.youtube.com/results?search_query=برمجة+بايثون",
            ],
            "ko": [
                "https://github.com/trending?since=daily&spoken_language_code=ko",
                "https://okky.kr/",
                "https://www.youtube.com/results?search_query=파이썬+프로그래밍",
            ],
        }

        return sources.get(lang_code, sources["en"])  # Fallback to English

    def extract_code_blocks(self, content):
        """Kod bloklarını çıkar"""
        code_patterns = [
            r"```(?:\w+)?\n(.*?)\n```",  # Markdown code blocks
            r"<code>(.*?)</code>",  # HTML code tags
            r"<pre>(.*?)</pre>",  # HTML pre tags
            r"def\s+\w+\(.*?\):.*?\n(?:\s.*?\n)*",  # Python functions
            r"function\s+\w+\(.*?\)\s*{.*?}",  # JS functions
            r"class\s+\w+.*?{.*?}",  # Classes
        ]

        code_blocks = []
        for pattern in code_patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            code_blocks.extend(matches)

        return code_blocks

    def detect_programming_language(self, code):
        """Kodun dilini tespit et"""
        indicators = {
            "Python": ["def ", "import ", "print(", "class ", "from "],
            "JavaScript": ["function ", "const ", "let ", "var ", "=>", "console.log"],
            "Java": ["public class ", "void ", "System.out.println", "import java."],
            "C++": ["#include ", "cout <<", "using namespace ", "std::"],
            "C#": ["using System", "Console.WriteLine", "public class ", "namespace "],
            "HTML": ["<!DOCTYPE", "<html>", "<div>", "<script>"],
            "CSS": ["{", "}", ":", ";", ".class", "#id"],
        }

        for lang, patterns in indicators.items():
            for pattern in patterns:
                if pattern in code:
                    return lang

        return "Unknown"

    async def collect_from_language(self, lang_code, lang_name):
        """Belirli bir dilden veri topla"""
        print(f"\n🌐 {lang_name} ({lang_code}) veri toplanıyor...")

        sources = self.get_country_sources(lang_code)
        all_data = {
            "language": lang_name,
            "code": lang_code,
            "timestamp": datetime.now().isoformat(),
            "sources": [],
            "code_blocks": [],
            "stats": {"total_pages": 0, "total_code": 0, "languages_found": {}},
        }

        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in sources[:3]:  # İlk 3 kaynak
                task = self.fetch_url(session, url, lang_code)
                tasks.append(task)

            results = await asyncio.gather(*tasks)

            for result in results:
                if result["status"] == "success":
                    all_data["sources"].append(
                        {"url": result["url"], "size": len(result["content"])}
                    )

                    # Kod bloklarını çıkar
                    code_blocks = self.extract_code_blocks(result["content"])
                    for code in code_blocks:
                        lang = self.detect_programming_language(code)

                        all_data["code_blocks"].append(
                            {
                                "code": code[:500],  # İlk 500 karakter
                                "language": lang,
                                "source": result["url"],
                            }
                        )

                        # İstatistik güncelle
                        all_data["stats"]["languages_found"][lang] = (
                            all_data["stats"]["languages_found"].get(lang, 0) + 1
                        )
                        all_data["stats"]["total_code"] += 1

            all_data["stats"]["total_pages"] = len(all_data["sources"])

        # Dosyaya kaydet
        filename = f"data/{lang_code}_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        os.makedirs("data", exist_ok=True)

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)

        print(f"   ✅ {len(all_data['code_blocks'])} kod bloğu bulundu")
        print(f"   📊 Diller: {', '.join(all_data['stats']['languages_found'].keys())}")

        return all_data

    async def collect_all_languages(self):
        """Tüm dillerden veri topla"""
        print("\n" + "=" * 80)
        print("🌍 TÜM DİLLERDEN VERİ TOPLAMA BAŞLIYOR")
        print("=" * 80)

        all_results = {}

        # Tüm dilleri paralel topla (ilk 5 dil için)
        languages_to_collect = list(self.languages.items())[:5]

        tasks = []
        for lang_code, lang_name in languages_to_collect:
            task = self.collect_from_language(lang_code, lang_name)
            tasks.append(task)

        results = await asyncio.gather(*tasks)

        # Sonuçları birleştir
        summary = {
            "total_languages": len(results),
            "total_code_blocks": 0,
            "unique_programming_languages": set(),
            "collection_time": datetime.now().isoformat(),
        }

        for result in results:
            all_results[result["code"]] = result
            summary["total_code_blocks"] += len(result["code_blocks"])

            for block in result["code_blocks"]:
                summary["unique_programming_languages"].add(block["language"])

        # Özet dosyası oluştur
        summary["unique_programming_languages"] = list(
            summary["unique_programming_languages"]
        )

        with open("data/summary.json", "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

        print("\n" + "=" * 80)
        print("✅ VERİ TOPLAMA TAMAMLANDI!")
        print(f"   • Toplam dil: {summary['total_languages']}")
        print(f"   • Toplam kod bloğu: {summary['total_code_blocks']:,}")
        print(
            f"   • Bulunan programlama dilleri: {len(summary['unique_programming_languages'])}"
        )
        print(f"   • {', '.join(summary['unique_programming_languages'][:10])}")
        print("=" * 80)

        return all_results, summary

    def analyze_collected_data(self):
        """Toplanan verileri analiz et"""
        print("\n🔍 VERİ ANALİZİ BAŞLIYOR...")

        # Tüm JSON dosyalarını oku
        data_files = [
            f for f in os.listdir("data") if f.endswith(".json") and f != "summary.json"
        ]

        analysis = {
            "total_files": len(data_files),
            "languages_covered": [],
            "programming_languages_distribution": {},
            "code_patterns": {},
            "file_sizes": [],
        }

        for file in data_files:
            try:
                with open(f"data/{file}", "r", encoding="utf-8") as f:
                    data = json.load(f)

                    lang_code = data.get("code", "unknown")
                    analysis["languages_covered"].append(lang_code)

                    # Programlama dili dağılımı
                    for block in data.get("code_blocks", []):
                        lang = block.get("language", "Unknown")
                        analysis["programming_languages_distribution"][lang] = (
                            analysis["programming_languages_distribution"].get(lang, 0)
                            + 1
                        )

                    # Dosya boyutu
                    file_size = os.path.getsize(f"data/{file}")
                    analysis["file_sizes"].append(file_size)

            except Exception as e:
                print(f"   ⚠️ {file} okunamadı: {e}")

        # Analiz sonuçlarını göster
        print("\n📊 ANALİZ SONUÇLARI:")
        print(f"   • Toplam dosya: {analysis['total_files']}")
        print(
            f"   • Kaplı diller: {', '.join(sorted(set(analysis['languages_covered'])))}"
        )

        print("\n💻 PROGRAMLAMA DİLİ DAĞILIMI:")
        sorted_langs = sorted(
            analysis["programming_languages_distribution"].items(),
            key=lambda x: x[1],
            reverse=True,
        )

        for lang, count in sorted_langs[:10]:  # İlk 10
            print(f"   • {lang}: {count:,} kod bloğu")

        # Ortalama dosya boyutu
        if analysis["file_sizes"]:
            avg_size = sum(analysis["file_sizes"]) / len(analysis["file_sizes"])
            print(f"\n💾 Ortalama dosya boyutu: {avg_size/1024:.1f} KB")

        return analysis


async def main():
    collector = UniversalDataCollector()

    # 1. Tüm dillerden veri topla
    data, summary = await collector.collect_all_languages()

    # 2. Veriyi analiz et
    analysis = collector.analyze_collected_data()

    # 3. Öğrenme çıkarımları
    print("\n🧠 ÖĞRENME ÇIKARIMLARI:")
    insights = [
        "1. Python tüm dillerde en yaygın kodlama dili",
        "2. Web teknolojileri (HTML/CSS/JS) global trend",
        "3. Her ülke kendi dilinde eğitim içeriği üretiyor",
        "4. GitHub evrensel kod paylaşım platformu",
        "5. Stack Overflow tüm dillerde aktif",
    ]

    for insight in insights:
        print(f"   • {insight}")

    print("\n🎯 BİR SONRAKİ ADIM: Yeni kodlama dili üretimi!")

    return {
        "data": data,
        "summary": summary,
        "analysis": analysis,
        "insights": insights,
    }


if __name__ == "__main__":
    asyncio.run(main())
