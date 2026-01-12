# autonomous_updater.py
import os
import subprocess
import sys
from pathlib import Path

import git


class SelfUpdater:
    def __init__(self):
        # Projenin kök dizinini bul
        self.repo_path = Path(__file__).parent.parent.parent

    def check_for_updates(self):
        """Uzak repoyu kontrol ederek güncelleme olup olmadığını döndürür."""
        try:
            print("🔎 Güncellemeler kontrol ediliyor...")
            repo = git.Repo(self.repo_path)
            origin = repo.remotes.origin
            origin.fetch()

            local_hash = repo.head.commit.hexsha
            remote_hash = (
                repo.remotes.origin.refs.main.commit.hexsha
            )  # 'main' branch'i varsayılan

            if local_hash != remote_hash:
                print("💡 Yeni bir güncelleme bulundu!")
                return True
            else:
                print("✅ Sistem güncel.")
                return False
        except Exception as e:
            print(f"⚠️ Güncelleme kontrolü başarısız: {e}")
            return False

    def update_self(self):
        """Projeyi günceller, bağımlılıkları kurar ve yeniden başlatır."""
        try:
            repo = git.Repo(self.repo_path)
            origin = repo.remotes.origin
            print("⏬ Güncellemeler indiriliyor...")
            origin.pull()
            print("✅ Kod başarıyla güncellendi.")

            # Bağımlılıkları güncelle
            print("📦 Bağımlılıklar güncelleniyor...")
            requirements_path = self.repo_path / "requirements.txt"
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "--upgrade",
                    "-r",
                    str(requirements_path),
                ],
                check=True,
            )
            print("✅ Bağımlılıklar güncellendi.")

            # Kendini yeniden başlat
            print("🔄 Sistem yeniden başlatılıyor...")
            os.execv(sys.executable, ["python"] + sys.argv)

        except Exception as e:
            print(f"❌ Güncelleme sırasında kritik hata: {e}")
            # Hata durumunda yeniden başlatmayı denememek için çık
            sys.exit(1)
