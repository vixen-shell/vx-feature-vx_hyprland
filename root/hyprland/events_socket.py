from fastapi import WebSocket
from typing import Callable
from . import content
from .hypr_events import HyprEventsListener


@content.add_handler("socket")
async def events(websocket: WebSocket):
    def on_open(websocket):
        HyprEventsListener.attach_websocket(websocket)

    def on_close(websocket):
        HyprEventsListener.detach_websocket(websocket)

    return on_open, None, on_close


@content.add_handler("action")
def add_event_listener(event_id: str, listener: Callable[[dict], None]):
    HyprEventsListener.add_listener(event_id, listener)


@content.add_handler("action")
def remove_event_listener(event_id: str, listener: Callable[[dict], None]):
    HyprEventsListener.remove_listener(event_id, listener)
