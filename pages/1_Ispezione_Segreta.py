import streamlit as st
import os
import json

st.set_page_config(page_title="Ispezione Live", layout="wide")
st.title("🔍 Ispezione File di Sistema Live")

# Controlliamo la cartella principale e i file presenti
st.write("### 📁 Elenco dei file attualmente salvati sul server:")
file_presenti = os.listdir('.')
st.write(file_presenti)

st.markdown("---")

# Tentativo di lettura del file delle scelte
nome_file = "scelte_fedelissimi.json"
if os.path.exists(nome_file):
    st.success(f"✅ Il file '{nome_file}' ESISTE sul server! Ecco i dati salvati dai ragazzi:")
    try:
        with open(nome_file, "r") as f:
            dati = json.load(f)
        st.json(dati)
    except Exception as e:
        st.error(f"Errore nella lettura del JSON: {e}")
else:
    st.warning(f"⚠️ Il file '{nome_file}' non è presente in questa directory.")

st.markdown("---")

# Controlliamo se ci sono file delle buste chiuse
st.write("### ✉️ Controllo file Buste (.json):")
buste = [f for f in file_presenti if f.startswith("busta_")]
if buste:
    st.success(f"Trovate {len(buste)} buste sigillate sul server.")
    st.write(buste)
else:
    st.info("Nessun file busta_...json trovato al momento.")
