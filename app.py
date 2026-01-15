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
    return {"Starter Deck": [{"q": "Elysian Hub", "a": "Custom settings enabled."}]}

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
    
    st.divider()

    # COLLECTION MANAGEMENT
    st.markdown("<p class='sidebar-label'>🗂 COLLECTIONS</p>", unsafe_allow_html=True)
    selected_deck = st.selectbox("Active Deck", list(st.session_state.decks.keys()))
    
    with st.expander("➕ Add New Collection"):
        new_name = st.text_input("Deck Name", placeholder="e.g. Biology 101")
        if st.button("Create Collection", use_container_width=True):
            if new_name and new_name not in st.session_state.decks:
                st.session_state.decks[new_name] = []
                save_data(st.session_state.decks)
                st.success(f"Created {new_name}")
                st.rerun()
    
    # SETTINGS SECTION
    st.divider()
    st.markdown("<p class='sidebar-label'>⚙️ SETTINGS & PREFERENCES</p>", unsafe_allow_html=True)
    with st.expander("Configure Workspace"):
        # Adjust Daily Goal
        st.session_state.daily_goal = st.number_input("Daily Card Goal", min_value=1, value=st.session_state.daily_goal)
        
        # Adjust Timer Length
        timer_choice = st.selectbox("Timer Mode", ["25m Pomodoro", "50m Deep Work", "5m Break", "10m Break"])
        if st.button("Apply Timer Setting"):
            durations = {"25m Pomodoro": 1500, "50m Deep Work": 3000, "5m Break": 300, "10m Break": 600}
            st.session_state.timer_seconds = durations[timer_choice]
            st.session_state.run_timer = False
            st.rerun()

        st.divider()
        if st.button("🗑️ CLEAR ALL DECKS", help="This will delete everything!"):
            st.session_state.decks = {"Starter Deck": []}
            save_data(st.session_state.decks)
            st.rerun()

    st.divider()
    
    # QUICK ADD & AI
    st.markdown("<p class='sidebar-label'>✨ AI MAGIC CREATE</p>", unsafe_allow_html=True)
    with st.expander("Auto-Generate"):
        ai_in = st.text_area("Question : Answer", height=80, key="ai_magic")
        if st.button("Magic Import"):
            for line in ai_in.split('\n'):
                if ":" in line:
                    q, a = line.split(":", 1)
                    st.session_state.decks[selected_deck].append({"q": q.strip(), "a": a.strip()})
            save_data(st.session_state.decks)
            st.rerun()

    st.divider()

    # FOCUS TIMER
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

# --- MAIN CONTENT ---
deck = st.session_state.decks[selected_deck]
if not deck:
    st.info("Collection is empty. Add cards in the sidebar!")
    with st.expander("➕ Create Card Manually"):
        mq = st.text_input("Question")
        ma = st.text_area("Answer")
        if st.button("Save Card"):
            st.session_state.decks[selected_deck].append({"q": mq, "a": ma})
            save_data(st.session_state.decks)
            st.rerun()
else:
    current_card = deck[st.session_state.card_idx]
    
    # Progress
    goal_pct = min(st.session_state.cards_viewed / st.session_state.daily_goal, 1.0)
    st.progress(goal_pct)
    st.markdown(f"<p class='progress-text'>{st.session_state.cards_viewed}/{st.session_state.daily_goal} COMPLETED TODAY</p>", unsafe_allow_html=True)

    # 3D CARD
    st.markdown(f"""
        <div class="flip-card-container">
            <input type="checkbox" id="cardFlip" class="flip-checkbox">
            <label for="cardFlip" class="flip-card-inner">
                <div class="flip-card-front">
                    <span class="card-label">QUESTION</span>
                    <div class="card-content">{current_card['q']}</div>
                </div>
                <div class="flip-card-back">
                    <span class="card-label">ANSWER</span>
                    <div class="card-content">{current_card['a']}</div>
                </div>
            </label>
        </div>
    """, unsafe_allow_html=True)

    col_prev, col_next = st.columns(2)
    if col_prev.button("← PREVIOUS", use_container_width=True):
        st.session_state.card_idx = (st.session_state.card_idx - 1) % len(deck)
        st.rerun()
    if col_next.button("NEXT →", use_container_width=True):
        st.session_state.card_idx = (st.session_state.card_idx + 1) % len(deck)
        st.session_state.cards_viewed += 1
        st.rerun()