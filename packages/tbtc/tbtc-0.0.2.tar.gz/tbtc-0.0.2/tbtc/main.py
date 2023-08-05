import os
from tbtc.tbtc_system import TBTC
from tbtc.session import setup_logging, init_web3, get_contracts
from tbtc.utils import initialize_contract
from tbtc.deposit import Deposit

setup_logging()
node_url = os.getenv("ROPSTEN_URL")
private_key = os.getenv("TBTC_PRIVATE_KEY")
w3 = init_web3(node_url)
version = "1.1.0"
deposit_address = "0xe336980ab9edd52FF50626F120f63889aD5F6b7B"
tx = '0xb3e5a3437bcea5d27927c3428db3f0144d6c58baa80b976ffb854bf696ae973c'
receipt = w3.eth.getTransactionReceipt(tx)

t = TBTC(version, w3, private_key)
lot_sizes = t.get_available_lot_sizes()
logs = t.system.events.Created().processReceipt(receipt)
# logs = t.create_deposit(lot_sizes[0])
d = Deposit(
    t, 
    logs[0]['args']['_depositContractAddress'],
    logs[0]['args']['_keepAddress']
)
address = d.get_signer_public_key()