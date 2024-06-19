import subprocess, json
from . import content


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


@content.add_handler("data")
def version():
    return hypr_info("version")


@content.add_handler("data")
def monitors():
    return hypr_info("monitors")


@content.add_handler("data")
def workspaces():
    return hypr_info("workspaces")


@content.add_handler("data")
def activeworkspace():
    return hypr_info("activeworkspace")


@content.add_handler("data")
def workspacerules():
    return hypr_info("workspacerules")


@content.add_handler("data")
def clients():
    return hypr_info("clients")


@content.add_handler("data")
def devices():
    return hypr_info("devices")


@content.add_handler("data")
def binds():
    return hypr_info("binds")


@content.add_handler("data")
def activewindow():
    return hypr_info("activewindow")


@content.add_handler("data")
def layers():
    return hypr_info("layers")


@content.add_handler("data")
def splash():
    return hypr_info("splash")


@content.add_handler("data")
def cursorpos():
    return hypr_info("cursorpos")


@content.add_handler("data")
def animations():
    return hypr_info("animations")


@content.add_handler("data")
def instances():
    return hypr_info("instances")


@content.add_handler("data")
def layouts():
    return hypr_info("layouts")


@content.add_handler("data")
def rollinglog():
    return hypr_info("rollinglog")
