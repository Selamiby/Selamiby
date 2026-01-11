"""
Seviye 2: AI-POWERED OTONOM SİSTEM
Context-Aware Yardım Sistemi - Kullanıcı alışkanlıkları, proaktif öneriler, hata önleme
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
from collections import defaultdict


class UserContextManager:
    """Kullanıcı bağlamı ve alışkanlıklarını yönet"""
    
    def __init__(self, context_file: str = "data/user_context.json"):
        self.context_file = Path(context_file)
        self.context_file.parent.mkdir(parents=True, exist_ok=True)
        self.user_context = self._load_context()
        
    def record_action(self, action_type: str, details: Dict):
        """Kullanıcı eylemini kaydet"""
        if "actions" not in self.user_context:
            self.user_context["actions"] = []
        
        self.user_context["actions"].append({
            "type": action_type,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        
        # Son 1000 eylemini tut
        self.user_context["actions"] = self.user_context["actions"][-1000:]
        
        self._save_context()
    
    def learn_habits(self) -> Dict:
        """Kullanıcı alışkanlıklarını öğren"""
        actions = self.user_context.get("actions", [])
        
        if not actions:
            return {"error": "No action history"}
        
        habits = {
            "most_used_actions": self._get_most_used_actions(actions),
            "action_times": self._analyze_action_times(actions),
            "common_files": self._find_common_files(actions),
            "preferred_operations": self._get_preferred_operations(actions)
        }
        
        return habits
    
    def get_proactive_suggestions(self) -> List[Dict]:
        """Proaktif öneriler sun"""
        habits = self.learn_habits()
        suggestions = []
        
        if "error" in habits:
            return suggestions
        
        # En sık yapılan işlemleri öner
        for action in habits.get("most_used_actions", [])[:3]:
            suggestions.append({
                "type": "frequent_action",
                "suggestion": f"You frequently {action['action']}",
                "frequency": action["count"]
            })
        
        # Hata önleme önerileri
        suggestions.extend(self._get_error_prevention_suggestions())
        
        return suggestions
    
    def predict_next_action(self) -> Dict:
        """Sonraki eylem tahmini yap"""
        actions = self.user_context.get("actions", [])
        
        if len(actions) < 2:
            return {"prediction": None}
        
        # Son eylemden sonra sıklıkla ne yapıyor?
        last_action = actions[-1]["type"] if actions else None
        
        sequences = self._find_action_sequences(actions)
        
        if last_action in sequences:
            next_likely = sequences[last_action]
            next_likely.sort(key=lambda x: x["frequency"], reverse=True)
            
            return {
                "last_action": last_action,
                "predicted_next": next_likely[0] if next_likely else None,
                "alternatives": next_likely[1:3]
            }
        
        return {"prediction": None}
    
    def _get_most_used_actions(self, actions: List) -> List[Dict]:
        """En sık yapılan işlemleri bul"""
        action_counts = defaultdict(int)
        
        for action in actions:
            action_counts[action["type"]] += 1
        
        return [
            {"action": action, "count": count}
            for action, count in sorted(action_counts.items(), 
                                       key=lambda x: x[1], reverse=True)
        ]
    
    def _analyze_action_times(self, actions: List) -> Dict:
        """Eylem zamanlarını analiz et"""
        hours = defaultdict(int)
        
        for action in actions:
            try:
                dt = datetime.fromisoformat(action["timestamp"])
                hours[dt.hour] += 1
            except Exception:
                pass
        
        if not hours:
            return {}
        
        peak_hour = max(hours.items(), key=lambda x: x[1])
        
        return {
            "peak_hour": peak_hour[0],
            "peak_activity": peak_hour[1],
            "hourly_distribution": dict(sorted(hours.items()))
        }
    
    def _find_common_files(self, actions: List) -> List[str]:
        """Sık kullanılan dosyaları bul"""
        files = defaultdict(int)
        
        for action in actions:
            details = action.get("details", {})
            if "file" in details:
                files[details["file"]] += 1
            elif "files" in details:
                for f in details["files"]:
                    files[f] += 1
        
        return [f for f, _ in sorted(files.items(), 
                                     key=lambda x: x[1], reverse=True)[:10]]
    
    def _get_preferred_operations(self, actions: List) -> Dict:
        """Tercih edilen işlemleri bul"""
        operations = defaultdict(int)
        
        for action in actions:
            details = action.get("details", {})
            if "operation" in details:
                operations[details["operation"]] += 1
        
        return dict(sorted(operations.items(), 
                          key=lambda x: x[1], reverse=True))
    
    def _find_action_sequences(self, actions: List) -> Dict:
        """Eylem dizilerini bul"""
        sequences = defaultdict(list)
        
        for i in range(len(actions) - 1):
            current = actions[i]["type"]
            next_action = actions[i + 1]["type"]
            
            # Diziye ekle
            found = False
            for seq in sequences[current]:
                if seq["action"] == next_action:
                    seq["frequency"] += 1
                    found = True
                    break
            
            if not found:
                sequences[current].append({"action": next_action, "frequency": 1})
        
        return sequences
    
    def _get_error_prevention_suggestions(self) -> List[Dict]:
        """Hata önleme önerileri"""
        suggestions = []
        
        # Çok büyük dosyalara dikkat et
        if "common_files" in self.learn_habits():
            suggestions.append({
                "type": "error_prevention",
                "suggestion": "Be careful with large files - consider backups",
                "priority": "high"
            })
        
        return suggestions
    
    def _load_context(self) -> Dict:
        """Bağlamı yükle"""
        if self.context_file.exists():
            try:
                with open(self.context_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}
    
    def _save_context(self):
        """Bağlamı kaydet"""
        with open(self.context_file, 'w') as f:
            json.dump(self.user_context, f, indent=2)


class ErrorPreventionSystem:
    """Hata önleme sistemi"""
    
    def __init__(self):
        self.error_patterns = {}
        self.prevention_rules = self._load_rules()
        
    def detect_risky_operation(self, operation: str, context: Dict) -> Dict:
        """Riskli işlemi tespit et"""
        risks = []
        
        # Kritik dosyayı silme riski
        if operation == "delete":
            path = context.get("path", "")
            if self._is_critical_file(path):
                risks.append({
                    "type": "critical_file_deletion",
                    "severity": "critical",
                    "message": f"You are about to delete a critical file: {path}",
                    "recommendation": "Make a backup first"
                })
        
        # Sistem dosyalarında değişiklik
        if operation in ["modify", "delete", "move"]:
            path = context.get("path", "")
            if self._is_system_file(path):
                risks.append({
                    "type": "system_file_operation",
                    "severity": "high",
                    "message": "This is a system file",
                    "recommendation": "Proceed with caution"
                })
        
        return {
            "operation": operation,
            "risky": len(risks) > 0,
            "risks": risks
        }
    
    def suggest_safe_alternative(self, operation: str, context: Dict) -> Dict:
        """Güvenli alternatif öner"""
        if operation == "delete":
            return {
                "alternative": "move_to_trash",
                "reason": "You can recover files from trash",
                "benefits": ["Can be undone", "Safer", "Data recovery possible"]
            }
        
        return {"alternative": None}
    
    def _is_critical_file(self, path: str) -> bool:
        """Kritik dosya mı"""
        critical_paths = [
            "system32", "windows", "drivers", 
            "/etc", "/sys", "/boot"
        ]
        
        for cp in critical_paths:
            if cp in path.lower():
                return True
        
        return False
    
    def _is_system_file(self, path: str) -> bool:
        """Sistem dosyası mı"""
        system_extensions = [".sys", ".dll", ".exe", ".ko"]
        system_dirs = ["Windows", "Program Files", "/usr", "/bin"]
        
        path_lower = path.lower()
        
        if any(path_lower.endswith(ext) for ext in system_extensions):
            return True
        
        if any(sdir in path for sdir in system_dirs):
            return True
        
        return False
    
    def _load_rules(self) -> Dict:
        """Kuralları yükle"""
        return {
            "never_delete_without_backup": True,
            "confirm_large_file_operations": True,
            "log_system_file_access": True
        }


# Global instances
user_context = UserContextManager()
error_prevention = ErrorPreventionSystem()
