# emotion_solver.py
import re


class EmotionSolver:
    def analyze_code_mood(self, code):
        moods = {
            "mutlu": ["# :)", "print('success')", "return True"],
            "üzgün": ["# TODO", "# FIXME", "except Exception as e"],
            "kızgın": ["# WTF", "# BUG", "raise Error"],
            "şaşkın": ["# ???", "# magic", "# hack"]
        }
        
        mood_score = {}
        for mood, indicators in moods.items():
            score = sum(code.count(indicator) for indicator in indicators)
            mood_score[mood] = score
        
        return max(mood_score.items(), key=lambda x: x[1])[0]
    
    def auto_fix_problems(self, code):
        fixes = [
            (r'= =', '=='),
            (r'print\s*\(', 'print('),
            (r'if\s*\(.*\)\s*:', 'if condition:'),
        ]
        
        for pattern, replacement in fixes:
            code = re.sub(pattern, replacement, code)
        
        return code
