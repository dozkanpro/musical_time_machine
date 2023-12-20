from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap5
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
        print(len(song_names))
        # Authenticate to Spotify
        my_spotify = Spotify()

        # Create Spotify playlist with 100 top song list
        playlist_url = my_spotify.create_list(song_names, songs_date)

        return render_template("index.html", song_names=song_names, form=form, url=playlist_url)
    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
