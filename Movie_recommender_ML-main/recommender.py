import pickle
import requests
import pandas as pd
import pandas as pd
import pickle
import ast
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# Load data
movies = pickle.load(open("/Volumes/BLACK_SHARK/Moodix/Movie_Reccomendation_System/Movie_recommender_ML-main/src/movie_list.pkl", "rb"))
similarity = pickle.load(open("/Volumes/BLACK_SHARK/Moodix/Movie_Reccomendation_System/Movie_recommender_ML-main/src/similarity.pkl", "rb"))

# Assuming the movies dataframe has a column 'genres' which contains genres of each movie in a list-like format.
# If not, we need to modify the dataset to include genres.

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
    """Return list of recommended movie titles and posters based on the movie title."""
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



# Modify the function to load the movies from the CSV file
def load_movies_from_csv():
    """Load movie data from CSV file."""
    # Read CSV file (ensure the path is correct)
    movies = pd.read_csv('/Volumes/BLACK_SHARK/Moodix/Movie_Reccomendation_System/tmdb_5000_movies.csv')
    movies.columns = movies.columns.str.strip().str.lower()  # clean column names
    return movies


def recommend_by_genres(genres):
    """Return movie recommendations based on genres."""
    try:
        # Load the genres CSV
        movies_csv = pd.read_csv("/Volumes/BLACK_SHARK/Moodix/Movie_Reccomendation_System/tmdb_5000_movies.csv")

        # Load the movie list from the pickle file
        with open('/Volumes/BLACK_SHARK/Moodix/Movie_Reccomendation_System/Movie_recommender_ML-main/src/movie_list.pkl', 'rb') as f:
            movie_list = pickle.load(f)

        # Ensure movie_list has 'movie_id'. Assuming it might have other relevant info.
        # If 'poster_url' is already in movie_list and up-to-date, you might not need fetch_poster for all.

        # Merge the genres CSV with the movie list (based on movie_id)
        movies = pd.merge(movies_csv, movie_list, on='movie_id', how='inner')

        # Convert the 'genres' column from stringified list of dictionaries to a list of genres
        movies['genres_list'] = movies['genres'].apply(lambda x: [d['name'] for d in ast.literal_eval(x)])

        # Filter the movies based on the input genres
        filtered_movies = movies[movies['genres_list'].apply(lambda x: any(genre in x for genre in genres))]

        recommended_titles = []
        recommended_posters = []

        # Recommend up to 5 movies from the filtered list
        for index, movie in filtered_movies.head(5).iterrows():
            movie_id = movie['movie_id']
            recommended_titles.append(movie['title'])
            poster_url = fetch_poster(movie_id)
            recommended_posters.append(poster_url)

        return recommended_titles, recommended_posters

    except FileNotFoundError as e:
        print(f"Error: One or more files not found: {e}")
        return [], []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return [], []
def get_movie_list():
    """Return list of all available movie titles."""
    return movies['title'].values
def get_genre_keywords(movies_df):
    """Extracts and combines genre names into a processable format."""
    genre_keywords = {}
    for index, row in movies_df.iterrows():
        genres = row['genres_list']
        movie_id = row['movie_id']
        genre_keywords[movie_id] = " ".join(genres)
    return genre_keywords
def recommend_by_mood(mood_description, movies_df, genre_keywords, top_n=5):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(genre_keywords.values())

    mood_vector = tfidf_vectorizer.transform([mood_description])
    cosine_similarities = cosine_similarity(mood_vector, tfidf_matrix)
    similarity_scores = list(enumerate(cosine_similarities[0]))
    sorted_similar_movies = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    recommended_movies = []
    recommended_posters = []

    for i in sorted_similar_movies[:top_n]:
        movie_id_from_keywords = list(genre_keywords.keys())[i[0]]
        # Check if the movie_id exists in movies_df
        movie = movies_df[movies_df['movie_id'] == movie_id_from_keywords]
        if not movie.empty:
            recommended_movies.append(movie.iloc[0]['title'])
            poster_url = fetch_poster(movie.iloc[0]['movie_id'])
            recommended_posters.append(poster_url)

    if not recommended_movies:
        # Fallback logic (moved here to be executed if no similar movies are found)
        mood_genre_map = {
            "happy": ["Comedy", "Adventure", "Family"],
            "sad": ["Drama", "Romance"],
            "exciting": ["Action", "Thriller"],
            "emotional": ["Drama", "Romance"],
            "funny": ["Comedy"],
            "scary": ["Horror", "Thriller"],
            "intense": ["Thriller", "Action"],
            "relaxing": ["Animation", "Fantasy"]
        }
        matched_genres = []
        for keyword in mood_description.lower().split():
            if keyword in mood_genre_map:
                matched_genres.extend(mood_genre_map[keyword])
        if matched_genres:
            titles, posters = recommend_by_genres(list(set(matched_genres)))
            return titles, posters, f"Fallback: matched genres from mood keywords: {', '.join(set(matched_genres))}"
        else:
            return [], [], "Sorry, we couldn’t match your mood to any genres. Try using different words."
    else:
        return recommended_movies, recommended_posters, "🎯 Based on your mood input!"
def load_movie_data():
    """Loads and preprocesses movie data."""
    try:
        movies_csv = pd.read_csv("/Volumes/BLACK_SHARK/Moodix/Movie_Reccomendation_System/tmdb_5000_movies.csv")
        with open('/Volumes/BLACK_SHARK/Moodix/Movie_Reccomendation_System/Movie_recommender_ML-main/src/movie_list.pkl', 'rb') as f:
            movie_list = pickle.load(f)
        # Rename 'id' to 'movie_id' in movies_csv if needed
        if 'id' in movies_csv.columns:
            movies_csv.rename(columns={'id': 'movie_id'}, inplace=True)

        movies = pd.merge(movie_list, movies_csv, on='movie_id', how='inner')

        movies['genres_list'] = movies['genres'].apply(lambda x: [d['name'] for d in ast.literal_eval(x)])
        return movies
    except FileNotFoundError as e:
        print(f"Error: One or more files not found: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during data loading: {e}")
        return None

if __name__ == '__main__':
    movies_df = load_movie_data()
    if movies_df is not None:
        genre_keywords = get_genre_keywords(movies_df)
        mood_input = input("Describe what kind of movie you're in the mood for: ")
        recommended_titles, recommended_posters, feedback = recommend_by_mood(mood_input, movies_df, genre_keywords)

        print(feedback)
        if recommended_titles:
            print("\nRecommended Movies:")
            for i in range(len(recommended_titles)):
                print(f"- {recommended_titles[i]}: Poster URL - {recommended_posters[i]}")


