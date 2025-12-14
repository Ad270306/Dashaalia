import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Dashaalia Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS PERSONNALISÉ (Look & Feel) ---
st.markdown("""
    <style>
        /* Import de la police Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* --- FOND GLOBAL --- */
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Inter', sans-serif;
        }
        
        /* --- CONTENEUR PRINCIPAL --- */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* --- SIDEBAR STYLING --- */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%);
            padding: 2rem 1rem;
        }
        
        [data-testid="stSidebar"] * {
            color: #e2e8f0 !important;
        }
        
        [data-testid="stSidebar"] h1 {
            color: #ffffff !important;
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        
        [data-testid="stSidebar"] .stMarkdown {
            color: #cbd5e0 !important;
        }
        
        /* --- CARTES MODERNISÉES --- */
        div[data-testid="stMetric"], 
        div[data-testid="stPlotlyChart"],
        div[data-testid="column"] > div {
            background: rgba(255, 255, 255, 0.95);
            padding: 1.8rem;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
            border: none;
            backdrop-filter: blur(10px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        div[data-testid="stMetric"]:hover,
        div[data-testid="stPlotlyChart"]:hover {
            transform: translateY(-4px);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
        }
        
        /* --- TYPOGRAPHIE --- */
        h1, h2, h3 {
            color: #ffffff !important;
            font-family: 'Inter', sans-serif;
            font-weight: 700;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        }
        
        h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        
        h2 {
            font-size: 1.3rem;
            color: #2d3748 !important;
            text-shadow: none;
            margin-bottom: 1rem;
        }
        
        /* --- MÉTRIQUES STYLISÉES --- */
        [data-testid="stMetricValue"] {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 0.9rem;
            color: #718096 !important;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        [data-testid="stMetricDelta"] {
            font-size: 0.85rem;
        }
        
        /* --- DATAFRAME STYLING --- */
        [data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
        }
        
        /* --- SÉPARATEURS --- */
        hr {
            margin: 2rem 0;
            border: none;
            height: 1px;
            background: rgba(255, 255, 255, 0.2);
        }
        
        /* --- MESSAGES INFO/WARNING --- */
        .stAlert {
            border-radius: 12px;
            border: none;
            backdrop-filter: blur(10px);
        }
        
        /* --- ANIMATIONS --- */
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        div[data-testid="stMetric"],
        div[data-testid="stPlotlyChart"] {
            animation: fadeIn 0.6s ease-out;
        }
        
        /* --- SCROLLBAR PERSONNALISÉE --- */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: rgba(102, 126, 234, 0.5);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(102, 126, 234, 0.8);
        }
    </style>
""", unsafe_allow_html=True)

# URL de l'API
API_URL = "http://127.0.0.1:8000"

# Fonction helper pour requêter l'API sans faire crasher l'app
def get_data(endpoint):
    try:
        response = requests.get(f"{API_URL}{endpoint}", timeout=2) # Timeout court pour ne pas bloquer
        if response.status_code == 200:
            return response.json()
    except Exception:
        return None
    return None

# --- SIDEBAR (Barre latérale) ---
with st.sidebar:
    # Vérification du statut de l'API
    api_status = get_data("/api/stats/overview") is not None
    status_icon = "🟢" if api_status else "🔴"
    status_text = "En ligne" if api_status else "Déconnecté"

    st.title("🏥 Dashaalia")
    st.caption(f"Statut API: {status_icon} {status_text}")
    st.markdown("---")
    st.write("Tableau de bord analytique des consultations médicales.")
    st.markdown("###")
    
    if not api_status:
         st.warning("⚠️ L'API semble éteinte. Lancez `python -m uvicorn main:app --reload`.")

# --- CONTENU PRINCIPAL ---

# Titre
st.header("📊 Vue d'ensemble des Performances")
st.markdown("---")

# --- SECTION 1: KPI CARDS ---
overview = get_data("/api/stats/overview")

if overview and overview.get("total_sessions") is not None:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Sessions Totales", value=overview.get("total_sessions", 0))
    with col2:
        avg_dur = overview.get('avg_duration')
        st.metric(label="Durée Moyenne", value=f"{avg_dur:.1f} min" if avg_dur else "N/A")
    with col3:
        avg_note = overview.get('avg_note')
        st.metric(label="Note Moyenne", value=f"{avg_note:.2f} / 5" if avg_note else "N/A")
    with col4:
        avg_qual = overview.get('avg_quality')
        # Petit indicateur de couleur selon le score
        delta_color = "normal"
        if avg_qual and avg_qual > 4.5: delta_color = "inverse" # Vert
        elif avg_qual and avg_qual < 3: delta_color = "off"     # Rouge

        st.metric(label="Qualité Score", value=f"{avg_qual:.2f}" if avg_qual else "N/A", delta="Objectif: 5.0", delta_color=delta_color)
