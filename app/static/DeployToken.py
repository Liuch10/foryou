from web3 import Web3, TestRPCProvider, HTTPProvider
from web3.contract import Contract, ConciseContract

f_abi = open('./contract/FoYoToken.abi', 'r')
abi = f_abi.readline()

f_bin = open('./contract/FoYoToken.bin', 'r')
bin = f_bin.readline()

# web3.py instance
w3 = Web3(HTTPProvider('http://127.0.0.1:8545'))

# # Instantiate and deploy contract
contract = w3.eth.contract(abi=abi, bytecode=bin)
deployed = contract.constructor().transact({'from': w3.eth.coinbase})
tx_receipt = w3.eth.waitForTransactionReceipt(deployed)
contract_instance = w3.eth.contract(abi=abi, bytecode=bin, address=tx_receipt['contractAddress'],
                                    ContractFactoryClass=ConciseContract)
print(tx_receipt)
print(contract_instance.balanceOf(w3.eth.coinbase))
