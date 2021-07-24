import mysql.connector
import csv


def loading_ratings(ratings_query):
    sql = "INSERT INTO stg_moviesdb.raw_ratings(user_id, movies_id, rating, time_stamp) VALUES (%s, %s, %s, %s)"
    my_data = []
    for row in ratings_query:
        res = list(row.values())
        user_Id = int(res[0])
        movies_Id = int(res[1])
        rating = float(res[2])
        time_stamp = int(res[3])
        args = (user_Id, movies_Id, rating, time_stamp)
        my_data.append(args)

    try:
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.executemany(sql, my_data)
            connection.commit()
    except connection.Error as e:
        print("Ошибка подключения: '" + str(e) + "'.")


def loading_movies(movies_query):
    sql1 = "INSERT INTO stg_moviesdb.raw_movies(movies_id, title, genres) VALUES (%s, %s, %s)"
    my_data1 = []
    for row in movies_query:
        res = list(row.values())
        movies_id = int(res[0])
        title = res[1]
        genres = res[2]
        args = (movies_id, title, genres)
        my_data1.append(args)

    try:
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("USE stg_moviesdb")
            cursor.executemany(sql1, my_data1)
            connection.commit()
    except connection.Error as e:
        print("Ошибка подключения: '" + str(e) + "'.")


def read_input_file(file_name):
    with open(file_name, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        output_list = [row for row in reader]
    return output_list


def execute_query(query_path):
    connection = mysql.connector.connect(
        user='root',
        password='mysql',
        host='localhost'
    )
    sql_file = open(query_path)
    sql_as_string = sql_file.read()
    cursor = connection.cursor()
    for result in cursor.execute(sql_as_string, multi=True):
        pass

    connection.commit()
    cursor.close()
    connection.close()
    connection.disconnect()


if __name__ == '__main__':
    connection = mysql.connector.connect(
        user='root',
        password='mysql',
        host='localhost'
    )

    movies_path = 'data/movies.csv'
    ratings_path = 'data/ratings.csv'
    movies_query = read_input_file(movies_path)
    ratings_query = read_input_file(ratings_path)

    create_moviesDb_path = 'SQL/DDL/Databases/create_moviesDb.sql'
    create_stg_moviesDb_path = 'SQL/DDL/Databases/create_stg_moviesDb.sql'
    create_top_movies_proc_path = 'SQL/DDL/Tables/create_table_top_movies.sql'
    create_table_raw_movies_path = 'SQL/DDL/Tables/create_table_raw_movies.sql'
    create_table_raw_ratings_path = 'SQL/DDL/Tables/create_table_raw_ratings.sql'

    normalize_movies_path = 'SQL/DDL/Views/normalize_movies.sql'
    normalize_ratings_path = 'SQL/DDL/Views/normalize_ratings.sql'

    create_response_path = 'SQL/DDL/Tables/create_response.sql'

    loading_top_movies_path = 'SQL/DML/Procedures/loading_top_movies.sql'

    filter_movies_path = 'SQL/DML/Procedures/filter_movies.sql'

    execute_query(create_moviesDb_path)
    execute_query(create_stg_moviesDb_path)
    execute_query(create_table_raw_movies_path)
    execute_query(create_table_raw_ratings_path)
    execute_query(create_top_movies_proc_path)
    loading_ratings(ratings_query)
    loading_movies(movies_query)
    execute_query(normalize_movies_path)
    execute_query(normalize_ratings_path)
    execute_query(create_response_path)
    execute_query(loading_top_movies_path)
    execute_query(filter_movies_path)