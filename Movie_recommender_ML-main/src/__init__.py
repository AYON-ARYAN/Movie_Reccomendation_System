import pandas as pd
import pickle

# Load your movie dataset (update filename if it's different)
df = pd.read_csv("/Volumes/BLACK_SHARK/Moodix/Movie_Reccomendation_System/tmdb_5000_movies.csv")

# You can print some rows to verify it's loaded correctly
print(df.head())

# Save the DataFrame as a pickle file
with open("movie_list.pkl", "wb") as f:
    pickle.dump(df, f)

print("✅ movie_list.pkl generated successfully!")
