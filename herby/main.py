import asyncio
import discord
from discord.ext import commands, tasks
from aiohttp import web

# Initialize bot
bot = commands.Bot(command_prefix="!", self_bot=True)

CHANNEL_ID = 1323861435654213643  
SPAM_MESSAGE = "asdasdasdasdadasdasdasdasdasdadasdadads" 
WAIT_TIME = 2.5                     

# --- Web Server Configuration for Render ---
async def handle(request):
    return web.Response(text="Bot is alive!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render automatically passes an internal port via environment variables
    import os
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Web server started on port {port}")

@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name}")
    # Start the web server concurrently so Render stays connected
    bot.loop.create_task(start_web_server())
    if not spam_loop.is_running():
        spam_loop.start()

@tasks.loop(seconds=1)
async def spam_loop():
    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        try:
            channel = await bot.fetch_channel(CHANNEL_ID)
        except Exception as e:
            print(f"Could not find or access channel: {e}")
            return

    print(f"\n--- Starting a new round ---")
    try:
        await channel.send(SPAM_MESSAGE)
        print("Message sent smoothly.")
    except discord.Forbidden:
        print("Error: No permission to send messages here.")
        return
    except Exception as e:
        print(f"Failed to send message: {e}")

    await asyncio.sleep(WAIT_TIME)

# DO NOT hardcode your token here when uploading to GitHub! 
import os
ACCOUNT_TOKEN = os.environ.get("DISCORD_TOKEN")
bot.run(ACCOUNT_TOKEN)
