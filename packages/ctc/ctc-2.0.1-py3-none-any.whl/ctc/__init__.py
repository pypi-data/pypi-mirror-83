"""
ctc modual

Author: Minecraft_XiaoYu
Discord: Minecraft_XiaoYu#5322
"""

from ctypes import windll

__all__ = ["BLACK", "DARKBLUE", "DARKGREEN", "DARKSKYBLUE", "DARKRED", "DARKPINK", "DARKYELLOW", "DARKWHITE", "DARKGRAY", "BLUE", "GREEN", "SKYBLUE", "RED", "PINK", "YELLOW", "WHITE", "setColor"]
__version__ = "2.1.0"

BLACK = object()
DARKBLUE = object()
DARKGREEN = object()
DARKSKYBLUE = object()
DARKRED = object()
DARKPINK = object()
DARKYELLOW = object()
DARKWHITE = object()
DARKGRAY = object()
BLUE = object()
GREEN = object()
SKYBLUE = object()
RED = object()
PINK = object()
YELLOW = object()
WHITE = object()

TEXT = {
    BLACK: 0x00,
    DARKBLUE: 0x01,
    DARKGREEN: 0x02,
    DARKSKYBLUE: 0x03,
    DARKRED: 0x04,
    DARKPINK: 0x05,
    DARKYELLOW: 0x06,
    DARKWHITE: 0x07,
    DARKGRAY: 0x08,
    BLUE: 0x09,
    GREEN: 0x0a,
    SKYBLUE: 0x0b,
    RED: 0x0c,
    PINK: 0x0d,
    YELLOW: 0x0e,
    WHITE: 0x0f,
}

BACKGROUND = {
    BLACK: 0x00,
    DARKBLUE: 0x10,
    DARKGREEN: 0x20,
    DARKSKYBLUE: 0x30,
    DARKRED: 0x40,
    DARKPINK: 0x50,
    DARKYELLOW: 0x60,
    DARKWHITE: 0x70,
    DARKGRAY: 0x80,
    BLUE: 0x90,
    GREEN: 0xa0,
    SKYBLUE: 0xb0,
    RED: 0xc0,
    PINK: 0xd0,
    YELLOW: 0xe0,
    WHITE: 0xf0,
}

out = windll.kernel32.GetStdHandle(-11)

def set_color(text: object = WHITE, background: object = BLACK) -> None:
    code = TEXT[text] | BACKGROUND[background]
    windll.kernel32.SetConsoleTextAttribute(out, code)
    return

class Font(object):
    def __init__(self, text: object = WHITE, background: object = BLACK) -> None:
        self.text = TEXT[text]
        self.background = BACKGROUND[background]
        return
    def set_text_color(self, color: object = WHITE) -> None:
        self.text = TEXT[color]
        return
    def set_text_background(self, color: object = BLACK) -> None:
        self.background = BACKGROUND[color]
        return
    def set_console_text_font(self) -> None:
        set_color(self.text, self.background)