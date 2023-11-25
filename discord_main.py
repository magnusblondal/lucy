import lucy.discord_bot.app_comm as app_comm
from config import settings

if __name__ == "__main__":
    app_comm.run(settings.DISCORD_TOKEN)
