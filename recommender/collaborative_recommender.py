from pathlib import Path
import pickle
import sys

project_path = Path(__file__).resolve().parent.parent

collaborative_path = project_path / "Data" / "collaborative.pkl"
books_with_rating_path = project_path / "Data" / "books_with_rating.pkl"

with open(collaborative_path,"rb") as file:
    user_book_rating_matrix = pickle.load(file)
    collaborative_similarity_model = pickle.load(file)

with open(books_with_rating_path,"rb") as file:
    books_with_ratings = pickle.load(file)


def collaborative_similar_books(book_title):
    book_rating_vector = user_book_rating_matrix.loc[book_title, :].values.reshape(1, -1)
    distances, similar_book_indices = collaborative_similarity_model.kneighbors(book_rating_vector, n_neighbors=11)

    books = []
    for title in user_book_rating_matrix.index[similar_book_indices[0]]:
        item = []
        if book_title == title: continue
        match = books_with_ratings[title == books_with_ratings["Book-Title"]]
        item.extend(match.drop_duplicates("Book-Title")["Book-Title"].values)
        item.extend(match.drop_duplicates("Book-Title")["Book-Author"].values)
        item.extend(match.drop_duplicates("Book-Title")["Image-URL-L"].values)
        item.extend(match.drop_duplicates("Book-Title")["Year-Of-Publication"].values)

        books.append(item)

    return books

if __name__ == "__main__":
    
    import os

    size_in_bytes = os.path.getsize(books_with_rating_path)
    size_in_mb = size_in_bytes / (1024 * 1024)

    print(f"{collaborative_path}: {size_in_mb:.2f} MB")