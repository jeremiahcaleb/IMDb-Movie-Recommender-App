import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# App config
st.set_page_config(page_title="🎬 IMDB Movie Recommendation App", layout="centered")

# Get base API URL from environment
API_BASE_URL = os.getenv("API_BASE_URL")

# Title
st.title("🎥 IMDB Movie Recommendation App")
st.markdown("Get top 10 recommendations based on your favorite movie 🎬")

# Input
movie_name = st.text_input("Enter a movie title:", placeholder="e.g. Iron Man")

# Button to trigger recommendation
if st.button("Recommend 🎯"):
    if not movie_name.strip():
        st.warning("Please enter a movie name!")
    elif not API_BASE_URL:
        st.error("API_BASE_URL not set in environment. Please check your .env file.")
    else:
        try:
            # Construct API endpoint
            endpoint = f"{API_BASE_URL.rstrip('/')}/recommend"
            params = {"title": movie_name.strip()}
            headers = {"ngrok-skip-browser-warning": "true"}

            # API call
            response = requests.get(endpoint, params=params, headers=headers)

            if response.status_code == 200:
                recommendations = response.json()

                if isinstance(recommendations, list) and recommendations:
                    st.success(f"Top 10 movies recommended for '{movie_name}':")
                    for idx, movie in enumerate(recommendations, start=1):
                        name = movie.get("Movie Name", "Unknown Title")
                        genre = movie.get("Genre", "")
                        rating = movie.get("Movie Rating", "")

                        st.markdown(f"""
                            <div style="padding: 10px; border-radius: 10px; background-color: #f0f2f6; margin-bottom: 10px;">
                                <h4 style="margin: 0;">🎬 {idx}. {name}</h4>
                                <small>{genre} — ⭐ {rating}</small>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No recommendations found. Try a different movie.")
            else:
                st.error(f"Failed to fetch recommendations. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Footer
st.markdown("---")
