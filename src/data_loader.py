import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import random

# Fonction pour charger les données du portefeuille
@st.cache_data
def load_portfolio_data():
    df = pd.read_csv("data/Portefeuille_8_business_models.csv")
    return df

# Fonction pour obtenir les données boursières actuelles
@st.cache_data(ttl=60)  # Cache pour 60 secondes
def get_stock_data(ticker, detailed=False):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Données actuelles
        current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
        previous_close = info.get('previousClose', info.get('regularMarketPreviousClose', 0))
        change = current_price - previous_close
        percent_change = (change / previous_close) * 100 if previous_close else 0

        # Données financières
        sector = info.get('sector', "Non disponible")
        industry = info.get('industry', "Non disponible")
        country = info.get('country', "USA")  # Pays par défaut

        # Métriques financières - utiliser notre mapping de rendement de dividende
        pe_ratio = info.get('trailingPE', 0)
        
        # Import en local pour éviter des dépendances circulaires
        from stock_utils import get_dividend_yields
        dividend_yields_dict = get_dividend_yields()
        dividend_yield = dividend_yields_dict.get(ticker, 1.0)  # Utiliser notre valeur prédéfinie

        # Performance annuelle (YTD)
        history = stock.history(period="ytd")
        if not history.empty:
            ytd_start = history.iloc[0]['Close']
            ytd_current = history.iloc[-1]['Close']
            ytd_change = ((ytd_current - ytd_start) / ytd_start) * 100
        else:
            ytd_change = 0

        # BPA
        eps = info.get('trailingEps', 0)
        market_cap = info.get('marketCap', 0) / 1_000_000_000  # Conversion en milliards

        # Historique des prix pour le graphique (si detailed=True)
        hist = pd.DataFrame()
        if detailed:
            hist = stock.history(period="1y")

        return {
            'current_price': current_price,
            'previous_close': previous_close,
            'change': change,
            'percent_change': percent_change,
            'sector': sector,
            'industry': industry,
            'country': country,
            'pe_ratio': pe_ratio,
            'dividend_yield': dividend_yield,
            'ytd_change': ytd_change,
            'eps': eps,
            'market_cap': market_cap,
            'history': hist
        }
    except Exception as e:
        # Pour la démo, générons des données aléatoires pour chaque société
        
        # Import en local pour éviter des dépendances circulaires
        from stock_utils import get_dividend_yields
        dividend_yields_dict = get_dividend_yields()
        
        # Mapping des pays par ticker pour la démo
        countries = {
            "GOOGL": "USA",
            "ERF.PA": "France",
            "GTT.PA": "France",
            "GD": "USA",
            "ROG.SW": "Suisse",
            "RR.L": "Royaume-Uni",
            "UBSG.SW": "Suisse",
            "VIE.PA": "France"
        }

        # Créer un historique de prix simulé
        date_range = pd.date_range(
            start=datetime.now() - timedelta(days=365),
            end=datetime.now(),
            freq='D'
        )
        price_start = random.uniform(500, 1000)
        prices = []
        current_price = price_start

        for _ in range(len(date_range)):
            current_price = current_price * (1 + random.uniform(-0.03, 0.03))
            prices.append(current_price)

        hist = pd.DataFrame({
            'Date': date_range,
            'Close': prices,
            'Open': [p * random.uniform(0.98, 1.0) for p in prices],
            'High': [p * random.uniform(1.0, 1.05) for p in prices],
            'Low': [p * random.uniform(0.95, 1.0) for p in prices],
            'Volume': [random.randint(1000000, 10000000) for _ in range(len(date_range))]
        }).set_index('Date')

        current_price = prices[-1]
        previous_close = prices[-2]
        change = current_price - previous_close
        percent_change = (change / previous_close) * 100

        return {
            'current_price': current_price,
            'previous_close': previous_close,
            'change': change,
            'percent_change': percent_change,
            'sector': "Technology",
            'industry': "Semiconductor Equipment & Materials",
            'country': countries.get(ticker, "USA"),
            'pe_ratio': random.uniform(15, 35),
            'dividend_yield': dividend_yields_dict.get(ticker, 1.0),
            'ytd_change': random.uniform(-15, 25),
            'eps': random.uniform(1, 30),
            'market_cap': random.uniform(10, 500),
            'history': hist
        }

