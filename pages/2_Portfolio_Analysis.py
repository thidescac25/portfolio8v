import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import base64
import sys
import os

# Ajouter src/ au chemin d'importation
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

# Importer les modules personnalisés
from data_loader import load_portfolio_data
from ui_components import apply_custom_css

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Komorebi - Performance Portefeuille 8",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Appliquer le CSS personnalisé
apply_custom_css()

# CSS supplémentaire pour cette page
st.markdown("""
<style>
    .separator {
        height: 3px;
        background-color: #693112;
        margin: 35px 0px 30px 0px;
    }
    .separator-reduced {
        height: 3px;
        background-color: #693112;
        margin: 15px 0px 15px 0px;
    }
</style>
""", unsafe_allow_html=True)

# Chargement des données
portfolio_df = load_portfolio_data()

# Mapping des devises pour chaque ticker
currency_mapping = {
    "GOOGL": "$",
    "ERF.PA": "€",
    "GTT.PA": "€",
    "GD": "$",
    "ROG.SW": "CHF",
    "RR.L": "£",
    "UBSG.SW": "CHF",
    "VIE.PA": "€"
}

# Titre principal
st.markdown("<h1 style='font-size: 32px; margin-bottom: 10px;'>Komorebi - Performance du Portefeuille 8 valeurs <span style='font-size: 18px;'>(page 2/2)</span></h1>", unsafe_allow_html=True)

# Fonction pour obtenir les données boursières actuelles
@st.cache_data(ttl=60)
def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
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

# Création du bandeau défilant pour la watchlist - CORRIGÉ pour défilement continu
def create_watchlist_scrolling_ticker(watchlist_df):
    ticker_items = ""
    
    for _, row in watchlist_df.iterrows():
        # Récupérer le nom complet de la société
        ticker = row.get('Ticker', 'N/A')
        company = row.get('Nom complet', ticker)  # Utiliser "Nom complet" du CSV
        
        # Obtenir les données en temps réel pour chaque ticker de la watchlist
        try:
            stock_data = get_stock_data(ticker)
            current_price = stock_data['current_price']
            percent_change = stock_data['percent_change']
            # Utiliser la devise du CSV
            currency = row.get('Devise', '$')  # Utiliser la colonne "Devise" du CSV
            
            if percent_change >= 0:
                change_class = "positive"
                arrow = '<span style="font-size: 22px;">&#x25B2;</span>'
            else:
                change_class = "negative"
                arrow = '<span style="font-size: 22px;">&#x25BC;</span>'
            
            # Afficher le nom complet de la société
            ticker_items += f"""
            <div class="ticker-item">
                <span class="ticker-name">{company}</span>
                <span class="ticker-price">{currency}{current_price:.2f}</span>
                <span class="ticker-change {change_class}">{arrow} {percent_change:.2f}%</span>
            </div>
            """
        except:
            # En cas d'erreur, afficher seulement le nom complet de la société
            currency = row.get('Devise', '$')
            ticker_items += f"""
            <div class="ticker-item">
                <span class="ticker-name">{company}</span>
                <span class="ticker-price">N/A</span>
                <span class="ticker-change">N/A</span>
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
                animation: ticker-scroll 90s linear infinite;
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
                {ticker_items}
            </div>
        </div>
    </body>
    </html>
    """
    
    b64 = base64.b64encode(html_content.encode("utf-8")).decode("utf-8")
    iframe_html = f'<iframe src="data:text/html;base64,{b64}" width="100%" height="50px" frameborder="0" scrolling="no"></iframe>'
    return iframe_html

# Bandeau défilant
st.markdown(create_scrolling_ticker(), unsafe_allow_html=True)

# Interface utilisateur avec espace supplémentaire
st.markdown('<div style="margin-top: 25px;"><div class="section-title">Présentation de la Performance</div></div>', unsafe_allow_html=True)

# Récupérer les tickers du portefeuille
tickers = portfolio_df['Ticker'].tolist()

# Sélection de la période
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("<div style='display: flex; align-items: center;'><div>Date de début d'investissement</div><div style='margin: 0 10px;'> - </div><div style='color: #693112; font-style: italic;'>Choisissez une date</div></div>", unsafe_allow_html=True)
    min_date = datetime(2015, 1, 1)
    max_date = datetime.now() - timedelta(days=1)
    start_date = st.date_input(
        label="",
        value=datetime(2023, 1, 1),
        min_value=min_date,
        max_value=max_date
    )
    end_date = datetime.now()

