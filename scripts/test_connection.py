# -----------------------------------------
# This script will test your connection with the Ethereum Classic network to ensure you're connected to the correct network before uploading the Ethscriptions.
# -----------------------------------------

from web3 import Web3

# Connect to Ethereum Classic RPC
rpc_url = 'https://etc.rivet.link'
web3 = Web3(Web3.HTTPProvider(rpc_url))

# Check connection
if web3.is_connected():
    print("Successfully connected to the Ethereum Classic network.")
else:
    print("Failed to connect to the Ethereum Classic network.")
