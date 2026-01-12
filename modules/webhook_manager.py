from typing import Dict, List

import requests


class WebhookManager:
    """
    Webhook kayıt ve tetikleme altyapısı.
    """

    def __init__(self):
        self.webhooks: List[str] = []

    def register(self, url: str):
        if url not in self.webhooks:
            self.webhooks.append(url)

    def unregister(self, url: str):
        if url in self.webhooks:
            self.webhooks.remove(url)

    def notify(self, event: str, data: Dict):
        payload = {"event": event, "data": data}
        for url in self.webhooks:
            try:
                requests.post(url, json=payload, timeout=3)
            except Exception:
                pass
            except Exception:
                pass
            except Exception:
                pass
