import asyncio
import websockets

async def listen():
    uri = "wss://certstream.calidog.io/"
    async with websockets.connect(uri) as websocket:
        print("Connected async!")
        async for message in websocket:
            print("Received:", len(message), "bytes")
            break

asyncio.run(listen())
