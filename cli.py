"""
    Functions to interact with user from cli.
"""

import sys
import os
import keyboard as kb


def select(options, get_key=False):
    """
    Prints options to select from and returns value
    """

    act = 0
    active_index = 0
    options_size = len(options)

    def incr_current():
        """ Increments current active index cycling"""
        nonlocal active_index
        nonlocal options_size

        active_index += 1

        if active_index == options_size:
            active_index = 0

    def decr_current():
        """ Decrements current active index cycling"""
        nonlocal active_index
        nonlocal options_size

        active_index -= 1

        if active_index == -1:
            active_index = (options_size - 1)

    print("Select from given options: ")

    def print_options():
        nonlocal options
        nonlocal active_index

        enum = None
        if not isinstance(options, (dict)):
            enum = enumerate(options)

        for key, option in enum:
            active_mark = ''
            if key == active_index:
                active_mark = '<-'
            # print(f"{key}. {option} {active_mark}\x0A")
            sys.stdout.write(f"{key}. {option} {active_mark}\x0A")
        sys.stdout.flush()

    def clear_screen():
        for option in options:
            # sys.stdout.write(f"\x1b\x5b\x41\x0d\x1b\x5b\x4b")
            sys.stdout.write(f"{kb.KB_UP}{kb.KB_CR}{kb.KB_NIX_CLEAR_TO_END}")

    while act != 10:
        # os.system('clear')
        clear_screen()
        print_options()
        act = ord(kb.wait_key())
        # print(str(hex(act)))
        # print(str(hex(kb.KB_UP[2])))
        if act == 27 and ord(sys.stdin.read(1)) == 91:
            scancode = ord(sys.stdin.read(1))
            if scancode == 65:  # key up
                decr_current()
            if scancode == 66:  # key down
                incr_current()
            if scancode == 67: # key right
                pass
            if scancode == 68: # key left
                pass

    if get_key is True:
        return active_index
    else:
        return options[active_index]


def confirm(prompt):
    """
    Prompts yes-no confirmation
    """
    sys.stdout.write(f"{prompt}[y/n]")
    sys.stdout.flush()
    answer = None
    while answer not in ['y', 'n']:
        answer = kb.wait_key().lower()
    sys.stdout.write(f" - {answer}\x0A")
    sys.stdout.flush()
    return answer == 'y'


def prompt(prompt):
    """
    Prompts yes-no confirmation
    """
    sys.stdout.write(f"{prompt}: ")
    sys.stdout.flush()
    answer = sys.stdin.readline()[:-1]
    sys.stdout.write(f" - {answer}\x0A")
    sys.stdout.flush()
    return answer