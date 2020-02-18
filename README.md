## Instructions for smart contract deployment on ethermint

**truffle requires to be installed**

`npm install -g truffle`

### Fetch the latest version of ethermint

`git submodule update --init --recursive`

**Building ethermint docker image**

`docker build -t emint_node ethermint_container/`


### Contract deployment using a single node cluster

```
# To start a single validator ethermint chain run
docker-compose -f single-validator-docker-compose.yaml up

# Switch to demo_contract dir, and run deploy_contact.py
cd demo_contract
pipenv install
pipenv shell
python scripts/tx_contract.py

# Shut down single validator ethermint by running
docker-compose -f single-validator-docker-compose.yaml down
```

### Contract deployment using a two validator node cluster

```
# To start a two validator ethermint chain run
docker-compose -f multiple_validators-docker-compose.yaml up

# Switch to demo_contract dir, and run deploy_contact.py
cd demo_contract
pipenv install
pipenv shell
python scripts/tx_contract.py

# Shut down single validator ethermint by running
docker-compose -f multiple_validators-docker-compose.yaml down
```
