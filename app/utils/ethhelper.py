from web3 import Web3, HTTPProvider


class EthHelper:
    def __init__(self, host='127.0.0.1', port='8545'):
        self.web3 = Web3(HTTPProvider('http://' + host + ":" + port))

    @staticmethod
    def getBlockNumber(host='127.0.0.1', port='8545'):
        web3 = Web3(HTTPProvider('http://' + host + ':' + port))
        return web3.eth.blockNumber

    def createAccount(self, passphrase='123456'):
        if self.web3:
            return address and passphrase
            return [self.web3.personal.newAccount(passphrase), passphrase]
        else:
            return [None, None]

    def lockAccount(self, addr):
        self.web3.personal.lockAccount(addr)


if __name__ == "__main__":
    # print(EthHelper.getBlockNumber())
    helper = EthHelper()
    address, passphrase = helper.createAccount("test")
    print(address + "\n" + passphrase)
    # the keystore file is stored in 'data' directory in the chain
