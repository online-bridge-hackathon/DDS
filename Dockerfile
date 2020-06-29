FROM debian:buster as dds-builder

RUN apt-get update
# Install only minimum required packages
RUN apt-get install -y --no-install-recommends \
  ca-certificates \
  cmake \
  git \
  g++ \
  ninja-build

# Make sure sources are the latest for the build operation
ARG CACHEBUST=1
ADD libdds /app

RUN rm -rf /app/.build && \
  mkdir -p /app/.build

WORKDIR /app/.build

# Configure using RelWithDebInfo. This will help if system is setup to generate
# a core file in case of crash. Installation prefix is /usr. It uses Ninja
# generator which has better cmake generator than recursive Makefiles.
RUN cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo \
      -DCMAKE_INSTALL_PREFIX=/usr \
      -G Ninja \
      .. && \
# Compile the library
    ninja && \
# Install only runtime files into /app/.build/install
# (Required step because it can modify RUNPATH)
    env DESTDIR=install cmake -DCMAKE_INSTALL_COMPONENT=Runtime -P cmake_install.cmake

FROM python:3.7-buster

# Copy installed runtime files to real image
COPY --from=dds-builder /app/.build/install/usr/lib /usr/lib

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY /src/ /app/

ENV FLASK_APP "api.py"


