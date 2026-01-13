import json
import os
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="NEXUS-ONE Command Center", layout="wide", page_icon="🚀")

st.title("🚀 NEXUS-ONE | Master Command Center")
st.markdown("---")

# Sidebar - System Status
st.sidebar.header("📡 Sistem Durumu")
metrics_path = Path("nexus_logs/learner_metrics.json")
if metrics_path.exists():
    with open(metrics_path, "r", encoding="utf-8") as f:
        metrics = json.load(f)

    st.sidebar.metric("Öğrenme Döngüsü", metrics.get("learning_cycles", 0))
    st.sidebar.metric("Toplam Modül", metrics.get("total_topics_learned", 0))
    st.sidebar.progress(min(metrics.get("total_topics_learned", 0) / 1000, 1.0), text="Mastery Progress")

# Main Dashboard
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🛠️ Son Üretilen Varlıklar (Real Assets)")
    asset_dir = Path("nexus_real_assets")
    if asset_dir.exists():
        files = sorted(asset_dir.glob("*"), key=os.path.getmtime, reverse=True)
        if files:
            for file in files[:5]:
                with st.expander(f"📁 {file.name}"):
                    if file.suffix.lower() in [".png", ".jpg", ".jpeg"]:
                        st.image(str(file))
                    elif file.suffix.lower() in [".mp3", ".wav"]:
                        st.audio(str(file))
                    elif file.suffix.lower() in [".glb", ".obj"]:
                        st.write(f"3D Model File: {file.name} (Download to view in 3D)")
                        with open(file, "rb") as f:
                            st.download_button("İndir", f, file_name=file.name)
        else:
            st.info("Henüz gerçek varlık üretilmedi.")

    st.header("📚 Son Öğrenilen Konular")
    journal_path = Path("NEXUS_JOURNAL.md")
    if journal_path.exists():
        st.markdown(journal_path.read_text(encoding="utf-8")[-2000:])
    else:
        st.info("Günlük henüz boş.")

with col2:
    st.header("🎯 Hızlı Komut Merkezi")
    with st.form("generate_asset"):
        st.subheader("Varlık Üret")
        target = st.selectbox("Tür", ["Görsel (Flux Pro)", "3D Model (TripoSR)", "Ses (Stable Audio)"])
        prompt = st.text_area("Ne üretilsin?", placeholder="Örn: Cyberpunk bir sokak lambası, 8k, low poly...")
        submit = st.form_submit_button("Üretimi Başlat")

        if submit and prompt:
            st.warning("Üretim başlatıldı, lütfen bekleyin...")
            from nexus_real_asset_factory import NexusAssetFactory
            factory = NexusAssetFactory()

            if "Görsel" in target:
                res = factory.generate_image(prompt)
            elif "3D" in target:
                res = factory.generate_3d_model(prompt)
            else:
                res = factory.generate_audio(prompt)

            if res:
                st.success(f"Başarıyla üretildi: {res}")
                st.rerun()
            else:
                st.error("Üretim sırasında bir hata oluştu. API anahtarlarını kontrol edin.")

    st.header("⚙️ Otonom Kontrol")
    if st.button("Sistemi Yeniden Başlat"):
        st.info("Yeniden başlatma komutu gönderildi...")

st.markdown("---")
st.caption("NEXUS-ONE | Autonomous Development Environment | 2026")
