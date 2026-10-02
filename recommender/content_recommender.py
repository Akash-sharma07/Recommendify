from pathlib import Path
import pickle

project_path = Path(__file__).resolve().parent.parent

content_books_path = project_path / "Data" / "content.pkl"

with open(content_books_path, "rb") as file:
    content_based_books_df = pickle.load(file)
    content_similarity_model = pickle.load(file)
    content_feature_matrix = pickle.load(file)

def recommend_similar_books(book_title: str):
    book_index = content_based_books_df[content_based_books_df["title"] == book_title].index[0]
    distances, similar_book_indices = content_similarity_model.kneighbors(content_feature_matrix[book_index], n_neighbors=11)

    similar_books = content_based_books_df.iloc[similar_book_indices[0][1:]]

    return similar_books


if __name__ == "__main__":
    
    import os

    size_in_bytes = os.path.getsize(content_books_path)
    size_in_mb = size_in_bytes / (1024 * 1024)

    print(f"{content_books_path}: {size_in_mb:.2f} MB")