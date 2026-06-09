import streamlit as st
import os
import json

st.title("🔍 Ispezione File di Sistema Live")

if os.path.exists("scelte_fedelissimi.json"):
    st.success("✅ Il file esiste sul server! Ecco il contenuto reale:")
    with open("scelte_fedelissimi.json", "r") as f:
        dati = json.load(f)
    st.json(dati)
else:
    st.warning("⚠️ Il file 'scelte_fedelissimi.json' non è ancora stato creato o è vuoto.")

if st.button("🔄 Aggiorna Pagina"):
    st.rerun()
