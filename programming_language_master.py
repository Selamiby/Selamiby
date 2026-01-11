# programming_language_master.py
import hashlib
import json
import os
import re
from collections import Counter
from datetime import datetime


class ProgrammingLanguageMaster:
    def __init__(self):
        self.languages = {
            "Python": {
                "extensions": [".py", ".pyw"],
                "keywords": ["def", "class", "import", "from", "if", "else", "for", "while"],
                "syntax": {
                    "function": "def function_name(parameters):",
                    "class": "class ClassName:",
                    "comment": "# Comment",
                    "string": "'string' or \"string\"",
                    "import": "import module or from module import something"
                }
            },
            "JavaScript": {
                "extensions": [".js", ".jsx", ".ts", ".tsx"],
                "keywords": ["function", "const", "let", "var", "if", "else", "for", "while"],
                "syntax": {
                    "function": "function functionName(parameters) { }",
                    "class": "class ClassName { }",
                    "comment": "// Comment or /* Comment */",
                    "string": "'string' or \"string\" or `template`",
                    "import": "import module from 'path'"
                }
            },
            "Java": {
                "extensions": [".java"],
                "keywords": ["public", "class", "void", "static", "if", "else", "for", "while"],
                "syntax": {
                    "function": "public void functionName(parameters) { }",
                    "class": "public class ClassName { }",
                    "comment": "// Comment or /* Comment */",
                    "string": "\"string\"",
                    "import": "import package.Class;"
                }
            },
            "C++": {
                "extensions": [".cpp", ".h", ".hpp"],
                "keywords": ["#include", "using", "namespace", "int", "void", "if", "else"],
                "syntax": {
                    "function": "returnType functionName(parameters) { }",
                    "class": "class ClassName { };",
                    "comment": "// Comment or /* Comment */",
                    "string": "\"string\"",
                    "import": "#include <library>"
                }
            },
            "Go": {
                "extensions": [".go"],
                "keywords": ["func", "package", "import", "if", "else", "for", "range"],
                "syntax": {
                    "function": "func functionName(parameters) returnType { }",
                    "struct": "type StructName struct { }",
                    "comment": "// Comment or /* Comment */",
                    "string": "\"string\" or `raw string`"
                }
            },
            "Rust": {
                "extensions": [".rs"],
                "keywords": ["fn", "let", "mut", "if", "else", "for", "while", "match"],
                "syntax": {
                    "function": "fn function_name(parameters) -> return_type { }",
                    "struct": "struct StructName { }",
                    "comment": "// Comment or /* Comment */",
                    "string": "\"string\""
                }
            }
        }
        
        # Tüm dillerden örnek kodlar
        self.sample_code = self.load_sample_codes()
        
        print("🧠 PROGRAMLAMA DİLİ UZMANI BAŞLATILIYOR...")
        print(f"📚 Bilinen diller: {len(self.languages)}")
    
    def load_sample_codes(self):
        """Örnek kodları yükle veya oluştur"""
        samples = {}
        
        # Python
        samples["Python"] = '''
# Fibonacci serisi
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# Sınıf örneği
class Calculator:
    def __init__(self):
        self.result = 0
    
    def add(self, x):
        self.result += x
        return self.result

# Lambda fonksiyonu
square = lambda x: x * x
'''
        
        # JavaScript
        samples["JavaScript"] = '''
// Fibonacci serisi
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// Sınıf örneği
class Calculator {
    constructor() {
        this.result = 0;
    }
    
    add(x) {
        this.result += x;
        return this.result;
    }
}

// Arrow function
const square = x => x * x;
'''
        
        # Daha fazla dil ekleyebilirsin...
        
        return samples
    
    def detect_language(self, code):
        """Kodun hangi dilde olduğunu tespit et"""
        scores = {}
        
        for lang_name, lang_info in self.languages.items():
            score = 0
            
            # Anahtar kelime kontrolü
            for keyword in lang_info["keywords"]:
                if keyword in code:
                    score += 1
            
            # Sözdizimi kalıpları kontrolü
            for pattern in lang_info["syntax"].values():
                if any(char in code for char in ["#", "//", "/*", "{", "}", ";"]) and \
                   pattern.split()[0] in code:
                    score += 1
            
            scores[lang_name] = score
        
        # En yüksek skorlu dili bul
        if scores:
            return max(scores.items(), key=lambda x: x[1])
        return ("Unknown", 0)
    
    def translate_code(self, source_code, source_lang, target_lang):
        """Kodu bir dilden diğerine çevir"""
        print(f"\n🔄 Çeviri: {source_lang} → {target_lang}")
        
        # Basit çeviri kuralları
        translation_rules = {
            "Python_to_JavaScript": {
                "def ": "function ",
                "print(": "console.log(",
                "self.": "this.",
                "True": "true",
                "False": "false",
                "None": "null"
            },
            "JavaScript_to_Python": {
                "function ": "def ",
                "console.log(": "print(",
                "this.": "self.",
                "true": "True",
                "false": "False",
                "null": "None",
                "let ": "",
                "const ": "",
                "var ": ""
            }
        }
        
        rule_key = f"{source_lang}_to_{target_lang}"
        if rule_key not in translation_rules:
            rule_key = f"{target_lang}_to_{source_lang}"
            # Tersine çevir
            if rule_key in translation_rules:
                # Ters çeviri için reverse rules
                rules = translation_rules[rule_key]
                reverse_rules = {v: k for k, v in rules.items()}
                translated_code = source_code
                for old, new in reverse_rules.items():
                    translated_code = translated_code.replace(old, new)
            else:
                return f"⚠️ {source_lang} → {target_lang} çevirisi henüz desteklenmiyor"
        else:
            rules = translation_rules[rule_key]
            translated_code = source_code
            for old, new in rules.items():
                translated_code = translated_code.replace(old, new)
        
        # Ek düzenlemeler
        if target_lang == "Python":
            translated_code = translated_code.replace(";", "")
            # Girintileri düzelt
            lines = translated_code.split('\n')
            translated_code = '\n'.join(['    ' + line if line.strip() and not line.strip().startswith(('def ', 'class ', 'if ', 'for ', 'while ')) else line for line in lines])
        
        return translated_code
    
    def learn_from_data(self, data_dir="data"):
        """Toplanan verilerden öğren"""
        print("\n📚 TOPLANAN VERİLERDEN ÖĞRENİYOR...")
        
        if not os.path.exists(data_dir):
            print(f"   ⚠️ {data_dir} klasörü bulunamadı")
            return {}
        
        # JSON dosyalarını analiz et
        code_patterns = Counter()
        language_distribution = Counter()
        
        for file in os.listdir(data_dir):
            if file.endswith(".json") and file != "summary.json":
                try:
                    with open(os.path.join(data_dir, file), "r", encoding="utf-8") as f:
                        data = json.load(f)
                        
                        for block in data.get("code_blocks", []):
                            code = block.get("code", "")
                            lang = block.get("language", "Unknown")
                            
                            language_distribution[lang] += 1
                            
                            # Basit pattern analizi
                            if "def " in code:
                                code_patterns["Python_function"] += 1
                            if "function " in code:
                                code_patterns["JS_function"] += 1
                            if "class " in code:
                                code_patterns["Class_definition"] += 1
                            if "import " in code:
                                code_patterns["Import_statement"] += 1
                            
                except Exception as e:
                    print(f"   ⚠️ {file} okunamadı: {e}")
        
        # Öğrenme sonuçları
        print(f"\n📊 ÖĞRENME SONUÇLARI:")
        print(f"   • Toplam kod bloğu: {sum(language_distribution.values()):,}")
        print(f"   • En popüler dil: {language_distribution.most_common(1)[0][0]}")
        
        print("\n🔍 KOD PATTERNLARI:")
        for pattern, count in code_patterns.most_common(5):
            print(f"   • {pattern}: {count:,}")
        
        return {
            "language_distribution": dict(language_distribution),
            "code_patterns": dict(code_patterns)
        }
    
    def create_new_language(self, name, base_lang="Python", features=[]):
        """Yeni bir programlama dili oluştur"""
        print(f"\n🎨 YENİ PROGRAMLAMA DİLİ OLUŞTURULUYOR: {name}")
        print(f"   • Temel dil: {base_lang}")
        print(f"   • Özellikler: {', '.join(features)}")
        
        # Yeni dil yapısı
        new_language = {
            "name": name,
            "base": base_lang,
            "features": features,
            "created": datetime.now().isoformat(),
            "syntax": {}
        }
        
        # Temel syntax'ı kopyala
        if base_lang in self.languages:
            new_language["syntax"] = self.languages[base_lang]["syntax"].copy()
        
        # Özel özellikler ekle
        if "simple" in features:
            new_language["syntax"]["function"] = "fn name(params) -> result"
            new_language["syntax"]["comment"] = "## Comment"
        
        if "modern" in features:
            new_language["syntax"]["type_inference"] = "var name = value"
            new_language["syntax"]["lambda"] = "param => expression"
        
        if "safe" in features:
            new_language["syntax"]["null_safety"] = "value!"
            new_language["syntax"]["immutable"] = "let name = value"
        
        # Örnek kod oluştur
        example_code = self.generate_example_code(new_language)
        
        new_language["example"] = example_code
        
        # Dosyaya kaydet
        os.makedirs("new_languages", exist_ok=True)
        filename = f"new_languages/{name.lower().replace(' ', '_')}.json"
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(new_language, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Yeni dil oluşturuldu: {filename}")
        print(f"\n📝 ÖRNEK KOD:")
        print(example_code)
        
        return new_language
    
    def generate_example_code(self, language_spec):
        """Yeni dil için örnek kod oluştur"""
        name = language_spec["name"]
        syntax = language_spec["syntax"]
        
        example = f"""
# {name} Programming Language - Example
# Created: {language_spec['created']}

# Function definition
{syntax.get('function', 'def hello()')}
    # This is a comment
    message = "Hello, World!"
    return message

# Class example
{syntax.get('class', 'class Person')}
    name: string
    age: number
    
    {syntax.get('function', 'def __init__')}(self, name, age)
        self.name = name
        self.age = age
    
    {syntax.get('function', 'def greet')}(self)
        return "Hello, my name is " + self.name

# Main program
main = {syntax.get('function', 'def main')}()
    person = Person("Alice", 30)
    print(person.greet())
    return 0
"""
        
        return example
    
    def analyze_and_improve(self):
        """Mevcut dilleri analiz et ve iyileştir"""
        print("\n🔧 DİL ANALİZİ VE İYİLEŞTİRME...")
        
        improvements = []
        
        # Python analizi
        python_issues = []
        if "Python" in self.languages:
            python_info = self.languages["Python"]
            
            # Eksik özellikleri tespit et
            if "async" not in str(python_info):
                python_issues.append("Async/await syntax eksik")
            if "type_hints" not in str(python_info):
                python_issues.append("Type hints eksik")
            
            if python_issues:
                improvements.append({
                    "language": "Python",
                    "issues": python_issues,
                    "suggestions": [
                        "async def async_function(): await operation",
                        "def typed_function(name: str) -> int: return len(name)"
                    ]
                })
        
        # JavaScript analizi
        js_issues = []
        if "JavaScript" in self.languages:
            js_info = self.languages["JavaScript"]
            
            if "optional_chaining" not in str(js_info):
                js_issues.append("Optional chaining (?.) eksik")
            if "nullish_coalescing" not in str(js_info):
                js_issues.append("Nullish coalescing (??) eksik")
            
            if js_issues:
                improvements.append({
                    "language": "JavaScript",
                    "issues": js_issues,
                    "suggestions": [
                        "const value = obj?.property",
                        "const result = input ?? 'default'"
                    ]
                })
        
        # İyileştirme önerilerini göster
        if improvements:
            print("💡 İYİLEŞTİRME ÖNERİLERİ:")
            for imp in improvements:
                print(f"\n   • {imp['language']}:")
                for issue in imp['issues']:
                    print(f"     - {issue}")
                for suggestion in imp['suggestions'][:2]:
                    print(f"     + {suggestion}")
        else:
            print("✅ Tüm diller güncel!")
        
        return improvements

def main():
    master = ProgrammingLanguageMaster()
    
    # 1. Verilerden öğren
    learning_results = master.learn_from_data()
    
    # 2. Kod analizi yap
    sample_code = '''
def merhaba(isim):
    print(f"Merhaba, {isim}!")
    return True

class Kullanici:
    def __init__(self, ad, yas):
        self.ad = ad
        self.yas = yas
'''
    
    detected_lang, score = master.detect_language(sample_code)
    print(f"\n🔍 KOD ANALİZİ:")
    print(f"   • Dil: {detected_lang} (skor: {score})")
    
    # 3. Kod çevirisi
    if detected_lang == "Python":
        translated = master.translate_code(sample_code, "Python", "JavaScript")
        print(f"\n🔄 ÇEVRİLMİŞ KOD (JavaScript):")
        print(translated[:500])
    
    # 4. Yeni dil oluştur
    new_lang = master.create_new_language(
        name="NexusLang",
        base_lang="Python",
        features=["simple", "modern", "safe", "fast"]
    )
    
    # 5. Mevcut dilleri analiz et
    improvements = master.analyze_and_improve()
    
    print("\n" + "="*80)
    print("🎯 PROGRAMLAMA DİLİ UZMANI GÖREVİ TAMAMLANDI!")
    print("="*80)
    
    return {
        "learning_results": learning_results,
        "new_language": new_lang,
        "improvements": improvements
    }

if __name__ == "__main__":
    main()
