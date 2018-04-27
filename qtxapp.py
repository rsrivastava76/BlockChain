from uuid import uuid4

from flask import Flask, jsonify, request

from cryptocurrency.QTXCryptoCurrency import QTXCryptoCurrency

app = Flask(__name__)

# creating a blockChain object
bChainObj = QTXCryptoCurrency()

# mining of BlockChain

# creating address for the node on port

node_address = str(uuid4()).replace('-', '')


@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = bChainObj.get_previous_block()
    previous_proof = previous_block['proof']
    proof = bChainObj.proof_of_work(previous_proof)
    previous_hash = bChainObj.hash(previous_block)
    bChainObj.add_transaction(sender=node_address, receiver='Ritesh', amount=1)
    block = bChainObj.create_block(proof, previous_hash)
    response = {'message': 'Congratulations you did it!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']
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
    else:
        response = {'is_va lid': valid,
                    'message': 'Validation function failed, chain is not valid'
                    }
    return jsonify(response), 200


@app.route('/add_transactions', methods=['POST'])
def add_transaction():
    print("HI")
    requestData = request.get_json()
    print("test", requestData)
    transaction_keys = ['sender', 'receiver', 'amount']

    if not all(key in requestData for key in transaction_keys):
        return 'Bad request', 400

    index = bChainObj.add_transaction(requestData['sender'], requestData['receiver'], requestData['amount'])

    response = {'message': f'Transaction will be added to the Block {index}'}

    return jsonify(response), 201


# decentralizing our BlockChain
@app.route('/connect_node', methods=['POST'])
def connect_node():
    requestData = request.get_json()

    nodes = requestData.get['nodes']
    if nodes is None:
        return 'Bad request', 400

    for address in nodes:
        if address is not None:
            bChainObj.add_node(address)

    response = {'message': 'All the Nodes are now connected ',
                'totalNodes' : list(bChainObj.nodes)
                }
    return jsonify(response), 201


# replace BlockChain
@app.route('/replace_chain', methods=['GET'])
def replace_chain():

    is_chain_replaced = bChainObj.replace_chain()

    if is_chain_replaced:
        response = {'is_valid': is_chain_replaced,
                    'message': 'The Nodes have different chain hence replaced by longest chain',
                    'new_chain' : bChainObj.chain
                    }
    else:
        response = {'is_va lid': is_chain_replaced,
                    'message': 'The Chain is largest one',
                    'actual_chain' : bChainObj.chain
                    }
    return jsonify(response), 200

# running the flask App

app.run(host='0.0.0.0', port=8080)
