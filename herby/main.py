import asyncio
import discord
from discord.ext import commands, tasks
from aiohttp import web

intents = discord.Intents.default()
# Add your proxy URL here (Format: http://username:password@proxy_address:port)
PROXY_URL = "http://your_proxy_here:port" 

bot = commands.Bot(command_prefix="!", self_bot=True, intents=intents, proxy=PROXY_URL)

CHANNEL_ID = 1323861435654213643  
SPAM_MESSAGE = "asdasdasdasdadasdasdasdasdasdadasdadads" 
WAIT_TIME = 2.5                     

async def handle(request):
    return web.Response(text="Bot is alive!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    import os
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name}")
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
            return

    try:
        await channel.send(SPAM_MESSAGE)
    except Exception as e:
        print(f"Error: {e}")

    await asyncio.sleep(WAIT_TIME)

import os
ACCOUNT_TOKEN = os.environ.get("DISCORD_TOKEN")
bot.run(ACCOUNT_TOKEN)
