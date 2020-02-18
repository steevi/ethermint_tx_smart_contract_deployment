import os
import time
from web3 import Web3, HTTPProvider, WebsocketProvider
from web3.eth import Account

# defaults for seed 0
GANACHE_PKS = [
        0x0cc0c2de7e8c30525b4ca3b9e0b9703fb29569060d403261055481df7014f7fa,
        0xb97de1848f97378ee439b37e776ffe11a2fff415b2f93dc240b2d16e9c184ba9,
        0x42f3b9b31fcaaa03ca71cab7d194979d0d1bedf16f8f4e9414f0ed4df699dd10,
        0x41219e3efe938f4b1b5bd68389705be763821460b940d5e2bd221f66f40028d3,
        0x64530eda5f401cc2e9bba4e7b2e0ba9b1bb9d95c344bf8643776b57bb6eb9845,
        0x76db32cb46895cdb4473c86b4468dbd45f46c1b3d7972002c72bea74efff18ef,
        0x3b747127e9ea07790d0fe9b8e5b6508953740d6cf0269d3145cdf1b69c22f2bb,
        0xc01836866febf10022ec9ae632677937f3070d4ed4819e5c6e03d3e8ec02dc2e,
        0xdf207d299d941818bb4f7822cf003662370a7d685016dfc3f1e2cac03d47fc1d,
        0x2d9d98ee99c8f7c664125ff2b3b91f356e880917b2d9fc508ffe1b647bd7a9fd
    ]


class AccountWrapper:
    """
    Wrapper to enable use of both accounts and unlocked addresses for most things (only raw address signing requires
    to have an explicit account for access to private key)
    """
    def __init__(self, account: Account = None, address: str = None):
        assert account or address
        assert not (account and address)
        self.account = account

        if account:
            self.address = account.address
        else:
            self.address = address


class Web3Connection:
    def __init__(self, network_url=None, use_infura=False, infura_network=None, infura_project_id=None,
                 avg_block_time=13, gas_limit=6_700_000, default_gas_price_gwei: int = 21, default_gas: int = 500_000,
                 chain_id: int = 1):
        """
        :param network_url: Connection to web3 provider. E.g. http://127.0.0.1:8545 for an existing ganache chain. None to start a new ganache chain
        :param infura_settings: dict with keys 'use_infura` (bool), 'network' (e.g. mainnet or ropsten), and `project_id`. If use_infura=True, network_url must be None
        :param avg_block_time: in seconds. Default: 13
        :param gas_limit: gas limit of the chain. Default: 6_700_000
        :param silent: verbosity, Defaukt: false
        """
        assert (network_url or use_infura) and not (network_url and use_infura), "Specify one of network_url or use_infura"

        self.use_infura = use_infura
        explorer_url = ''

        self.network_url = network_url
        self.avg_block_time = avg_block_time
        self.gas_limit = gas_limit
        self.default_gas_price = Web3.toWei(str(default_gas_price_gwei), 'gwei')
        self.default_gas = default_gas
        self.explorer_url = explorer_url
        self.w3 = None
        self.chain_id = chain_id

    def connect_to_w3(self):
        provider = HTTPProvider(self.network_url)
        w3 = Web3(provider)
        time.sleep(5)
        assert w3.isConnected(), "Not connected"
        self.w3 = w3
        return True

    @property
    def accounts(self):
        return self.w3.eth.accounts

    def send_signed_tx(self, function, account: AccountWrapper, wait_for_receipt=True, nonce=None,
                       gas=None, gas_price=None, value=0):
        """Infura only excepts raw transactions. So build and sign it before sending"""
        if nonce is None:
            nonce = self.w3.eth.getTransactionCount(account.address)

        skeleton = {'from': account.address,
                    'nonce': nonce,
                    'value': value,
                    'gas': gas}
        # do not rely on automatic gas estimation, might fail on certain nodes/ providers
        if gas is None:
            skeleton['gas'] = self.default_gas
        if gas_price is None:
            skeleton['gasPrice'] = self.default_gas_price

        if account.account is not None:
            skeleton['chainId'] = self.chain_id
            constructed_txn = function.buildTransaction(skeleton)
            signed = account.account.signTransaction(constructed_txn)
            tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        else:
            tx_hash = function.transact(skeleton)

        if wait_for_receipt:
            tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
            assert tx_receipt.status == 1, 'Tx failed with status {}, receipt: {}'.format(tx_receipt.status, tx_receipt)
        else:
            tx_receipt = None
        return tx_hash, tx_receipt

def create_account(conn: Web3Connection, pk: str = None, addr: str = None) -> AccountWrapper:
    assert pk is None or addr is None, "Provide one of pk and addr"
    if pk:
        account = AccountWrapper(conn.w3.eth.account.privateKeyToAccount(pk))
    elif addr:
        assert addr in conn.accounts, "Address not in known accounts"
        account = AccountWrapper(address=addr)
    else:
        account = AccountWrapper(address=conn.accounts[0])

    print(f"New account with address: {account.address}")
    return account
