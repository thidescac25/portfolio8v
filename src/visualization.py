import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import streamlit as st
import numpy as np
from datetime import datetime

# Créer le tableau du portefeuille avec hauteur fixe - VERSION CORRIGÉE
def create_portfolio_table(comp_df):
    # Fonction pour déterminer la couleur du fond en fonction de la variation
    def get_bg_color(val):
        if val > 0:
            return "#9CAF88"  # Vert olive clair pour les valeurs positives
        elif val < 0:
            return "#C8AD7F"  # Beige ambré pour les valeurs négatives
        else:
            return "#DBDBCE"  # Beige grisé clair pour les valeurs neutres

    # Créer des valeurs pour les cellules formatées avec texte en gras
    index_vals = [f"<b>{i}</b>" for i in range(1, len(comp_df) + 1)]
    society_vals = [f"<b>{val}</b>" for val in comp_df['Société']]
    price_vals = [f"<b>{val:.2f}</b>" for val in comp_df['Prix']]
    device_vals = [f"<b>{val}</b>" for val in comp_df['Devise']]
    sector_vals = [f"<b>{val}</b>" for val in comp_df['Secteur']]
    country_vals = [f"<b>{val}</b>" for val in comp_df['Pays']]

    # Préparer les valeurs de variation formatées et les couleurs de fond
    variation_vals = []
    bg_colors = []

    for val in comp_df["Variation (%) du jour"]:
        if val > 0:
            variation_vals.append(f"<b>+{val:.2f}%</b>")
        else:
            variation_vals.append(f"<b>{val:.2f}%</b>")
        bg_colors.append(get_bg_color(val))

    # Créer le tableau avec l'ordre des colonnes modifié et le gradient de couleur pour la variation
    fig = go.Figure()

    # Ajouter le tableau principal avec le nouvel ordre des colonnes
    fig.add_trace(go.Table(
        columnwidth=[40, 200, 120, 80, 60, 150, 120],  # Élargir la colonne Société
        header=dict(
            values=[
                '<b>Index</b>', 
                '<b>Société</b>',
                '<b>Variation du jour (%)</b>',
                '<b>Prix</b>',
                '<b>Devise</b>', 
                '<b>Secteur</b>', 
                '<b>Pays</b>'
            ],
            font=dict(size=14, color='white'),
            fill_color='#693112',  # Marron foncé pour les en-têtes
            align=['center', 'center', 'center', 'center', 'center', 'center', 'center'],
            height=40,
            line_color='lightgrey',  # NOUVEAU : Couleur des bordures header
            line_width=1             # NOUVEAU : Épaisseur des bordures header
        ),
        cells=dict(
            values=[
                index_vals, 
                society_vals,
                variation_vals,
                price_vals,
                device_vals,
                sector_vals,
                country_vals
            ],
            font=dict(size=13, color='#102040', family="Arial"),  # Texte en bleu foncé et en gras
            fill_color=[
                'white', 
                'white',
                bg_colors,  # Appliquer les couleurs de fond pour la colonne variation
                'white',
                'white', 
                'white', 
                'white'
            ],
            align=['center', 'left', 'center', 'center', 'center', 'center', 'center'],
            line_color='lightgrey',  # Légère bordure entre les cellules
            line_width=1,            # NOUVEAU : Épaisseur des bordures cellules
            height=30
        )
    ))

    # Calculer la hauteur exacte pour afficher toutes les lignes
    table_height = 40 + (len(comp_df) * 30) + 10

    # Ajuster la mise en page
    fig.update_layout(
        margin=dict(l=5, r=5, t=5, b=5),
        height=table_height,
        autosize=False
    )
    
    return fig, table_height

# Créer le graphique d'une action
def create_stock_chart(hist, ticker, currency, period_selection):
    # Filtrer l'historique selon la période sélectionnée
    if period_selection == "1 mois":
        filtered_hist = hist.iloc[-30:]
    elif period_selection == "6 mois":
        filtered_hist = hist.iloc[-180:]
    else:  # 1 an
        filtered_hist = hist

    # Calculer les statistiques
    avg_price = filtered_hist['Close'].mean()
    max_price = filtered_hist['Close'].max()
    min_price = filtered_hist['Close'].min()

    # Créer le graphique
    fig = go.Figure()
    
    # Ajouter la courbe de prix
    fig.add_trace(
        go.Scatter(
            x=filtered_hist.index,
            y=filtered_hist['Close'],
            mode='lines',
            name='Prix',
            line=dict(color='#693112', width=2)
        )
    )
    
    # Ajouter le volume en barres
    if 'Volume' in filtered_hist.columns:
        volume_scale = filtered_hist['Volume'] / filtered_hist['Volume'].max() * filtered_hist['Close'].min() * 0.2
        fig.add_trace(
            go.Bar(
                x=filtered_hist.index,
                y=volume_scale,
                marker_color='rgba(105, 49, 18, 0.2)',
                name='Volume',
                yaxis='y2'
            )
        )
    
    # Mise en page du graphique
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
    
    return fig, avg_price, max_price, min_price

