FROM python:3.9-alpine

RUN apk add --no-cache bash gcc linux-headers musl-dev && \
    pip install netifaces && \
    apk del gcc linux-headers musl-dev

COPY src/multicast.py .
RUN chmod a+x multicast.py

ENTRYPOINT ["bash"]
