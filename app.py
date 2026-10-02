from flask import Flask, render_template, request
import pickle
from pathlib import Path
from recommender.content_recommender import recommend_similar_books, content_based_books_df
from recommender.collaborative_recommender import collaborative_similar_books, user_book_rating_matrix
from recommender.movie_recommender import movies_df, recommend_movies, get_recommended_posters


# =========================
# PATHS
# =========================

project_path = Path(__file__).resolve().parent

book_path = project_path / "Data" / "Top_50_books.pkl"


# =========================
# LOAD BOOK DATA
# =========================

with open(book_path, "rb") as file:
    top_books_data = pickle.load(file)


# =========================
# FLASK APP
# =========================

app = Flask(__name__)

print(type(top_books_data))

# =========================
# HOME
# =========================

@app.route("/")
def home():
    return render_template("home.html")


# =========================
# BOOKS
# =========================

@app.route("/books")
def books():
    books_data = top_books_data.head(6).to_dict(orient="records")

    return render_template(
        "books.html",
        books=books_data
    )


# =========================
# TOP 50 BOOKS
# =========================

@app.route("/books/top")
def top_books():
    book_data = top_books_data.to_dict(orient="records")

    return render_template(
        "top_books.html",
        books=book_data
    )


# =========================
# CONTENT BASED
# =========================
@app.route("/books/content", methods=["GET", "POST"])
def content_books():

    query = request.args.get("q", "").strip()

    search_results = []
    recommendations = []
    selected_book = ""
    error = ""

    # -------- SEARCH --------

    if query:

        matches = content_based_books_df[
            content_based_books_df["title"]
            .astype(str)
            .str.contains(
                query,
                case=False,
                na=False,
                regex=False
            )
        ].head(10)

        search_results = matches.to_dict(
            orient="records"
        )

    # -------- SELECT BOOK --------

    if request.method == "POST":

        selected_book = request.form.get(
            "book_title", ""
        ).strip()

        try:

            recommendations = recommend_similar_books(
                selected_book
            ).to_dict(orient="records")

        except IndexError:

            error = "Please select a valid book from the search results."

        except Exception as e:

            print("ERROR:", e)

            error = "Something went wrong while generating recommendations."

    return render_template(
        "content_books.html",
        query=query,
        search_results=search_results,
        recommendations=recommendations,
        selected_book=selected_book,
        error=error
    )


# =========================
# COLLABORATIVE
# =========================

@app.route("/books/collaborative", methods=["GET","POST"])
def collaborative_books():
    book_titles = user_book_rating_matrix.index

    recommendations = []
    selected_book = ""
    error = ""

    if request.method == "POST":

        selected_book = request.form.get("book_title", "").strip()

        try:
            recommendations = collaborative_similar_books(str(selected_book))
        except IndexError as e:
            error = "Please select a valid book."
        except Exception as e:
            print("ERROR:", e)

            error = "Something went wrong while generating recommendations."

    return render_template("collaborative_books.html",
                           book_titles = book_titles,
                            recommendations = recommendations,
                            selected_book = selected_book,
                            error = error
                        )


    


    # return render_template("collaborative_books.html")


# =========================
# MOVIES
# =========================

@app.route("/movies", methods=["GET", "POST"])
def movies():

    movie_titles = movies_df["title"].dropna().tolist()

    recommendations = []
    selected_movie = ""
    error = ""

    if request.method == "POST":

        selected_movie = request.form.get("movie_title", "").strip()

        try:
            # Get recommended movies
            recommended_df = recommend_movies(selected_movie)

            # Fetch TMDB posters
            movie_ids = recommended_df["id"].tolist()
            poster_urls = get_recommended_posters(movie_ids)

            # Convert dataframe to records
            recommendations = recommended_df.to_dict(orient="records")

            # Add poster URL to each movie
            for movie, poster in zip(recommendations, poster_urls):
                movie["poster"] = poster

        except IndexError:
            error = "Please select a valid movie."

        except Exception as e:
            print("ERROR:", e)
            error = "Something went wrong while generating recommendations."

    return render_template(
        "movies.html",
        movie_titles=movie_titles,
        recommendations=recommendations,
        selected_movie=selected_movie,
        error=error
    )


# =========================
# ABOUT
# =========================

@app.route("/about")
def about():
    return render_template("about.html")


# =========================
# CONTACT
# =========================

@app.route("/contact")
def contact():
    return render_template("contact.html")


# =========================
# RUN
# =========================

if __name__ == "__main__":
    app.run()