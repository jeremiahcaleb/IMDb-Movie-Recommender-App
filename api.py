import os
from flask import Flask, request, jsonify
from pyngrok import ngrok
import joblib
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

ngrok_token = os.getenv("NGROK_AUTHTOKEN")
if not ngrok_token:
    raise EnvironmentError("❌ NGROK_AUTHTOKEN not found. Please set it as an environment variable or in a .env file.")
os.environ["NGROK_AUTHTOKEN"] = ngrok_token

# Load the model
try:
    model = joblib.load("imdb_recommender.pkl")
except Exception as e:
    raise RuntimeError(f"❌ Failed to load model: {e}")

cosine_sim = model["cosine_sim"]
data = model["data"]
index_map = model["index_map"]

# Initialize Flask app
app = Flask(__name__)

@app.route("/recommend", methods=["GET"])
def recommend():
    title = request.args.get("title")
    if not title:
        return jsonify({"error": "Missing 'title' parameter."}), 400

    if title not in index_map:
        return jsonify({"error": f"Movie '{title}' not found in the dataset."}), 404

    idx = index_map[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:11]
    movie_indices = [i[0] for i in sim_scores]

    # Columns to return
    columns_to_show = [col for col in ["Movie Name", "Genre", "Movie Rating"] if col in data.columns]
    results = data.iloc[movie_indices][columns_to_show].to_dict(orient="records")

    return jsonify(results)

# Start ngrok tunnel
public_url = ngrok.connect(5000)
print(f"🔗 Your IMDb recommender is live at: {public_url}")

# Run the Flask app
app.run()
