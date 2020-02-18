import argparse
from pathlib import Path

from web3Wrapper.Web3Connection import Web3Connection, GANACHE_PKS, create_account
from web3Wrapper.ContractHelper import ContractHelper

def connect_web3(chain_id=1):
    network_url = 'http://127.0.0.1:8545'
    conn = Web3Connection(network_url, avg_block_time=1, chain_id = chain_id)
    conn.connect_to_w3()
    return conn

def send_tx(conn: Web3Connection, _from: str, to: str, value: int, wait: bool = True):
    tx_hash = conn.w3.eth.sendTransaction({'from': _from, 'to': to, 'value': value,
                                           # 'chainId': conn.chain_id,
                                           'gas': conn.default_gas,
                                           'gasPrice': conn.default_gas_price,
                                           'nonce': conn.w3.eth.getTransactionCount(_from)})
    if wait:
        tx_receipt = conn.w3.eth.waitForTransactionReceipt(tx_hash)
        assert tx_receipt.status == 1, 'Tx failed with status {}, receipt: {}'.format(tx_receipt.status, tx_receipt)
    else:
        tx_receipt = None
    return tx_hash, tx_receipt

def deploy_contract(conn: Web3Connection, owner):
    p = Path(__file__).resolve().parent.parent
    build_root = p / 'contract'
    contract_names = ['CrowdsaleToken', 'SafeMathLib']
    contract_helper = ContractHelper(conn, build_root, contract_names)

    token = contract_helper.deploy_crowdsale_token(owner)
    return token

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Set up parameters')
    parser.add_argument('--chainid', dest='chainid', type=int,  help='Chain id to use', default=8)
    args = parser.parse_args()

    conn = connect_web3(chain_id=args.chainid)

    # unlocked account as defined in the etheremint server
    token_owner_account = create_account(conn, addr=conn.accounts[0])
    b = conn.w3.eth.getBalance(token_owner_account.address)
    assert b > 0, "Token owner has a zero balance"

    # send a standard transfer transaction
    print("Sending standard transaction")
    _to = conn.w3.eth.account.from_key(private_key=GANACHE_PKS[1])
    send_tx(conn, token_owner_account.address, _to.address, 100)
    print("Standard transaction sent")

    # deploy a smart contract
    token = deploy_contract(conn, token_owner_account)

