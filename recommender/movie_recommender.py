import pickle
import asyncio
import aiohttp
from pathlib import Path
from dotenv import load_dotenv
import os
import gzip

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

project_path = Path(__file__).resolve().parent.parent

with gzip.open(project_path / "Data" / "movies_data.pkl", "rb") as file:
    movies_df, similarity_matrix = pickle.load(file)  


REQUEST_HEADERS = {"User-Agent": "Mozilla/5.0"}  # avoids server-side blocking for missing User-Agent


# ---------- Recommendation Logic ----------
def recommend_movies(selected_title: str):
    """Return top 10 movies most similar to the selected movie."""
    movie_index = movies_df[movies_df["title"] == selected_title].index[0]

    # sort all movies by similarity score, skip index 0 (the movie itself)
    similarity_scores = sorted(
        enumerate(similarity_matrix[movie_index]),
        key=lambda score_pair: score_pair[1],
        reverse=True,
    )[1:11]

    similar_movie_indices = [index for index, score in similarity_scores]
    return movies_df.iloc[similar_movie_indices]


# ---------- Poster Fetching (Async) ----------
async def fetch_poster_url(session: aiohttp.ClientSession, movie_id: int, retries: int = 3):
    """Fetch a single movie's poster URL from TMDB, retrying with exponential backoff on failure."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"

    for attempt in range(retries):
        try:
            async with session.get(url, headers=REQUEST_HEADERS, timeout=aiohttp.ClientTimeout(total=10)) as response:
                response.raise_for_status()
                movie_data = await response.json()
                poster_path = movie_data.get("poster_path")
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
        except Exception:
            if attempt == retries - 1:
                return None
            await asyncio.sleep(2 ** attempt)  # 1s, 2s, 4s backoff


async def fetch_all_posters(movie_ids):
    """Fetch posters for multiple movies concurrently."""
    async with aiohttp.ClientSession() as session:
        poster_urls = await asyncio.gather(*(fetch_poster_url(session, movie_id) for movie_id in movie_ids))
    return list(poster_urls)

def get_recommended_posters(movie_ids):
    posters_path = asyncio.run(fetch_all_posters(movie_ids=movie_ids))
    return posters_path


if __name__ == "__main__":

    similar = recommend_movies("Avatar")
    print(similar)
    
    import os

    size_in_bytes = os.path.getsize(project_path / "Data" / "movies_data.pkl")
    size_in_mb = size_in_bytes / (1024 * 1024)

    print(f"{project_path / "Data" / "movies_data.pkl"}: {size_in_mb:.2f} MB")