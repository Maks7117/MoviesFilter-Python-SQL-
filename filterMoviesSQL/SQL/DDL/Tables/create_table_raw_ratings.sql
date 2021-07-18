DROP TABLE IF EXISTS stg_moviesdb.raw_ratings;
CREATE TABLE stg_moviesdb.raw_ratings(
	user_id INT,
	movies_id INT PRIMARY KEY,
    rating FLOAT,
    time_stamp INT
    );