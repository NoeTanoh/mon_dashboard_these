import streamlit as st
import base64
import os

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Thèse",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Fonction pour encoder vidéo en base64
def get_base64_video(video_path):
    try:
        if os.path.exists(video_path):
            with open(video_path, "rb") as video_file:
                return base64.b64encode(video_file.read()).decode()
        else:
            print(f"Vidéo non trouvée: {video_path}")
            return None
    except Exception as e:
        print(f"Erreur vidéo: {e}")
        return None

# CSS pour les styles et animations
def load_css():
    return """
    <style>
    /* Masquer les éléments Streamlit par défaut */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    .stDecoration {display:none;}
    
    /* Rendre le conteneur principal transparent */
    .main .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 0rem;
        padding-right: 0rem;
        background-color: transparent !important;
    }
    
    /* Rendre tout l'arrière-plan transparent */
    .stApp {
        background-color: transparent !important;
    }
    
    .main {
        background-color: transparent !important;
    }
    
    /* Masquer la barre latérale */
    .css-1d391kg {
        display: none;
    }
    
    /* Container principal */
    .main-container {
        position: relative;
        height: 100vh;
        width: 100vw;
        overflow: hidden;
    }
    
    /* Vidéo en arrière-plan */
    .video-background {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        object-fit: cover;
        z-index: -10;
    }
    
    /* Overlay sombre */
    .overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(0, 0, 0, 0.4);
        z-index: -9;
    }
    
    /* Texte central avec animation de couleur */
    .welcome-text {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
        z-index: 10;
        animation: colorChange 2s infinite;
        width: 100%;
    }
    
    /* Animation de changement de couleur toutes les 2 secondes */
    @keyframes colorChange {
        0% { color: #ff6b6b; }
        25% { color: #4ecdc4; }
        50% { color: #45b7d1; }
        75% { color: #f39c12; }
        100% { color: #ff6b6b; }
    }
    
    /* Styles du titre principal */
    .welcome-title {
        font-size: 4rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.7);
    }
    
    /* Styles du sous-titre */
    .welcome-subtitle {
        font-size: 1.8rem;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
        font-weight: 300;
    }
    
    /* Styles du bouton */
    .custom-button {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        border: none;
        padding: 18px 45px;
        font-size: 1.3rem;
        font-weight: bold;
        color: white;
        border-radius: 50px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .custom-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.4);
        background: linear-gradient(45deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Bouton positionné sous le texte - centré parfaitement */
    .button-container {
        position: fixed;
        top: 65%;
        left: 50%;
        transform: translateX(-50%);
        z-index: 15;
        text-align: center;
        width: 100%;
    }
    
    /* Design amélioré du bouton - VRAIMENT CENTRÉ */
    .stButton {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #ff6b6b, #4ecdc4, #45b7d1, #f39c12) !important;
        border: 2px solid #ffffff !important;
        padding: 18px 40px !important;
        font-size: 1.5rem !important;
        font-weight: bold !important;
        color: white !important;
        border-radius: 50px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 
            0 10px 30px rgba(0,0,0,0.3),
            0 0 20px rgba(255,107,107,0.4) !important;
        text-transform: uppercase !important;
        letter-spacing: 3px !important;
        width: 320px !important;
        height: 65px !important;
        margin: 0 auto !important;
        display: block !important;
        position: relative !important;
        overflow: hidden !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.08) !important;
        box-shadow: 
            0 15px 40px rgba(0,0,0,0.4),
            0 0 30px rgba(78,205,196,0.6) !important;
        background: linear-gradient(135deg, #4ecdc4, #45b7d1, #f39c12, #ff6b6b) !important;
        border-color: #fff !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(1.05) !important;
    }
    
    /* Animation de pulsation */
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255,107,107,0.7); }
        70% { box-shadow: 0 0 0 10px rgba(255,107,107,0); }
        100% { box-shadow: 0 0 0 0 rgba(255,107,107,0); }
    }
    
    .stButton > button {
        animation: pulse 2s infinite !important;
    }
    </style>
    """

def main():
    # Charger les styles CSS
    st.markdown(load_css(), unsafe_allow_html=True)
    
    # Tentative de chargement de la vidéo
    video_path = "assets/videos/background.mp4"
    video_base64 = get_base64_video(video_path)
    
    # Afficher un message de debug
    if not video_base64:
        st.info("💡 Pour voir la vidéo en arrière-plan, place ton fichier vidéo dans: assets/videos/background.mp4")
    
    # Affichage de la vidéo ou fallback
    if video_base64:
        st.markdown(f"""
        <div class="main-container">
            <video autoplay muted loop class="video-background">
                <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
            </video>
            <div class="overlay"></div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Fallback avec arrière-plan dégradé si pas de vidéo
        st.markdown("""
        <div class="main-container">
            <div style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; 
                        background: linear-gradient(45deg, #667eea 0%, #764ba2 50%, #f093fb 100%); 
                        z-index: -10;"></div>
            <div class="overlay"></div>
        </div>
        """, unsafe_allow_html=True)
    
    # Contenu principal - Texte centré
    st.markdown("""
    <div class="welcome-text">
        <div class="welcome-title">BIENVENUE SUR NOTRE PLATEFORME</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Conteneur pour le bouton - VRAIMENT centré
    st.markdown("""
    <div style="position: fixed; top: 65%; left: 50%; transform: translate(-50%, -50%); z-index: 20;">
        <form action="/dashboard" method="get" target="_blank">
            <button type="submit" style="
                background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #f39c12);
                border: none;
                padding: 20px 35px;
                font-size: 1.8rem;
                font-weight: bold;
                color: white;
                border-radius: 40px;
                cursor: pointer;
                box-shadow: 0 10px 30px rgba(0,0,0,0.4), 0 0 20px rgba(255,107,107,0.5);
                text-transform: uppercase;
                letter-spacing: 3px;
                transition: all 0.3s ease;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
                animation: pulse 2s infinite;
            "
            onmouseover="this.style.transform='scale(1.1) translateY(-5px)'; this.style.boxShadow='0 20px 40px rgba(0,0,0,0.6), 0 0 30px rgba(78,205,196,0.7)'"
            onmouseout="this.style.transform='scale(1) translateY(0px)'; this.style.boxShadow='0 10px 30px rgba(0,0,0,0.4), 0 0 20px rgba(255,107,107,0.5)'"
            onclick="window.open('http://localhost:8502', '_blank')">
                🚀 ACCÉDER AU DASHBOARD
            </button>
        </form>
    </div>
    
    <style>
    @keyframes pulse {
        0% { box-shadow: 0 10px 30px rgba(0,0,0,0.4), 0 0 0 0 rgba(255,107,107,0.7); }
        50% { box-shadow: 0 10px 30px rgba(0,0,0,0.4), 0 0 0 15px rgba(255,107,107,0); }
        100% { box-shadow: 0 10px 30px rgba(0,0,0,0.4), 0 0 0 0 rgba(255,107,107,0); }
    }
    </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()