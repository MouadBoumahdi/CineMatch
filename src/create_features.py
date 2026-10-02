import json

import pandas as pd


with open("data/processed/movies.json", encoding="utf-8") as file:
    movies = pd.DataFrame(json.load(file))

dates = pd.to_datetime(movies["release_date"], errors="coerce")
movies["release_year"] = dates.dt.year.astype("Int64")
movies["release_month"] = dates.dt.month.astype("Int64")
movies["decade"] = (movies["release_year"] // 10) * 10

movies["genre_count"] = movies["genres"].apply(len)
movies["keyword_count"] = movies["keywords"].apply(len)
movies["overview_word_count"] = movies["overview"].fillna("").str.split().str.len()
movies["runtime_category"] = pd.cut(
    movies["runtime"],
    bins=[0, 90, 120, float("inf")],
    labels=["short", "medium", "long"],
    right=False,
)

feature_columns = [
    "movie_id", "release_year", "release_month", "decade",
    "genre_count", "keyword_count", "overview_word_count", "runtime_category",
]
features = movies[feature_columns]
features.to_json("data/processed/movie_features.json", orient="records", indent=2)

print("Films with features:", len(features))
print("Missing release years:", features["release_year"].isna().sum())
print("Missing runtime categories:", features["runtime_category"].isna().sum())
print("Saved: data/processed/movie_features.json")
