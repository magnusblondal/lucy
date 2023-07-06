import lucy.discord_bot.app_comm as app_comm

APPLICATION_ID = 1112084773351997523
PUBLIC_KEY = "dbc83290d4c1c32f01fbbabf3428a39eab44116c3d5cac1ba5a87414ac878377"
TOKEN = "MTExMjA4NDc3MzM1MTk5NzUyMw.G86ADl.9jFGQ06EK-YbviI-G0XCgV2bZf5JmCZtoSpCzQ"
PERMISSIONS_INTEGER = 534726047808
# url = "https://discord.com/api/oauth2/authorize?client_id=1112084773351997523&permissions=18135502552128&scope=bot"

if __name__ == "__main__":
    app_comm.run(TOKEN)