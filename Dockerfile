FROM quay.io/packet/packet-hardware:latest

# Install tools
RUN apt update && apt install -y lldpd

COPY ./ /opt/discover-metal
# Install discover-metal
RUN pip3 install --no-cache-dir /opt/discover-metal && \
    rm -rf /opt/packet-hardware

ENTRYPOINT ["discover-metal"]
