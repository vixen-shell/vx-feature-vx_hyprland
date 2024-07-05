from fastapi import WebSocket
from typing import Callable
from . import content, utils
from .hypr_events import HyprEventsListener


class EventHandler(utils.SocketHandler):
    async def on_opening(self, websocket: WebSocket):
        HyprEventsListener.attach_websocket(websocket)

    async def on_closing(self, websocket: WebSocket):
        HyprEventsListener.detach_websocket(websocket)


@content.add_handler("socket")
def events():
    return EventHandler()


@content.add_handler("action")
def add_event_listener(event_id: str, listener: Callable[[dict], None]):
    HyprEventsListener.add_listener(event_id, listener)


@content.add_handler("action")
def remove_event_listener(event_id: str, listener: Callable[[dict], None]):
    HyprEventsListener.remove_listener(event_id, listener)
