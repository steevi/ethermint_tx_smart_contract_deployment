FROM golang:buster AS build-env

# Set up dependencies
ENV PACKAGES make git curl

# Set working directory for the build
WORKDIR /go/src/github.com/cosmos/ethermint

# Install dependencies
RUN apt install -y $PACKAGES

# Add source files
COPY ./ethermint/ .

# Make the binary
RUN make build

# Final image
FROM debian:buster

# Copy over binaries from the build-env
COPY --from=build-env /go/src/github.com/cosmos/ethermint/build/emintd /usr/bin/emintd
COPY --from=build-env /go/src/github.com/cosmos/ethermint/build/emintcli /usr/bin/emintcli

COPY run-node.sh /usr/bin/run-node.sh
COPY run-server.sh /usr/bin/run-server.sh
COPY run_local_node.sh /usr/bin/run_local_node.sh
COPY run_local_server.sh /usr/bin/run_local_server.sh

WORKDIR /genesis_data
COPY ./genesis_data/ .

EXPOSE 26656
EXPOSE 26657
EXPOSE 26658
STOPSIGNAL SIGTERM
