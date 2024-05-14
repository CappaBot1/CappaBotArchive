import asyncio, discord, os, random, sys, typing
from discord import app_commands
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
SERVER = discord.Object(948070330486882355)

# Basic variables
personToReact = 0
personToCopy = 0

# Print some info
print(f"Last 4 digits of bot token: {TOKEN[-4:]}")
print(f"CappaBot ID: {CAPPABOT}")
print(f"Server: {SERVER.id}")

# Make the discord client
client = discord.Client(intents=discord.Intents.all())

# Make the command tree
tree = app_commands.CommandTree(client)

# Stop command. Will stop the program from running.
@tree.command(
	description="Stop me."
)
async def stop(interaction: discord.Interaction):
	print("Stopping from the stop command.")
	await interaction.response.send_message("Ok, I'll stop now.")
	sys.exit("Someone told me to stop.")

# Testing command. Subject to change.
@tree.command(
	description="Testing command"
)
async def test(interaction: discord.Interaction):
	print("Test")
	await interaction.response.send_message("Testing...")
	for i in range(1, 122):
		x = i/4
		await interaction.edit_original_response(content=f"Testing number {x}\n{'-'*int(x*4)}")
	await interaction.followup.send("Done testing.")

# Ping command. Reply with "pong" asap
@tree.command(
	description="I will reply with 'pong' as fast as I can."
)
async def ping(interaction: discord.Interaction):
	print("Got ping command")
	print(interaction)
	await interaction.response.send_message("Pong")

# React command. Give a user to react to. If blank, don't react to anyone
@tree.command(
	description="I will react to the user you specify. If empty, stop reacting."
)
@app_commands.describe(
	member="The user to react to."
)
async def react(interaction: discord.Interaction, member: typing.Optional[discord.Member] = None):
	global personToReact

	# If a user was given, react to them
	if member:
		personToReact = str(member)
	# Else, react to no one
	else:
		personToReact = "no one"

	# Say who I will react to
	await interaction.response.send_message(f"I will react to {personToReact}")

# Copy command. Give a user to copy. If blank, don't copy anyone
@tree.command(
	description="I will copy the user you specify. If empty, stop copying."
)
@app_commands.describe(
	member="The user to copy."
)
async def copy(interaction: discord.Interaction, member: typing.Optional[discord.Member] = None):
	global personToCopy

	# If a user was given, copy them
	if member:
		personToCopy = str(member)
	# Else, copy no one
	else:
		personToCopy = "no one"

	# Say who I will copy
	await interaction.response.send_message(f"I will copy {personToCopy}.")

# The voice commands
class VoiceGroup(app_commands.Group):
	# Connect to a voice channel
	@app_commands.command(
		name="connect",
		description="Connect to a given voice channel."
	)
	@app_commands.describe(
		channel = "The voice channel I will join."
	)
	async def connect(self, interaction: discord.Interaction, channel: discord.VoiceChannel):
		await interaction.response.send_message(f"Trying to connect to {channel}.")
		await channel.connect()
		await interaction.edit_original_response(content=f"Connected to {channel}.")

	# Disconnect from a voice channel
	@app_commands.command(
		name="disconnect",
		description="Disconnect from the current voice call I am in."
	)
	async def disconnect(self, interaction: discord.Interaction):
		await interaction.response.send_message("Trying to disconnect.")
		for voice_client in client.voice_clients:
			if voice_client.guild == interaction.guild:
				await voice_client.disconnect()
		await interaction.response.edit_message(content="Disconnected.")

@tree.command(
	name="say",
	description="Say whatever string of text you input."
)
@app_commands.describe(
	text="The text I will output."
)
async def say(interaction: discord.Interaction, text: str):
	await interaction.response.send_message(text)

# This will run when the bot is ready to take inputs
@client.event
async def on_ready():
	# Print that we have connected to discord.
	print(f'{client.user} has connected to Discord!')

	# Add the voice commands to the command tree
	voiceGroup = VoiceGroup(name="voice", description="The voice commands can make me connect and disconnect from a voice call.")
	tree.add_command(voiceGroup)

	# Copy the commands to the server
	tree.copy_global_to(guild=SERVER)
	# Sync the commands to the server
	await tree.sync(guild=SERVER)

	if DEBUG:
		user = client.get_user(CAPPABOT)
		await user.send("Cappa Bot has started")

		#channel = client.get_channel(CHANNEL)
		#await channel.send("Cappa Bot is online")
	
	print("Finished loading.")

# When someone send a message
@client.event
async def on_message(message: discord.Message):
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
			
			# Check if "wrong" is in the message and say something if there is.
			if "wrong" in message.content.lower():
				await message.channel.send("Haha, you said 'wrong'. Get timed out.")
			
			# Check if "puh" is in the message and respond with the puh gif
			if "puh" in message.content.lower():
				await message.channel.send(file=discord.File("puh.gif"))

			# Check if I need to react to the person
			if message.author.name == personToReact:
				# React to them
				print("I should react to that")
				reactionImage = REACTION_IMAGE_PATH + random.choice(REACTION_IMAGE_NAMES)
				await message.reply("", file=discord.File(reactionImage))
			
			# Check if I need to copy the person
			if message.author.name == personToCopy:
				# Copy them
				print("I should copy that")
				await message.channel.send(message.content)

	# If the message was sent in a text channel
	else:
		print(f"""Message in DM's. Details:
	Sent from: {message.author.name} / {message.author.global_name}
	Contents: {message.content}""")
	
	print("-"*50)

client.run(TOKEN)

#CHANNEL.send("Cappa Bot died :(")

print("Cappa Bot has ended.") 