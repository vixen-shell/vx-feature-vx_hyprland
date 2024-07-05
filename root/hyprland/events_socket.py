from fastapi import WebSocket
from typing import Callable
from . import content, utils
from .hypr_events import HyprEventsListener


class EventHandler(utils.SocketHandler):
    def __init__(self, websocket: WebSocket) -> None:
        super().__init__(websocket)

    async def on_opening(self):
        HyprEventsListener.attach_websocket(self.websocket)

    async def on_closing(self):
        HyprEventsListener.detach_websocket(self.websocket)


@content.add_handler("socket")
def events(websocket: WebSocket):
    return EventHandler(websocket)


@content.add_handler("action")
def add_event_listener(event_id: str, listener: Callable[[dict], None]):
    HyprEventsListener.add_listener(event_id, listener)


@content.add_handler("action")
def remove_event_listener(event_id: str, listener: Callable[[dict], None]):
    HyprEventsListener.remove_listener(event_id, listener)
