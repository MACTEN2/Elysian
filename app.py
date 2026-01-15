import streamlit as st
import json
import os
import pandas as pd

# --- DATA STORAGE ---
DB_FILE = "decks.json"

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: return json.load(f)
        except: pass
    return {"Starter Deck": [{"q": "Welcome to Elysian", "a": "Clear, bold, and focused study."}]}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

if "decks" not in st.session_state:
    st.session_state.decks = load_data()
if "card_idx" not in st.session_state:
    st.session_state.card_idx = 0
if "flipped" not in st.session_state:
    st.session_state.flipped = False

# --- UI CONFIG ---
st.set_page_config(page_title="Elysian Study", page_icon="🌿", layout="centered")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 class='sidebar-logo'>🌿 ELYSIAN</h1>", unsafe_allow_html=True)
    selected_deck = st.selectbox("Current Collection", list(st.session_state.decks.keys()))
    
    st.divider()
    
    with st.expander("➕ QUICK ADD"):
        q = st.text_input("Front Side")
        a = st.text_area("Back Side")
        if st.button("Save Card", use_container_width=True):
            if q and a:
                st.session_state.decks[selected_deck].append({"q": q, "a": a})
                save_data(st.session_state.decks)
                st.rerun()

    if st.button("➕ NEW DECK", use_container_width=True):
        new_name = f"Deck {len(st.session_state.decks) + 1}"
        st.session_state.decks[new_name] = []
        save_data(st.session_state.decks)
        st.rerun()

# --- TABS FOR DIFFERENT VIEWS ---
tab1, tab2 = st.tabs(["📖 STUDY MODE", "🗂 MANAGE DECK"])

# --- TAB 1: STUDY MODE ---
with tab1:
    deck = st.session_state.decks[selected_deck]
    if not deck:
        st.warning("This collection is currently empty.")
    else:
        current_card = deck[st.session_state.card_idx]
        st.markdown(f"<p class='progress-text'>{selected_deck.upper()} / {st.session_state.card_idx + 1} OF {len(deck)}</p>", unsafe_allow_html=True)

        display_text = current_card['a'] if st.session_state.flipped else current_card['q']
        label_text = "THE ANSWER" if st.session_state.flipped else "THE QUESTION"
        
        st.markdown(f"""
            <div class="card-container">
                <p class="card-type-label">{label_text}</p>
                <h1 class="card-main-content">{display_text}</h1>
            </div>
        """, unsafe_allow_html=True)

        col_f, col_p, col_n = st.columns([2,1,1])
        with col_f:
            if st.button("🔄 FLIP", use_container_width=True):
                st.session_state.flipped = not st.session_state.flipped
                st.rerun()
        with col_p:
            if st.button("PREV", use_container_width=True):
                st.session_state.card_idx = (st.session_state.card_idx - 1) % len(deck)
                st.session_state.flipped = False
                st.rerun()
        with col_n:
            if st.button("NEXT", use_container_width=True):
                st.session_state.card_idx = (st.session_state.card_idx + 1) % len(deck)
                st.session_state.flipped = False
                st.rerun()

# --- TAB 2: MANAGE DECK ---
with tab2:
    st.subheader(f"Edit {selected_deck}")
    deck = st.session_state.decks[selected_deck]
    
    if not deck:
        st.info("No cards to show.")
    else:
        for i, card in enumerate(deck):
            with st.container():
                # Display each card in a mini-editor row
                col_q, col_a, col_del = st.columns([2, 2, 1])
                
                new_q = col_q.text_input(f"Front #{i+1}", value=card['q'], key=f"q_{selected_deck}_{i}")
                new_a = col_a.text_input(f"Back #{i+1}", value=card['a'], key=f"a_{selected_deck}_{i}")
                
                # Check for changes and update
                if new_q != card['q'] or new_a != card['a']:
                    st.session_state.decks[selected_deck][i] = {"q": new_q, "a": new_a}
                    save_data(st.session_state.decks)
                
                if col_del.button("🗑️", key=f"del_{selected_deck}_{i}"):
                    st.session_state.decks[selected_deck].pop(i)
                    save_data(st.session_state.decks)
                    st.rerun()
                st.markdown("---")