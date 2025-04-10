# recommender.py

import pickle
import requests
import pandas as pd

# Load data
movies = pickle.load(open("/Volumes/BLACK_SHARK/Moodix/Movie_Reccomendation_System/Movie_recommender_ML-main/src/movie_list.pkl", "rb"))
similarity = pickle.load(open("/Volumes/BLACK_SHARK/Moodix/Movie_Reccomendation_System/Movie_recommender_ML-main/src/similarity.pkl", "rb"))

def fetch_poster(movie_id):
    """Fetch movie poster URL from TMDB using movie ID."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_path = data.get("poster_path")
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return ""

def recommend(movie_title):
    """Return list of recommended movie titles and posters."""
    if movie_title not in movies['title'].values:
        return [], []

    index = movies[movies['title'] == movie_title].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_titles = []
    recommended_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_titles.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_titles, recommended_posters

def get_movie_list():
    """Return list of all available movie titles."""
    return movies['title'].values
