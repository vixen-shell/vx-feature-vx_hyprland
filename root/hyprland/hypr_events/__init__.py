from .HyprEventsListener import HyprEventsListener


class lifespan:
    from .. import content

    @staticmethod
    @content.on_startup
    def on_startup():
        HyprEventsListener.start()

    @staticmethod
    @content.on_shutdown
    def on_shutdown():
        HyprEventsListener.stop()
