# Telegram Bridge Configuration
# Fill in your details below

# Telegram API Credentials (get from https://my.telegram.org/apps)
API_ID = 12345678  # Replace with your API ID (8-digit number)
API_HASH = 'your_api_hash_here'  # Replace with your API Hash (32-character string)

# Channel IDs (get from Telegram Web URL or @userinfobot)
SOURCE_CHAT_ID = -1001234567890  # Replace with your source channel ID (the paid channel)
DEST_CHAT_ID = -1009876543210    # Replace with your destination channel ID (your channel)

# Session string will be set in the systemd service file
# Generate it using: python3 generate_session.py
