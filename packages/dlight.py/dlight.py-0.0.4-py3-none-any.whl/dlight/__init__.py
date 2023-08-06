import aiohttp
import concurrent.futures
import asyncio
import json
websocketconnection = None

class events():
    async def on_message(message):
        return
    async def on_connect():
        return
    async def on_client_error(error):
        return
    async def on_dlight_error(error):
        return


class action():
    async def send(content,channel, footer=None):
        global globalbottoken
        global websocketconnection
        await websocketconnection.send_str(json.dumps({"t": "MESSAGE_CREATE","d": {"Auth": globalbottoken,"content": content,"channelid": channel, "footer":footer}}))

async def main(token):
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('wss://ws.dlight.xyz') as ws:

            global websocketconnection
            websocketconnection = ws
            while True:
              try:
                message = await ws.receive()
                message = message.json()
                if message['t'] == 'MESSAGE_CREATE':
                    class messageformat:
                        def __init__(self,message):
                            self.messagedata = message["d"]
                            self.content = message["d"]['content']
                            self.channel = message["d"]['channelid']
                            self.author_nametag = message['d']['author']['nametag']
                            self.author_username = message["d"]["author"]["username"]
                            self.author_isbot = message["d"]["author"]["bot"]
                            self.connection = ws
                    messagecontent = messageformat(message)
                    task = asyncio.create_task(events.on_message(messageformat(message)))
                    await task
                if message['t'] == None and message['op'] == 10:
                    task = asyncio.create_task(events.on_connect())
                    await task
                if message['t'] == "ERROR":
                    task = asyncio.create_task(events.on_dlight_error(message['d']))
                    await task
              except Exception as error:
                    task = asyncio.create_task(events.on_client_error(error))
                    await task

def run(token):
    global globalbottoken
    globalbottoken = token
    asyncio.run(main("token"))
