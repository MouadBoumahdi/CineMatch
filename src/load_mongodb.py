import json
import os
from datetime import datetime

from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()
mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
client.admin.command("ping")
movies_collection = client["cinematch"]["movies"]
movies_collection.create_index("movie_id", unique=True)

with open("data/processed/movies.json", encoding="utf-8") as file:
    movies = json.load(file)

for movie in movies:
    if movie["release_date"]:
        movie["release_date"] = datetime.fromisoformat(movie["release_date"])
    movies_collection.replace_one({"movie_id": movie["movie_id"]}, movie, upsert=True)

print("Films in MongoDB:", movies_collection.count_documents({}))

print("French-language films:")
for movie in movies_collection.find(
    {"original_language": "fr"}, {"_id": 0, "title": 1}
).limit(5):
    print(movie)

print("Highly rated films:")
for movie in movies_collection.find(
    {"vote_average": {"$gte": 8}}, {"_id": 0, "title": 1, "vote_average": 1}
).limit(5):
    print(movie)

print("Top genres:")
pipeline = [
    {"$unwind": "$genres"},
    {"$group": {"_id": "$genres", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 10},
]
for result in movies_collection.aggregate(pipeline):
    print(result)

client.close()
