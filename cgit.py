#!/bin/python3
import requests
import socket
import time
from enum import Enum
from halo import Halo


class State(Enum):

    GIT_ACTIVE = 1
    GIT_DEAD = 2

    SOCK_ALIVE = 3
    SOCK_DEAD = 4

    SPINNER_ALIVE = 5
    SPINNER_DEAD = 6
    SPINNER_STOP = 7


def main(host="172.17.195.139", port=22):

    spinnerState = State.SPINNER_DEAD
    gitState = State.GIT_DEAD
    SOCK_STATE = State.SOCK_DEAD

    while SOCK_STATE == State.SOCK_DEAD:
        try:
            socket.setdefaulttimeout(3)
            _sock = socket.socket(socket.AF_INET,
                                 socket.SOCK_STREAM)
            _sock_result = _sock.connect_ex((host,port))

            if _sock_result == 0:
                SOCK_STATE = State.SOCK_ALIVE
                print("\nServer online, moving on")
                break
            elif _sock_result == 1:
                SOCK_STATE = State.SOCK_DEAD

        except:
            socket.close()
            SOCK_STATE = State.SOCK_DEAD
            continue
        time.sleep(.5)

    while gitState == State.GIT_DEAD:
        try:
            _req = requests.get(f"http://{host}")

            if _req.status_code == 502:
                spinnerState = State.SPINNER_ALIVE
                continue

            elif req.status_code == 200:
                spinnerState = State.SPINNER_STOP
                gitState = State.GIT_ACTIVE
                print("\nGit online now!")
                exit(0)
            time.sleep(.5)
        except:
            continue

def isSpinning(spinnerState):
    _spinner = Halo(text='Waiting for Git to come online', spinner='dots')
    if spinnerState == State.SPINNER_DEAD:
        _spinner.start()
    while spinnerState == State.SPINNER_ALIVE:
        if spinnerState == State.SPINNER_STOP:
            _spinner.stop()
        continue
        time.sleep(.5)


if __name__ == "__main__":
    isSpinning(State.SPINNER_DEAD)
    main()
