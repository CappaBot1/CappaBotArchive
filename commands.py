import requests
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

url = "https://discord.com/api/v10/applications/1235729322027913218/guilds/948070330486882355/commands"

# Testing command
json = {
    "name": "test",
    "type": 3
}

# For authorization, you can use either your bot token
headers = {
    "Authorization": f"Bot {TOKEN}"
}

r = requests.post(url, headers=headers, json=json)