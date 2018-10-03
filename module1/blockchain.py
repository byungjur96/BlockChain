# -*- coding: utf-8 -*-
# Module 1 - Create a BlockChain
# flask, request(mining, add transaction), postman needed
# Flask version==0.12.2
# get: get actual state of bc, mining / post: add a new transaction

import datetime  # for timestamp
import hashlib  # hash the blocks
import json  # to encode blocks
from flask import Flask, jsonify


# Part 1. Building a BlockChain
class BlockChain:
    def __init__(self):
        self.chain = []
        # generate genesis block
        self.create_block(proof=1, previous_hash='0')  # sha256을 사용할 때는 encoded string만 입력받음

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    # function that miners have to execute to find proof
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        # four leading zeros
        while not check_proof:
            # have to be not symmetry
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    # function that check if everything is alright
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]

            # check if previous_hash of each block is equal to hash of previous block
            if block['previous_hash'] != self.hash(previous_block):
                return False

            # check if each block has correct Proof-Of-Work
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False

            previous_block = block
            block_index += 1
        return True


# Part 2. Mining Our BlockChain

# Creating a Web App
app = Flask(__name__)

# Creating a BlockChain
bc = BlockChain()


# Mine a new Block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = bc.get_previous_block()
    previous_proof = previous_block['proof']
    proof = bc.proof_of_work(previous_proof)
    previous_hash = bc.hash(previous_block)
    block = bc.create_block(proof, previous_hash)
    response = {
        'message': 'Congratulations, you just mined a block!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200


# Get the full BlockChains
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
        'chain': bc.chain,
        'length': len(bc.chain)
    }
    return jsonify(response), 200


# Check if the BlockChain is valid
@app.route('/is_valid', methods=['GET'])
def is_valid():
    chain = bc.chain
    if bc.is_chain_valid(chain):
        response = {
            'message': 'The chain is valid!'
        }
    else:
        response = {
            'message': 'The chain is not valid!'
        }
    return jsonify(response), 200


# Running the App
app.run(host='0.0.0.0', port=5000)
