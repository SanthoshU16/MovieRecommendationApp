import os
import pandas as pd
import streamlit as st
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ast import literal_eval
import pycountry

# -------------------- PAGE CONFIG --------------------
st.set_page_config(layout="wide")
st.title("🎬 Movie Recommender")

TMDB_API_KEY = "b1b1dc89770344f6675d558c42205f9f"

# -------------------- DATA LOADING --------------------
@st.cache_resource
def load_data():
    movies_file = "tmdb_5000_movies.csv"
    credits_file = "tmdb_5000_credits.csv"

    MOVIES_URL = "https://github.com/SanthoshU16/MovieRecommendationApp/releases/download/v1.0/tmdb_5000_movies.csv"
    CREDITS_URL = "https://github.com/SanthoshU16/MovieRecommendationApp/releases/download/v1.0/tmdb_5000_credits.csv"

    def download_file(url, filename):
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            st.error("❌ Failed to download dataset")
            st.stop()
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

    if not os.path.exists(movies_file):
        download_file(MOVIES_URL, movies_file)

    if not os.path.exists(credits_file):
        download_file(CREDITS_URL, credits_file)

    movies = pd.read_csv(movies_file)
    credits = pd.read_csv(credits_file)

    movies = movies.merge(credits, on="title")
    
    movies = movies[[
        "movie_id", "title", "overview", "genres", "keywords",
        "cast", "crew", "original_language", "release_date", "vote_average"
    ]]

    def extract_names(x):
        try:
            return " ".join([i["name"] for i in literal_eval(x)])
        except:
            return ""

    def get_director(x):
        try:
            for i in literal_eval(x):
                if i["job"] == "Director":
                    return i["name"]
        except:
            return ""
        return ""

    movies["tags"] = (
        movies["overview"].fillna("") + " "
        + movies["genres"].apply(extract_names) + " "
        + movies["keywords"].apply(extract_names) + " "
        + movies["cast"].apply(
            lambda x: " ".join([i["name"] for i in literal_eval(x)[:3]])
            if pd.notnull(x) else ""
        ) + " "
        + movies["crew"].apply(get_director)
    ).str.lower()

    cv = CountVectorizer(max_features=5000, stop_words="english")
    vectors = cv.fit_transform(movies["tags"])
    similarity = cosine_similarity(vectors)

    return movies, similarity
with st.spinner("Loading movie data..."):
    movies, similarity = load_data()
    
# -------------------- HELPERS --------------------
def fetch_poster(title):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}"
        data = requests.get(url).json()
        if data["results"] and data["results"][0].get("poster_path"):
            return "https://image.tmdb.org/t/p/w500" + data["results"][0]["poster_path"]
    except:
        pass
    return "https://via.placeholder.com/300x450?text=No+Poster"

def get_language_name(code):
    try:
        return pycountry.languages.get(alpha_2=code).name
    except:
        return code

def recommend(selected_title):
    index = movies[movies["title"] == selected_title].index[0]
    distances = list(enumerate(similarity[index]))
    sorted_movies = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]

    recs = []
    for i in sorted_movies:
        data = movies.iloc[i[0]]

        try:
            genres = ", ".join([g["name"] for g in literal_eval(data["genres"])])
        except:
            genres = "N/A"

        try:
            cast = ", ".join([a["name"] for a in literal_eval(data["cast"])[:3]])
        except:
            cast = "N/A"

        try:
            crew = literal_eval(data["crew"])
            director = next((p["name"] for p in crew if p["job"] == "Director"), "N/A")
        except:
            director = "N/A"

        try:
            year = pd.to_datetime(data["release_date"]).year
        except:
            year = "N/A"

        recs.append({
            "title": data["title"],
            "poster_url": fetch_poster(data["title"]),
            "rating": data.get("vote_average", "N/A"),
            "genres": genres,
            "overview": data.get("overview", "No description."),
            "director": director,
            "cast": cast,
            "year": year,
            "language": get_language_name(data.get("original_language", ""))
        })
    return recs

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.header("🎯 Filters")

    years = sorted(
        movies["release_date"].dropna().apply(lambda x: pd.to_datetime(x).year).unique()
    )
    year_filter = st.selectbox("📅 Release Year", ["All"] + list(map(str, years)))

    languages = sorted(movies["original_language"].dropna().unique())
    language_names = [get_language_name(l) for l in languages if get_language_name(l)]
    language_filter = st.selectbox("🌐 Language", ["All"] + language_names)

    st.header("❤️ Favorites")
    if "favorites" not in st.session_state:
        st.session_state.favorites = []

    for i, fav in enumerate(st.session_state.favorites):
        st.image(fav["poster_url"], use_container_width=True)
        st.markdown(f"**{fav['title']} ({fav['year']})**")
        if st.button("❌ Remove", key=f"remove_{i}"):
            st.session_state.favorites.pop(i)
            st.rerun()

# -------------------- MAIN UI --------------------
movie_input = st.text_input("Enter a movie name:")

if movie_input:
    matches = movies[movies["title"].str.lower().str.contains(movie_input.lower())]
    if not matches.empty:
        selected_title = st.selectbox("Select the correct movie:", matches["title"].tolist())
        recommendations = recommend(selected_title)

        if year_filter != "All":
            recommendations = [r for r in recommendations if str(r["year"]) == year_filter]
        if language_filter != "All":
            recommendations = [r for r in recommendations if r["language"] == language_filter]

        st.subheader(f"🎬 Recommendations for '{selected_title}'")
        cols = st.columns(3)

        for idx, movie in enumerate(recommendations):
            with cols[idx % 3]:
                st.image(movie["poster_url"], use_container_width=True)
                st.markdown(f"**{movie['title']} ({movie['year']})**")
                st.markdown(f"⭐ {movie['rating']} | 🎭 {movie['genres']}")
                st.markdown(f"🎥 *{movie['director']}*")
                st.markdown(f"👥 *{movie['cast']}*")
                st.markdown(movie["overview"][:120] + "...")

                if movie not in st.session_state.favorites:
                    if st.button("💾 Add to Favorites", key=f"fav_{movie['title']}"):
                        st.session_state.favorites.append(movie)
                        st.rerun()
else:
    st.info("Start by typing a movie name above 🎥")
