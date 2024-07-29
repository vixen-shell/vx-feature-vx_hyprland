import subprocess, json
from .. import content


def hypr_info(info_id: str):
    result = subprocess.run(
        f"hyprctl {info_id} -j", shell=True, capture_output=True, text=True
    )

    if result.returncode != 0:
        raise Exception(result.stderr)

    try:
        return json.loads(result.stdout)
    except:
        return result.stdout


class HyprInfos:
    @staticmethod
    @content.add_handler("data")
    def version():
        return hypr_info("version")

    @staticmethod
    @content.add_handler("data")
    def monitors():
        return hypr_info("monitors")

    @staticmethod
    @content.add_handler("data")
    def workspaces():
        return hypr_info("workspaces")

    @staticmethod
    @content.add_handler("data")
    def activeworkspace():
        return hypr_info("activeworkspace")

    @staticmethod
    @content.add_handler("data")
    def workspacerules():
        return hypr_info("workspacerules")

    @staticmethod
    @content.add_handler("data")
    def clients():
        return hypr_info("clients")

    @staticmethod
    @content.add_handler("data")
    def devices():
        return hypr_info("devices")

    @staticmethod
    @content.add_handler("data")
    def binds():
        return hypr_info("binds")

    @staticmethod
    @content.add_handler("data")
    def activewindow():
        return hypr_info("activewindow")

    @staticmethod
    @content.add_handler("data")
    def layers():
        return hypr_info("layers")

    @staticmethod
    @content.add_handler("data")
    def splash():
        return hypr_info("splash")

    @staticmethod
    @content.add_handler("data")
    def cursorpos():
        return hypr_info("cursorpos")

    @staticmethod
    @content.add_handler("data")
    def animations():
        return hypr_info("animations")

    @staticmethod
    @content.add_handler("data")
    def instances():
        return hypr_info("instances")

    @staticmethod
    @content.add_handler("data")
    def layouts():
        return hypr_info("layouts")

    @staticmethod
    @content.add_handler("data")
    def rollinglog():
        return hypr_info("rollinglog")
