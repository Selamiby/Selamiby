import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

import pandas as pd
import psutil
import streamlit as st
from streamlit_ace import st_ace
from streamlit_agraph import Config, Edge, Node, agraph

from nexus_brain import NexusBrain

# Page Config
st.set_page_config(page_title="NEXUS-ONE Command Center v3", layout="wide", page_icon="🧠")

# Brain Instance
brain = NexusBrain()

# Session State for Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Paths
WORKSPACE = Path(os.getcwd())
MODULES_DIR = WORKSPACE / "nexus_modules"
ASSETS_DIR = WORKSPACE / "nexus_real_assets"
KNOWLEDGE_DIR = WORKSPACE / "infinite_knowledge"
LOGS_DIR = WORKSPACE / "nexus_logs"
JOURNAL_PATH = WORKSPACE / "NEXUS_JOURNAL.md"

# Sidebar - System Health & Quick Actions
with st.sidebar:
    st.header("⚡ NEXUS-ONE BIOS")
    cpu_usage = psutil.cpu_percent()
    mem_usage = psutil.virtual_memory().percent
    st.write(f"CPU: {cpu_usage}%")
    st.progress(cpu_usage / 100)
    st.write(f"RAM: {mem_usage}%")
    st.progress(mem_usage / 100)
    
    st.divider()
    
    st.subheader("🤖 Human Feedback")
    feedback = st.text_area("Yapay Zekaya Talimat Ver:", placeholder="Örn: Daha fazla siber güvenlik çalış...")
    if st.button("Talimatı Gönder"):
        with open(LOGS_DIR / "human_instructions.txt", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().isoformat()}] {feedback}\n")
        st.success("Talimat sisteme iletildi.")

# Main Navigation
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Dashboard", 
    "🕸️ Neural Net", 
    "📝 Code Editor", 
    "💬 Sohbet",
    "💻 Terminal", 
    "📂 System Logs"
])

# Tab 1: Dashboard
with tab1:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.header("🚀 Üretim Hattı")
        if ASSETS_DIR.exists():
            files = sorted(ASSETS_DIR.glob("*"), key=os.path.getmtime, reverse=True)
            if files:
                for file in files[:3]:
                    with st.expander(f"📁 Asset: {file.name}"):
                        if file.suffix.lower() in [".png", ".jpg", ".jpeg"]:
                            st.image(str(file))
                        elif file.suffix.lower() in [".mp3", ".wav"]:
                            st.audio(str(file))
                        else: st.write(f"Binary: {file.name}")
            else:
                st.info("Henüz varlık üretilmedi.")
        
        st.divider()
        st.header("📘 Son Analizler")
        if JOURNAL_PATH.exists():
            content = JOURNAL_PATH.read_text(encoding="utf-8")
            st.markdown(content[-5000:] if len(content) > 5000 else content)
            
    with col2:
        st.header("🎯 Anlık Üretim")
        target = st.selectbox("Tür", ["Görsel", "3D Model", "Ses"])
        prompt = st.text_input("Prompt:", key="instant_prompt")
        if st.button("Hızlı Üret"):
            from nexus_real_asset_factory import NexusAssetFactory
            factory = NexusAssetFactory()
            with st.spinner("Üretiliyor..."):
                if target == "Görsel": res = factory.generate_image(prompt)
                elif target == "3D Model": res = factory.generate_3d_model(prompt)
                else: res = factory.generate_audio(prompt)
                
                if res:
                    st.success(f"Başarıyla üretildi: {res}")
                    st.rerun()
                else:
                    st.error("Hata oluştu.")

# Tab 2: Neural Net (Graphs)
with tab2:
    st.header("🕸️ Bilgi Sinir Ağı")
    nodes = []
    edges = []
    
    # Root Node
    nodes.append(Node(id="NEXUS", label="NEXUS-ONE", size=400, color="#FF4B4B"))
    
    # Domain Nodes & Topic Nodes
    if KNOWLEDGE_DIR.exists():
        knowledge_files = list(KNOWLEDGE_DIR.glob("*.json"))[:40] 
        domains = set()
        for kf in knowledge_files:
            try:
                data = json.loads(kf.read_text(encoding="utf-8"))
                domain = data.get("domain", "Unknown")
                topic = data.get("topic", "Topic")
                
                if domain not in domains:
                    nodes.append(Node(id=domain, label=domain, color="#667eea", size=300))
                    edges.append(Edge(source="NEXUS", target=domain))
                    domains.add(domain)
                
                nodes.append(Node(id=topic, label=topic, size=150, color="#10b981"))
                edges.append(Edge(source=domain, target=topic))
            except: continue
            
    config = Config(width=1200, height=800, directed=True, nodeHighlightBehavior=True, highlightColor="#F7A7A6", collapsible=True)
    agraph(nodes=nodes, edges=edges, config=config)

# Tab 3: Code Editor
with tab3:
    st.header("📝 Modül Editörü")
    if MODULES_DIR.exists():
        module_files = [f.name for f in MODULES_DIR.glob("*.py")]
        selected_file = st.selectbox("Düzenlenecek Modül:", module_files)
        if selected_file:
            file_path = MODULES_DIR / selected_file
            content = file_path.read_text(encoding="utf-8")
            
            st.subheader(f"Düzenleniyor: {selected_file}")
            new_code = st_ace(value=content, language="python", theme="monokai", height=500, key="ace_editor")
            
            if st.button("Kaydet ve Uygula"):
                file_path.write_text(new_code, encoding="utf-8")
                st.success(f"{selected_file} güncellendi ve otonom sisteme işlendi!")

# Tab 4: Sohbet
with tab4:
    st.header("💬 NEXUS-ONE Sohbet")
    
    # History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input
    if prompt := st.chat_input("NEXUS-ONE ile konuş..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Düşünüyorum..."):
                response = brain.think(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

# Tab 5: Terminal
with tab5:
    st.header("💻 Otonom Terminal")
    cmd = st.text_input("Komut Çalıştır (PowerShell):", placeholder="dir, python nexus_one.py, etc...")
    if st.button("Çalıştır"):
        try:
            result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
            if result.stdout:
                st.code(result.stdout)
            if result.stderr:
                st.error(result.stderr)
        except Exception as e:
            st.error(f"Hata: {e}")

# Tab 6: System Logs
with tab6:
    st.header("📂 Log İzleyici")
    log_files = sorted(list(LOGS_DIR.glob("*.log")) + list(LOGS_DIR.glob("*.txt")), key=os.path.getmtime, reverse=True)
    selected_log = st.selectbox("Log Dosyası Seç:", [f.name for f in log_files])
    if selected_log:
        log_content = (LOGS_DIR / selected_log).read_text(encoding="utf-8")
        st.text_area("Son Kayıtlar", log_content[-10000:] if len(log_content) > 10000 else log_content, height=600)

st.divider()
st.caption("NEXUS-ONE | Advanced Command Center v3.0 | 2026")
