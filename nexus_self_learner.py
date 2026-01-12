"""
NEXUS-ONE Self-Learning Engine
--------------------------------
Autonomous learning system that:
- Watches workspace for new code/commands
- Learns patterns and techniques
- Expands knowledge graph
- Self-updates command tree
- Runs 24/7 in background

Learning Sources:
- Local Python files (AST analysis)
- GitHub repos (web_navigator)
- YouTube tutorials (video learning)
- Online documentation
- User interactions (chat logs)
"""

import ast
import hashlib
import json
import logging
import os
import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import nexus_multimodal as mm

# Setup
WORKSPACE = Path(__file__).parent
DATA_DIR = WORKSPACE / "nexus_data"
KNOWLEDGE_DIR = DATA_DIR / "knowledge_graph"
KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)

LOG_DIR = WORKSPACE / "nexus_logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "self_learner.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("SelfLearner")

# Try to import AI modules
try:
    from code_generator import CodeGenerator
    CODE_GEN_AVAILABLE = True
except ImportError:
    CODE_GEN_AVAILABLE = False
    logger.warning("CodeGenerator not available")

try:
    from web_navigator import WebNavigator
    from nexus_learning_tracker import record_event
    WEB_NAV_AVAILABLE = True
except ImportError:
    WEB_NAV_AVAILABLE = False
    logger.warning("WebNavigator not available")


class KnowledgeGraph:
    """
    Knowledge graph for storing and relating learned information.
    Stores: concepts, commands, code patterns, relationships
    """
    
    def __init__(self):
        self.graph_file = KNOWLEDGE_DIR / "knowledge_graph.json"
        self.graph = self.load_graph()
        
    def load_graph(self) -> Dict:
        """Load knowledge graph from disk"""
        if self.graph_file.exists():
            try:
                return json.loads(self.graph_file.read_text(encoding='utf-8'))
            except Exception as e:
                logger.error(f"Failed to load knowledge graph: {e}")
        
        # Default structure
        return {
            "concepts": {},  # {concept_name: {description, examples, related, learned_at}}
            "commands": {},  # {command_name: {syntax, description, examples, category}}
            "code_patterns": {},  # {pattern_id: {code, description, use_cases, frequency}}
            "relationships": [],  # [{from, to, type, strength}]
            "statistics": {
                "total_concepts": 0,
                "total_commands": 0,
                "total_patterns": 0,
                "last_updated": None,
                "learning_sessions": 0
            }
        }
    
    def save_graph(self):
        """Persist knowledge graph to disk"""
        self.graph["statistics"]["last_updated"] = datetime.now().isoformat()
        self.graph_file.write_text(json.dumps(self.graph, indent=2, ensure_ascii=False), encoding='utf-8')
        logger.info(f"Knowledge graph saved: {self.graph['statistics']['total_concepts']} concepts, "
                   f"{self.graph['statistics']['total_commands']} commands")

        # Mirror stats to global tracker
        try:
            record_event(
                source="self_learner",
                concepts_learned=self.graph["statistics"].get("total_concepts", 0),
                commands_learned=self.graph["statistics"].get("total_commands", 0),
                patterns_learned=self.graph["statistics"].get("total_patterns", 0),
            )
        except Exception:
            pass
    
    def add_concept(self, name: str, description: str, examples: List[str] = None, related: List[str] = None):
        """Add or update a concept"""
        if name not in self.graph["concepts"]:
            self.graph["statistics"]["total_concepts"] += 1
        
        self.graph["concepts"][name] = {
            "description": description,
            "examples": examples or [],
            "related": related or [],
            "learned_at": datetime.now().isoformat(),
            "importance": 1.0
        }
        logger.info(f"Learned concept: {name}")
    
    def add_command(self, name: str, syntax: str, description: str, category: str = "general", 
                   examples: List[str] = None):
        """Add or update a command"""
        if name not in self.graph["commands"]:
            self.graph["statistics"]["total_commands"] += 1
        
        self.graph["commands"][name] = {
            "syntax": syntax,
            "description": description,
            "category": category,
            "examples": examples or [],
            "usage_count": self.graph["commands"].get(name, {}).get("usage_count", 0),
            "learned_at": datetime.now().isoformat()
        }
        logger.info(f"Learned command: {name} ({category})")
    
    def add_pattern(self, code: str, description: str, use_cases: List[str] = None) -> str:
        """Add code pattern and return pattern ID"""
        pattern_id = hashlib.md5(code.encode()).hexdigest()[:12]
        
        if pattern_id not in self.graph["code_patterns"]:
            self.graph["statistics"]["total_patterns"] += 1
            self.graph["code_patterns"][pattern_id] = {
                "code": code,
                "description": description,
                "use_cases": use_cases or [],
                "frequency": 1,
                "learned_at": datetime.now().isoformat()
            }
        else:
            self.graph["code_patterns"][pattern_id]["frequency"] += 1
        
        logger.info(f"Learned pattern: {pattern_id} (freq: {self.graph['code_patterns'][pattern_id]['frequency']})")
        return pattern_id
    
    def add_relationship(self, from_entity: str, to_entity: str, rel_type: str, strength: float = 1.0):
        """Add relationship between entities"""
        rel = {
            "from": from_entity,
            "to": to_entity,
            "type": rel_type,
            "strength": strength
        }
        
        # Avoid duplicates
        existing = next((r for r in self.graph["relationships"] 
                        if r["from"] == from_entity and r["to"] == to_entity and r["type"] == rel_type), None)
        
        if existing:
            existing["strength"] = min(10.0, existing["strength"] + 0.5)  # Increase strength
        else:
            self.graph["relationships"].append(rel)
    
    def get_related_concepts(self, concept: str, max_depth: int = 2) -> List[str]:
        """Get related concepts using BFS"""
        if concept not in self.graph["concepts"]:
            return []
        
        visited = set()
        queue = [(concept, 0)]
        related = []
        
        while queue:
            current, depth = queue.pop(0)
            if current in visited or depth > max_depth:
                continue
            
            visited.add(current)
            if current != concept:
                related.append(current)
            
            # Add direct relationships
            for rel in self.graph["relationships"]:
                if rel["from"] == current and rel["to"] not in visited:
                    queue.append((rel["to"], depth + 1))
        
        return related[:20]  # Limit results


    def analyze_audio_file(self, audio_path: Path) -> Dict[str, Any]:
        """Optional audio analysis using speech_recognition if available."""
        info = mm.transcribe_audio(audio_path)
        if info.get("ok"):
            try:
                record_event(source="audio", audio_events=1)
            except Exception:
                pass
        return info
    
    def get_top_patterns(self, limit: int = 10) -> List[Dict]:
        """Get most frequently used patterns"""
        patterns = sorted(self.graph["code_patterns"].items(), 
                         key=lambda x: x[1]["frequency"], reverse=True)
        return [{"id": p[0], **p[1]} for p in patterns[:limit]]


