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
    return {"Starter Deck": [{"q": "Welcome to Elysian", "a": "Your new productivity hub."}]}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- SESSION STATE ---
if "decks" not in st.session_state: st.session_state.decks = load_data()
if "card_idx" not in st.session_state: st.session_state.card_idx = 0
if "show_answer" not in st.session_state: st.session_state.show_answer = False
if "daily_goal" not in st.session_state: st.session_state.daily_goal = 20
if "cards_viewed" not in st.session_state: st.session_state.cards_viewed = 0
if "timer_seconds" not in st.session_state: st.session_state.timer_seconds = 1500
if "run_timer" not in st.session_state: st.session_state.run_timer = False

# --- UI CONFIG ---
st.set_page_config(page_title="Elysian Hub", page_icon="🌿", layout="wide")

if os.path.exists("style.css"):
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- SIDEBAR: THE COMMAND CENTER ---
with st.sidebar:
    st.markdown("<h1 class='sidebar-logo'>🌿 ELYSIAN</h1>", unsafe_allow_html=True)
    
    selected_deck = st.selectbox("🗂 ACTIVE COLLECTION", list(st.session_state.decks.keys()))
    
    st.divider()

    # 1. DECK STATS
    st.markdown("<p class='sidebar-label'>📊 DECK STATS</p>", unsafe_allow_html=True)
    total_cards = len(st.session_state.decks[selected_deck])
    st.markdown(f"<div class='stat-card'><span>Total Cards:</span> <span style='color:#00FFC2;'>{total_cards}</span></div>", unsafe_allow_html=True)

    st.divider()

    # 2. DAILY GOAL TRACKER
    st.markdown("<p class='sidebar-label'>🎯 DAILY GOAL</p>", unsafe_allow_html=True)
    goal_progress = min(st.session_state.cards_viewed / st.session_state.daily_goal, 1.0)
    st.progress(goal_progress)
    st.caption(f"{st.session_state.cards_viewed} / {st.session_state.daily_goal} cards mastered")

    st.divider()

    # 3. FOCUS TIMER
    st.markdown("<p class='sidebar-label'>⏱️ FOCUS SPRINT</p>", unsafe_allow_html=True)
    mins, secs = divmod(st.session_state.timer_seconds, 60)
    st.markdown(f"<div class='timer-box-mini'>{mins:02d}:{secs:02d}</div>", unsafe_allow_html=True)
    
    tc1, tc2 = st.columns(2)
    if not st.session_state.run_timer:
        if tc1.button("▶ START", use_container_width=True):
            st.session_state.run_timer = True
            st.rerun()
    else:
        if tc1.button("⏹ STOP", use_container_width=True, type="primary"):
            st.session_state.run_timer = False
            st.rerun()
    if tc2.button("🔄", use_container_width=True):
        st.session_state.timer_seconds = 1500
        st.rerun()

    if st.session_state.run_timer and st.session_state.timer_seconds > 0:
        time.sleep(1)
        st.session_state.timer_seconds -= 1
        st.rerun()

# --- MAIN CONTENT ---
deck = st.session_state.decks[selected_deck]

if deck:
    current_card = deck[st.session_state.card_idx]
    
    # Progress Header
    st.markdown(f"## {selected_deck} <span style='color:#888; font-size:1rem;'>Card {st.session_state.card_idx + 1} of {len(deck)}</span>", unsafe_allow_html=True)
    
    # Split Panel Layout
    q_col, a_col = st.columns(2)
    
    with q_col:
        st.markdown(f"""
            <div class="panel question-panel">
                <p class="label">QUESTION</p>
                <div class="content-text">{current_card['q']}</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("REVEAL ANSWER", use_container_width=True):
            st.session_state.show_answer = not st.session_state.show_answer
            st.rerun()

    with a_col:
        if st.session_state.show_answer:
            st.markdown(f"""
                <div class="panel answer-panel">
                    <p class="label" style="color:#00FFC2;">ANSWER</p>
                    <div class="content-text">{current_card['a']}</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="panel placeholder-panel">
                    <div class="content-text" style="color:#333; opacity:0.2;">Hidden</div>
                </div>
            """, unsafe_allow_html=True)

    # Navigation
    st.markdown("<br>", unsafe_allow_html=True)
    n1, n2, n3 = st.columns([1,1,1])
    if n1.button("← PREVIOUS", use_container_width=True):
        st.session_state.card_idx = (st.session_state.card_idx - 1) % len(deck)
        st.session_state.show_answer = False
        st.rerun()
    if n3.button("NEXT →", use_container_width=True):
        st.session_state.card_idx = (st.session_state.card_idx + 1) % len(deck)
        st.session_state.show_answer = False
        st.session_state.cards_viewed += 1 # Track progress for the daily goal
        st.rerun()

# --- COLLECTION MANAGEMENT ---
st.markdown("<br><hr><br>", unsafe_allow_html=True)
st.subheader("📝 Collection Manager")
for i, card in enumerate(deck):
    col_q, col_a, col_d = st.columns([2, 2, 0.5])
    u_q = col_q.text_input("Q", value=card['q'], key=f"q{i}", label_visibility="collapsed")
    u_a = col_a.text_input("A", value=card['a'], key=f"a{i}", label_visibility="collapsed")
    if u_q != card['q'] or u_a != card['a']:
        st.session_state.decks[selected_deck][i] = {"q": u_q, "a": u_a}
        save_data(st.session_state.decks)
    if col_d.button("🗑️", key=f"d{i}"):
        st.session_state.decks[selected_deck].pop(i)
        save_data(st.session_state.decks)
        st.rerun()