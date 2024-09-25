#!/usr/bin/env python3
import sys
import argparse

from typing import BinaryIO


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="path to libUE4Server-UnrealTournament-Linux-Shipping.so")
    args = parser.parse_args()

    with open(args.file, "r+b") as f:
        try:
            verify(f)
        except:
            print("Doesn't look like a libUE4Server-UnrealTournament-Linux-Shipping.so to me!")
            sys.exit(1)

        patch_tick_rate(f)


def verify(f: BinaryIO):
    """Verify file is the correct file we want to patch."""
    f.seek(0x90fc14)
    data = f.read(5)
    assert data == b"\xe8\x47\xe9\xd0\xff"


def patch_tick_rate(f):
    """
    Original
    --------------------------------------------
    00d07877 83 f8 79        CMP        EAX,0x79
    00d0787a b9 78 00        MOV        ECX,0x78
             00 00
    00d0787f 0f 4c c8        CMOVL      ECX,EAX
    
    Patch
    --------------------------------------------
    00d07877 89 c1           MOV        ECX,EAX
    00d07879 90              NOP
    00d0787a 90              NOP
    ...
    00d07881 90              NOP
    """

    f.seek(0xd07877)

    # Move the tick rate from the configuration file to the return value
    f.write(b"\x89\xc1")  # MOV ECX, EAX

    # NOP sled to remove the upper-bound checks
    f.write(b"\x90" * 9)

    print("Patched tick rate")


if __name__ == "__main__":
    main()
