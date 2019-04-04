from aiohttp import web, ClientSession
import asyncio
import discord 
from discord.ext import commands
from pymongo import MongoClient
import os
import json
import datetime

mongo = MongoClient()

file_path = os.path.dirname(__file__)

if file_path != '':
    settings_file = f"{file_path}/webserver_settings.json"
else:
    settings_file = "webserver_settings.json"

with open(settings_file) as settings:
    data = json.load(settings)
    webserver_password = data['webserver_password']
    discord_webhook = data['discord_webhook_url']

class TestServer(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def webserver(self):
        async def handler(request):
            data = await request.json()
            headers = dict(request.headers)
            authorization = headers.get('Authorization')
            if authorization == webserver_password:
                print("New upvote!")
                user_id = int(data.get('user'))
                bot_id = int(data.get('bot')) # ID of the bot that was upvoted
                request_type = data.get('type')
                weekend_status = data.get('isWeekend')
                now = datetime.datetime.utcnow()
                mongo.voters.vote.insert_one({
                    'type': request_type,
                    'user': user_id,
                    'bot': bot_id,
                    'weekend': weekend_status,
                    'time': now
                    })

                user = self.bot.get_user(user_id)
                if user:
                    upvoter = f"**Upvoter:** {user} ({user.mention})"
                else:
                    upvoter = f"**Upvoter:** <@{user_id}> ({user_id})"

                if bot_id != self.bot.user.id:
                    bot = self.bot.get_user(bot_id)
                    if bot:
                        upvoted_bot = f"**Upvoted bot:** {bot} ({bot.mention})"
                    else:
                        upvoted_bot = f"**Upvoted bot:** <@{bot_id}> ({bot_id})"
                else:
                    bot = self.bot.user
                    upvoted_bot = f"**Upvoted bot:** {bot} ({bot.mention})"

                if discord_webhook != "":
                    embed_title = "Test" if request_type == 'test' else 'New upvote!'
                    embed = discord.Embed(title=embed_title, description=f"{upvoter}\n{upvoted_bot}", timestamp=now, color=discord.Color.green())

                async with ClientSession() as session:
                    webhook = discord.Webhook.from_url(discord_webhook, adapter=discord.AsyncWebhookAdapter(session))
                    await webhook.send(embed=embed)

                return web.Response() # OK
            else:
                print(f"Wrong password:\nAuthorization header: {authorization}\nWebserver password: {webserver_password}")
                return web.Response(status=403) # Password is wrong

        async def testing(self):
            return web.Response(text="It works!")

        app = web.Application(loop=self.bot.loop)
        app.router.add_post('/dblwebhook', handler)
        app.router.add_get('/test', testing)
        runner = web.AppRunner(app)
        await runner.setup()
        self.site = web.TCPSite(runner, '0.0.0.0', 5000)
        await self.bot.wait_until_ready()
        await self.site.start()

    def cog_unload(self):
        mongo.close()
        asyncio.ensure_future(self.site.stop())

def setup(bot):
    ts = TestServer(bot)
    bot.add_cog(ts)
    bot.loop.create_task(ts.webserver())