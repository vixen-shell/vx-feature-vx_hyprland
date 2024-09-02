from vx_root import root_feature
from .events import HyprEvents
from .infos import HyprInfos

root_feature().init(
    {
        "autostart": True,
        "frames": "disable",
        "state": "disable",
    }
)
