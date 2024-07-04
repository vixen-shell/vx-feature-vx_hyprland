from fastapi import WebSocket
from typing import Callable
from . import content
from .hypr_events import HyprEventsListener


@content.add_handler("socket")
async def events(websocket: WebSocket):
    try:
        HyprEventsListener.attach_websocket(websocket)

        while True:
            text = await websocket.receive_text()
            if text == "close":
                HyprEventsListener.detach_websocket(websocket)
                await websocket.close()
                break
    except:
        HyprEventsListener.detach_websocket(websocket)


@content.add_handler("action")
def add_event_listener(event_id: str, listener: Callable[[dict], None]):
    HyprEventsListener.add_listener(event_id, listener)


@content.add_handler("action")
def remove_event_listener(event_id: str, listener: Callable[[dict], None]):
    HyprEventsListener.remove_listener(event_id, listener)
