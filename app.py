import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
import os

# 1. CONFIGURATION DE PAGE PREMIUM
st.set_page_config(
    page_title="LapinEco Pro+",
    page_icon="🐇",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. STYLE CSS DARK MODE (Le Front-End "Waouh")
st.markdown("""
<style>
    .stApp { background-color: #121212; color: #FFFFFF; font-family: 'Segoe UI', sans-serif; }
    h1 { color: #FFFFFF; font-weight: 800; text-align: center; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 0px; }
    .subtitle { text-align: center; color: #BDBDBD; font-style: italic; margin-bottom: 30px; }
    h3 { color: #FF1744; font-weight: 600; border-bottom: 1px solid #424242; padding-bottom: 5px; }

    /* Onglets Premium */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #212121; color: #BDBDBD; padding: 10px 25px; border-radius: 5px; border: none;
    }
    .stTabs [aria-selected="true"] { background-color: #FF1744 !important; color: #FFFFFF !important; }

    /* KPI Cards */
    [data-testid="stMetric"] { 
        background-color: #1E1E1E; padding: 15px; border-radius: 10px; border: 1px solid #333333; 
    }
    div[data-testid="stMetricValue"] > div { color: #FFFFFF; font-weight: 800; }
    div[data-testid="stMetricLabel"] > label { color: #FF1744; text-transform: uppercase; }
    
    /* Formulaire */
    .stForm { background-color: #1E1E1E; border-radius: 12px; border: 1px solid #333333; }
    button[kind="primaryFormSubmit"] { 
        background-color: #FF1744; color: white; width: 100%; border-radius: 8px; border: none; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 3. INITIALISATION DE LA MÉMOIRE
if 'liste_ventes' not in st.session_state:
    st.session_state.liste_ventes = [
        {'Race': 'Néo-Zélandais', 'Prix_Vente': 12000, 'Poids_kg': 3.2},
        {'Race': 'Géant de Bouscat', 'Prix_Vente': 15000, 'Poids_kg': 4.5},
        {'Race': 'Papillon', 'Prix_Vente': 13000, 'Poids_kg': 3.8}
    ]

# 4. EN-TÊTE AVEC LOGO (Gestion du logo par défaut)
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
logo_path = 'logo.png'
if os.path.exists(logo_path):
    st.image(Image.open(logo_path), width=120)
else:
    # Logo par défaut si le fichier n'est pas là
    st.markdown("<h1 style='font-size: 80px; margin: 0;'>🐇</h1>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<h1>LapinEco Pro+</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Expertise en Collecte et Analyse de Données Cunicoles</p>", unsafe_allow_html=True)

df = pd.DataFrame(st.session_state.liste_ventes)

# 5. ESPACE DE TRAVAIL
tab1, tab2, tab3 = st.tabs(["📊 DATA HUB", "💰 FINANCES", "📈 ANALYTICS"])

with tab1:
    st.subheader("Base Centrale des Ventes")
    st.dataframe(df, use_container_width=True)
    
    with st.expander("➕ Enregistrer une Nouvelle Transaction"):
        with st.form("form_lapin", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            race = c1.text_input("Race", placeholder="ex: Calfornie")
            poids = c2.number_input("Poids (kg)", min_value=0.1, step=0.1)
            prix = c3.number_input("Prix (FCFA)", min_value=0, step=500)
            if st.form_submit_button("VALIDER L'ENREGISTREMENT"):
                if race:
                    st.session_state.liste_ventes.append({'Race': race, 'Prix_Vente': prix, 'Poids_kg': poids})
                    st.success(f"Vente de {race} ajoutée !")
                    st.rerun()

with tab2:
    st.subheader("Indicateurs Financiers")
    if not df.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("CA TOTAL", f"{df['Prix_Vente'].sum():,} FCFA")
        c2.metric("PRIX MOYEN", f"{df['Prix_Vente'].mean():,.0f} FCFA")
        c3.metric("POIDS MOYEN", f"{df['Poids_kg'].mean():.2f} kg")
        st.markdown("#### Transactions Récentes")
        st.table(df.tail(5))

with tab3:
    st.subheader("Analyses Visuelles")
    plt.style.use('dark_background')
    if len(df) > 1:
        col1, col2 = st.columns(2)
        with col1:
            fig1, ax1 = plt.subplots()
            df['Race'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax1, colors=sns.color_palette('Reds'))
            ax1.set_ylabel('')
            st.pyplot(fig1)
        with col2:
            fig2, ax2 = plt.subplots()
            sns.regplot(data=df, x='Poids_kg', y='Prix_Vente', ax=ax2, scatter_kws={'color': '#FF1744'}, line_kws={'color': 'white'})
            st.pyplot(fig2)
    else:
        st.info("Besoin de plus de données pour les graphiques.")
