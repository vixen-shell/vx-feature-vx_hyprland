from fastapi import WebSocket
from typing import Callable
from . import content
from .hypr_events import HyprEventsListener


@content.add_handler("socket")
def events(websocket: WebSocket):
    async def on_open():
        HyprEventsListener.attach_websocket(websocket)

    async def on_close():
        HyprEventsListener.detach_websocket(websocket)

    return on_open, None, on_close


@content.add_handler("action")
def add_event_listener(event_id: str, listener: Callable[[dict], None]):
    HyprEventsListener.add_listener(event_id, listener)


@content.add_handler("action")
def remove_event_listener(event_id: str, listener: Callable[[dict], None]):
    HyprEventsListener.remove_listener(event_id, listener)
