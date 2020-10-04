#!/bin/python3
import sys
import requests
import socket
import time
import argparse
import ipaddress
from uwupy.networking import pyuwuICMPTimeout
from uwupy.generics import Oopsie
from enum import Enum
from halo import Halo


parser = argparse.ArgumentParser()
parser.add_argument("--host", help='ip-address', type=str)
args = parser.parse_args()
host = args.host

#   TODO: Add peristance to Halo Plugin 

SPINNER_PERIST_DATA_FAIL = ''
SPINNER_PERIST_DATA_WARNING = ''
SPINNER_PERIST_DATA_SUCCEED = ''
SPINNER_PERIST_DATA_SUCCEED_SOCK = ''
SPINNER_PERIST_DATA_FAIL_SOCK = ''


class State(Enum):

    GIT_ACTIVE = 1
    GIT_DEAD = 2

    SOCK_ALIVE = 3
    SOCK_DEAD = 4

    SPINNER_ALIVE = 5
    SPINNER_DEAD = 6
    SPINNER_STOP = 7
    SPINNER_WARNING = 8
    SPINNER_FAIL = 9
    SPINNER_SUCCEED = 10
    SPINNER_FAIL_SOCK = 11
    SPINNER_SUCCEED_SOCK = 12


def main(host):
    try:
        ipaddress.ip_address(host)
    except ValueError:
        spinnerState = State.SPINNER_WARNING
        SPINNER_PERIST_DATA_WARNING = f'{host} is not a valid ip address'
#        print("\nfail ip warn")

    count = 0
    spinnerState = State.SPINNER_DEAD
    gitState = State.GIT_DEAD
    SOCK_STATE = State.SOCK_DEAD

    try:
        while SOCK_STATE == State.SOCK_DEAD:
            try:
                count += 1
                socket.setdefaulttimeout(3)
                _sock = socket.socket(socket.AF_INET,
                                      socket.IPPROTO_ICMP)
                _sock_result = _sock.connect_ex((host,22))

                if _sock_result == 0:
                    time.sleep(5)
                    spinnerState_inside = State.SPINNER_SUCCEED_SOCK
                    SOCK_STATE = State.SOCK_ALIVE
                    SPINNER_PERIST_DATA_SUCCEED_SOCK = 'Success! Server is alive.'
                    break
                elif _sock_result == 1:
                    SOCK_STATE = State.SOCK_DEAD
                elif count == 1000:
                    spinnerState_inside = State.SPINNER_FAIL
                    SPINNER_PERIST_DATA_FAIL_SOCK = 'Sock Timeout exceeded'
                    exit(1)

            except:
                #socket.shutdown()
                #socket.close()
                SOCK_STATE = State.SOCK_DEAD
                continue
            time.sleep(.5)

    except KeyboardInterrupt:
        pass

    try:
        while gitState == State.GIT_DEAD:
            try:
                _req = requests.get(f"http://{host}")

                if _req.status_code == 502:
                    spinnerState = State.SPINNER_ALIVE
                    continue

                elif req.status_code == 200:
                    spinnerState = State.SPINNER_SUCCEED
                    gitState = State.GIT_ACTIVE
                    SPINNER_PERIST_DATA_SUCCEED = 'Success! Git Service is alive.'
                    exit(0)
                time.sleep(.5)
            except:
                continue

    except KeyboardInterrupt:
        pass

def isSpinning(spinnerState):
    spinnerState_inside = None
    _spinner = Halo(text='Waiting for Git to come online', spinner='dots')
    if spinnerState == State.SPINNER_DEAD:
        _spinner.start()
    while spinnerState == State.SPINNER_ALIVE:
        if spinnerState_inside == State.SPINNER_STOP:
            _spinner.stop()
        if spinnerState_inside == State.SPINNER_SUCCEED:
           _spinner.succeed(text=SPINNER_PERIST_DATA_SUCCEED)
        if spinnerState_inside == State.SPINNER_WARNING:
            _spinner.warn(text=SPINNER_PERIST_DATA_WARNING)
        if spinnerState_inside == State.SPINNER_FAIL:
            _spinner.fail(text=SPINNER_PERIST_DATA_FAIL)
            exit(1)
        if spinnerState_inside == State.SPINNER_SUCCEED_SOCK:
            _spinner.succeed(text='is this getting here')
        if spinnerState_inside == State.SPINNER_FAIL_SOCK:
            _spinner.fail(text=SPINNER_PERIST_DATA_FAIL_SOCK)
            exit(1)
        continue
        time.sleep(.5)


if __name__ == "__main__":
    isSpinning(State.SPINNER_DEAD)
    main(host)
