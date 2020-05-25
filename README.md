# DDS
An api which returns DDS results for a given board.

Uses the Bo Hagland solver https://github.com/dds-bridge/dds -- requires the libdds.so (or dds.dll in windows) to be installed and accessible.
Credit to Alexis Rimbaud of NukkAI for the python dds wrapper.

To build and install libdds.so under MacOS:

git clone https://github.com/dds-bridge/dds.git
cd dds/src
make -f Makefiles/Makefile_Mac_clang_shared THREADING=
ln libdds.so /usr/local/lib

### Build & Deploy DDS api ###

Prerequirements:
1. Docker
2. kubectl
3. helm (version 3)

Build the application stack using:
```
$ make build
```

Push to the remote registry:
```
$ make push
```

Or combined build+push using the:
```
$ make release
```

Deploy it on the server:
```
$ make deploy
```
