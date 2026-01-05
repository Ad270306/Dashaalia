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
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #cbd5e1 100%);
            font-family: 'Inter', sans-serif;
        }
        
        /* --- CONTENEUR PRINCIPAL --- */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 100%;
        }
        
        /* --- SIDEBAR STYLING --- */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 100%) !important;
            padding: 2rem 1rem;
        }
        
        [data-testid="stSidebar"] * {
            color: #ffffff !important;
        }
        
        [data-testid="stSidebar"] h1 {
            color: #ffffff !important;
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        [data-testid="stSidebar"] .css-1v0mbdj, 
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] .stMarkdown {
            color: #e0e7ff !important;
            font-weight: 500;
        }
        
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"],
        [data-testid="stSidebar"] .stCaption {
            color: #c7d2fe !important;
            font-weight: 600;
        }
        
        /* Style pour la boîte des métriques dans la sidebar */
        .sidebar-metrics {
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            padding: 1.2rem;
            margin: 1.5rem 0;
            backdrop-filter: blur(10px);
        }
        
        .sidebar-metrics h3 {
            color: #ffffff !important;
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .sidebar-metrics p {
            color: #e0e7ff !important;
            font-size: 0.9rem;
            margin: 0.5rem 0;
            line-height: 1.6;
        }
        
        .sidebar-metrics strong {
            color: #ffffff !important;
            font-weight: 700;
        }
        
        /* Uniformisation des hauteurs des cartes métriques avec alignement parfait */
        div[data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.98);
            padding: 1.8rem;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
            border: 1px solid rgba(226, 232, 240, 0.8);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            min-height: 160px;
            height: 160px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        
        div[data-testid="stMetric"]:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.18);
        }
        
        /* Style des conteneurs de graphiques pour uniformiser les tailles */
        div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
            background: rgba(255, 255, 255, 0.98);
            padding: 1.5rem;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
            border: 1px solid rgba(226, 232, 240, 0.8);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            height: 100%;
        }
        
        div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
        }
        
        /* --- TYPOGRAPHIE --- */
        h1 {
            color: #1e293b !important;
            font-family: 'Inter', sans-serif;
            font-weight: 700;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        h2, h3 {
            color: #1e293b !important;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            text-shadow: none;
            margin-bottom: 1rem;
        }
        
        /* Amélioration du style des métriques */
        [data-testid="stMetricValue"] {
            font-size: 2.8rem !important;
            font-weight: 700 !important;
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 0.9rem !important;
            color: #64748b !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 0.5rem;
        }
        
        [data-testid="stMetricDelta"] {
            font-size: 0.85rem !important;
            font-weight: 500;
        }
        
        /* --- DATAFRAME STYLING --- */
        [data-testid="stDataFrame"] {
            background: rgba(255, 255, 255, 0.98);
            padding: 1rem;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
        }
        
        /* --- SÉPARATEURS --- */
        hr {
            margin: 2.5rem 0;
            border: none;
            height: 2px;
            background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.4), transparent);
        }
        
        /* --- ANIMATIONS --- */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        div[data-testid="stMetric"],
        div[data-testid="stVerticalBlock"] {
            animation: fadeInUp 0.6s ease-out;
        }
        
        /* --- SCROLLBAR PERSONNALISÉE --- */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(226, 232, 240, 0.3);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: rgba(59, 130, 246, 0.6);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(59, 130, 246, 0.9);
        }
        
        /* Style pour les messages d'alerte */
        .stAlert {
            border-radius: 12px;
            border: none;
            backdrop-filter: blur(10px);
            background: rgba(255, 255, 255, 0.95) !important;
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
    
    overview = get_data("/api/stats/overview")
    if overview:
        st.markdown("""
            <div class="sidebar-metrics">
                <h3>📊 Données Récentes</h3>
            </div>
        """, unsafe_allow_html=True)
        
        total_sessions = overview.get('total_sessions', 0)
        avg_duration = overview.get('avg_duration', 0)
        avg_note = overview.get('avg_note', 0)
        
        st.markdown(f"""
            <div class="sidebar-metrics">
                <p><strong>Sessions Totales:</strong> {total_sessions}</p>
                <p><strong>Durée Moyenne:</strong> {avg_duration:.1f} min</p>
                <p><strong>Note Moyenne:</strong> {avg_note:.2f} / 5</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.write("Tableau de bord analytique des consultations médicales.")
    
    if not api_status:
         st.warning("⚠️ L'API semble éteinte. Lancez `python -m uvicorn main:app --reload`.")

# --- CONTENU PRINCIPAL ---

st.title("📊 Tableau de Bord Analytique")
st.markdown("---")

# --- SECTION 1: KPI CARDS ---
overview = get_data("/api/stats/overview")

if overview and overview.get("total_sessions") is not None:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Sessions Totales", value=f"{overview.get('total_sessions', 0):,}")
    with col2:
        avg_dur = overview.get('avg_duration', 0)
        st.metric(label="Durée Moyenne", value=f"{avg_dur:.1f} min")
    with col3:
        avg_note = overview.get('avg_note', 0)
        st.metric(label="Note Moyenne", value=f"{avg_note:.2f} / 5")
    with col4:
        avg_qual = overview.get('avg_quality', 0)
        delta_color = "normal"
        if avg_qual > 4.5: 
            delta_color = "inverse"
        elif avg_qual < 3: 
            delta_color = "off"
        st.metric(label="Qualité Score", value=f"{avg_qual:.2f}", delta="Objectif: 5.0", delta_color=delta_color)
elif api_status:
    st.info("ℹ️ La base de données est vide. Lancez le script d'importation.")

st.markdown("###")

col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📈 Tendance des Sessions")
    daily_data = get_data("/api/stats/daily")
    if daily_data and len(daily_data) > 0:
        df_daily = pd.DataFrame(daily_data)
        fig = px.area(df_daily, x="date", y="sessions_count", template="plotly_white")
        fig.update_traces(
            line_color='#3b82f6', 
            fillcolor="rgba(59, 130, 246, 0.3)", 
            line_width=3
        )
        fig.update_layout(
            xaxis_title="Date", 
            yaxis_title="Nombre de Sessions", 
            margin=dict(l=40, r=40, t=40, b=40), 
            height=400,
            plot_bgcolor='rgba(255,255,255,0.9)',
            paper_bgcolor='rgba(255,255,255,0.9)',
            font=dict(family="Inter, sans-serif", size=12, color="#1e293b"),
            xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Pas de données temporelles disponibles.")

with col_right:
    st.subheader("🌍 Top Langues")
    lang_data = get_data("/api/stats/top-languages")
    if lang_data and len(lang_data) > 0:
        df_langs = pd.DataFrame(lang_data)
        colors = ['#3b82f6', '#06b6d4', '#8b5cf6', '#ec4899', '#f59e0b']
        fig = px.pie(
            df_langs, 
            names="_id", 
            values="count", 
            hole=0.5, 
            template="plotly_white", 
            color_discrete_sequence=colors
        )
        fig.update_traces(
            textinfo='percent+label', 
            textposition='outside', 
            textfont_size=13,
            marker=dict(line=dict(color='white', width=2))
        )
        fig.update_layout(
            showlegend=False, 
            margin=dict(l=20, r=20, t=40, b=20), 
            height=400,
            paper_bgcolor='rgba(255,255,255,0.9)',
            font=dict(family="Inter, sans-serif", size=12, color="#1e293b")
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Pas de données de langues disponibles.")

st.markdown("###")

col3, col4 = st.columns(2)

with col3:
    st.subheader("🏥 Répartition par Service")
    service_data = get_data("/api/stats/by-service")
    if service_data and len(service_data) > 0:
        df_service = pd.DataFrame(service_data)
        fig = px.bar(
            df_service, 
            y="_id", 
            x="count", 
            orientation='h', 
            template="plotly_white"
        )
        fig.update_traces(
            marker_color='#3b82f6',
            marker_line_color='rgba(59, 130, 246, 0.3)',
            marker_line_width=1,
            texttemplate='%{x}',
            textposition='outside'
        )
        fig.update_layout(
            showlegend=False, 
            xaxis_title="Nombre de Sessions", 
            yaxis_title="Services", 
            margin=dict(l=20, r=40, t=40, b=40), 
            height=450,
            plot_bgcolor='rgba(255,255,255,0.9)',
            paper_bgcolor='rgba(255,255,255,0.9)',
            font=dict(family="Inter, sans-serif", size=12, color="#1e293b"),
            xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
            yaxis=dict(tickfont=dict(size=11, color="#1e293b"))
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Pas de données de services disponibles.")

with col4:
    st.subheader("💬 Interactions Moyennes")
    inter = get_data("/api/stats/interactions")
    if inter and inter.get('avg_total'):
        categories = ['Patient', 'Praticien', 'Total']
        values = [
            inter.get('avg_patient', 0), 
            inter.get('avg_praticien', 0), 
            inter.get('avg_total', 0)
        ]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            line_color='#3b82f6',
            line_width=3,
            fillcolor="rgba(59, 130, 246, 0.25)",
            marker=dict(size=10, color='#1e3a8a')
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True, 
                    range=[0, max(values) + 2], 
                    gridcolor='rgba(0,0,0,0.1)',
                    tickfont=dict(size=11, color="#1e293b")
                ),
                angularaxis=dict(
                    gridcolor='rgba(0,0,0,0.1)',
                    tickfont=dict(size=12, color="#1e293b")
                )
            ), 
            template="plotly_white",
            margin=dict(l=60, r=60, t=40, b=40), 
            height=450,
            paper_bgcolor='rgba(255,255,255,0.9)',
            font=dict(family="Inter, sans-serif", color="#1e293b")
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Pas de données d'interactions disponibles.")

st.markdown("---")

st.subheader("📋 Historique des Sessions Récentes")
sessions = get_data("/api/sessions?limit=20")
if sessions and len(sessions) > 0:
    df_s = pd.DataFrame(sessions)
    cols_wanted = ["date", "service", "langue", "duree_minutes", "note_praticien", "qualite_score"]
    avail_cols = [c for c in cols_wanted if c in df_s.columns]
    
    if avail_cols:
        styled_df = df_s[avail_cols].style.format({
            "note_praticien": "{:.1f}",
            "qualite_score": "{:.1f}",
            "duree_minutes": "{:.0f}"
        })
        
        st.dataframe(
            styled_df,
            use_container_width=True,
            height=450
        )
elif api_status:
    st.info("Aucune session trouvée en base.")
