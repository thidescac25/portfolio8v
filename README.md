Komorebi Investments 10 Stocks

Application interactive de suivi et d’analyse d’un portefeuille international de 10 actions, développée avec Streamlit.

Cette version prolonge le projet initial "Komorebi Investments 8 Stocks" avec deux nouvelles valeurs majeures et une architecture de données modernisée.

🚀 Fonctionnalités principales

📈 Suivi en temps réel :
Bandeau défilant affichant les prix actuels et les variations instantanées des 10 valeurs.

💹 Analyse comparative :
Performance historique comparée à plusieurs indices de référence (CAC 40, S&P 500, etc.).

💰 Simulation d’investissement :
Évolution d’un portefeuille hypothétique de 1 000 000 € réparti équitablement entre les 10 actions.

🌍 Répartition sectorielle et géographique :
Graphiques interactifs des allocations par secteur et pays.

🧮 Indicateurs fondamentaux :
PER, rendement du dividende, capitalisation boursière, BPA, variation YTD, etc.

💱 Support multidevise :
Conversion automatique selon la devise du ticker : €, $, £, CHF.

📊 Visualisations interactives :
Graphiques Plotly pour suivre l’évolution des cours sur 1 mois, 6 mois ou 1 an.

🏛️ Présentation des business models :
Texte descriptif pour chaque entreprise afin de comprendre sa logique économique et son “moat”.

💼 Composition du portefeuille (Version 2.0 – Octobre 2025)
Ticker	Société	Pays	Secteur
GOOGL	Alphabet Inc.	🇺🇸 USA	Technologie
ERF.PA	Eurofins Scientific	🇫🇷 France	Biotechnologie
GTT.PA	Gaztransport & Technigaz	🇫🇷 France	Énergie / GNL
GD	General Dynamics	🇺🇸 USA	Défense
ROG.SW	Roche Holding	🇨🇭 Suisse	Santé / Pharma
RR.L	Rolls-Royce Holdings	🇬🇧 Royaume-Uni	Aéronautique / Énergie
UBSG.SW	UBS Group	🇨🇭 Suisse	Banque / Gestion d’actifs
VIE.PA	Veolia Environnement	🇫🇷 France	Services aux collectivités
RIO.L	Rio Tinto plc	🇬🇧 Royaume-Uni	Matières premières / Cuivre / Lithium
SLB	Schlumberger (SLB)	🇺🇸 USA	Énergie / Services pétroliers

🧩 Structure du projet
portfolio10v/
│
├── app.py                        # Page d’accueil et routage vers Business Models
├── pages/
│   ├── Business_Models.py        # Présentation des modèles économiques
│   ├── Performance_du_Portefeuille.py
│   └── ROLLS_ROYCE_HOLDINGS.py   # Page dédiée d'analyse détaillée
│
├── src/
│   ├── data_loader.py            # Chargement du CSV et des données YFinance
│   ├── stock_utils.py            # Devises, rendements, formatage
│   ├── ui_components.py          # CSS, bandeau défilant, mise en page
│   └── visualization.py          # Fonctions de graphiques Plotly
│
├── data/
│   ├── Portefeuille_10_business_models.csv
│   └── Tickers_Yahoo_F.xlsx
│
├── images/                       # Logos, captures d’écran
├── requirements.txt              # Dépendances Python
└── README.md                     # Documentation du projet

🌐 Déploiement

L’application peut être déployée sur :
Streamlit Community Cloud
ou sur un serveur privé / VPS (ex : PythonAnywhere, Render, ou Railway).

👤 Auteur

Thierry (thidescac25)
💼 Data Analyst – Concepteur d’outils décisionnels
📍 France