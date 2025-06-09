import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
from stock_utils import get_dividend_yields

# Fonction pour charger les données du portefeuille
@st.cache_data
def load_portfolio_data():
    df = pd.read_csv("data/Portefeuille_8_business_models.csv")
    return df

# Fonction pour obtenir les données boursières actuelles - VERSION SIMPLE QUI MARCHE
@st.cache_data(ttl=60) 
def get_stock_data(ticker, detailed=False):
    """
    Récupère les données récentes d'une action.
    
    Arguments:
        ticker (str): Symbole de l'action
        detailed (bool): Si True, récupère des données plus détaillées
        
    Returns:
        dict: Dictionnaire contenant les données de l'action
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Données actuelles
        current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
        previous_close = info.get('previousClose', info.get('regularMarketPreviousClose', 0))
        change = current_price - previous_close
        percent_change = (change / previous_close) * 100 if previous_close else 0
        
        result = {
            'current_price': current_price,
            'previous_close': previous_close,
            'change': change,
            'percent_change': percent_change
        }
        
        if detailed:
            # Données financières
            sector = info.get('sector', "Non disponible")
            industry = info.get('industry', "Non disponible")
            country = info.get('country', "USA") 
            
            # Métriques financières
            pe_ratio = info.get('trailingPE', 0)
            dividend_yields_dict = get_dividend_yields()
            dividend_yield = dividend_yields_dict.get(ticker, 1.0)
            
            # Performance annuelle (YTD)
            history = stock.history(period="ytd")
            if not history.empty:
                ytd_start = history.iloc[0]['Close']
                ytd_current = history.iloc[-1]['Close']
                ytd_change = ((ytd_current - ytd_start) / ytd_start) * 100
            else:
                ytd_change = 0
            
            # BPA et capitalisation
            eps = info.get('trailingEps', 0)
            market_cap = info.get('marketCap', 0) / 1_000_000_000 
            
            # Historique des prix pour le graphique
            hist = stock.history(period="1y")
            
            # Ajouter les données détaillées
            result.update({
                'sector': sector,
                'industry': industry,
                'country': country,
                'pe_ratio': pe_ratio,
                'dividend_yield': dividend_yield,
                'ytd_change': ytd_change,
                'eps': eps,
                'market_cap': market_cap,
                'history': hist
            })
            
        return result
        
    except Exception as e:
        # Gestion d'erreur simplifiée
        st.warning(f"Erreur lors de la récupération des données pour {ticker}: {e}")
        
        # Retourner une structure minimale mais valide
        dividend_yields_dict = get_dividend_yields()
        
        result = {
            'current_price': 0,
            'previous_close': 0,
            'change': 0,
            'percent_change': 0
        }
        
        if detailed:
            result.update({
                'sector': "Non disponible",
                'industry': "Non disponible",
                'country': "Non disponible",
                'pe_ratio': 0,
                'dividend_yield': dividend_yields_dict.get(ticker, 0),
                'ytd_change': 0,
                'eps': 0,
                'market_cap': 0,
                'history': pd.DataFrame()
            })
            
        return result

# Récupérer les données historiques
@st.cache_data(ttl=3600)  # Cache pour 1 heure
def get_historical_data(tickers, start_date=None, end_date=None):
    """
    Récupère les données historiques pour une liste de tickers.
    
    Arguments:
        tickers (list): Liste des symboles d'actions
        start_date (datetime, optional): Date de début
        end_date (datetime, optional): Date de fin
        
    Returns:
        dict: Dictionnaire de DataFrames avec historique des prix
    """
    if end_date is None:
        end_date = datetime.now()
        
    data = {}
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(start=start_date, end=end_date)
            if not hist.empty:
                hist.index = hist.index.tz_localize(None)
                data[ticker] = hist
            else:
                data[ticker] = pd.DataFrame()
        except Exception as e:
            st.warning(f"Erreur lors de la récupération des données historiques pour {ticker}: {e}")
            data[ticker] = pd.DataFrame()
    return data

# Charger les données de secteur et pays pour les tickers
@st.cache_data
def load_sector_country_data(tickers):
    """
    Récupère secteur et pays pour chaque ticker via yfinance.
    
    Arguments:
        tickers (list): Liste des symboles d'actions
        
    Returns:
        DataFrame: DataFrame avec secteur et pays pour chaque ticker
    """
    data = []
    for tk in tickers:
        try:
            info = yf.Ticker(tk).info
            data.append({
                "Ticker": tk,
                "Sector": info.get("sector", "Non disponible"),
                "Country": info.get("country", "Non disponible")
            })
        except Exception as e:
            st.warning(f"Erreur lors de la récupération des données sectorielles pour {tk}: {e}")
            data.append({
                "Ticker": tk,
                "Sector": "Non disponible",
                "Country": "Non disponible"
            })
    return pd.DataFrame(data)

# Charger les données de la watchlist
@st.cache_data
def load_watchlist_data():
    try:
        return pd.read_csv("data/stock_data_7v.csv")
    except Exception as e:
        st.error(f"Erreur lors du chargement de la watchlist: {e}")
        # Retourner un DataFrame vide avec les colonnes attendues
        return pd.DataFrame(columns=[
            'Nom_complet', 'Ticker', 'Pays', 'Industrie', 'Devise',
            'PER_historique', 'Rendement_du_dividende', 'Recommandation_cle'
        ])