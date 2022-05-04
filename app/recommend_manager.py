import pandas as pd
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity
import os

import warnings

warnings.filterwarnings("ignore")  # ignore warnings

class MovieManager():
    def __init__(self):
        self.item_similarity_df = self.load_recommendation()
        self.movie_watched = []

    def load_recommendation(self):
        item_similarity_df = pd.read_csv(
            r"dataset_collab/similarity_model.csv", index_col=0)
        print("DF LOADED")

        # TODO: CACHCE item_similarity_df

        return item_similarity_df

    def add_movie(self, movie):
        self.movie_watched.append(movie)

    def clear_movie(self):
        self.movie_watched.clear()

    def get_watched_movie(self):
        return self.movie_watched

    def check_seen(self, recommended_movies, watched_movies):
        for movie in watched_movies:
            if recommended_movies == movie[0]:
                return True
        return False

    def get_similar_movies(self, movie_name, user_ratings):
        try:
            similar_score = self.item_similarity_df[movie_name]*(
                user_ratings-2.5)
            similar_movies = similar_score.sort_values(ascending=False)
        except Exception as e:
            print(f"EXCEPTION: \n{e}")
            similar_movies = pd.Series([])

        return similar_movies

    def getRecommendations(self, watched_movies):
        print(
            f"*****************************Watched Movies:\n{watched_movies}")
        similar_movies = pd.DataFrame()

        #TODO: When only a single movie is watched it will not iterate
        for movie, rating in watched_movies:
            similar_movies = similar_movies.append(
                self.get_similar_movies(movie, rating), ignore_index=True)

        all_recommend = similar_movies.sum().sort_values(ascending=False)  

        print(
            f"*****************************ALL RECOMMENDED:\n{all_recommend}")

        recommended_movies = []

        for movie, score in all_recommend.iteritems():
            if not self.check_seen(movie, watched_movies):
                recommended_movies.append(movie)

        if len(recommended_movies) > 100:
            recommended_movies = recommended_movies[0:100]

        return recommended_movies


if __name__ == "__main__":
    #When running this py file add "app/dataset..." in path
    pass
    # movieManager = MovieManager()

    # movie_user = [
    #     ("Zombieland (2009)", 5),
    #     ("Zootopia (2016)", 1),
    #     ("10 Cloverfield Lane (2016)", 1),
    #     ("(500) Days of Summer (2009)", 3),
    #     ("10 Things I Hate About You (1999)", 3)
    # ]
    # movieManager.add_movie(["Zombieland (2009)", 5])
    # movieManager.add_movie(["Zootopia (2016)", 1])

    # recommended_movies = movieManager.getRecommendations(movieManager.get_watched_movie())
    # print(recommended_movies)

