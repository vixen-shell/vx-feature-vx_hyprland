import subprocess, json


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
    def version():
        return hypr_info("version")

    @staticmethod
    def monitors():
        return hypr_info("monitors")

    @staticmethod
    def workspaces():
        return hypr_info("workspaces")

    @staticmethod
    def activeworkspace():
        return hypr_info("activeworkspace")

    @staticmethod
    def workspacerules():
        return hypr_info("workspacerules")

    @staticmethod
    def clients():
        return hypr_info("clients")

    @staticmethod
    def devices():
        return hypr_info("devices")

    @staticmethod
    def binds():
        return hypr_info("binds")

    @staticmethod
    def activewindow():
        return hypr_info("activewindow")

    @staticmethod
    def layers():
        return hypr_info("layers")

    @staticmethod
    def splash():
        return hypr_info("splash")

    @staticmethod
    def cursorpos():
        return hypr_info("cursorpos")

    @staticmethod
    def animations():
        return hypr_info("animations")

    @staticmethod
    def instances():
        return hypr_info("instances")

    @staticmethod
    def layouts():
        return hypr_info("layouts")

    @staticmethod
    def rollinglog():
        return hypr_info("rollinglog")
