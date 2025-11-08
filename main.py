#!/usr/bin/env python3
"""Animated console banner: "Zoe is amazing" with colors and flashing.

Usage: python main.py [--count N] [--interval S] [--flash]
"""
from __future__ import annotations

import argparse
import os
import signal
import sys
import time
from typing import List

try:
    from pyfiglet import Figlet
except Exception:  # pragma: no cover - handled later with clear message
    Figlet = None  # type: ignore

try:
    from colorama import init as colorama_init
    from colorama import Fore, Style
except Exception:  # pragma: no cover
    Fore = Style = None  # type: ignore
    colorama_init = None  # type: ignore


def clear_screen() -> None:
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")


def make_colors() -> List[str]:
    # keep a sequence of vibrant colors
    return [
        Fore.RED,
        Fore.GREEN,
        Fore.YELLOW,
        Fore.BLUE,
        Fore.MAGENTA,
        Fore.CYAN,
        Fore.WHITE,
    ]


def signal_handler(sig, frame):
    # move cursor to next line and exit cleanly
    print(Style.RESET_ALL)
    sys.exit(0)


def main() -> None:
    parser = argparse.ArgumentParser(description="Animated colored console banner")
    parser.add_argument("--count", type=int, default=40, help="Number of animation frames (default: 40)")
    parser.add_argument("--interval", type=float, default=0.12, help="Seconds between frames")
    parser.add_argument("--flash", action="store_true", help="Use ANSI blink effect (if supported)")
    parser.add_argument("--font", type=str, default="standard", help="pyfiglet font to use")
    parser.add_argument("--exclaim", type=int, default=3, help="Number of exclamation marks to append (default: 3)")
    args = parser.parse_args()

    # graceful Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    if Figlet is None or colorama_init is None:
        print("Missing dependencies. Please run: python -m pip install -r requirements.txt")
        sys.exit(1)

    colorama_init()
    fig = Figlet(font=args.font)

    colors = make_colors()
    blink = "\x1b[5m" if args.flash else ""
    reset = Style.RESET_ALL

    text = "Zoe is amazing" + "!" * args.exclaim

    for i in range(args.count):
        clear_screen()
        color = colors[i % len(colors)]
        rendered = fig.renderText(text)

        # Compose the line with optional blink and a bright style
        out = f"{blink}{Style.BRIGHT}{color}{rendered}{reset}"

        # Print centered-ish: try to pad left based on terminal width if available
        try:
            cols = os.get_terminal_size().columns
            first_line = rendered.splitlines()[0] if rendered.splitlines() else ""
            pad = max((cols - len(first_line)) // 2, 0)
        except Exception:
            pad = 0

        if pad:
            # print each line with left padding
            for line in rendered.splitlines():
                print(" " * pad + f"{blink}{Style.BRIGHT}{color}{line}{reset}")
        else:
            print(out)

        # small heartbeat to produce a flashing/strobing effect
        time.sleep(args.interval)

    # final reset
    print(Style.RESET_ALL)


if __name__ == "__main__":
    main()
