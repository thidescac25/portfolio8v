import streamlit as st
import pandas as pd
import yfinance as yf
import base64
import plotly.graph_objects as go
from datetime import datetime, timedelta
import re

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Komorebi Investments",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"  # Pour cacher la barre latérale par défaut
)

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

# Rendements des dividendes par société (données manuelles en %)
dividend_yields = {
    "GOOGL": 0.52,      # Alphabet
    "ERF.PA": 1.05,     # Eurofins Scientific
    "GTT.PA": 4.21,     # Gaztransport et Technigaz
    "GD": 2.01,         # General Dynamics
    "ROG.SW": 3.53,     # Roche Holding
    "RR.L": 1.17,       # Rolls-Royce
    "UBSG.SW": 1.82,    # UBS Group
    "VIE.PA": 4.41      # Veolia
}

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
        
        # Données financières
        sector = info.get('sector', "Non disponible")
        industry = info.get('industry', "Non disponible")
        country = info.get('country', "USA")  # Pays par défaut
        
        # Métriques financières - utiliser notre mapping de rendement de dividende
        pe_ratio = info.get('trailingPE', 0)
        dividend_yield = dividend_yields.get(ticker, 1.0)  # Utiliser notre valeur prédéfinie
        
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
        market_cap = info.get('marketCap', 0) / 1_000_000_000  # Conversion en milliards
        
        # Historique des prix pour le graphique
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
        import random
        
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
        date_range = pd.date_range(start=datetime.now() - timedelta(days=365), end=datetime.now(), freq='D')
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
            'country': countries.get(ticker, "USA"),  # Obtenir le pays depuis notre mapping
            'pe_ratio': random.uniform(15, 35),
            'dividend_yield': dividend_yields.get(ticker, 1.0),  # Utiliser notre valeur prédéfinie
            'ytd_change': random.uniform(-15, 25),
            'eps': random.uniform(1, 30),
            'market_cap': random.uniform(10, 500),
            'history': hist
        }

# Titre principal 
st.title("Komorebi Investments 8 stocks")

