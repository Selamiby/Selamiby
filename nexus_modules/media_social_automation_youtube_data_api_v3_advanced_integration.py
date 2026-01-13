import os
import json
from googleapiclient.discovery import build

class YouTubeDataAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def get_channel_info(self, channel_id):
        request = self.youtube.channels().list(
            part="snippet,contentDetails,statistics",
            id=channel_id
        )
        response = request.execute()
        return response['items'][0]

    def get_video_info(self, video_id):
        request = self.youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )
        response = request.execute()
        return response['items'][0]

    def get_playlist_info(self, playlist_id):
        request = self.youtube.playlists().list(
            part="snippet,contentDetails",
            id=playlist_id
        )
        response = request.execute()
        return response['items'][0]

    def get_playlist_items(self, playlist_id):
        request = self.youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id
        )
        response = request.execute()
        return response['items']

def main():
    api_key = "YOUR_API_KEY"
    youtube = YouTubeDataAPI(api_key)
    channel_id = "UC_x5XG1OV2P6uZZ5FSM9Ttw"
    video_id = "dQw4w9WgXcQ"
    playlist_id = "PLBwF4879UK"

    channel_info = youtube.get_channel_info(channel_id)
    video_info = youtube.get_video_info(video_id)
    playlist_info = youtube.get_playlist_info(playlist_id)
    playlist_items = youtube.get_playlist_items(playlist_id)

    print(json.dumps(channel_info, indent=4))
    print(json.dumps(video_info, indent=4))
    print(json.dumps(playlist_info, indent=4))
    print(json.dumps(playlist_items, indent=4))

if __name__ == "__main__":
    main()

# NEXUS-ONE CORE MODULE - PRODUCTION READY