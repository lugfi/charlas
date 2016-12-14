FROM ubuntu

RUN apt-get update -y && \
    apt-get install -y python \
    python-flask \
    python-psycopg2

ADD server.py /opt/demo/

CMD python /opt/demo/server.py