# Création du bandeau défilant avec un iframe HTML personnalisé
def create_scrolling_ticker():
    # Générer le contenu HTML pour le bandeau défilant
    ticker_items = ""
    
    for _, row in portfolio_df.iterrows():
        stock_data = get_stock_data(row['Ticker'])
        ticker = row['Ticker']
        currency = currency_mapping.get(ticker, "$")  # Utiliser la devise correspondante
        
        # Déterminer la classe CSS et flèche en fonction de la variation
        if stock_data['change'] >= 0:
            change_class = "positive"
            arrow = '<span style="font-size: 22px;">&#x25B2;</span>'  # Code HTML pour triangle pointant vers le haut
        else:
            change_class = "negative"
            arrow = '<span style="font-size: 22px;">&#x25BC;</span>'  # Code HTML pour triangle pointant vers le bas
        
        # Ajouter les informations de cette action au bandeau
        ticker_items += f"""
        <div class="ticker-item">
            <span class="ticker-name">{row['Société']}</span>
            <span class="ticker-price">{currency}{stock_data['current_price']:.2f}</span>
            <span class="ticker-change {change_class}">{arrow} {stock_data['percent_change']:.2f}%</span>
        </div>
        """
    
    # Code HTML complet pour le bandeau défilant avec spécification UTF-8
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
                padding: 15px 0;
            }}
            .ticker-tape {{
                display: inline-block;
                animation: ticker-scroll 120s linear infinite;  /* Ralenti à 120 secondes */
                padding-left: 100%;
            }}
            .ticker-item {{
                display: inline-block;
                padding: 0 50px;  /* Plus d'espace entre les éléments */
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
                {ticker_items}  <!-- Dupliquer les éléments pour assurer un défilement continu -->
            </div>
        </div>
    </body>
    </html>
    """
    
    # Encodage en base64 pour l'iframe avec spécification UTF-8 explicite
    b64 = base64.b64encode(html_content.encode("utf-8")).decode("utf-8")
    
    # Injecter l'iframe avec le contenu HTML
    iframe_html = f'<iframe src="data:text/html;base64,{b64}" width="100%" height="60px" frameborder="0" scrolling="no"></iframe>'
    
    return iframe_html

# Affichage du bandeau défilant
st.markdown(create_scrolling_ticker(), unsafe_allow_html=True)

# Custom CSS pour les cartes et autres éléments
st.markdown("""
<style>
    .stApp {
        background-color: #ffffff;  /* Fond blanc au lieu de bleu ciel */
    }
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    h1 {
        margin-bottom: 0.5rem;
    }
    .company-header {
        font-size: 32px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 5px;
        color: #102040;
    }
    .sector-header {
        font-size: 20px;
        font-weight: 500;
        margin-bottom: 25px;
        color: #555;
    }
    .section-container {
        padding: 25px 0;
    }
    .section-title {
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 20px;
        color: #693112;
        border-bottom: 3px solid #693112;
        padding-bottom: 10px;
    }
    .business-text {
        font-size: 20px;
        line-height: 1.7;
        font-weight: bold;
        text-align: justify;
    }
    .select-label {
        font-weight: bold;
        text-decoration: underline;
        color: #693112;
        margin-bottom: 10px;
        font-size: 18px;
    }
    .stSelectbox > div > div {
        background-color: #f9f5f2;
        border-color: #c0a080;
    }
    .stSelectbox > div > div > div {
        color: #693112;
        font-weight: 700 !important;
        font-size: 18px !important;
    }
    .chart-container {
        height: 400px;
        margin-top: 20px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Texte pour le sélecteur de société avec style souligné et couleur brune
st.markdown('<div class="select-label">Sélectionnez une société</div>', unsafe_allow_html=True)

# Liste déroulante pour sélectionner une société
companies = portfolio_df['Société'].tolist()
selected_company = st.selectbox("", companies, label_visibility="collapsed")

# Trouver les données de la société sélectionnée
company_data = portfolio_df[portfolio_df['Société'] == selected_company].iloc[0]
ticker = company_data['Ticker']
business_model = company_data['Business_models']

# Récupérer les données boursières et financières
stock_data = get_stock_data(ticker)

# Récupérer la devise pour la société sélectionnée
currency = currency_mapping.get(ticker, "$")

# Affichage des informations de la société (sans logo)
st.markdown(f'''
<div class="company-header">
    {selected_company}
</div>
<div class="sector-header">{stock_data["industry"]} - {stock_data["country"]}</div>
''', unsafe_allow_html=True)

# Business Model
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Business Model de la société</div>', unsafe_allow_html=True)
st.markdown(f'<div class="business-text">{business_model}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Titre "Indicateurs" avec séparateur
st.markdown('<div class="section-container" style="padding-top:0;">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Indicateurs</div>', unsafe_allow_html=True)

# Métriques financières - Toutes avec fond beige clair uniforme
# Création des colonnes pour les métriques
col1, col2, col3, col4, col5 = st.columns(5)

# Couleur beige clair uniforme pour toutes les métriques
beige_bg = "#f9f5f2"  # Beige clair

# Valorisation - PER
with col1:
    st.markdown(
        f"""
        <div style="background-color:{beige_bg}; padding:20px; border-radius:10px; text-align:center;">
            <div style="font-size:14px; color:#693112;margin-bottom:10px;">📈 Valorisation</div>
            <div style="font-size:28px; font-weight:bold;">{stock_data['pe_ratio']:.1f}</div>
            <div style="font-size:14px; color:#888;">PER</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Rendement - Dividende
with col2:
    st.markdown(
        f"""
        <div style="background-color:{beige_bg}; padding:20px; border-radius:10px; text-align:center;">
            <div style="font-size:14px; color:#693112;margin-bottom:10px;">💰 Rendement</div>
            <div style="font-size:28px; font-weight:bold;">{stock_data['dividend_yield']:.2f}%</div>
            <div style="font-size:14px; color:#888;">Dividende</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Performance - YTD
with col3:
    ytd_class = "#28a745" if stock_data['ytd_change'] >= 0 else "#dc3545"
    ytd_sign = "+" if stock_data['ytd_change'] >= 0 else ""
    st.markdown(
        f"""
        <div style="background-color:{beige_bg}; padding:20px; border-radius:10px; text-align:center;">
            <div style="font-size:14px; color:#693112;margin-bottom:10px;">📊 Performance</div>
            <div style="font-size:28px; font-weight:bold; color:{ytd_class};">{ytd_sign}{stock_data['ytd_change']:.2f}%</div>
            <div style="font-size:14px; color:#888;">YTD</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# BPA
with col4:
    st.markdown(
        f"""
        <div style="background-color:{beige_bg}; padding:20px; border-radius:10px; text-align:center;">
            <div style="font-size:14px; color:#693112;margin-bottom:10px;">💵 BPA</div>
            <div style="font-size:28px; font-weight:bold;">{currency}{stock_data['eps']:.2f}</div>
            <div style="font-size:14px; color:#888;">Par action</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Capitalisation
with col5:
    st.markdown(
        f"""
        <div style="background-color:{beige_bg}; padding:20px; border-radius:10px; text-align:center;">
            <div style="font-size:14px; color:#693112;margin-bottom:10px;">💼 Capitalisation</div>
            <div style="font-size:28px; font-weight:bold;">{currency}{stock_data['market_cap']:.2f}B</div>
            <div style="font-size:14px; color:#888;">Milliards</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown('</div>', unsafe_allow_html=True)

# Section Performance
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Performance sur 52 semaines</div>', unsafe_allow_html=True)

# Récupérer l'historique des prix
hist = stock_data['history']

# Calculer les statistiques
if not hist.empty:
    avg_price = hist['Close'].mean()
    max_price = hist['Close'].max()
    min_price = hist['Close'].min()
    
    # Afficher les statistiques principales
    stats_col1, stats_col2, stats_col3 = st.columns(3)
    with stats_col1:
        st.markdown(f'''
        <div style="text-align: center;">
            <div style="font-size: 14px; color: #666;">Prix Moyen</div>
            <div style="font-size: 24px; font-weight: bold;">{currency}{avg_price:.1f}</div>
        </div>
        ''', unsafe_allow_html=True)
        
    with stats_col2:
        st.markdown(f'''
        <div style="text-align: center;">
            <div style="font-size: 14px; color: #666;">Plus Haut</div>
            <div style="font-size: 24px; font-weight: bold;">{currency}{max_price:.1f}</div>
            <div style="font-size: 12px; color: #28a745;">↑ {max_price - avg_price:.1f}</div>
        </div>
        ''', unsafe_allow_html=True)
        
    with stats_col3:
        st.markdown(f'''
        <div style="text-align: center;">
            <div style="font-size: 14px; color: #666;">Plus Bas</div>
            <div style="font-size: 24px; font-weight: bold;">{currency}{min_price:.1f}</div>
            <div style="font-size: 12px; color: #dc3545;">↓ {avg_price - min_price:.1f}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Options de période
    periods = ["1 mois", "6 mois", "1 an"]
    period_selection = st.radio("Période", periods, horizontal=True, index=2)
    
    # Filtrer les données selon la période sélectionnée
    if period_selection == "1 mois":
        filtered_hist = hist.iloc[-30:]
    elif period_selection == "6 mois":
        filtered_hist = hist.iloc[-180:]
    else:  # 1 an
        filtered_hist = hist
    
    # Créer le graphique
    st.markdown('<div style="margin-top: 20px;">Évolution du cours - ' + period_selection + '</div>', unsafe_allow_html=True)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=filtered_hist.index,
        y=filtered_hist['Close'],
        mode='lines',
        name='Prix',
        line=dict(color='#693112', width=2)
    ))
    
    # Ajouter le volume en bas
    fig.add_trace(go.Bar(
        x=filtered_hist.index,
        y=filtered_hist['Volume'] / filtered_hist['Volume'].max() * filtered_hist['Close'].min() * 0.2,
        marker_color='rgba(105, 49, 18, 0.2)',
        name='Volume',
        yaxis='y2'
    ))
    
    # Mise en page
    fig.update_layout(
        height=450,
        margin=dict(l=0, r=0, t=10, b=10),
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        yaxis=dict(
            title=f'Prix ({currency})',
            side='left',
            showgrid=True,
            gridcolor='rgba(105, 49, 18, 0.1)'
        ),
        yaxis2=dict(
            showgrid=False,
            showticklabels=False,
            overlaying='y',
            range=[0, filtered_hist['Close'].min() * 0.3]
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(105, 49, 18, 0.1)'
        ),
        plot_bgcolor='white'
    )
    
    st.plotly_chart(fig, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)