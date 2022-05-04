import pandas as pd
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, jsonify , render_template
from recommend_manager import MovieManager

import warnings

warnings.filterwarnings("ignore")  # ignore warnings

movieManager = MovieManager()
app = Flask(__name__)

# ------------------------------- FLASK ROUTES ------------------------------- #


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/recommend", methods=["GET"])
def recommend_api():
    ''' API CALL '''
    movie_user = [
        ("Zombieland (2009)", 5),
        ("Zootopia (2016)", 1),
        ("10 Cloverfield Lane (2016)", 1),
        ("(500) Days of Summer (2009)", 3),
        ("10 Things I Hate About You (1999)", 3)
    ]

    recommended_movies = movieManager.getRecommendations(movie_user)

    return jsonify(recommended_movies)

# ------------------------------- BACKEND FUNCS ------------------------------ #



if __name__ == '__main__':
    app.run(debug = True)

# https://medium.com/code-heroku/how-to-turn-your-machine-learning-scripts-into-projects-you-can-demo-cbc5611ca442
