import pandas as pd
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, jsonify , render_template

import warnings

warnings.filterwarnings("ignore")  # ignore warnings

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

    recommended_movies = getRecommendations(movie_user)

    return jsonify(recommended_movies)

# ------------------------------- BACKEND FUNCS ------------------------------ #


def load_recommendation():
    item_similarity_df = pd.read_csv(
        "dataset_collab/similarity_model.csv", index_col=0)
    print("DF LOADED")

    # TODO: CACHCE item_similarity_df

    return item_similarity_df


def check_seen(recommended_movies, watched_movies):
    for movie in watched_movies:
        if recommended_movies == movie[0]:
            return True
    return False


def get_similar_movies(movie_name, user_ratings):
    try:
        similar_score = item_similarity_df[movie_name]*(user_ratings-2.5)
        similar_movies = similar_score.sort_values(ascending=False)
    except:
        print("Don't have movie in model")
        similar_movies = pd.Series([])

    return similar_movies


def getRecommendations(watched_movies):
    print(f"*****************************Watched Movies:\n{watched_movies}")
    similar_movies = pd.DataFrame()

    for movie, rating in watched_movies:
        similar_movies = similar_movies.append(
            get_similar_movies(movie, rating), ignore_index=True)

    all_recommend = similar_movies.sum().sort_values(ascending=False)  # CLEAN

    print(f"*****************************ALL RECOMMENDED:\n{all_recommend}")

    recommended_movies = []

    for movie, score in all_recommend.iteritems():
        if not check_seen(movie, watched_movies):
            recommended_movies.append(movie)

    if len(recommended_movies) > 100:
        recommended_movies = recommended_movies[0:100]

    return recommended_movies


if __name__ == '__main__':
    item_similarity_df = load_recommendation()
    app.run()

# https://medium.com/code-heroku/how-to-turn-your-machine-learning-scripts-into-projects-you-can-demo-cbc5611ca442