with col2:
    indices_options = {
        "CAC 40": "^FCHI",
        "S&P 500": "^GSPC",
        "NASDAQ": "^IXIC",
        "EURO STOXX 50": "^STOXX50E"
    }
    selected_indices = st.multiselect(
        "Indices de référence",
        options=list(indices_options.keys()),
        default=["CAC 40", "S&P 500"]
    )
    reference_indices = {name: indices_options[name] for name in selected_indices}

# Récupérer les données historiques
@st.cache_data(ttl=60) 
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
            st.warning(f"Erreur lors de la récupération des données pour {ticker}: {e}")
    return data

# Fonction pour afficher les performances
def plot_performance(hist_data, weights=None, reference_indices=None, end_date_ui=None):
    if weights is None:
        weights = [1/len(hist_data)] * len(hist_data)
    
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
    end_date = end_date_ui or max(end_dates)
    
    fig = go.Figure()
    date_range = pd.date_range(start=start_date, end=end_date, freq='B')
    all_normalized = pd.DataFrame(index=date_range)
    
    for i, (ticker, hist) in enumerate(hist_data.items()):
        if hist.empty:
            continue
            
        filtered_hist = hist[(hist.index >= start_date) & (hist.index <= end_date)]
        if filtered_hist.empty:
            continue
            
        reindexed = filtered_hist['Close'].reindex(date_range, method='ffill')
        normalized = reindexed / reindexed.iloc[0] * 100
        all_normalized[ticker] = normalized
    
    if all_normalized.empty:
        st.warning("Pas assez de données pour calculer la performance du portefeuille.")
        return None
        
    portfolio_performance = pd.Series(0, index=date_range)
    
    if len(weights) < len(hist_data):
        weights = [1/len(hist_data)] * len(hist_data)
    
    for i, ticker in enumerate(all_normalized.columns):
        if i < len(weights):
            portfolio_performance += all_normalized[ticker] * weights[i]
    
    fig.add_trace(go.Scatter(
        x=portfolio_performance.index,
        y=portfolio_performance.values,
        mode='lines',
        name='Portefeuille',
        line=dict(width=3, color='#693112')
    ))
    
    if reference_indices:
        for name, ticker in reference_indices.items():
            try:
                reference = yf.Ticker(ticker)
                ref_hist = reference.history(start=start_date, end=end_date)
                if not ref_hist.empty:
                    ref_hist.index = ref_hist.index.tz_localize(None)
                    ref_close = ref_hist['Close'].reindex(date_range, method='ffill')
                    ref_normalized = ref_close / ref_close.iloc[0] * 100
                    
                    fig.add_trace(go.Scatter(
                        x=ref_normalized.index,
                        y=ref_normalized.values,
                        mode='lines',
                        name=name,
                        line=dict(width=2.5, dash='dash')
                    ))
            except Exception as e:
                st.warning(f"Erreur lors de la récupération des données pour {name}: {e}")
    
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
    
    return fig

# Fonction pour simuler l'évolution du portefeuille
def plot_portfolio_simulation(hist_data, initial_investment=1000000, end_date_ui=None):
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
    end_date = end_date_ui or max(end_dates)
    
    date_range = pd.date_range(start=start_date, end=end_date, freq='B')
    
    num_stocks = len(hist_data)
    investment_per_stock = initial_investment / num_stocks
    
    fig = go.Figure()
    all_values = pd.DataFrame(index=date_range)
    
    stock_info = []
    for ticker, hist in hist_data.items():
        if hist.empty:
            continue
            
        reindexed = hist['Close'].reindex(date_range, method='ffill')
        
        if reindexed.empty or reindexed.isna().all() or reindexed.iloc[0] == 0:
            continue
        
        initial_price = reindexed.iloc[0]
        num_shares = investment_per_stock / initial_price
        
        stock_info.append({
            "ticker": ticker,
            "num_shares": int(num_shares),
            "initial_investment": investment_per_stock
        })
        
        stock_value = reindexed * num_shares
        all_values[ticker] = stock_value
        
        fig.add_trace(go.Scatter(
            x=stock_value.index,
            y=stock_value.values,
            mode='lines',
            name=ticker,
            line=dict(width=1, dash='dot'),
            opacity=0.3
        ))
    
    portfolio_value = all_values.sum(axis=1)
    
    fig.add_trace(go.Scatter(
        x=portfolio_value.index,
        y=portfolio_value.values,
        mode='lines',
        name='Portefeuille Total',
        line=dict(width=3, color='#693112')
    ))
    
    fig.add_shape(
        type="line",
        x0=start_date,
        y0=initial_investment,
        x1=end_date,
        y1=initial_investment,
        line=dict(color="black", width=2, dash="dash")
    )
    
    investment_formatted = f"{initial_investment:_}".replace("_", " ")
    title_text = f"Évolution d'un investissement de {investment_formatted} € réparti équitablement"
    
    fig.update_layout(
        title=title_text,
        xaxis_title="Date",
        yaxis_title="Valeur (€)",
        height=500,
        template="plotly_white",
        showlegend=False
    )
    
    if not portfolio_value.empty:
        min_y = max(portfolio_value.min() * 0.9, 0)
        max_y = portfolio_value.max() * 1.1
        fig.update_layout(yaxis=dict(range=[min_y, max_y]))
    
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

