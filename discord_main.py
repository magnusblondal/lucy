import lucy.discord_bot.app_comm as app_comm
from config import settings

# url = "https://discord.com/api/oauth2/authorize?client_id=1112084773351997523&permissions=18135502552128&scope=bot"

if __name__ == "__main__":
    app_comm.run(settings.DISCORD_TOKEN)