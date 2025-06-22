# Telegram Channel Bridge

A reliable Python script that automatically forwards messages from a paid/restricted Telegram channel to your own channel using the Telegram API.

## 🚀 Features

- **No Bot Required**: Uses your user account via MTProto API
- **Handles Restricted Channels**: Works with channels where bots can't be added
- **Reliable Forwarding**: Forwards text, media, and all message types with original formatting
- **Tmux Session**: Persistent background execution with easy monitoring
- **Error Handling**: Robust handling of Telegram API errors and rate limits
- **Logging**: Comprehensive logging with timestamp filtering

## 📋 Prerequisites

- Linux server Ubuntu/Debian recommended (I ran it using Ubuntu 22.04)
- Python 3.7+
- tmux
- Active Telegram account

## 🔧 Step-by-Step Setup

### Step 1: Get Telegram API Credentials

1. **Visit**: https://my.telegram.org/auth
2. **Login** with your phone number
3. **Go to API Development Tools**: https://my.telegram.org/apps
4. **Create a new application**:
   - App title: `Channel Bridge`
   - Short name: `bridge`
   - Platform: `Desktop`
5. **Save your credentials**:
   - `API_ID`: 8-digit number
   - `API_HASH`: 32-character string

### Step 2: Get Channel IDs

#### Method 1: Using Telegram Web
1. **Open**: https://web.telegram.org
2. **Navigate to your channels**
3. **Look at URL**: `https://web.telegram.org/k/#-1001234567890`
4. **The ID is the number after `#`**: `-1001234567890`

#### Method 2: Using Bot
1. **Add @userinfobot to channels** (if possible, if not then use the method above)
2. **Forward any message to @userinfobot**
3. **It will show the channel ID**

### Step 3: Install Dependencies

```bash
# Update system
sudo apt update

# Install requirements
sudo apt install -y python3 python3-pip tmux

# Install Telethon
pip3 install telethon
```

### Step 4: Setup Project

```bash
# Create project directory
mkdir -p ~/tg-bridge
cd ~/tg-bridge

# Download/create files (copy from GitHub artifacts)
# - bridge.py
# - generate_session.py  
# - config.py

# Make scripts executable
chmod +x *.py
```

### Step 5: Configure

```bash
# Edit configuration
nano config.py
```

**Update values:**
```python
API_ID = 12345678  # Your API ID
API_HASH = 'your_api_hash_here'  # Your API Hash
SOURCE_CHAT_ID = -1001234567890  # Source channel ID
DEST_CHAT_ID = -1001234567891    # Destination channel ID
```

### Step 6: Generate Session String

```bash
cd ~/tg-bridge
python3 generate_session.py
```

**Follow prompts:**
1. Enter phone number (with country code)
2. If 2FA enabled enter verification code
3. Enter password
4. **Copy the session string**

### Step 7: Start Bridge in Tmux

```bash
# Start tmux session
tmux new-session -d -s telegram-bridge

# Set session string and run bridge
tmux send-keys -t telegram-bridge "cd ~/tg-bridge" Enter
tmux send-keys -t telegram-bridge "export TG_STRING_SESSION='YOUR_SESSION_STRING_HERE'" Enter
tmux send-keys -t telegram-bridge "python3 bridge.py" Enter

# Attach to view logs
tmux attach -t telegram-bridge
```

**Expected output:**
```
✅ Client started successfully
✅ Source channel: [Channel Name]
✅ Destination channel: [Channel Name]
✅ Test message sent successfully
🚀 Bridge is live and listening for messages...
```

**To detach**: Press `Ctrl+B`, then `D`

### Step 8: Verify Operation

Check your destination channel for the test message: "🤖 Bridge started at [timestamp]"

## 🔧 Management Commands

### View Bridge Status
```bash
# Attach to tmux session
tmux attach -t telegram-bridge

# List tmux sessions
tmux list-sessions
```

### Restart Bridge
```bash
# Kill session
tmux kill-session -t telegram-bridge

# Start new session
tmux new-session -d -s telegram-bridge
tmux send-keys -t telegram-bridge "cd ~/tg-bridge" Enter
tmux send-keys -t telegram-bridge "export TG_STRING_SESSION='YOUR_SESSION_STRING_HERE'" Enter
tmux send-keys -t telegram-bridge "python3 bridge.py" Enter
```

### Stop Bridge
```bash
tmux kill-session -t telegram-bridge
```

### Auto-start on Boot (Optional)

Add to crontab:
```bash
crontab -e
```

Add line:
```bash
@reboot tmux new-session -d -s telegram-bridge && tmux send-keys -t telegram-bridge "cd ~/tg-bridge && export TG_STRING_SESSION='YOUR_SESSION_STRING_HERE' && python3 bridge.py" Enter
```

## 🔧 Alternative: Systemd Service (Advanced Users)

If you prefer systemd over tmux:

```bash
# Copy service file to systemd
sudo cp tg-bridge.service /etc/systemd/system/
sudo nano /etc/systemd/system/tg-bridge.service

# Update session string in service file
# Then start service
sudo systemctl daemon-reload
sudo systemctl enable tg-bridge
sudo systemctl start tg-bridge

# Monitor
sudo journalctl -u tg-bridge -f
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. "ModuleNotFoundError: No module named 'telethon'"
```bash
pip3 install telethon
```

#### 2. Tmux session not found
```bash
# Check existing sessions
tmux list-sessions

# Create new session if needed
tmux new-session -d -s telegram-bridge
```

#### 3. "PersistentTimestampOutdatedError"
This is a harmless Telegram API warning. The bridge continues working normally.

#### 4. "No permission to write to destination channel"
- Ensure you're an admin of the destination channel
- Verify correct channel ID
- Check channel allows posting

#### 5. Bridge stops unexpectedly
```bash
# Check tmux session
tmux attach -t telegram-bridge

# Test manually
export TG_STRING_SESSION='your_session_string'
python3 bridge.py
```

#### 6. Messages not preserving formatting
The bridge uses direct forwarding to preserve original formatting and embeds.

### Clear Old Logs
```bash
# Restart tmux session to clear logs
tmux kill-session -t telegram-bridge
# Then start new session
```

### Regenerate Session String
```bash
cd ~/tg-bridge
python3 generate_session.py
# Update session string in your tmux commands
```

## 📁 File Structure

```
tg-bridge/
├── README.md              # This guide
├── bridge.py             # Main bridge script
├── generate_session.py   # Session string generator
├── config.py             # Configuration file
└── tg-bridge.service     # Systemd service (optional)
```

## 🔒 Security Notes

- **Keep session string secure** - provides full Telegram account access
- **Don't share session string**
- **Use dedicated Telegram account** if possible
- **Monitor logs regularly**

## 📄 License

Provided as-is for educational purposes. Use responsibly and comply with Telegram's Terms of Service.

## ⚠️ Disclaimer

For personal use only. Ensure compliance with Telegram's Terms of Service and applicable laws.
