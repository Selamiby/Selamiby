import json
import logging
import os
from pathlib import Path

import fal_client
import requests
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] 🎨 FACTORY: %(message)s")
logger = logging.getLogger("AssetFactory")

class NexusAssetFactory:
    """
    NEXUS-ONE Real Asset Production Line.
    Generates REAL 3D models, textures, images, and audio using FAL.AI and OpenAI.
    """
    def __init__(self):
        self.fal_key = os.getenv("FAL_AI_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.output_dir = Path("nexus_real_assets")
        self.output_dir.mkdir(exist_ok=True)

        if self.fal_key:
            os.environ["FAL_KEY"] = self.fal_key

    def generate_image(self, prompt: str, filename: str = None) -> str:
        """Sıfırdan gerçek, yüksek kaliteli görsel/dokur (texture) üretir."""
        if not self.fal_key:
            return "Error: FAL_AI_API_KEY missing."

        logger.info(f"🖼️ Görsel üretiliyor: {prompt}")
        try:
            handler = fal_client.submit(
                "fal-ai/flux/pro",
                arguments={
                    "prompt": f"Professional high-quality asset, {prompt}, highly detailed, 8k",
                    "image_size": "landscape_16_9"
                },
            )
            result = handler.get()
            image_url = result['images'][0]['url']

            # Download image
            if not filename:
                filename = f"img_{os.urandom(4).hex()}.png"

            filepath = self.output_dir / filename
            response = requests.get(image_url)
            with open(filepath, "wb") as f:
                f.write(response.content)

            logger.info(f"✅ Görsel başarıyla kaydedildi: {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Görsel üretim hatası: {e}")
            return None

    def generate_3d_model(self, prompt: str, filename: str = None) -> str:
        """Sıfırdan gerçek 3D model (GLB/OBJ) üretir - SİMÜLASYON DEĞİLDİR."""
        if not self.fal_key:
            return "Error: FAL_AI_API_KEY missing."

        logger.info(f"🧊 3D Model üretiliyor: {prompt}")
        try:
            # TripoSR or similar 3D model generation
            handler = fal_client.submit(
                "fal-ai/tripo-sr",
                arguments={
                    "prompt": prompt
                },
            )
            result = handler.get()
            # Note: Result format depends on model, usually a URL to a .glb
            model_url = result.get('model_mesh', {}).get('url')

            if not model_url:
                logger.warning("FAL 3D model URL'i dönmedi, fallback yapılıyor.")
                return None

            if not filename:
                filename = f"model_{os.urandom(4).hex()}.glb"

            filepath = self.output_dir / filename
            response = requests.get(model_url)
            with open(filepath, "wb") as f:
                f.write(response.content)

            logger.info(f"✅ 3D Model başarıyla kaydedildi: {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"3D Model üretim hatası: {e}")
            return None

    def generate_audio(self, prompt: str, filename: str = None) -> str:
        """Sıfırdan gerçek ses efekti veya müzik üretir."""
        if not self.fal_key:
            return "Error: FAL_AI_API_KEY missing."

        logger.info(f"🎵 Ses üretiliyor: {prompt}")
        try:
            handler = fal_client.submit(
                "fal-ai/stable-audio",
                arguments={
                    "prompt": prompt,
                    "seconds_total": 10
                },
            )
            result = handler.get()
            audio_url = result['audio']['url']

            if not filename:
                filename = f"audio_{os.urandom(4).hex()}.mp3"

            filepath = self.output_dir / filename
            response = requests.get(audio_url)
            with open(filepath, "wb") as f:
                f.write(response.content)

            logger.info(f"✅ Ses dosyası kaydedildi: {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Ses üretim hatası: {e}")
            return None

if __name__ == "__main__":
    # Test
    factory = NexusAssetFactory()
    # factory.generate_image("A futuristic cyberpunk city gate", "gate.png")
