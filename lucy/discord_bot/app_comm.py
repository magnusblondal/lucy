from typing import Optional

import discord
from discord import app_commands

import requests

LUCY_URL = "http://127.0.0.1:8000"

# from ..api.app.infrastructure.bot_repository import BotRepository


MY_GUILD = discord.Object(id=1104712326994722857)  # guild id


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')


@client.tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')

@client.tree.command()
async def bots(interaction: discord.Interaction):
    """Get list of bots."""
    response = requests.get(LUCY_URL + "/bot")
    if response.status_code == 200:
        data = response.json()
        bots = data["data"]
        embed = discord.Embed(title="Bots", description="Hér eru bottarnir", color=0x00ff00)
        embed.set_author(name="Lucy", url="http://127.0.0.1:8000", icon_url="https://cdn.discordapp.com/attachments/1112094929431318608/1112758213746626570/iammaz_android_small.jpg")
        embed.add_field(name="Field1", value="hi", inline=True)
        embed.add_field(name="\u200B", value="hooo", inline=True)
        for bb in bots:
            embed.add_field(name=bb['name'], value=f"{bb['capital']} {bb['entry_size']} {bb['so_size']} {bb['id']}", inline=False)
        await interaction.response.send_message(embed=embed)
    else:
        resp = f"Request failed with status code {response.status_code}"
        print(resp)
        await interaction.response.send_message(resp)


@client.tree.command()
@app_commands.describe(
    bot_id='Bot Id',
)
async def bot(interaction: discord.Interaction, bot_id: str):
    """Show single bot."""
    url = LUCY_URL + "/bot/" + bot_id + "/summary"
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        bot = data["data"]
        embed = discord.Embed(title=bot["name"], description=bot['description'], color=0x00ff00)
        embed.set_author(name="Lucy", url=url, icon_url="https://cdn.discordapp.com/attachments/1112094929431318608/1112758213746626570/iammaz_android_small.jpg")
        embed.add_field(name="\u200B", value="hooo", inline=True)
        embed.add_field(name=bot["name"], value=f"{bot['capital']} {bot['entry_size']} {bot['so_size']} {bot['id']} {bot['max_safety_orders']} {bot['allow_shorts']} ", inline=False)
        embed.add_field(name="Number of positions", value=bot['positions'], inline=True)
        embed.add_field(name="Open positions", value=bot['currently_open_positions'], inline=True)
        embed.add_field(name="Step 3", value=bot['profit'], inline=False)



        await interaction.response.send_message(embed=embed)
    else:
        resp = f"Request failed with status code {response.status_code}"
        print(resp)
        print(response.text)
        await interaction.response.send_message(resp)








# The rename decorator allows us to change the display of the parameter on Discord.
# In this example, even though we use `text_to_send` in the code, the client will use `text` instead.
# Note that other decorators will still refer to it as `text_to_send` in the code.
@client.tree.command()
@app_commands.rename(text_to_send='text')
@app_commands.describe(text_to_send='Text to send in the current channel')
async def send(interaction: discord.Interaction, text_to_send: str):
    """Sends the text into the current channel."""
    await interaction.response.send_message(text_to_send)


# To make an argument optional, you can either give it a supported default argument
# or you can mark it as Optional from the typing standard library. This example does both.
@client.tree.command()
@app_commands.describe(member='The member you want to get the joined date from; defaults to the user who uses the command')
async def joined(interaction: discord.Interaction, member: Optional[discord.Member] = None):
    """Says when a member joined."""
    # If no member is explicitly provided then we use the command user here
    member = member or interaction.user

    # The format_dt function formats the date time into a human readable representation in the official client
    await interaction.response.send_message(f'{member} joined {discord.utils.format_dt(member.joined_at)}')


# A Context Menu command is an app command that can be run on a member or on a message by
# accessing a menu within the client, usually via right clicking.
# It always takes an interaction as its first parameter and a Member or Message as its second parameter.

# This context menu command only works on members
@client.tree.context_menu(name='Show Join Date')
async def show_join_date(interaction: discord.Interaction, member: discord.Member):
    # The format_dt function formats the date time into a human readable representation in the official client
    await interaction.response.send_message(f'{member} joined at {discord.utils.format_dt(member.joined_at)}')


# This context menu command only works on messages
@client.tree.context_menu(name='Report to Moderators')
async def report_message(interaction: discord.Interaction, message: discord.Message):
    # We're sending this response message with ephemeral=True, so only the command executor can see it
    await interaction.response.send_message(
        f'Thanks for reporting this message by {message.author.mention} to our moderators.', ephemeral=True
    )

    # Handle report by sending it into a log channel
    log_channel = interaction.guild.get_channel(0)  # replace with your channel id

    embed = discord.Embed(title='Reported Message')
    if message.content:
        embed.description = message.content

    embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
    embed.timestamp = message.created_at

    url_view = discord.ui.View()
    url_view.add_item(discord.ui.Button(label='Go to Message', style=discord.ButtonStyle.url, url=message.jump_url))

    await log_channel.send(embed=embed, view=url_view)


def run(token):
    client.run(token)
