DROP PROCEDURE IF EXISTS moviesDb.filter_movies;
CALL moviesdb.loading_top_movies();
CREATE PROCEDURE moviesdb.filter_movies(
			  IN titles TEXT
            , IN year_min INT
            , IN year_max INT
            , IN rating_min FLOAT
            , IN rating_max FLOAT
            , IN genres TEXT
            , IN limit_films INT
)
INSERT INTO moviesdb.responce (genre,title,movie_year,rating)
SELECT genre, title, movie_year, rating
FROM moviesdb.TOP_MOVIES
WHERE TITLE REGEXP titles
AND RATING >= rating_min AND RATING <= rating_max
AND MOVIE_YEAR >= year_min AND MOVIE_YEAR <= year_max
AND GENRE REGEXP genres
ORDER BY RATING DESC
LIMIT limit_films