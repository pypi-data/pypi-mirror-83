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
deposit_address = "0xd7Edcd864c79C54AEFD82636103BA263C361d49D"
keep_address = '0x51a46759C9adf1a163764Fd387ef3f6738584686'

t = TBTC(version, w3, 'testnet', private_key)
lot_sizes = t.get_available_lot_sizes()
# deposit = t.create_deposit(lot_sizes[1])
deposit = Deposit(t, deposit_address, keep_address)
address = deposit.get_signer_public_key()