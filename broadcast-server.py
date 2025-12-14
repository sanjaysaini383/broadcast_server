import argparse
from server import run_server
from client import run_client

def main():
    parser = argparse.ArgumentParser(description="WebSocket Broadcast Server")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Server command
    server_parser = subparsers.add_parser("start", help="Start the broadcast server")
    server_parser.add_argument("--host", default="localhost", help="Host to bind the server (default: localhost)")
    server_parser.add_argument("--port", type=int, default=8765, help="Port to bind the server (default: 8765)")
    
    # Client command
    client_parser = subparsers.add_parser("connect", help="Connect to the broadcast server")
    client_parser.add_argument("--host", default="localhost", help="Server host (default: localhost)")
    client_parser.add_argument("--port", type=int, default=8765, help="Server port (default: 8765)")
    
    args = parser.parse_args()

    if args.command == "start":
        run_server(args.host, args.port)
    elif args.command == "connect":
        run_client(args.host, args.port)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()