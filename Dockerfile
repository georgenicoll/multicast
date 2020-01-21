FROM python:alpine3.11

RUN apk add --no-cache bash

COPY src/multicast.py .
RUN chmod a+x multicast.py

ENTRYPOINT ["bash"]