class SelfLearner:
    """
    Main autonomous learning engine.
    Continuously learns from workspace, web, and self-updates.
    """
    
    def __init__(self, learning_rate: float = 5.0, aggressive: bool = True):
        self.learning_rate = learning_rate
        self.aggressive = aggressive  # Aggressive mode learns from more sources
        self.knowledge = KnowledgeGraph()
        
        # Track processed files (to avoid re-learning)
        self.processed_files: Set[str] = set()
        self.file_hashes: Dict[str, str] = {}
        
        # Initialize AI modules
        self.code_gen = CodeGenerator() if CODE_GEN_AVAILABLE else None
        self.web_nav = None  # Lazy init (Chrome driver)
        
        # Learning stats
        self.stats = {
            "sessions": 0,
            "files_learned": 0,
            "concepts_learned": 0,
            "commands_learned": 0,
            "patterns_learned": 0,
            "web_sessions": 0,
            "start_time": datetime.now(),
            "last_learn_time": None
        }
        
        logger.info(f"SelfLearner initialized (rate: {learning_rate}x, aggressive: {aggressive})")
    
    def get_file_hash(self, file_path: Path) -> str:
        """Get MD5 hash of file content"""
        try:
            content = file_path.read_bytes()
            return hashlib.md5(content).hexdigest()
        except Exception:
            return ""
    
    def should_process_file(self, file_path: Path) -> bool:
        """Check if file needs to be processed (new or changed)"""
        file_str = str(file_path)
        current_hash = self.get_file_hash(file_path)
        
        if file_str not in self.processed_files or self.file_hashes.get(file_str) != current_hash:
            self.file_hashes[file_str] = current_hash
            return True
        return False
    
    def learn_from_python_file(self, file_path: Path):
        """Learn concepts, commands, and patterns from Python file"""
        try:
            content = file_path.read_text(encoding='utf-8')
            tree = ast.parse(content)
            
            # Extract functions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_name = node.name
                    docstring = ast.get_docstring(node) or "No description"
                    
                    # Add as concept
                    self.knowledge.add_concept(
                        name=f"function:{func_name}",
                        description=docstring[:200],
                        examples=[f"def {func_name}(...)"],
                        related=[f"file:{file_path.name}"]
                    )
                    
                    # Extract pattern
                    func_code = ast.get_source_segment(content, node)
                    if func_code and len(func_code) < 500:  # Reasonable size
                        self.knowledge.add_pattern(
                            code=func_code[:300],
                            description=f"Function: {func_name}",
                            use_cases=[docstring[:100]]
                        )
                    
                    self.stats["patterns_learned"] += 1
                
                # Extract class definitions
                elif isinstance(node, ast.ClassDef):
                    class_name = node.name
                    docstring = ast.get_docstring(node) or "No description"
                    
                    self.knowledge.add_concept(
                        name=f"class:{class_name}",
                        description=docstring[:200],
                        examples=[f"class {class_name}:"],
                        related=[f"file:{file_path.name}"]
                    )
                    
                    self.stats["concepts_learned"] += 1
            
            # Extract imports (learn dependencies)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self.knowledge.add_concept(
                            name=f"module:{alias.name}",
                            description=f"Python module: {alias.name}",
                            related=[f"file:{file_path.name}"]
                        )
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        self.knowledge.add_concept(
                            name=f"module:{node.module}",
                            description=f"Python module: {node.module}",
                            related=[f"file:{file_path.name}"]
                        )
            
            self.processed_files.add(str(file_path))
            self.stats["files_learned"] += 1
            logger.info(f"Learned from: {file_path.name}")
            
        except Exception as e:
            logger.debug(f"Could not parse {file_path.name}: {e}")
    
    def learn_from_workspace(self, max_files: Optional[int] = None):
        """Scan workspace and learn from all Python files"""
        logger.info("Starting workspace learning session...")
        start_time = time.time()
        
        python_files = list(WORKSPACE.rglob("*.py"))
        
        # Filter out venv, __pycache__, etc.
        python_files = [f for f in python_files 
                       if not any(exclude in str(f) for exclude in 
                                 ['venv', '__pycache__', '.venv', 'node_modules', 'build', 'dist'])]
        
        if max_files:
            python_files = python_files[:max_files]
        
        learned_count = 0
        for file_path in python_files:
            if self.should_process_file(file_path):
                self.learn_from_python_file(file_path)
                learned_count += 1
                
                # Respect learning rate (delay between files)
                if self.learning_rate < 5.0:
                    time.sleep(0.1 / self.learning_rate)
        
        elapsed = time.time() - start_time
        logger.info(f"Workspace learning complete: {learned_count} files processed in {elapsed:.1f}s")
        
        self.knowledge.save_graph()
        self.stats["last_learn_time"] = datetime.now()
    
    def learn_from_web(self, topics: List[str]):
        """Learn from web sources (YouTube, GitHub, docs)"""
        if not WEB_NAV_AVAILABLE:
            logger.warning("Web learning unavailable (selenium not installed)")
            return
        
        if not self.web_nav:
            self.web_nav = WebNavigator(headless=True)
        
        logger.info(f"Starting web learning: {topics}")
        
        for topic in topics:
            try:
                # Google search for topic
                results = self.web_nav.search_google(f"{topic} python tutorial")
                
                # Add concept from search results
                self.knowledge.add_concept(
                    name=f"topic:{topic}",
                    description=f"Web-learned topic: {topic}",
                    examples=[r[:100] for r in results.get('top_results', [])[:3]]
                )
                
                self.stats["concepts_learned"] += 1
                self.stats["web_sessions"] += 1
                
                # Delay between searches
                time.sleep(2.0 / self.learning_rate)
                
            except Exception as e:
                logger.error(f"Web learning error for {topic}: {e}")
        
        self.knowledge.save_graph()
    
    def learn_from_chat_logs(self):
        """Analyze chat logs to learn new commands and patterns"""
        log_files = list(LOG_DIR.glob("*.log"))
        
        command_patterns = [
            r'"([^"]+\s+ara)"',  # Search commands
            r'"(kod yaz [^"]+)"',  # Code generation
            r'"(unity proje [^"]+)"',  # Game engine
            r'"(öğrenme hızı \d+x)"'  # Learning rate
        ]
        
        for log_file in log_files:
            try:
                content = log_file.read_text(encoding='utf-8')
                
                for pattern in command_patterns:
                    matches = re.findall(pattern, content)
                    for match in matches:
                        # Extract command structure
                        parts = match.split()
                        if len(parts) >= 2:
                            action = parts[1] if len(parts) > 1 else parts[0]
                            
                            self.knowledge.add_command(
                                name=match,
                                syntax=match,
                                description=f"User command: {action}",
                                category="chat",
                                examples=[match]
                            )
                            
                            self.stats["commands_learned"] += 1
            
            except Exception as e:
                logger.debug(f"Could not parse log {log_file.name}: {e}")
        
        self.knowledge.save_graph()
    
    def autonomous_learning_cycle(self, duration_seconds: Optional[int] = None):
        """
        Main learning loop - runs continuously or for specified duration.
        Learns from: workspace, web, chat logs, GitHub repos
        """
        logger.info(f"Starting autonomous learning cycle (duration: {duration_seconds or 'infinite'}s)")
        start_time = time.time()
        cycle = 0
        
        # Topics to learn from web (can be expanded dynamically)
        web_topics = [
            "machine learning", "deep learning", "web scraping", 
            "automation", "API development", "game development",
            "natural language processing", "computer vision"
        ]
        
        while True:
            cycle += 1
            cycle_start = time.time()
            
            logger.info(f"=== Learning Cycle {cycle} ===")
            
            # 1. Learn from workspace (always)
            self.learn_from_workspace(max_files=50 if self.aggressive else 20)
            
            # 2. Learn from chat logs (every cycle)
            self.learn_from_chat_logs()
            
            # 3. Web learning (aggressive mode only, alternate topics)
            if self.aggressive and WEB_NAV_AVAILABLE and cycle % 3 == 0:
                topic = web_topics[cycle % len(web_topics)]
                self.learn_from_web([topic])
            
            # 4. Save stats
            self.stats["sessions"] = cycle
            self.stats["last_learn_time"] = datetime.now()
            
            cycle_elapsed = time.time() - cycle_start
            logger.info(f"Cycle {cycle} complete in {cycle_elapsed:.1f}s | "
                       f"Concepts: {self.knowledge.graph['statistics']['total_concepts']} | "
                       f"Commands: {self.knowledge.graph['statistics']['total_commands']} | "
                       f"Patterns: {self.knowledge.graph['statistics']['total_patterns']}")
            
            # Check duration limit
            if duration_seconds and (time.time() - start_time) >= duration_seconds:
                logger.info(f"Learning cycle ended after {duration_seconds}s")
                break
            
            # Wait before next cycle (adjusted by learning rate)
            wait_time = 60.0 / self.learning_rate  # Base: 1 minute
            logger.info(f"Waiting {wait_time:.1f}s before next cycle...")
            time.sleep(wait_time)
        
        # Final save
        self.knowledge.save_graph()
        self.save_stats()
    
    def save_stats(self):
        """Save learning statistics"""
        stats_file = DATA_DIR / "learning_stats.json"
        stats_data = {
            **self.stats,
            "start_time": self.stats["start_time"].isoformat(),
            "last_learn_time": self.stats["last_learn_time"].isoformat() if self.stats["last_learn_time"] else None,
            "knowledge_graph": self.knowledge.graph["statistics"]
        }
        stats_file.write_text(json.dumps(stats_data, indent=2), encoding='utf-8')
        logger.info(f"Stats saved: {stats_file}")
    
    def get_learning_report(self) -> str:
        """Generate learning report"""
        total_time = datetime.now() - self.stats["start_time"]
        
        report = f"""
🧠 NEXUS-ONE Self-Learning Report
=====================================
Learning Rate: {self.learning_rate}x (Aggressive: {self.aggressive})
Total Sessions: {self.stats['sessions']}
Uptime: {total_time}

📚 Knowledge Acquired:
  • Concepts: {self.knowledge.graph['statistics']['total_concepts']}
  • Commands: {self.knowledge.graph['statistics']['total_commands']}
  • Code Patterns: {self.knowledge.graph['statistics']['total_patterns']}
  • Files Processed: {self.stats['files_learned']}
  • Web Sessions: {self.stats['web_sessions']}

🔗 Knowledge Relationships: {len(self.knowledge.graph['relationships'])}

⚡ Learning Performance:
  • Concepts/hour: {self.stats['concepts_learned'] / max(1, total_time.total_seconds() / 3600):.1f}
  • Last Update: {self.stats['last_learn_time'] or 'N/A'}

🎯 Top Patterns (by frequency):
"""
        top_patterns = self.knowledge.get_top_patterns(5)
        for i, pattern in enumerate(top_patterns, 1):
            report += f"  {i}. {pattern['description'][:50]} (used {pattern['frequency']}x)\n"
        
        return report


def main():
    """CLI interface for self-learner"""
    import argparse
    
    parser = argparse.ArgumentParser(description="NEXUS-ONE Self-Learning Engine")
    parser.add_argument("--rate", type=float, default=5.0, help="Learning rate multiplier (default: 5.0)")
    parser.add_argument("--aggressive", action="store_true", help="Enable aggressive learning (web + more)")
    parser.add_argument("--duration", type=int, help="Learning duration in seconds (default: infinite)")
    parser.add_argument("--report", action="store_true", help="Show learning report and exit")
    
    args = parser.parse_args()
    
    learner = SelfLearner(learning_rate=args.rate, aggressive=args.aggressive)
    
    if args.report:
        print(learner.get_learning_report())
        return
    
    try:
        learner.autonomous_learning_cycle(duration_seconds=args.duration)
    except KeyboardInterrupt:
        logger.info("Learning interrupted by user")
        learner.save_stats()
        print("\n" + learner.get_learning_report())


if __name__ == "__main__":
    main()
