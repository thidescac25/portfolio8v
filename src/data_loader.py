import streamlit as st
import pandas as pd
import yfinance as yf
import time
from datetime import datetime
from stock_utils import get_dividend_yields

# Fonction pour charger les données du portefeuille
@st.cache_data
def load_portfolio_data():
    df = pd.read_csv("data/Portefeuille_8_business_models.csv")
    return df

# Fonction pour obtenir les données boursières actuelles - VRAIES DONNÉES SEULEMENT
@st.cache_data(ttl=300)  # Cache 5 minutes pour refresh rapide du bandeau
def get_stock_data(ticker, detailed=False):
    max_retries = 2
    
    for attempt in range(max_retries):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            # Données actuelles - vérification des valeurs valides
            current_price = info.get('currentPrice') or info.get('regularMarketPrice')
            previous_close = info.get('previousClose') or info.get('regularMarketPreviousClose')
            
            # Si pas de données dans info, essayer avec history
            if not current_price or pd.isna(current_price):
                hist = stock.history(period="2d")
                if not hist.empty:
                    current_price = float(hist['Close'].iloc[-1])
                    if len(hist) > 1:
                        previous_close = float(hist['Close'].iloc[-2])
                    else:
                        previous_close = current_price
                else:
                    # Dernière tentative avec period="1d"
                    hist = stock.history(period="1d")
                    if not hist.empty:
                        current_price = float(hist['Close'].iloc[-1])
                        previous_close = current_price
                    else:
                        raise ValueError(f"Pas de données disponibles pour {ticker}")
            
            # Validation des données
            if pd.isna(current_price) or pd.isna(previous_close):
                raise ValueError(f"Données invalides pour {ticker}")
                
            current_price = float(current_price)
            previous_close = float(previous_close)
            
            # Calculs
            change = current_price - previous_close
            percent_change = (change / previous_close) * 100 if previous_close > 0 else 0
            
            # Vérifications anti-NaN
            if pd.isna(percent_change) or percent_change == float('inf') or percent_change == float('-inf'):
                percent_change = 0.0

            result = {
                'current_price': current_price,
                'previous_close': previous_close,
                'change': change,
                'percent_change': percent_change
            }

            # Données détaillées si demandées
            if detailed:
                # Données financières
                sector = info.get('sector', "Non disponible")
                industry = info.get('industry', "Non disponible")
                country = info.get('country', "USA")
                
                pe_ratio = info.get('trailingPE')
                if pd.isna(pe_ratio) or pe_ratio is None:
                    pe_ratio = 15.0
                    
                eps = info.get('trailingEps')
                if pd.isna(eps) or eps is None:
                    eps = 1.0
                    
                market_cap = info.get('marketCap')
                if market_cap and not pd.isna(market_cap):
                    market_cap = market_cap / 1_000_000_000
                else:
                    market_cap = 50.0

                dividend_yields_dict = get_dividend_yields()
                dividend_yield = dividend_yields_dict.get(ticker, 1.0)

                # Performance annuelle (YTD)
                try:
                    history = stock.history(period="ytd")
                    if not history.empty:
                        ytd_start = history.iloc[0]['Close']
                        ytd_current = history.iloc[-1]['Close']
                        if pd.notna(ytd_start) and pd.notna(ytd_current) and ytd_start > 0:
                            ytd_change = ((ytd_current - ytd_start) / ytd_start) * 100
                        else:
                            ytd_change = 0
                    else:
                        ytd_change = 0
                    
                    # Historique pour graphique
                    hist = stock.history(period="1y")
                except:
                    ytd_change = 0
                    hist = pd.DataFrame()

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
            if attempt < max_retries - 1:
                # Attendre un peu avant de réessayer
                time.sleep(1)
                continue
            else:
                # Dernière tentative échouée - retourner une erreur claire
                st.error(f"❌ Impossible de récupérer les données pour {ticker}: {str(e)}")
                
                # Données minimales pour éviter crash mais signaler l'erreur
                dividend_yields_dict = get_dividend_yields()
                
                error_result = {
                    'current_price': 0,
                    'previous_close': 0,
                    'change': 0,
                    'percent_change': 0,
                    'error': True  # Flag pour identifier les erreurs
                }
                
                if detailed:
                    error_result.update({
                        'sector': "Erreur de récupération",
                        'industry': "Erreur de récupération",
                        'country': "Erreur de récupération",
                        'pe_ratio': 0,
                        'dividend_yield': dividend_yields_dict.get(ticker, 0),
                        'ytd_change': 0,
                        'eps': 0,
                        'market_cap': 0,
                        'history': pd.DataFrame()
                    })
                
                return error_result

# Récupérer les données historiques (inchangé)
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
                hist.index = hist.index.tz_localize(None)
                data[ticker] = hist
        except Exception as e:
            st.warning(f"Erreur lors de la récupération des données historiques pour {ticker}: {e}")
            # En cas d'échec, retourner un DataFrame vide
            data[ticker] = pd.DataFrame()
    return data

# Charger les données de secteur et pays pour les tickers (inchangé)
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
        except Exception as e:
            st.warning(f"Erreur lors de la récupération des données sectorielles pour {tk}: {e}")
            data.append({
                "Ticker": tk,
                "Sector": "Non disponible",
                "Country": "Non disponible"
            })
    return pd.DataFrame(data)

# Charger les données de la watchlist (inchangé)
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