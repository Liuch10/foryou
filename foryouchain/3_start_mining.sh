#!/bin/sh
geth --datadir="./data" --networkid 8008  --rpc --rpccorsdomain="*" --rpcport="8545" --minerthreads="1" --mine --nodiscover --maxpeers=0 --unlock 0 console

