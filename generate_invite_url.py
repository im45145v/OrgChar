"""
Generate Discord bot invitation URL
"""

import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlencode

# Load environment variables
load_dotenv()

# Get bot token from environment
bot_token = os.getenv("DISCORD_BOT_TOKEN")

if not bot_token:
    print("Error: DISCORD_BOT_TOKEN not found in .env file")
    exit(1)

# Try to get the application ID using the Discord API
try:
    headers = {
        'Authorization': f'Bot {bot_token}'
    }
    response = requests.get('https://discord.com/api/v10/users/@me', headers=headers)
    if response.status_code == 200:
        data = response.json()
        client_id = data.get('id')
        bot_name = data.get('username')
        print(f"Successfully retrieved bot information: {bot_name} (ID: {client_id})")
    else:
        print(f"Error getting bot information from Discord API: {response.status_code}")
        print("Please enter your bot's client ID manually.")
        client_id = input("Enter your bot's client ID: ")
except Exception as e:
    print(f"Error: {e}")
    print("Please enter your bot's client ID manually.")
    client_id = input("Enter your bot's client ID: ")

# Required permissions
permissions = [
    "READ_MESSAGES",      # View channels
    "SEND_MESSAGES",      # Send messages
    "EMBED_LINKS",        # Embed links
    "READ_MESSAGE_HISTORY", # Read message history
    "USE_EXTERNAL_EMOJIS", # Use external emojis
    "ADD_REACTIONS",      # Add reactions
]

# Calculate permission integer
permission_map = {
    "READ_MESSAGES": 1 << 10,         # 1024
    "SEND_MESSAGES": 1 << 11,         # 2048
    "EMBED_LINKS": 1 << 14,           # 16384
    "READ_MESSAGE_HISTORY": 1 << 16,  # 65536
    "USE_EXTERNAL_EMOJIS": 1 << 18,   # 262144
    "ADD_REACTIONS": 1 << 6,          # 64
}

permission_int = sum(permission_map[p] for p in permissions)

# Generate OAuth2 URL
params = {
    'client_id': client_id,
    'scope': 'bot applications.commands',
    'permissions': permission_int
}

url = f"https://discord.com/api/oauth2/authorize?{urlencode(params)}"

print("\n=== Discord Bot Invitation URL ===\n")
print(url)
print("\nOpen this URL in your browser to add the bot to your server.")
print("Note: You need to have 'Manage Server' permission in the server you want to add the bot to.")
