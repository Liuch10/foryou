#!/bin/sh
geth --datadir="./data" account new >> ./account0.info
echo  "next?"
read
geth --datadir="./data" init genesisblock.json
