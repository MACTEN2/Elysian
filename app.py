import streamlit as st
import json
import os

# --- DATA STORAGE ---
DB_FILE = "decks.json"

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: return json.load(f)
        except: pass
    return {"Starter Deck": [{"q": "Welcome to Elysian", "a": "Hover and click to see the magic."}]}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

if "decks" not in st.session_state:
    st.session_state.decks = load_data()
if "card_idx" not in st.session_state:
    st.session_state.card_idx = 0

# --- UI CONFIG ---
st.set_page_config(page_title="Elysian Study", page_icon="🗒️", layout="centered")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 class='sidebar-logo'>🌿 ELYSIAN</h1>", unsafe_allow_html=True)
    selected_deck = st.selectbox("Collection", list(st.session_state.decks.keys()))
    
    st.divider()
    with st.expander("📂 NEW COLLECTION"):
        name = st.text_input("Name", key="new_deck_name")
        if st.button("Create", use_container_width=True):
            if name and name not in st.session_state.decks:
                st.session_state.decks[name] = []
                save_data(st.session_state.decks)
                st.rerun()

    with st.expander("📝 ADD CARD"):
        q = st.text_input("Question")
        a = st.text_area("Answer")
        if st.button("Save Card", use_container_width=True):
            if q and a:
                st.session_state.decks[selected_deck].append({"q": q, "a": a})
                save_data(st.session_state.decks)
                st.rerun()

# --- MAIN INTERFACE ---
tab1, tab2 = st.tabs(["📖 STUDY", "🗂 MANAGE"])

with tab1:
    deck = st.session_state.decks[selected_deck]
    if not deck:
        st.info("Deck is empty.")
    else:
        current_card = deck[st.session_state.card_idx]
        
        # 3D ANIMATED CARD HTML
        # We use a checkbox trick to handle the flip state visually
        st.markdown(f"""
            <div class="flip-card">
                <input type="checkbox" id="flip-trigger" class="flip-checkbox">
                <label for="flip-trigger" class="flip-card-inner">
                    <div class="flip-card-front">
                        <p class="card-label">QUESTION</p>
                        <div class="card-text">{current_card['q']}</div>
                    </div>
                    <div class="flip-card-back">
                        <p class="card-label">ANSWER</p>
                        <div class="card-text">{current_card['a']}</div>
                    </div>
                </label>
            </div>
        """, unsafe_allow_html=True)

        # Navigation
        st.markdown("<br>", unsafe_allow_html=True)
        col_p, col_n = st.columns(2)
        with col_p:
            if st.button("← PREVIOUS", use_container_width=True):
                st.session_state.card_idx = (st.session_state.card_idx - 1) % len(deck)
                st.rerun()
        with col_n:
            if st.button("NEXT →", use_container_width=True):
                st.session_state.card_idx = (st.session_state.card_idx + 1) % len(deck)
                st.rerun()

with tab2:
    st.subheader("Manage Collection")
    for i, card in enumerate(deck):
        c1, c2, c3 = st.columns([2, 2, 0.5])
        u_q = c1.text_input(f"Q{i}", value=card['q'], key=f"q{i}", label_visibility="collapsed")
        u_a = c2.text_input(f"A{i}", value=card['a'], key=f"a{i}", label_visibility="collapsed")
        if c3.button("🗑️", key=f"d{i}"):
            st.session_state.decks[selected_deck].pop(i)
            save_data(st.session_state.decks)
            st.rerun()