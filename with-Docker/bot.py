from datetime import datetime, timezone
import discord
import asyncio
import pytz
import os
from mcstatus import JavaServer

TOKEN = os.getenv("DISCORD_TOKEN") 
GUILD_ID = os.getenv("GUILD_ID")
CHANNEL_ID =  None
server_ip = None
server = None
update_task = None

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

# Function to update the message
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await tree.sync(guild=discord.Object(id=GUILD_ID))

# Function to get current time
timezone = pytz.timezone("Europe/Rome")
def get_time():
    return datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S")

# Slash command: /setip
@tree.command(name="setip", description="Imposta l'indirizzo IP del server Minecraft", guild=discord.Object(id=GUILD_ID))
async def setip(interaction: discord.Interaction, ip: str):
    global server_ip, server
    server_ip = ip
    try:
        server = JavaServer.lookup(server_ip)
        await interaction.response.send_message(f"IP del server impostato a `{ip}`", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Errore nel settare il server IP: `{e}`", ephemeral=True)

    await start_update_loop()                                            

# Slash command: /setchannel
@tree.command(name="setchannel", description="Imposta il canale per gli aggiornamenti", guild=discord.Object(id=GUILD_ID))
async def setchannel(interaction: discord.Interaction):
    global CHANNEL_ID
    CHANNEL_ID = interaction.channel.id
    await interaction.response.send_message(f"Canale impostato: {interaction.channel.mention}", ephemeral=True)

    await start_update_loop()

async def start_update_loop():
    global update_task
    if update_task is None and CHANNEL_ID and server_ip:
        channel = client.get_channel(CHANNEL_ID)
        if not channel:
            print("Errore: canale non trovato")
            return

        async for message in channel.history(limit=10):
            if message.author == client.user:
                break
        else:
            message = await channel.send("Retrieving messages")

        update_task = client.loop.create_task(update_loop(message))

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

# Message loop
async def update_loop(message):
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
        await asyncio.sleep(60)

client.run(TOKEN)