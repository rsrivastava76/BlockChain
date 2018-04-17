
from flask import Flask, jsonify
from blockchain.Blockchain import Blockchain

app = Flask(__name__)

# creating a blockChain object
bChainObj = Blockchain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = bChainObj.get_previous_block()
    previous_proof = previous_block['proof']
    proof = bChainObj.proof_of_work(previous_proof)
    previous_hash = bChainObj.hash(previous_block)
    block = bChainObj.create_block(proof, previous_hash)
    response = {'message': 'Congratulations you did it!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']
                }
    return jsonify(response), 200


@app.route('/get_chain', methods=['GET'])
def get_chain():

    response = {'chain': bChainObj.chain,
                'message': 'Congratulations you did it!',
                'length': len(bChainObj.chain),
                }
    return jsonify(response), 200


# BlockChain is valid
@app.route('/is_valid', methods=['GET'])
def is_valid():

    valid = bChainObj.is_chain_valid(bChainObj.chain)

    if valid:
        response = {'is_valid': valid,
                'message': 'Validation function executed successfully'
                }
    else :
        response = {'is_valid': valid,
                    'message': 'Validation function failed, chain is not valid'
                    }

    return jsonify(response), 200

# running the flask App

app.run(host='0.0.0.0', port=8080)