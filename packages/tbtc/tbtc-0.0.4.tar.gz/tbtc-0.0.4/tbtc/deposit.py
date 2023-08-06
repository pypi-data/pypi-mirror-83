from tbtc.utils import initialize_contract
from tbtc.bitcoin_helpers import point_to_p2wpkh_address

class Deposit():
    """
    Deposit class to interact with the deposit contract
    """

    def __init__(self, tbtc_system, deposit_contract, keep_address):
        self.deposit_address = deposit_contract
        self.keep_address = keep_address
        self.tbtc_system = tbtc_system
        self.deposit_contract = initialize_contract(tbtc_system.w3, deposit_contract, "Deposit")
        self.keep_contract = initialize_contract(tbtc_system.w3, keep_address, "BondedECDSAKeep")
        
    def __repr__(self):
        return f"Deposit contract at: {self.deposit_contract}"

    def get_signer_public_key(self):
        # finding qn existing public key event
        event = self.tbtc_system._get_existing_public_key_event(self.deposit_address)
        # no registered public key found
        if event == []:
            # check if key is ready
            transaction_filter = self.keep_contract.events.PublicKeyPublished.createFilter(
                fromBlock='earliest',
                toBlock='latest'
            )
            key_ready_event = transaction_filter.get_all_entries()
            if key_ready_event is None:
                logger.info("Retry again later key has not been published yet")
                return None
            else:
                call = self.deposit_contract.functions.retrieveSignerPubkey()
                receipt = self.tbtc_system._manage_transaction(
                    call, 
                    gas_limit=160000
                    )
                event = self.tbtc_system.system.events.RegisteredPubkey().processReceipt(receipt)
        return point_to_p2wpkh_address(
            event[0]['args']['_signingGroupPubkeyX'], 
            event[0]['args']['_signingGroupPubkeyY']
            )
