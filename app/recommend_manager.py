import pandas as pd
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity
import os

import warnings

warnings.filterwarnings("ignore")  # ignore warnings

class MovieManager():
    def __init__(self):
        self.item_similarity_df = self.load_recommendation()
        self.movie_dict = self.load_movie_dict() 
        self.movie_watched = []
        self.recommended_movies_index = []

    def load_recommendation(self):
        item_similarity_df = pd.read_csv(
            r"data/similarity_model.csv", index_col=0)
        print("DF LOADED")
        return item_similarity_df

    def load_movie_dict(self):
        movie_pd = pd.read_csv(
            r"data/movie_list.csv", index_col=0)
        movie_dict = movie_pd.to_dict()["title"]
        print("MOVIE DICT LOADED")
        return movie_dict

    def get_movie_list(self):
        movie_pd = pd.read_csv(
            r"data/movie_list.csv", index_col=0)
        movie_list = self.movie_dict
        movie_list = list(movie_list.values()) 

        return movie_list


    def add_movie(self, movie):
        self.movie_watched.append(movie)

    def clear_movie(self):
        self.movie_watched.clear()

    def get_watched_movie(self):
        return self.movie_watched

    def get_a_movie_index(self , movie):
        for movie_id , movie_name in self.movie_watched.items():
            if movie_name == movie:
                return movie_id

    def getRecommendations(self, watched_movies):
        ''' Return a list of recommended movies using collaborative filtering'''

        print(
            f"*****************************Watched Movies:\n{watched_movies}")
        similar_movies = pd.DataFrame()

        for movie, rating in watched_movies:
            similar_movies = similar_movies.append(
                self.get_similar_movie(movie, rating), ignore_index=True)

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

    def get_similar_movie(self, movie_name, user_ratings):
        try:
            similar_score = self.item_similarity_df[movie_name]*(
                user_ratings-2.5)
            similar_movies = similar_score.sort_values(ascending=False)
        except Exception as e:
            print(f"EXCEPTION: \n{e}")
            similar_movies = pd.Series([])

        return similar_movies

    def check_seen(self, recommended_movies, watched_movies):
        for movie in watched_movies:
            if recommended_movies == movie[0]:
                return True
        return False


    def get_all_movies_index(self , recommended_movies):
        for movie in recommended_movies:
            self.recommended_movies_index.append(self.get_a_movie_index(movie))
        return self.recommended_movies_index
        

    def get_a_movie_index(self, search_movie):
        for movie_id , movie_name in self.movie_dict.items():
            if movie_name == search_movie:
                return movie_id

    def clear_movie_index(self):
        self.recommended_movies_index.clear()
        print("Cleared all recommended movies index")


if __name__ == "__main__":
    #When running this py file add "app/dataset..." in path
    # pass
    movieManager = MovieManager()

    print(movieManager.get_movie_list())

    # movieDict = movieManager.load_movie_dict()
    # print(list(movieDict.values()))

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

    # recommended_movies_index = []
    # for movie in recommended_movies:
    #     recommended_movies_index.append(movieManager.get_a_movie_index(movie))

    # print(recommended_movies_index)

    # movieManager.get_all_movies_index(recommended_movies)
    # print("----------------------------")
    # print(movieManager.recommended_movies_index)


    # print(type(movieManager.recommended_movies_index))
    # print(type(recommended_movies))

    # combined_dict = dict(zip(movieManager.recommended_movies_index , recommended_movies))
    # print(type(combined_dict))
    # print(combined_dict)
    # print(combined_dict[79702])
        

