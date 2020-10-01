# Deploying DDS (API) on AWS as a Lambda function

## Overview
If libdds.so needs updating then it needs to be compiled on Amazon Linux, via a docker image, which requires a build environment with the expected cmake version set by libdds.  The instructions below walk through the steps needed 

## Environment
The lambda function runs on the Amazon Linux hosts and the library libdds.so must be built with the same interpreter

The following commands are for Linux-like systems (tested on Ubuntu 20.04)

### Clone libbds
```git clone https://github.com/online-bridge-hackathon/libdds.git $(pwd)/libdds```

### Prep build environment for Amazon Linux
cmake version 3.12 or higher is required for building libdds
```head $(pwd)/libdds/CMakeLists.txt```

Download the cmake package from https://cmake.org/files/v3.12/
```wget -qO- https://cmake.org/files/v3.12/cmake-3.12.4.tar.gz | tar zxvf - -C libdds/```

### Run Amazon Linux locally to build libdss.so
Load docker image with $(pwd)/libdds mounted.  You'll get a bash prompt
```docker run -v $(pwd)/libdds/:/tmp/libdds -it amazonlinux```

Install native dev environment
```yum install gcc-c++ make```

Navigate to the cmake folder previously downloaded
```cd /tmp/libdds/cmake-3.12.4```

Compile cmake
```./bootstrap
gmake
cd ..
```

Run cmake 
```./cmake-3.12.4/bin/cmake .```

Run make to compile libdds
```make```

Exit the container
```exit```

Copy over the libdds.so files to, an ideally empty folder
```rsync -a libdds/src/libdds.so* deploy-aws/libdds/```

### Prep python environment
Create a virtual environment
```
cd deploy-aws
virtualenv venv
source ./venv/bin/activate
```

Install modules including zappa
```pip3 install -r requirements.txt```

Initialize zappa and configure auth to AWS
TODO

Deploy to AWS
```zappa update dev```     (if not yet deployed zappa deploy dev)

To re(certify) the ACM SSL cert created
```zappa certify```

Watching the logs
```zappa tail```

Test Lambda works
```
curl --header "Content-Type: application/json" --request POST --data '{"hands":{"S":["D3", "C6", "DT", "D8", "DJ", "D6", "CA", "C3", "S2", "C2", "C4", "S9", "S7"],"W":["DA", "S4", "HT", "C5", "D4", "D7", "S6", "S3", "DK", "CT", "D2", "SK","H8"],"N":["C7", "H6", "H7", "H9", "CJ", "SA", "S8", "SQ", "D5", "S5", "HK", "C8", "HA"],"E":["H2", "H5", "CQ", "D9", "H4", "ST", "HQ", "SJ", "HJ", "DQ", "H3", "C9", "CK"]}}' https://dds.aws.globalbridge.app/api
```