# Récupérer les données historiques
@st.cache_data(ttl=3600)  # Cache pour 1 heure
def get_historical_data(tickers, start_date=None, end_date=None):
    if end_date is None:
        end_date = datetime.now()

    data = {}
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(start=start_date, end=end_date)
            if not hist.empty:
                # Conversion des dates
                hist.index = hist.index.tz_localize(None)
                data[ticker] = hist
        except Exception as e:
            # En cas d'erreur, générer des données de démo
            date_range = pd.date_range(start=start_date, end=end_date, freq='D')
            price_start = random.uniform(500, 1000)
            prices = []
            current_price = price_start

            for _ in range(len(date_range)):
                current_price = current_price * (1 + random.uniform(-0.01, 0.01))
                prices.append(current_price)

            hist = pd.DataFrame({
                'Close': prices,
                'Open': [p * random.uniform(0.98, 1.0) for p in prices],
                'High': [p * random.uniform(1.0, 1.05) for p in prices],
                'Low': [p * random.uniform(0.95, 1.0) for p in prices],
                'Volume': [random.randint(100000, 1000000) for _ in range(len(date_range))]
            }, index=date_range)
            
            data[ticker] = hist
    return data

# Charger les données de secteur et pays pour les tickers
@st.cache_data
def load_sector_country_data(tickers):
    data = []
    for tk in tickers:
        try:
            info = yf.Ticker(tk).info
            data.append({
                "Ticker": tk,
                "Sector": info.get("sector", "Non disponible"),
                "Country": info.get("country", "Non disponible")
            })
        except Exception:
            # Mapping par défaut pour la démo
            sectors = {
                "GOOGL": "Technology",
                "ERF.PA": "Healthcare",
                "GTT.PA": "Energy",
                "GD": "Industrials",
                "ROG.SW": "Healthcare",
                "RR.L": "Industrials",
                "UBSG.SW": "Financials",
                "VIE.PA": "Utilities"
            }
            countries = {
                "GOOGL": "USA",
                "ERF.PA": "France",
                "GTT.PA": "France",
                "GD": "USA",
                "ROG.SW": "Switzerland",
                "RR.L": "United Kingdom",
                "UBSG.SW": "Switzerland",
                "VIE.PA": "France"
            }
            data.append({
                "Ticker": tk,
                "Sector": sectors.get(tk, "Non disponible"),
                "Country": countries.get(tk, "Non disponible")
            })
    return pd.DataFrame(data)

# Charger les données de la watchlist
@st.cache_data
def load_watchlist_data():
    try:
        return pd.read_csv("data/stock_data_7v.csv")
    except Exception:
        # Créer des données de démonstration si le fichier n'existe pas
        data = {
            'Nom_complet': ['Tesla Inc.', 'Apple Inc.', 'Microsoft Corp.', 'LVMH SA', 'Toyota Motor Corp.', 'JPMorgan Chase', 'Nestlé SA'],
            'Ticker': ['TSLA', 'AAPL', 'MSFT', 'MC.PA', 'TM', 'JPM', 'NESN.SW'],
            'Pays': ['USA', 'USA', 'USA', 'France', 'Japan', 'USA', 'Switzerland'],
            'Industrie': ['Automobile', 'Technology', 'Technology', 'Luxury Goods', 'Automobile', 'Banking', 'Food & Beverage'],
            'Devise': ['$', '$', '$', '€', '¥', '$', 'CHF'],
            'PER_historique': [80.5, 27.8, 34.2, 29.6, 12.3, 11.8, 24.5],
            'Rendement_du_dividende': [0.0, 0.005, 0.008, 0.015, 0.025, 0.028, 0.022],
            'Recommandation_cle': ['Buy', 'Strong Buy', 'Buy', 'Hold', 'Buy', 'Strong Buy', 'Hold']
        }
        return pd.DataFrame(data)