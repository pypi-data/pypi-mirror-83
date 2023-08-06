# tBTC.py

A python client to interact with the [tbtc](https://tbtc.network/) protocol.

tBTC Protocol version: `1.1.0`


## Setup:
1. Create & activate virtulenv (python 3.6+)
2. Install the library using pypi. 

    ```
    pip install tbtc
    ```

## Usage:
1. Initialize the tbtc system
    ```
    >>> from tbtc.session import init_web3
    >>> w3 = init_web3(infura_url)
    >>> version = "1.1.0"
    >>> t = TBTC(version, w3, 'testnet', private_key)
    ```

2. Get lot sizes
    ```
    >>> lot_sizes = t.get_available_lot_sizes()
    ```

3. Create a deposit contract
    ```
    >>> logs = t.create_deposit(lot_sizes[0])
    ```

4. Get the bitcoin address for depositing BTC
    ```
    >>> d = Deposit(
    ... t, 
    ... logs[0]['args']['_depositContractAddress'],
    ... logs[0]['args']['_keepAddress']
    ... )
    >>> address = d.get_signer_public_key()
    ```

## Development:
1. Clone & enter the repo. `git clone https://github.com/ankitchiplunkar/tbtc.py.git`
2. Install required libraries. `pip install -r requirements.txt`

## Testing:
1. Run the tests locally 

    ```pytest -vv tests/```
