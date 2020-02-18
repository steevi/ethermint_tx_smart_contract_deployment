#!/usr/bin/env sh

# remove files to reset state of the chain
rm -rf ~/.emint*

# Set moniker and chain-id for Ethermint (Moniker can be anything, chain-id must be an integer)
emintd init mymoniker --chain-id 8

# config for testing: remove prompts for key password
emintcli config keyring-backend test

mnemonic="disease mountain circle olive impose change grape citizen cup seek course walk strategy balance picnic safe priority remain science coconut raise green outdoor clean"
echo ${mnemonic} | emintcli keys add test --recover

# Set up config for CLI
emintcli config chain-id 8
emintcli config output json
emintcli config indent true
emintcli config trust-node true

# Allocate genesis accounts (cosmos formatted addresses)
emintd add-genesis-account $(emintcli keys show test -a) 100000000000000000000000000photon,100000000000000000000000000stake

# Sign genesis transaction
emintd gentx --name test --keyring-backend test

# Collect genesis tx
emintd collect-gentxs

# Run this to ensure everything worked and that the genesis file is setup correctly
emintd validate-genesis

# Start the node (remove the --pruning=nothing flag if historical queries are not needed)
emintd start --rpc.laddr tcp://0.0.0.0:26657
