#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 NEXUS GITHUB TRENDING LEARNER
GitHub trending'den otomatik öğrenme
"""

import json
import logging
from datetime import datetime
from pathlib import Path

import requests

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')
logger = logging.getLogger(__name__)

class GitHubTrendingLearner:
    def __init__(self):
        self.knowledge_base = Path("github_trending_knowledge")
        self.knowledge_base.mkdir(exist_ok=True)
        self.learned_repos = []
    
    def fetch_trending(self):
        """GitHub trending repos al"""
        try:
            url = "https://api.github.com/search/repositories"
            params = {
                "q": "stars:>1000 created:>2025-01-01",
                "sort": "stars",
                "order": "desc",
                "per_page": 10
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                repos = response.json().get('items', [])
                logger.info(f"📊 {len(repos)} trending repo bulundu")
                return repos
            else:
                logger.warning(f"⚠️ GitHub API: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"❌ Fetch error: {e}")
            return []
    
    def learn_from_repo(self, repo):
        """Repo'dan öğren"""
        try:
            knowledge = {
                "name": repo['name'],
                "full_name": repo['full_name'],
                "description": repo.get('description', 'No description'),
                "stars": repo['stargazers_count'],
                "language": repo.get('language', 'Unknown'),
                "topics": repo.get('topics', []),
                "url": repo['html_url'],
                "learned_at": datetime.now().isoformat()
            }
            
            # Save knowledge
            file_name = f"{repo['name'].replace('/', '_')}.json"
            file_path = self.knowledge_base / file_name
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(knowledge, f, indent=2, ensure_ascii=False)
            
            self.learned_repos.append(repo['name'])
            logger.info(f"✅ Learned: {repo['name']} ({repo['stargazers_count']} ⭐)")
            
        except Exception as e:
            logger.error(f"❌ Learn error: {e}")
    
    def run(self):
        """Ana öğrenme döngüsü"""
        logger.info("🔥 GITHUB TRENDING LEARNER BAŞLADI")
        
        repos = self.fetch_trending()
        
        for repo in repos[:10]:
            self.learn_from_repo(repo)
        
        logger.info(f"✅ {len(self.learned_repos)} repo öğrenildi")
        logger.info(f"💾 Bilgiler: {self.knowledge_base}/")

if __name__ == "__main__":
    learner = GitHubTrendingLearner()
    learner.run()
