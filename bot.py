import selfcord
from selfcord.ext import tasks
import random
import asyncio
import configparser
import os

config = configparser.ConfigParser()
config_file = os.path.join(os.path.dirname(__file__), 'config.txt')
config.read(config_file)

client = selfcord.Client()

channel_id = int(config.get('Configuration','ChannelID'))
randomness = bool(config.get('Configuration','Randomness'))
messages = str(config.get('Configuration','TaskMessages')).split(",")
timed = int(config.get('Configuration','TaskTime'))
token = str(config.get('Configuration','Token'))
delay = 0
completed=0

@tasks.loop(minutes = timed+delay)
async def best_loop():
    try:
        if randomness == True:
            delay = random.randint(3,10)
        else:
            delay = 0
        channel = client.get_channel(channel_id)
        for msg in messages:
            await channel.send(msg)
            await asyncio.sleep(6)
        global completed
        completed+=1
        print(f'Task completed! ({completed})')
    except:
        print('Improper configuration! :(')

@client.event
async def on_ready():
    print(f'Ready to do some tasks! >:3 ({client.user})')
    best_loop.start()

client.run(token)
