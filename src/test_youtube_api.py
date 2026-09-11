from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("YOUTUBE_API_KEY")

youtube = build("youtube", "v3", developerKey=api_key)

request = youtube.videos().list(
    part="snippet,statistics",
    id="dQw4w9WgXcQ"  # a well-known public video ID, just for testing
)
response = request.execute()

video = response["items"][0]
print("Title:", video["snippet"]["title"])
print("Views:", video["statistics"]["viewCount"])
print("Likes:", video["statistics"].get("likeCount", "N/A"))