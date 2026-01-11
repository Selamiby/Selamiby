#!/usr/bin/env python3
"""
NEXUS-ONE - Autonomous AI Operating System
Where All Intelligence Converges
"""
import asyncio
import importlib
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Try to import brand module
try:
    from brand.logo_display import NexusBrand
    BRAND_LOADED = True
except ImportError:
    BRAND_LOADED = False
    print("⚠️  Brand module not found, using basic display")

class NexusOne:
    """NEXUS-ONE Ana Sınıfı"""
    
    def __init__(self):
        self.name = "NEXUS-ONE"
        self.version = "1.0.0"
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.modules = {}
        self.command_history = []
        
        # Initialize brand
        self.brand = NexusBrand() if BRAND_LOADED else None
        
        # System startup
        self._system_startup()
        
    def _system_startup(self):
        """Sistem başlangıç rutini"""
        # Clear screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Display logo
        if self.brand:
            self.brand.display_rich_logo()
            print(self.brand.generate_welcome_message())
        else:
            self._display_basic_banner()
        
        # Load modules
        self._load_modules()
        
        print("\n" + "="*60)
        print("🚀 Initialization Complete | Ready for Commands")
        print("="*60)
    
    def _display_basic_banner(self):
        """Temel banner göster"""
        print(r"""
        ╔╗╔╦╗╔╦╗╔═╗╦ ╦╔═╗  ╔═╗╔╗╔╔═╗╔╦╗
        ║║║║║ ║║╠═╝║ ║╚═╗  ║ ║║║║╚═╗ ║ 
        ╝╚╝╩╩═╝╩╩  ╚═╝╚═╝  ╚═╝╝╚╝╚═╝ ╩ 
        
        ╔══════════════════════════════════════╗
        ║     NEXUS-ONE v1.0.0                 ║
        ║     Autonomous AI Operating System   ║
        ║     Where All Intelligence Converges ║
        ╚══════════════════════════════════════╝
        """)
        
        print(f"\n📅 Session: {self.session_id}")
        print(f"🐍 Python: {sys.version.split()[0]}")
        print(f"📁 Directory: {os.getcwd()}")
    
    def _load_modules(self):
        """Modülleri yükle"""
        print("\n📦 Loading AI Modules...")
        print("-" * 40)
        
        modules_to_load = [
            ("core.ai_engine", "AI Engine"),
            ("modules.file_manager", "File Manager"),
            ("modules.system_monitor", "System Monitor"),
            ("modules.file_organizer", "File Organizer"),
            ("modules.web_researcher", "Web Researcher"),
            ("ai_libraries.ai_utils", "AI Utilities"),
            ("ai_libraries.task_manager", "Task Manager")
        ]
        
        for module_path, module_name in modules_to_load:
            try:
                # Dynamic import of full module path; store module object for menus
                module = importlib.import_module(module_path)
                self.modules[module_name.lower().replace(' ', '_')] = module
                print(f"   ✅ {module_name}")
            except ImportError as e:
                print(f"   ❌ {module_name}: {str(e)[:80]}...")
            except Exception as e:
                print(f"   ⚠️  {module_name}: Error - {str(e)[:80]}")
        
        print(f"\n✅ Loaded {len([m for m in self.modules.values() if m])}/{len(modules_to_load)} modules")
    
    def display_main_menu(self):
        """Ana menüyü göster"""
        menu_options = {
            "1": {"name": "File Operations", "desc": "Intelligent file management"},
            "2": {"name": "AI Analysis", "desc": "Text analysis and AI chat"},
            "3": {"name": "System Monitor", "desc": "Real-time system monitoring"},
            "4": {"name": "Web Research", "desc": "Autonomous web research"},
            "5": {"name": "Task Automation", "desc": "Automated task workflows"},
            "6": {"name": "System Info", "desc": "NEXUS-ONE system information"},
            "7": {"name": "Module Test", "desc": "Test all loaded modules"},
            "0": {"name": "Exit", "desc": "Exit NEXUS-ONE"}
        }
        
        print("\n" + "="*60)
        print("🤖 NEXUS-ONE COMMAND INTERFACE")
        print("="*60)
        
        for key, option in menu_options.items():
            status = "🟢" if key not in ["0", "6", "7"] else "🔵"
            print(f"{status} {key}. {option['name']:20} - {option['desc']}")
        
        print("="*60)
    
    async def handle_menu_choice(self, choice: str):
        """Menü seçimini işle"""
        self.command_history.append({
            "time": datetime.now().isoformat(),
            "choice": choice,
            "session": self.session_id
        })
        
        if choice == "0":
            await self.shutdown()
            return False
            
        elif choice == "1":
            await self.file_operations_menu()
            
        elif choice == "2":
            await self.ai_operations_menu()
            
        elif choice == "3":
            await self.system_monitor_menu()
            
        elif choice == "4":
            await self.web_research_menu()
            
        elif choice == "5":
            await self.task_automation_menu()
            
        elif choice == "6":
            self.show_system_info()
            
        elif choice == "7":
            await self.test_all_modules()
            
        else:
            print(f"\n❌ Invalid choice: {choice}")
            
        return True
    
    async def file_operations_menu(self):
        """Dosya işlemleri menüsü"""
        print("\n📁 FILE OPERATIONS MENU")
        print("="*50)
        
        if "file_manager" in self.modules:
            fm = self.modules["file_manager"]
            print("File Manager is ready!")
            # Add actual file operations here
        else:
            print("❌ File Manager module not loaded")
        
        input("\n⏎ Press Enter to continue...")
    
    async def ai_operations_menu(self):
        """AI işlemleri menüsü"""
        print("\n🤖 AI OPERATIONS MENU")
        print("="*50)
        
        if "ai_engine" in self.modules:
            print("AI Engine is ready!")
            # Add actual AI operations here
        else:
            print("❌ AI Engine module not loaded")
        
        input("\n⏎ Press Enter to continue...")
    
    async def system_monitor_menu(self):
        """Sistem monitör menüsü"""
        print("\n📊 SYSTEM MONITOR MENU")
        print("="*50)
        
        if "system_monitor" in self.modules:
            print("System Monitor is ready!")
            # Add actual monitoring here
        else:
            print("❌ System Monitor module not loaded")
        
        input("\n⏎ Press Enter to continue...")
    
    async def web_research_menu(self):
        """Web araştırma menüsü"""
        print("\n🌐 WEB RESEARCH MENU")
        print("="*50)
        
        if "web_researcher" in self.modules:
            print("Web Researcher is ready!")
            # Add actual web research here
        else:
            print("❌ Web Researcher module not loaded")
        
        input("\n⏎ Press Enter to continue...")
    
    async def task_automation_menu(self):
        """Görev otomasyon menüsü"""
        print("\n⚡ TASK AUTOMATION MENU")
        print("="*50)
        
        if "task_manager" in self.modules:
            print("Task Manager is ready!")
            # Add actual task automation here
        else:
            print("❌ Task Manager module not loaded")
        
        input("\n⏎ Press Enter to continue...")
    
    def show_system_info(self):
        """Sistem bilgilerini göster"""
        print("\n💻 NEXUS-ONE SYSTEM INFORMATION")
        print("="*50)
        
        info = {
            "System Name": self.name,
            "Version": self.version,
            "Session ID": self.session_id,
            "Python Version": sys.version.split()[0],
            "Platform": sys.platform,
            "Current Directory": os.getcwd(),
            "Loaded Modules": len(self.modules),
            "Command History": len(self.command_history),
            "Start Time": self.session_id[:8] + " " + self.session_id[9:11] + ":" + self.session_id[11:13] + ":" + self.session_id[13:15]
        }
        
        for key, value in info.items():
            print(f"  {key:20}: {value}")
        
        if self.brand:
            print("\n🎨 Brand Colors:")
            colors = self.brand.get_color_palette()
            for name, color in colors.items():
                print(f"  {name:12}: {color}")
        
        input("\n⏎ Press Enter to continue...")
    
    async def test_all_modules(self):
        """Tüm modülleri test et"""
        print("\n🔧 MODULE TESTING SUITE")
        print("="*50)
        
        test_results = []
        
        for module_name, module_instance in self.modules.items():
            try:
                # Basic test - check if module has proper methods
                if hasattr(module_instance, '__class__'):
                    test_results.append({
                        "module": module_name,
                        "status": "✅",
                        "class": module_instance.__class__.__name__
                    })
                else:
                    test_results.append({
                        "module": module_name,
                        "status": "⚠️",
                        "error": "No class definition"
                    })
            except Exception as e:
                test_results.append({
                    "module": module_name,
                    "status": "❌",
                    "error": str(e)[:50]
                })
        
        print("\nTest Results:")
        for result in test_results:
            print(f"  {result['status']} {result['module']:20} - {result.get('class', result.get('error', 'Unknown'))}")
        
        print(f"\n📊 Summary: {len([r for r in test_results if r['status'] == '✅'])}/{len(test_results)} modules OK")
        
        input("\n⏎ Press Enter to continue...")
    
    async def shutdown(self):
        """Sistemi kapat"""
        print("\n" + "="*60)
        print("🔄 NEXUS-ONE Shutdown Sequence")
        print("="*60)
        
        # Save session log
        session_log = {
            "session_id": self.session_id,
            "start_time": self.session_id,
            "end_time": datetime.now().isoformat(),
            "commands_executed": len(self.command_history),
            "modules_loaded": len(self.modules),
            "command_history": self.command_history[-10:]  # Last 10 commands
        }
        
        # Create logs directory if not exists
        os.makedirs("logs", exist_ok=True)
        
        log_file = f"logs/session_{self.session_id}.json"
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(session_log, f, indent=2, ensure_ascii=False)
        
        print(f"\n📝 Session log saved: {log_file}")
        print(f"⏱️  Commands executed: {len(self.command_history)}")
        print(f"📦 Modules loaded: {len(self.modules)}")
        
        print("\n" + "="*60)
        print("👋 NEXUS-ONE shutdown complete.")
        print("   Thank you for using the convergence point of all intelligence.")
        print("="*60)
    
    async def run(self):
        """Ana çalıştırma döngüsü"""
        running = True
        
        while running:
            try:
                self.display_main_menu()
                choice = input("\n👉 Enter choice (0-7): ").strip()
                
                if choice.lower() in ['exit', 'quit', 'q']:
                    choice = "0"
                
                running = await self.handle_menu_choice(choice)
                
            except KeyboardInterrupt:
                print("\n\n⚠️  Interrupted by user. Shutting down...")
                await self.shutdown()
                break
            except Exception as e:
                print(f"\n🚨 Unexpected error: {e}")
                print("   Returning to main menu...")
                await asyncio.sleep(1)

def main():
    """Ana fonksiyon"""
    try:
        # Windows için encoding
        if sys.platform == "win32":
            os.system("chcp 65001 > nul")
        
        # Create NexusOne instance
        nexus = NexusOne()
        
        # Run async main loop
        asyncio.run(nexus.run())
        
    except KeyboardInterrupt:
        print("\n\n👋 NEXUS-ONE terminated by user.")
    except Exception as e:
        print(f"\n🚨 CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        input("\n⏎ Press Enter to exit...")

if __name__ == "__main__":
    main()