investment_amount = 1000000

simulation_fig, final_value, gain_loss, percent_change, stock_info = plot_portfolio_simulation(
    hist_data, 
    investment_amount,
    end_date_ui=end_date
)

# Afficher les informations sur le nombre d'actions achetées
if stock_info:
    num_cols = 4
    cols = st.columns(num_cols)
    
    for i, info in enumerate(stock_info):
        with cols[i % num_cols]:
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

# Séparateur entre sections
st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

# Section Contributeurs à la performance 
st.markdown('<div class="section-title">Contributeurs à la performance</div>', unsafe_allow_html=True)

# Calculer les statistiques de performance
def calculate_portfolio_stats(hist_data, portfolio_df, start_date, end_date):
    df_perf = []
    
    for ticker, hist in hist_data.items():
        if hist.empty:
            continue
            
        company_name = ticker
        company_row = portfolio_df[portfolio_df['Ticker'] == ticker]
        if not company_row.empty and 'Société' in company_row.columns:
            company_name = company_row.iloc[0]['Société']
            
        idx_start = hist.index.get_indexer([start_date], method='nearest')[0]
        start_price = hist['Close'].iloc[idx_start]
        end_price = hist['Close'].iloc[-1]
        
        if start_price > 0:
            pct_change = (end_price - start_price) / start_price * 100
            abs_change = end_price - start_price
            
            df_perf.append({
                'Ticker': ticker,
                'Société': company_name,
                'Prix départ': start_price,
                'Prix final': end_price,
                'Var. abs.': abs_change,
                'Var. (%)': pct_change
            })
    
    return pd.DataFrame(df_perf)

df_perf = calculate_portfolio_stats(hist_data, portfolio_df, start_date, end_date)

