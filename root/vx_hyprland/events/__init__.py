from typing import Callable
from fastapi import WebSocket
from vx_root import root_feature
from .EventWatcher import EventWatcher
from .EventData import EventIds


feature = root_feature()


@feature.on_startup
def on_startup():
    if not EventWatcher.start():
        return False

    return True


@feature.on_shutdown
def on_shutdown():
    EventWatcher.stop()
    return True


class HyprEvents:
    @staticmethod
    def add_listener(event_id: EventIds, listener: Callable[[dict], None]):
        EventWatcher.add_listener(event_id, listener)

    @staticmethod
    def remove_listener(event_id: EventIds, listener: Callable[[dict], None]):
        EventWatcher.remove_listener(event_id, listener)

    @staticmethod
    def attach_websocket(websocket: WebSocket):
        EventWatcher.attach_websocket(websocket)

    @staticmethod
    def detach_websocket(websocket: WebSocket):
        EventWatcher.detach_websocket(websocket)
