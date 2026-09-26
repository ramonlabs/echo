import logging

import colorlog

LOG_FMT = "%(log_color)s%(asctime)s %(levelname)s%(reset)s %(source)s%(message)s"
TIME_FMT = "%H:%M:%S"
COLOR_FMT = {
    "DEBUG": "cyan",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "bold_red",
}


class _Formatter(colorlog.ColoredFormatter):
    # the root logger has no useful name so only named ones get a prefix
    def format(self, record):
        record.source = "" if record.name == "root" else f"[{record.name}] "
        return super().format(record)


def configure(debug=False):
    level = logging.DEBUG if debug else logging.INFO
    handler = colorlog.StreamHandler()
    handler.setFormatter(
        _Formatter(LOG_FMT, TIME_FMT, log_colors=COLOR_FMT),
    )
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)


logger = logging.getLogger()
