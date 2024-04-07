import hashlib
import json
from time import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from base64 import b64encode


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash = '1', proof = 100)

    def new_block(self,proof,previous_hash = None):
        block = {
            'index' : len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.harsh(self.chain[-1]),
        }
        
        self.current_transactions = []
        self.chain.append(block)
        return block
    
    def new_transaction(self,sender,recipient,amount,asset_data):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'asset_data': self.encrypt_asset_data(asset_data,recipient),
        })
        return self.last_block['index'] + 1
    
    def encrypt_asset_data(self,asset_data,recipient_public_key):
        recipient_key = RSA.import_key(recipient_public_key)
        cipher_rsa = PKCS1_v1_5.new(recipient_key)
        encrypted_data = cipher_rsa.encrypt(asset_data.encode())
        return b64encode(encrypted_data).decode()
    
    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    @property
    def last_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof,proof) is False:
            proof += 1

        return proof
    
    @staticmethod
    def valid_proof(last_proof,proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4]== "0000"
    
blockchain = Blockchain()

sender_key = RSA.generate(2048)
recipient_key = RSA.generate(2048)

sender_public_key = sender_key.publickey().export_key().decode()
recipient_public_key = recipient_key.publickey().export_key().decode()

asset_data = "Your asset data here"
transaction_index = blockchain.new_transaction(sender_public_key, recipient_public_key,1, asset_data)
print("Transaction added. Index:", transaction_index)
last_block = blockchain.last_block
last_proof = last_block['proof']
proof = blockchain.proof_of_work(last_proof)
previous_hash = blockchain.hash(last_block)
block = blockchain.new_block(proof, previous_hash)
print("New blockm] mined.")

print("Blockchain:")
print(json.dumps(blockchain.chain,indent=4))
