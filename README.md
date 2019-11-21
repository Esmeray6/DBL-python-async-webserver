## DBL-python-async-webserver
An aiohttp webserver made for usage in discord.py bot cogs to keep track of upvoters.

## Requirements

* [MongoDB](https://www.mongodb.com/download-center/community)
  * [pymongo](https://api.mongodb.com/python/current/installation.html)
* [Python3.6+](https://www.python.org/downloads/release/python-360/)
* [Git](https://git-scm.com/downloads)
* discord.py rewrite (v1.0.0+) `python -m pip install -U discord.py` for Windows or `pip3 install -U discord.py` for Linux and MacOS.
  (Incompatible with discord.py async (0.16.12). Your bot has to use `rewrite` version.)

## Setting up

On Windows, you will have to open port 5000 on your router.

### Running

1. Put `webserver_settings.json` and `server.py` into your bot's cogs folder.
2. Run the bot.

### Webhooks

If you want this webserver to post a message in a certain channel when someone votes for your bot, follow the guide below.

1. Create a webhook in preferred channel.
2. Copy the webhook URL.
3. Open `webserver_settings.json` with any text editor.
4. In `discord_webhook_url` field, enter the webhook URL.
5. Save the file.
