#!/usr/bin/env bash

##
## Input parameters
##
BINARY=/usr/bin/${BINARY:-emintd}
ID=${ID:-0}
VALIDATOR_STATE_FILE="/genesis_data/node${ID}/data/priv_validator_state.json"
##
## Assert linux binary
##
if ! [ -f "${BINARY}" ]; then
	echo "The binary $(basename "${BINARY}") cannot be found. Please add the binary to the shared folder. Please use the BINARY environment variable if the name of the binary is not 'gaiad' E.g.: -e BINARY=gaiad_my_test_version"
	exit 1
fi

##
## Create priv_validator_state.json if it does not exist
##
if [ ! -f "$VALIDATOR_STATE_FILE" ];
then
  echo "$VALIDATOR_STATE_FILE not found"
  echo "---"
  echo "Creating priv_validator_state.json"
  echo '{' >> $VALIDATOR_STATE_FILE
  echo '  "height": "0",' >> $VALIDATOR_STATE_FILE
  echo '  "round": "0",' >> $VALIDATOR_STATE_FILE
  echo '  "step": 0' >> $VALIDATOR_STATE_FILE
  echo '}' >> $VALIDATOR_STATE_FILE
  chmod 666 $VALIDATOR_STATE_FILE
fi

##
## Run binary with all parameters
##
export EMINTHOMEDIR="/genesis_data/node${ID}"

"${BINARY}" start --home "${EMINTHOMEDIR}" --rpc.laddr tcp://0.0.0.0:26657