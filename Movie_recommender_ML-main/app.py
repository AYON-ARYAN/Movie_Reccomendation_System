import streamlit as st
from recommender import recommend_by_genres


st.set_page_config(page_title="Moodix - Movie Recommender", layout="wide")

import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from recommender import recommend, get_movie_list
import json
import os
from datetime import datetime

# --- User History Persistence Setup ---
HISTORY_FILE = "user_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def log_user_interaction(user_id, movie_title):
    history = load_history()
    if user_id not in history:
        history[user_id] = []
    history[user_id].append([movie_title, str(datetime.now())])
    save_history(history)

def get_user_history(user_id):
    history = load_history()
    return history.get(user_id, [])

# --- Auth Config ---
with open('/Volumes/BLACK_SHARK/Moodix/Movie_Reccomendation_System/Movie_recommender_ML-main/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

name, authentication_status, username = authenticator.login("Login", "main")

# --- Handle Login Status ---
if authentication_status is False:
    st.error("❌ Incorrect username or password")

elif authentication_status is None:
    st.warning("👋 Please enter your username and password")

elif authentication_status:
    # --- Main App Starts ---
    authenticator.logout("Logout", "sidebar")
    st.sidebar.write(f"Welcome, {name} 👋")

    # Page selection
    page = st.sidebar.radio("📂 Choose Recommendation Mode", ["🎞️ By Movie Title", "🧠 By Mood/Description"])

    if page == "🎞️ By Movie Title":
        st.title("🎬 MOODIX - Smart Movie Recommendation System")

        movie_list = get_movie_list()
        selected_movie = st.selectbox("🎞️ Select a movie you liked:", movie_list)

        if st.button("🎯 Show Recommendations"):
            log_user_interaction(name, selected_movie)
            recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

            if recommended_movie_names:
                st.subheader("📽️ You might also like:")
                cols = st.columns(5)
                for i in range(5):
                    with cols[i]:
                        st.text(recommended_movie_names[i])
                        st.image(recommended_movie_posters[i])
            else:
                st.warning("No recommendations found. Please try another movie.")

        with st.expander("🔍 Your Movie History"):
            history = get_user_history(name)
            if history:
                for title, timestamp in history[::-1]:
                    st.write(f"{timestamp}: {title}")
            else:
                st.write("No movie history yet.")

    elif page == "🧠 By Mood/Description":
        st.title("🧠 Mood-Based Recommendation")

        user_input = st.text_input("Describe what kind of movie you're in the mood for:",
                                   "I'm feeling happy and want something funny and light-hearted.")

        def mood_to_genres(text):
            text = text.lower()
            mood_map = {
                "sad": ["Comedy", "Feel-Good", "Adventure"],
                "happy": ["Romance", "Musical", "Comedy"],
                "bored": ["Thriller", "Adventure", "Action"],
                "inspiring": ["Biography", "Drama"],
                "scared": ["Horror"],
                "love": ["Romance", "Drama"],
                "funny": ["Comedy"],
                "action": ["Action", "Adventure"],
                "thriller": ["Thriller"],
                "mystery": ["Mystery", "Thriller"]
            }
            matched_genres = []
            for word, genres in mood_map.items():
                if word in text:
                    matched_genres.extend(genres)
            return list(set(matched_genres))

        if st.button("🔍 Find Movies For Me"):
            genres = mood_to_genres(user_input)
            if genres:
                st.markdown(f"🎯 We matched your mood to these genres: `{', '.join(genres)}`")
                rec_names, rec_posters = recommend_by_genres(genres)  # ✅ Correct function for genre-based recs
                # Your function must handle genres too
                if rec_names:
                    cols = st.columns(5)
                    for i in range(min(5, len(rec_names))):
                        with cols[i]:
                            st.text(rec_names[i])
                            st.image(rec_posters[i])
                else:
                    st.warning("Couldn't find recommendations. Try describing your mood differently.")
            else:
                st.info("Could not detect a genre from your description. Try a different phrase.")
