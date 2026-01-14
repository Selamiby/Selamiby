"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:20
🚀 Status: ACTIVE / PRODUCTION
"""

import os
import sys
import unittest
from pathlib import Path

# Set workspace root
WORKSPACE = Path("c:/Users/selam/NEXUS-ONE")
sys.path.append(str(WORKSPACE))

class TestNexusSovereignV3(unittest.TestCase):
    def test_01_production_layers(self):
        """Üretim katmanlarının mevcudiyetini ve temel importlarını test eder."""
        print("\n[TEST]: Üretim katmanları kontrol ediliyor...")
        layers = ["nexus_layer_combat.py", "nexus_layer_economy.py", "nexus_layer_unique.py", "nexus_layer_architecture.py"]
        for layer in layers:
            path = WORKSPACE / "production" / layer
            self.assertTrue(path.exists(), f"Layer missing: {layer}")
            print(f"  - {layer}: OK")

    def test_02_ecs_kernel(self):
        """Sovereign ECS mimarisinin çalışabilirliğini test eder."""
        print("[TEST]: ECS Çekirdek testi başlatılıyor...")
        from production.nexus_layer_architecture import (AIControl,
                                                         EntityManager,
                                                         Position)
        kernel = EntityManager()
        entity = kernel.create_entity()
        entity.add(Position(10, 20, 30))
        self.assertIsNotNone(entity.get(Position))
        self.assertEqual(entity.get(Position).x, 10)
        print("  - ECS Kernel Integrity: OK")

    def test_03_visual_master_syntax(self):
        """Görsel motorun dosya yapısını ve sözdizimini test eder."""
        print("[TEST]: Görsel motor (Visual Master) sözdizimi kontrolü...")
        import py_compile
        visual_path = WORKSPACE / "visuals" / "visual_master.py"
        try:
            py_compile.compile(str(visual_path), doraise=True)
            print("  - Visual Master Syntax: OK")
        except Exception as e:
            self.fail(f"Visual Master syntax error: {e}")

    def test_04_config_integrity(self):
        """Config dosyasının geçerliliğini test eder."""
        print("[TEST]: Config dosyası kontrolü...")
        config_path = WORKSPACE / "nexus_one_config.json"
        import json
        with open(config_path, 'r') as f:
            data = json.load(f)
            self.assertIn("economy", data)
        print("  - Config Integrity: OK")

if __name__ == "__main__":
    print("\n" + "="*50)
    print("--- NEXUS V3 INTEGRATION TEST (PRE-LAUNCH) ---")
    print("="*50)
    
    # Run tests
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNexusSovereignV3)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    
    if result.wasSuccessful():
        print("\n✅ TÜM TESTLER BAŞARILI. SİSTEM OTOMATİK BAŞLATILIYOR...")
        sys.exit(0)
    else:
        print("\n❌ TESTLER BAŞARISIZ. SİSTEMİ KONTROL EDİN.")
        sys.exit(1)
