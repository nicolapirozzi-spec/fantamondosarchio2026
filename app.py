import streamlit as st
import pandas as pd
import os
import json
import math

st.set_page_config(page_title="FantaMondosarchio2026", layout="wide", page_icon="⚽")

# --- DATABASE UTENTI ---
UTENTI = {
    "dorindo": {"squadra": "AVELLINO", "nome": "Dorindo", "priorita": 1, "admin": False},
    "emilio": {"squadra": "LOS POLLOS HMN", "nome": "Emilio", "priorita": 2, "admin": False},
    "michelangelo": {"squadra": "EL RIGORITA", "nome": "Michelangelo", "priorita": 3, "admin": False},
    "fabio": {"squadra": "AS BULLA", "nome": "Fabio", "priorita": 4, "admin": False},
    "nicola": {"squadra": "OGGETTIVAMENTE", "nome": "Nicola", "priorita": 5, "admin": True}, # ADMIN
    "salvatore": {"squadra": "MEME MASTER FC", "nome": "Salvatore", "priorita": 6, "admin": False},
    "carmine": {"squadra": "MIDISSOCIO", "nome": "Carmine", "priorita": 7, "admin": False}
}

TOP_PLAYERS = {
    "D": ["DUMFRIES", "MENDES", "HAKIMI", "VAN DIJK", "MARQUINHOS", "THEO", "CANCELO"],
    "C": ["OLISE", "BELLINGHAM", "MUSIALA", "DOKU", "FERNANDES", "PEDRI", "OLMO"],
    "A": ["MBAPPE", "KANE", "DEMBELE", "YAMAL", "VINICIUS", "MESSI", "RONALDO"]
}
TUTTI_I_TOP = TOP_PLAYERS["D"] + TOP_PLAYERS["C"] + TOP_PLAYERS["A"]

# --- FUNZIONI CARICAMENTO ---
def carica_rose():
    if os.path.exists("database_rose.xlsx"):
        try:
            df = pd.read_excel("database_rose.xlsx", sheet_name="input_rose")
            df.columns = df.columns.str.strip()
            return df
        except: return pd.DataFrame()
    return pd.DataFrame()

def carica_listone_mondiale():
    if os.path.exists("quotazioni_mondiale.xlsx"):
        try:
            df = pd.read_excel("quotazioni_mondiale.xlsx")
            df.columns = df.columns.str.strip()
            return df
        except: return pd.DataFrame()
    return pd.DataFrame()

df_rose = carica_rose()
df_mondiale = carica_listone_mondiale()

def filtra_giocatori_squadra(squadra):
    if df_rose.empty: return pd.DataFrame()
    col_squadra = "FantaSquadra"
    if col_squadra in df_rose.columns:
        return df_rose[df_rose[col_squadra].str.strip() == squadra.strip()]
    return pd.DataFrame()

# --- GESTIONE PERSISTENZA SCELTE ---
def carica_scelte_file():
    if os.path.exists("scelte_fedelissimi.json"):
        try:
            with open("scelte_fedelissimi.json", "r") as f:
                return json.load(f)
        except: return {}
    return {}

def salva_scelte_file(scelte):
    with open("scelte_fedelissimi.json", "w") as f:
        json.dump(scelte, f)

def calcola_tassa_da_file(squadra):
    scelte = carica_scelte_file()
    if squadra in scelte:
        return scelte[squadra]["tassa"]
    giocatori = filtra_giocatori_squadra(squadra)
    if giocatori.empty: return 0
    return math.floor((giocatori["Quotazione"].sum() * 0.20) + 0.5)

# --- LOGIN ---
if "autenticato" not in st.session_state:
    st.session_state["autenticato"] = False
    st.session_state["utente_loggato"] = ""
    st.session_state["squadra_loggata"] = ""
    st.session_state["priorita"] = 99
    st.session_state["is_admin"] = False

