import streamlit as st
import json
import os
import time

# --- DATA STORAGE ---
DB_FILE = "decks.json"

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: return json.load(f)
        except: pass
    return {"Starter Deck": [{"q": "Elysian Pro", "a": "High-impact 3D study mode active."}]}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- SESSION STATE ---
if "decks" not in st.session_state: st.session_state.decks = load_data()
if "card_idx" not in st.session_state: st.session_state.card_idx = 0
if "daily_goal" not in st.session_state: st.session_state.daily_goal = 20
if "cards_viewed" not in st.session_state: st.session_state.cards_viewed = 0
if "timer_seconds" not in st.session_state: st.session_state.timer_seconds = 1500
if "run_timer" not in st.session_state: st.session_state.run_timer = False

# --- UI CONFIG ---
st.set_page_config(page_title="Elysian Hub", page_icon="🗒️", layout="centered")

if os.path.exists("style.css"):
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- SIDEBAR: COMMAND CENTER ---
with st.sidebar:
    st.markdown("<h1 class='sidebar-logo'>🗒️ ELYSIAN</h1>", unsafe_allow_html=True)
    selected_deck = st.selectbox("🗂 ACTIVE COLLECTION", list(st.session_state.decks.keys()))
    
    with st.expander("➕ NEW COLLECTION"):
        n_name = st.text_input("Name")
        if st.button("Create Deck"):
            if n_name and n_name not in st.session_state.decks:
                st.session_state.decks[n_name] = []
                save_data(st.session_state.decks)
                st.rerun()

    st.divider()
    st.markdown("<p class='sidebar-label'>✨ AI MAGIC CREATE</p>", unsafe_allow_html=True)
    with st.expander("Auto-Generate Stack"):
        ai_in = st.text_area("Question : Answer", height=100)
        if st.button("Magic Import"):
            for line in ai_in.split('\n'):
                if ":" in line:
                    q, a = line.split(":", 1)
                    st.session_state.decks[selected_deck].append({"q": q.strip(), "a": a.strip()})
            save_data(st.session_state.decks)
            st.rerun()

    st.divider()
    st.markdown("<p class='sidebar-label'>⏱️ FOCUS SPRINT</p>", unsafe_allow_html=True)
    mins, secs = divmod(st.session_state.timer_seconds, 60)
    st.markdown(f"<div class='timer-box-mini'>{mins:02d}:{secs:02d}</div>", unsafe_allow_html=True)
    
    tc1, tc2 = st.columns(2)
    if not st.session_state.run_timer:
        if tc1.button("▶ START", use_container_width=True): st.session_state.run_timer = True; st.rerun()
    else:
        if tc1.button("⏹ STOP", use_container_width=True, type="primary"): st.session_state.run_timer = False; st.rerun()
    if tc2.button("🔄", use_container_width=True): st.session_state.timer_seconds = 1500; st.rerun()

    if st.session_state.run_timer and st.session_state.timer_seconds > 0:
        time.sleep(1)
        st.session_state.timer_seconds -= 1
        st.rerun()

# --- MAIN CONTENT: THE 3D FLASHCARD ---
deck = st.session_state.decks[selected_deck]

if not deck:
    st.info("Collection is empty. Add cards in the sidebar!")
else:
    current_card = deck[st.session_state.card_idx]
    
    # Progress Bar
    goal_pct = min(st.session_state.cards_viewed / st.session_state.daily_goal, 1.0)
    st.progress(goal_pct)
    st.markdown(f"<p class='progress-text'>{st.session_state.cards_viewed}/{st.session_state.daily_goal} CARDS TOWARD DAILY GOAL</p>", unsafe_allow_html=True)

    # 3D SMOOTH FLIP CARD (HTML/CSS ONLY FOR MAXIMUM SMOOTHNESS)
    # The 'flip-checkbox' trick allows the user to click the card to rotate it.
    st.markdown(f"""
        <div class="flip-card-container">
            <input type="checkbox" id="cardFlip" class="flip-checkbox">
            <label for="cardFlip" class="flip-card-inner">
                <div class="flip-card-front">
                    <span class="card-label">QUESTION</span>
                    <div class="card-content">{current_card['q']}</div>
                    <span class="card-hint">Tap to see answer</span>
                </div>
                <div class="flip-card-back">
                    <span class="card-label">ANSWER</span>
                    <div class="card-content">{current_card['a']}</div>
                    <span class="card-hint">Tap to see question</span>
                </div>
            </label>
        </div>
    """, unsafe_allow_html=True)

    # Navigation Controls
    col_prev, col_next = st.columns(2)
    if col_prev.button("← PREVIOUS", use_container_width=True):
        st.session_state.card_idx = (st.session_state.card_idx - 1) % len(deck)
        st.rerun()
    if col_next.button("NEXT →", use_container_width=True):
        st.session_state.card_idx = (st.session_state.card_idx + 1) % len(deck)
        st.session_state.cards_viewed += 1
        st.rerun()

# --- BOTTOM: MANAGER ---
st.markdown("<br><br><hr>", unsafe_allow_html=True)
with st.expander("🗂 MANAGE COLLECTION"):
    for i, card in enumerate(deck):
        c_q, c_a, c_d = st.columns([2, 2, 0.5])
        u_q = c_q.text_input(f"Q", value=card['q'], key=f"edit_q{i}", label_visibility="collapsed")
        u_a = c_a.text_input(f"A", value=card['a'], key=f"edit_a{i}", label_visibility="collapsed")
        if u_q != card['q'] or u_a != card['a']:
            st.session_state.decks[selected_deck][i] = {"q": u_q, "a": u_a}
            save_data(st.session_state.decks)
        if c_d.button("🗑️", key=f"del_{i}"):
            st.session_state.decks[selected_deck].pop(i)
            save_data(st.session_state.decks)
            st.rerun()