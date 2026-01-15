## Elysian Study
Where Focus Meets Aesthetic Productivity
Elysian Study is a high-performance, 3D-animated flashcard application designed to transform the way students and professionals master new information. It blends a minimalist aesthetic with powerful productivity tools to create a "flow state" environment for learning.


## 💡 Why Elysian?
Traditional flashcard apps often feel cluttered or purely functional. Elysian was built on the philosophy that a beautiful workspace leads to better focus. By combining smooth 3D animations with a dark-mode "Command Center," Elysian makes the cognitive load of studying feel lighter and more engaging.

## 🎯 Purpose
The purpose of this project is to provide a seamless, local-first learning tool that respects the user's time. It aims to:

- Reduce Friction: Quickly import notes using AI-ready formatting.

- ncourage Consistency: Track daily goals to build a study habit.

- Enhance Focus: Utilize an integrated Pomodoro timer to prevent burnout.

## ✨ Key Features
- 3D Interactive Flashcards: A large, immersive single-card view with hardware-accelerated 3D flip animations for a tactile feel.
- AI Magic Create: A batch-import tool that allows users to paste notes in Question : Answer format and instantly generate entire decks.
- Integrated Focus Timer: A neon-lit Pomodoro timer in the sidebar to manage study sprints (25-minute default).
- Daily Goal Tracking: A visual progress system that tracks card reviews against a customizable daily target.
- Collection Management: Create, edit, and delete multiple study decks via an organized sidebar and a dedicated manager.
- Local Persistence: All data is saved to a local decks.json file, ensuring your data stays yours.

## 🛠 Tech Stack
Elysian is built using modern web and data tools:

- Python: The core logic engine.

- Streamlit: Used for the web interface and state management.

- CSS3 (Custom): Extensively used for the 3D transforms, animations, and the "Elysian Dark" aesthetic.

- HTML5: Utilized for the interactive card structures.

- JSON: Used as a lightweight, local database for storage.

## ⚙️ How It Works
Elysian operates on a State-Driven Architecture.

* The Sidebar acts as the controller, modifying the "Session State" (Current Deck, Timer State, Card Index).

* The UI reacts to state changes. For example, clicking "Next" updates the card index and resets the visual flip state of the card.

* The 3D Flip is handled entirely by the browser's CSS engine using a "Checkbox Hack," which ensures the animation is butter-smooth and doesn't require a page reload to flip.

## 🚀 Getting Started
Prerequisites
Python 3.8 or higher installed on your system.

## Installation
1. Clone the files: Place app.py and style.css in the same folder.

2. Install Streamlit:

3. Bash
- pip install streamlit
- Running the App
- Open your terminal or command prompt.

4. Navigate to the folder containing the files.

5. Run the following command:

Bash
- streamlit run app.py
- The app will automatically open in your default web browser (usually at http://localhost:8501).

## 📝 Usage
1. Select/Create a Deck: Use the sidebar dropdown or the "New Collection" expander.

2. Add Cards: Use "AI Magic Create" for many cards or the "Manage" section at the bottom for manual entries.

3. Study: Click the card to flip it and see the answer. Use the "Next" and "Previous" buttons to navigate.

4. Focus: Click "Start" on the Focus Timer and try to hit your "Daily Goal" before the timer runs out!