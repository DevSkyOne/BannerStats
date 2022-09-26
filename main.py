import json
from discord.ext import commands
from datetime import datetime
from PIL import Image, ImageFont, ImageDraw
import discord, asyncio

client = discord.Client(intents=discord.Intents.default())

with open('config.json', 'r') as f:
    config = json.load(f)


@client.event
async def on_ready():
    await banner_loop()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)



async def banner_loop():
    while True:
        invite = await client.fetch_invite(config.get('invite'))

        banner_stock = Image.open("Banner.png")

        font = ImageFont.truetype('OpenSans-ExtraBold.ttf', 50)

        draw = ImageDraw.Draw(banner_stock)

        members = invite.approximate_member_count
        online = invite.approximate_presence_count

        # Members
        draw.text((140, 410), str(members), font=font, color="white")

        # Online
        if online >= 1000:
            draw.text((708, 410), str(online), font=font, color="white")
        else:
            draw.text((740, 410), str(online), font=font, color="white")

        banner_stock.save('Banner_New.png')

        print(f"Created Image - {members}(Total) - {online}(Online)")

        with open('Banner_New.png', 'rb') as f:
            banner = f.read()
        guild = client.get_guild(config.get('guildId'))
        await guild.edit(banner=banner)
        await asyncio.sleep(300)


client.run(config.get('token'))
