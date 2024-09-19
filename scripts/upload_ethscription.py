# -----------------------------------------
# This script will upload each Hexadecimal as an individual Ethscription to the Ethereum Classic Mordor Testnet. 
# -----------------------------------------

import os
import json
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Connect to Ethereum Classic RPC
rpc_url = 'https://rpc.mordor.etccooperative.org/'
web3 = Web3(Web3.HTTPProvider(rpc_url))

# Ensure connection is successful
if not web3.is_connected():
    print("Failed to connect to the Ethereum Classic network.")
    exit()

# Your wallet address and private key from environment variables
wallet_address = os.getenv('WALLET_ADDRESS')
private_key = os.getenv('PRIVATE_KEY')

# Define the directory with your hex files
hex_dir = 'hex_svgs'
tx_hashes = {}

# Function to send a transaction with hex data as calldata
def send_ethscription(hex_data, to_address, private_key, nonce):
    gas_price = web3.eth.gas_price

    tx = {
        'nonce': nonce,
        'to': to_address,
        'value': 0,
        'gas': 2000000,
        'gasPrice': gas_price,
        'data': hex_data,
        'chainId': 63  # Chain ID for Ethereum Classic Mordor Testnet
    }

    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return tx_hash.hex()

# Get the starting nonce
nonce = web3.eth.get_transaction_count(wallet_address)

# Process each hex file and send transactions
for root, dirs, files in os.walk(hex_dir):
    for file in files:
        if file.endswith('.hex'):
            hex_input_path = os.path.join(root, file)
            
            # Read hex data
            with open(hex_input_path, 'r') as hex_file:
                hex_data = hex_file.read().strip()

            # Send the transaction
            tx_hash = send_ethscription(hex_data, wallet_address, private_key, nonce)
            tx_hashes[file] = tx_hash
            print(f'Transaction sent. Tx hash: {tx_hash}')

            # Increment nonce
            nonce += 1

# Save transaction hashes to a JSON file
with open(os.path.join(hex_dir, 'transaction_hashes.json'), 'w') as json_file:
    json.dump(tx_hashes, json_file, indent=4)

print("Transactions complete. Transaction hashes saved to transaction_hashes.json")
