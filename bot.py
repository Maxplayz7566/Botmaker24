import asyncio
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
    global reply_modules
    reply_modules = {}
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
                            'embed': embed_data,
                            'type': 'reply'
                        }
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON in file {filename}: {e}")

def execute_code(code):
    """Execute the code and return the result."""
    try:
        # Create a dictionary to hold local variables
        local_vars = {}
        # Define the environment for execution, including safe access to the requests library
        exec_env = {
            "__builtins__": __builtins__,
            "requests": requests,
            "math": math,
            "random": random,
        }

        exec(code, exec_env, local_vars)

        return str(local_vars['result'])

    except Exception as e:
        print(f"Error executing code: {str(e)}")
        return f"Error executing code: {str(e)} with code: {code}"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')

    load_reply_modules('./modules')
    print("Loaded reply modules:", reply_modules)


def execute_code_in_string(text):
    while True:
        start = text.find("${")
        if start == -1:
            break
        end = text.find("}$", start)
        if end == -1:
            break

        code_to_execute = text[start + 2:end].strip()
        result = execute_code(code_to_execute)

        text = text[:start] + str(result) + text[end + 2:]

    return text

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    load_reply_modules('./modules')

    if message.content in reply_modules:
        reply_data = reply_modules[message.content]
        reply_message = reply_data['message']
        embed_data = reply_data['embed']

        reply_message = execute_code_in_string(reply_message)

        embed = None
        if embed_data:
            # Execute code in the embed description if it exists
            if 'description' in embed_data:
                embed_data['description'] = execute_code_in_string(embed_data['description'])
            embed = discord.Embed.from_dict(embed_data)

        await message.reply(content=reply_message, embed=embed)

    await bot.process_commands(message)
