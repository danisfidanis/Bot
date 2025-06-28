import discord
from discord.ext import commands
from discord import app_commands
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)
tree = app_commands.CommandTree(client)

GUILD_ID = 1090287511525412944
VERIFICATION_CHANNEL_ID = 1378297006140948560
PLAYER_ROLE_NAME = "player"

used_nicknames = set()

# Read nicknames from file
def load_users():
    try:
        with open("UsersList.txt", "r") as f:
            return set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        return set()

valid_users = load_users()

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.channel.id != VERIFICATION_CHANNEL_ID or message.author.bot:
        return

    nickname = message.content.strip()
    member = message.author

    if nickname in valid_users and nickname not in used_nicknames:
        used_nicknames.add(nickname)
        try:
            await member.edit(nick=nickname)
            role = discord.utils.get(member.guild.roles, name=PLAYER_ROLE_NAME)
            if role:
                await member.add_roles(role)
            await message.reply(f"✅ Verified as `{nickname}`!")
        except discord.Forbidden:
            await message.reply("❌ I don't have permission to change your nickname.")
    else:
        await message.reply("❌ Invalid or already used nickname.")

# Slash commands
@tree.command(name="hello", description="Say hello", guild=discord.Object(id=GUILD_ID))
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"👋 Hello, {interaction.user.name}!")

@tree.command(name="serverinfo", description="Get server info", guild=discord.Object(id=GUILD_ID))
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    await interaction.response.send_message(
        f"📌 Server Name: {guild.name}\n👥 Members: {guild.member_count}"
    )

@tree.command(name="avatar", description="Show your avatar", guild=discord.Object(id=GUILD_ID))
async def avatar(interaction: discord.Interaction):
    await interaction.response.send_message(interaction.user.avatar.url)

@tree.command(name="react", description="Bot reacts to your message", guild=discord.Object(id=GUILD_ID))
async def react(interaction: discord.Interaction):
    await interaction.response.send_message("Reacting! 👍")
