import asyncio
import discord
import os
import sys
import random
from dotenv import load_dotenv

# CappaBot.py
print("CappaBot has started loading...")

# Enivornment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
SERVER = os.getenv("DISCORD_GUILD")
CHANNEL = int(os.getenv("DISCORD_CHANNEL_ID"))
CAPPABOT = int(os.getenv("DISCORD_CAPPABOT_ID"))

# Constant variables
DEBUG = False

# Basic variables
personToReact = 0

print(f"Last 5 digits of token: {TOKEN[-5:]}")
print(f"Channel ID: {CHANNEL}")
print(f"CappaBot ID: {CAPPABOT}")

# intents = discord.Intents(3136)
intents = discord.Intents.all()
#intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
	print(f'{client.user} has connected to Discord!')

	if DEBUG:
		user = client.get_user(CAPPABOT)
		await user.send("Cappa Bot has started")

		channel = client.get_channel(CHANNEL)
		await channel.send("Cappa Bot is online")

# When someone send a message
@client.event
async def on_message(message):
	global personToReact
	global personToCopy
	# Print the message info
	print(message)
	# If the message was sent in a DM to the bot
	if message.guild:
		# If the message was sent by a bot
		if message.author.bot:
			print("Messsage sent by bot")

			# If the message was sent by me
			if message.author.name == "Cappa Bot":
				print(f"Message was sent by me in: {message.guild.name} > {message.channel.name} | {message.contents}")
			# If the message was sent by dad bot
			if message.author.name == "Dad Bot":
				# Say shut up dad bot
				await message.reply("Shut up dad bot.")
			
		# If the message was not sent by a bot	
		else:
			# Print message details
			print(f"""Message in text channel. Details:
	Server: {message.guild.name}
	Channel: {message.channel.name}
	Sent from: {message.author}
	Contents: {message.content}""")
			
			# Check if from Niv
			#if message.author.name == "drporknswine":
			#	await message.channel.send("<@783924515549347870> said something")
   
			# Check if the message was from the person I need to react to
			if message.author.id == personToReact:
				# React to them
				print("I should react to that")
				await message.reply("[reaction image]")

			# Check if it was a command
			if message.content.lower() == "stop":
				message.channel.send("Ok, I'll stop now.")
				print("I should stop now")
				sys.exit("Someone told me to stop.")
			elif message.content.lower()[:5] == "react":
				personToReact = int(message.content[8:-1])
				print(f"I will react to: {personToReact}")
				await message.channel.send(f"I will react to <@{personToReact}>")

			elif message.content.lower()[:4] == "copy":
				personToCopy = int(message.content[7:-1])
				print(f"I will copy: {personToCopy}")
				await message.channel.send(f"I will copy <@{personToCopy}>")
	
	# If the message was sent in a text channel
	else:
		print(f"""Message in DM's. Details:
	Sent from: {message.author.name} / {message.author.global_name}
	Contents: {message.contents}""")
		
	print("-"*50)

client.run(TOKEN)

CHANNEL.send("Cappa Bot died :(")

print("Cappa Bot has ended.") 