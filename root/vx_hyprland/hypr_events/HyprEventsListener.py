import os, asyncio
from fastapi import WebSocket
from typing import List, Callable
from .EventData import EventData, event_data_map
from .. import utils, content

HYPR_SOCKET_PATH = "{}/hypr/{}/.socket2.sock".format(
    os.getenv("XDG_RUNTIME_DIR"), os.getenv("HYPRLAND_INSTANCE_SIGNATURE")
)


def is_valid_event_id(id: str) -> bool:
    available_event_ids = list(event_data_map.keys())

    if not id in available_event_ids:
        return False

    return True


class HyprEventsListener:
    _task: asyncio.Task = None
    _websockets: List[WebSocket] = []
    _listeners: dict[str, list[Callable[[dict], None]]] = {}

    @staticmethod
    def check_hypr_socket():
        return os.path.exists(HYPR_SOCKET_PATH)

    @staticmethod
    async def listener_task():
        reader, _ = await asyncio.open_unix_connection(HYPR_SOCKET_PATH)

        while True:
            data = EventData(await reader.readline()).to_json

            for websocket in HyprEventsListener._websockets:
                await websocket.send_json(data)

            for event_id in HyprEventsListener._listeners.keys():
                if event_id == data["id"]:
                    listeners = HyprEventsListener._listeners[event_id]

                    for listener in listeners:
                        try:
                            listener(data["data"])
                        except Exception as e:
                            utils.Logger.log_exception(e)

    @staticmethod
    def start():
        if not HyprEventsListener._task:
            if not HyprEventsListener.check_hypr_socket():
                utils.Logger.log(
                    f"[{content.feature_name}]: Socket not found", "WARNING"
                )
                return

            utils.Logger.log(f"[{content.feature_name}]: Start event listener")
            HyprEventsListener._task = asyncio.create_task(
                HyprEventsListener.listener_task()
            )

    @staticmethod
    def stop():
        if HyprEventsListener._task:
            utils.Logger.log(f"[{content.feature_name}]: Stop event listener")
            HyprEventsListener._task.cancel()
            HyprEventsListener._task = None

    @staticmethod
    def attach_websocket(websocket: WebSocket):
        HyprEventsListener._websockets.append(websocket)

    @staticmethod
    def detach_websocket(websocket: WebSocket):
        HyprEventsListener._websockets.remove(websocket)

    @staticmethod
    def add_listener(event_id: str, listener: Callable[[dict], None]):
        if not is_valid_event_id(event_id):
            return

        listeners = HyprEventsListener._listeners.get(event_id)

        if listeners:
            listeners.append(listener)
        else:
            HyprEventsListener._listeners[event_id] = [listener]

    @staticmethod
    def remove_listener(event_id: str, listener: Callable[[dict], None]):
        if not is_valid_event_id(event_id):
            return

        listeners = HyprEventsListener._listeners.get(event_id)

        if listeners:
            listeners.remove(listener)

            if len(listeners) == 0:
                HyprEventsListener._listeners.pop(event_id)
