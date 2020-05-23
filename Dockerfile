FROM debian:stretch as dds-builder

RUN apt-get update
RUN apt-get install -y \
  git \
  build-essential \
  libboost-thread-dev

RUN mkdir -p /app

RUN git clone https://github.com/df7cb/dds /app && \
  cd /app && \
  git checkout linux-memory

WORKDIR /app/src

RUN cp ./Makefiles/Makefile_linux_shared ./Makefile
RUN make clean && make

FROM python:3.7-stretch

RUN apt-get update
RUN apt-get install -y libboost-thread-dev

COPY --from=dds-builder /app/src/libdds.so /usr/lib/

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY /src/ /app/

ENV FLASK_APP "api.py"


