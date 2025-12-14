# Broadcast Server

A lightweight broadcast server for delivering messages to many connected clients in real time.  
Supports HTTP-based publishing and WebSocket-based subscriptions so producers can push messages and clients can receive them instantly.

Works well as a simple pub/sub layer for notifications, live updates, chat, presence signals, and real-time dashboards.

---

## Table of contents
- [Features](#features)
- [Quick start](#quick-start)
  - [Run with Docker](#run-with-docker)
  - [Run locally](#run-locally)
- [Configuration](#configuration)
- [API](#api)
  - [HTTP publish](#http-publish)
  - [WebSocket subscription](#websocket-subscription)
  - [Health and metrics](#health-and-metrics)
- [Examples](#examples)
  - [Publish with curl](#publish-with-curl)
  - [Browser WebSocket client](#browser-websocket-client)
- [Deployment & scaling](#deployment--scaling)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## Features
- Publish messages over HTTP (POST).
- Real-time delivery to subscribers via WebSocket.
- Simple authentication token support for publishers.
- Optional CORS configuration.
- Health endpoint for container orchestration.
- Minimal dependencies — easy to containerize and deploy.

---

## Quick start

### Run with Docker
1. Build (if a Dockerfile is present):
   ```bash
   docker build -t broadcast-server .
   ```
2. Run:
   ```bash
   docker run -e PORT=8080 -e BROADCAST_SECRET="s3cr3t" -p 8080:8080 broadcast-server
   ```

### Run locally
1. Clone the repo:
   ```bash
   git clone https://github.com/sanjaysaini383/broadcast_server.git
   cd broadcast_server
   ```
2. Install dependencies and run according to the project's language/runtime:
   - For Node.js (example):
     ```bash
     npm install
     npm start
     ```
   - For other runtimes, use the project's README or start script defined in package files.
3. Set environment variables (see [Configuration](#configuration)) before running if needed.

---

## Configuration

Typical environment variables (adjust to your implementation):

- PORT — Port to listen on (default: 8080)
- BROADCAST_SECRET — Secret or token required to publish messages
- CORS_ORIGINS — Comma-separated list of allowed origins for browser clients
- LOG_LEVEL — Logging verbosity (info, debug, warn, error)
- MAX_CLIENTS — Optional limit for concurrent clients/subscribers

Set them in your environment or Docker container.



Notes:
- `topic` can be used to scope messages to a subset of clients if the server implements topic filtering.

### WebSocket subscription
- Endpoint: ws://<host>:<port>/ws
- Query params or subprotocols can be used for identifying topics, e.g.:
  - ws://localhost:8080/ws?topic=orders
- On connect, server will start sending messages published to the subscribed topics.
- Server may accept a token for restricted subscriptions, either as a query param or WebSocket subprotocol.


## Examples

### Publish with curl
```bash
curl -X POST http://localhost:8080/broadcast \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer s3cr3t" \
  -d '{
    "topic": "news",
    "message": { "title": "Hello", "body": "World" }
  }'
```

### Browser WebSocket client (JavaScript)
```javascript
const ws = new WebSocket("ws://localhost:8080/ws?topic=news");

ws.onopen = () => {
  console.log("connected");
};

ws.onmessage = (evt) => {
  const data = JSON.parse(evt.data);
  console.log("received", data);
};

ws.onclose = () => {
  console.log("disconnected");
};
```

---

## Deployment & scaling
- Run behind a load balancer that supports sticky sessions or use a broker (e.g., Redis, NATS) for multi-instance message distribution.
- For high availability:
  - Use a shared message bus (Redis Pub/Sub, Kafka, NATS) so each instance can receive published messages and forward to its connected clients.
  - Employ health checks and automatic restarts via Kubernetes or Docker Swarm.
- Use TLS (HTTPS / WSS) in production to secure messages in transit.

---

## Testing
- Unit tests: run the project's test command (e.g., `npm test` / `pytest` / `go test`).
- Integration tests:
  - Start the server locally.
  - Use curl or an HTTP client to POST messages.
  - Use a WebSocket client to subscribe and verify messages are received.
- Load test with tools like `wrk`, `k6`, or `locust` to validate connection handling and throughput.

---

## Contributing
Contributions are welcome. Please:
1. Open an issue to discuss major changes.
2. Send a pull request with a clear description and tests where applicable.
3. Follow the existing code style and include documentation for new features.

---

## License
Specify the license used by this project (e.g., MIT, Apache-2.0). If no license file exists, add one to clarify usage rights.

---

## Author
sanjaysaini383

