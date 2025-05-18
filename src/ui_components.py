import streamlit as st
import base64

# Appliquer le CSS personnalisé
def apply_custom_css():
    st.markdown(
        """
        <style>
            .stApp {
                background-color: #ffffff;
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
                font-size: 18px;
                line-height: 1.6;
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
        </style>
        """,
        unsafe_allow_html=True
    )

# Créer le bandeau défilant
def create_scrolling_ticker(portfolio_df, stock_data_dict, currency_mapping):
    # Générer le contenu HTML pour le bandeau défilant
    ticker_items = ""

    for _, row in portfolio_df.iterrows():
        stock_data = stock_data_dict.get(row['Ticker'], {})
        ticker = row['Ticker']
        currency = currency_mapping.get(ticker, "$")  # Utiliser la devise correspondante

        # Déterminer la classe CSS et flèche en fonction de la variation
        if stock_data.get('change', 0) >= 0:
            change_class = "positive"
            arrow = '<span style="font-size: 22px;">&#x25B2;</span>'  # triangle haut
        else:
            change_class = "negative"
            arrow = '<span style="font-size: 22px;">&#x25BC;</span>'  # triangle bas

        # Ajouter les informations de cette action au bandeau
        ticker_items += f"""
        <div class="ticker-item">
            <span class="ticker-name">{row['Société']}</span>
            <span class="ticker-price">{currency}{stock_data.get('current_price', 0):.2f}</span>
            <span class="ticker-change {change_class}">{arrow} {stock_data.get('percent_change', 0):.2f}%</span>
        </div>
        """

    # Code HTML complet pour le bandeau défilant
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
                padding: 12px 0;
            }}
            .ticker-tape {{
                display: inline-block;
                animation: ticker-scroll 80s linear infinite;
                padding-left: 100%;
            }}
            .ticker-item {{
                display: inline-block;
                padding: 0 50px;
                color: white;
                font-size: 18px;
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

    # Encodage en base64 pour l'iframe
    b64 = base64.b64encode(html_content.encode("utf-8")).decode("utf-8")
    iframe_html = (
        f'<iframe src="data:text/html;base64,{b64}" width="100%" height="52px" '
        'frameborder="0" scrolling="no"></iframe>'
    )
    return iframe_html

# Créer les titres formatés
def create_title(title_text):
    return f"<h1 style='font-size: 32px; margin-bottom: 10px;'>{title_text}</h1>"

# Créer une carte métrique
def create_metric_card(title, value, subtitle, is_currency=False, currency="€", is_percentage=False, positive_color=False):
    # Formatage de la valeur
    if is_percentage:
        formatted_value = f"{value:+.2f}%" if isinstance(value, (int, float)) else value
        color_class = "positive" if value >= 0 else "negative"
    elif is_currency:
        formatted_value = f"{currency}{value:,}".replace(",", " ")
        color_class = "positive" if positive_color and value >= 0 else "negative" if positive_color and value < 0 else "neutral"
    else:
        formatted_value = f"{value:,}".replace(",", " ") if isinstance(value, (int, float)) else value
        color_class = "neutral"
    
    return f"""
    <div class="metric-container">
        <div class="metric-title">{title}</div>
        <div class="metric-value {color_class}">{formatted_value}</div>
        <div class="metric-subtitle">{subtitle}</div>
    </div>
    """

# Créer le pied de page
def create_footer():
    return """
    <div style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #666;">
        <p>Komorebi Investments © 2025 - Analyse de Portefeuille</p>
        <p style="font-size: 12px; margin-top: 10px;">
            Les informations présentées ne constituent en aucun cas un conseil d'investissement, ni une sollicitation
            à acheter ou vendre des instruments financiers. L'investisseur est seul responsable de ses décisions
            d'investissement.
        </p>
    </div>
    """