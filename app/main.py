import os
from dotenv import load_dotenv
from app.discord_client import MessageCleaner
from app.database import init_db, SessionLocal, ServerConfig
import asyncio

load_dotenv()

bot = MessageCleaner()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='clear')
async def clear_messages(ctx, limit: int = None):
    try:
        if bot.is_deleting and bot.current_channel == ctx.channel.id:
            await ctx.send("A deletion process is already running in this channel. Use !stop to cancel it.", delete_after=5)
            return
        status_msg = await ctx.send("Starting message deletion... This may take a while.")
        deleted, failed = await bot.delete_messages(ctx.channel.id, limit)
        if failed > 0:
            response = f"Deleted {deleted} messages. {failed} messages were already deleted or not found."
        else:
            response = f"Successfully deleted {deleted} messages." if bot.is_deleting else f"Deletion stopped after removing {deleted} messages."
        await status_msg.edit(content=response)
        await asyncio.sleep(5)
        await status_msg.delete()
    except Exception as e:
        await ctx.send(f"Error: {str(e)}", delete_after=5)

@bot.command(name='setup')
async def setup_channel(ctx):
    db = SessionLocal()
    try:
        config = ServerConfig(
            server_id=str(ctx.guild.id),
            channel_id=str(ctx.channel.id)
        )
        db.add(config)
        db.commit()
        await ctx.send("Channel configured successfully!", delete_after=5)
    except Exception as e:
        await ctx.send(f"Error: {str(e)}", delete_after=5)
    finally:
        db.close()

@bot.command(name='stop')
async def stop_deletion(ctx):
    """Stops the current message deletion process"""
    if bot.stop_deletion(ctx.channel.id):
        await ctx.send("Stopping message deletion...", delete_after=5)
    else:
        await ctx.send("No deletion process is currently running in this channel.", delete_after=5)

def main():
    init_db()
    bot.run(os.getenv('DISCORD_BOT_TOKEN'))

if __name__ == "__main__":
    main() 