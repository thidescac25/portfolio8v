import streamlit as st
from PIL import Image
import os
import yfinance as yf
from datetime import datetime
import base64
from io import BytesIO

# Configuration de la page
st.set_page_config(
    page_title="Fiche d'Investissement - Rolls-Royce Holdings plc",
    page_icon="📊",
    layout="wide"
)

# CSS personnalisé pour reproduire le style de la fiche HTML
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    
    .stButton > button {
        width: 100%;
    }
    
    .header-container {
        text-align: center;
        padding-bottom: 20px;
        margin-bottom: 30px;
    }
    
    .company-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1e3a8a;
        margin: 10px 0;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #64748b;
        margin-bottom: 20px;
    }
    
    .recommendation-box {
        background: linear-gradient(135deg, #22c55e, #16a34a);
        color: white;
        padding: 30px;
        border-radius: 10px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .recommendation-box h2 {
        margin: 0 0 10px 0;
        font-size: 2rem;
    }
    
    .unity-contract {
        background: linear-gradient(135deg, #5D4037, #8D6E63);
        color: white;
        padding: 25px;
        border-radius: 10px;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .metric-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        height: 100%;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #1e3a8a;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #64748b;
        margin-top: 5px;
    }
    
    .positive {
        color: #16a34a;
        font-weight: bold;
    }
    
    .section-header {
        color: #1e3a8a;
        border-bottom: 2px solid #8d6e63;
        padding-bottom: 10px;
        font-size: 1.1rem;
        margin-top: 30px;
        margin-bottom: 20px;
        font-weight: bold;
    }
    
    .division-card {
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 20px;
        background: #fafbfc;
        height: 100%;
    }
    
    .division-header {
        background: #1e3a8a;
        color: white;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 15px;
        font-weight: bold;
        text-align: center;
    }
    
    .division-header-green {
        background: #16a34a;
        color: white;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 15px;
        font-weight: bold;
        text-align: center;
    }
    
    .division-header-brown {
        background: #5D4037;
        color: white;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 15px;
        font-weight: bold;
        text-align: center;
    }
    
    .catalyst-item {
        background: #f0f9ff;
        border-left: 3px solid #8d6e63;
        padding: 15px;
        margin: 10px 0;
        border-radius: 3px;
    }
    
    .new-development {
        background: linear-gradient(135deg, #1e3a8a, #3b82f6);
        color: white;
        padding: 20px;
        margin: 15px 0;
        border-radius: 8px;
    }
    
    .strengths {
        background: #f0f9ff;
        border-left: 4px solid #22c55e;
        padding: 20px;
        border-radius: 5px;
    }
    
    .weaknesses {
        background: #fef2f2;
        border-left: 4px solid #ef4444;
        padding: 20px;
        border-radius: 5px;
    }
    
    .final-recommendation {
        text-align: center;
        background: #22c55e;
        color: white;
        padding: 30px;
        border-radius: 10px;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 30px 0;
    }
    
    table {
        width: 100%;
        margin: 15px 0;
    }
    
    th {
        background: #f1f5f9;
        color: #1e3a8a;
        padding: 10px;
        text-align: center;
        font-weight: bold;
    }
    
    td {
        padding: 10px;
        border-bottom: 1px solid #e2e8f0;
        text-align: center;
    }
    
    .centered-logo {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Titre de la page avec (page 3/3) en gras
st.markdown("""
<div style="text-align: center; margin-bottom: 20px;">
    <h2>Fiche Investissement Valeur - Analyse mai 2025 <span style="font-size: 0.6em; font-weight: bold;">(page 3/3)</span></h2>
</div>
""", unsafe_allow_html=True)

# Séparateur marron foncé
st.markdown('<hr style="height:2px;border:none;color:#5D4037;background-color:#5D4037;" />', unsafe_allow_html=True)

# Header avec logo centré
st.markdown("""
<div class="centered-logo">
""", unsafe_allow_html=True)

try:
    logo_image = Image.open("images/rolls.png")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image(logo_image, width=150)
except FileNotFoundError:
    # Fallback si l'image n'est pas trouvée - logo centré
    logo_html = """
    <div style="display: flex; justify-content: center; margin-bottom: 20px;">
        <div style="width: 150px; height: 90px; background-color: #0033A0; border-radius: 15px; display: flex; flex-direction: column; justify-content: center; align-items: center; border: 3px solid white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <div style="color: white; font-size: 1.2rem; font-weight: bold; letter-spacing: 3px; margin-bottom: 5px;">ROLLS</div>
            <div style="background-color: white; width: 80%; height: 30px; display: flex; justify-content: center; align-items: center; margin: 5px 0;">
                <span style="color: #0033A0; font-size: 2rem; font-weight: bold;">RR</span>
            </div>
            <div style="color: white; font-size: 1.2rem; font-weight: bold; letter-spacing: 3px; margin-top: 5px;">ROYCE</div>
        </div>
    </div>
    """
    st.markdown(logo_html, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center;">
    <div class="company-title">ROLLS-ROYCE HOLDINGS PLC</div>
    <div style="font-size: 0.9rem; color: #64748b; text-align: center;">Ticker: RR.L (Londres) | RYCEY (NYSE ADR)</div>
</div>
""", unsafe_allow_html=True)

# Recommandation principale
st.markdown("""
<div class="recommendation-box">
    <h2>🎯 RECOMMANDATION : ACHAT</h2>
    <div style="font-size: 1.3rem;">Objectif révisé 12-18 mois : 1000-1200p (+25-50%)</div>
</div>
""", unsafe_allow_html=True)

# Contrat Unity
st.markdown("""
<div class="unity-contract">
    <h2 style="color: white; margin-top: 0;">🛡️ Contrat "UNITY" – Record Historique de £9 Milliards</h2>
    <table style="width:80%; margin: 0 auto; color:white; text-align: center;">
        <tr>
            <th style="width:20%; text-align: center; background-color: #F5F5DC;">Élément</th>
            <th style="text-align: center; background-color: #F5F5DC; color: #5D4037;">Détail</th>
        </tr>
        <tr>
            <td>💼 <strong>Montant</strong></td>
            <td>Plus important contrat de défense jamais signé au Royaume-Uni : <strong>£9 Mrd sur 8 ans</strong></td>
        </tr>
        <tr>
            <td>🏛️ <strong>Client</strong></td>
            <td>Ministère britannique de la Défense (MoD)</td>
        </tr>
        <tr>
            <td>☢️ <strong>Objet</strong></td>
            <td>Conception, production et maintenance des <strong>réacteurs nucléaires pour sous-marins</strong></td>
        </tr>
        <tr>
            <td>👷 <strong>Impact emploi</strong></td>
            <td><strong>5 000 emplois créés ou sécurisés</strong>, principalement à Derby et Sheffield</td>
        </tr>
        <tr>
            <td>💰 <strong>Économies publiques</strong></td>
            <td><strong>£400 millions d'économies pour le contribuable</strong> grâce à la rationalisation du programme</td>
        </tr>
        <tr>
            <td>🛡️ <strong>Programmes concernés</strong></td>
            <td><strong>Classe Dreadnought</strong> (SNLE) + <strong>SSN-AUKUS</strong> (sous-marins d'attaque nouvelle génération)</td>
        </tr>
    </table>
</div>
""", unsafe_allow_html=True)

# Métriques clés avec cours actualisé - espace augmenté avant
st.markdown("<h3 style='text-align: center; margin: 50px 0 30px 0;'>Indicateurs Clés</h3>", unsafe_allow_html=True)

# Récupération du cours actuel avec yfinance
try:
    ticker = yf.Ticker("RR.L")
    current_price = ticker.info.get('currentPrice', None)
    if current_price is None:
        # Essayer avec regularMarketPrice
        current_price = ticker.info.get('regularMarketPrice', None)
    if current_price:
        current_price_str = f"{current_price:.0f}p"
    else:
        current_price_str = "N/A"
except:
    current_price_str = "N/A"

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">£65,67Mrd</div>
        <div class="metric-label">Capitalisation</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value positive">+57%</div>
        <div class="metric-label">Profit Opérationnel 2024</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">13,8%</div>
        <div class="metric-label">Marge Opérationnelle</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">£17,4Mrd</div>
        <div class="metric-label">Carnet commandes au 31 déc. 2024</div>
    </div>
    """, unsafe_allow_html=True)

# Section I - Présentation (titre réduit et espace augmenté)
st.markdown('<h4 class="section-header">I. PRÉSENTATION DE LA SOCIÉTÉ</h4>', unsafe_allow_html=True)

# Séparateur marron
st.markdown('<hr style="height:2px;border:none;color:#5D4037;background-color:#5D4037;" />', unsafe_allow_html=True)

st.info("**Positionnement :** 2ème fabricant mondial moteurs avions • 16ème contractant défense mondial • Leader mondial propulsion nucléaire navale")

# Tableau informations générales
st.markdown("""
<table>
    <tr>
        <th>Informations Générales</th>
        <th>Détails</th>
    </tr>
    <tr>
        <td><strong>Siège social</strong></td>
        <td>Londres, Royaume-Uni</td>
    </tr>
    <tr>
        <td><strong>Fondée</strong></td>
        <td>1904 (holding constituée en 2011)</td>
    </tr>
    <tr>
        <td><strong>Employés</strong></td>
        <td>~55 000 (dont 15 700 à Derby)</td>
    </tr>
    <tr>
        <td><strong>CEO</strong></td>
        <td>Tufan Erginbilgic (depuis janvier 2023)</td>
    </tr>
    <tr>
        <td><strong>Modèle économique</strong></td>
        <td>Power-by-the-Hour : Vente moteurs + maintenance long terme</td>
    </tr>
</table>
""", unsafe_allow_html=True)

# Séparateur marron
st.markdown('<hr style="height:2px;border:none;color:#5D4037;background-color:#5D4037;" />', unsafe_allow_html=True)

# Section II - Résultats financiers (titre réduit)
st.markdown('<h4 class="section-header">II. RÉSULTATS FINANCIERS 2024</h4>', unsafe_allow_html=True)

# Séparateur marron
st.markdown('<hr style="height:2px;border:none;color:#5D4037;background-color:#5D4037;" />', unsafe_allow_html=True)

st.markdown("""
<table>
    <tr>
        <th>Indicateur</th>
        <th>2024</th>
        <th>2023</th>
        <th>Variation</th>
    </tr>
    <tr>
        <td><strong>CA sous-jacent</strong></td>
        <td>£17,85 Mrd</td>
        <td>£15,41 Mrd</td>
        <td class="positive">+17%</td>
    </tr>
    <tr>
        <td><strong>Profit opérationnel</strong></td>
        <td>£2,46 Mrd</td>
        <td>£1,59 Mrd</td>
        <td class="positive">+57%</td>
    </tr>
    <tr>
        <td><strong>Marge opérationnelle</strong></td>
        <td>13,8%</td>
        <td>10,3%</td>
        <td class="positive">+3,5pts</td>
    </tr>
    <tr>
        <td><strong>Free Cash Flow</strong></td>
        <td>£2,43 Mrd</td>
        <td>£1,29 Mrd</td>
        <td class="positive">+88%</td>
    </tr>
    <tr>
        <td><strong>Position nette de trésorerie</strong></td>
        <td>£475M</td>
        <td>-£1,95 Mrd</td>
        <td class="positive">+£2,43 Mrd</td>
    </tr>
</table>
""", unsafe_allow_html=True)

# Section III - Structure par divisions (titre réduit)
st.markdown('<h4 class="section-header">III. STRUCTURE PAR DIVISIONS</h4>', unsafe_allow_html=True)

# Encart Power-by-the-Hour corrigé - contenu HTML affiché correctement
st.markdown("""
<div style="background: #f8f4f1; border: 1px solid #5D4037; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
    <h3 style="color: #5D4037; margin-top: 0;">🔄 "Power-by-the-Hour" : le modèle économique de Rolls-Royce</h3>
    <p>Rolls-Royce continue d'exploiter activement son modèle "Power-by-the-Hour" (PBH) en 2025. Ce concept, introduit en 1962, est désormais intégré dans ses offres de services long terme, notamment via le programme <strong>TotalCare®</strong>, qui couvre plus de 4 000 moteurs en service.</p>
</div>
""", unsafe_allow_html=True)

# Tableaux Power-by-the-Hour affichés correctement
st.markdown("""
<h4 style="color: #5D4037;">✅ Avantages du modèle Power-by-the-Hour</h4>
<table style="width:100%;">
    <tr>
        <th style="width:50%;">Pour les compagnies aériennes</th>
        <th style="width:50%;">Pour Rolls-Royce</th>
    </tr>
    <tr>
        <td>🔹 <strong>Prévisibilité budgétaire</strong> : Coûts de maintenance fixes par heure de vol, facilitant la planification financière.</td>
        <td>🔹 <strong>Revenus récurrents</strong> : Génère des flux de trésorerie stables sur la durée de vie des moteurs.</td>
    </tr>
    <tr>
        <td>🔹 <strong>Réduction des immobilisations</strong> : Moins de besoins en stocks de pièces détachées et en infrastructures de maintenance.</td>
        <td>🔹 <strong>Fidélisation client</strong> : Renforce les relations à long terme avec les opérateurs.</td>
    </tr>
    <tr>
        <td>🔹 <strong>Disponibilité accrue des appareils</strong> : Maintenance proactive assurée par Rolls-Royce, réduisant les temps d'arrêt.</td>
        <td>🔹 <strong>Collecte de données</strong> : Accès aux données opérationnelles pour améliorer la performance des moteurs.</td>
    </tr>
</table>

<h4 style="color: #5D4037; margin-top: 15px;">⚠️ Inconvénients du modèle Power-by-the-Hour</h4>
<table style="width:100%;">
    <tr>
        <th style="width:50%;">Pour les compagnies aériennes</th>
        <th style="width:50%;">Pour Rolls-Royce</th>
    </tr>
    <tr>
        <td>🔸 <strong>Coût total potentiellement plus élevé</strong> : Sur le long terme, les frais cumulés peuvent dépasser ceux d'une maintenance à la demande.</td>
        <td>🔸 <strong>Risque financier accru</strong> : En cas de baisse des heures de vol (ex. pandémie), les revenus diminuent, mais les coûts fixes subsistent.</td>
    </tr>
    <tr>
        <td>🔸 <strong>Moins de flexibilité</strong> : Engagements contractuels à long terme pouvant limiter les options de maintenance alternatives.</td>
        <td>🔸 <strong>Responsabilité accrue</strong> : Obligation de maintenir des niveaux de performance élevés pour éviter des pénalités contractuelles.</td>
    </tr>
</table>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="division-card">
        <div class="division-header">🛩️ CIVIL AEROSPACE (51% CA)</div>
        <strong>Revenus 2024 :</strong> £9,04 Mrd (+24%)<br>
        <strong>Marge :</strong> 16,6% (vs 11,6% en 2023)<br>
        <strong>Catalyseur UltraFan :</strong> Tests pleine puissance réussis 100% SAF<br>
        <strong>Innovation :</strong> +10% d'efficacité vs Trent XWB, architecture à réducteur unique
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="division-card" style="margin-top: 20px;">
        <div class="division-header-brown">⚡ POWER SYSTEMS (24% CA)</div>
        <strong>Revenus 2024 :</strong> £4,27 Mrd (+11%)<br>
        <strong>H1 2024 :</strong> +56% profit opérationnel (€222M)<br>
        <strong>Boom Data Centers :</strong> +42% croissance équipements IA<br>
        <strong>BESS (systèmes de stockage d'énergie par batteries) :</strong> Contrats majeurs EU (Lettonie, Pays-Bas)
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="division-card">
        <div class="division-header">🛡️ DEFENCE (25% CA)</div>
        <strong>Revenus 2024 :</strong> £4,52 Mrd (+13%)<br>
        <strong>Contrat Unity :</strong> £9 Mrd sur 8 ans (plus gros contrat de l'histoire de RR)<br>
        <strong>Programmes :</strong> AUKUS, Dreadnought, propulsion nucléaire<br>
        <strong>Carnet :</strong> £17,4 Mrd record historique
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="division-card" style="margin-top: 20px;">
        <div class="division-header-green">🔬 SMR & NEW MARKETS</div>
        <strong>SMR 470 MWe :</strong> 18 mois d'avance vs concurrents EU<br>
        <strong>ČEZ Partnership :</strong> ČEZ a acquis une participation de 20 % dans Rolls-Royce SMR, 3 GWe République Tchèque<br>
        <strong>Siemens Energy :</strong> Partenariat exclusif turbines<br>
        <strong>Space Tech :</strong> £4,8M de financement par l'UK Space Agency pour des microréacteurs spatiaux
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="new-development">
    <strong>🚀 Développements Breakthrough 2024-2025 :</strong> Contrat Unity record, SMR commercialisation ČEZ, UltraFan validation, boom BESS data centers, propulsion spatiale nucléaire - évolution technologique et commerciale confirmée toutes divisions.
</div>
""", unsafe_allow_html=True)

# Séparateur marron
st.markdown('<hr style="height:2px;border:none;color:#5D4037;background-color:#5D4037;" />', unsafe_allow_html=True)

# Section IV - Guidance (titre réduit)
st.markdown('<h4 class="section-header">IV. GUIDANCE 2025 & OBJECTIFS MID-TERM RELEVÉS</h4>', unsafe_allow_html=True)

# Séparateur marron
st.markdown('<hr style="height:2px;border:none;color:#5D4037;background-color:#5D4037;" />', unsafe_allow_html=True)

st.markdown("### 🎯 Guidance 2025 (confirmée)")
st.markdown("""
- **Profit opérationnel :** £2,7-2,9 Mrd
- **Free Cash Flow :** £2,7-2,9 Mrd
- **Objectifs mid-term atteints avec 2 ans d'avance**
""")

st.markdown("### 📈 Nouvelle Guidance Mid-term (2028) - RELEVÉE")
st.markdown("""
<table>
    <tr>
        <th>Indicateur</th>
        <th>Nouveaux Objectifs 2028</th>
        <th>Anciens Objectifs 2027</th>
    </tr>
    <tr>
        <td><strong>Profit opérationnel</strong></td>
        <td>£3,6-3,9 Mrd</td>
        <td>£2,5-2,8 Mrd</td>
    </tr>
    <tr>
        <td><strong>Marge opérationnelle</strong></td>
        <td>15-17%</td>
        <td>13-15%</td>
    </tr>
    <tr>
        <td><strong>Free Cash Flow</strong></td>
        <td>£4,2-4,5 Mrd</td>
        <td>£2,8-3,1 Mrd</td>
    </tr>
    <tr>
        <td><strong>Return on Capital</strong></td>
        <td>18-21%</td>
        <td>16-18%</td>
    </tr>
</table>
""", unsafe_allow_html=True)

# Séparateur marron
st.markdown('<hr style="height:2px;border:none;color:#5D4037;background-color:#5D4037;" />', unsafe_allow_html=True)

# Section V - Innovations technologiques (titre réduit)
st.markdown('<h4 class="section-header">V. INNOVATIONS TECHNOLOGIQUES</h4>', unsafe_allow_html=True)

# Séparateur marron
st.markdown('<hr style="height:2px;border:none;color:#5D4037;background-color:#5D4037;" />', unsafe_allow_html=True)

st.markdown("### 🤖 Programme IntelligentEngine - Robotique Avancée")

st.markdown("""
<div class="catalyst-item">
    <strong>Robots SWARM :</strong> Robots miniatures 10mm déployés commercialement, inspection moteurs 5 min vs 5h actuellement
</div>
<div class="catalyst-item">
    <strong>Robots INSPECT :</strong> Périscopes embarqués permanents pour auto-inspection continue et maintenance prédictive
</div>
<div class="catalyst-item">
    <strong>Robots Boreblending :</strong> Réparation laser à distance opérationnelle chez clients VIP, économies 80% maintenance
</div>
""", unsafe_allow_html=True)

st.markdown("### 🔬 Intelligence Artificielle & Digital Twin")

st.markdown("""
<div class="catalyst-item">
    <strong>R2 Data Labs :</strong> Hub d'innovation dédié à l'IA industrielle qui développe des applications permettant d'optimiser la conception, la fabrication et les opérations à travers toutes les divisions de Rolls-Royce
</div>
<div class="catalyst-item">
    <strong>Partenariat Altair :</strong> Collaboration stratégique utilisant l'IA pour analyser les données massives de tests et simulations, permettant des économies de millions d'euros sur les coûts de capteurs et de certification
</div>
<div class="catalyst-item">
    <strong>Aerogility AI :</strong> Contrat de 5 ans pour l'utilisation de jumeaux numériques basés sur l'IA permettant des prévisions avancées et une planification stratégique de la maintenance
</div>
""", unsafe_allow_html=True)

# Séparateur marron
st.markdown('<hr style="height:2px;border:none;color:#5D4037;background-color:#5D4037;" />', unsafe_allow_html=True)

# Section VI - UltraFan (titre réduit)
st.markdown('<h4 class="section-header">VI. ULTRAFAN - ÉVOLUTION TECHNOLOGIQUE VALIDÉE</h4>', unsafe_allow_html=True)

# Séparateur marron
st.markdown('<hr style="height:2px;border:none;color:#5D4037;background-color:#5D4037;" />', unsafe_allow_html=True)

st.markdown("""
<div class="new-development">
    <strong>🔥 Tests Pleine Puissance Réussis :</strong> UltraFan testé à puissance maximale avec 100% SAF en novembre 2023, confirmant +10% d'efficacité vs Trent XWB. Architecture à réducteur unique : la gearbox de l'UltraFan permet au ventilateur de tourner plus lentement que la turbine, optimisant l'efficacité aérodynamique et la consommation de carburant, avec une puissance record mondiale de 50 MW.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<table>
    <tr>
        <th>Caractéristique UltraFan</th>
        <th>Détail Technique</th>
        <th>Avantage Concurrentiel</th>
    </tr>
    <tr>
        <td><strong>Efficacité énergétique</strong></td>
        <td>+10 % par rapport au moteur Trent XWB</td>
        <td class="positive">Meilleur rendement mondial en consommation de carburant</td>
    </tr>
    <tr>
        <td><strong>Diamètre du ventilateur</strong></td>
        <td>140 pouces</td>
        <td>6 pouces de plus que le GE9X → plus grande poussée</td>
    </tr>
    <tr>
        <td><strong>Boîte de vitesses (gearbox)</strong></td>
        <td>Puissance record de 50 MW</td>
        <td class="positive">Technologie exclusive optimisant performance moteur</td>
    </tr>
    <tr>
        <td><strong>Capacité de modulation (scaling)</strong></td>
        <td>Plage de poussée : 25 000 à 110 000 lb</td>
        <td>UltraFlexibilité pour court, moyen et long-courrier</td>
    </tr>
</table>
""", unsafe_allow_html=True)

# Séparateur marron
st.markdown('<hr style="height:2px;border:none;color:#5D4037;background-color:#5D4037;" />', unsafe_allow_html=True)

# Section VII - SMR (titre réduit)
st.markdown('<h4 class="section-header">VII. SMR - PERCÉES COMMERCIALES MAJEURES</h4>', unsafe_allow_html=True)

st.markdown("""
<h3>🔋 SMR – Partenariats Commerciaux Stratégiques</h3>

<div class="division-card">
    <div class="division-header-green">🇨🇿 Partenariat stratégique avec ČEZ</div>
    <ul>
        <li><strong>Participation au capital</strong> : ČEZ prend une <strong>participation de 20 %</strong> dans Rolls-Royce SMR (investissement estimé à plusieurs centaines de millions de livres sterling).</li>
        <li><strong>Déploiement initial</strong> : Objectif de <strong>3 GWe installés</strong> en République Tchèque à l'horizon <strong>2030</strong>.</li>
        <li><strong>Démarrage opérationnel</strong> : <strong>Travaux préparatoires dès 2025</strong>.</li>
        <li><strong>Ambition continentale</strong> : Le partenariat vise à <strong>soutenir le déploiement des SMR dans toute l'Europe</strong>, avec la République Tchèque comme base pilote.</li>
    </ul>
</div>

<div class="division-card" style="margin-top: 20px;">
    <div class="division-header-green">⚙️ Accord exclusif avec Siemens Energy</div>
    <ul>
        <li><strong>Rôle</strong> : Fournisseur <strong>exclusif des turbines vapeur</strong> pour tous les SMR Rolls-Royce à venir.</li>
        <li><strong>Portée</strong> : Accord couvrant <strong>l'ensemble des futurs projets SMR</strong>.</li>
        <li><strong>Échéance</strong> : Signature du <strong>contrat final attendue fin 2025</strong>.</li>
        <li><strong>Portée stratégique</strong> : Renforcement de la chaîne industrielle avec un <strong>partenaire mondial de premier plan</strong>.</li>
    </ul>
</div>

<div class="division-card" style="margin-top: 20px;">
    <div class="division-header-brown">🛡️ Avantage réglementaire et industriel</div>
    <ul>
        <li><strong>Avance réglementaire</strong> : Rolls-Royce SMR dispose de <strong>18 mois d'avance sur tous ses concurrents européens</strong>.</li>
        <li><strong>Certification</strong> : Déjà en <strong>phase 3 du UK GDA (Generic Design Assessment)</strong>.</li>
        <li><strong>Infrastructure clé</strong> : Une <strong>usine pilote opérationnelle à Sheffield</strong> produit les composants des prototypes SMR.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Section VIII - Propulsion spatiale (titre réduit)
st.markdown('<h4 class="section-header">VIII. PROPULSION SPATIALE - INNOVATION BREAKTHROUGH</h4>', unsafe_allow_html=True)

# Séparateur marron
st.markdown('<hr style="height:2px;border:none;color:#5D4037;background-color:#5D4037;" />', unsafe_allow_html=True)

st.markdown("""
<div class="new-development">
    <strong>🚀 Microréacteurs Nucléaires Spatiaux :</strong> £4,8M de financement par l'UK Space Agency pour des microréacteurs spatiaux (total £9,1M). Partenaires Oxford + Bangor Universities. Démonstration vol spatial fin décennie. Applications : propulsion satellites, bases lunaires.
</div>
""", unsafe_allow_html=True)

# Séparateur marron
st.markdown('<hr style="height:2px;border:none;color:#5D4037;background-color:#5D4037;" />', unsafe_allow_html=True)

# Section IX - Power Systems (titre réduit)
st.markdown('<h4 class="section-header">IX. POWER SYSTEMS - EXPLOSION BESS & DATA CENTERS</h4>', unsafe_allow_html=True)

# Séparateur marron
st.markdown('<hr style="height:2px;border:none;color:#5D4037;background-color:#5D4037;" />', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value positive">+56%</div>
        <div class="metric-label">Profit Op H1 2024</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">10,3%</div>
        <div class="metric-label">Marge Opérationnelle</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value positive">+42%</div>
        <div class="metric-label">Croissance Data Centers</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">64%</div>
        <div class="metric-label">Cash Conversion</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("### 🔋 BESS - Projets Majeurs Confirmés")
st.markdown("""
- **Lettonie :** Un des plus gros BESS Union Européenne
- **Pays-Bas Castor :** 62,6 MWh (plus gros du pays)
- **Pays-Bas Zeewolde :** 65,2 MWh operational été 2025
- **Allemagne :** Projets multiples intégration renouvelables
""")

# Section X - Catalyseurs (titre réduit)
st.markdown('<h4 class="section-header">X. 🔋 Catalyseurs de Croissance Confirmés</h4>', unsafe_allow_html=True)

# Séparateur marron
st.markdown('<hr style="height:2px;border:none;color:#5D4037;background-color:#5D4037;" />', unsafe_allow_html=True)

st.markdown("""
<h3>🚀 Transformation Accélérée (2022–2024)</h3>
<ul>
   <li><strong>Leadership Tufan Erginbilgic</strong> : transformation « One Rolls-Royce » réussie, objectifs 2027 atteints <strong>2 ans en avance</strong>.</li>
   <li><strong>+700 % de progression de l'action</strong> depuis janvier 2023, reflet d'un repositionnement stratégique et opérationnel réussi.</li>
</ul>

<h3>📈 Leviers Stratégiques Clés</h3>
<ul>
   <li><strong>Défense</strong> : contrat Unity (£9 Mrd, 8 ans de revenus sécurisés), soutien géopolitique renforcé via AUKUS.</li>
   <li><strong>Net Zero</strong> : UltraFan (+10 % d'efficacité, 100 % SAF), SMR en phase avancée (partenariats ČEZ + Siemens, avance réglementaire).</li>
   <li><strong>Power Systems / Data Centers</strong> : croissance rapide du besoin énergétique → déploiement de BESS (Lettonie, Pays-Bas).</li>
   <li><strong>Espace</strong> : développement de microréacteurs nucléaires (financement total £9,1M, Oxford + Bangor), avec applications satellites, bases lunaires.</li>
   <li><strong>Technologies différenciantes</strong> : gearbox UltraFan (50 MW), robots SWARM, maintenance IA → <strong>barrières à l'entrée technologiques élevées</strong>.</li>
</ul>

<div style="display: flex; gap: 20px; margin-top: 20px;">
    <div style="flex: 1;">
        <div class="strengths">
            <h3>🟢 Forces Consolidées</h3>
            <ul>
                <li>Revenus récurrents sécurisés sur plusieurs années</li>
                <li>Avancées probantes réglementaires et technologiques sur les SMR</li>
                <li>Positionnement clair sur toutes les mégatendances : défense, Net Zero, data, espace</li>
                <li>Écosystème de partenariats industriels stratégiques</li>
            </ul>
        </div>
    </div>
    <div style="flex: 1;">
        <div class="weaknesses">
            <h3>🔶 Points de Vigilance</h3>
            <ul>
                <li>Complexité de gestion multi-programmes (SMR, UltraFan, spatial)</li>
                <li>Dépendance à la chaîne d'approvisionnement (en atténuation via robotisation)</li>
                <li>Longs cycles de développement (notamment pour nucléaire et spatial)</li>
                <li>Concurrence active sur les segments historiques</li>
                <li>Pression potentielle sur les coûts de transition énergétique</li>
            </ul>
        </div>
    </div>
</div>

<div style="background: linear-gradient(135deg, #1e3a8a, #3b82f6); color: white; padding: 25px; border-radius: 10px; margin: 20px 0;">
    <h3 style="color: white; margin-top: 0;">✅ Conclusion</h3>
    <p>Rolls-Royce Holdings entre dans une <strong>phase de réaccélération durable</strong>, tirée par des <strong>leviers technologiques, commerciaux et géopolitiques convergents</strong>. La combinaison d'un modèle d'affaires récurrent, d'un leadership technologique consolidé et d'une exécution stratégique maîtrisée confère à Rolls-Royce un positionnement de croissance robuste parmi les leaders industriels européens.</p>
</div>
""", unsafe_allow_html=True)

# RECOMMANDATION sans "FINALE"
st.markdown("""
<div class="final-recommendation">
    RECOMMANDATION : ACHAT
    <br><span style="font-size: 1.2rem;">Objectif 12-18 mois : 1000-1200p (+25-50%)</span>
    <br><span style="font-size: 1rem; font-style: italic;">Transformation + Innovation + Contrats stratégiques = Potentiel validé</span>
</div>
""", unsafe_allow_html=True)

# Footer avec disclaimer et séparateur marron
st.markdown('<hr style="height:2px;border:none;color:#5D4037;background-color:#5D4037;" />', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; font-size: 0.9rem; color: #6b7280; margin-top: 30px;">
    <strong>Fiche réalisée le 23 mai 2025</strong>
    <br><br>
    Komorebi Investments © 2025 - Analyse de Portefeuille<br>
    <em>Les informations présentées ne constituent en aucun cas un conseil d'investissement, ni une sollicitation à acheter ou vendre des instruments financiers. L'investisseur est seul responsable de ses décisions d'investissement.</em>
</div>
""", unsafe_allow_html=True)