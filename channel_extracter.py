from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set up your API key
api_key = 'YOUR_API_KEY'  # Replace with your actual API key

# Create a YouTube service object
youtube = build('youtube', 'v3', developerKey=api_key)

# Function to retrieve the YouTube account link from a video link
def get_account_link(video_url):
    try: 
        if '?v=' in video_url:
            # Extract the video ID from the URL
            video_id = video_url.split('?v=')[1]

            # Call the API to get video details
            video_response = youtube.videos().list(
                part='snippet',
                id=video_id
            ).execute()

            # Extract the channel ID from the video details
            channel_id = video_response['items'][0]['snippet']['channelId']

            # Construct the YouTube account link
            account_link = f'https://www.youtube.com/channel/{channel_id}'

            return account_link
        elif "youtube.com/user/" in video_url or "youtube.com/channel/" in video_url or "youtube.com/c/" in video_url:
            return video_url
        else:
            return None

    except HttpError as e:
        print('An HTTP error occurred:')
        print(e)
        return None
    except KeyError:
        print('Invalid video URL. Please provide a valid YouTube video link.')
        return None