# DDS
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-0-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
An api that returns double-dummy results for a given board.

Uses Bo Hagland's solver https://github.com/dds-bridge/dds -- requires the libdds.so (or dds.dll in windows) to be installed and accessible.
Credit to Alexis Rimbaud of NukkAI for the python dds wrapper.


# Build and install libdds library for local testing

```
make libdds-build
cd libdds/.build
```

The python loader looks for the library from libdds/.build/src. If the file is
found from build directory then the found library is preferred before a library
in a system directory.

# Install a local server using Flask, then test it manually:

```
pip3 install Flask
pip install flask-restful
pip install flask_cors
cd DDS
python3 -m src.api
# In a separate terminal window…
make curl_local
```

# Install Docker for MacOS

https://medium.com/@yutafujii_59175/a-complete-one-by-one-guide-to-install-docker-on-your-mac-os-using-homebrew-e818eb4cfc3

### Build & Deploy DDS api ###

Prerequirements:
0. Download code
1. Docker
2. kubectl
3. helm (version 3)
4. gcloud

Configure gcloud auth:

5. Run `gcloud auth login <your.email@whatever.com>`

6. Run `gcloud auth application-default login`


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
