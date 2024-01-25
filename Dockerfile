FROM python:slim

RUN pip install \
        getmac \
        paho-mqtt \
        pyyaml

COPY weatherstation/ /weatherstation/.

CMD [ "python3", "/weatherstation/__main__.py" ]