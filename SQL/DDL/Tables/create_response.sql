DROP TABLE IF EXISTS moviesDb.responce;
CREATE TABLE moviesDb.responce (
   genre text,
   title text,
   movie_year int DEFAULT NULL,
   rating float DEFAULT NULL
 )