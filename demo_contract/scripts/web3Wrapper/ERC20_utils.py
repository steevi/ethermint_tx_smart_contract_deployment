FET_TOKEN_PARAMS = {
    '_name': "Fetch.AI",
    '_symbol': "FET",
    '_initialSupply': 1152997575 * 10 ** 18,
    '_decimals': 18,
    '_mintable': False
}

def as_tok(amount):
    return amount * 10 ** FET_TOKEN_PARAMS['_decimals']

def as_FET(amount_tok):
    return amount_tok / 10 ** FET_TOKEN_PARAMS['_decimals']
