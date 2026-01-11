import logging
import smtplib
from typing import Optional


class ErrorHandler:
    def __init__(self, alert_email: Optional[str] = None, smtp_server: Optional[str] = None):
        self.logger = logging.getLogger("AETHEROS_ERROR_HANDLER")
        self.logger.setLevel(logging.ERROR)
        handler = logging.FileHandler("logs/error.log")
        handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
        self.logger.addHandler(handler)
        self.alert_email = alert_email
        self.smtp_server = smtp_server

    def handle(self, exc: Exception, context: Optional[str] = None):
        msg = f"[ERROR] {context or ''}: {exc}"
        self.logger.error(msg)
        self.send_alert(msg)
        # Otomatik kurtarma stratejileri burada uygulanabilir

    def send_alert(self, message: str):
        if self.alert_email and self.smtp_server:
            try:
                with smtplib.SMTP(self.smtp_server) as server:
                    server.sendmail(
                        from_addr=self.alert_email,
                        to_addrs=[self.alert_email],
                        msg=f"Subject: AETHEROS ERROR\n\n{message}"
                    )
            except Exception as e:
                self.logger.error(f"Alert gönderilemedi: {e}")

    def classify(self, exc: Exception) -> str:
        # Basit hata sınıflandırma
        if isinstance(exc, FileNotFoundError):
            return "FileError"
        elif isinstance(exc, ConnectionError):
            return "NetworkError"
        elif isinstance(exc, ValueError):
            return "ValueError"
        return "GeneralError"

    def recover(self, exc: Exception):
        # Otomatik kurtarma stratejileri örneği
        if isinstance(exc, FileNotFoundError):
            # Eksik dosya için otomatik oluşturma
            pass
        elif isinstance(exc, ConnectionError):
            # Ağ bağlantısı tekrar dene
            pass
        # ...
        # ...
        # ...
