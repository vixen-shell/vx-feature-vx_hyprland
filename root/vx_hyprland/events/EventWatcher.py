import os, asyncio
from vx_root import root_feature, utils
from fastapi import WebSocket
from typing import List, Callable
from .EventData import EventData, event_data_map

feature = root_feature()

HYPR_SOCKET_PATH = "{}/hypr/{}/.socket2.sock".format(
    os.getenv("XDG_RUNTIME_DIR"), os.getenv("HYPRLAND_INSTANCE_SIGNATURE")
)


def is_valid_event_id(id: str) -> bool:
    available_event_ids = list(event_data_map.keys())

    if not id in available_event_ids:
        return False

    return True


class EventWatcher:
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

            for websocket in EventWatcher._websockets:
                await websocket.send_json(data)

            for event_id in EventWatcher._listeners.keys():
                if event_id == data["id"]:
                    listeners = EventWatcher._listeners[event_id]

                    for listener in listeners:
                        try:
                            listener(data["data"])
                        except Exception as e:
                            EventWatcher._listeners[event_id].remove(listener)
                            utils.logger.log(
                                f"[{feature.name}]: Listener '{listener.__name__}' raise exception",
                                "WARNING",
                            )
                            utils.logger.log(
                                f"[{feature.name}]: Listener '{listener.__name__}' removed",
                                "WARNING",
                            )
                            utils.logger.log_exception(e)

    @staticmethod
    def start() -> bool:
        if not EventWatcher._task:
            if not EventWatcher.check_hypr_socket():
                utils.logger.log(f"[{feature.name}]: Socket not found", "WARNING")
                return False

            utils.logger.log(f"[{feature.name}]: Start event listener")
            EventWatcher._task = asyncio.create_task(EventWatcher.listener_task())

            return True

    @staticmethod
    def stop():
        if EventWatcher._task:
            utils.logger.log(f"[{feature.name}]: Stop event listener")
            EventWatcher._task.cancel()
            EventWatcher._task = None

    @staticmethod
    def attach_websocket(websocket: WebSocket):
        EventWatcher._websockets.append(websocket)

    @staticmethod
    def detach_websocket(websocket: WebSocket):
        EventWatcher._websockets.remove(websocket)

    @staticmethod
    def add_listener(event_id: str, listener: Callable[[dict], None]):
        if not is_valid_event_id(event_id):
            return

        listeners = EventWatcher._listeners.get(event_id)

        if listeners:
            listeners.append(listener)
        else:
            EventWatcher._listeners[event_id] = [listener]

    @staticmethod
    def remove_listener(event_id: str, listener: Callable[[dict], None]):
        if not is_valid_event_id(event_id):
            return

        listeners = EventWatcher._listeners.get(event_id)

        if listeners:
            listeners.remove(listener)

            if len(listeners) == 0:
                EventWatcher._listeners.pop(event_id)
