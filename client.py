import asyncio
import websockets
import sys

async def listen_messages(websocket):
    """Listen for messages from server"""
    try:
        async for message in websocket:
            print(f"\n{message}")
            print("You: ", end="", flush=True)
    except websockets.exceptions.ConnectionClosed:
        print("\nConnection closed by server")
async def send_messages(websocket):
    """Send user input messages to server"""
    loop = asyncio.get_event_loop()
    while True:
        try:
            # Read input asynchronously
            message = await loop.run_in_executor(None, input, "You: ")
            if message.lower() in ['exit', 'quit']:
                print("Disconnecting...")
                break
            await websocket.send(message)
        except Exception as e:
            print(f"Error sending message: {e}")
            break

async def connect_client(host='localhost', port=8765):
    """Connect to the WebSocket server"""
    uri = f"ws://{host}:{port}"
    try:
        async with websockets.connect(uri) as websocket:
            print(f"Connected to {uri}")
            print("Type your message and press Enter. Type 'exit' to quit.\n")
            
            # Run both listener and sender concurrently
            await asyncio.gather(
                listen_messages(websocket),
                send_messages(websocket)
            )
    except ConnectionRefusedError:
        print(f"Could not connect to server at {uri}. Make sure the server is running.")
    except Exception as e:
        print(f"Connection error: {e}")

def run_client(host='localhost', port=8765):
    """Entry point for starting client"""
    try:
        asyncio.run(connect_client(host, port))
    except KeyboardInterrupt:
        print("\nClient shutting down gracefully...")