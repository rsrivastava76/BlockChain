import datetime
import hashlib
import json
from flask import flask, jsonify

class Blockchain:

    def __int__(self):
        self.chain = []
        self.create_block (proof = 1, previous_hash = '0')

    def create_block(self, proof, previous_hash):
        block = {'index':len(self.chain)+1 ,
                 'timestamp': str(datetime.datetime.now()),
                 'proof' : proof,
                 'prev_hash' : previous_hash
                 }
        self.chain.append(block)
        return block

    