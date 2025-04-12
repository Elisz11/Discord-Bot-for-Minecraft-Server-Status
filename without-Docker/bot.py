from datetime import datetime, timezone
import discord
import asyncio
import pytz
import os
from mcstatus import JavaServer

TOKEN = ""  # Insert your Discord bot token here
CHANNEL_ID =  # Insert the channel ID here (without quotes)
server_ip = ""  # Insert the server IP here

server = JavaServer.lookup(server_ip)

intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Function to fetch server status
async def fetch_status():
    try:
        status = await server.async_status()
        players = status.players.online
        
        if status.players.sample:
            players_list = "\n".join([f"  - `{player.name}`" for player in status.players.sample])
        else:
            players_list = "  - `No players online`"  

        print(f"Players: {players}, Names: \n{players_list}")

    except Exception as e:
        print(f"Error retrieving status: {e}")
        players = "Offline"
        players_list = "`Offline`"

    return players, players_list

# Function to get current time
timezone = pytz.timezone("Europe/Rome")
def get_time():
    return datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S")

# Function to update the message
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

    channel = client.get_channel(CHANNEL_ID)
    if not channel:
        print("Error: channel does not exist!")
        return

    async for message in channel.history(limit=10):
        if message.author == client.user:
            break
    else:
        message = await channel.send("Retrieving messages")

    while True:
        players, players_list = await fetch_status()
        
        if players != "Offline":
            players_status = "Online"
        else:
            players_status = players

        newMessage = (
            f"## Server Status\n"
            f"**IP:**  `{server_ip}`\n"
            f"- Status:  `{players_status}`\n"
            f"- Players:  `{players}`\n"
            f"{players_list}\n\n"
            f"-# Last update: `{get_time()}`"
        )

        await message.edit(content=newMessage)
        await asyncio.sleep(30)

client.run(TOKEN)
