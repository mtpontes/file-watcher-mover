from enum import Enum


class Constants(Enum):
    TEMPORARY_FILE_EXTENSIONS = (
        # Browsers
        ".tmp",
        ".crdownload",
        ".part",
        ".download",
        ".partial",
        ".opdownload",
        ".brdownload",
        ".safaridownload",
        # Torrent clients
        ".!qB",
        ".!ut",
        ".!bt",
        ".!qd",
        ".td",
        ".aria2",
        # Downlaod managers
        ".bc!",
        ".dlpart",
        ".dctmp",
        ".gettmp",
        ".fdmtmp",
        ".fdmdownload",
        ".idm",
        ".dap",
        ".jc!",
        ".fget",
    )
