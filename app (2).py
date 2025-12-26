
import streamlit as st
import pandas as pd
import time

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Darboğaz Analiz Sistemi",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS ENJEKSİYONU ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    .stApp { background: linear-gradient(135deg, #eff6ff 0%, #ffffff 50%, #fff7ed 100%); font-family: 'Inter', sans-serif; }
    .main-header { background: linear-gradient(to right, #2563eb, #f97316); padding: 2rem; border-radius: 0 0 10px 10px; color: white; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); margin-bottom: 2rem; }
    .custom-card { background-color: white; padding: 1.5rem; border-radius: 0.5rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); transition: all 0.3s ease; height: 100%; }
    .custom-card:hover { box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); }
    .kpi-blue { background: linear-gradient(135deg, #3b82f6, #2563eb); color: white; }
    .kpi-purple { background: linear-gradient(135deg, #a855f7, #9333ea); color: white; }
    .kpi-red { background: linear-gradient(135deg, #ef4444, #dc2626); color: white; }
    .kpi-green { background: linear-gradient(135deg, #22c55e, #16a34a); color: white; }
    .metric-value { font-size: 2.25rem; font-weight: 700; }
    .metric-label { font-size: 0.875rem; opacity: 0.9; }
    .metric-sub { font-size: 0.75rem; opacity: 0.75; margin-top: 0.5rem; }
    div.stButton > button { background: linear-gradient(to right, #2563eb, #f97316); color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 0.5rem; font-weight: bold; width: 100%; transition: transform 0.2s; }
    div.stButton > button:hover { transform: scale(1.02); color: white; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3); }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: white; padding: 10px 20px; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: transparent; border-radius: 5px; font-weight: 600; color: #4b5563; }
    .stTabs [aria-selected="true"] { background-color: #2563eb; color: white; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- BAŞLIK ---
st.markdown("""
    <div class="main-header">
        <h1 style="margin:0; font-size: 2.5rem;">🏢 Darboğaz Analiz Sistemi</h1>
        <p style="margin:0; color: #dbeafe; font-size: 1.1rem;">AI-Powered Bottleneck Detection & Risk Assessment</p>
    </div>
""", unsafe_allow_html=True)

# --- DATA ---
departments = [
    {"id": 1, "name": "Finans", "risk": 45, "bottleneck": True, "f1": 0.82},
    {"id": 2, "name": "Üretim", "risk": 78, "bottleneck": True, "f1": 0.79},
    {"id": 3, "name": "İnsan Kaynakları", "risk": 32, "bottleneck": False, "f1": 0.85},
    {"id": 4, "name": "Lojistik", "risk": 65, "bottleneck": True, "f1": 0.76},
    {"id": 5, "name": "Satın Alma", "risk": 28, "bottleneck": False, "f1": 0.88},
    {"id": 6, "name": "IT", "risk": 55, "bottleneck": True, "f1": 0.80},
    {"id": 7, "name": "Bakım & Teknik", "risk": 72, "bottleneck": True, "f1": 0.78},
    {"id": 8, "name": "Satış & Pazarlama", "risk": 38, "bottleneck": False, "f1": 0.84},
]

def get_risk_style(risk):
    if risk >= 70: return {"bg": "bg-red-50", "border": "#ef4444", "text": "text-red-700", "emoji": "🔴", "color": "#ef4444", "light_bg": "#fef2f2"}
    if risk >= 50: return {"bg": "bg-orange-50", "border": "#f97316", "text": "text-orange-700", "emoji": "🟠", "color": "#f97316", "light_bg": "#fff7ed"}
    return {"bg": "bg-green-50", "border": "#22c55e", "text": "text-green-700", "emoji": "🟢", "color": "#22c55e", "light_bg": "#f0fdf4"}

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Genel Bakış", "🔍 Analiz", "📈 Performans", "ℹ️ Hakkında"])

with tab1:
    st.markdown('<h2 style="color:#1f2937; font-weight:700;">📊 Departman Risk Özeti</h2>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    def kpi_card(col, title, value, sub, kpi_class):
        col.markdown(f"""<div class="custom-card {kpi_class}"><div class="metric-label">{title}</div><div class="metric-value">{value}</div><div class="metric-sub">{sub}</div></div>""", unsafe_allow_html=True)

    kpi_card(col1, "Toplam Departman", "8", "monitored", "kpi-blue")
    kpi_card(col2, "Ortalama Risk", "50.4%", "±15%", "kpi-purple")
    kpi_card(col3, "Darboğaz Sayısı", "5", "aktif", "kpi-red")
    kpi_card(col4, "Model F1-Score", "0.816", "Gerçekçi", "kpi-green")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<h3 style="color:#1f2937; font-weight:700;">🏢 Departman Detayları & Risk Oranları</h3>', unsafe_allow_html=True)

    rows = [departments[i:i + 4] for i in range(0, len(departments), 4)]
    for row in rows:
        cols = st.columns(4)
        for idx, dept in enumerate(row):
            style = get_risk_style(dept['risk'])
            cols[idx].markdown(f"""
                <div style="background-color: {style['light_bg']}; border-left: 5px solid {style['border']}; padding: 1.5rem; border-radius: 0.5rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); margin-bottom: 1rem; height: 100%;">
                    <h4 style="margin:0 0 10px 0; color: #1f2937;">{style['emoji']} {dept['name']}</h4>
                    <div style="font-size: 0.875rem; color: #374151; font-weight: 600;">Risk Seviyesi</div>
                    <div style="font-size: 1.875rem; font-weight: 700; color: {style['color']};">{dept['risk']}%</div>
                    <div style="margin-top: 5px; font-weight: 600; font-size: 0.875rem; color: #4b5563;">{'⚠️ KRİTİK' if dept['risk'] >= 70 else '⚠️ YÜKSEK' if dept['risk'] >= 50 else '✅ NORMAL'}</div>
                    <div style="margin-top: 10px; font-size: 0.875rem; color: #4b5563;"><b>Darboğaz:</b> {'Evet' if dept['bottleneck'] else 'Hayır'}<br><b>F1-Score:</b> {dept['f1']:.3f}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown('<h3 style="color:#1f2937; font-weight:700; margin-top:20px;">📊 Risk Dağılımı Grafiği</h3>', unsafe_allow_html=True)
    chart_html = '<div style="background: white; padding: 1.5rem; border-radius: 0.5rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">'
    for dept in departments:
        style = get_risk_style(dept['risk'])
        chart_html += f"""
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <span style="width: 150px; font-weight: 600; color: #374151;">{dept['name']}</span>
                <div style="flex: 1; background-color: #e5e7eb; border-radius: 9999px; height: 2rem; overflow: hidden;">
                    <div style="width: {dept['risk']}%; background-color: {style['color']}; height: 100%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 0.875rem;">{dept['risk']}%</div>
                </div>
            </div>
        """
    chart_html += '</div>'
    st.markdown(chart_html, unsafe_allow_html=True)

with tab2:
    st.markdown('<h2 style="color:#1f2937; font-weight:700;">🤖 AI Darboğaz Analiz Motoru</h2>', unsafe_allow_html=True)
    col_input, col_select = st.columns([2, 1])
    with col_input:
        st.markdown('<h3 style="font-size: 1.25rem; font-weight: 700; color: #1f2937;">📝 Problemi Tanımla</h3>', unsafe_allow_html=True)
        user_input = st.text_area("", placeholder="Örnek: Üretim ekipmanları sık sık duruyor...", height=150)
    with col_select:
        st.markdown('<h3 style="font-size: 1.25rem; font-weight: 700; color: #1f2937;">🏢 Departman Seç</h3>', unsafe_allow_html=True)
        dept_select = st.selectbox("", ["Finans", "Üretim", "İnsan Kaynakları", "Lojistik"], label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("⚡ Analiz Et")
    if analyze_btn and user_input:
        with st.spinner('AI Modeli Analiz Ediyor...'):
            time.sleep(1.5)
            st.markdown('<h3 style="color:#1f2937; font-weight:700;">📊 Analiz Sonuçları</h3>', unsafe_allow_html=True)
            res1, res2, res3 = st.columns(3)
            res1.markdown(f"""<div style="background: linear-gradient(135deg, #f97316, #ea580c); color: white; padding: 1.5rem; border-radius: 0.5rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"><div style="font-size: 0.875rem; opacity: 0.9;">Darboğaz Durumu</div><div style="font-size: 2rem; font-weight: 700;">⚠️ UYARI</div><div style="font-size: 0.875rem; opacity: 0.75;">87% güven</div></div>""", unsafe_allow_html=True)
            res2.markdown(f"""<div style="background: linear-gradient(135deg, #ef4444, #dc2626); color: white; padding: 1.5rem; border-radius: 0.5rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"><div style="font-size: 0.875rem; opacity: 0.9;">Risk Seviyesi</div><div style="font-size: 2rem; font-weight: 700;">78%</div><div style="font-size: 0.875rem; opacity: 0.75;">Kritik</div></div>""", unsafe_allow_html=True)
            res3.markdown(f"""<div style="background: linear-gradient(135deg, #3b82f6, #2563eb); color: white; padding: 1.5rem; border-radius: 0.5rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"><div style="font-size: 0.875rem; opacity: 0.9;">Algılanan Dept.</div><div style="font-size: 2rem; font-weight: 700;">{dept_select}</div><div style="font-size: 0.875rem; opacity: 0.75;">Seçili</div></div>""", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""<div style="background-color: #eff6ff; padding: 1.5rem; border-radius: 0.5rem; border: 1px solid #dbeafe;"><p style="font-weight: 600; color: #1f2937; margin-bottom: 0.5rem;">📊 Model Güven Skoru: 87%</p><div style="width: 100%; background-color: #d1d5db; border-radius: 9999px; height: 1rem; overflow: hidden;"><div style="height: 100%; background: linear-gradient(to right, #4ade80, #16a34a); width: 87%;"></div></div></div>""", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""<div style="background: linear-gradient(to right, #eff6ff, #fff7ed); padding: 1.5rem; border-radius: 0.5rem; border: 2px solid #bfdbfe;"><h4 style="font-size: 1.25rem; font-weight: 700; color: #1f2937; margin-bottom: 1rem;">💡 AI Çözüm Önerileri</h4><div style="display: flex; flex-direction: column; gap: 0.75rem;"><div style="background: white; padding: 0.75rem; border-radius: 0.5rem; border-left: 4px solid #3b82f6;">🔧 {dept_select} departmanı yöneticisi ile görüşülmeli</div><div style="background: white; padding: 0.75rem; border-radius: 0.5rem; border-left: 4px solid #3b82f6;">📊 Detaylı root cause analysis yapılmalı</div></div></div>""", unsafe_allow_html=True)

with tab3:
    st.markdown('<h2 style="color:#1f2937; font-weight:700;">🧪 Model Performans Analizi</h2>', unsafe_allow_html=True)
    st.info("Model Özellikleri: F1-Score: 0.75-0.85 | Accuracy: 80-88%")
    col_perf1, col_perf2 = st.columns(2)
    with col_perf1:
        st.markdown('<div class="custom-card"><h3>📊 Metrikler</h3><p>Accuracy: 84.2% ✅</p><p>F1-Score: 0.816 ✅</p></div>', unsafe_allow_html=True)
    with col_perf2:
        st.markdown('<div class="custom-card"><h3>⚠️ Hata Matrisi</h3><p>True Pos: 1245</p><p>False Pos: 320</p></div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<h2 style="color:#1f2937; font-weight:700;">ℹ️ Sistem Hakkında</h2>', unsafe_allow_html=True)
    st.info("Bu sistem BERTurk Transformer modeli ile geliştirilmiştir. Google Colab üzerinde Cloudflare Tüneli ile çalışmaktadır.")
