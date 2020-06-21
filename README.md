# DDS
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-0-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
An api that returns double-dummy results for a given board.

Uses Bo Hagland's solver https://github.com/dds-bridge/dds -- requires the libdds.so (or dds.dll in windows) to be installed and accessible.
Credit to Alexis Rimbaud of NukkAI for the python dds wrapper.


# Build and install libdds.so under MacOS #

```
git clone https://github.com/dds-bridge/dds.git
cd dds/src
make -f Makefiles/Makefile_Mac_clang_shared THREADING=
ln libdds.so /usr/local/lib
```

# Install a local server using Flask, then test it manually:

```
pip3 install Flask
pip install flask-restful
pip install flask_cors
cd src
python api.py
# In a separate terminal window…
curl --header "Content-Type: application/json"   --request POST   --data '{"hands":{"S":["D3", "C6", "DT", "D8", "DJ", "D6", "CA", "C3", "S2", "C2", "C4", "S9", "S7"],"W":["DA", "S4", "HT", "C5", "D4", "D7", "S6", "S3", "DK", "CT", "D2", "SK","H8"],"N":["C7", "H6", "H7", "H9", "CJ", "SA", "S8", "SQ", "D5", "S5", "HK", "C8", "HA"],"E":["H2", "H5", "CQ", "D9", "H4", "ST", "HQ", "SJ", "HJ", "DQ", "H3", "C9", "CK"]}}'   http://localhost:5000/api/dds-table/
```

# Install Docker for MacOS

https://medium.com/@yutafujii_59175/a-complete-one-by-one-guide-to-install-docker-on-your-mac-os-using-homebrew-e818eb4cfc3

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

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!