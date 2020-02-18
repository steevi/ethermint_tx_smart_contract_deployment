#!/usr/bin/env sh
sleep 5

# remove files to reset state of the chain
rm -rf ~/.emint*

# Set up config for CLI
emintcli config chain-id 8 --home /genesis_data/emintcli
emintcli config output json --home /genesis_data/emintcli
emintcli config indent true --home /genesis_data/emintcli
# node to connect to
emintcli config node ${NODE} --home /genesis_data/emintcli

# TODO: options for different key, laddr, chainId

emintcli rest-server --laddr tcp://0.0.0.0:8545 --unlock-key ${KEYNAME} --home /genesis_data/emintcli keyring-backend test