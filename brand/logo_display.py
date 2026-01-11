"""
NEXUS-ONE Logo Display Module
"""
import os
import sys
from pathlib import Path
from typing import Optional
import json

class NexusBrand:
    """NEXUS-ONE marka ve logo yönetimi"""
    
    def __init__(self):
        self.brand_data = self._load_brand_data()
        self.logo_path = Path(__file__).parent / "logos"
        
    def _load_brand_data(self) -> dict:
        """Marka verilerini yükle"""
        return {
            "name": "NEXUS-ONE",
            "version": "1.0.0",
            "slogan": "Where All Intelligence Converges",
            "colors": {
                "primary": "#0A74DA",
                "secondary": "#00D4AA",
                "accent": "#FF6B9D",
                "dark": "#0A0A1E",
                "light": "#F0F4FF"
            },
            "fonts": {
                "primary": "Inter",
                "secondary": "JetBrains Mono",
                "display": "Orbitron"
            },
            "logo_variants": ["full_color", "monochrome", "icon_only", "animated"]
        }
    
    def display_ascii_logo(self) -> str:
        """ASCII logo göster"""
        ascii_logo = r"""
        ╔╗╔╦╗╔╦╗╔═╗╦ ╦╔═╗  ╔═╗╔╗╔╔═╗╔╦╗
        ║║║║║ ║║╠═╝║ ║╚═╗  ║ ║║║║╚═╗ ║ 
        ╝╚╝╩╩═╝╩╩  ╚═╝╚═╝  ╚═╝╝╚╝╚═╝ ╩ 
        
        ╔══════════════════════════════════════╗
        ║     Autonomous AI Operating System   ║
        ║      Where All Intelligence Converges║
        ╚══════════════════════════════════════╝
        """
        return ascii_logo
    
    def display_rich_logo(self):
        """Zengin formatlı logo göster (rich kütüphanesi ile)"""
        try:
            from rich.console import Console
            from rich.panel import Panel
            from rich.text import Text
            from rich.box import ROUNDED
            
            console = Console()
            
            # Renkli logo
            logo_text = Text()
            logo_text.append("╔╗╔╦╗╔╦╗╔═╗╦ ╦╔═╗  ╔═╗╔╗╔╔═╗╔╦╗\n", style="bold cyan")
            logo_text.append("║║║║║ ║║╠═╝║ ║╚═╗  ║ ║║║║╚═╗ ║ \n", style="bold blue")
            logo_text.append("╝╚╝╩╩═╝╩╩  ╚═╝╚═╝  ╚═╝╝╚╝╚═╝ ╩ \n", style="bold cyan")
            
            panel = Panel(
                logo_text,
                title="[bold #00D4AA]NEXUS-ONE[/bold #00D4AA]",
                subtitle="[italic #FF6B9D]Where All Intelligence Converges[/italic #FF6B9D]",
                box=ROUNDED,
                border_style="#0A74DA",
                padding=(1, 2)
            )
            
            console.print(panel)
            
        except ImportError:
            # Fallback to ASCII
            print(self.display_ascii_logo())
    
    def get_color_palette(self) -> dict:
        """Renk paletini getir"""
        return self.brand_data["colors"]
    
    def generate_welcome_message(self) -> str:
        """Karşılama mesajı oluştur"""
        import platform
        from datetime import datetime
        
        system_info = {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "python": platform.python_version(),
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        welcome = f"""
        ┌─────────────────────────────────────────────────────┐
        │  [NEXUS-ONE v{self.brand_data['version']}] Initializing...        │
        │  System: {system_info['system']} {system_info['release']} ({system_info['machine']})  │
        │  Python: {system_info['python']}                              │
        │  Time: {system_info['time']}                          │
        │                                                     │
        │  "Where All Intelligence Converges"                 │
        └─────────────────────────────────────────────────────┘
        """
        
        return welcome
    
    def save_logo_info(self, filepath: str):
        """Logo bilgilerini JSON olarak kaydet"""
        info = {
            "brand": self.brand_data,
            "logo_files": {
                "full_logo": str(self.logo_path / "nexus_logo.svg"),
                "icon": str(self.logo_path / "nexus_icon.svg"),
                "ascii": self.display_ascii_logo()
            },
            "usage": {
                "python": "from brand.logo_display import NexusBrand",
                "display": "NexusBrand().display_rich_logo()",
                "colors": "NexusBrand().get_color_palette()"
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def print_color_samples():
        """Renk örneklerini göster"""
        colors = {
            "Primary (#0A74DA)": "\033[38;2;10;116;218m█\033[0m Nexus Blue",
            "Secondary (#00D4AA)": "\033[38;2;0;212;170m█\033[0m Quantum Teal", 
            "Accent (#FF6B9D)": "\033[38;2;255;107;157m█\033[0m Spark Pink",
            "Dark (#0A0A1E)": "\033[38;2;10;10;30m█\033[0m Deep Space",
            "Light (#F0F4FF)": "\033[38;2;240;244;255m█\033[0m Cosmic Mist"
        }
        
        print("\n🎨 NEXUS-ONE Color Palette:")
        print("═" * 50)
        for name, sample in colors.items():
            print(f"  {sample}")

# Terminalde test
if __name__ == "__main__":
    brand = NexusBrand()
    
    print("\n" + "="*60)
    brand.display_rich_logo()
    print("\n" + "="*60)
    
    print(brand.generate_welcome_message())
    
    brand.print_color_samples()
    
    # Logo bilgilerini kaydet
    brand.save_logo_info("brand/logo_info.json")
    print("\n✅ Logo information saved to brand/logo_info.json")
