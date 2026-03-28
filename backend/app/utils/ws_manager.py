import asyncio
from collections import defaultdict
from fastapi import WebSocket


class ConnectionManager:
    """Manages WebSocket connections per business.

    A business can have multiple active connections (e.g., multiple tabs).
    Events are broadcast to all connections for a given business_id.
    """

    def __init__(self):
        self._connections: dict[str, set[WebSocket]] = defaultdict(set)

    def connect(self, business_id: str, ws: WebSocket):
        self._connections[business_id].add(ws)

    def disconnect(self, business_id: str, ws: WebSocket):
        self._connections[business_id].discard(ws)
        if not self._connections[business_id]:
            del self._connections[business_id]

    async def send_to_business(self, business_id: str, event_type: str, data: dict):
        """Send an event to all connections for a business."""
        if business_id not in self._connections:
            return
        message = {"type": event_type, "data": data}
        dead = []
        for ws in self._connections[business_id]:
            try:
                await ws.send_json(message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self._connections[business_id].discard(ws)

    async def broadcast(self, event_type: str, data: dict):
        """Send an event to ALL connected businesses."""
        tasks = []
        for business_id in list(self._connections.keys()):
            tasks.append(self.send_to_business(business_id, event_type, data))
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    @property
    def active_connections(self) -> int:
        return sum(len(conns) for conns in self._connections.values())


manager = ConnectionManager()
