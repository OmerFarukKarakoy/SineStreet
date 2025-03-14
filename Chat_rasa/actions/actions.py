# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import List, Text, Dict, Any
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import json

# Load movie data
def load_movies():
    with open('film.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['movies']

MOVIES = load_movies()

class ActionRecommendMovie(Action):
    def name(self) -> Text:
        return "action_recommend_movie"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Extract slots
        genre = tracker.get_slot("genre")
        year = tracker.get_slot("year")
        rating = tracker.get_slot("rating")

        # Filter movies based on slots
        filtered_movies = MOVIES

        if genre:
            filtered_movies = [movie for movie in filtered_movies if genre.lower() in [g.lower() for g in movie['genre']]]

        if year:
            if "before" in year.lower():
                year_limit = int(year.split()[0])
                filtered_movies = [movie for movie in filtered_movies if movie['release_year'] < year_limit]
            elif "after" in year.lower():
                year_limit = int(year.split()[0])
                filtered_movies = [movie for movie in filtered_movies if movie['release_year'] > year_limit]

        if rating:
            try:
                filtered_movies = [movie for movie in filtered_movies if movie['rating'] >= float(rating)]
            except ValueError:
                dispatcher.utter_message(text="Geçerli bir IMDb puanı giriniz.")
                return []

        # Generate response
        if filtered_movies:
            response = "\n".join([
                f"- {movie['title']} ({movie['release_year']}) - IMDb: {movie['rating']}" for movie in filtered_movies[:5]
            ])
            dispatcher.utter_message(text=f"İşte önerdiğim filmler:\n{response}")
        else:
            dispatcher.utter_message(text="Maalesef, kriterlerinize uygun film bulamadım.")

        return []

class ActionSetGenre(Action):
    def name(self) -> Text:
        return "action_set_genre"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        genre = tracker.latest_message.get("text")
        dispatcher.utter_message(text=f"{genre} türünde filmler arıyorsunuz.")
        return [SlotSet("genre", genre)]

class ActionRecommendByActor(Action):
    def name(self) -> Text:
        return "action_recommend_by_actor"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        actor = tracker.get_slot("actor")
        if not actor:
            dispatcher.utter_message(text="Lütfen bir oyuncu adı belirtin.")
            return []

        filtered_movies = [movie for movie in MOVIES if actor.lower() in [a.lower() for a in movie['actors']]]

        if filtered_movies:
            response = "\n".join([
                f"- {movie['title']} ({movie['release_year']}) - IMDb: {movie['rating']}" for movie in filtered_movies[:5]
            ])
            dispatcher.utter_message(text=f"{actor} ile ilgili önerdiğim filmler:\n{response}")
        else:
            dispatcher.utter_message(text=f"Maalesef, {actor} ile ilgili film bulamadım.")

        return []

class ActionRecommendByDirector(Action):
    def name(self) -> Text:
        return "action_recommend_by_director"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        director = tracker.get_slot("director")
        if not director:
            dispatcher.utter_message(text="Lütfen bir yönetmen adı belirtin.")
            return []

        filtered_movies = [movie for movie in MOVIES if director.lower() in movie['director'].lower()]

        if filtered_movies:
            response = "\n".join([
                f"- {movie['title']} ({movie['release_year']}) - IMDb: {movie['rating']}" for movie in filtered_movies[:5]
            ])
            dispatcher.utter_message(text=f"{director} tarafından yönetilen filmler:\n{response}")
        else:
            dispatcher.utter_message(text=f"Maalesef, {director} tarafından yönetilen bir film bulamadım.")

        return []

class ActionRecommendByRating(Action):
    def name(self) -> Text:
        return "action_recommend_by_rating"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        rating = tracker.get_slot("rating")
        if not rating:
            dispatcher.utter_message(text="Lütfen bir IMDb puanı belirtin.")
            return []

        try:
            filtered_movies = [movie for movie in MOVIES if movie['rating'] >= float(rating)]
        except ValueError:
            dispatcher.utter_message(text="Geçerli bir IMDb puanı giriniz.")
            return []

        if filtered_movies:
            response = "\n".join([
                f"- {movie['title']} ({movie['release_year']}) - IMDb: {movie['rating']}" for movie in filtered_movies[:5]
            ])
            dispatcher.utter_message(text=f"{rating} ve üstü puanlı önerilerim:\n{response}")
        else:
            dispatcher.utter_message(text=f"Maalesef, {rating} ve üstü puanlı film bulamadım.")

        return []

class ActionMovieDetail(Action):
    def name(self) -> Text:
        return "action_movie_detail"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        movie_title = tracker.latest_message.get("text")
        filtered_movies = [movie for movie in MOVIES if movie_title.lower() in movie['title'].lower()]

        if filtered_movies:
            movie = filtered_movies[0]
            response = (f"Film: {movie['title']}\n"
                        f"Tür: {', '.join(movie['genre'])}\n"
                        f"Yıl: {movie['release_year']}\n"
                        f"IMDb: {movie['rating']}\n"
                        f"Yönetmen: {movie['director']}\n"
                        f"Oyuncular: {', '.join(movie['actors'])}\n"
                        f"Konu: {movie['plot']}")
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text="Maalesef, bu film hakkında bilgi bulamadım.")

        return []
