from typing import Callable
from fastapi import WebSocket
from .HyprEventsListener import HyprEventsListener
from .. import content, utils


class __lifespan:
    @staticmethod
    @content.on_startup
    def on_startup():
        HyprEventsListener.start()

    @staticmethod
    @content.on_shutdown
    def on_shutdown():
        HyprEventsListener.stop()


class __socket_events:
    @staticmethod
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


class HyprEvents:
    @staticmethod
    def add_listener(event_id: str, listener: Callable[[dict], None]):
        HyprEventsListener.add_listener(event_id, listener)

    @staticmethod
    def remove_listener(event_id: str, listener: Callable[[dict], None]):
        HyprEventsListener.remove_listener(event_id, listener)
