# Mapping des devises pour chaque ticker
def get_currency_mapping():
    return {
        "GOOGL": "$",     # Dollar américain pour Alphabet
        "ERF.PA": "€",    # Euro pour Eurofins Scientific
        "GTT.PA": "€",    # Euro pour Gaztransport et Technigaz
        "GD": "$",        # Dollar américain pour General Dynamics
        "ROG.SW": "CHF",  # Franc suisse pour Roche Holding
        "RR.L": "£",      # Livre sterling pour Rolls-Royce Holdings
        "UBSG.SW": "CHF", # Franc suisse pour UBS Group
        "VIE.PA": "€",    # Euro pour Veolia Environnement
        "RIO.L": "£",     # Livre sterling pour Rio Tinto plc (Londres)
        "SLB": "$"        # Dollar américain pour Schlumberger (NYSE)
    }


# Rendements des dividendes par société (valeurs manuelles en %)
def get_dividend_yields():
    return {
        "GOOGL": 0.52,     # Alphabet
        "ERF.PA": 1.05,    # Eurofins Scientific
        "GTT.PA": 4.21,    # Gaztransport et Technigaz
        "GD": 2.01,        # General Dynamics
        "ROG.SW": 3.53,    # Roche Holding
        "RR.L": 1.17,      # Rolls-Royce Holdings
        "UBSG.SW": 1.82,   # UBS Group
        "VIE.PA": 4.41,    # Veolia Environnement
        "RIO.L": 6.00,     # Rio Tinto plc (dividende très élevé)
        "SLB": 2.30        # Schlumberger (rendement modéré)
    }


# Déterminer la devise d'un ticker
def determine_currency(ticker):
    currency_map = get_currency_mapping()
    return currency_map.get(ticker, "$")