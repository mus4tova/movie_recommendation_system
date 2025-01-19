import re
import mlflow
import requests
from loguru import logger

from src.settings import TMDB_API_KEY


class DataLoader:
    def __init__(self):
        pass

    def extract_imdb_id(self, imdb_url):
        """
        Function to extract IMDb ID from link
        """
        try:
            # "tt" + from 5 to 9 numbers (IMDb ID length is usually 9 numbers)
            match = re.search(r"tt\d{5,9}", imdb_url)
            return match.group()
        except StopIteration:
            return "Unable to select movie id. Load another link"

    def get_movie_from_imdb(self, imdb_url):
        # Extract IMDb ID from link
        imdb_id = self.extract_imdb_id(imdb_url)
        if not imdb_id:
            logger.info("Error. Invalid IMDb URL")

        # Request a movie by IMDb ID
        tmdb_url = f"https://api.themoviedb.org/3/find/{imdb_id}"
        params = {"api_key": TMDB_API_KEY, "external_source": "imdb_id"}
        response = requests.get(tmdb_url, params=params)
        if response.status_code != 200:
            logger.info(
                f"Error. Failed to connect to TMDb API. Status code: {response.status_code}"
            )
            return {
                "error": f"Failed to connect to TMDb API. Status code: {response.status_code}"
            }

        data = response.json()
        #logger.info(f"Response: \n{data}")

        # Check if there is a result
        if not data.get("movie_results") and not data.get("tv_results"):
            logger.info(f"Error. No movie or TV show found for this IMDb ID")
            return {"error": "No movie or TV show found for this IMDb ID"}

        # Check if it's a movie or a TV series
        if data.get("movie_results"):
            movie = data["movie_results"][0]
            return {
                "type": "movie",
                "name": movie.get("title"),
                "overview": movie.get("overview"),
                "media_type": movie.get("media_type"),
                "original_language": movie.get("original_language"),
                "genre_ids": movie.get("genre_ids"),
                "popularity": movie.get("popularity"),
                "release_date": movie.get("release_date"),
                "vote_average": movie.get("vote_average"),
                "vote_count": movie.get("vote_count"),
                "origin_country": movie.get("origin_country"),
            }
        elif data.get("tv_results"):
            tv_show = data["tv_results"][0]
            return {
                "type": "tv_show",
                "name": tv_show.get("name"),
                "overview": tv_show.get("overview"),
                "media_type": tv_show.get("media_type"),
                "original_language": tv_show.get("original_language"),
                "genre_ids": tv_show.get("genre_ids"),
                "popularity": tv_show.get("popularity"),
                "first_air_date": tv_show.get("first_air_date"),
                "vote_average": tv_show.get("vote_average"),
                "vote_count": tv_show.get("vote_count"),
                "origin_country": tv_show.get("origin_country"),
            }

    def example(self, imdb_url):
        # Get result
        movie_data = self.get_movie_from_imdb(imdb_url)

        if "error" in movie_data:
            logger.info(f"Error: {movie_data['error']}")
        else:
            logger.info(f"Result: {movie_data}")
