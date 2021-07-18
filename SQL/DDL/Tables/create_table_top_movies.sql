DROP TABLE IF EXISTS moviesDb.top_movies;
CREATE TABLE IF NOT EXISTS moviesDb.top_movies(
	genre TEXT,
    title TEXT,
    movie_year INT,
    rating FLOAT
    );