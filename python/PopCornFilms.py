from flask import Flask, render_template, request, redirect, url_for, session, Markup, flash
import re
import os
import sqlite3
import requests
from tmdbv3api import Movie
from tmdbv3api import TMDb
from tmdbv3api import TV
from tmdbv3api import Person

tmdb = TMDb()
tmdb.api_key = '85a4b4ec78f11d3bc5735bb89ddd4385'

folder = os.getcwd()

mov = Movie()
tv = TV()
per = Person()
app = Flask(__name__, template_folder=folder, static_folder=folder)



# API-----------------------------------------------------------------------------------------
url_top_rated_movies = "https://api.themoviedb.org/3/movie/top_rated?language=en-US&page=1"
url_upcoming_movies = "https://api.themoviedb.org/3/movie/upcoming"
url_now_playing = "https://api.themoviedb.org/3/movie/now_playing"
url_popular = "https://api.themoviedb.org/3/tv/popular?language=en-US&page=1"


headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4NWE0YjRlYzc4ZjExZDNiYzU3MzViYjg5ZGRkNDM4NSIsInN1YiI6IjY0N2NmNzM2MjYzNDYyMDEzMzcxMjI4NCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.rpmd2_LuHwcodLsPS48IVcuy3nn6FKzU_OOS_rxJIvs"
}

response_top_films = requests.get(url_top_rated_movies, headers=headers).json()
response_upcoming_films = requests.get(url_upcoming_movies, headers=headers).json()
response_now_playing = requests.get(url_now_playing, headers=headers).json()
response_popular = requests.get(url_popular, headers=headers).json()
# API-----------------------------------------------------------------------------------------



# re(maybe useless)-----------------------------------------------------------------------------------------
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

def check(email):
 
    if(re.fullmatch(regex, email)):
        return "Valid Email"
 
    else:
        return "Invalid Email"
# re(maybe useless)-----------------------------------------------------------------------------------------



# database-----------------------------------------------------------------------------------------
connect = sqlite3.connect("other/userss.db", check_same_thread=False)
cursor = connect.cursor()

user_table = "users"
create_table_query = f"""CREATE TABLE IF NOT EXISTS {user_table} (nickname TEXT, email TEXT, password TEXT);"""
cursor.execute(create_table_query)

genres_table = "genres"
create_table_genres = f"""CREATE TABLE IF NOT EXISTS {genres_table} (nickname TEXT, email TEXT, password TEXT);"""
cursor.execute(create_table_genres)


def regval(cursor, table, column, value):
            query = 'SELECT 1 from {} WHERE {} = ? LIMIT 1'.format(table, column)
            return cursor.execute(query, (value,)).fetchone() is not None
# database-----------------------------------------------------------------------------------------



# main window-----------------------------------------------------------------------------------------
@app.route("/", methods=["GET"])
def index():
    
    return render_template("templates/main_window.html", 
                           response_top_films=response_top_films, 
                           response_upcoming_films=response_upcoming_films, 
                           response_now_playing=response_now_playing,
                           response_popular=response_popular
                           )
# main window-----------------------------------------------------------------------------------------



# registration-----------------------------------------------------------------------------------------
@app.route("/registration", methods=["POST"])
def registration():
        what_nickname = request.form['username']
        what_email = request.form['email']
        what_password = request.form['password']
        if check(what_email) == 'Valid Email':
            if regval(cursor, 'users', 'email', what_email):
                print('exists')
            else:
                cursor.execute("INSERT INTO users (nickname, email, password) VALUES (?, ?, ?)", (what_nickname, what_email, what_password))
                connect.commit()

        else:
             print('invalid')
        
        return render_template('templates/login.html')


@app.route("/reg", methods=["POST"])
def reg():
    return render_template("templates/reg.html")
# registration-----------------------------------------------------------------------------------------



# login-----------------------------------------------------------------------------------------
@app.route("/login", methods=["POST"])
def login():
    what_email = request.form['email']
    what_password = request.form['password']
    if check(what_email) == 'Valid Email':
        if regval(cursor, 'users', 'email', what_email) and regval(cursor, 'users', 'password', what_password):
            print('YES')
            connect.commit()
            return render_template('templates/main_window.html',
                            response_top_films=response_top_films, 
                           response_upcoming_films=response_upcoming_films, 
                           response_now_playing=response_now_playing,
                           response_popular=response_popular)
            
        else:
            print('NO')
    else:
        print('invalid')
        return render_template('templates/login.html')
    

