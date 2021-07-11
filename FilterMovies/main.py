import argparse
import csv
import re


def parse_args():
    parser = argparse.ArgumentParser(description='movies filter')
    parser.add_argument('-n', '--number', type=int, help='number of films')
    parser.add_argument('-g', '--genres', nargs='+', required=False, help='enter the genres you want')
    parser.add_argument('-yf', '--year_from', type=int, help='enter the year from')
    parser.add_argument('-yt', '--year_to', type=int, help='enter the year to')
    parser.add_argument('-rg', '--regexp', type=str, help='name of the ".+name"')
    parser.add_argument('-m', '--movies_file', type=str, help='Input moves fail')
    parser.add_argument('-r', '--rating', type=float, help='rating film')
    parser.add_argument('-rf', '--ratings_file', type=str, help='Input ratings fail')
    parser.add_argument('-u', '--output_file', type=str, help='output file csv_like')
    return parser.parse_args()


def first(movies, count):
    if len(movies) > count:
        return movies[:count]
    else:
        return movies


def sort(movies):
    return sorted(movies, key=lambda x: x['rating'], reverse=True)


def join(movies, ratings):
    output_list = []

    for i in movies:
        if i['movieId'] in ratings:
            i.update(rating=ratings[i['movieId']])
            output_list.append(i)
    return output_list


def filter_movies_by_year_from(movies, year_from):
    return [r for r in movies if r['year'] >= year_from]


def filter_movies_by_year_to(movies, year_to):
    return [r for r in movies if r['year'] <= year_to]


def filter_ratings(ratings, rating):
    output_dict = {}
    for k, v in ratings.items():
        if v >= rating:
            output_dict[k] = v
    return output_dict


def filter_genres(movies, genres):
    output_list = []
    for i in movies:
        for k in genres:
            if k in i["genres"]:
                output_list.append(i)
                break
    return output_list


def filter_movies_by_name(movies, regexp):
    return [r for r in movies if re.match(regexp, r['title'])]


def average_rating_by_movie_id(ratings):
    output_dict = {}
    for i in ratings:
        movie_id = i['movieId']
        rating = i['rating']
        if movie_id in output_dict:
            val = output_dict[movie_id]
            val.append(rating)
        else:
            output_dict[movie_id] = [rating]
    for k, v in output_dict.items():
        avg = round(sum(v) / len(v), 1)
        output_dict[k] = avg
    return output_dict


def normalize_rating(ratings):
    output_list = []
    key_deleted = 'userId'
    key_deleted_2 = 'timestamp'
    for i in ratings:
        if key_deleted in i:
            del i[key_deleted]
        if key_deleted_2 in i:
            del i[key_deleted_2]
        i.update(rating=float(i['rating']), movieId=int(i['movieId']))
        output_list.append(i)
    return output_list


def normalize_movies(movies):
    output_list = []
    exp = r'.+\((\d{4})\)$'
    for i in movies:
        cur_title = i['title']
        if re.match(exp, cur_title):
            year = int(re.findall(exp, cur_title)[0])
            new_title = re.sub(r'(\(\d{4}\))$', '', cur_title).strip()
            i.update(year=year, title=new_title)
        else:
            i.update(year=-1)
        i.update(genres=i['genres'].split('|'), movieId=int(i['movieId']))
        output_list.append(i)

    return output_list


def read_input_file(file_name):
    with open(file_name, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        output_list = [row for row in reader]
    return output_list


if __name__ == '__main__':
    args = parse_args()
    movies = read_input_file(args.movies_file)
    ratings = read_input_file(args.ratings_file)
    movies = normalize_movies(movies)
    ratings = normalize_rating(ratings)
    ratings

    if args.regexp is not None:
        movies = filter_movies_by_name(movies, args.regexp)

    if args.genres is not None:
        movies = filter_genres(movies, args.genres)

    if args.year_from is not None:
        movies = filter_movies_by_year_from(movies, args.year_from)

    if args.year_to is not None:
        movies = filter_movies_by_year_to(movies, args.year_to)

    if args.rating is not None:
        ratings = filter_ratings(ratings, args.rating)

    movies = join(movies, ratings)
    movies = sort(movies)

    if args.number is not None:
        movies = first(movies, args.number)

    for r in movies:
        print(r['genres'], r['title'], r['year'], r['rating'])
