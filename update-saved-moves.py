#!/usr/bin/env python3
import sys
import struct
import argparse

from typing import BinaryIO

# Program offset does not start 0, so adjust it's offset to the actual offset
# in the file.
GHIDRA_OFFSET = 0x180000c00

MAX_SAVED_MOVES_OFFSET = 0x180342f61+3
MAX_FREE_MOVES_OFFSET = 0x180342f68+3

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-saved-moves", "-s", type=int, default=96)
    parser.add_argument("--max-free-moves", "-f", type=int, default=96)
    parser.add_argument("file", help="path to UE4-Engine-Win64-Shipping.dll")
    args = parser.parse_args()

    with open(args.file, "r+b") as f:
        try:
            verify(f)
        except:
            print("Doesn't look like a UE4-Engine-Win64-Shipping.dll to me!")
            sys.exit(1)

        patch_max_saved_moves(f, args.max_saved_moves)
        patch_max_free_moves(f, args.max_free_moves)


def adjust_offset(offset: int):
    return offset - GHIDRA_OFFSET


def verify(f: BinaryIO):
    """Verify file is the correct file we want to patch."""
    f.seek(adjust_offset(0x180342f5d))
    data = f.read(4)
    assert data == b"\x4c\x89\x7f\x48"


def patch_int32(f, offset, value: int):
    f.seek(adjust_offset(offset))
    f.write(struct.pack("i", value))


def patch_max_saved_moves(f, value: int):
    """
    Original
    --------------------------------------------
    180342f61 c7 47 50       MOV        dword ptr [RDI + 0x50],0x60
              60 00 00 00

    Patch
    --------------------------------------------
    180342f61 c7 47 50       MOV        dword ptr [RDI + 0x50],<value>
              <value as int32>
    """
    patch_int32(f, MAX_SAVED_MOVES_OFFSET, value)
    print(f"Patched max saved moves to {value}")


def patch_max_free_moves(f, value: int):
    """
    Original
    --------------------------------------------
    180342f68 c7 47 54        MOV        dword ptr [RDI + 0x54],0x60
              60 00 00 00

    Patch
    --------------------------------------------
    180342f68 c7 47 54        MOV        dword ptr [RDI + 0x54],<value>
              <value as int32>
    """
    patch_int32(f, MAX_FREE_MOVES_OFFSET, value)
    print(f"Patched max free moves to {value}")


if __name__ == "__main__":
    main()