# Tracer les performances comparées
def plot_performance(hist_data, weights=None, reference_indices=None, end_date_ui=None, force_start_date=None):
    if not hist_data:
        return None

    if weights is None:
        weights = [1/len(hist_data)] * len(hist_data)

    start_dates = []
    end_dates = []

    for ticker, hist in hist_data.items():
        if not hist.empty:
            start_dates.append(hist.index[0])
            end_dates.append(hist.index[-1])

    if not start_dates or not end_dates:
        return None

    start_dt = force_start_date or max(start_dates)
    end_dt = end_date_ui or max(end_dates)

    fig = go.Figure()
    date_range = pd.date_range(start=start_dt, end=end_dt, freq='B')
    all_normalized = pd.DataFrame(index=date_range)
    portfolio_trace = None
    indices_traces = []

    for i, (ticker, hist) in enumerate(hist_data.items()):
        if hist.empty:
            continue
        filtered_hist = hist[(hist.index >= start_dt) & (hist.index <= end_dt)]
        if filtered_hist.empty:
            continue
        reindexed = filtered_hist['Close'].reindex(date_range, method='ffill')
        normalized = reindexed / reindexed.iloc[0] * 100
        all_normalized[ticker] = normalized

    if all_normalized.empty:
        return None

    portfolio_perf = pd.Series(0, index=date_range)
    if len(weights) < len(all_normalized.columns):
        weights = [1/len(all_normalized.columns)] * len(all_normalized.columns)

    for i, col in enumerate(all_normalized.columns):
        portfolio_perf += all_normalized[col] * weights[i]

    portfolio_trace = go.Scatter(
        x=portfolio_perf.index,
        y=portfolio_perf.values,
        mode='lines',
        name='Portefeuille',
        line=dict(width=3, color='#693112')
    )

    if reference_indices:
        import yfinance as yf
        for name, ticker in reference_indices.items():
            try:
                ref = yf.Ticker(ticker)
                ref_hist = ref.history(start=start_dt, end=end_dt)
                if not ref_hist.empty:
                    ref_hist.index = ref_hist.index.tz_localize(None)
                    ref_close = ref_hist['Close'].reindex(date_range, method='ffill')
                    ref_norm = ref_close / ref_close.iloc[0] * 100
                    indices_traces.append(go.Scatter(
                        x=ref_norm.index,
                        y=ref_norm.values,
                        mode='lines',
                        name=name,
                        line=dict(width=2.5, dash='dash')
                    ))
            except Exception as e:
                st.warning(f"Erreur lors de la récupération des données pour {name}: {str(e)}")

    fig.add_trace(portfolio_trace)
    for trace in indices_traces:
        fig.add_trace(trace)

    fig.update_layout(
        title="Performance Comparée (Base 100)",
        xaxis_title="Date",
        yaxis_title="Performance (%)",
        height=500,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    # Ajuster l'échelle Y
    y_vals = list(portfolio_trace.y) + sum([list(trace.y) for trace in indices_traces], [])
    if y_vals:
        min_y = max(min(y_vals) * 0.9, 0)
        max_y = min(max(y_vals) * 1.1, max(y_vals) * 1.5)
        reasonable_max = max(150, min(max_y, 300))
        fig.update_layout(yaxis=dict(range=[min_y, reasonable_max]))

    return fig

# Simuler l'évolution du portefeuille
def plot_portfolio_simulation(hist_data, initial_investment=1000000, end_date_ui=None, max_traces=15, force_start_date=None):
    if not hist_data:
        return None, 0, 0, 0, []
        
    start_dates = []
    end_dates = []

    for ticker, hist in hist_data.items():
        if not hist.empty:
            start_dates.append(hist.index[0])
            end_dates.append(hist.index[-1])

    if not start_dates or not end_dates:
        return None, 0, 0, 0, []

    start_dt = force_start_date or max(start_dates)
    end_dt = end_date_ui or max(end_dates)
    date_range = pd.date_range(start=start_dt, end=end_dt, freq='B')
    num_stocks = len(hist_data)
    invest_each = initial_investment / num_stocks

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
        num_shares = invest_each / initial_price
        stock_info.append({
            "ticker": ticker,
            "num_shares": num_shares,
            "initial_investment": invest_each
        })
        stock_value = reindexed * num_shares
        all_values[ticker] = stock_value
        
        # Limiter le nombre de traces individuelles pour une meilleure lisibilité
        if len(stock_info) <= max_traces:
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
    
    # Ligne d'investissement initial
    fig.add_shape(
        type="line",
        x0=start_dt,
        y0=initial_investment,
        x1=end_dt,
        y1=initial_investment,
        line=dict(color="black", width=2, dash="dash")
    )

    fig.update_layout(
        title=(
            f"Évolution d'un investissement de "
            f"{f'{initial_investment:_}'.replace('_', ' ')} € réparti équitablement"
        ),
        xaxis_title="Date",
        yaxis_title="Valeur (€)",
        height=500,
        template="plotly_white",
        showlegend=False
    )

    if not portfolio_value.empty:
        y_min = max(portfolio_value.min() * 0.9, 0)
        y_max = portfolio_value.max() * 1.1
        fig.update_layout(yaxis=dict(range=[y_min, y_max]))

    if portfolio_value.empty:
        final_val = initial_investment
        gain_loss = 0
        pct_change = 0
    else:
        final_val = portfolio_value.iloc[-1]
        gain_loss = final_val - initial_investment
        pct_change = (gain_loss / initial_investment) * 100

    return fig, final_val, gain_loss, pct_change, stock_info

# Calculer les statistiques du portefeuille
def calculate_portfolio_stats(hist_data, portfolio_df, start_date, end_date):
    df_perf = []
    
    # Pour chaque ticker dans les données historiques
    for ticker, hist in hist_data.items():
        if hist.empty:
            continue
            
        # Récupérer le nom de la société
        company_name = ticker
        company_row = portfolio_df[portfolio_df['Ticker'] == ticker]
        if not company_row.empty and 'Société' in company_row.columns:
            company_name = company_row.iloc[0]['Société']
            
        # Calculer la performance entre les dates
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

# Afficher les principaux contributeurs
def display_top_contributors(df_perf):
    if df_perf.empty:
        st.warning("Pas de données disponibles pour les contributeurs.")
        return
        
    st.markdown('<div class="section-title">Meilleurs et pires contributeurs</div>', unsafe_allow_html=True)
    
    # Trier pour obtenir les meilleurs et les pires
    df_sorted = df_perf.sort_values(by='Var. (%)', ascending=False)
    best = df_sorted.head(3)
    worst = df_sorted.tail(3)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h5>📈 Meilleures performances</h5>", unsafe_allow_html=True)
        for i, row in best.iterrows():
            st.markdown(f"""
            <div style="background-color:#f0f8f0; border-left:4px solid #28a745; padding:10px; margin:5px 0; border-radius:5px;">
                <div style="font-weight:bold;">{row['Société']}</div>
                <div style="display:flex; justify-content:space-between;">
                    <span>{row['Prix départ']:.2f} → {row['Prix final']:.2f}</span>
                    <span style="color:#28a745; font-weight:bold;">+{row['Var. (%)']:.2f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("<h5>📉 Moins bonnes performances</h5>", unsafe_allow_html=True)
        for i, row in worst.iterrows():
            color = "#dc3545" if row['Var. (%)'] < 0 else "#28a745"
            sign = "" if row['Var. (%)'] < 0 else "+"
            st.markdown(f"""
            <div style="background-color:#fff0f0; border-left:4px solid {color}; padding:10px; margin:5px 0; border-radius:5px;">
                <div style="font-weight:bold;">{row['Société']}</div>
                <div style="display:flex; justify-content:space-between;">
                    <span>{row['Prix départ']:.2f} → {row['Prix final']:.2f}</span>
                    <span style="color:{color}; font-weight:bold;">{sign}{row['Var. (%)']:.2f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Créer les graphiques à barres pour secteur et pays
def create_bar_charts(df_sc):
    # Graphique secteur
    sector_data = df_sc.groupby('Sector')['Weight'].sum().reset_index()
    sector_data = sector_data.sort_values('Weight', ascending=True)  # Pour les barres horizontales
    
    fig_sector = go.Figure()
    fig_sector.add_trace(go.Bar(
        y=sector_data['Sector'],
        x=sector_data['Weight'] * 100,  # Convertir en pourcentage
        orientation='h',
        marker=dict(color='#693112'),
        text=[f"{x:.1f}%" for x in sector_data['Weight'] * 100],
        textposition='auto'
    ))
    
    fig_sector.update_layout(
        title="Répartition Sectorielle",
        xaxis_title="Allocation (%)",
        yaxis_title="Secteur",
        height=450,
        margin=dict(l=10, r=10, t=40, b=10),
        template="plotly_white"
    )
    
    # Graphique pays
    country_data = df_sc.groupby('Country')['Weight'].sum().reset_index()
    country_data = country_data.sort_values('Weight', ascending=True)  # Pour les barres horizontales
    
    fig_geo = go.Figure()
    fig_geo.add_trace(go.Bar(
        y=country_data['Country'],
        x=country_data['Weight'] * 100,  # Convertir en pourcentage
        orientation='h',
        marker=dict(color='#102040'),
        text=[f"{x:.1f}%" for x in country_data['Weight'] * 100],
        textposition='auto'
    ))
    
    fig_geo.update_layout(
        title="Répartition Géographique",
        xaxis_title="Allocation (%)",
        yaxis_title="Pays",
        height=450,
        margin=dict(l=10, r=10, t=40, b=10),
        template="plotly_white"
    )
    
    return fig_sector, fig_geo