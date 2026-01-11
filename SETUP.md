# 1. Yeni bir dizin oluşturun
mkdir nexus_project && cd nexus_project

# 2. Sanal ortam kurun
python -m venv .venv

# 3. Aktif edin ve Nexus'u çalıştırın
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate

# 4. Paketleri kurun
pip install psutil requests
