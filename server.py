import asyncio
import websockets

connected_clients = set()

async def handle_client(websocket):
    """Handle incoming client connections and messages"""
    # Register client
    connected_clients.add(websocket)
    client_id = id(websocket)
    print(f"Client {client_id} connected.")
    try:
        async for message in websocket:
            print(f"Received message from client {client_id}: {message}")
            # Broadcast the message to all connected clients
            await broadcast_message(f"Client {client_id} says: {message}")
    except websockets.exceptions.ConnectionClosed:
            print(f"Client {client_id} disconnected.")
    finally:
        # Unregister client
        connected_clients.remove(websocket)
        print(f"Client {client_id} removed from connected clients.")

async def broadcast_message(message):
     if connected_clients:
        # Use asyncio.gather to send to all clients concurrently
        await asyncio.gather(
            *[client.send(message) for client in connected_clients],
            return_exceptions=True
        )

async def start_server(host='localhost', port=8765):
    """Start the WebSocket server"""
    server = await websockets.serve(handle_client, host, port)
    print(f"Server started on ws://{host}:{port}")
    print("Waiting for client connections...")
    await asyncio.Future()  # Run forever

def run_server(host='localhost', port=8765):
    """Entry point for starting server"""
    try:
        asyncio.run(start_server(host, port))
    except KeyboardInterrupt:
        print("\nServer shutting down gracefully...")