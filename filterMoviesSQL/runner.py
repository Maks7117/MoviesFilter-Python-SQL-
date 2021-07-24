import mysql.connector
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='movies filter')
    parser.add_argument('-n',  '--number', type=int, help='number of films', default=10)
    parser.add_argument('-g',  '--genres', type=str, help='enter the genres you want', default='.*')
    parser.add_argument('-yf', '--year_from', type=int, help='enter the year from', default=0)
    parser.add_argument('-yt', '--year_to', type=int, help='enter the year to', default=10000)
    parser.add_argument('-t',  '--title', type=str, help='name of the film', default='.*')
    parser.add_argument('-rf', '--rating_from', type=float, help='rating film from', default=0)
    parser.add_argument('-rt', '--rating_to', type=float, help='rating film to', default=5)
    return parser.parse_args()


def user_request():

    cursor = connection.cursor(buffered=True)
    parameters = []
    for genre in args.genres.split(sep='|'):
        parameters.append((
                           args.title,
                           args.year_from,
                           args.year_to,
                           args.rating_from,
                           args.rating_to,
                           genre,
                           args.number))
        print(parameters)

    sql = """CAll moviesdb.FILTER_MOVIES(%s,%s,%s,%s,%s,%s,%s)"""

    cursor.executemany(sql, parameters)
    connection.commit()

    cursor.execute("select * from moviesdb.responce")
    for row in cursor.fetchall().__str__().split(sep='), ('):
        print(row)
    cursor.execute("delete from moviesdb.responce where true")
    connection.commit()
    connection.close()
    cursor.close()


if __name__ == '__main__':
    args = parse_args()
    connection = mysql.connector.connect(
        user='root',
        password='mysql',
        host='localhost')

    user_request()
