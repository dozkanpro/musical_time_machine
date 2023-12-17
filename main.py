from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap5
from flask_paginate import Pagination, get_page_parameter
from wtforms import DateField, SubmitField
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from spotify import Spotify
import os

URL = "https://www.billboard.com/charts/hot-100/"

# Initiate Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
Bootstrap5(app)


# Create Form
class SongsDate(FlaskForm):
    date = DateField("Date", format='%Y-%m-%d', default=datetime.now())
    submit = SubmitField("Submit")


# Home page
@app.route('/', methods=["GET", "POST"])
def home():
    form = SongsDate()
    if form.validate_on_submit():
        songs_date = form.date.data
        print(songs_date)

        # Web Scrapping to get 100 top song list
        response = requests.get(url=f"{URL}{songs_date}")
        soup = BeautifulSoup(response.text, "html.parser")
        song_names_spans = soup.select("li ul li h3")
        song_names = [song.getText().strip() for song in song_names_spans]

        # Authenticate to Spotify
        my_spotify = Spotify()

        # Create Spotify playlist with 100 top song list
        playlist_url = my_spotify.create_list(song_names, songs_date)

        search = False
        q = request.args.get('q')
        if q:
            search = True

        page = request.args.get(get_page_parameter(), type=int, default=1)

        pagination = Pagination(page=page, total=len(song_names), search=search, css_framework='bootstrap5')

        page = request.args.get('page', type=int, default=1)
        print(page)
        per_page = 10  # Number of items per page
        offset = (page - 1) * per_page
        all_songs = song_names[offset:offset + per_page]

        # Create a Pagination object
        pagination = Pagination(page=page, per_page=per_page, total=len(song_names), css_framework='bootstrap5')

        return render_template("index.html", song_names=song_names, form=form, url=playlist_url, pagination=pagination)
    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
