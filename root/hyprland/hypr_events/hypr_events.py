from typing import List

event_data_map = {
    "workspace": ["workspace_name"],
    "workspacev2": ["workspace_id", "workspace_name"],
    "focusedmon": ["monitor_name", "workspace_name"],
    "activewindow": ["window_class", "window_title"],
    "activewindowv2": ["window_address"],
    "fullscreen": ["value"],
    "monitorremoved": ["monitor_name"],
    "monitoradded": ["monitor_name"],
    "monitoraddedv2": ["monitor_id", "monitor_name", "monitor_description"],
    "createworkspace": ["workspace_name"],
    "createworkspacev2": ["workspace_id", "workspace_name"],
    "destroyworkspace": ["workspace_name"],
    "destroyworkspacev2": ["workspace_id", "workspace_name"],
    "moveworkspace": ["workspace_name", "monitor_name"],
    "moveworkspacev2": ["workspace_id", "workspace_name", "monitor_name"],
    "renameworkspace": ["workspace_id", "new_name"],
    "activespecial": ["workspace_name", "monitor_name"],
    "activelayout": ["keyboard_name", "layout_name"],
    "openwindow": ["window_address", "workspace_name", "window_class", "window_title"],
    "closewindow": ["window_address"],
    "movewindow": ["window_address", "workspace_name"],
    "movewindowv2": ["window_address", "workspace_id", "workspace_name"],
    "openlayer": ["namespace"],
    "closelayer": ["namespace"],
    "submap": ["submap_name"],
    "changefloatingmode": ["window_address", "floating"],
    "urgent": ["window_address"],
    "minimize": ["window_address", "minimized"],
    "screencast": ["state", "owner"],
    "windowtitle": ["window_address"],
    "ignoregrouplock": ["value"],
    "lockgroups": ["value"],
    "configreloaded": [],
    "pin": ["window_address", "pin_state"],
}


class EventData:
    def __init__(self, data_bytes: bytes) -> None:
        self._process_raw_data(data_bytes)

    def _process_raw_data(self, data_bytes: bytes):
        def list_to_dict(event_id: str, data_list: List[str] = None) -> dict:
            data_dict = {}

            if data_list and event_id in event_data_map:
                event_data_names = event_data_map.get(self._id)

                for index, data_name in enumerate(event_data_names):
                    data_dict[data_name] = {"0": False, "1": True}.get(
                        data_list[index], data_list[index]
                    )

            return data_dict

        raw_data = data_bytes.decode("utf-8").rstrip("\n").split(">>")

        self._id = raw_data[0]
        self._data = list_to_dict(
            event_id=raw_data[0],
            data_list=raw_data[1].split(",") if len(raw_data) > 1 else None,
        )

    @property
    def to_json(self):
        return {"id": self._id, "data": self._data}
