import os
import json

import discord
from discord.ext import commands

# Imports for code execution
import requests
from random import random
import math
# End imports for code execution

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=" ", intents=intents)

reply_modules = {}

def load_reply_modules(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                try:
                    data = json.load(file)

                    if data.get('type') == 'reply':
                        command = data.get('command')
                        reply_content = data.get('replyContent', {}).get('message', '')
                        embed_data = data.get('replyContent', {}).get('embed', None)

                        # Create a command key for easy access
                        command_key = json.load(open('data.json', 'r'))['prefix'] + command

                        # Store the reply content and embed data
                        reply_modules[command_key] = {
                            'message': reply_content,
                            'embed': embed_data
                        }
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON in file {filename}: {e}")

def execute_code(code):
    """Execute the code and return the result."""
    try:
        # Create a dictionary to hold local variables
        local_vars = {}
        # Allow requests and any other libraries you want to use
        exec(code, {"__builtins__": __builtins__, "requests": requests, "bot": bot, "math": math, "random": random}, local_vars)
        # Try to get a result from the local variables
        if 'result' in local_vars:
            return str(local_vars['result'])
        return str(local_vars) if local_vars else "No output"
    except Exception as e:
        return f"Error executing code: {str(e)}"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')

    load_reply_modules('./modules')
    print("Loaded reply modules:", reply_modules)

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    load_reply_modules('./modules')

    if message.content in reply_modules:
        reply_data = reply_modules[message.content]
        reply_message = reply_data['message']
        embed_data = reply_data['embed']

        # Check for ${arbitrary python code} in the reply message
        while "${" in reply_message and "}" in reply_message:
            start = reply_message.find("${") + 2
            end = reply_message.find("}", start)
            if end == -1:
                break  # No closing brace found
            code_to_execute = reply_message[start:end].strip()
            result = execute_code(code_to_execute)
            reply_message = reply_message.replace(f"${{{code_to_execute}}}", str(result))

        # Create an embed if embed data exists
        embed = None
        if embed_data:
            embed = discord.Embed.from_dict(embed_data)

        await message.reply(content=reply_message, embed=embed)

    await bot.process_commands(message)
