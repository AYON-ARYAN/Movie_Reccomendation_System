import streamlit as st
st.set_page_config(page_title="Moodix - Movie Recommender", layout="wide")  # MUST BE FIRST

# Now import everything else
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

# --- Streamlit Authenticator Configuration ---
with open('/Volumes/BLACK_SHARK/Moodix/Movie_Reccomendation_System/Movie_recommender_ML-main/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

name, authentication_status, username = authenticator.login("Login", "main")

# --- App Logic Starts Here ---
if authentication_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.write(f"Welcome, {name} 👋")

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

    # --- Show User History ---
    with st.expander("🔍 Your Movie History"):
        history = get_user_history(name)
        if history:
            for title, timestamp in history[::-1]:
                st.write(f"{timestamp}: {title}")
        else:
            st.write("No movie history yet.")

elif authentication_status is False:
    st.error("Incorrect username or password")

elif authentication_status is None:
    st.warning("Please enter your username and password")
