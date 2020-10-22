#FROM python:3.8.6-alpine3.12
FROM python:3

#RUN apk add --no-cache bash && \
RUN    pip install --no-cache-dir netifaces

COPY src/multicast.py .
RUN chmod a+x multicast.py

ENTRYPOINT ["bash"]
