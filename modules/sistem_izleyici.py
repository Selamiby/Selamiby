# modules/sistem_izleyici.py
import psutil

class SistemIzleyici:
    def calis(self, gorev=""):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        return f"CPU: %{cpu}, RAM: %{ram}"
