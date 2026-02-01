from web3 import Web3
import json, os
from dotenv import load_dotenv
load_dotenv()

provider = os.getenv("RPC_URL")
private_key = os.getenv("PRIVATE_KEY")
account = os.getenv("ACCOUNT")

w3 = Web3(Web3.HTTPProvider(provider))

with open("contract/abi.json") as f:
    abi = json.load(f)

with open("contract/contract_address.txt") as f:
    contract_address = f.read().strip()
contract = w3.eth.contract(address=contract_address, abi=abi)

def send_to_chain(prediction: int, data_hash: str):
    nonce = w3.eth.get_transaction_count(account)
    tx = contract.functions.storeResult(prediction, data_hash).build_transaction({
        "from": account,
        "nonce": nonce,
        "gas": 250000,
        "gasPrice": w3.eth.gas_price
    })
    
    signed = w3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    return tx_hash.hex()
