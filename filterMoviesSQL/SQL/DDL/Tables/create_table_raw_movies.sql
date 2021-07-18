DROP TABLE IF EXISTS stg_moviesdb.raw_movies;
CREATE TABLE stg_moviesdb.raw_movies(
	movies_id INT PRIMARY KEY,
    title TEXT,
    genres TEXT
    );