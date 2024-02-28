import discord
import discord.ext
import os
import urllib.request
import re
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.all() 
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()

    await client.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name="/help, /play-song"))

    print(f"Status: online")


@tree.command(name="ban", description="ban user")
async def ban_user(interaction: discord.Interaction, user: discord.Member):
    if user:
        await interaction.guild.ban(user=user)
        await interaction.response.send_message(f"**User:** {user.mention} was not a skibidi sigma.")
    else:
        await interaction.response.send_message(f"**User:** {user.mention} doesn't exist.")


@tree.command(name="name", description="description")
async def slash_command(interaction: discord.Interaction):    
    await interaction.response.send_message(f'Hello {interaction.user.mention}')

@tree.command(name="play-song", description="plays a song")
async def play_song(interaction, song: str, loop: bool = False):
    encoded_song = urllib.parse.quote(f'{song} song')
    
    url = f"https://www.youtube.com/results?search_query={encoded_song}"

    html = urllib.request.urlopen(url)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    if interaction.user.voice:
        channel = interaction.user.voice.channel
        await interaction.user.voice.channel.connect(reconnect=True)
        await interaction.response.send_message(f"https://www.youtube.com/watch?v={video_ids[1]}")
        print(f'Channel: {channel}')
    else:
        await interaction.response.send_message("You must be in a voice channel to use this command.")

@tree.command(name="help", description="Help")
async def help(interaction: discord.Interaction):
    await interaction.response.send_message("Commands: /play-song, /name, /give-admin")

client.run(os.environ.get("PRIVATEKEY"))