st.sidebar.title("🔐 Accesso Area Riservata")
if not st.session_state["autenticato"]:
    password_input = st.sidebar.text_input("Inserisci la tua Password:", type="password")
    if st.sidebar.button("Accedi"):
        pass_clean = password_input.lower().strip()
        if pass_clean in UTENTI:
            st.session_state["autenticato"] = True
            st.session_state["utente_loggato"] = UTENTI[pass_clean]["nome"]
            st.session_state["squadra_loggata"] = UTENTI[pass_clean]["squadra"]
            st.session_state["priorita"] = UTENTI[pass_clean]["priorita"]
            st.session_state["is_admin"] = UTENTI[pass_clean]["admin"]
            st.rerun()
        else: st.sidebar.error("❌ Password errata!")
else:
    st.sidebar.write(f"👤 **Utente:** {st.session_state['utente_loggato']}")
    st.sidebar.write(f"🛡️ **Squadra:** {st.session_state['squadra_loggata']}")
    if st.sidebar.button("Logout"):
        st.session_state["autenticato"] = False
        st.session_state.clear()
        st.rerun()

if not st.session_state["autenticato"]:
    st.warning("🔒 Inserisci la tua password nel menu laterale per accedere.")
else:
    opzioni_menu = ["Home", "I miei Fedelissimi", "Listone Mondiale 2026", "🔥 Invia Buste Chiuse"]
    if st.session_state["is_admin"]: 
        opzioni_menu.append("⚙️ Pannello di Controllo Admin")
        opzioni_menu.append("🔍 ISPEZIONE OUTPUT FEDELISSIMI")
         
    menu = st.sidebar.selectbox("Menu Principale", opzioni_menu)
     
    tassa_squadra = calcola_tassa_da_file(st.session_state['squadra_loggata'])
    budget_buste = 100 - tassa_squadra

    if menu == "Home":
        st.info(f"Ciao {st.session_state['utente_loggato']}! Sessione protetta.")
        st.markdown(f"""
        - **Tassa Fedelissimi:** 20% sul blocco dei soli giocatori confermati (Arrotondato ad intero matematico reale, es: 5.4 -> **5M**, 4.4 -> **4M**).
        - **Budget Buste:** 100M Meno la Tassa dei Fedelissimi.
        """)

  elif menu == "🔍 ISPEZIONE OUTPUT FEDELISSIMI" and st.session_state["is_admin"]:
        st.write("### 📂 Output delle Scelte dei Fedelissimi Salvate sul Server")
        if os.path.exists("scelte_fedelissimi.json"):
            try:
                with open("scelte_fedelissimi.json", "r") as f:
                    st.json(json.load(f))
            except Exception as e: st.error(f"Errore fedelissimi: {e}")
        else: st.warning("Nessun file fedelissimi.")

        st.markdown("---")
        st.write("### ✉️ CONTENUTO DETTAGLIATO DI TUTTE LE BUSTE")
        for u in UTENTI.values():
            nome_file = f"busta_{u['nome'].lower()}.json"
            if os.path.exists(nome_file):
                try:
                    with open(nome_file, "r") as f:
                        dati_busta = json.load(f)
                    st.info(f"📩 Busta di: **{u['nome']}** ({u['squadra']})")
                    st.json(dati_busta) # Ti stampa a schermo l'offerta esatta e le 7 preferenze per reparto
                except Exception as e:
                    st.error(f"Errore lettura busta {u['nome']}: {e}")
            else:
                st.warning(f"❌ Nessuna busta trovata per {u['nome']}")

    elif menu == "I miei Fedelissimi":
        st.write(f"### 📑 Gestione Fedelissimi - {st.session_state['squadra_loggata']}")
        st.write("Seleziona i giocatori da confermare. Togli la spunta per scartarli e premi SALVA:")
        
        giocatori = filtra_giocatori_squadra(st.session_state['squadra_loggata'])
        
        if giocatori.empty:
            st.info("ℹ️ Nessun fedelissimo trovato per questa squadra. Budget Buste: 100M.")
        else:
            scelte_salvate = carica_scelte_file().get(st.session_state['squadra_loggata'], {}).get("giocatori", None)
            
            valore_corrente = 0
            giocatori_spuntati = []
            
            for idx, row in giocatori.iterrows():
                default_val = row['Giocatore'] in scelte_salvate if scelte_salvate is not None else True
                
                spuntato = st.checkbox(
                    f"{row['Giocatore']} ({row['Ruolo'].upper()}) — Valore: {row['Quotazione']} cr.",
                    value=default_val,
                    key=f"chk_{row['Giocatore']}_{idx}"
                )
                if spuntato:
                    valore_corrente += row['Quotazione']
                    giocatori_spuntati.append(row['Giocatore'])
            
            tassa_calcolata = math.floor((valore_corrente * 0.20) + 0.5)
            budget_risultante = 100 - tassa_calcolata
            
            st.markdown("---")
            st.metric("Tassa sulla selezione attuale", f"{tassa_calcolata} M")
            st.metric("Budget risultante per le tue Buste Chiuse", f"{budget_risultante} M")
            
            if st.button("💾 Salva Scelte Fedelissimi"):
                tutte_le_scelte = carica_scelte_file()
                tutte_le_scelte[st.session_state['squadra_loggata']] = {
                    "tassa": tassa_calcolata,
                    "giocatori": giocatori_spuntati
                }
                salva_scelte_file(tutte_le_scelte)
                st.success(f"🎯 Scelte salvate! Budget aggiornato a {budget_risultante}M. Ora puoi andare nel menu delle Buste.")
                st.rerun()

    elif menu == "Listone Mondiale 2026":
        st.write("### 📋 Quotazioni Ufficiali")
        if not df_mondiale.empty:
            df_vis = df_mondiale.copy()
            col_g = 'Giocatore' if 'Giocatore' in df_vis.columns else 'giocatore'
            if col_g in df_vis.columns:
                df_vis[col_g] = df_vis[col_g].apply(lambda x: f"⭐ {x} (TOP)" if str(x).upper().strip() in TUTTI_I_TOP else x)
            st.dataframe(df_vis, use_container_width=True, hide_index=True)

    elif menu == "🔥 Invia Buste Chiuse":
        st.write(f"### 📥 Compilazione Buste - Budget: **{budget_buste}M**")
        col_o1, col_o2, col_o3 = st.columns(3)
        off_dif = col_o1.number_input("Spesa DIFESA:", min_value=0, max_value=100, step=1, key="off_d")
        off_cen = col_o2.number_input("Spesa CENTROCAMPO:", min_value=0, max_value=100, step=1, key="off_c")
        off_att = col_o3.number_input("Spesa ATTACCO:", min_value=0, max_value=100, step=1, key="off_a")
         
        totale_offerto = off_dif + off_cen + off_att
        if totale_offerto == budget_buste: st.success("✅ Somma corretta.")
        else: st.warning(f"⚠️ Totale distribuito: {totale_offerto}M / {budget_buste}M.")
         
        gerarchia_d, gerarchia_c, gerarchia_a = [], [], []
        opzioni_d = ["-- Seleziona Difensore --"] + TOP_PLAYERS["D"]
        opzioni_c = ["-- Seleziona Centrocampista --"] + TOP_PLAYERS["C"]
        opzioni_a = ["-- Seleziona Attaccante --"] + TOP_PLAYERS["A"]
         
        tab_d, tab_c, tab_a = st.tabs(["🛡️ Difesa", "🧠 Centrocampo", "🔥 Attacco"])
        with tab_d:
            for i in range(7): gerarchia_d.append(st.selectbox(f"Posizione {i+1} Difesa:", opzioni_d, index=0, key=f"ger_d_{i}"))
        with tab_c:
            for i in range(7): gerarchia_c.append(st.selectbox(f"Posizione {i+1} Centrocampo:", opzioni_c, index=0, key=f"ger_c_{i}"))
        with tab_a:
            for i in range(7): gerarchia_a.append(st.selectbox(f"Posizione {i+1} Attacco:", opzioni_a, index=0, key=f"ger_a_{i}"))

        ha_vuoti = ("-- Seleziona Difensore --" in gerarchia_d) or ("-- Seleziona Centrocampista --" in gerarchia_c) or ("-- Seleziona Attaccante --" in gerarchia_a)
        ha_duplicati = (len(set(gerarchia_d)) != 7) or (len(set(gerarchia_c)) != 7) or (len(set(gerarchia_a)) != 7)

        if ha_vuoti: st.info("ℹ️ Seleziona tutti i 21 giocatori.")
        elif ha_duplicati: st.error("🚨 Non inserire duplicati nello stesso reparto.")
        elif totale_offerto != budget_buste: st.error(f"🚨 La somma deve fare esattamente {budget_buste}M.")
        else:
            if st.button("🔒 Invia e Sigilla Buste"):
                dati_busta = {"squadra": st.session_state["squadra_loggata"], "priorita": st.session_state["priorita"], "offerte": {"D": off_dif, "C": off_cen, "A": off_att}, "gerarchie": {"D": gerarchia_d, "C": gerarchia_c, "A": gerarchia_a}}
                with open(f"busta_{st.session_state['utente_loggato'].lower()}.json", "w") as f: json.dump(dati_busta, f)
                st.success("🎯 Busta salvata con successo!")

    elif menu == "⚙️ Pannello di Controllo Admin" and st.session_state["is_admin"]:
        st.write("### 🎛️ Console Admin")
         
        dati_budget_totali = []
        for u in UTENTI.values():
            t_p = calcola_tassa_da_file(u["squadra"])
            dati_budget_totali.append({
                "FantaSquadra": u["squadra"], 
                "Allenatore": u["nome"], 
                "Tassa Fedelissimi": f"{t_p} M", 
                "BUDGET BUSTE REALE": f"{100 - t_p} M"
            })
        st.table(pd.DataFrame(dati_budget_totali))
         
        st.markdown("---")
         
        if st.button("🗑️ Cancella tutte le Buste e Scelte Fedelissimi"):
            conteggio = 0
            for u in UTENTI.values():
                f_busta = f"busta_{u['nome'].lower()}.json"
                if os.path.exists(f_busta):
                    os.remove(f_busta)
                    conteggio += 1
            if os.path.exists("scelte_fedelissimi.json"):
                os.remove("scelte_fedelissimi.json")
             
            chiavi_buste = [k for k in st.session_state.keys() if k.startswith("off_") or k.startswith("ger_") or k.startswith("chk_")]
            for k in chiavi_buste: del st.session_state[k]
                 
            st.success(f"💥 Reset totale completato! Cancellati {conteggio} file. Login attivo.")
            st.rerun()

        st.markdown("---")
        for u in UTENTI.values():
            stato = "✅" if os.path.exists(f"busta_{u['nome'].lower()}.json") else "❌"
            st.write(f"{stato} {u['nome']} ({u['squadra']})")
        st.markdown("---")
         
        if st.button("⚡ Esegui Risoluzione Mercato"):
            tutte_le_buste = []
            for u in UTENTI.values():
                path_b = f"busta_{u['nome'].lower()}.json"
                if os.path.exists(path_b):
                    with open(path_b, "r") as f: tutte_le_buste.append(json.load(f))
                         
            if not tutte_le_buste: st.error("Nessuna busta depositata!")
            else:
                assegnazioni_finali = []
                for rep in ["D", "C", "A"]:
                    buste_ordinate = sorted(tutte_le_buste, key=lambda x: (x["offerte"][rep], -x["priorita"]), reverse=True)
                    giocatori_gia_assegnati = set()
                    for b in buste_ordinate:
                        squadra_corrente = b["squadra"]
                        offerta_fatta = b["offerte"][rep]
                        sua_gerarchia = b["gerarchie"][rep]
                        giocatore_vinto = "NESSUNO"
                        if offerta_fatta > 0:
                             for g_scelto in sua_gerarchia:
                                 if g_scelto not in giocatori_gia_assegnati and g_scelto in TOP_PLAYERS[rep]:
                                     giocatore_vinto = g_scelto
                                     giocatori_gia_assegnati.add(g_scelto)
                                     break
                        assegnazioni_finali.append({"Reparto": rep, "FantaSquadra": squadra_corrente, "Offerta": f"{offerta_fatta} M", "Top Player Assegnato": giocatore_vinto})
                st.success("🎉 Risoluzione completata!")
                st.table(pd.DataFrame(assegnazioni_finali))
