import asyncio
import discord
from discord import app_commands
import os
import sys
import random
from dotenv import load_dotenv

# CappaBot.py
print("CappaBot has started loading...")

# Enivornment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CAPPABOT = int(os.getenv("DISCORD_CAPPABOT_ID"))

# Constant variables
DEBUG = False
REACTION_IMAGE_PATH = "../reactionImages/"
REACTION_IMAGE_NAMES = os.listdir(REACTION_IMAGE_PATH)
SERVER = 948070330486882355

# Basic variables
personToReact = 0
personToCopy = 0

print(f"Last 4 digits of bot token: {TOKEN[-4:]}")
print(f"CappaBot ID: {CAPPABOT}")

intents = discord.Intents.all()

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(
    name="test",
    description="Testing command",
    guild=discord.Object(id=SERVER)
)
async def first_command(interaction):
    await interaction.response.send_message("Hello!")

@client.event
async def on_ready():
	print(f'{client.user} has connected to Discord!')

	if DEBUG:
		user = client.get_user(CAPPABOT)
		await user.send("Cappa Bot has started")

		#channel = client.get_channel(CHANNEL)
		#await channel.send("Cappa Bot is online")

# When someone send a message
@client.event
async def on_message(message):
	global personToReact
	global personToCopy
	# Print the message info
	print(message)

	# Try parse the data into command and data
	try:
		command = message.content.lower().split(" ", 1)[0]
		data = " ".join(message.content.split()[1:])
		if DEBUG:
			print(f"Command: {command}")
			print(f"Data: {data}")
	
	# It might just be a command
	except:
		command = message.content.lower()
	# If the message was sent in a DM to the bot
	if message.guild:
		# If the message was sent by a bot
		if message.author.bot:
			print("Messsage sent by bot")

			# If the message was sent by me
			if message.author.name == "Cappa Bot":
				print(f"Message was sent by me in: {message.guild.name} > {message.channel.name} | {message.content}")
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

			# Check if the message is a command
			
			# Stop command
			if command == "stop":
				print("I should stop now")
				await message.channel.send("Ok, I'll stop now.")
				sys.exit("Someone told me to stop.")

			# React command
			elif command == "react":
				personToReact = int(message.content[8:-1])
				print(f"I will react to: {personToReact}")
				await message.channel.send(f"I will react to <@{personToReact}>")

			# Copy command
			elif message.content.lower()[:4] == "copy":
				personToCopy = int(message.content[7:-1])
				print(f"I will copy: {personToCopy}")
				await message.channel.send(f"I will copy <@{personToCopy}>")


			# Check if I need to react to the person
			if message.author.id == personToReact:
				# React to them
				print("I should react to that")
				reactionImage = REACTION_IMAGE_PATH + random.choice(REACTION_IMAGE_NAMES)
				await message.reply("", file=discord.File(reactionImage))
			
			# Check if I need to copy the person
			if message.author.id == personToCopy:
				# Copy them
				print("I should copy that")
				await message.channel.send(message.content)

	# If the message was sent in a text channel
	else:
		print(f"""Message in DM's. Details:
	Sent from: {message.author.name} / {message.author.global_name}
	Contents: {message.content}""")
		
	# Check DM command
	if command == "say":
		channelToSend = "0"
		toSend = "none"

		print("I will try to say something.")
		print(data)
		try:
			print("Trying to split")
			channelToSend, toSend = data.split(" ", 1)
			print("I split it")
		except:
			print("Failed to split")
			await message.channel.send("Invalid amount of parameters")
		
		print(channelToSend)
		print(toSend)

		print("Trying to conver channel ID to integer")
		if channelToSend.isnumeric():
			channelToSend = int(channelToSend)
			print("Changed to integer")
		else:
			await message.channel.send("Invalid channel ID, must be a number")

		print(type(channelToSend))

		print(f"Message: '{toSend}' was sent by {message.author.name}.")
		await client.get_channel(channelToSend).send(toSend)
	
	print("-"*50)

client.run(TOKEN)

#CHANNEL.send("Cappa Bot died :(")

print("Cappa Bot has ended.") 