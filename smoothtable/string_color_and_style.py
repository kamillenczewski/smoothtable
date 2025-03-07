from .constants import EMPTY


COLORS =  {
    "black": '\033[30m',
    "red": '\033[31m',
    "green": '\033[32m',
    "orange": '\033[33m',
    "blue": '\033[34m',
    "purple": '\033[35m',
    "cyan": '\033[36m',
    "lightgrey": '\033[37m',
    "darkgrey": '\033[90m',
    "lightred": '\033[91m',
    "lightgreen": '\033[92m',
    "yellow": '\033[93m',
    "lightblue": '\033[94m',
    "pink": '\033[95m',
    "lightcyan": '\033[96m'
}

TEXT_STYLES = {
    "bold": '\033[01m',
    "underline": '\033[04m',
    "reverse": '\033[07m',
    "strikethrough": '\033[09m',
    "invisible": '\033[08m'
}

RESET_STR_FORMAT_TAG = '\033[0m'


def getColor(tag):
    return COLORS[tag] if tag in COLORS else EMPTY

def getStyle(tag):
    return TEXT_STYLES[tag] if tag in TEXT_STYLES else EMPTY