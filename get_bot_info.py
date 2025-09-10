"""
Get Discord bot information and generate an invitation URL
"""

import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlencode

# Load environment variables
load_dotenv()

# Get bot token from environment
bot_token = os.getenv("DISCORD_BOT_TOKEN", "").strip('"')

if not bot_token:
    print("Error: DISCORD_BOT_TOKEN not found in .env file")
    exit(1)

print(f"Using bot token: {bot_token[:10]}...{bot_token[-5:]}")

# Get the application ID using the Discord API
headers = {
    'Authorization': f'Bot {bot_token}'
}

try:
    response = requests.get('https://discord.com/api/v10/users/@me', headers=headers)
    response.raise_for_status()
    
    data = response.json()
    client_id = data.get('id')
    bot_name = data.get('username')
    
    print(f"\nBot Information:")
    print(f"Name: {bot_name}")
    print(f"Client ID: {client_id}")
    
    # Required permissions for the bot
    permissions = 274877975552  # Standard permissions needed for a bot with message reading/sending capability
    
    # Generate OAuth2 URL
    params = {
        'client_id': client_id,
        'permissions': permissions,
        'scope': 'bot applications.commands'
    }
    
    url = f"https://discord.com/api/oauth2/authorize?{urlencode(params)}"
    
    print("\n=== Discord Bot Invitation URL ===\n")
    print(url)
    print("\nOpen this URL in your browser to add the bot to your server.")
    print("Note: You need to have 'Manage Server' permission in the server you want to add the bot to.")
    
except requests.exceptions.HTTPError as err:
    print(f"HTTP Error: {err}")
    print(f"Response content: {response.text}")
    print("\nPossible issues:")
    print("1. The bot token might be invalid or expired")
    print("2. The Discord API might be having issues")
    print("\nPlease check your token in the .env file and try again.")
    
except Exception as e:
    print(f"Error: {e}")
    print("Please get your client ID from the Discord Developer Portal manually.")
