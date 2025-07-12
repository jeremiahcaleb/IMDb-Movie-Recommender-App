import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import re
import joblib
import warnings

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Ignore warnings
warnings.filterwarnings("ignore")

# Plotting defaults
plt.rcParams.update({
    'font.size': 13,
    'figure.titlesize': 20,
    'figure.figsize': (16, 10)
})
sns.set_style("dark")

# Load the data
def load_data(filepath):
    data = pd.read_csv(filepath)
    if 'Unnamed: 0' in data.columns:
        data.drop('Unnamed: 0', axis=1, inplace=True)
    return data

# Clean release year
def extract_year(text):
    match = re.search(r'\d{4}', str(text))
    return int(match.group()) if match else np.nan

# Clean watch time
def clean_watch_time(value):
    return value[:-4] if isinstance(value, str) else np.nan

# Clean Meatscore
def clean_meatscore(value):
    if value == "****" or pd.isna(value):
        return np.nan
    return value.strip()

# Clean Gross column
def parse_gross(value):
    if not isinstance(value, str):
        return np.nan
    if value.startswith('$'):
        if 'B' in value:
            return float(re.sub(r'[^\d.]', '', value)) * 1000
        if 'M' in value:
            return float(re.sub(r'[^\d.]', '', value))
    return np.nan

# Build recommendation system
def build_recommender(data):
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(data["Description"].fillna(""))
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    index_map = pd.Series(data.index, index=data['Movie Name']).drop_duplicates()
    return tfidf, cosine_sim, index_map

# Recommend movies
def get_recommendations(title, cosine_sim, data, index_map, top_n=10):
    if title not in index_map:
        return ["Title not found in dataset."]
    idx = index_map[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n + 1]
    indices = [i[0] for i in sim_scores]
    return data['Movie Name'].iloc[indices].tolist()

# Main processing
def process_imdb(filepath):
    data = load_data(filepath)

    # Clean columns
    data['ReleaseYear'] = data['Year of Release'].apply(extract_year)
    data['TotalTime'] = data['Watch Time'].apply(clean_watch_time)
    data['Meatscore'] = data['Meatscore of movie'].apply(clean_meatscore)
    data['Worth'] = data['Gross'].apply(parse_gross)

    # Drop unused columns
    for col in ['Year of Release', 'Watch Time', 'Votes', 'Meatscore of movie', 'Gross']:
        if col in data.columns:
            data.drop(col, axis=1, inplace=True)

    # Handle missing values
    data.fillna(method='bfill', inplace=True)

    # Convert types
    data['ReleaseYear'] = data['ReleaseYear'].astype(int)
    data['Meatscore'] = data['Meatscore'].astype(int)
    data['Worth'] = pd.to_numeric(data['Worth'], errors='coerce')

    # Build recommendation engine
    tfidf, cosine_sim, index_map = build_recommender(data)

    # Save model and data
    joblib.dump({
        "tfidf": tfidf,
        "cosine_sim": cosine_sim,
        "data": data,
        "index_map": index_map
    }, "imdb_recommender.pkl")

    print("✅ Model and data saved as imdb_recommender.pkl")
    return data

# Run script
if __name__ == "__main__":
    dataset = "dataset.csv"  # Update path as needed
    processed_data = process_imdb(dataset)
