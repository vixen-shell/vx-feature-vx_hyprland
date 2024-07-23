from fastapi import WebSocket
from . import content, utils
from .hypr_events import HyprEventsListener


@content.add_handler("socket")
def events(websocket: WebSocket):
    class EventHandler(utils.SocketHandler):
        def __init__(self, websocket: WebSocket) -> None:
            super().__init__(websocket)

        async def on_opening(self):
            HyprEventsListener.attach_websocket(self.websocket)

        async def on_closing(self):
            HyprEventsListener.detach_websocket(self.websocket)

    return EventHandler(websocket)