@app.route("/log", methods=["POST"])
def log():
    return render_template("templates/login.html")
# login-----------------------------------------------------------------------------------------



# upcoming movies-----------------------------------------------------------------------------------------
@app.route("/upcoming")
def upcoming():
    return render_template('templates/upcoming.html', response_upcoming_films=response_upcoming_films)
# upcoming movies-----------------------------------------------------------------------------------------



# top rated movies-----------------------------------------------------------------------------------------
@app.route("/top_rated/<int:page_num>")
def top_rated(page_num):
    return render_template('templates/topratedfilms.html', response_top_films=response_top_films, page_num=page_num)

@app.route("/top_rated/next/<int:page_num>")
def next_top(page_num):
    page_num +=1
    url_top_rated_movies = f"https://api.themoviedb.org/3/movie/top_rated?language=en-US&page={page_num}"
    response_top_films = requests.get(url_top_rated_movies, headers=headers).json()
    return render_template('templates/topratedfilms.html', response_top_films=response_top_films, page_num=page_num)

@app.route("/top_rated/back/<int:page_num>")
def previous_top(page_num):
    if page_num >= 2:
        page_num -=1
        url_top_rated_movies = f"https://api.themoviedb.org/3/movie/top_rated?language=en-US&page={page_num}"
        response_top_films = requests.get(url_top_rated_movies, headers=headers).json()
        return render_template('templates/topratedfilms.html', response_top_films=response_top_films, page_num=page_num)
# top rated movies-----------------------------------------------------------------------------------------



# popular movies-----------------------------------------------------------------------------------------
@app.route("/popular/<int:page_num>")
def popular():
    return render_template('templates/popular_films.html', response_popular=response_popular)

@app.route("/popular/next/<int:page_num>")
def next_popular(page_num):
    page_num +=1
    url_popular = f"https://api.themoviedb.org/3/tv/popular?language=en-US&page={page_num}"
    response_popular = requests.get(url_popular, headers=headers).json()
    return render_template('templates/popular_films.html', response_popular=response_popular, page_num=page_num)

@app.route("/popular/back/<int:page_num>")
def previous_popular(page_num):
    if page_num >= 2:
        page_num -=1
        url_popular = f"https://api.themoviedb.org/3/tv/popular?language=en-US&page={page_num}"
        response_popular = requests.get(url_popular, headers=headers).json()
        return render_template('templates/popular_films.html', response_popular=response_popular, page_num=page_num)
# popular movies-----------------------------------------------------------------------------------------



# movie info-----------------------------------------------------------------------------------------
@app.route("/info/movie/id=<int:movie_id>")
def info_movie(movie_id):
    m = mov.details(movie_id)
    movie_title = m.title
    movie_overview = m.overview
    poster = m.poster_path
    rating = m.vote_average
    rating = round(rating/10*100)
    release_date = m.release_date
    release_date = release_date[:-6]
    similar = mov.similar(movie_id)
    budget = m.budget
    homepage = m.homepage
    tagline = m.tagline 
    votecount = m.vote_count
    genres = m.genres
    url_credits = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    response_credits = requests.get(url_credits, headers=headers).json()
    return render_template('templates/info_movie.html', **locals())
# movie info-----------------------------------------------------------------------------------------



# person info-----------------------------------------------------------------------------------------
@app.route("/info/person/id=<int:person_id>")
def person_info(person_id):
    person = per.details(person_id)
    name = person.name
    biography = person.biography
    profile_path = person.profile_path
    place_of_birth = person.place_of_birth
    birthday = person.birthday
    gender = person.gender
    deathday = person.deathday
    return render_template('templates/person_info.html', **locals())
# person info-----------------------------------------------------------------------------------------



# search-----------------------------------------------------------------------------------------
@app.route("/search", methods=["POST"])
def search():
    what = request.form['search']
    search = mov.search(what)
    return render_template("templates/search.html", search=search, what=what)
# search-----------------------------------------------------------------------------------------



# loop-----------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.debug = True
    app.run()
    