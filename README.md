# DDS
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-0-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
An api that returns double-dummy results for a given deal.

## deploy on AWS as a Lambda
[deploy-aws](deploy-aws/README.md)

## deploy on GCP as a KS8 Container

## Usage
```
curl --header "Content-Type: application/json" --request POST --data '{"hands":{"S":["D3", "C6", "DT", "D8", "DJ", "D6", "CA", "C3", "S2", "C2", "C4", "S9", "S7"],"W":["DA", "S4", "HT", "C5", "D4", "D7", "S6", "S3", "DK", "CT", "D2", "SK","H8"],"N":["C7", "H6", "H7", "H9", "CJ", "SA", "S8", "SQ", "D5", "S5", "HK", "C8", "HA"],"E":["H2", "H5", "CQ", "D9", "H4", "ST", "HQ", "SJ", "HJ", "DQ", "H3", "C9", "CK"]}}' https://dds.prod.globalbridge.app/api/dds-table/
```
or equivalently
```
make curl_prod
```
Uses Bo Hagland's solver https://github.com/dds-bridge/dds -- requires libdds.so (dds.dll on MS-Windows, libdds.2.dylib on MacOS.) The *make* targets `build` and `start_local_server` will build this library for you. 

Our thanks to Alexis Rimbaud of NukkAI for the Python dds wrapper.

## Install a local server using Flask, then test it manually:

```
pip3 install -r requirements.txt

make start_local_server

make curl_local
```

If you want to change the C++ library's build configuration,
[README.libdds.md](README.libdds.md) provides information about the process.

### Configuration ###

The server supports optional configuration using a `server.yaml` file. The file is
read from the current working directory. The repository includes `example_server.yaml`.

## Install Docker for MacOS

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
