import requests
import json
import re
import os

def fetch_youtube_video_data(video_id, api_key, video_type):
    """Fetch detailed video data using YouTube Data API."""
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet,statistics",
        "id": video_id,
        "key": api_key
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if "items" in data and len(data["items"]) > 0:
            video_info = data["items"][0]
            stats = video_info.get("statistics", {})
            snippet = video_info.get("snippet", {})
            
            # Extract details
            title = snippet.get("title", "N/A")
            description = snippet.get("description", "")
            channel_title = snippet.get("channelTitle", "N/A")
            published_at = snippet.get("publishedAt", "N/A")
            hashtags = extract_hashtags(title + " " + description)
            
            # Truncate description to fit within size limit (8000 bytes)
            
            
            return {
                "video_id": video_id,
                "video_type": video_type,
                "title": title,
                
                "channel": channel_title,
                "published_date": published_at,
                "likes": stats.get("likeCount", "N/A"),
                "comments": stats.get("commentCount", "N/A"),
                "hashtags": hashtags
            }
        else:
            print(f"No data found for video ID: {video_id}")
            return None
    else:
        print(f"Error fetching video data: {response.status_code}, {response.json()}")
        return None

def extract_hashtags(text):
    """Extract hashtags from a given text."""
    return re.findall(r"#\w+", text)

def truncate_to_fit(text, max_length=8000):
    """Truncate text to ensure it fits within the specified byte size limit."""
    # Ensure the text does not exceed the byte size limit
    encoded_text = text.encode('utf-8')
    if len(encoded_text) > max_length:
        return encoded_text[:max_length].decode('utf-8', 'ignore')  # Truncate if too long
    return text

def append_data_to_json(data, filename="youtube_video_data.json"):
    """Append new data to an existing JSON file or create a new file."""
    if os.path.exists(filename):
        with open(filename, "r") as json_file:
            existing_data = json.load(json_file)
    else:
        existing_data = []
    
    existing_data.append(data)
    
    with open(filename, "w") as json_file:
        json.dump(existing_data, json_file, indent=4)
    print(f"Data appended to {filename}")

def extract_video_id_and_type(url):
    """Extract video ID and determine video type (YouTube/Shorts)."""
    if "youtube.com/shorts/" in url:
        return url.split("shorts/")[1].split("?")[0], "Shorts"
    elif "youtube.com/watch?v=" in url:
        return url.split("v=")[1].split("&")[0], "YouTube"
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0], "YouTube"  # Handling shortened URLs
    else:
        print(f"Invalid URL format: {url}")
        return None, None

def process_urls_from_file(file_path, api_key, output_file="youtube_video_data.json"):
    """Read video URLs from a text file and fetch data for each."""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    with open(file_path, "r") as file:
        urls = file.readlines()
    
    for url in urls:
        url = url.strip()
        video_id, video_type = extract_video_id_and_type(url)
        if video_id:
            video_data = fetch_youtube_video_data(video_id, api_key, video_type)
            if video_data:
                append_data_to_json(video_data, output_file)

def main():
    # Replace this with your actual YouTube Data API key
    api_key = "AIzaSyCHUfKUWyvMckHryTVj8lx6xRsoBog0M-Y"
    
    # Replace this with the path to your text file containing YouTube URLs
    input_file = "C:/Users/hp/Desktop/datascraper/youtube_links.txt"
    
    # Output JSON file to store video data
    output_file = "youtube_video_data.json"
    
    # Process URLs and fetch data
    process_urls_from_file(input_file, api_key, output_file)

if __name__ == "__main__":
    main()
