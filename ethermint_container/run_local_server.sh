#!/usr/bin/env sh
sleep 5

# remove files to reset state of the chain
rm -rf ~/.emint*

# config for testing: remove prompts for key password
emintcli config keyring-backend test

mnemonic="disease mountain circle olive impose change grape citizen cup seek course walk strategy balance picnic safe priority remain science coconut raise green outdoor clean"
echo ${mnemonic} | emintcli keys add test --recover

# Set up config for CLI
emintcli config chain-id 8
emintcli config output json
emintcli config indent true
emintcli config trust-node true
# node to connect to
emintcli config node ${NODE}

# TODO: options for different key, laddr, chainId

emintcli rest-server --laddr tcp://0.0.0.0:8545 --unlock-key test