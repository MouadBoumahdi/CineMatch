import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


with open("data/processed/movies.json", encoding="utf-8") as file:
    movies = pd.DataFrame(json.load(file))

movies["year"] = pd.to_datetime(movies["release_date"], errors="coerce").dt.year
os.makedirs("data/processed/plots", exist_ok=True)
sns.set_theme(style="whitegrid")


def save_plot(name):
    plt.tight_layout()
    plt.savefig(f"data/processed/plots/{name}.png", dpi=150)
    plt.close()


# Ratings and popularity
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
sns.histplot(movies["vote_average"], bins=30, ax=axes[0])
axes[0].set(title="Ratings", xlabel="Average rating (0–10)")
pop_limit = movies["popularity"].quantile(0.99)
sns.histplot(movies.loc[movies["popularity"] <= pop_limit, "popularity"], bins=30, ax=axes[1])
axes[1].set(title="Popularity (up to 99th percentile)", xlabel="Popularity")
save_plot("ratings_popularity")

# Films by genre
genre_counts = movies["genres"].explode().dropna().value_counts()
plt.figure(figsize=(9, 5))
sns.barplot(x=genre_counts.head(10).values, y=genre_counts.head(10).index, color="steelblue")
plt.title("Top 10 genres")
plt.xlabel("Number of films")
save_plot("genres")

# Releases by year
year_counts = movies["year"].dropna().astype(int).value_counts().sort_index()
plt.figure(figsize=(10, 4))
plt.plot(year_counts.index, year_counts.values)
plt.title("Films by release year")
plt.xlabel("Year")
plt.ylabel("Number of films")
save_plot("releases_by_year")

# Runtime
plt.figure(figsize=(8, 4))
sns.histplot(movies["runtime"].dropna(), bins=35)
plt.axvline(movies["runtime"].median(), color="red", label="Median")
plt.title("Runtime distribution")
plt.xlabel("Minutes")
plt.legend()
save_plot("runtime")

# Budget and revenue: zeros are excluded because they may mean unknown.
financial = movies[(movies["budget"] > 0) & (movies["revenue"] > 0)]
plt.figure(figsize=(7, 5))
sns.scatterplot(data=financial, x="budget", y="revenue", alpha=0.35, s=18)
plt.xscale("log")
plt.yscale("log")
plt.title("Budget and revenue (positive values)")
save_plot("budget_revenue")

# Votes and popularity
voted = movies[movies["vote_count"] > 0]
plt.figure(figsize=(7, 5))
sns.scatterplot(data=voted, x="vote_count", y="popularity", alpha=0.35, s=18)
plt.xscale("log")
plt.yscale("log")
plt.title("Votes and popularity (films with votes)")
save_plot("votes_popularity")

# Boxplots of runtime for the most common genres
top_genres = genre_counts.head(5).index.tolist()
runtime_by_genre = movies[["genres", "runtime"]].explode("genres").dropna()
runtime_by_genre = runtime_by_genre[runtime_by_genre["genres"].isin(top_genres)]
plt.figure(figsize=(9, 5))
sns.boxplot(data=runtime_by_genre, x="genres", y="runtime", order=top_genres, showfliers=False)
plt.title("Runtime by genre (five most common genres)")
plt.xlabel("Genre")
plt.ylabel("Minutes")
save_plot("runtime_boxplots")

# Correlations between numeric columns
numeric = ["runtime", "budget", "revenue", "popularity", "vote_average", "vote_count"]
correlation_data = movies[numeric].copy()
correlation_data["budget"] = correlation_data["budget"].replace(0, float("nan"))
correlation_data["revenue"] = correlation_data["revenue"].replace(0, float("nan"))
correlations = correlation_data.corr()
plt.figure(figsize=(8, 6))
sns.heatmap(correlations, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1)
plt.title("Numeric correlations")
save_plot("correlations")

print("Saved 8 charts in data/processed/plots/")
