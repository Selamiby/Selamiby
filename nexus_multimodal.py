#!/usr/bin/env python3
"""
NEXUS-ONE Multimodal Utils
- Optional OCR for images (pytesseract + Pillow)
- Optional audio transcription (speech_recognition)
Gracefully degrades if deps not installed.
"""
from pathlib import Path
from typing import Any, Dict

# Lazy imports
try:
    from PIL import Image
except Exception:
    Image = None

try:
    import pytesseract
except Exception:
    pytesseract = None

try:
    import speech_recognition as sr
except Exception:
    sr = None


def analyze_image(path: Path) -> Dict[str, Any]:
    """Run lightweight analysis + OCR if available."""
    info: Dict[str, Any] = {"path": str(path), "ok": False}
    try:
        if not path.exists():
            info["error"] = "file not found"
            return info
        if not Image:
            info["error"] = "Pillow not installed"
            return info

        img = Image.open(path)
        info.update(
            {
                "ok": True,
                "size": img.size,
                "mode": img.mode,
            }
        )

        if pytesseract:
            try:
                text = pytesseract.image_to_string(img)
                info["ocr_text"] = text[:500]
            except Exception as e:
                info["ocr_error"] = str(e)
        else:
            info["ocr_error"] = "pytesseract not installed"
    except Exception as e:
        info["error"] = str(e)
    return info


def transcribe_audio(path: Path) -> Dict[str, Any]:
    """Transcribe audio if speech_recognition is available."""
    info: Dict[str, Any] = {"path": str(path), "ok": False}
    try:
        if not path.exists():
            info["error"] = "file not found"
            return info
        if not sr:
            info["error"] = "speech_recognition not installed"
            return info

        recognizer = sr.Recognizer()
        with sr.AudioFile(str(path)) as source:
            audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio, language="tr-TR")
            info["ok"] = True
            info["transcript"] = text
        except Exception as e:
            info["error"] = str(e)
    except Exception as e:
        info["error"] = str(e)
    return info


if __name__ == "__main__":
    from pprint import pprint

    print("Multimodal utils ready. Run analyze_image(Path) or transcribe_audio(Path)")
