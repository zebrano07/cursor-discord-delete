import discord
from discord.ext import commands
import os
import asyncio
from discord.errors import NotFound

class MessageCleaner(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)
        self.is_deleting = False
        self.current_channel = None
        
    async def delete_messages(self, channel_id: int, limit: int = None):
        channel = self.get_channel(channel_id)
        if not channel:
            raise ValueError("Channel not found")
            
        self.is_deleting = True
        self.current_channel = channel_id
        deleted = 0
        failed = 0
        
        try:
            if limit:
                async for message in channel.history(limit=limit):
                    if not self.is_deleting:
                        return deleted
                    try:
                        await asyncio.sleep(1.5)
                        await message.delete()
                        deleted += 1
                    except NotFound:
                        failed += 1
                        continue
            else:
                async for message in channel.history():
                    if not self.is_deleting:
                        return deleted
                    try:
                        await asyncio.sleep(1.5)
                        await message.delete()
                        deleted += 1
                    except NotFound:
                        failed += 1
                        continue
        finally:
            self.is_deleting = False
            self.current_channel = None
        
        return deleted, failed 

    def stop_deletion(self, channel_id: int) -> bool:
        """Returns True if deletion was stopped, False if no deletion was in progress"""
        if self.is_deleting and self.current_channel == channel_id:
            self.is_deleting = False
            return True
        return False 