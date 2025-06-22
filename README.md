# Telegram Channel Bridge

Automatically forwards messages from a paid/restricted Telegram channel to your own channel.

## What You Need

- Linux server (Ubuntu/Debian)
- Python 3.7+
- Active Telegram account
- Admin access to destination channel

## Setup Guide

### 1. Get Telegram API Keys

1. Go to https://my.telegram.org/auth
2. Login with your phone number
3. Click "API Development Tools" 
4. Fill out the form:
   - App title: `Channel Bridge`
   - Short name: `bridge`
   - Platform: `Desktop`
5. Copy your `API_ID` (8 digits) and `API_HASH` (32 characters)

### 2. Find Channel IDs

**Method 1 - Telegram Web:**
1. Open https://web.telegram.org
2. Go to your source channel (paid channel)
3. Copy the number from URL: `https://web.telegram.org/k/#-1001234567890`
4. The ID is `-1001234567890`
5. Go to your own channel (destination channel)  #Obviously you have to create it, if not already done so
6. Copy the number from URL: `https://web.telegram.org/k/#-1009876543210`
7. The ID is `-1009876543210`

**Method 2 - Bot:**
1. Add @userinfobot to both channels
2. Forward any message to the bot
3. It shows the channel ID

### 3. Install Dependencies

```bash
# Download files from GitHub
git clone https://github.com/KillerScrope/telegram-bridge.git
cd telegram-bridge

# Install dependencies
sudo apt update
sudo apt install -y python3 python3-pip tmux
pip3 install telethon

# Make scripts runnable
chmod +x *.py
4. Configure Settings
Edit the config file:
bashnano config.py
Replace the example values:
pythonAPI_ID = 12345678  # Your API ID from step 1
API_HASH = 'abc123...'  # Your API Hash from step 1
SOURCE_CHAT_ID = -1001234567890  # Source channel ID from step 2
DEST_CHAT_ID = -1009876543210    # Destination channel ID from step 2
5. Get Session String
Run the session generator:
bashpython3 generate_session.py
Follow the prompts:

Enter phone number with country code (+1234567890)
Enter verification code from Telegram
Enter 2FA password if you have one
Copy the long session string that appears

6. Start the Bridge
bash# Create tmux session
tmux new-session -d -s telegram-bridge

# Run the bridge (replace YOUR_SESSION_STRING with your actual string)
tmux send-keys -t telegram-bridge "cd ~/telegram-bridge" Enter
tmux send-keys -t telegram-bridge "export TG_STRING_SESSION='YOUR_SESSION_STRING'" Enter
tmux send-keys -t telegram-bridge "python3 bridge.py" Enter

# View the bridge running
tmux attach -t telegram-bridge
You should see:
✅ Client started successfully
✅ Source channel: [Your Channel Name]
✅ Destination channel: [Your Channel Name]
✅ Test message sent successfully
🚀 Bridge is live and listening for messages...
Press Ctrl+B then D to detach and leave it running.
Daily Usage
Check if running:
bashtmux list-sessions
View logs:
bashtmux attach -t telegram-bridge
Restart bridge:
bashtmux kill-session -t telegram-bridge
# Then repeat step 6
Stop bridge:
bashtmux kill-session -t telegram-bridge
Auto-Start on Reboot
Add to startup:
bashcrontab -e
Add this line:
bash@reboot tmux new-session -d -s telegram-bridge && tmux send-keys -t telegram-bridge "cd ~/telegram-bridge && export TG_STRING_SESSION='YOUR_SESSION_STRING' && python3 bridge.py" Enter
Troubleshooting
"No module named 'telethon'"
bashpip3 install telethon
"No permission to write"

Make sure you're admin of destination channel
Check channel allows posting

Bridge stops working

Check tmux session: tmux attach -t telegram-bridge
Restart if needed: tmux kill-session -t telegram-bridge

Timestamp warnings
These are harmless and don't affect functionality.
Advanced: Systemd Service
For automatic management, copy tg-bridge.service to /etc/systemd/system/, edit the session string, then:
bashsudo systemctl daemon-reload
sudo systemctl enable tg-bridge
sudo systemctl start tg-bridge
Security

Never share your session string
Use a dedicated Telegram account if possible
Keep your API credentials private

Files

bridge.py - Main script
config.py - Your settings
generate_session.py - Creates session string
setup.sh - Auto installer (optional)
tg-bridge.service - Systemd service (optional)
