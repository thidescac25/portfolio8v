import streamlit as st
import pandas as pd
import sys
import os
import plotly.graph_objects as go
import streamlit.components.v1 as components

# Ajouter src/ au chemin d'importation
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

# Importer les modules personnalisés
from data_loader import load_portfolio_data, get_stock_data, load_sector_country_data
from stock_utils import get_currency_mapping, get_dividend_yields, determine_currency
from ui_components import apply_custom_css, create_scrolling_ticker, create_title, create_footer
from visualization import create_stock_chart, create_portfolio_table

# Configuration de la page
st.set_page_config(
    page_title="Komorebi Investments 8 stocks",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Appliquer le CSS personnalisé
apply_custom_css()

# Titre principal 
st.markdown(
    create_title("Komorebi Investments 8 stocks <span style='font-size:18px;'>(page 1/2)</span>"),
    unsafe_allow_html=True
)

# Chargement des données
portfolio_df = load_portfolio_data()
currency_mapping = get_currency_mapping()
dividend_yields = get_dividend_yields()

@st.cache_data(ttl=60)
def get_all_stock_data(tickers):
    d = {}
    for t in tickers:
        d[t] = get_stock_data(t)
    return d

tickers = portfolio_df['Ticker'].tolist()
stock_data_dict = get_all_stock_data(tickers)

# Charger les données secteur/pays
df_sc = load_sector_country_data(tickers)
sector_map = dict(zip(df_sc["Ticker"], df_sc["Sector"]))
country_map = dict(zip(df_sc["Ticker"], df_sc["Country"]))

# Affichage du bandeau défilant
st.markdown(create_scrolling_ticker(portfolio_df, stock_data_dict, currency_mapping), unsafe_allow_html=True)

# Ajout d'espace après le bandeau défilant
st.markdown('<div style="height:35px;"></div>', unsafe_allow_html=True)

# Texte pour le sélecteur de société
st.markdown('<div class="select-label">Sélectionnez une société</div>', unsafe_allow_html=True)

# Liste déroulante pour sélectionner une société
companies = portfolio_df['Société'].tolist()
selected_company = st.selectbox("", companies, label_visibility="collapsed")

# Trouver les données de la société sélectionnée
company_data = portfolio_df[portfolio_df['Société'] == selected_company].iloc[0]
ticker = company_data['Ticker']
business_model = company_data['Business_models']

# Récupérer les données boursières et financières
stock_data = get_stock_data(ticker, detailed=True)

# Récupérer la devise
currency = determine_currency(ticker)

# Affichage des informations de la société
st.markdown(
    f'''
    <div class="company-header">
        {selected_company}
    </div>
    <div class="sector-header">{stock_data["industry"]} - {stock_data["country"]}</div>
    ''',
    unsafe_allow_html=True
)

# Business Model avec padding-top réduit
st.markdown('<div class="section-container" style="padding-top:10px;">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Business Model de la société</div>', unsafe_allow_html=True)
st.markdown(f'<div class="business-text">{business_model}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Indicateurs
st.markdown('<div class="section-container" style="padding-top:0;">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Statistiques du jour</div>', unsafe_allow_html=True)

cols = st.columns(5)
metrics = [
    ("Valorisation",   stock_data["pe_ratio"],        "PER",        False),
    ("Rendement",      stock_data["dividend_yield"],  "Dividende",  True),
    ("Performance",    stock_data["ytd_change"],      "YTD",        True),
    ("BPA",            stock_data["eps"],             "Par action", False),
    ("Capitalisation", stock_data["market_cap"],      "Milliards",  False),
]
beige = "#f9f5f2"

for col, (title, val, subtitle, is_pct) in zip(cols, metrics):
    color = "#28a745" if is_pct and val >= 0 else "#dc3545" if is_pct else "#102040"
    disp  = f"{val:+.2f}%" if is_pct else f"{val:.2f}"
    with col:
        st.markdown(f"""
        <div style="background:{beige}; padding:20px; border-radius:10px; text-align:center;">
          <div style="font-size:14px; color:#693112; margin-bottom:10px;">{title}</div>
          <div style="font-size:28px; font-weight:bold; color:{color};">{disp}</div>
          <div style="font-size:14px; color:#888;">{subtitle}</div>
        </div>
        """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Performance sur 52 semaines
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Performance sur 52 semaines</div>', unsafe_allow_html=True)

hist = stock_data.get("history", pd.DataFrame())
if not hist.empty:
    sel, *_ = st.radio("Période", ["1 mois","6 mois","1 an"], horizontal=True, index=2)
    fig, *_ = create_stock_chart(hist, ticker, currency, sel)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Données historiques non disponibles pour cette action.")
st.markdown('</div>', unsafe_allow_html=True)

# Composition du portefeuille
st.markdown('<div class="section-title">Composition du portefeuille</div>', unsafe_allow_html=True)

# CSS OPTIMAL - Solution ChatGPT v2 + largeur complète
st.markdown("""
<style>
/* 1/ Enlève tout espace sous le tableau plotly (Solution ChatGPT v2) */
.stPlotlyChart > div {
    margin-bottom: 0 !important;
    padding-bottom: 0 !important;
}

/* 2/ Force le titre suivant à coller en haut (Solution ChatGPT v2) */
.section-title.next {
    margin-top: 5px !important;
    margin-bottom: 5px !important;
}

/* 3/ Largeur complète du tableau (Ma contribution) */
.portfolio-table-container {
    width: 100vw !important;
    margin-left: calc(-50vw + 50%) !important;
    margin-right: calc(-50vw + 50%) !important;
    padding: 0 !important;
}

.portfolio-table-container iframe {
    width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

# Préparation du DataFrame pour le tableau
comp = []
for _, r in portfolio_df.iterrows():
    sd = stock_data_dict.get(r["Ticker"], {})
    comp.append({
        "Société":               r["Société"],
        "Variation (%) du jour": sd.get("percent_change", 0),
        "Prix":                  sd.get("current_price", 0),
        "Devise":                determine_currency(r["Ticker"]),
        "Secteur":               sector_map.get(r["Ticker"], "N/A"),
        "Pays":                  country_map.get(r["Ticker"], "N/A"),
    })
comp_df = pd.DataFrame(comp)
comp_df.index = range(1, len(comp_df) + 1)

# Utiliser la fonction modulaire pour créer le tableau AVEC sa hauteur originale
table_fig, table_height = create_portfolio_table(comp_df)

# Forcer la largeur complète dans Plotly
table_fig.update_layout(
    width=None,
    autosize=True,
    margin=dict(l=0, r=0, t=0, b=0)
)

# Convertir en HTML
html_str = table_fig.to_html(
    include_plotlyjs="cdn", 
    full_html=False,
    config={'displayModeBar': False}
)

# Affichage du tableau dans un conteneur élargi
st.markdown('<div class="portfolio-table-container">', unsafe_allow_html=True)
components.html(html_str, height=table_height, scrolling=False)
st.markdown('</div>', unsafe_allow_html=True)

# SUPPRESSION du spacer + titre avec classe "next" (Solution ChatGPT v2)
st.markdown('<div class="section-title next">Performance du jour des valeurs</div>', unsafe_allow_html=True)

n     = len(comp_df)
pos   = sum(v>0 for v in comp_df["Variation (%) du jour"])
neg   = sum(v<0 for v in comp_df["Variation (%) du jour"])
neu   = n - pos - neg
pos_p = pos/n*100; neg_p = neg/n*100; neu_p = neu/n*100

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
      <div class="metric-container">
        <div class="metric-title">📈 Nombre de valeurs</div>
        <div class="metric-value">{n}</div>
        <div class="metric-subtitle">actions</div>
      </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
      <div class="metric-container">
        <div class="metric-title">💹 Performances positives</div>
        <div class="metric-value positive">{pos} ({pos_p:.1f}%)</div>
        <div class="metric-subtitle">valeurs en hausse</div>
      </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown(f"""
      <div class="metric-container">
        <div class="metric-title">📉 Performances négatives</div>
        <div class="metric-value negative">{neg} ({neg_p:.1f}%)</div>
        <div class="metric-subtitle">valeurs en baisse</div>
      </div>
    """, unsafe_allow_html=True)
with c4:
    st.markdown(f"""
      <div class="metric-container">
        <div class="metric-title">⚖️ Performances neutres</div>
        <div class="metric-value neutral">{neu} ({neu_p:.1f}%)</div>
        <div class="metric-subtitle">valeurs stables</div>
      </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown(create_footer(), unsafe_allow_html=True)