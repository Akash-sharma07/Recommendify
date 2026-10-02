# Recommendify

### Book & Movie Recommendation System

Recommendify is a Flask-based recommendation platform where I brought my
book and movie recommendation projects together into one application.

The main idea behind this project was to understand how recommendation
systems work in practice and then turn those models into a simple web
application that people can actually interact with.

## Live Demo

[Open Recommendify](https://recommendify-f4vu.onrender.com)

---

## What Recommendify Does

Recommendify currently provides different ways to discover books and movies.

### Books

- Top 50 Books
- Content-Based Book Recommendation
- Collaborative Book Recommendation

### Movies

- Content-Based Movie Recommendation

You can select a book or movie and get recommendations based on the
underlying recommendation model.

---

## Book Recommendation

The book section contains three different parts.

### 1. Top 50 Books

A simple section that displays a collection of the top 50 books from the
prepared dataset.

### 2. Content-Based Recommendation

This system recommends books that are similar to the book selected by the
user.

For the recommendation process, I used information such as:

- Book title
- Author
- Category

The text features are processed using TF-IDF, and similarity is calculated
to find books that are closer to the selected book.

### 3. Collaborative Recommendation

The collaborative recommendation system recommends books using patterns
from reader preferences and the existing collaborative filtering model.

This gives a different recommendation approach compared with
content-based filtering.

---

## Movie Recommendation

The movie recommendation system is content-based.

For this project, I worked with the TMDB 5000 Movies and Credits datasets.

I combined movie information and extracted useful features such as:

- Genres
- Keywords
- Overview
- Production companies
- Cast
- Director

These features are combined to create movie tags.

The tags are then converted into numerical representations using TF-IDF.

Finally, cosine similarity is used to find movies that are similar to the
movie selected by the user.

Movie posters are retrieved using the TMDB API.

---

## How It Works

### Book Content-Based Recommendation

```text
Book Data
    ↓
Data Cleaning
    ↓
Feature Selection
    ↓
Text Processing
    ↓
TF-IDF
    ↓
Similarity Calculation
    ↓
Recommended Books
