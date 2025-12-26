"""
Name: Anika Pawa
PennKey: pawa7
Recitation: 209
Program Execution: N/A, this file is not intended to be run directly,
                   as it is meant to be imported.
Description: This program implements a movie recommendation system using user-based
             collaborative filtering, generating personalized movie suggestions based
             on the similarity of users' genre preferences and past ratings.
"""

from collections import defaultdict
import json
from math import sqrt
import random

class MovieRecommender:
    def __init__(self, movie_info_filename: str, user_ratings_filename: str):
        """
        Inputs:
        movie_info_filename: name of JSON file containing mapping of movie IDs
                             to info
        user_ratings_filename: name of JSON file containing mapping of user
                               IDs to ratings
        """
        movie_info_file = open(movie_info_filename, "r")
        user_ratings_file = open(user_ratings_filename, "r")

        self.movie_info = MovieRecommender.read_from_json(movie_info_file)
        self.all_user_ratings = MovieRecommender.read_from_json(
            user_ratings_file
        )

        movie_info_file.close()
        user_ratings_file.close()

        self.all_user_preferences = {
            int(user_id): self.ratings_to_preferences(user_ratings)
            for user_id, user_ratings in self.all_user_ratings.items()
        }

    @staticmethod
    def read_from_json(file):
        """
        You don't need to do anything with this function!
        Inputs:
        file:   pointer to file containing the dictionary to process

        Returns:
        The dictionary represented by the JSON, transforming all string
        keys into int keys for consistency.
        """
        dictionary = {int(k): v for k, v in json.load(file).items()}
        for key in dictionary:
            value = dictionary[key]
            if isinstance(value, dict):
                dictionary[key] = {int(k): v for k, v in value.items()}
        return dictionary

    def add_new_ratings(self, new_ratings_filename: str):
        """
        You don't need to do anything with this function!
        Inputs:
        new_ratings_filename:   file of new ratings JSON to include.
        """
        new_ratings_file = open(new_ratings_filename, "r")
        new_ratings = MovieRecommender.read_from_json(new_ratings_file)
        new_ratings_file.close()

        new_preferences = {
            int(user_id): self.ratings_to_preferences(user_ratings)
            for user_id, user_ratings in new_ratings.items()
        }
        self.all_user_ratings.update(new_ratings)
        self.all_user_preferences.update(new_preferences)

    def ratings_to_preferences(
        self, user_ratings: dict[int, float]
    ) -> dict[str, float]:
        """
        Inputs:
        user_ratings        -   mapping of movie IDs to ratings,
                                representing one user's ratings.

        Returns:
        dict mapping movie genres to the average rating that the user awards
        to movies from that genre. If the user has never seen a movie
        belonging to some particular genre, then that genre will not be
        present as a key in dictionary that is returned
        """
        # sum of ratings per genre
        genre_totals = defaultdict(float)

        # number of movies rated per genre
        genre_counts = defaultdict(int)

        for movie_id, rating in user_ratings.items():
            # get genres for this movie
            genres = self.movie_info[movie_id][1]
            for genre in genres:
                genre_totals[genre] += rating
                genre_counts[genre] += 1

        # compute average rating per genre
        genre_averages = {
            genre: genre_totals[genre] / genre_counts[genre]
            for genre in genre_totals
        }

        return genre_averages

    @staticmethod
    def cosine_similarity(
        first: dict[str, float], second: dict[str, float]
    ) -> float:
        """Calculates the cosine similarity between the two users' ratings profiles.

        Args:
            first (dict[str, float]): first user's ratings profile
            second (dict[str, float]): second user's ratings profile

        Returns:
            float: cosine similarity of the two users' ratings profiles.
        """

        # compute numerator: sum of products for genres both users rated
        common_genres = set(first.keys()) & set(second.keys())
        numerator = sum(first[genre] * second[genre] for genre in common_genres)

        # compute denominator: product of magnitudes
        sum1 = sum(rating**2 for rating in first.values())
        sum2 = sum(rating**2 for rating in second.values())
        denominator = (sum1 ** 0.5) * (sum2 ** 0.5)

        # avoid division by zero
        if denominator == 0:
            return 0.0

        return numerator / denominator

    def find_similar_user_by_id(self, user_id: int) -> int:
        """Find the ID of a user who has the preferences
        that are most similar to the user whose ID was
        passed in as input.

        Args:
            user_id (int): ID of the user to find another similar user to

        Returns:
            int: id of the user with preferences most similar to the input
                 user; ties broken in favor of higher ID values.
        """

        # get the target user's genre preferences
        target_prefs = self.all_user_preferences[user_id]

        # initialize lower than possible cosine similarity
        best_similarity = -1
        most_similar_user = None

        # iterate through all users in the dataset
        for other_id, other_prefs in self.all_user_preferences.items():
            # only compare if this is not the target user
            if other_id != user_id:

                # compute cosine similarity between target user and this other user
                similarity = self.cosine_similarity(target_prefs, other_prefs)

                # check if this user has a higher similarity or ties with a higher
                # user ID
                higher_id = (similarity == best_similarity and other_id > most_similar_user)
                if similarity > best_similarity or higher_id:
                    best_similarity = similarity
                    most_similar_user = other_id

        return most_similar_user

    def make_recommendations_for_id(
        self, recommender_id: int, recipient_id: int
    ) -> set[str]:
        """Given a user who wants recommendations and another user, return a set of up to five
        movie names as recommendations.

        Args:
            recommender_id (int): id of the user whose ratings will be used as recommendation
            recipient_id (int): id of the user who wants a recommendation

        Returns:
            set[str]: a set of up to five movie titles. These movies must meet the criteria that
                      the recipient has not rated them, they are tagged with at least one of
                      the recipient's top two rated genres, and they are the most highly rated
                      movies by the recommender that meet the previous two conditions.
        """

        # collect needed data
        recommender_ratings = self.all_user_ratings[recommender_id]
        recipient_ratings = self.all_user_ratings[recipient_id]
        recipient_prefs = self.all_user_preferences[recipient_id]

        # if the recipient has no preference data at all, cannot identify top genres
        if len(recipient_prefs) == 0:
            return set()

        # identify top two genres
        # sort genres by their average rating (descending) and take the top two
        top_two_genres = [
            genre for genre, rating in
            sorted(recipient_prefs.items(), key=lambda item: item[1], reverse=True)[:2]
        ]

        top_two_genres = set(top_two_genres)

        # filter out movies the recipient has already rated
        unseen_movies = [
            movie_id for movie_id in self.movie_info
            if movie_id not in recipient_ratings
        ]

        # from unseen movies, keep only those matching at least one top genre
        # and that the recommender has rated
        candidate_movies = []
        for movie_id in unseen_movies:
            title, genres = self.movie_info[movie_id]

            # check shared genre
            has_shared_genre = False
            for g in genres:
                if g in top_two_genres:
                    has_shared_genre = True

                # recommender must have rated this movie
                if has_shared_genre and movie_id in recommender_ratings:
                    candidate_movies.append(movie_id)

        # no valid recommendations
        if len(candidate_movies) == 0:
            return set()

        # sort candidates by recommender’s rating (descending)
        best_movies = sorted(
            candidate_movies,
            key=lambda m_id: recommender_ratings[m_id],
            reverse=True
        )[:5]

        # convert movie IDs to titles and return
        return {self.movie_info[movie_id][0] for movie_id in best_movies}
