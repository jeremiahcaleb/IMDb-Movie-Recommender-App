# 🎬 IMDb Movie Recommendation System

A content-based movie recommender system using TF-IDF and cosine similarity on IMDb movie descriptions. The project features:

- Model training with `train.py`
- Flask API exposed via ngrok (`api.py`)
- Streamlit frontend (`app.py`)
- Environment-based config for ngrok tokens and URLs

---

## 📂 Project Structure

```

IMDb-Movie-Recommender-App/
├── model_training/
│   ├── dataset.csv          # Raw IMDb dataset
│   └── train.py             # Model training script
├── .env                     # Environment variables (ngrok token & API URL)
├── api.py                   # Flask API + ngrok server
├── app.py                   # Streamlit frontend app
├── imdb_recommender.pkl     # Saved model (created after training)
├── requirements.txt
├── README.md

````

---

## ⚙️ Setup & Run Instructions

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/jeremiahcaleb/IMDb-Movie-Recommender-App.git
cd IMDb-Movie-Recommender-App
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
````

### 3. Train the model

Run the training script to process the dataset and generate the recommendation model.

```bash
python model_training\train.py
```

This will generate `imdb_recommender.pkl` inside the folder.

### 4. Add your ngrok auth token

Create or update `.env` file in the root directory with your ngrok token:

```env
NGROK_AUTHTOKEN=your_token_here
```

### 5. Start the Flask API with ngrok tunnel

Run the API server (this will start ngrok and print the public URL):

```bash
python api.py
```

Note the public ngrok URL printed in the console (e.g., `https://abc123.ngrok-free.app`).

### 6. Update `.env` with ngrok URL

Add the API_BASE_URL to your `.env` file:

```env
API_BASE_URL=https://abc123.ngrok-free.app
```

### 7. Run the Streamlit frontend

Start the Streamlit app which will consume the Flask API:

```bash
streamlit run app.py
```

---

## 🔌 How It Works

* `train.py` creates the model from raw data.
* `api.py` serves recommendations via Flask, exposed through ngrok.
* `app.py` provides a user-friendly interface to query recommendations.
* `.env` stores sensitive info — your ngrok token and public API URL.

---

## 🧪 Testing the API (Optional)

Use Postman or your browser to test:

```bash
GET https://abc123.ngrok-free.app/recommend?title=Iron Man
```

---

## 🛠️ Tech Stack

* Python 3.9+
* Flask
* Streamlit
* Scikit-learn
* pyngrok
* Pandas, NumPy

---

## Contributions are welcome!
