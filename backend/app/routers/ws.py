import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.utils.ws_manager import manager

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    """Main WebSocket endpoint for real-time updates.

    Clients send: {"type": "auth", "token": "<jwt>"}
    Server sends: {"type": "...", "data": {...}}

    Event types: payment_received, invoice_updated, reminder_sent,
                 notification, dashboard_update
    """
    await ws.accept()
    business_id = None

    try:
        # Wait for auth message
        auth_msg = await ws.receive_text()
        data = json.loads(auth_msg)

        if data.get("type") != "auth" or not data.get("token"):
            await ws.send_json({"type": "error", "message": "Send auth token first"})
            await ws.close(code=4001)
            return

        from app.utils.auth import _decode_token
        business_id = _decode_token(data["token"])
        if not business_id:
            await ws.send_json({"type": "error", "message": "Invalid token"})
            await ws.close(code=4001)
            return

        manager.connect(business_id, ws)
        await ws.send_json({"type": "connected", "data": {"business_id": business_id}})

        # Keep connection alive, handle client messages
        while True:
            msg = await ws.receive_text()
            parsed = json.loads(msg)

            if parsed.get("type") == "ping":
                await ws.send_json({"type": "pong"})

    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        if business_id:
            manager.disconnect(business_id, ws)
