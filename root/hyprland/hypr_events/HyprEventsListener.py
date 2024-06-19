import os, asyncio
from fastapi import WebSocket
from typing import List
from .hypr_events import EventData
from .. import utils, content

HYPR_SOCKET_PATH = "{}/hypr/{}/.socket2.sock".format(
    os.getenv("XDG_RUNTIME_DIR"), os.getenv("HYPRLAND_INSTANCE_SIGNATURE")
)


class HyprEventsListener:
    _task: asyncio.Task = None
    _websockets: List[WebSocket] = []

    @staticmethod
    def check_hypr_socket():
        return os.path.exists(HYPR_SOCKET_PATH)

    @staticmethod
    async def listener_task():
        reader, _ = await asyncio.open_unix_connection(HYPR_SOCKET_PATH)

        while True:
            data = EventData(await reader.readline())

            for websocket in HyprEventsListener._websockets:
                await websocket.send_json(data.to_json)

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

    @staticmethod
    def attach_websocket(websocket: WebSocket):
        HyprEventsListener._websockets.append(websocket)

    @staticmethod
    def detach_websocket(websocket: WebSocket):
        HyprEventsListener._websockets.remove(websocket)
