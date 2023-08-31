#!/usr/bin/env python3
"""Example to get keyboard presses without blocking a main running thread."""

import concurrent.futures
import time
from inputs import get_key

oi=0

def read_keyboard():
    global oi 
    while True:
        for event in get_key():
            if event.state == 1:
                print("key pressed")
                oi = oi + 1


def run():
    global oi
    while True:
        print("running...", oi)
        time.sleep(1)


def main():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(read_keyboard)
        executor.submit(run)


if __name__ == "__main__":
    main()


