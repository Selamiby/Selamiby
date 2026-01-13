import os
import json
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build

class VideoMetadataOptimizer:
    def __init__(self, api_key, youtube_channel_id):
        self.api_key = api_key
        self.youtube_channel_id = youtube_channel_id
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def get_video_ids(self):
        request = self.youtube.search().list(
            part="id,snippet",
            channelId=self.youtube_channel_id,
            maxResults=50
        )
        response = request.execute()
        video_ids = [item['id']['videoId'] for item in response['items']]
        return video_ids

    def get_video_metadata(self, video_id):
        request = self.youtube.videos().list(
            part="id,snippet,contentDetails",
            id=video_id
        )
        response = request.execute()
        metadata = response['items'][0]
        return metadata

    def optimize_video_metadata(self, video_id, metadata):
        title = metadata['snippet']['title']
        description = metadata['snippet']['description']
        tags = metadata['snippet'].get('tags', [])
        keywords = [word.strip() for word in title.split()]
        keywords.extend([word.strip() for word in description.split()])
        keywords.extend(tags)
        keywords = list(set(keywords))
        metadata['snippet']['tags'] = keywords
        request = self.youtube.videos().update(
            part="snippet",
            body=metadata
        )
        response = request.execute()
        return response

    def scrape_video_transcript(self, video_id):
        url = f"https://www.youtube.com/watch?v={video_id}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        transcript = soup.find('div', {'id': 'transcript'})
        if transcript:
            return transcript.text.strip()
        else:
            return None

    def optimize_video_transcript(self, video_id, transcript):
        if transcript:
            keywords = [word.strip() for word in transcript.split()]
            keywords = list(set(keywords))
            return keywords
        else:
            return None

def main():
    api_key = "YOUR_API_KEY"
    youtube_channel_id = "YOUR_CHANNEL_ID"
    optimizer = VideoMetadataOptimizer(api_key, youtube_channel_id)
    video_ids = optimizer.get_video_ids()
    for video_id in video_ids:
        metadata = optimizer.get_video_metadata(video_id)
        optimized_metadata = optimizer.optimize_video_metadata(video_id, metadata)
        transcript = optimizer.scrape_video_transcript(video_id)
        optimized_transcript = optimizer.optimize_video_transcript(video_id, transcript)
        print(f"Optimized video {video_id} metadata and transcript")

if __name__ == "__main__":
    main()
# NEXUS-ONE CORE MODULE - PRODUCTION READY