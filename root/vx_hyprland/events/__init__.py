from typing import Callable
from fastapi import WebSocket
from vx_root import root_feature
from .HyprEventsListener import HyprEventsListener
from .EventData import EventIds


feature = root_feature()


@feature.on_startup
def on_startup():
    if not HyprEventsListener.start():
        return False

    return True


@feature.on_shutdown
def on_shutdown():
    HyprEventsListener.stop()
    return True


class HyprEvents:
    @staticmethod
    def add_listener(event_id: EventIds, listener: Callable[[dict], None]):
        HyprEventsListener.add_listener(event_id, listener)

    @staticmethod
    def remove_listener(event_id: EventIds, listener: Callable[[dict], None]):
        HyprEventsListener.remove_listener(event_id, listener)

    @staticmethod
    def attach_websocket(websocket: WebSocket):
        HyprEventsListener.attach_websocket(websocket)

    @staticmethod
    def detach_websocket(websocket: WebSocket):
        HyprEventsListener.detach_websocket(websocket)
