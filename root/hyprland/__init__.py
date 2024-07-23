from vx_feature_utils import Utils

utils = Utils.define_feature_utils()
content = Utils.define_feature_content(
    {"autostart": True, "frames": "disable", "state": "disable"}
)

from .hypr_events import HyprEventsListener


from .events_socket import *
from .hypr_infos import *
