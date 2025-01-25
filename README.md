# YouTubeBot

A lightweight IRC bot that provides real-time YouTube video information and search capabilities using the YouTube Data API. YouTubeBot is designed to be simple to set up, easy to configure, and free to use as it relies on the free YouTube Data API service (up to a certain quota limit).

![Python](https://img.shields.io/badge/python-3.6%2B-blue)
![YouTube Data API v3](https://img.shields.io/badge/YouTube%20Data%20API-v3-red)

## IRC Server Details

Join us on MansionNET IRC to chat with us, test the bot, and discover new YouTube content!

🌐 **Server:** irc.inthemansion.com
🔒 **Port:** 6697 (SSL)
📝 **Channels:** #opers, #general, #welcome, #music, #heavy_metal, #devs, #test_room, #lobby

## Features

- Automatically detects YouTube video links shared in the chat and responds with:
  - Video title
  - Channel name
  - View count
  - Like count
- Allows users to search for YouTube videos using the `!yt search <query>` command
- Allows users to retrieve information about a YouTube channel using the `!yt channel <name>` command
- Supports multiple IRC channels
- Utilizes YouTube Data API for video and channel information
- SSL/TLS support for secure IRC connections
- Easy to configure and customize

## Requirements

- Python 3.6 or higher
- `irc` library for IRC client functionality
- `google-api-python-client` library for YouTube Data API integration
- YouTube Data API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MansionNET/YouTubeBot.git
   cd YouTubeBot
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Obtain a YouTube Data API key:
   - Go to the [Google Developers Console](https://console.developers.google.com/)
   - Create a new project or select an existing one
   - Enable the YouTube Data API v3
   - Create an API key

5. Create a `config.py` file in the project directory with the following content:
   ```python
   YOUTUBE_API_KEY = 'YOUR_API_KEY'
   ```
   Replace `'YOUR_API_KEY'` with your actual YouTube Data API key.

## Usage

Start the bot:
```bash
python youtubebot.py
```

### Available Commands

In any channel where the bot is present:
- `!yt search <query>` - Search for YouTube videos based on the provided query
  - Example: `!yt search funny cat videos`
- `!yt channel <name>` - Retrieve information about a YouTube channel with the specified name
  - Example: `!yt channel PewDiePie`
- `!yt help` - Display available commands

## API Information

YouTubeBot uses the YouTube Data API v3 for video and channel information. An API key is required, and you must comply with the [YouTube API Services Terms of Service](https://developers.google.com/youtube/terms/api-services-terms-of-service).

Please be aware of the API usage limits and quotas to avoid exceeding them.

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and contribute to the project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- YouTube for providing the YouTube Data API
- The IRC community for continued support of the protocol

## Project Status

This project is actively maintained. If you encounter any issues or have suggestions, please open an issue on GitHub.
