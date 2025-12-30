# 🎬 Movie Recommendation System

A **content-based Movie Recommendation Web Application** built using **Machine Learning, NLP, and Streamlit**. The app recommends movies similar to a selected movie by analyzing metadata such as genres, keywords, cast, crew, and overview.

---

## 🚀 Live Demo

🔗 **Live App:** https://movierecommendation-app.streamlit.app/

---

## 📌 Features

* 🔍 Content-based movie recommendations
* 🎭 Uses genres, keywords, cast, crew & overview
* 🌐 Language filter
* 📅 Release year filter
* 🖼️ Movie posters fetched via TMDB API
* ❤️ Add & manage favorite movies
* ⚡ Fast similarity computation using Cosine Similarity

---

## 🛠️ Tech Stack

### **Programming & ML**

* Python
* Pandas, NumPy
* Scikit-learn (Cosine Similarity, CountVectorizer)

### **Web Framework**

* Streamlit

### **APIs & Utilities**

* TMDB API (posters & metadata)
* PyCountry (language mapping)

### **Tools & Platforms**

* VS Code
* GitHub
* Streamlit Community Cloud
* Kaggle (dataset source)

---

## 📂 Dataset

This project uses the **TMDB 5000 Movies Dataset**:

* `tmdb_5000_movies.csv`
* `tmdb_5000_credits.csv`

📦 Dataset is hosted via **GitHub Releases** and automatically downloaded by the app.

> ⚠️ Dataset is used **only for educational and project demonstration purposes**.

---

## ⚙️ How It Works

1. Movie metadata is combined into a single **tags** feature
2. Text features are vectorized using **CountVectorizer**
3. **Cosine similarity** is calculated between movies
4. Top similar movies are recommended based on similarity score

---

## 📁 Project Structure

```
MovieRecommendationApp/
│
├── app.py                     # Streamlit application
├── requirements.txt           # Project dependencies
├── recommend.py               #recommend System
├── tmdb_5000_movies.csv       # Dataset (downloaded automatically)
├── tmdb_5000_credits.csv      # Dataset (downloaded automatically)
└── README.md                  # Project documentation
```

---

## ▶️ Run Locally

### 1️⃣ Clone the repository

```bash
git clone https://github.com/SanthoshU16/MovieRecommendationApp.git
cd MovieRecommendationApp
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the app

```bash
streamlit run app.py
```

---

## 🔑 TMDB API Key Setup

* Get a free API key from: [https://www.themoviedb.org/](https://www.themoviedb.org/)
* Replace the API key in `app.py`:

```python
TMDB_API_KEY = "your_api_key_here"
```

---

## 🌱 Future Improvements

* 🔄 Hybrid recommender system (content + collaborative filtering)
* 👤 User-based personalization
* 📊 Rating-based recommendations
* ☁️ Cloud database integration

---

## 👨‍💻 Author

**Santhosh U**
🎓 B.Tech AI&DS Student | 💡 AI & ML Enthusiast
🔗 GitHub: [https://github.com/SanthoshU16](https://github.com/SanthoshU16)

🔗 LinkedIn: [https://www.linkedin.com/in/santhoshu1/]

---

## ⭐ Acknowledgements

* Kaggle – TMDB Dataset
* TMDB API
* Streamlit Community

---
