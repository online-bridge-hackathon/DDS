# DDS
An api which returns DDS results for a given board.

Uses the Bo Hagland solver https://github.com/dds-bridge/dds -- requires the libdds.so (or dds.dll in windows) to be installed and accessible.

### Build & Deploy ###

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
