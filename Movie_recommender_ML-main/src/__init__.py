import pickle

with open('movie_list.pkl', 'rb') as f:
    data = pickle.load(f)

print(type(data))
print(data.columns if hasattr(data, 'columns') else 'Not a DataFrame')
print(data.head() if hasattr(data, 'head') else data[:5])
