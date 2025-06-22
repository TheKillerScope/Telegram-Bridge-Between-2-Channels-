#!/usr/bin/env python3
"""
Telegram Channel Bridge - Forwards messages from source to destination channel
"""

import asyncio
import logging
import os
import sys
from datetime import datetime
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.errors import (
    PersistentTimestampOutdatedError,
    FloodWaitError,
    ChannelPrivateError,
    ChatWriteForbiddenError
)

# Import configuration
try:
    from config import API_ID, API_HASH, SOURCE_CHAT_ID, DEST_CHAT_ID
except ImportError:
    # Fallback to direct configuration if config.py doesn't exist
    API_ID = 12345678
    API_HASH = '1a2c3bdcf44444aa6f7e8bb99999c000'
    SOURCE_CHAT_ID = -1001234567890
    DEST_CHAT_ID = -1009876543210

# Get session string from environment variable
SESSION_STRING = os.getenv('TG_STRING_SESSION', '')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/var/log/tg-bridge.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)

class TelegramBridge:
    def __init__(self):
        if not SESSION_STRING:
            raise ValueError("TG_STRING_SESSION environment variable is required")
        
        self.client = TelegramClient(
            StringSession(SESSION_STRING),
            API_ID,
            API_HASH,
            device_model="Bridge Bot",
            system_version="1.0",
            app_version="1.0"
        )
        
        self.source_entity = None
        self.dest_entity = None
        self.is_running = False

    async def start(self):
        """Initialize the client and entities"""
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                await self.client.start()
                logger.info("✅ Client started successfully")
                break
            except PersistentTimestampOutdatedError as e:
                logger.warning(f"⚠️ Timestamp outdated during start (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(5 * (attempt + 1))  # Progressive delay
                    continue
                else:
                    logger.warning("⚠️ Proceeding despite timestamp error")
            except Exception as e:
                logger.error(f"❌ Failed to start client (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(5 * (attempt + 1))
                    continue
                else:
                    return False
        
        # Get and cache entities with retry logic
        for entity_name, entity_id, attr_name in [
            ("source", SOURCE_CHAT_ID, "source_entity"),
            ("destination", DEST_CHAT_ID, "dest_entity")
        ]:
            for attempt in range(max_retries):
                try:
                    entity = await self.client.get_entity(entity_id)
                    setattr(self, attr_name, entity)
                    logger.info(f"✅ {entity_name.capitalize()} channel: {getattr(entity, 'title', 'Unknown')}")
                    break
                except PersistentTimestampOutdatedError as e:
                    logger.warning(f"⚠️ Timestamp error getting {entity_name} entity (attempt {attempt + 1}): {e}")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(3 * (attempt + 1))
                        continue
                    else:
                        logger.warning(f"⚠️ Proceeding with {entity_name} entity despite timestamp error")
                        try:
                            entity = await self.client.get_entity(entity_id)
                            setattr(self, attr_name, entity)
                            break
                        except:
                            logger.error(f"❌ Could not get {entity_name} entity after all retries")
                            return False
                except Exception as e:
                    logger.error(f"❌ Failed to get {entity_name} entity (attempt {attempt + 1}): {e}")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(3 * (attempt + 1))
                        continue
                    else:
                        return False
        
        # Test message sending capability
        try:
            test_msg = f"🤖 Bridge started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            await self.client.send_message(self.dest_entity, test_msg)
            logger.info("✅ Test message sent successfully")
        except ChatWriteForbiddenError:
            logger.error("❌ No permission to write to destination channel")
            return False
        except Exception as e:
            logger.warning(f"⚠️ Test message failed: {e}")
        
        return True

    async def forward_message(self, event):
        """Forward a message from source to destination"""
        try:
            message = event.message
            
            # Skip if message is empty or from wrong source
            if not message or message.chat_id != SOURCE_CHAT_ID:
                return
            
            # Log the incoming message
            content_preview = (message.text or "Media content")[:50] + "..." if len(message.text or "") > 50 else (message.text or "Media content")
            logger.info(f"📨 Received: {content_preview}")
            
            # Forward the message
            if message.text:
                # Text message
                await self.client.send_message(
                    self.dest_entity, 
                    message.text,
                    parse_mode='html'
                )
            elif message.media:
                # Media message
                await self.client.send_message(
                    self.dest_entity,
                    message,
                    caption=message.text or ""
                )
            else:
                # Other message types
                await self.client.forward_messages(
                    self.dest_entity,
                    message,
                    self.source_entity
                )
            
            logger.info("✅ Message forwarded successfully")
            
        except FloodWaitError as e:
            logger.warning(f"⏳ Rate limited, waiting {e.seconds} seconds")
            await asyncio.sleep(e.seconds)
        except ChatWriteForbiddenError:
            logger.error("❌ No permission to write to destination channel")
        except Exception as e:
            logger.error(f"❌ Failed to forward message: {e}")

    async def run(self):
        """Main run loop"""
        if not await self.start():
            logger.error("❌ Failed to initialize bridge")
            return
        
        # Register event handler
        @self.client.on(events.NewMessage(chats=SOURCE_CHAT_ID))
        async def handle_new_message(event):
            await self.forward_message(event)
        
        self.is_running = True
        logger.info("🚀 Bridge is live and listening for messages...")
        
        try:
            # Keep the client running
            await self.client.run_until_disconnected()
        except KeyboardInterrupt:
            logger.info("👋 Bridge stopped by user")
        except Exception as e:
            logger.error(f"❌ Bridge crashed: {e}")
        finally:
            self.is_running = False
            await self.cleanup()

    async def cleanup(self):
        """Clean up resources"""
        try:
            if self.client.is_connected():
                await self.client.disconnect()
                logger.info("✅ Client disconnected")
        except Exception as e:
            logger.error(f"❌ Error during cleanup: {e}")

async def main():
    """Main entry point with retry logic"""
    max_retries = 3
    retry_delay = 10
    
    for attempt in range(max_retries):
        try:
            logger.info(f"🔄 Starting bridge (attempt {attempt + 1}/{max_retries})")
            bridge = TelegramBridge()
            await bridge.run()
            break  # If we get here, the bridge ran successfully
            
        except ValueError as e:
            logger.error(f"❌ Configuration error: {e}")
            sys.exit(1)
            
        except PersistentTimestampOutdatedError as e:
            logger.warning(f"⚠️ Timestamp outdated error (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                logger.info(f"🔄 Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                logger.error("❌ Max retries reached for timestamp error")
                sys.exit(1)
                
        except Exception as e:
            logger.error(f"❌ Unexpected error (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                logger.info(f"🔄 Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
                retry_delay *= 2
            else:
                logger.error("❌ Max retries reached")
                sys.exit(1)

if __name__ == "__main__":
    # Ignore timestamp errors that don't affect functionality
    logging.getLogger('telethon').setLevel(logging.WARNING)
    
    # Run the bridge
    asyncio.run(main())
