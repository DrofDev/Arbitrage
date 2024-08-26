import asyncio
import websockets
import json

async def subscribe_to_stream(uri, stream):
    async with websockets.connect(uri) as websocket:
        # Subscribe to the stream
        subscribe_message = json.dumps({
            "method": "SUBSCRIPTION",
            "params": [stream]
        })
        await websocket.send(subscribe_message)
        print(f"Sent subscription message: {subscribe_message}")

        # Wait for a response to confirm the subscription
        response = await websocket.recv()
        print(f"Received response: {response}")

        # Keep the connection open and listen for messages
        while True:
            try:
                message = await websocket.recv()
                message = json.loads(message)
                print(f"Received message: {message['d']}")
            except websockets.ConnectionClosed:
                print("Connection closed")
                break

# Main function to run the subscription
async def main():
    uri = "wss://wbs.mexc.com/ws"
    stream = "spot@public.bookTicker.v3.api@AAVEUSDT"  # Example symbol
    await subscribe_to_stream(uri, stream)

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
