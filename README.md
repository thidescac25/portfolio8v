Komorebi Investments 8 stocks 

Application de présentation et de suivi d'un portefeuille de 8 actions internationales développée avec Streamlit.

Fonctionnalités

Suivi en temps réel : Bandeau défilant avec les prix actuels et variations des 8 valeurs du portefeuille
Présentation comparative : Performance historique comparée aux indices majeurs (CAC 40, S&P 500, etc.)
Simulation d'investissement : Évolution d'un portefeuille d'1M€ réparti équitablement
Présentation sectorielle et géographique : Visualisation de la répartition du portefeuille
Métriques détaillées : PER, rendement du dividende, capitalisation, BPA, etc.
Données multidevises : Support de plusieurs devises (€, $, £, CHF)
Graphiques interactifs : Visualisation de l'évolution des cours sur différentes périodes
Présentation des business models : Mise en valeur des modèles économiques comme critère de sélection

Composition du portefeuille
Le portefeuille est composé de 8 actions internationales diversifiées :

GOOGL (Alphabet) - USA
ERF.PA (Eurofins Scientific) - France
GTT.PA (Gaztransport et Technigaz) - France
GD (General Dynamics) - USA
ROG.SW (Roche Holding) - Suisse
RR.L (Rolls-Royce) - Royaume-Uni
UBSG.SW (UBS Group) - Suisse
VIE.PA (Veolia) - France

Structure du projet

app.py : Page d'accueil avec bandeau défilant et sélection d'entreprise
pages/2_Portfolio_Analysis.py : Présentation détaillée du portefeuille
data/Portefeuille_8_business_models.csv : Données des entreprises

Technologies utilisées

Python 3.x
Streamlit pour l'interface web
Pandas & NumPy pour la présentation de données
Plotly pour les graphiques interactifs
yfinance pour les données boursières
Intégration HTML/CSS pour le bandeau défilant

Installation locale
bash# Cloner le dépôt
git clone https://github.com/thidescac25/portfolio8v.git
cd portfolio8v

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app.py

Déploiement
L'application est déployée sur Streamlit Sharing et accessible via le compte utilisateur thidescac25.

Auteur
Thierry - thidescac25