import json
import os
import subprocess
from pathlib import Path

from web3Wrapper.ERC20_utils import FET_TOKEN_PARAMS
from web3Wrapper.Web3Connection import Web3Connection, AccountWrapper


class ContractHelper:
    def __init__(self, conn: Web3Connection, build_root: str, contract_names: list):
        self.conn = conn

        multi_send_path = Path(__file__).resolve().parent / 'multiSend'
        self.contracts = self._get_contracts(build_root, contract_names)
        self.contracts['MultiSend'] = self._get_contracts(multi_send_path, ['MultiSend'], compile=False)['MultiSend']

    @staticmethod
    def _compile_contracts(build_root: str):
        cwd = os.getcwd()
        os.chdir(build_root)
        p = subprocess.run(['truffle' + ('.cmd' if os.name == 'nt' else ''), 'compile'])
        os.chdir(cwd)
        assert p.returncode == 0, "Compilation failed"

    def _get_contracts(self, build_root: str, contract_names: list, compile: bool = True):
        if compile:
            self._compile_contracts(build_root)
            path = os.path.join(build_root, 'build', 'contracts')
        else:
            path = build_root

        contracts = {}
        for contract in contract_names:
            with open(os.path.join(path, contract + '.json'), "r") as f:
                contracts[contract] = json.load(f)
        return contracts

    @staticmethod
    def _link_contract(bytecode, libName, libAddress):
        """Replace placeholder in bytecode with deployed address"""
        repeats = 40 - len(libName) - 2
        assert repeats > 0, "libName too long"
        symbol = "__" + libName + repeats * "_"
        return bytecode.replace(symbol, libAddress.lower()[2:])

    def deploy_contracts(self, name, address, gas=None, gas_price=None, links=None, contract_args=None):
        if contract_args is None:
            contract_args = {}
        if gas is None:
            gas = self.conn.gas_limit

        bytecode = self.contracts[name]['bytecode']
        if links:
            for libName, libAddress in links.items():
                bytecode = self._link_contract(bytecode, libName, libAddress)

        Contract = self.conn.w3.eth.contract(abi=self.contracts[name]['abi'], bytecode=bytecode)

        tx_hash, tx_receipt = self.conn.send_signed_tx(Contract.constructor(**contract_args),
                                                       address,
                                                       wait_for_receipt=True,
                                                       gas=gas,
                                                       gas_price=gas_price)

        contract = self.conn.w3.eth.contract(address=tx_receipt.contractAddress, abi=self.contracts[name]['abi'])

        print('{} deployed at {}{}'.format(name, self.conn.explorer_url, contract.address))

        return contract

    def deploy_crowdsale_token(self, account: AccountWrapper, gas=None, gas_price=None):
        safe_math_lib = self.deploy_contracts('SafeMathLib', account, gas, gas_price)
        token = self.deploy_contracts('CrowdsaleToken', account,
                                      links={'SafeMathLib': safe_math_lib.address},
                                      contract_args=FET_TOKEN_PARAMS)
        tx_hash, tx_receipt = self.conn.send_signed_tx(token.functions.setReleaseAgent(account.address), account)
        tx_hash, tx_receipt = self.conn.send_signed_tx(token.functions.releaseTokenTransfer(), account)
        return token