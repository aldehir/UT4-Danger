# UT4-Danger

Binary patches to the UT4 Linux Server.

**Backup your original binaries before applying patch.***

## Remove tickrate limit

```console
$ python3 remove-tickrate-limit.py /path/to/libUE4Server-UnrealTournament-Linux-Shipping.so
```


## Adjust max saved moves / max free moves

```console
$ python3 update-saved-moves.py --max-saved-moves 200 --max-free-moves 200 /path/to/UE4-Engine-Win64-Shipping.dll
```