elif api_status:
     st.info("ℹ️ La base de données est vide. Lancez le script d'importation.")

st.markdown("###") # Espacement

# --- SECTION 2: GRAPHIQUES ---
# Utilisation de conteneurs (st.container) pour mieux appliquer le style CSS de "carte"
col_left, col_right = st.columns([2, 1]) # La colonne de gauche est 2x plus large

with col_left:
    with st.container():
        st.subheader("📈 Tendance des sessions (Journalier)")
        daily_data = get_data("/api/stats/daily")
        if daily_data and len(daily_data) > 0:
            df_daily = pd.DataFrame(daily_data)
            fig = px.area(df_daily, x="date", y="sessions_count", template="plotly_white")
            fig.update_traces(line_color='#667eea', fillcolor="rgba(102, 126, 234, 0.3)", line_width=3)
            fig.update_layout(
                xaxis_title=None, 
                yaxis_title=None, 
                margin=dict(l=20, r=20, t=40, b=20), 
                height=350,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter, sans-serif", color="#2d3748")
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.caption("Pas de données temporelles disponibles.")

with col_right:
    with st.container():
        st.subheader("🌍 Top Langues")
        lang_data = get_data("/api/stats/top-languages")
        if lang_data and len(lang_data) > 0:
            df_langs = pd.DataFrame(lang_data)
            colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b']
            fig = px.pie(df_langs, names="_id", values="count", hole=0.6, template="plotly_white", color_discrete_sequence=colors)
            fig.update_traces(textinfo='percent+label', textposition='outside', textfont_size=12)
            fig.update_layout(
                showlegend=False, 
                margin=dict(l=20, r=20, t=40, b=20), 
                height=350,
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter, sans-serif", color="#2d3748")
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
             st.caption("Pas de données de langues disponibles.")

# --- SECTION 3: SERVICES & INTERACTIONS ---
st.markdown("###")
col3, col4 = st.columns(2)

with col3:
    with st.container():
        st.subheader("🏥 Répartition par Service")
        service_data = get_data("/api/stats/by-service")
        if service_data and len(service_data) > 0:
            df_service = pd.DataFrame(service_data)
            colors_gradient = ['#667eea', '#7c6bef', '#9258f4', '#a845f9', '#be32fe']
            fig = px.bar(df_service, y="_id", x="count", orientation='h', template="plotly_white", color="_id", color_discrete_sequence=colors_gradient)
            fig.update_layout(
                showlegend=False, 
                xaxis_title="Nombre de Sessions", 
                yaxis_title=None, 
                margin=dict(l=20, r=20, t=40, b=20), 
                height=350,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter, sans-serif", color="#2d3748")
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
             st.caption("Pas de données de services disponibles.")

with col4:
    with st.container():
        st.subheader("💬 Radar des Interactions")
        inter = get_data("/api/stats/interactions")
        if inter and inter.get('avg_total'):
            categories = ['Patient', 'Praticien', 'Total Moy.']
            values = [inter.get('avg_patient', 0), inter.get('avg_praticien', 0), inter.get('avg_total', 0)]
            # Pour fermer le radar, il faut répéter la première valeur à la fin
            values.append(values[0])
            categories.append(categories[0])
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                line_color='#667eea',
                line_width=3,
                fillcolor="rgba(102, 126, 234, 0.3)",
                marker=dict(size=8, color='#764ba2')
            ))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, max(values)+1], gridcolor='rgba(0,0,0,0.1)'),
                    angularaxis=dict(gridcolor='rgba(0,0,0,0.1)')
                ), 
                template="plotly_white",
                margin=dict(l=40, r=40, t=40, b=40), 
                height=350,
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter, sans-serif", color="#2d3748")
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
             st.caption("Pas de données d'interactions disponibles.")

# --- DERNIÈRES SESSIONS ---
st.markdown("---")
with st.container():
    st.subheader("📋 Historique Récent")
    sessions = get_data("/api/sessions?limit=15")
    if sessions and len(sessions) > 0:
        df_s = pd.DataFrame(sessions)
        cols_wanted = ["date", "service", "langue", "duree_minutes", "note_praticien", "qualite_score"]
        # On ne garde que les colonnes qui existent vraiment dans les données
        avail_cols = [c for c in cols_wanted if c in df_s.columns]
        
        st.dataframe(
            df_s[avail_cols].style.format({"note_praticien": "{:.1f}", "qualite_score": "{:.1f}"}),
            use_container_width=True,
            height=400
        )
    elif api_status:
        st.caption("Aucune session trouvée en base.")
