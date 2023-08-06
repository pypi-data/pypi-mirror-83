"""
ctc modual

Author: Minecraft_XiaoYu
Discord: Minecraft_XiaoYu#5322
"""

from ctypes import windll

__all__ = ["BLACK", "DARKBLUE", "DARKGREEN", "DARKSKYBLUE", "DARKRED", "DARKPINK", "DARKYELLOW", "DARKWHITE", "DARKGRAY", "BLUE", "GREEN", "SKYBLUE", "RED", "PINK", "YELLOW", "WHITE", "setColor"]
__version__ = "2.0.0"

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

def setcolor(text = WHITE, background = BLACK):
    code = TEXT[text] | BACKGROUND[background]
    windll.kernel32.SetConsoleTextAttribute(out, code)
    return
