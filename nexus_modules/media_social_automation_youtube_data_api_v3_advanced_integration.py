import os
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

class YouTubeDataAPI:
    def __init__(self, API_KEY, API_SECRET):
        self.API_KEY = API_KEY
        self.API_SECRET = API_SECRET
        self.youtube = self.__build_youtube_api()

    def __build_youtube_api(self):
        creds = service_account.Credentials.from_service_account_file(
            'path/to/service_account_key.json',
            scopes=['https://www.googleapis.com/auth/youtube.force-ssl']
        )
        return build('youtube', 'v3', credentials=creds)

    def search_videos(self, query, max_results=10):
        request = self.youtube.search().list(
            part='id,snippet',
            q=query,
            maxResults=max_results
        )
        response = request.execute()
        return response['items']

    def get_video_details(self, video_id):
        request = self.youtube.videos().list(
            part='id,snippet,contentDetails,statistics',
            id=video_id
        )
        response = request.execute()
        return response['items'][0]

    def get_channel_videos(self, channel_id, max_results=10):
        request = self.youtube.search().list(
            part='id,snippet',
            channelId=channel_id,
            maxResults=max_results,
            order='date'
        )
        response = request.execute()
        return response['items']

def main():
    api_key = 'YOUR_API_KEY'
    api_secret = 'YOUR_API_SECRET'
    youtube_api = YouTubeDataAPI(api_key, api_secret)

    query = 'Python Programming'
    videos = youtube_api.search_videos(query)
    for video in videos:
        print(video['id']['videoId'], video['snippet']['title'])

    video_id = 'VIDEO_ID'
    video_details = youtube_api.get_video_details(video_id)
    print(video_details['id'], video_details['snippet']['title'])

    channel_id = 'CHANNEL_ID'
    channel_videos = youtube_api.get_channel_videos(channel_id)
    for video in channel_videos:
        print(video['id']['videoId'], video['snippet']['title'])

# NEXUS-ONE CORE MODULE