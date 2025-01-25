import irc.client
import ssl
import re
import time
from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs

class YouTubeBot:
    def __init__(self, server, port, channels, nickname, youtube_api_key):
        self.server = server
        self.port = port
        self.channels = channels
        self.nickname = nickname
        self.youtube = build('youtube', 'v3', developerKey=youtube_api_key)
        
        # Initialize IRC client
        self.reactor = irc.client.Reactor()
        self.connection = self.reactor.server()
        
        # Set up event handlers
        self.connection.add_global_handler("welcome", self.on_connect)
        self.connection.add_global_handler("pubmsg", self.on_pubmsg)
        self.connection.add_global_handler("privmsg", self.on_pubmsg)
        
    def start(self):
        """Start the bot"""
        print(f"Connecting to {self.server}:{self.port}...")
        
        # Enable SSL
        ssl_factory = irc.connection.Factory(wrapper=ssl.wrap_socket)
        
        try:
            self.connection.connect(self.server, self.port, self.nickname, 
                                 connect_factory=ssl_factory)
        except irc.client.ServerConnectionError as e:
            print(f"Error connecting to server: {e}")
            return
            
        self.reactor.process_forever()
        
    def on_connect(self, connection, event):
        print(f"Connected to {self.server}")
        for channel in self.channels:
            connection.join(channel)
            print(f"Joined {channel}")
        
    def on_pubmsg(self, connection, event):
        """Handle public messages"""
        message = event.arguments[0]
        
        # Check for YouTube links
        youtube_urls = self.extract_youtube_urls(message)
        for url in youtube_urls:
            video_info = self.get_video_info(url)
            if video_info:
                self.send_video_info(connection, video_info, event)
        
        # Check for commands
        if message.startswith('!yt'):
            self.handle_youtube_command(connection, event)
            
    def extract_youtube_urls(self, message):
        """Extract YouTube video IDs from message"""
        urls = []
        # Match both youtube.com and youtu.be URLs
        youtube_regex = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]+)'
        matches = re.finditer(youtube_regex, message)
        for match in matches:
            urls.append(match.group(1))
        return urls
    
    def get_video_info(self, video_id):
        """Get information about a YouTube video"""
        try:
            request = self.youtube.videos().list(
                part='snippet,statistics',
                id=video_id
            )
            response = request.execute()
            
            if not response['items']:
                return None
                
            video = response['items'][0]
            return {
                'title': video['snippet']['title'],
                'channel': video['snippet']['channelTitle'],
                'views': video['statistics']['viewCount'],
                'likes': video['statistics'].get('likeCount', 'N/A'),
                'comments': video['statistics'].get('commentCount', 'N/A')
            }
        except Exception as e:
            print(f"Error getting video info: {e}")
            return None
            
    def send_video_info(self, connection, video_info, event):
        """Send video information with colors"""
        message = (
            f"\x0300,04 ► \x0f"  # Red background, white arrow
            f"\x0301,00YouTube\x0f | "  # White background, black text
            f"{video_info['title']} | "
            f"\x0300,04Channel\x0f {video_info['channel']} | "
            f"\x0300,04Views\x0f {video_info['views']} | "
            f"\x0300,04Likes\x0f {video_info['likes']}"
        )
        connection.privmsg(event.target, message)
        
    def handle_youtube_command(self, connection, event):
        """Handle YouTube commands"""
        message = event.arguments[0].split()
        if len(message) < 2:
            return
            
        command = message[1].lower()
        args = ' '.join(message[2:]) if len(message) > 2 else ''
        
        if command == 'help':
            help_msg = (
                f"\x0300,04► \x0f"  # Red background, white arrow
                f"\x0301,00YouTube Bot Commands\x0f | "  # White background, black text
                "!yt search <query> - Search for videos | "
                "!yt channel <name> - Get channel info | "
                "Also detects and shows info for any YouTube links!"
            )
            connection.privmsg(event.target, help_msg)
            
        elif command == 'search':
            if args:
                results = self.search_videos(args)
                if results:
                    for video in results[:3]:
                        connection.privmsg(event.target, 
                            f"\x0300,04► \x0f"  # Red background, white arrow
                            f"\x0301,00YouTube Search\x0f | "  # White background, black text
                            f"\x0300{video['title']}\x0f | "
                            f"\x0312https://youtu.be/{video['id']}\x0f")
                else:
                    connection.privmsg(event.target, 
                        f"\x0300,04► \x0f"  # Red background, white arrow
                        f"\x0301,00YouTube\x0f | No videos found!")
                    
        elif command == 'channel':
            if args:
                channel_info = self.get_channel_info(args)
                if channel_info:
                    connection.privmsg(event.target,
                        f"\x0300,04► \x0f"  # Red background, white arrow
                        f"\x0301,00YouTube Channel\x0f | "  # White background, black text
                        f"{channel_info['title']} | "
                        f"\x0300,04Subscribers\x0f {channel_info['subscribers']} | "
                        f"\x0300,04Videos\x0f {channel_info['videos']} | "
                        f"\x0300,04Total Views\x0f {channel_info['views']}")
                else:
                    connection.privmsg(event.target, 
                        f"\x0300,04► \x0f"  # Red background, white arrow
                        f"\x0301,00YouTube\x0f | Channel not found!")
                    
    def search_videos(self, query):
        """Search for YouTube videos"""
        try:
            request = self.youtube.search().list(
                part='snippet',
                q=query,
                type='video',
                maxResults=3
            )
            response = request.execute()
            
            results = []
            for item in response['items']:
                results.append({
                    'id': item['id']['videoId'],
                    'title': item['snippet']['title']
                })
            return results
        except Exception as e:
            print(f"Error searching videos: {e}")
            return None
            
    def get_channel_info(self, channel_name):
        """Get information about a YouTube channel"""
        try:
            # First search for the channel
            request = self.youtube.search().list(
                part='snippet',
                q=channel_name,
                type='channel',
                maxResults=1
            )
            response = request.execute()
            
            if not response['items']:
                return None
                
            channel_id = response['items'][0]['id']['channelId']
            
            # Then get detailed channel information
            request = self.youtube.channels().list(
                part='snippet,statistics',
                id=channel_id
            )
            response = request.execute()
            
            if not response['items']:
                return None
                
            channel = response['items'][0]
            return {
                'title': channel['snippet']['title'],
                'subscribers': channel['statistics'].get('subscriberCount', 'N/A'),
                'videos': channel['statistics']['videoCount'],
                'views': channel['statistics']['viewCount']
            }
        except Exception as e:
            print(f"Error getting channel info: {e}")
            return None

if __name__ == "__main__":
    # Configuration
    SERVER = "irc.inthemansion.com"
    PORT = 6697
    CHANNELS = ["#opers", "#general", "#welcom", "#music", "#heavy_metal", "#devs", "#test_room", "#lobby"]
    NICKNAME = "YouTubeBot"
    
    try:
        from config import YOUTUBE_API_KEY
    except ImportError:
        print("Please create config.py with your YOUTUBE_API_KEY")
        exit(1)
    
    bot = YouTubeBot(SERVER, PORT, CHANNELS, NICKNAME, YOUTUBE_API_KEY)
    try:
        bot.start()
    except KeyboardInterrupt:
        print("\nBot shutting down...")
        exit(0)
