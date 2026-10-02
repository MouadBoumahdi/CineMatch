import json

import pandas as pd


# 1. Read the detailed films saved by Step 1.
with open("data/raw/tmdb_raw.json", encoding="utf-8") as file:
    raw = json.load(file)

movies = pd.DataFrame(raw["movie_details"].values())
movies = movies.rename(columns={"id": "movie_id"})
columns = [
    "movie_id", "title", "overview", "release_date", "runtime",
    "original_language", "genres", "keywords", "budget", "revenue",
    "popularity", "vote_average", "vote_count",
]
movies = movies[columns].copy()

# 2. Inspect the data before changing it.
numeric = ["runtime", "budget", "revenue", "popularity", "vote_average", "vote_count"]
categorical = ["original_language", "genres"]
text = ["title", "overview", "keywords"]

print("Films:", len(movies))
print("Column types:\n", movies.dtypes.to_string())
print("Missing values:\n", movies.isna().sum().to_string())
print("Duplicate IDs:", movies.duplicated("movie_id").sum())
print("Zero runtimes:", (movies["runtime"] == 0).sum())
print("Zero budgets:", (movies["budget"] == 0).sum())
print("Zero revenues:", (movies["revenue"] == 0).sum())
print("Negative numbers:", (movies[numeric] < 0).sum().sum())
print("Invalid ratings:", (~movies["vote_average"].between(0, 10)).sum())
print("Numeric:", numeric)
print("Categorical:", categorical)
print("Text:", text)

# 3. Clean duplicates, numbers, dates, and text.
movies = movies.drop_duplicates("movie_id")
for column in numeric:
    movies[column] = pd.to_numeric(movies[column], errors="coerce")
    movies.loc[movies[column] < 0, column] = None

movies.loc[movies["runtime"] == 0, "runtime"] = None
movies.loc[movies["vote_average"] > 10, "vote_average"] = None
movies["release_date"] = pd.to_datetime(movies["release_date"], errors="coerce")

for column in ["title", "overview", "original_language"]:
    movies[column] = movies[column].fillna("").str.strip()


def genre_names(genres):
    return [genre["name"] for genre in genres]


def keyword_names(data):
    return [keyword["name"] for keyword in data["keywords"]]


movies["genres"] = movies["genres"].apply(genre_names)
movies["keywords"] = movies["keywords"].apply(keyword_names)

# 4. Check the cleaned data and save it.
print("Empty overviews:", (movies["overview"] == "").sum())
print("Empty genres:", movies["genres"].apply(len).eq(0).sum())
print("Empty keywords:", movies["keywords"].apply(len).eq(0).sum())
print("Missing dates:", movies["release_date"].isna().sum())
print("Missing runtimes:", movies["runtime"].isna().sum())

movies.to_json(
    "data/processed/movies.json", orient="records", date_format="iso",
    force_ascii=False, indent=2,
)
print("Saved", len(movies), "clean films in data/processed/movies.json")
