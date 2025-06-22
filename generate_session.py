#!/usr/bin/env python3
"""
Telegram Session String Generator
Run this script to generate a session string for the bridge
"""

import asyncio
import sys
from telethon import TelegramClient
from telethon.sessions import StringSession

# Try to import from config, fallback to manual input
try:
    from config import API_ID, API_HASH
    print(f"📱 Using API credentials from config.py")
    print(f"   API_ID: {API_ID}")
    print(f"   API_HASH: {API_HASH[:8]}...")
except ImportError:
    print("⚠️ config.py not found. Please enter your API credentials manually.")
    print("Get them from: https://my.telegram.org/apps")
    try:
        API_ID = int(input("Enter your API_ID: "))
        API_HASH = input("Enter your API_HASH: ")
    except (ValueError, KeyboardInterrupt):
        print("\n❌ Invalid input or cancelled by user")
        sys.exit(1)

async def generate_session():
    """Generate a session string"""
    print("\n🔐 Generating Telegram session string...")
    print("=" * 50)
    print("You'll need to provide:")
    print("• Your phone number (with country code)")
    print("• Verification code sent to your Telegram")
    print("• Your 2FA password (if enabled)")
    print("=" * 50)
    print()
    
    # Create client with empty string session
    client = TelegramClient(StringSession(), API_ID, API_HASH)
    
    try:
        print("🔄 Connecting to Telegram...")
        
        # Start the client and authenticate
        await client.start()
        
        print("✅ Authentication successful!")
        
        # Get the session string
        session_string = client.session.save()
        
        print("\n" + "=" * 80)
        print("🎉 SESSION STRING GENERATED SUCCESSFULLY!")
        print("=" * 80)
        print()
        print("🔑 Your session string:")
        print("-" * 80)
        print(session_string)
        print("-" * 80)
        print()
        print("📋 IMPORTANT INSTRUCTIONS:")
        print("1. COPY the session string above")
        print("2. Edit the systemd service file:")
        print("   nano /etc/systemd/system/tg-bridge.service")
        print("3. Replace 'YOUR_SESSION_STRING_HERE' with your session string")
        print("4. Save and reload the service:")
        print("   systemctl daemon-reload")
        print("   systemctl restart tg-bridge")
        print()
        print("⚠️  SECURITY WARNING:")
        print("• Never share this session string with anyone!")
        print("• It provides full access to your Telegram account")
        print("• Store it securely")
        print()
        
        # Test the session and show user info
        me = await client.get_me()
        print(f"📱 Authenticated as:")
        print(f"   Name: {me.first_name} {me.last_name or ''}")
        print(f"   Username: @{me.username or 'No username'}")
        print(f"   Phone: {me.phone or 'Hidden'}")
        print(f"   User ID: {me.id}")
        print()
        
    except KeyboardInterrupt:
        print("\n👋 Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("• Check your internet connection")
        print("• Verify your API_ID and API_HASH are correct")
        print("• Make sure you entered the correct phone number")
        print("• Check if you received the verification code")
    finally:
        await client.disconnect()
        print("\n🔌 Disconnected from Telegram")

if __name__ == "__main__":
    try:
        asyncio.run(generate_session())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)
