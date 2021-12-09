"""
    Provides functions to work with keyboard on low-level
"""
import sys

KB_UP = "\x1b\x5b\x41"
KB_DOWN = "\x1b\x5b\x42"
KB_RIGHT = "\x1b\x5b\x43"
KB_LEFT = "\x1b\x5b\x44"
KB_CR = "\x0d"
KB_NIX_CLEAR_TO_END = "\x1b\x5b\x4b"


def wait_key():
    ''' Wait for a key press on the console and return it. '''
    result = None
    import termios
    fd = sys.stdin.fileno()

    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    try:
        result = sys.stdin.read(1)
    except IOError:
        pass
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)

    return result
