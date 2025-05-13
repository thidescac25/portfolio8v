import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import base64

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Komorebi - Performance Portefeuille 8",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"  # Barre latérale toujours visible
)

# CSS personnalisé pour la page
st.markdown("""
<style>
    .stApp {
        background-color: #ffffff;
    }
    .section-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
        color: #693112;
        border-bottom: 3px solid #693112;
        padding-bottom: 10px;
    }
    .metric-container {
        background-color: #f9f5f2;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-title {
        font-size: 16px;
        color: #693112;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
    }
    .metric-subtitle {
        font-size: 12px;
        color: #888;
    }
    .positive {
        color: #28a745;
    }
    .negative {
        color: #dc3545;
    }
    .neutral {
        color: #102040;
    }
    .stock-info-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 10px;
        margin: 10px 0 20px 0;
    }
    .stock-info-item {
        background-color: #f9f5f2;
        border-radius: 5px;
        padding: 8px 12px;
        border-left: 4px solid #693112;
        min-width: 180px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Fonction pour charger les données du CSV
@st.cache_data
def load_portfolio_data():
    df = pd.read_csv("data/Portefeuille_8_business_models.csv")
    return df

# Chargement des données
portfolio_df = load_portfolio_data()

# Mapping des devises pour chaque ticker
currency_mapping = {
    "GOOGL": "$",    # Dollar américain pour Alphabet
    "ERF.PA": "€",   # Euro pour Eurofins Scientific
    "GTT.PA": "€",   # Euro pour Gaztransport et Technigaz
    "GD": "$",       # Dollar américain pour General Dynamics
    "ROG.SW": "CHF", # Franc suisse pour Roche Holding
    "RR.L": "£",     # Livre sterling pour Rolls-Royce
    "UBSG.SW": "CHF", # Franc suisse pour UBS Group
    "VIE.PA": "€"    # Euro pour Veolia
}

# Titre principal
st.markdown("<h1 style='font-size: 32px; margin-bottom: 10px;'>Komorebi - Performance du Portefeuille composé des 8 valeurs</h1>", unsafe_allow_html=True)

# Fonction pour obtenir les données boursières actuelles
@st.cache_data(ttl=60)  # Cache pour 60 secondes
def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Données actuelles
        current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
        previous_close = info.get('previousClose', info.get('regularMarketPreviousClose', 0))
        change = current_price - previous_close
        percent_change = (change / previous_close) * 100 if previous_close else 0
        
        return {
            'current_price': current_price,
            'previous_close': previous_close,
            'change': change,
            'percent_change': percent_change
        }
    except Exception as e:
        # Pour la démo, générons des données aléatoires en cas d'erreur
        import random
        current_price = random.uniform(500, 1000)
        previous_close = current_price * random.uniform(0.95, 1.05)
        change = current_price - previous_close
        percent_change = (change / previous_close) * 100
        
        return {
            'current_price': current_price,
            'previous_close': previous_close,
            'change': change,
            'percent_change': percent_change
        }

# Création du bandeau défilant
def create_scrolling_ticker():
    ticker_items = ""
    
    for _, row in portfolio_df.iterrows():
        stock_data = get_stock_data(row['Ticker'])
        ticker = row['Ticker']
        currency = currency_mapping.get(ticker, "$")
        
        if stock_data['change'] >= 0:
            change_class = "positive"
            arrow = '<span style="font-size: 22px;">&#x25B2;</span>'
        else:
            change_class = "negative"
            arrow = '<span style="font-size: 22px;">&#x25BC;</span>'
        
        ticker_items += f"""
        <div class="ticker-item">
            <span class="ticker-name">{row['Société']}</span>
            <span class="ticker-price">{currency}{stock_data['current_price']:.2f}</span>
            <span class="ticker-change {change_class}">{arrow} {stock_data['percent_change']:.2f}%</span>
        </div>
        """
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                margin: 0;
                padding: 0;
                overflow: hidden;
                background-color: #102040;
                font-family: Arial, sans-serif;
            }}
            .ticker-container {{
                width: 100%;
                overflow: hidden;
                white-space: nowrap;
                padding: 10px 0;
            }}
            .ticker-tape {{
                display: inline-block;
                animation: ticker-scroll 120s linear infinite;
                padding-left: 100%;
            }}
            .ticker-item {{
                display: inline-block;
                padding: 0 50px;
                color: white;
                font-size: 20px;
            }}
            .ticker-name {{
                font-weight: bold;
                margin-right: 15px;
            }}
            .ticker-price {{
                margin-right: 15px;
            }}
            .positive {{
                color: #00ff00;
                font-weight: bold;
            }}
            .negative {{
                color: #ff4d4d;
                font-weight: bold;
            }}
            @keyframes ticker-scroll {{
                0% {{ transform: translate3d(0, 0, 0); }}
                100% {{ transform: translate3d(-100%, 0, 0); }}
            }}
        </style>
    </head>
    <body>
        <div class="ticker-container">
            <div class="ticker-tape">
                {ticker_items}
                {ticker_items}
            </div>
        </div>
    </body>
    </html>
    """
    
    b64 = base64.b64encode(html_content.encode("utf-8")).decode("utf-8")
    iframe_html = f'<iframe src="data:text/html;base64,{b64}" width="100%" height="50px" frameborder="0" scrolling="no"></iframe>'
    return iframe_html

# Bandeau défilant après le titre principal
st.markdown(create_scrolling_ticker(), unsafe_allow_html=True)

# Interface utilisateur
st.markdown('<div class="section-title">Présentation de la Performance</div>', unsafe_allow_html=True)

# Récupérer les tickers du portefeuille
tickers = portfolio_df['Ticker'].tolist()
company_names = portfolio_df['Société'].tolist()

# Sélection de la période
col1, col2 = st.columns([3, 1])

with col1:
    # Date de début d'investissement
    st.markdown("<div style='display: flex; align-items: center;'><div>Date de début d'investissement</div><div style='margin: 0 10px;'> - </div><div style='color: #693112; font-style: italic;'>Choisissez une date</div></div>", unsafe_allow_html=True)
    min_date = datetime(2015, 1, 1)
    max_date = datetime.now() - timedelta(days=1)
    start_date = st.date_input(
        label="",  # Label vide car nous utilisons le markdown ci-dessus
        value=datetime(2023, 1, 1),
        min_value=min_date,
        max_value=max_date
    )
    end_date = datetime.now()

with col2:
    # Sélection des indices de référence
    indices_options = {
        "CAC 40": "^FCHI",
        "S&P 500": "^GSPC",
        "NASDAQ": "^IXIC",
        "EURO STOXX 50": "^STOXX50E"
    }
    selected_indices = st.multiselect(
        "Indices de référence",
        options=list(indices_options.keys()),
        default=["CAC 40"]
    )
    reference_indices = {name: indices_options[name] for name in selected_indices}

# Récupérer les données historiques
@st.cache_data(ttl=60) 
def get_historical_data(tickers, start_date=None, end_date=None):
    # Si end_date n'est pas fourni, utiliser la date actuelle
    if end_date is None:
        end_date = datetime.now()
        
    data = {}
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(start=start_date, end=end_date)
            if not hist.empty:
                # Pour éviter les problèmes de fuseau horaire, rendons les dates "naïves"
                hist.index = hist.index.tz_localize(None)
                data[ticker] = hist
        except Exception as e:
            st.warning(f"Erreur lors de la récupération des données pour {ticker}: {e}")
    return data

# Fonction pour afficher les performances
def plot_performance(hist_data, weights=None, reference_indices=None, end_date_ui=None):
    if weights is None:
        weights = [1/len(hist_data)] * len(hist_data)
    
    # Trouver les dates communes
    start_dates = []
    end_dates = []
    
    for ticker, hist in hist_data.items():
        if not hist.empty:
            start_dates.append(hist.index[0])
            end_dates.append(hist.index[-1])
    
    if not start_dates or not end_dates:
        st.warning("Pas assez de données pour créer un graphique.")
        return None
    
    start_date = max(start_dates)
    # Utiliser la date de fin fournie par l'UI ou la date maximale disponible
    end_date = end_date_ui or max(end_dates)
    
    # Créer le graphique
    fig = go.Figure()
    
    # Créer une plage de dates sans fuseau horaire
    date_range = pd.date_range(start=start_date, end=end_date, freq='B')
    
    # Initialiser le DataFrame pour les performances normalisées
    all_normalized = pd.DataFrame(index=date_range)
    
    # Variables pour stocker les traces
    portfolio_trace = None
    indices_traces = []
    
    # Ajouter chaque action
    for i, (ticker, hist) in enumerate(hist_data.items()):
        if hist.empty:
            continue
            
        # Filtrer par dates communes
        filtered_hist = hist[(hist.index >= start_date) & (hist.index <= end_date)]
        if filtered_hist.empty:
            continue
            
        # Réindexer pour s'assurer que les dates correspondent
        reindexed = filtered_hist['Close'].reindex(date_range, method='ffill')
        
        # Normaliser à 100
        normalized = reindexed / reindexed.iloc[0] * 100
        all_normalized[ticker] = normalized
    
    # Calculer la performance du portefeuille
    if all_normalized.empty:
        st.warning("Pas assez de données pour calculer la performance du portefeuille.")
        return None
        
    portfolio_performance = pd.Series(0, index=date_range)
    
    # Poids par défaut si nécessaire
    if len(weights) < len(hist_data):
        weights = [1/len(hist_data)] * len(hist_data)
    
    # Ajouter la contribution de chaque action
    for i, ticker in enumerate(all_normalized.columns):
        if i < len(weights):  # S'assurer que nous avons un poids pour cette action
            portfolio_performance += all_normalized[ticker] * weights[i]
    
    # Créer la trace du portefeuille
    portfolio_trace = go.Scatter(
        x=portfolio_performance.index,
        y=portfolio_performance.values,
        mode='lines',
        name='Portefeuille',
        line=dict(width=3, color='#693112')
    )
    
    # Ajouter les indices de référence
    if reference_indices:
        for name, ticker in reference_indices.items():
            try:
                reference = yf.Ticker(ticker)
                ref_hist = reference.history(start=start_date, end=end_date)
                if not ref_hist.empty:
                    # Rendre les dates naïves
                    ref_hist.index = ref_hist.index.tz_localize(None)
                    
                    # Réindexer pour correspondre à notre date_range
                    ref_close = ref_hist['Close'].reindex(date_range, method='ffill')
                    
                    # Normaliser
                    ref_normalized = ref_close / ref_close.iloc[0] * 100
                    
                    # Sauvegarder la trace de l'indice
                    indices_traces.append(go.Scatter(
                        x=ref_normalized.index,
                        y=ref_normalized.values,
                        mode='lines',
                        name=name,
                        line=dict(width=2.5, dash='dash')  # Ligne plus épaisse pour les indices
                    ))
            except Exception as e:
                st.warning(f"Erreur lors de la récupération des données pour {name}: {e}")
    
    # Ajouter les traces dans l'ordre : d'abord le portefeuille, puis les indices
    if portfolio_trace:
        fig.add_trace(portfolio_trace)
    
    for trace in indices_traces:
        fig.add_trace(trace)
    
    # Mise en forme
    fig.update_layout(
        title="Performance Comparée (Base 100)",
        xaxis_title="Date",
        yaxis_title="Performance (%)",
        height=500,
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Ajuster l'échelle Y pour mieux voir les courbes principales
    y_values = []
    
    # Récupérer les valeurs du portefeuille
    if portfolio_trace:
        y_values.extend(portfolio_trace.y)
    
    # Récupérer les valeurs des indices
    for trace in indices_traces:
        y_values.extend(trace.y)
    
    if y_values:
        # Calculer les percentiles pour déterminer une échelle appropriée
        y_values = [y for y in y_values if y is not None]
        if y_values:
            min_y = max(min(y_values) * 0.9, 0)  # Ne pas descendre en dessous de 0
            max_y = min(max(y_values) * 1.1, max(y_values) * 1.5)  # Limiter l'étendue supérieure
            
            # Calculer une valeur max raisonnable (ne pas aller trop haut)
            reasonable_max = max(150, min(max_y, 300))  # Entre 150% et 300% max
            
            # Mettre à jour les limites de l'axe Y
            fig.update_layout(yaxis=dict(range=[min_y, reasonable_max]))
    
    return fig

# Fonction pour simuler l'évolution du portefeuille
def plot_portfolio_simulation(hist_data, initial_investment=1000000, end_date_ui=None):
    # Trouver les dates communes
    start_dates = []
    end_dates = []
    
    for ticker, hist in hist_data.items():
        if not hist.empty:
            start_dates.append(hist.index[0])
            end_dates.append(hist.index[-1])
    
    if not start_dates or not end_dates:
        st.warning("Pas assez de données pour créer une simulation.")
        return None, 0, 0, 0, []
    
    start_date = max(start_dates)
    # Utiliser la date de fin fournie par l'UI ou la date maximale disponible
    end_date = end_date_ui or max(end_dates)
    
    # Créer une plage de dates sans fuseau horaire
    date_range = pd.date_range(start=start_date, end=end_date, freq='B')
    
    # Répartition équitable
    num_stocks = len(hist_data)
    investment_per_stock = initial_investment / num_stocks
    
    # Créer le graphique
    fig = go.Figure()
    
    # Initialiser le DataFrame pour les valeurs
    all_values = pd.DataFrame(index=date_range)
    
    # Calculer l'évolution de la valeur de chaque action
    stock_info = []
    for ticker, hist in hist_data.items():
        if hist.empty:
            continue
            
        # Réindexer pour correspondre à notre date_range
        reindexed = hist['Close'].reindex(date_range, method='ffill')
        
        if reindexed.empty or reindexed.isna().all() or reindexed.iloc[0] == 0:
            continue
        
        # Calculer le nombre d'actions achetées au début
        initial_price = reindexed.iloc[0]
        num_shares = investment_per_stock / initial_price
        
        # Stocker les informations pour l'affichage
        stock_info.append({
            "ticker": ticker,
            "num_shares": int(num_shares),
            "initial_investment": investment_per_stock
        })
        
        # Calculer la valeur au fil du temps
        stock_value = reindexed * num_shares
        all_values[ticker] = stock_value
        
        # Ajouter au graphique
        fig.add_trace(go.Scatter(
            x=stock_value.index,
            y=stock_value.values,
            mode='lines',
            name=ticker,
            line=dict(width=1, dash='dot'),
            opacity=0.3
        ))
    
    # Calculer la valeur totale du portefeuille
    portfolio_value = all_values.sum(axis=1)
    
    # Ajouter le portefeuille total
    fig.add_trace(go.Scatter(
        x=portfolio_value.index,
        y=portfolio_value.values,
        mode='lines',
        name='Portefeuille Total',
        line=dict(width=3, color='#693112')
    ))
    
    # Ajouter une ligne pour l'investissement initial
    fig.add_shape(
        type="line",
        x0=start_date,
        y0=initial_investment,
        x1=end_date,
        y1=initial_investment,
        line=dict(color="black", width=2, dash="dash")
    )
    
    # Mise en forme (MODIFIÉ)
    fig.update_layout(
        title=f"Évolution d'un investissement de {f"{initial_investment:_}".replace("_", " ")} € réparti équitablement",
        xaxis_title="Date",
        yaxis_title="Valeur (€)",
        height=500,
        template="plotly_white",
        showlegend=False  # Supprimer la légende complètement
    )
    
    # Ajuster l'échelle Y pour mieux voir les courbes principales
    if not portfolio_value.empty:
        min_y = max(portfolio_value.min() * 0.9, 0)  # Ne pas descendre sous zéro
        max_y = portfolio_value.max() * 1.1
        
        # Mettre à jour les limites de l'axe Y
        fig.update_layout(yaxis=dict(range=[min_y, max_y]))
    
    # Calculer le gain/perte total
    if portfolio_value.empty:
        final_value = initial_investment
        gain_loss = 0
        percent_change = 0
    else:
        final_value = portfolio_value.iloc[-1]
        gain_loss = final_value - initial_investment
        percent_change = (gain_loss / initial_investment) * 100
    
    return fig, final_value, gain_loss, percent_change, stock_info

with st.spinner("Chargement des données historiques..."):
    hist_data = get_historical_data(tickers, start_date, end_date)

# Afficher le graphique de performance
performance_fig = plot_performance(
    hist_data, 
    reference_indices=reference_indices,
    end_date_ui=end_date
)
if performance_fig:
    st.plotly_chart(performance_fig, use_container_width=True, key="performance_chart")

# Simulation d'investissement
st.markdown('<div class="section-title">Simulation d\'investissement</div>', unsafe_allow_html=True)

# Montant d'investissement
investment_amount = 1000000  # 1 million d'euros fixe

# Simulation
simulation_fig, final_value, gain_loss, percent_change, stock_info = plot_portfolio_simulation(
    hist_data, 
    investment_amount,
    end_date_ui=end_date
)

# Afficher les informations sur le nombre d'actions achetées
if stock_info:
    # Créer une disposition en colonnes (4 colonnes par ligne pour les écrans moyens)
    num_cols = 4  # Nombre de colonnes souhaité
    cols = st.columns(num_cols)
    
    # Distribuer les tickers dans les colonnes
    for i, info in enumerate(stock_info):
        with cols[i % num_cols]:  # Répartir équitablement entre les colonnes
            st.markdown(
                f"""
                <div style="background-color:#f9f5f2; padding:8px; 
                     border-left:4px solid #693112; border-right:4px solid #693112;
                     margin:4px 0; border-radius:5px; text-align:center; height:100%;">
                    <div style="font-weight:bold; font-size:14px;">{info['ticker']}</div>
                    <div style="font-size:12px;">{round(info['num_shares'])} actions</div>
                    <div style="font-size:12px;">{f"{int(info['initial_investment']):_}".replace("_", " ")} €</div>
                </div>
                """,
                unsafe_allow_html=True
            )

if simulation_fig:
    st.plotly_chart(simulation_fig, use_container_width=True, key="simulation_chart")
    
    # Afficher les résultats de la simulation (MODIFIÉ)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            f"""
            <div class="metric-container">
                <div class="metric-title">Valeur finale</div>
                <div class="metric-value">{f"{int(final_value):_}".replace("_", " ")} €</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div class="metric-container">
                <div class="metric-title">Gain/Perte</div>
                <div class="metric-value {'positive' if gain_loss >= 0 else 'negative'}">{'+' if gain_loss >= 0 else ''}{f"{int(gain_loss):_}".replace("_", " ")} €</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div class="metric-container">
                <div class="metric-title">Performance</div>
                <div class="metric-value {'positive' if percent_change >= 0 else 'negative'}">{percent_change:+.2f}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# Ajouter un séparateur marron entre la section de simulation et les camemberts
st.markdown("""
<div style="height: 3px; background-color: #693112; margin: 40px 0px 30px 0px;"></div>
""", unsafe_allow_html=True)

# Charger les métriques
@st.cache_data(ttl=60)
def load_metrics(tickers):
    rows = []
    for ticker in tickers:
        try:
            info = yf.Ticker(ticker).info
            # helpers
            def txt(k): return info.get(k, None)
            def num(k):
                v = info.get(k, None)
                return float(v) if v is not None else None
            rows.append({
                "Ticker":           ticker,
                "Nom complet":      txt("longName"),
                "Pays":             txt("country"),
                "Secteur":          txt("sector"),
                "Industrie":        txt("industry"),
                "Exchange":         txt("exchange"),
                "Devise":           txt("currency"),
                "Prix Ouv.":        num("open"),
                "Prix Actuel":      num("currentPrice"),
                "Clôture Prec.":    num("previousClose"),
                "52-sem. Bas":      num("fiftyTwoWeekLow"),
                "52-sem. Haut":     num("fiftyTwoWeekHigh"),
                "Moyenne 50j":      num("fiftyDayAverage"),
                "Moyenne 200j":     num("twoHundredDayAverage"),
                "Volume":           num("volume"),
                "Vol Moy. (10j)":   num("averageDailyVolume10Day"),
                "Market Cap":       num("marketCap"),
                "Beta":             num("beta"),
                "PER (TTM)":        num("trailingPE"),
                "PER Forward":      num("forwardPE"),
                "Div Yield":        num("dividendYield"),
                "Reco Analyses":    txt("recommendationKey"),
                "Objectif Prix":    num("targetMeanPrice"),
                "Nb Avis Anal.":    num("numberOfAnalystOpinions"),
            })
        except Exception as e:
            # Ajouter une ligne avec l'erreur
            st.warning(f"Erreur lors de la récupération des métriques pour {ticker}: {e}")
            rows.append({
                "Ticker":           ticker,
                "Nom complet":      f"Erreur : {str(e)}",
                "Pays":             None,
                "Secteur":          None,
                "Industrie":        None,
                "Exchange":         None,
                "Devise":           None,
                "Prix Ouv.":        None,
                "Prix Actuel":      None,
                "Clôture Prec.":    None,
                "52-sem. Bas":      None,
                "52-sem. Haut":     None,
                "Moyenne 50j":      None,
                "Moyenne 200j":     None,
                "Volume":           None,
                "Vol Moy. (10j)":   None,
                "Market Cap":       None,
                "Beta":             None,
                "PER (TTM)":        None,
                "PER Forward":      None,
                "Div Yield":        None,
                "Reco Analyses":    None,
                "Objectif Prix":    None,
                "Nb Avis Anal.":    None,
            })
    dfm = pd.DataFrame(rows).set_index("Ticker")
    return dfm

# Utilisation des métriques pour les camemberts mais pas d'affichage de tableau ici
metrics_df = load_metrics(tickers)

# Section pour les graphiques en camembert (répartition géographique et sectorielle)
st.markdown("### Répartition du Portefeuille")

# Utiliser le code fourni pour les camemberts
@st.cache_data
def load_sector_country(tickers):
    """Récupère secteur et pays pour chaque ticker via yfinance."""
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
            st.warning(f"Erreur lors de la récupération des données pour {tk}: {e}")
            data.append({
                "Ticker": tk,
                "Sector": "Non disponible",
                "Country": "Non disponible"
            })
    return pd.DataFrame(data)

# Charger les données secteur/pays
df_sc = load_sector_country(tickers)

# Allocation égale
df_sc["Weight"] = 1.0 / len(df_sc)

# Calcul des répartitions
sector_alloc = df_sc.groupby("Sector")["Weight"].sum().reset_index()
country_alloc = df_sc.groupby("Country")["Weight"].sum().reset_index()

# Afficher les camemberts côte à côte
col_pie1, col_pie2 = st.columns(2)

with col_pie1:
 # Version corrigée du camembert sectoriel (MODIFIÉ)
 colors = ['#693112', '#8B4513', '#A0522D', '#CD853F', '#D2691E', '#B8860B', '#DAA520']
 
 # Créer le graphique avec couleurs personnalisées
 fig_sector = px.pie(
     sector_alloc,
     names="Sector",
     values="Weight",
     title="Répartition Sectorielle",
     color="Sector",
     color_discrete_sequence=colors
 )
 
 # Configurer les textes dans le camembert
 fig_sector.update_traces(
     textposition="inside", 
     texttemplate="%{label}<br>%{percent:.0%}",  # Enlever les virgules en utilisant .0%
     textfont=dict(color='white'),  # Uniformiser tous les titres en blanc
     marker=dict(line=dict(color='#693112', width=1.5))  # Bordure marron
 )
 
 fig_sector.update_layout(
     showlegend=False,  # Supprimer la légende
     font=dict(color="#102040"),
     title_font=dict(color="#693112", size=18)
 )
 
 st.plotly_chart(fig_sector, use_container_width=True, key="sector_pie")

with col_pie2:
 # Camembert géographique avec différentes nuances de bleu
 blue_palette = ['#102040', '#1A365D', '#27496D', '#142F43', '#0F3460', '#2C3E50', '#34495E', '#283747']
 
 fig_geo = px.pie(
     country_alloc,
     names="Country",
     values="Weight",
     title="Répartition Géographique",
     color_discrete_sequence=blue_palette
 )
 fig_geo.update_traces(
     textposition="inside", 
     texttemplate="%{label}<br>%{percent:.0%}",  # Enlever les virgules
     textfont=dict(color='white')  # Uniformiser tous les titres en blanc
 )
 fig_geo.update_layout(
     showlegend=False,  # Supprimer la légende
     font=dict(color="#102040"),
     title_font=dict(color="#693112", size=18)
 )
 
 st.plotly_chart(fig_geo, use_container_width=True, key="geo_pie")

# Ajouter un séparateur marron entre les sections
st.markdown("""
<div style="height: 3px; background-color: #693112; margin: 40px 0px 30px 0px;"></div>
""", unsafe_allow_html=True)

# Affichage du tableau des métriques
st.markdown("### Tableau détaillé des valeurs")
st.dataframe(
 metrics_df.style.format({
     col: '{:.2f}' for col in metrics_df.select_dtypes(include=['float64']).columns
 }).background_gradient(
     cmap='YlOrBr', 
     subset=['Prix Actuel', 'Market Cap', 'PER (TTM)', 'Div Yield']
 ),
 use_container_width=True,
 key="metrics_table"
)

# Pied de page
st.markdown("""
<div style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #666;">
 <p>Komorebi Investments © 2025 - Analyse de Portefeuille</p>
 <p style="font-size: 12px; margin-top: 10px;">Les informations présentées ne constituent en aucun cas un conseil d'investissement, ni une sollicitation à acheter ou vendre des instruments financiers. L'investisseur est seul responsable de ses décisions d'investissement.</p>
</div>
""", unsafe_allow_html=True)