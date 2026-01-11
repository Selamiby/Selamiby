# language_generator_ai.py
import hashlib
import json
import os
import random
from datetime import datetime


class LanguageGeneratorAI:
    def __init__(self):
        self.language_features = {
            "paradigms": ["object-oriented", "functional", "procedural", "declarative", "imperative"],
            "typing": ["static", "dynamic", "strong", "weak", "gradual", "inferred"],
            "memory_management": ["garbage-collected", "manual", "reference-counting", "RAII"],
            "concurrency": ["async/await", "threads", "coroutines", "actors", "CSP"],
            "syntax_style": ["C-like", "Python-like", "Lisp-like", "ML-like", "unique"]
        }
        
        self.base_templates = {
            "C-like": {
                "function": "returnType functionName(parameters) {\n    // code\n}",
                "class": "class ClassName {\n    // members\n};",
                "loop": "for (int i = 0; i < n; i++) {\n    // code\n}",
                "condition": "if (condition) {\n    // code\n} else {\n    // code\n}"
            },
            "Python-like": {
                "function": "def function_name(parameters):\n    # code\n    return result",
                "class": "class ClassName:\n    def __init__(self):\n        pass",
                "loop": "for item in collection:\n    # code",
                "condition": "if condition:\n    # code\nelse:\n    # code"
            },
            "Lisp-like": {
                "function": "(defun function-name (parameters)\n    ; code\n    (return result))",
                "class": "(defclass class-name ()\n    ((slot1 :initarg :slot1)\n     (slot2 :initarg :slot2)))",
                "loop": "(loop for i from 0 below n do\n    ; code)",
                "condition": "(if condition\n    ; then\n    ; else)"
            }
        }
        
        print("🤖 AI DİL ÜRETİCİ BAŞLATILIYOR...")
    
    def generate_language_name(self):
        """Rastgele dil ismi üret"""
        prefixes = ["Nex", "Py", "Java", "C", "Go", "Rus", "Swif", "Kot", "Scal", "Elix"]
        suffixes = ["on", "ix", "lang", "script", "sharp", "++", "--", "λ", "σ", "π"]
        middles = ["", "ro", "ta", "mi", "vo", "la", "ti", "no", "va", "do"]
        
        name = random.choice(prefixes) + random.choice(middles) + random.choice(suffixes)
        
        # Benzersiz hash ekle
        hash_part = hashlib.md5(name.encode()).hexdigest()[:4]
        
        return f"{name}-{hash_part}"
    
    def select_features(self):
        """Rastgele dil özellikleri seç"""
        selected = {}
        
        for category, options in self.language_features.items():
            # 1-3 özellik seç
            count = random.randint(1, min(3, len(options)))
            selected[category] = random.sample(options, count)
        
        return selected
    
    def generate_syntax(self, features, template_style):
        """Seçilen özelliklere göre syntax oluştur"""
        if template_style not in self.base_templates:
            template_style = "C-like"
        
        syntax = self.base_templates[template_style].copy()
        
        # Özelliklere göre modify
        if "functional" in features["paradigms"]:
            syntax["lambda"] = "(lambda parameters: expression)"
            syntax["map"] = "map(function, collection)"
            syntax["filter"] = "filter(predicate, collection)"
        
        if "static" in features["typing"]:
            syntax["variable"] = "Type variableName = value"
            syntax["function_with_types"] = "functionName(param: Type) -> ReturnType"
        else:
            syntax["variable"] = "var variableName = value"
        
        if "async/await" in features["concurrency"]:
            syntax["async_function"] = "async def functionName():\n    result = await operation"
            syntax["async_call"] = "await asyncFunction()"
        
        if "garbage-collected" in features["memory_management"]:
            syntax["memory"] = "// Automatic garbage collection"
        else:
            syntax["memory"] = "// Manual memory management required"
        
        return syntax
    
    def generate_standard_library(self, language_name, features):
        """Standart kütüphane oluştur"""
        stdlib = {
            "io": [
                f"{language_name}.print(value)",
                f"{language_name}.read()",
                f"{language_name}.write(file, data)"
            ],
            "collections": [
                f"{language_name}.List()",
                f"{language_name}.Map()",
                f"{language_name}.Set()"
            ],
            "math": [
                f"{language_name}.math.sqrt(x)",
                f"{language_name}.math.sin(x)",
                f"{language_name}.math.random()"
            ]
        }
        
        # Özelliklere özel modüller ekle
        if "functional" in features["paradigms"]:
            stdlib["functional"] = [
                f"{language_name}.functools.map(f, list)",
                f"{language_name}.functools.filter(pred, list)",
                f"{language_name}.functools.reduce(f, list)"
            ]
        
        if "async/await" in features["concurrency"]:
            stdlib["async"] = [
                f"{language_name}.async.sleep(seconds)",
                f"{language_name}.async.gather(tasks)",
                f"{language_name}.async.create_task(func)"
            ]
        
        return stdlib
    
    def generate_example_programs(self, language_name, syntax):
        """Örnek programlar oluştur"""
        examples = {}
        
        # 1. Hello World
        if "function" in syntax:
            hello_template = syntax["function"].replace("functionName", "main")
            hello_code = hello_template.replace("// code", f'print("Hello, {language_name}!")')
            examples["hello_world"] = hello_code
        
        # 2. Fibonacci
        fib_code = f'''
# Fibonacci in {language_name}
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# Test
for i in range(10):
    print(f"fib({{i}}) = {{fibonacci(i)}}")
'''
        examples["fibonacci"] = fib_code
        
        # 3. Class example
        if "class" in syntax:
            class_code = syntax["class"].replace("ClassName", "Person")
            class_code = class_code.replace("// members", "name: string\n    age: number")
            examples["class_example"] = class_code
        
        return examples
    
    def create_new_language(self):
        """Tamamen yeni bir programlama dili oluştur"""
        print("\n🎨 YENİ PROGRAMLAMA DİLİ OLUŞTURULUYOR...")
        
        # 1. Dil ismi üret
        language_name = self.generate_language_name()
        print(f"   • İsim: {language_name}")
        
        # 2. Özellikler seç
        features = self.select_features()
        print(f"   • Paradigmalar: {', '.join(features['paradigms'])}")
        print(f"   • Tip sistemi: {', '.join(features['typing'])}")
        print(f"   • Eşzamanlılık: {', '.join(features['concurrency'])}")
        
        # 3. Syntax stili seç
        syntax_style = random.choice(features["syntax_style"])
        print(f"   • Syntax stili: {syntax_style}")
        
        # 4. Syntax oluştur
        syntax = self.generate_syntax(features, syntax_style)
        
        # 5. Standart kütüphane oluştur
        stdlib = self.generate_standard_library(language_name, features)
        
        # 6. Örnek programlar oluştur
        examples = self.generate_example_programs(language_name, syntax)
        
        # 7. Dil spesifikasyonu oluştur
        language_spec = {
            "name": language_name,
            "version": "1.0.0",
            "created": datetime.now().isoformat(),
            "features": features,
            "syntax": syntax,
            "standard_library": stdlib,
            "examples": examples,
            "compiler_target": random.choice(["bytecode", "native", "JVM", "WASM", "interpreted"]),
            "license": random.choice(["MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause", "Proprietary"])
        }
        
        # 8. Dosyaya kaydet
        os.makedirs("generated_languages", exist_ok=True)
        filename = f"generated_languages/{language_name}.json"
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(language_spec, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Yeni dil oluşturuldu: {filename}")
        print(f"\n📝 ÖRNEK KOD (Hello World):")
        if "hello_world" in examples:
            print(examples["hello_world"])
        
        return language_spec
    
    def generate_multiple_languages(self, count=5):
        """Birden fazla dil oluştur"""
        print(f"\n🏭 {count} YENİ DİL ÜRETİMİ BAŞLIYOR...")
        
        languages = []
        for i in range(count):
            print(f"\n[{i+1}/{count}]")
            lang = self.create_new_language()
            languages.append(lang)
        
        # Özet raporu
        print("\n" + "="*80)
        print("📊 ÜRETİLEN DİLLER ÖZETİ:")
        
        paradigms_count = {}
        typing_count = {}
        
        for lang in languages:
            for paradigm in lang["features"]["paradigms"]:
                paradigms_count[paradigm] = paradigms_count.get(paradigm, 0) + 1
            
            for typing in lang["features"]["typing"]:
                typing_count[typing] = typing_count.get(typing, 0) + 1
        
        print(f"\n   • Toplam dil: {len(languages)}")
        print(f"   • En popüler paradigma: {max(paradigms_count.items(), key=lambda x: x[1])[0]}")
        print(f"   • En popüler tip sistemi: {max(typing_count.items(), key=lambda x: x[1])[0]}")
        
        # Tüm dilleri birleştir
        all_languages_file = "generated_languages/ALL_LANGUAGES.json"
        with open(all_languages_file, "w", encoding="utf-8") as f:
            json.dump(languages, f, indent=2, ensure_ascii=False)
        
        print(f"\n📁 Tüm diller: {all_languages_file}")
        
        return languages

def main():
    generator = LanguageGeneratorAI()
    
    # 1. Tek dil oluştur
    print("="*80)
    print("🤖 AI DİL ÜRETİCİ - TEK DİL MODU")
    print("="*80)
    
    single_language = generator.create_new_language()
    
    # 2. Çoklu dil oluştur
    print("\n" + "="*80)
    print("🏭 AI DİL ÜRETİCİ - ÇOKLU DİL MODU")
    print("="*80)
    
    multiple_languages = generator.generate_multiple_languages(3)
    
    # 3. Sonuçlar
    print("\n" + "="*80)
    print("🎯 DİL ÜRETİMİ TAMAMLANDI!")
    print("="*80)
    
    total_examples = sum(len(lang.get("examples", {})) for lang in multiple_languages)
    
    print(f"""
📊 SONUÇLAR:
   • Oluşturulan toplam dil: {len(multiple_languages) + 1}
   • Toplam örnek kod: {total_examples + len(single_language.get("examples", {}))}
   • Kaydedilen dosya: generated_languages/ klasörü
   • Her dil için: JSON spec + örnek kodlar

🚀 BİR SONRAKİ ADIM:
   Bu diller için compiler/interpreter yazabilirsiniz!
   Veya daha fazla dil üretmek için tekrar çalıştırın.
    """)
    
    return {
        "single_language": single_language,
        "multiple_languages": multiple_languages
    }

if __name__ == "__main__":
    main()
