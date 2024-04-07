from flask import Flask, request, jsonify, render_template
from web3 import Web3, HTTPProvider
import os
import json

app = Flask(__name__)

# Connect to XinFin blockchain node
rpc_url = "https://rpc.xinfin.network/"
web3 = Web3(HTTPProvider(rpc_url))

# Get the absolute path to the ABI file
abi_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'contract_abi.json'))

# Load the contract ABI with error handling
try:
    with open(abi_file_path, 'r') as abi_file:
        contract_abi = json.load(abi_file)
except FileNotFoundError:
    print("Error: ABI file not found")
    contract_abi = None
except json.decoder.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
    contract_abi = None

# Load the contract ABI and address if available
contract_address = "0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2"  # Your contract address
contract = web3.eth.contract(address=contract_address, abi=contract_abi) if contract_abi else None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transaction', methods=['POST'])
def transaction():
    asset = request.form.get('asset')
    # Perform encryption and store encrypted_asset and key
    encrypted_asset = 'Encrypted Asset'  # Placeholder for actual encryption
    key = 'Encryption Key'  # Placeholder for actual key
    return render_template('transaction.html', encrypted_asset=encrypted_asset, key=key)

@app.route('/decrypt', methods=['POST'])
def decrypt():
    encrypted_asset = request.form.get('encrypted_asset')
    key = request.form.get('key')
    # Perform decryption and store decrypted_asset
    decrypted_asset = 'Decrypted Asset'  # Placeholder for actual decryption
    return render_template('decrypted.html', decrypted_asset=decrypted_asset)

@app.route('/add_property', methods=['POST'])
def add_property():
    if contract is None:
        return jsonify({'error': 'Contract not initialized'})

    property_id = request.json.get('property_id')
    property_details = request.json.get('property_details')

    # Call the addProperty function of the smart contract
    tx_hash = contract.functions.addProperty(property_id, property_details).transact()

    # Wait for the transaction to be mined
    web3.eth.waitForTransactionReceipt(tx_hash)

    return jsonify({'message': 'Property added successfully'})

@app.route('/transfer_ownership', methods=['POST'])
def transfer_ownership():
    if contract is None:
        return jsonify({'error': 'Contract not initialized'})

    property_id = request.json.get('property_id')
    new_owner_address = request.json.get('new_owner_address')

    # Call the transferOwnership function of the smart contract
    tx_hash = contract.functions.transferOwnership(property_id, new_owner_address).transact()

    # Wait for the transaction to be mined
    web3.eth.waitForTransactionReceipt(tx_hash)

    return jsonify({'message': 'Ownership transferred successfully'})

if __name__ == '__main__':
    app.run(debug=True)
