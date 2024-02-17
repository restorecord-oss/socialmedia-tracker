# Youtube Video/Shorts

from googleapiclient.discovery import build
import requests


def youtube(video_id):
    api_key = 'AIzaSyBLthhMnTm_B481Hh4HQc443cSlYBDtCwE'
    # Build the YouTube client
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    # Retrieve the video details
    request = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    )
    response = request.execute()
    
    # Parse the response to extract details
    if response.get('items', []):
        video_data = response['items'][0]
        title = video_data['snippet']['title']
        views = video_data['statistics']['viewCount']
        likes = video_data['statistics'].get('likeCount', 'Likes not available')
        comments = video_data['statistics'].get('commentCount', 'Comments not available')
        
        return { 'success': True, 'data': {'video_id': video_id, 'title': title, 'views': views, 'likes': likes, 'comments': comments}}
    else:
        print("[get_data] Video not found or access not granted")
        return { 'success': False, 'error': 'Video not found or access not granted'}



# Tiktok

def tiktok(video_id):
    access_token = 'ACCESS'

    # Hypothetical URL for TikTok's API endpoint to get video details
    url = f"https://api.tiktok.com/v1/videos/details?video_id={video_id}&access_token={access_token}"
    
    # Make the API request
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Assuming the API response structure contains these fields
        title = data['data']['title']
        views = data['data']['statistics']['viewCount']
        likes = data['data']['statistics']['likeCount']
        comments = data['data']['statistics']['commentCount']
        
        return { 'video_id': video_id, 'title': title, 'views': views, 'likes': likes, 'comments': comments}
    
    else:
        print("[get_data TikTok] Failed to fetch video details or access not granted")
        return "Failed to fetch video details or access not granted"



# INstagram Reels

def instagram(video_id):
    """
    Fetch views, likes, and comments for an Instagram Reels video using a hypothetical API endpoint.
    
    Parameters:
    - video_id: The unique identifier for the Instagram Reels video.
    
    Returns:
    A dictionary with video details or a message indicating failure.
    """
    
    # Hypothetical URL for Instagram's API endpoint to get video details
    url = f"https://api.instagram.com/v1/reels/{video_id}?fields=title,views,likes,comments&access_token=ACCESS_TOKEN"
    
    # Make the API request
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Assuming the API response structure contains these fields
        title = data['title']
        views = data['views']
        likes = data['likes']
        comments = data['comments']
        
        return {
            'title': title,
            'views': views,
            'likes': likes,
            'comments': comments
        }
    else:
        print("[get_data Instagram] Failed to fetch video details or access not granted")
        return "Failed to fetch video details or access not granted"