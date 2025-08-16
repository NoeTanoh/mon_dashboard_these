import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests

# Appliquer un style CSS personnalisé
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    .main {background-color: #f5f5f5; font-family: 'Roboto', sans-serif;}
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #009e60 0%, #f77f00 100%);
        color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .sidebar .sidebar-content h1, .sidebar .sidebar-content h2, .sidebar .sidebar-content h3 {
        color: #ffffff;
        font-weight: 700;
    }
    .stSelectbox, .stButton>button {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 8px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #f77f00;
        color: #ffffff;
        transform: scale(1.05);
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .kpi-rendement {
        border-left: 5px solid #009e60;
    }
    .kpi-revenu {
        border-left: 5px solid #f77f00;
    }
    .kpi-icon {
        font-size: 24px;
        color: #333333;
    }
    .kpi-value {
        color: #009e60;
        font-weight: 700;
    }
    .kpi-value-revenu {
        color: #f77f00;
        font-weight: 700;
    }
    h1.theme1 {color: #009e60; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);}
    h1.theme2 {color: #f77f00; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);}
    h1.theme3 {color: #333333; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);}
    h1.theme4 {color: #0066cc; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);}
    h2, h3 {
        color: #f77f00;
        font-family: 'Roboto', sans-serif;
        font-weight: 400;
    }
    .recommendation {
        background-color: #e0f2e9;
        padding: 15px;
        border-left: 5px solid #009e60;
        border-radius: 8px;
        margin-top: 20px;
        font-family: 'Roboto', sans-serif;
        font-size: 16px;
        display: flex;
        align-items: center;
        gap: 10px;
        animation: fadeIn 1s ease-in;
    }
    .recommendation i {
        color: #f77f00;
        font-size: 20px;
    }
    .weather-box {
        background: linear-gradient(135deg, #009e60 0%, #f77f00 100%);
        color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        margin-top: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
        animation: fadeIn 1s ease-in;
    }
    .weather-box i {
        font-size: 24px;
    }
    .divider {
        border-top: 2px solid #009e60;
        margin: 20px 0;
    }
    .plotly-chart {
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    @keyframes fadeIn {
        from {opacity: 0;}
        to {opacity: 1;}
    }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
""", unsafe_allow_html=True)

# Configuration de la mise en page Streamlit
st.set_page_config(page_title="Système d'Aide à la Décision - Bassin Cotonnier Ivoirien", layout="wide")

# Fonction pour récupérer la météo (simulée pour l'exemple)
def get_weather(city="Abidjan"):
    # Pour une implémentation réelle, utilisez l'API OpenWeatherMap
    # api_key = "VOTRE_CLÉ_API"
    # url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    # response = requests.get(url).json()
    # Simulé pour l'exemple
    return {"temp": 28, "feels_like": 31, "weather": "partly cloudy", "icon": "fas fa-cloud-sun"}

# Charger les données
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(r"C:\Users\HP\Documents\mon_dashboard_these\pages\donnees_coton_regions_corrigees.csv")
        # Nettoyage des données
        df = df.dropna()  # Supprimer les lignes avec valeurs manquantes
        df = df[df["Nom_Region"] != "A_VERIFIER"]  # Supprimer la région A_VERIFIER
        df["Annee"] = df["Annee"].astype(int)
        df["Mois_num"] = df["Mois_num"].astype(int)
        df["Rendement_ha"] = df["Rendement_ha"].astype(float)
        df["Revenu_Net"] = df["Revenu_Net"].astype(float)
        df["Cout_Intrants"] = df["Cout_Intrants"].astype(float)
        return df
    except FileNotFoundError:
        st.error("Erreur : Le fichier 'donnees_coton_regions_corrigees.csv' n'a pas été trouvé. Veuillez vérifier le chemin du fichier.")
        return pd.DataFrame()

df = load_data()
if df.empty:
    st.stop()

# Fonction pour formater les nombres
def format_number(value):
    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    elif value >= 1_000:
        return f"{value / 1_000:.2f}K"
    return f"{value:.2f}"

# Barre latérale pour la navigation et les filtres
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Choisir un thème",
    [
        "🌍 Performance régionale et environnementale",
        "🌾 Efficacité des pratiques culturales",
        "💰 Optimisation des intrants et coûts",
        "📈 Tendances temporelles et profils des producteurs",
    ],
)

# Filtres interactifs
st.sidebar.subheader("Filtres")
regions = ["Toutes"] + sorted(df["Nom_Region"].unique())
region_filter = st.sidebar.selectbox("Région", regions)
annees = ["Toutes"] + sorted(df["Annee"].unique())
annee_filter = st.sidebar.selectbox("Année", annees)
types_sol = ["Tous"] + sorted(df["Type_Sol"].unique())
sol_filter = st.sidebar.selectbox("Type de sol", types_sol)
types_culture = ["Tous"] + sorted(df["Type_Culture"].unique())
culture_filter = st.sidebar.selectbox("Type de culture", types_culture)
experience_filter = st.sidebar.selectbox("Niveau d'expérience", ["Tous"] + sorted(df["Niveau_Experience"].unique()))
financement_filter = st.sidebar.selectbox("Accès au financement", ["Tous"] + sorted(df["Acces_Financement"].unique()))

# Appliquer les filtres
filtered_df = df.copy()
if region_filter != "Toutes":
    filtered_df = filtered_df[filtered_df["Nom_Region"] == region_filter]
if annee_filter != "Toutes":
    filtered_df = filtered_df[filtered_df["Annee"] == int(annee_filter)]
if sol_filter != "Tous":
    filtered_df = filtered_df[filtered_df["Type_Sol"] == sol_filter]
if culture_filter != "Tous":
    filtered_df = filtered_df[filtered_df["Type_Culture"] == culture_filter]
if experience_filter != "Tous":
    filtered_df = filtered_df[filtered_df["Niveau_Experience"] == experience_filter]
if financement_filter != "Tous":
    filtered_df = filtered_df[filtered_df["Acces_Financement"] == financement_filter]

# Afficher la météo dans le footer
weather = get_weather()
weather_icon = weather["icon"]
weather_text = f"<div class='weather-box'><i class='{weather_icon}'></i> Météo à Abidjan : {weather['temp']}°C (Ressenti : {weather['feels_like']}°C) - {weather['weather']}</div>"
st.sidebar.markdown("<hr class='divider'>", unsafe_allow_html=True)
st.sidebar.markdown(weather_text, unsafe_allow_html=True)

# Thème 1 : Performance régionale et environnementale
if page == "🌍 Performance régionale et environnementale":
    st.markdown("<h1 class='theme1'>Performance Régionale et Environnementale</h1>", unsafe_allow_html=True)
    st.markdown("**Analyse des rendements, revenus et coûts par région et conditions environnementales pour optimiser l'implantation.**")

    # Calcul des KPIs
    kpi_region = filtered_df.groupby(["Nom_Region", "Type_Sol"]).agg({
        "Rendement_ha": "mean",
        "Revenu_Net": "mean",
        "Cout_Intrants": "mean"
    }).reset_index()
    kpi_region["Taux_Rentabilite"] = kpi_region["Revenu_Net"] / kpi_region["Cout_Intrants"]

    # Afficher les KPIs
    st.subheader("Indicateurs Clés")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='stMetric kpi-rendement'><i class='fas fa-seedling kpi-icon'></i><div><strong>Rendement moyen (kg/ha)</strong><br><span class='kpi-value'>{format_number(kpi_region['Rendement_ha'].mean())} kg/ha</span></div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='stMetric kpi-revenu'><i class='fas fa-money-bill-wave kpi-icon'></i><div><strong>Revenu net moyen</strong><br><span class='kpi-value-revenu'>{format_number(kpi_region['Revenu_Net'].mean())} FCFA</span></div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='stMetric kpi-rendement'><i class='fas fa-coins kpi-icon'></i><div><strong>Coût intrants moyen</strong><br><span class='kpi-value'>{format_number(kpi_region['Cout_Intrants'].mean())} FCFA</span></div></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='stMetric kpi-rendement'><i class='fas fa-chart-line kpi-icon'></i><div><strong>Taux de rentabilité</strong><br><span class='kpi-value'>{kpi_region['Taux_Rentabilite'].mean():.2%}</span></div></div>", unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # Graphique en barres : Rendement par région et type de sol
    st.subheader("Rendement par Région et Type de Sol")
    fig1 = px.bar(
        kpi_region,
        x="Nom_Region",
        y="Rendement_ha",
        color="Type_Sol",
        title="Rendement moyen par région et type de sol",
        labels={"Rendement_ha": "Rendement (kg/ha)", "Nom_Region": "Région"},
        color_discrete_map={"Limoneux": "#d4a017", "Argileux": "#009e60", "Sableux": "#f77f00"}
    )
    fig1.update_layout(title_x=0.5, plot_bgcolor="#ffffff", paper_bgcolor="#ffffff", font=dict(family="Roboto", size=12))
    st.plotly_chart(fig1, use_container_width=True)

    # Carte de la Côte d'Ivoire
    st.subheader("Carte des Performances par Région")
    region_coords = {
        "Gbêkê": {"lat": 7.7, "lon": -5.0},
        "Poro": {"lat": 9.5, "lon": -5.6},
        "Bagoué": {"lat": 9.8, "lon": -6.4},
        "Worodougou": {"lat": 8.3, "lon": -6.5},
        "Kabadougou": {"lat": 9.1, "lon": -7.5},
        "Tchologo": {"lat": 10.0, "lon": -5.7},
        "Hambol": {"lat": 8.2, "lon": -5.1}
    }
    kpi_region["lat"] = kpi_region["Nom_Region"].map(lambda x: region_coords.get(x, {"lat": 9.0})["lat"])
    kpi_region["lon"] = kpi_region["Nom_Region"].map(lambda x: region_coords.get(x, {"lon": -6.0})["lon"])
    fig2 = px.scatter_mapbox(
        kpi_region,
        lat="lat",
        lon="lon",
        size="Rendement_ha",
        color="Revenu_Net",
        hover_name="Nom_Region",
        hover_data=["Rendement_ha", "Revenu_Net"],
        title="Rendement et revenu net par région en Côte d'Ivoire",
        color_continuous_scale=["#f77f00", "#009e60"],
        size_max=30
    )
    fig2.update_layout(
        mapbox_style="open-street-map",
        mapbox_center={"lat": 7.5, "lon": -5.5},
        mapbox_zoom=5.5,
        title_x=0.5,
        margin={"r":0,"t":50,"l":0,"b":0},
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(family="Roboto", size=12)
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Nuage de points : Rendement vs pluviométrie
    st.subheader("Rendement vs Pluviométrie")
    fig3 = px.scatter(
        filtered_df,
        x="Pluviometrie_Moyenne",
        y="Rendement_ha",
        color="Type_Sol",
        title="Rendement vs pluviométrie par type de sol",
        labels={"Pluviometrie_Moyenne": "Pluviométrie (mm)", "Rendement_ha": "Rendement (kg/ha)"},
        color_discrete_map={"Limoneux": "#d4a017", "Argileux": "#009e60", "Sableux": "#f77f00"}
    )
    fig3.update_layout(title_x=0.5, plot_bgcolor="#ffffff", paper_bgcolor="#ffffff", font=dict(family="Roboto", size=12))
    st.plotly_chart(fig3, use_container_width=True)

    # Tableau interactif
    st.subheader("Tableau des Performances")
    st.dataframe(kpi_region[["Nom_Region", "Type_Sol", "Rendement_ha", "Revenu_Net", "Taux_Rentabilite"]], use_container_width=True)

    # Recommandation dynamique
    if not kpi_region.empty:
        top_region = kpi_region.loc[kpi_region["Rendement_ha"].idxmax()]
        st.markdown(f"<div class='recommendation'><i class='fas fa-lightbulb'></i> **Recommandation** : La région {top_region['Nom_Region']} avec un sol {top_region['Type_Sol']} présente un rendement moyen de {format_number(top_region['Rendement_ha'])} kg/ha. Privilégiez cette combinaison pour la culture.</div>", unsafe_allow_html=True)

# Thème 2 : Efficacité des pratiques culturales
elif page == "🌾 Efficacité des pratiques culturales":
    st.markdown("<h1 class='theme2'>Efficacité des Pratiques Culturales</h1>", unsafe_allow_html=True)
    st.markdown("**Évaluation de l'impact des pratiques agricoles sur la productivité et la rentabilité.**")

    # Calcul des KPIs
    kpi_culture = filtered_df.groupby("Type_Culture").agg({
        "Rendement_ha": "mean",
        "Revenu_Net": "mean",
        "Cout_Phytosanitaire": "mean"
    }).reset_index()

    # Afficher les KPIs
    st.subheader("Indicateurs Clés")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='stMetric kpi-rendement'><i class='fas fa-seedling kpi-icon'></i><div><strong>Rendement (Manuelle)</strong><br><span class='kpi-value'>{format_number(kpi_culture[kpi_culture['Type_Culture'] == 'Manuelle']['Rendement_ha'].iloc[0] if 'Manuelle' in kpi_culture['Type_Culture'].values else 0)} kg/ha</span></div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='stMetric kpi-rendement'><i class='fas fa-tractor kpi-icon'></i><div><strong>Rendement (Motorisée)</strong><br><span class='kpi-value'>{format_number(kpi_culture[kpi_culture['Type_Culture'] == 'Motorisée']['Rendement_ha'].iloc[0] if 'Motorisée' in kpi_culture['Type_Culture'].values else 0)} kg/ha</span></div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='stMetric kpi-revenu'><i class='fas fa-coins kpi-icon'></i><div><strong>Coût phyto. moyen</strong><br><span class='kpi-value-revenu'>{format_number(kpi_culture['Cout_Phytosanitaire'].mean())} FCFA</span></div></div>", unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # Graphique en barres : Rendement par type de culture
    st.subheader("Rendement par Type de Culture et Saison")
    fig4 = px.bar(
        filtered_df.groupby(["Type_Culture", "Saison"])["Rendement_ha"].mean().reset_index(),
        x="Type_Culture",
        y="Rendement_ha",
        color="Saison",
        title="Rendement moyen par type de culture et saison",
        labels={"Rendement_ha": "Rendement (kg/ha)", "Type_Culture": "Type de culture"},
        color_discrete_sequence=["#009e60", "#f77f00"]
    )
    fig4.update_layout(title_x=0.5, plot_bgcolor="#ffffff", paper_bgcolor="#ffffff", font=dict(family="Roboto", size=12))
    st.plotly_chart(fig4, use_container_width=True)

    # Graphique en boîte : Revenu net par type de culture
    st.subheader("Distribution du Revenu Net")
    fig5 = px.box(
        filtered_df,
        x="Type_Culture",
        y="Revenu_Net",
        title="Distribution du revenu net par type de culture",
        labels={"Revenu_Net": "Revenu net (FCFA)", "Type_Culture": "Type de culture"},
        color_discrete_sequence=["#009e60"]
    )
    fig5.update_layout(title_x=0.5, plot_bgcolor="#ffffff", paper_bgcolor="#ffffff", font=dict(family="Roboto", size=12))
    st.plotly_chart(fig5, use_container_width=True)

    # Graphique en donut : Proportion des producteurs utilisant des drones
    st.subheader("Utilisation des Drones")
    fig6 = px.pie(
        filtered_df,
        names="Utilisation_Drone",
        title="Proportion des producteurs utilisant des drones",
        hole=0.4,
        color_discrete_sequence=["#009e60", "#f77f00"]
    )
    fig6.update_layout(title_x=0.5, font=dict(family="Roboto", size=12))
    st.plotly_chart(fig6, use_container_width=True)

    # Tableau interactif
    st.subheader("Tableau des Pratiques")
    st.dataframe(kpi_culture, use_container_width=True)

    # Recommandation dynamique
    if not kpi_culture.empty:
        top_culture = kpi_culture.loc[kpi_culture["Rendement_ha"].idxmax(), "Type_Culture"]
        top_yield = kpi_culture["Rendement_ha"].max()
        st.markdown(f"<div class='recommendation'><i class='fas fa-lightbulb'></i> **Recommandation** : La culture {top_culture} génère un rendement moyen de {format_number(top_yield)} kg/ha. Investir dans cette pratique peut augmenter la productivité.</div>", unsafe_allow_html=True)

# Thème 3 : Optimisation des intrants et coûts
elif page == "💰 Optimisation des intrants et coûts":
    st.markdown("<h1 class='theme3'>Optimisation des Intrants et Coûts</h1>", unsafe_allow_html=True)
    st.markdown("**Identification des intrants les plus efficaces pour maximiser le rendement et minimiser les coûts.**")

    # Calcul des KPIs
    kpi_intrants = filtered_df.groupby("Type_Engrais").agg({
        "Rendement_ha": "mean",
        "Cout_Intrants": "mean",
        "Superficie_Cultivee": "mean"
    }).reset_index()
    kpi_intrants["Cout_Intrants_ha"] = kpi_intrants["Cout_Intrants"] / kpi_intrants["Superficie_Cultivee"]

    # Afficher les KPIs
    st.subheader("Indicateurs Clés")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='stMetric kpi-rendement'><i class='fas fa-seedling kpi-icon'></i><div><strong>Rendement (NPK)</strong><br><span class='kpi-value'>{format_number(kpi_intrants[kpi_intrants['Type_Engrais'] == 'NPK']['Rendement_ha'].iloc[0] if 'NPK' in kpi_intrants['Type_Engrais'].values else 0)} kg/ha</span></div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='stMetric kpi-rendement'><i class='fas fa-seedling kpi-icon'></i><div><strong>Rendement (Urée)</strong><br><span class='kpi-value'>{format_number(kpi_intrants[kpi_intrants['Type_Engrais'] == 'Urée']['Rendement_ha'].iloc[0] if 'Urée' in kpi_intrants['Type_Engrais'].values else 0)} kg/ha</span></div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='stMetric kpi-revenu'><i class='fas fa-coins kpi-icon'></i><div><strong>Coût intrants moyen/ha</strong><br><span class='kpi-value-revenu'>{format_number(kpi_intrants['Cout_Intrants_ha'].mean())} FCFA/ha</span></div></div>", unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # Graphique en barres : Rendement par type d'engrais
    st.subheader("Rendement par Type d'Engrais")
    fig7 = px.bar(
        filtered_df.groupby(["Type_Engrais", "Nom_Region"])["Rendement_ha"].mean().reset_index(),
        x="Type_Engrais",
        y="Rendement_ha",
        color="Nom_Region",
        title="Rendement moyen par type d'engrais et région",
        labels={"Rendement_ha": "Rendement (kg/ha)", "Type_Engrais": "Type d'engrais"},
        color_discrete_sequence=["#009e60", "#f77f00", "#d4a017"]
    )
    fig7.update_layout(title_x=0.5, plot_bgcolor="#ffffff", paper_bgcolor="#ffffff", font=dict(family="Roboto", size=12))
    st.plotly_chart(fig7, use_container_width=True)

    # Nuage de points : Coût vs rendement
    st.subheader("Coût vs Rendement")
    fig8 = px.scatter(
        filtered_df,
        x="Cout_Intrants",
        y="Rendement_ha",
        color="Type_Semence",
        title="Coût des intrants vs rendement par type de semence",
        labels={"Cout_Intrants": "Coût des intrants (FCFA)", "Rendement_ha": "Rendement (kg/ha)"},
        color_discrete_sequence=["#009e60", "#f77f00", "#d4a017"]
    )
    fig8.update_layout(title_x=0.5, plot_bgcolor="#ffffff", paper_bgcolor="#ffffff", font=dict(family="Roboto", size=12))
    st.plotly_chart(fig8, use_container_width=True)

    # Graphique en barres empilées : Répartition des coûts
    st.subheader("Répartition des Coûts")
    cost_breakdown = filtered_df.groupby("Type_Culture")[["Cout_Engrais", "Cout_Semence", "Cout_Phytosanitaire"]].mean().reset_index()
    fig9 = go.Figure(data=[
        go.Bar(name="Coût Engrais", x=cost_breakdown["Type_Culture"], y=cost_breakdown["Cout_Engrais"], marker_color="#009e60"),
        go.Bar(name="Coût Semence", x=cost_breakdown["Type_Culture"], y=cost_breakdown["Cout_Semence"], marker_color="#f77f00"),
        go.Bar(name="Coût Phyto.", x=cost_breakdown["Type_Culture"], y=cost_breakdown["Cout_Phytosanitaire"], marker_color="#d4a017")
    ])
    fig9.update_layout(barmode="stack", title="Répartition des coûts par type de culture", xaxis_title="Type de culture", yaxis_title="Coût (FCFA)", title_x=0.5, plot_bgcolor="#ffffff", paper_bgcolor="#ffffff", font=dict(family="Roboto", size=12))
    st.plotly_chart(fig9, use_container_width=True)

    # Tableau interactif
    st.subheader("Tableau des Intrants")
    st.dataframe(kpi_intrants, use_container_width=True)

    # Recommandation dynamique
    if not kpi_intrants.empty:
        top_engrais = kpi_intrants.loc[kpi_intrants["Rendement_ha"].idxmax(), "Type_Engrais"]
        top_yield = kpi_intrants["Rendement_ha"].max()
        st.markdown(f"<div class='recommendation'><i class='fas fa-lightbulb'></i> **Recommandation** : L'engrais {top_engrais} offre un rendement moyen de {format_number(top_yield)} kg/ha. Privilégiez cet engrais pour un bon rapport coût/efficacité.</div>", unsafe_allow_html=True)

# Thème 4 : Tendances temporelles et profils des producteurs
elif page == "📈 Tendances temporelles et profils des producteurs":
    st.markdown("<h1 class='theme4'>Tendances Temporelles et Profils des Producteurs</h1>", unsafe_allow_html=True)
    st.markdown("**Analyse des tendances saisonnières et de l'impact des profils des producteurs sur la performance.**")

    # Calcul des KPIs
    kpi_temp = filtered_df.groupby(["Annee", "Saison"]).agg({
        "Rendement_ha": "mean",
        "Revenu_Net": "mean"
    }).reset_index()
    kpi_profil = filtered_df.groupby("Classe_Age").agg({
        "Rendement_ha": "mean",
        "Revenu_Net": "mean"
    }).reset_index()
    kpi_experience = filtered_df.groupby("Niveau_Experience")["Revenu_Net"].mean().reset_index()

    # Afficher les KPIs
    st.subheader("Indicateurs Clés")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='stMetric kpi-rendement'><i class='fas fa-cloud-rain kpi-icon'></i><div><strong>Rendement (Saison des pluies)</strong><br><span class='kpi-value'>{format_number(kpi_temp[kpi_temp['Saison'] == 'Saison des pluies']['Rendement_ha'].mean() if 'Saison des pluies' in kpi_temp['Saison'].values else 0)} kg/ha</span></div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='stMetric kpi-rendement'><i class='fas fa-sun kpi-icon'></i><div><strong>Rendement (Saison sèche)</strong><br><span class='kpi-value'>{format_number(kpi_temp[kpi_temp['Saison'] == 'Saison sèche']['Rendement_ha'].mean() if 'Saison sèche' in kpi_temp['Saison'].values else 0)} kg/ha</span></div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='stMetric kpi-revenu'><i class='fas fa-money-bill-wave kpi-icon'></i><div><strong>Revenu net (Expert)</strong><br><span class='kpi-value-revenu'>{format_number(kpi_experience[kpi_experience['Niveau_Experience'] == 'Expert']['Revenu_Net'].iloc[0] if 'Expert' in kpi_experience['Niveau_Experience'].values else 0)} FCFA</span></div></div>", unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # Graphique en ligne : Évolution du rendement
    st.subheader("Évolution du Rendement")
    fig10 = px.line(
        kpi_temp,
        x="Annee",
        y="Rendement_ha",
        color="Saison",
        title="Évolution du rendement par année et saison",
        labels={"Rendement_ha": "Rendement (kg/ha)", "Annee": "Année"},
        color_discrete_sequence=["#009e60", "#f77f00"]
    )
    fig10.update_layout(title_x=0.5, plot_bgcolor="#ffffff", paper_bgcolor="#ffffff", font=dict(family="Roboto", size=12))
    st.plotly_chart(fig10, use_container_width=True)

    # Graphique en boîte : Revenu net par expérience
    st.subheader("Revenu Net par Expérience")
    fig11 = px.box(
        filtered_df,
        x="Niveau_Experience",
        y="Revenu_Net",
        title="Distribution du revenu net par niveau d'expérience",
        labels={"Revenu_Net": "Revenu net (FCFA)", "Niveau_Experience": "Niveau d'expérience"},
        color_discrete_sequence=["#009e60"]
    )
    fig11.update_layout(title_x=0.5, plot_bgcolor="#ffffff", paper_bgcolor="#ffffff", font=dict(family="Roboto", size=12))
    st.plotly_chart(fig11, use_container_width=True)

    # Graphique en donut : Proportion des producteurs par accès au financement
    st.subheader("Accès au Financement")
    fig12 = px.pie(
        filtered_df,
        names="Acces_Financement",
        title="Proportion des producteurs avec/sans accès au financement",
        hole=0.4,
        color_discrete_sequence=["#009e60", "#f77f00"]
    )
    fig12.update_layout(title_x=0.5, font=dict(family="Roboto", size=12))
    st.plotly_chart(fig12, use_container_width=True)

    # Heatmap : Rendement par mois et année
    st.subheader("Rendement par Mois et Année")
    heatmap_data = filtered_df.pivot_table(values="Rendement_ha", index="Mois_num", columns="Annee", aggfunc="mean")
    fig13 = px.imshow(
        heatmap_data,
        labels=dict(x="Année", y="Mois", color="Rendement (kg/ha)"),
        title="Rendement moyen par mois et année",
        color_continuous_scale=["#f77f00", "#009e60"]
    )
    fig13.update_layout(title_x=0.5, font=dict(family="Roboto", size=12))
    st.plotly_chart(fig13, use_container_width=True)

    # Recommandation dynamique
    if not kpi_experience.empty:
        top_experience = kpi_experience.loc[kpi_experience["Revenu_Net"].idxmax(), "Niveau_Experience"]
        top_revenu = kpi_experience["Revenu_Net"].max()
        st.markdown(f"<div class='recommendation'><i class='fas fa-lightbulb'></i> **Recommandation** : Les producteurs {top_experience.lower()} obtiennent un revenu net moyen de {format_number(top_revenu)} FCFA. Encouragez les programmes de formation pour les débutants.</div>", unsafe_allow_html=True)