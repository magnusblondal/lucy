import discord
from discord.ext import commands
# import responses

# async def send_message(ctx, message, is_private):
#     await ctx.send(message)

# class LucyBot:
#     def __init__(self) -> None:        
#         intents = discord.Intents.default()
#         intents.message_content = True
#         self.client = discord.Client(intents=intents)

#     @self.client.event
#     async def on_ready(self):
#         print(f'We have logged in as {self.client.user}')

#     @client.event
#     async def on_message(self, message):
#         if message.author == self.client.user:
#             return

#         if message.content.startswith('$hello'):
#             await message.channel.send('Hello!')

#     def run(self, public_key):
#         self.client.run(public_key)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

def run(token):
    client.run(token)
