import requests
from datetime import datetime

def search_youtube_shorts(query, api_key):
    """Search YouTube for Shorts based on the input query."""
    # URL for the YouTube search API
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",  # We are only looking for video results
        "videoDuration": "short",  # Filter for short videos (YouTube Shorts typically are under 60 seconds)
        "key": api_key
    }

    # Send request to YouTube API
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        video_links = []
        
        for item in data.get("items", []):
            # Get video ID from the response
            video_id = item["id"].get("videoId")
            if video_id:
                # Format it as a YouTube Shorts link
                shorts_url = f"https://www.youtube.com/shorts/{video_id}"
                video_links.append(shorts_url)
        
        return video_links
    else:
        print(f"Error searching YouTube: {response.status_code}, {response.json()}")
        return None

def main():
    # YouTube Data API key (Replace with your API key)
    api_key = "AIzaSyCHUfKUWyvMckHryTVj8lx6xRsoBog0M-Y"
    
    # User input for Zodiac sign
    zodiac_sign = input("Enter your zodiac sign: ").strip().lower()

    # Get today's date in the format YYYY-MM-DD
    today_date = datetime.today().strftime('%Y-%m-%d')

    # Create the search query in Hindi
    query = f"aaj ka rashifal {zodiac_sign} {today_date} in shorts"
    
    # Search YouTube for Shorts based on the query
    print(f"Searching YouTube for: {query}")
    shorts_links = search_youtube_shorts(query, api_key)
    
    if shorts_links:
        print(f"Found {len(shorts_links)} Shorts videos:")
        for link in shorts_links:
            print(link)
    else:
        print("No Shorts videos found.")

if __name__ == "__main__":
    main()
