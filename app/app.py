import pandas as pd
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, jsonify , render_template , flash
from recommend_manager import MovieManager

import warnings

warnings.filterwarnings("ignore")  # ignore warnings

movieManager = MovieManager()
app = Flask(__name__)
app.config.update(
    TESTING = True,
    SECRET_KEY = "password"
)

# ------------------------------- FLASK ROUTES ------------------------------- #


@app.route("/" , methods=["POST" , "GET"])
def home():
    error = False
    error_message = ""

    try:
        if request.method == "POST":
            movie_form_input = request.form["movie_input"]
            try:
                rating_form_input = int(request.form["rating_input"])
            except Exception as e:
                print("EXCEPTION: at rating_form_input")


            if movie_form_input and rating_form_input:
                movieManager.add_movie([movie_form_input , rating_form_input])
                flash(f"Successfully added [{movie_form_input}]" , "info")
            else:
                error = True
                error_message = "Movie Input box Empty"
                print("No movie Added , Detected Empty form")


            print(f"{movie_form_input} added")
    except Exception as e:
        print(f"EXCEPTION AT HOME: {e}")
        print("MOVIE NOT IN DB")

    return render_template("index.html" , error = error , error_msg = error_message)


@app.route("/get_recommend", methods=["POST"])
def get_recommendation():
    recommended_movies = movieManager.getRecommendations(movieManager.get_watched_movie())

    return jsonify('',render_template('dynamic_movies.html', RECO_MOVIES = recommended_movies))

@app.route("/display_recommendation")
def display_recommendation():
    '''
        when get_recommendation is clicked
            display all recommended movies
    '''
    pass

@app.route("/clear_movies" , methods=["POST" , "GET"])
def clear_existing_movies():
    movieManager.clear_movie()
    log_message = "Movies Cleared"
    print("Movies Cleared")

    return jsonify('',render_template('dynamic_movies.html' , LOG = log_message))

if __name__ == '__main__':
    app.run(debug = True)

