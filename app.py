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

# Load CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- SIDEBAR (High Contrast) ---
with st.sidebar:
    st.markdown("<h1 class='sidebar-logo'>🌿 ELYSIAN</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sidebar-tagline'>Focus Environment</p>", unsafe_allow_html=True)
    
    selected_deck = st.selectbox("Current Collection", list(st.session_state.decks.keys()))
    
    st.markdown("---")
    
    with st.expander("📝 ADD NEW CARD"):
        q = st.text_input("Front Side (Question)")
        a = st.text_area("Back Side (Answer)")
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

# --- MAIN INTERFACE ---
deck = st.session_state.decks[selected_deck]

if not deck:
    st.warning("This collection is currently empty.")
else:
    current_card = deck[st.session_state.card_idx]
    
    # Progress indicator
    st.markdown(f"<p class='progress-text'>{selected_deck.upper()} / CARD {st.session_state.card_idx + 1} OF {len(deck)}</p>", unsafe_allow_html=True)

    # The Interactive Card
    display_text = current_card['a'] if st.session_state.flipped else current_card['q']
    label_text = "THE ANSWER" if st.session_state.flipped else "THE QUESTION"
    
    st.markdown(f"""
        <div class="card-container">
            <p class="card-type-label">{label_text}</p>
            <h1 class="card-main-content">{display_text}</h1>
        </div>
    """, unsafe_allow_html=True)

    # Controls
    flip_col, space, nav_col1, nav_col2 = st.columns([2, 1, 1, 1])
    
    with flip_col:
        if st.button("🔄 FLIP CARD", use_container_width=True):
            st.session_state.flipped = not st.session_state.flipped
            st.rerun()
            
    with nav_col1:
        if st.button("PREV", use_container_width=True):
            st.session_state.card_idx = (st.session_state.card_idx - 1) % len(deck)
            st.session_state.flipped = False
            st.rerun()
            
    with nav_col2:
        if st.button("NEXT", use_container_width=True):
            st.session_state.card_idx = (st.session_state.card_idx + 1) % len(deck)
            st.session_state.flipped = False
            st.rerun()