import json
import web3

from web3 import Web3, TestRPCProvider, HTTPProvider
from solc import compile_source
from web3.contract import ConciseContract
from config import TOKEN_ABI_FILE, TOKEN_BIN_FILE, CONTRACT_ADDRESS


class EthHelper:
    def __init__(self, host='127.0.0.1', port='8545'):
        self.w3 = Web3(HTTPProvider('http://' + host + ":" + port))
        self._contract()

    def _contract(self, abi_file=TOKEN_ABI_FILE, bin_file=TOKEN_BIN_FILE,
                  contract_address=CONTRACT_ADDRESS):

        if (abi_file and bin_file and contract_address):
            with open(abi_file, 'r') as f_abi:
                contract_abi = f_abi.readline()
            with open(bin_file, 'r') as f_bin:
                contract_bin = f_bin.readline()

            self.concise_contract_instance = self.w3.eth.contract(abi=contract_abi, bytecode=contract_bin,
                                                                  address=contract_address,
                                                                  ContractFactoryClass=ConciseContract)
        else:
            self.concise_contract_instance = None

    @staticmethod
    def getBlockNumber(host='127.0.0.1', port='8545'):
        web3 = Web3(HTTPProvider('http://' + host + ':' + port))
        return web3.eth.blockNumber

    def createAccount(self, passphrase=''):
        if self.w3:
            return address and passphrase
            return [self.web3.personal.newAccount(passphrase), passphrase]
        else:
            return [None, None]

    def lockAccount(self, addr):
        self.w3.personal.lockAccount(addr)

    def reward(self, targetAdd, num_token):
        transact_hash = self.concise_contract_instance.transfer(Web3.toChecksumAddress(targetAdd), num_token,
                                                                transact={'from': self.w3.eth.coinbase})
        # reward_receipt = self.w3.eth.waitForTransactionReceipt(transact_hash)
        return transact_hash


if __name__ == "__main__":
    # print(EthHelper.getBlockNumber())
    helper = EthHelper()
    address, passphrase = helper.createAccount("test")
    print(address + "\n" + passphrase)
    # the keystore file is stored in 'data' directory in the chain
