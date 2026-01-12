# robotics_controller.py
class RoboticsController:
    def send_command(self, device, command):
        responses = {
            "move": f"🤖 {device} hareket ediyor: {command}",
            "scan": f"🔍 {device} tarama yapıyor...",
            "collect": f"📦 {device} veri topluyor...",
            "return": f"↩️ {device} geri dönüyor",
        }
        return responses.get(command, f"✅ {device}: {command} tamamlandı")

    def autonomous_mission(self, mission_type):
        return f"🚀 {mission_type} görevi başlatıldı (simülasyon)"
