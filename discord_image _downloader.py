import discord
from discord.ext import commands
import os
import aiohttp
import re

BOT_TOKEN = 'token here'
CHANNEL_IDS = [id here]  # Add your channel IDs here to add more just put a , then a space then the next one

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}#{bot.user.discriminator}')
    print(f'Bot ID: {bot.user.id}')
    
    for channel_id in CHANNEL_IDS:
        channel = bot.get_channel(channel_id)
        if channel:
            print(f'Found channel: {channel.name} (ID: {channel.id})')
            await download_images(channel)
        else:
            print(f'Could not find channel with ID: {channel_id}')
    
    await bot.close()

async def download_images(channel):
    if not os.path.exists('images'):
        os.makedirs('images')

    async for message in channel.history(limit=None):
        print(f'Processing message ID: {message.id} in channel {channel.name}')
        for attachment in message.attachments:
            print(f'Found attachment: {attachment.filename}')
            if attachment.filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp')):
                await save_image(attachment.url, attachment.filename, channel.name)
        
        urls = re.findall(r'(https?://\S+)', message.content)
        for url in urls:
            if url.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp')):
                filename = url.split("/")[-1]
                await save_image(url, filename, channel.name)

async def save_image(url, filename, channel_name):
    channel_path = os.path.join('images', channel_name)
    if not os.path.exists(channel_path):
        os.makedirs(channel_path)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(os.path.join(channel_path, filename), 'wb') as f:
                    f.write(await response.read())
                print(f'Downloaded {filename} from {channel_name}')
            else:
                print(f'Failed to download {filename} from {url} with status {response.status}')

bot.run(BOT_TOKEN)
