import discord, os, random, sys, typing
from discord import app_commands, FFmpegPCMAudio
from dotenv import load_dotenv

# CappaBot.py
print("CappaBot has started loading...")

# Enivornment variables
load_dotenv(dotenv_path=".env")
TOKEN = os.getenv("DISCORD_TOKEN")
OWNER = int(os.getenv("DISCORD_OWNER_ID"))
try:
	DEBUG = os.getenv("DEBUG")
except:
	DEBUG = False

try:
	if os.getenv("SERVER"):
		print("Running on server")
		SERVER = True
except:
	print("Not running on server")
	SERVER = False

print("Debug is set to: " + DEBUG)

if DEBUG:
	print("I am at: " + os.getcwd())

# Try find the reaction images
try:
	# Get reaction images
	REACTION_IMAGE_PATH = "reactionImages/"
	reactionImageNames = os.listdir(REACTION_IMAGE_PATH)
except:
	# Reaction image folder doesn't exist
	print("No reaction images found")
	REACTION_IMAGE_PATH = ""
	reactionImageNames = ("puh.gif", "john.gif")

# Print the amount of reaction images found
print(f"Found {len(reactionImageNames)} reaction images in {REACTION_IMAGE_PATH}")

# Shuffle the order of the reactionImages and set the number to 0
random.shuffle(reactionImageNames)
reactionImageNumber = 0

# Basic variables
personToReact = "no one"
personToCopy = "no one"
personToQuote = "no one"

# Make the discord client
client = discord.Client(intents=discord.Intents.all())

# Make the command tree
tree = app_commands.CommandTree(client)

# The exit command
def exit():
	print("Exiting...")
	sys.exit("Cappa Bot has terminated.")

# Stop command. Will stop the program from running.
@tree.command(
	description="Stop me."
)
async def stop(interaction: discord.Interaction):
	print("Stopping from the stop command.")
	await interaction.response.send_message("Ok, I'll stop now.")
	exit()

# Testing command. Subject to change.
@tree.command(
	description="Testing command"
)
async def test(interaction: discord.Interaction):
	print("Test")
	await interaction.response.send_message("Testing...")
	# Put test here:
	
	# End of test
	await interaction.followup.send("Done testing.")

# Ping command. Reply with "pong" asap
@tree.command(
	description="I will reply with 'pong' as fast as I can."
)
async def ping(interaction: discord.Interaction):
	print("Got ping command")
	print(interaction)
	await interaction.response.send_message("Pong")

# The John command
@tree.command(
	description="John image"
)
async def john(interaction: discord.Interaction):
	await interaction.response.send_message("John", file=discord.File("john.gif"))

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
	await interaction.response.send_message(f"I will react to {personToReact}", ephemeral=True)

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
	await interaction.response.send_message(f"I will copy {personToCopy}.", ephemeral=True)

# Quote command. Give a user to quote. If blank, don't quote anyone
@tree.command(
	description="I will put quotes around any message the user sends. If empty, stop quoting."
)
@app_commands.describe(
	member="The user to quote."
)
async def quote(interaction: discord.Interaction, member: typing.Optional[discord.Member] = None):
	global personToQuote

	# If a user was given, quote them
	if member:
		personToQuote = str(member)
	# Else, quote no one
	else:
		personToQuote = "no one"

	# Say who I will quote
	await interaction.response.send_message(f"I will quote {personToQuote}.", ephemeral=True)

# The calculator command
@tree.command(
	description="Calculator"
)
@app_commands.describe(
	operation="The math operation",
	num_one="The first number",
	num_two="The second number"
)
@app_commands.choices(
	operation=[
		app_commands.Choice(name="add", value="+"),
		app_commands.Choice(name="subtract", value="-"),
		app_commands.Choice(name="multiply", value="*"),
		app_commands.Choice(name="divide", value="/")
	]
)
async def calculator(interaction: discord.Interaction, operation: app_commands.Choice[str], num_one: float, num_two: float):
	calculation = f"{num_one} {operation.value} {num_two}"
	await interaction.response.send_message(f"Calculating: {calculation}")
	answer = eval(calculation)
	await interaction.followup.send(answer)

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
		global voiceChannel
		voiceChannel = await channel.connect()
		audioFile = FFmpegPCMAudio("connectedAudio.wav")
		player = voiceChannel.play(audioFile)
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
		await interaction.edit_original_response(content="Disconnected.")
	
	# Play the "toPlay.wav" file
	@app_commands.command(
		name="play",
		description="Play the audio."
	)
	async def play(self, interaction: discord.Interaction):
		await interaction.response.send_message(f"Trying to play audio.")
		audioFile = FFmpegPCMAudio("toPlay.wav")
		player = voiceChannel.play(audioFile)
		await interaction.edit_original_response(content="Playing audio.")

