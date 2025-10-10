def get_currency_mapping():
    return {
        "GOOGL": "$",
        "ERF.PA": "€",
        "GTT.PA": "€",
        "GD": "$",
        "ROG.SW": "CHF",
        "RR.L": "£",
        "UBSG.SW": "CHF",
        "VIE.PA": "€",
        "RIO.L": "£",
        "OTIS": "$"
    }

def get_dividend_yields():
    return {
        "GOOGL": 0.52,
        "ERF.PA": 1.05,
        "GTT.PA": 4.21,
        "GD": 2.01,
        "ROG.SW": 3.53,
        "RR.L": 1.17,
        "UBSG.SW": 1.82,
        "VIE.PA": 4.41,
        "RIO.L": 6.00,
        "OTIS": 1.50
    }

def determine_currency(ticker):
    currency_map = get_currency_mapping()
    return currency_map.get(ticker, "$")