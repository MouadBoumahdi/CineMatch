import json
import os
import time

import requests
from dotenv import load_dotenv


TARGET_MOVIES = 3000
RAW_FILE = "data/raw/tmdb_raw.json"

load_dotenv()
token = os.getenv("TMDB_TOKEN")
if not token:
    raise SystemExit("Add TMDB_TOKEN to .env first.")

headers = {"Authorization": f"Bearer {token}"}


def get_json(url, params):
    for attempt in range(1, 4):
        response = requests.get(url, headers=headers, params=params, timeout=20)
        if response.status_code == 429:
            print("Too many requests. Waiting 10 seconds. Attempt", attempt, "of 3")
            time.sleep(10)
            continue
        response.raise_for_status()
        data = response.json()
        if not data:
            raise ValueError("TMDB returned an empty response.")
        return data
    raise RuntimeError("TMDB is still limiting requests. Try again later.")


if os.path.exists(RAW_FILE):
    with open(RAW_FILE, encoding="utf-8") as file:
        raw = json.load(file)
else:
    raw = {"pages": {}, "movie_details": {}}


def save_raw():
    with open(RAW_FILE, "w", encoding="utf-8") as file:
        json.dump(raw, file, ensure_ascii=False, indent=2)


page_number = 1
while len(raw["movie_details"]) < TARGET_MOVIES:
    page_key = str(page_number)
    if page_key in raw["pages"]:
        page = raw["pages"][page_key]
    else:
        page_url = "https://api.themoviedb.org/3/discover/movie"
        page_options = {"page": page_number, "language": "en-US"}
        page = get_json(page_url, page_options)
        raw["pages"][page_key] = page
        save_raw()
    films = page.get("results", [])
    if not films:
        break

    for film in films:
        movie_id = str(film["id"])
        if movie_id in raw["movie_details"]:
            continue

        movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        movie_options = {"language": "en-US", "append_to_response": "keywords"}
        movie_data = get_json(movie_url, movie_options)
        raw["movie_details"][movie_id] = movie_data
        save_raw()

        if len(raw["movie_details"]) >= TARGET_MOVIES:
            break

    print("Page", page_number, "- films saved:", len(raw["movie_details"]))
    total_pages = page["total_pages"]
    if page_number >= total_pages:
        break
    page_number += 1





    

print("Finished:", len(raw["movie_details"]), "films in", RAW_FILE)