class SuggestionGroup(app_commands.Group):
	# Add a suggestion to the file
	@app_commands.command(
		name="add",
		description="Add a suggestion."
	)
	async def addSuggestion(self, interaction: discord.Interaction, text: str):
		await interaction.response.send_message(f"Adding your suggestion: {text}")
		
		print(f"Adding \"{text}\" to the suggestions file")
		with open("suggestions.txt", "a") as file:
			file.write(text + "\n")

	# Show all of the suggestions in the suggestions.txt file
	@app_commands.command(
		name="show",
		description="Show the current suggestions."
	)
	async def showSuggestions(self, interaction: discord.Interaction):
		await interaction.response.send_message("Showing suggestions...")

		with open("suggestions.txt", "r") as file:
			for i, suggestion in enumerate(file.readlines()):
				await interaction.followup.send(f"{i}: {suggestion}")

	# Remove a suggestion from the suggestions.txt file
	@app_commands.command(
		name="remove",
		description="Remove a suggestion from the suggestion file."
	)
	@app_commands.describe(
		line_num = "The line of the suggestion file to remove"
	)
	async def removeSuggestion(self, interaction: discord.Interaction, line_num: int):
		await interaction.response.send_message(f"Removing line {line_num}")

		with open("suggestions.txt", "r") as fileIn:
			oldFile = fileIn.readlines()
		
		with open("suggestions.txt", "w") as fileOut:
			for i, line in enumerate(oldFile):
				if not i == line_num:
					fileOut.write(line)
				else:
					print(f"Removed \"{line}\" from the suggestions file")
					await interaction.followup.send(f"\"{line}\" has been removed.")

# The say command. Repeat whatever input the user gives.
@tree.command(
	name="say",
	description="Say whatever string of text you input."
)
@app_commands.describe(
	text="The text I will output."
)
async def say(interaction: discord.Interaction, text: str):
	await interaction.response.send_message("Doin` it", ephemeral=True)
	await interaction.channel.send(text)

# The sync command
@tree.command(
	description="Sync commands for this server"
)
async def sync(interaction: discord.Interaction):
	await interaction.response.send_message("Syncing...")
	await tree.sync(guild=interaction.guild)
	await interaction.edit_original_response(content="Synced")

# The clear command should clear old commands
@tree.command(
	description="Clears old commands"
)
async def clear_old(interaction: discord.Interaction):
	await interaction.response.send_message("Clearing...")
	tree.clear_commands(guild=interaction.guild)
	await interaction.edit_original_response(content="Clear")

# The clear command should clear old commands
@tree.command(
	description="Count your days."
)
async def count_days(interaction: discord.Interaction):
	await interaction.response.send_message("...", file=discord.File("count_your_days.gif"))

# This will run when the bot is ready to take inputs
@client.event
async def on_ready():
	# Print that we have connected to discord.
	print(f'{client.user} has connected to Discord!')

	# Add the voice commands to the command tree
	tree.add_command(VoiceGroup(name="voice", description="The voice commands can make me connect and disconnect from a voice call."))

	# Add the suggestion commands to the command tree
	tree.add_command(SuggestionGroup(name="suggestions", description="The suggestion commands modify the suggestions.txt file."))

	# Sync globally
	print("Syncing globally...")
	await tree.sync(guild=None)

	if DEBUG:
		user = client.get_user(OWNER)
		await user.send("Cappa Bot has started")
	
	print("Finished loading.")

# When someone send a message
@client.event
async def on_message(message: discord.Message):
	global personToReact
	global personToCopy
	global personToQuote

	global reactionImageNumber

	# Print the message info
	if DEBUG:
		print(message)
	else:
		print("I saw a message")

	# If the message was sent in a server
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
			
		# If the message was not sent by me (to prevent looping)
		if message.author.name != "Cappa Bot":
			# Print message details
			if DEBUG:
				print(f"""Message in text channel. Details:
	Server: {message.guild.name}
	Channel: {message.channel.name}
	Sent from: {message.author}
	Contents: {message.content}""")

			# Check if "wrong" is in the message and if it was sent in the server. Say something if there is.
			if "wrong" in message.content.lower() and message.guild.id == 948070330486882355:
				await message.channel.send("Haha, you said 'wrong'. Get timed out.")
			
			if str(message.author) == "callumpuddle":
				print("callum talked")
				user = client.get_user(1225557797329178624)
				await user.send("shut up callum")

			# Check if "puh" is in the message and respond with the puh gif
			if "puh" in message.content.lower():
				for word in message.content.lower().split(" "):
					if "puh" in word:
						randomNum = random.random()
						print(randomNum)
						if randomNum < 0.18:
							await message.channel.send(file=discord.File("puh.gif"))

			# Check if "pluh" is in the message and react with 🗣️
			if "pluh" in message.content.lower():
				await message.add_reaction(u"\U0001F5E3")

			# Check if I need to react to the person
			if message.author.name == personToReact:
				# React to them
				print("I should react to that")
				reactionImage = REACTION_IMAGE_PATH + reactionImageNames[reactionImageNumber % len(reactionImageNames)]
				reactionImageNumber += 1
				await message.reply("", file=discord.File(reactionImage))
			
			# Check if I need to copy the person
			if message.author.name == personToCopy:
				# Copy them
				print("I should copy that")
				await message.channel.send(message.content)
			
			# Check if I need to quote the person
			if message.author.name == personToQuote:
				# Quote them
				print("I should quote that")
				await message.channel.send(f"\"{message.content}\"")

	# If the message was sent in a DM channel
	else:
		if DEBUG:
			print(f"""Message in DM's. Details:
	Sent from: {message.author.name} / {message.author.global_name}
	Contents: {message.content}""")
	
	print("-"*50)

print("Starting discord client")
client.run(TOKEN)
print("Ended discord client")

print("Cappa Bot has ended.")