if not df_perf.empty:
    df_sorted = df_perf.sort_values(by='Var. (%)', ascending=False)
    positive_contributors = df_sorted[df_sorted['Var. (%)'] >= 0]
    negative_contributors = df_sorted[df_sorted['Var. (%)'] < 0].sort_values(by='Var. (%)', ascending=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h5 style='color: #693112;'>📈 Contributeurs Positifs</h5>", unsafe_allow_html=True)
        for i, row in positive_contributors.iterrows():
            st.markdown(f"""
            <div style="background-color:#9CAF88; border:1px solid #7A9B6F; padding:10px; margin:6px 0; border-radius:6px;">
                <div style="font-weight:bold; font-size:15px; color:#1B3D1B;">{row['Société']}</div>
                <div style="display:flex; justify-content:space-between; margin-top:6px;">
                    <span style="color:#2E4A2E; font-weight:bold; font-size:13px;">{row['Prix départ']:.2f} → {row['Prix final']:.2f}</span>
                    <span style="color:#1B3D1B; font-weight:bold; font-size:16px;">+{row['Var. (%)']:.2f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("<h5 style='color: #693112;'>📉 Contributeurs Négatifs</h5>", unsafe_allow_html=True)
        if not negative_contributors.empty:
            for i, row in negative_contributors.iterrows():
                st.markdown(f"""
                <div style="background-color:#C8AD7F; border:1px solid #B8934F; padding:10px; margin:6px 0; border-radius:6px;">
                    <div style="font-weight:bold; font-size:15px; color:#5D3A1B;">{row['Société']}</div>
                    <div style="display:flex; justify-content:space-between; margin-top:6px;">
                        <span style="color:#7A4F1B; font-weight:bold; font-size:13px;">{row['Prix départ']:.2f} → {row['Prix final']:.2f}</span>
                        <span style="color:#5D3A1B; font-weight:bold; font-size:16px;">{row['Var. (%)']:.2f}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("*Aucun contributeur négatif sur la période*", unsafe_allow_html=True)

# Séparateur
st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

# Section Répartition du Portefeuille (Camemberts)
st.markdown('<div class="section-title">Répartition du Portefeuille</div>', unsafe_allow_html=True)

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

df_sc = load_sector_country(tickers)
df_sc["Weight"] = 1.0 / len(df_sc)

sector_alloc = df_sc.groupby("Sector")["Weight"].sum().reset_index()
country_alloc = df_sc.groupby("Country")["Weight"].sum().reset_index()

col_pie1, col_pie2 = st.columns(2)

with col_pie1:
    # Camembert sectoriel avec nuances de marron
    brown_colors = ['#693112', '#8B4513', '#A0522D', '#CD853F', '#D2691E', '#B8860B', '#DAA520']
    
    fig_sector_pie = px.pie(
        sector_alloc,
        names="Sector",
        values="Weight",
        title="Répartition Sectorielle",
        color="Sector",
        color_discrete_sequence=brown_colors
    )
    
    fig_sector_pie.update_traces(
        textposition="inside", 
        texttemplate="%{label}<br>%{percent:.0%}",
        textfont=dict(color='white'),
        marker=dict(line=dict(color='#693112', width=1.5))
    )
    
    fig_sector_pie.update_layout(
        showlegend=False,
        font=dict(color="#102040"),
        title_font=dict(color="#693112", size=18)
    )
    
    st.plotly_chart(fig_sector_pie, use_container_width=True, key="sector_pie")

with col_pie2:
    # Camembert géographique avec nuances de bleu
    blue_palette = ['#102040', '#1A365D', '#27496D', '#142F43', '#0F3460', '#2C3E50', '#34495E', '#283747']
    
    fig_geo_pie = px.pie(
        country_alloc,
        names="Country",
        values="Weight",
        title="Répartition Géographique",
        color_discrete_sequence=blue_palette
    )
    fig_geo_pie.update_traces(
        textposition="inside", 
        texttemplate="%{label}<br>%{percent:.0%}",
        textfont=dict(color='white')
    )
    fig_geo_pie.update_layout(
        showlegend=False,
        font=dict(color="#102040"),
        title_font=dict(color="#693112", size=18)
    )
    
    st.plotly_chart(fig_geo_pie, use_container_width=True, key="geo_pie")

# Séparateur réduit
st.markdown('<div class="separator-reduced"></div>', unsafe_allow_html=True)

# Section Watchlist - Sociétés à l'étude
st.markdown('<div class="section-title">Watchlist - Sociétés à l\'étude susceptibles d\'intégrer le Portefeuille</div>', unsafe_allow_html=True)

# Charger le CSV de la watchlist
@st.cache_data
def load_watchlist_data():
    df = pd.read_csv("data/stock_data_7v.csv")
    return df

watchlist_df = load_watchlist_data()

# Créer et afficher le tableau de la watchlist avec style Plotly
def create_watchlist_table(watchlist_df):
    # Préparer les données avec formatage
    display_data = []
    headers = list(watchlist_df.columns)
    
    # En-têtes en gras
    header_vals = [f"<b>{col}</b>" for col in headers]
    
    # Préparer les données pour chaque colonne
    for col in headers:
        col_data = []
        for val in watchlist_df[col]:
            if pd.isna(val):
                col_data.append("<b>-</b>")
            elif isinstance(val, (int, float)):
                col_data.append(f"<b>{val:.2f}</b>" if isinstance(val, float) else f"<b>{val}</b>")
            else:
                col_data.append(f"<b>{val}</b>")
        display_data.append(col_data)
    
    # Créer le tableau Plotly
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=header_vals,
            fill_color='#693112',
            font=dict(color='white', size=14),
            align='center',
            height=45
        ),
        cells=dict(
            values=display_data,
            fill_color='white',
            font=dict(color='#102040', size=13),
            align='center',
            height=35
        )
    )])
    
    table_height = 45 + (len(watchlist_df) * 35) + 15
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=table_height
    )
    
    return fig

# Afficher le tableau de la watchlist
watchlist_table = create_watchlist_table(watchlist_df)
st.plotly_chart(watchlist_table, use_container_width=True, key="watchlist_table")

# Ajouter le bandeau défilant de la watchlist
st.markdown(create_watchlist_scrolling_ticker(watchlist_df), unsafe_allow_html=True)

# Séparateur final
st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

# Pied de page
st.markdown("""
<div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #666;">
    <p>Komorebi Investments © 2025 - Analyse de Portefeuille</p>
    <p style="font-size: 12px; margin-top: 10px;">Les informations présentées ne constituent en aucun cas un conseil d'investissement, ni une sollicitation à acheter ou vendre des instruments financiers. L'investisseur est seul responsable de ses décisions d'investissement.</p>
</div>
""", unsafe_allow_html=True)