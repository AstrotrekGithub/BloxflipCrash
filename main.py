from websocket import create_connection
import json, time
import requests
import random
import cloudscraper
import discord
from discord import app_commands


class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False 

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: 
            await tree.sync() 
            self.synced = True

# create discord client
client = aclient()
tree = app_commands.CommandTree(client)

# this is needed or else it will break
authentication = 'foza#7901'

@tree.command(name='crashjoin', description='Auto join a crash game with prediction.') 
async def self(interaction: discord.Interaction, bet: int, auth_token : str):
    # create cloudscraper, gets crash data
    scraper = cloudscraper.create_scraper(
        browser={
            'custom': 'ScraperBot/1.0',
        }
    )

    crash = scraper.get('https://api.bloxflip.com/games/crash').json()
    # get current crash status and sees if the game has started or not
    if authentication != 'foza#7901':
        print('stop skidding')
        return
    if crash['current']['status'] != 2:
        e = discord.Embed(title='Bloxflip Crash',description='Crash game currently in progress!')
        e.set_footer(text='Made By foza#7901')
        await interaction.response.send_message(embed=e,ephemeral=True)
        return

    ws = create_connection('wss://ws.bloxflip.com/socket.io/?EIO=3&transport=websocket',header={
        'Sec-WebSocket-Key': 'pPdhX6P/x8ZRc/lPDrNKqA==',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    })
    ws.send('40/crash,')
    # send ping
    ws.send(f'42/crash,["auth","{auth_token}"]')
    # authenticate with token via bloxflip websocket
    history = crash["history"]
    a =  [float(crashpoint["crashPoint"]) for crashpoint in history][::-1][-7:]
    average=(sum(a)/7)
    e = discord.Embed(title='Bloxflip Crash',description=f'Successfully joined game!\n**Prediction**: {int(average)}')
    e.set_footer(text='Made By foza#7901')
    await interaction.response.send_message(embed=e,ephemeral=True)
    ws.send('42/crash,'+json.dumps(
        ["join-game",
            {
                "autoCashoutPoint":int(average),
                "betAmount": int(bet)
            }
    ]))

# CREDITS | DONT REMOVE
# made by foza#7901
# CREDITS | DONT REMOVE

# put bot token where it says bot token here
client.run('bottokenhere')
