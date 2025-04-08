import asyncio
import websockets

async def test_stream():
    uri = "ws://localhost:8000/stream"  # This matches your FastAPI websocket route
    async with websockets.connect(uri) as websocket:
        while True:
            data = await websocket.recv()
            print(data)

asyncio.run(test_stream())
