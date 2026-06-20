import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ============== PAGE CONFIG ==============
st.set_page_config(
    page_title="Melaju Menuju Masa Depan: EV Indonesia",
    page_icon="🚗⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============== CUSTOM CSS ==============
st.markdown("""
<style>
    .main { background-color: #0d1b2a; }
    .stApp { background: linear-gradient(180deg, #0d1b2a 0%, #1b2a41 100%); }
    h1, h2, h3, h4, p, span, label, .stMarkdown { color: #e8f1f2; }
    .metric-card {
        background: linear-gradient(135deg, #16324f 0%, #1b4965 100%);
        border-radius: 14px;
        padding: 18px 20px;
        border: 1px solid #2c6e91;
    }
    .big-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #5fd068, #62cdff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
    }
    .section-badge {
        display: inline-block;
        background: #5fd068;
        color: #0d1b2a !important;
        border-radius: 8px;
        padding: 2px 10px;
        font-weight: 700;
        margin-right: 8px;
    }
    div[data-testid="stMetricValue"] { color: #5fd068; }
    div[data-testid="stMetricLabel"] { color: #cfe8ef; }
</style>
""", unsafe_allow_html=True)

# ============== DATA ==============
trend_df = pd.DataFrame({
    "Tahun": [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
    "Penjualan EV": [2, 0, 2, 0, 0, 27, 2, 91, 363, 761, 11079, 17560, 49150, 115300, None]
})
# Note: 2025 full-year not yet known; only Q1 known separately
trend_df = trend_df[trend_df["Tahun"] <= 2024]

q1_df = pd.DataFrame({
    "Periode": ["Q1 2024 (Jan-Mar 2024)", "Q1 2025 (Jan-Mar 2025)"],
    "Penjualan EV": [19260, 27616]
})

faktor_pendorong = [
    "Insentif PPN dan PPnBM",
    "Masuknya merek EV baru",
    "Harga EV semakin kompetitif",
    "Dukungan pemerintah terhadap industri baterai nasional"
]

merek_ev = ["BYD", "VinFast", "Wuling", "Chery"]

pangsa_df = pd.DataFrame({
    "Kategori": ["EV", "Non-EV"],
    "Persentase": [18, 82]
})

tantangan = {
    "Infrastruktur": "Jumlah charging station belum merata, banyak daerah belum memiliki SPKLU.",
    "Harga Kendaraan": "Harga EV masih relatif lebih tinggi dibandingkan kendaraan non-EV.",
    "Jarak Tempuh & Pengisian Daya": "Masih menjadi kekhawatiran calon pengguna EV.",
    "Dampak Lingkungan Industri Nikel": "Pertambangan nikel mendukung industri baterai, akan tetapi menimbulkan tantangan baru."
}

infrastruktur_poin = [
    "Perkembangan SPKLU terus dilakukan.",
    "Infrastruktur menjadi fokus utama bagi pemerintah dan PLN.",
    "Teknologi ultra fast charging mulai masuk ke Indonesia."
]

roadmap_df = pd.DataFrame({
    "Tahun": ["2025", "2026", "2027", "2030"],
    "Milestone": [
        "Pertumbuhan penjualan EV dan perluasan insentif pemerintah.",
        "Operasional pabrik baterai EV hasil kerja sama Indonesia-CATL di Jawa Barat.",
        "Penguatan ekosistem baterai dan manufaktur EV nasional.",
        "Produksi 600.000 mobil listrik & 2,45 juta motor listrik per tahun. Indonesia ditargetkan menjadi pusat industri EV dan baterai ASEAN."
    ]
})

# ============== SIDEBAR FILTERS ==============
st.sidebar.title("⚙️ Filter & Navigasi")
st.sidebar.markdown(
    "Gunakan filter di bawah untuk mengeksplorasi data perkembangan kendaraan listrik di Indonesia.")

tahun_range = st.sidebar.slider(
    "Rentang Tahun (Tren Penjualan EV)",
    min_value=int(trend_df["Tahun"].min()),
    max_value=int(trend_df["Tahun"].max()),
    value=(2011, 2024)
)

tantangan_pilih = st.sidebar.multiselect(
    "Pilih Tantangan yang ingin ditampilkan",
    options=list(tantangan.keys()),
    default=list(tantangan.keys())
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Anggota Kelompok 6:** \n\n1. Najwa Anisa Putri\n2. Hasna Rofifah Wardani\n3. Dewi Nur'Aini")

# ============== HEADER ==============
st.markdown('<div class="big-title">🚗⚡ MELAJU MENUJU MASA DEPAN</div>',
            unsafe_allow_html=True)
st.markdown(
    "#### Perkembangan, Tren, dan Tantangan Kendaraan Listrik di Indonesia")
st.markdown(
    "Kendaraan listrik (*Electric Vehicle*/EV) menjadi salah satu inovasi penting dalam transformasi "
    "transportasi modern. Di Indonesia, pertumbuhan penjualan EV terus menunjukkan tren positif seiring "
    "dukungan pemerintah, perkembangan teknologi, serta meningkatnya kesadaran masyarakat terhadap energi "
    "yang lebih ramah lingkungan."
)
st.markdown("---")

# ============== ROW 1: KPI METRICS ==============
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Penjualan EV Q1 2025", "27.616 unit", "+43,4% vs Q1 2024")
with col2:
    st.metric("Penjualan EV Q1 2024", "19.260 unit")
with col3:
    st.metric("Penjualan EV 2024 (Total)", "115.300 unit")
with col4:
    st.metric("Pangsa Pasar EV 2025", "18%",
              "dari total penjualan kendaraan baru")

st.markdown("---")

# ============== ROW 2: Q1 COMPARISON + TREND LINE ==============
col_left, col_right = st.columns([1, 1.4])

with col_left:
    st.markdown('<span class="section-badge">1</span> **Pertumbuhan Penjualan EV Q1 2025**',
                unsafe_allow_html=True)
    fig_bar = go.Figure(go.Bar(
        x=q1_df["Periode"],
        y=q1_df["Penjualan EV"],
        text=q1_df["Penjualan EV"],
        texttemplate="%{text:,}",
        textposition="outside",
        marker_color=["#62cdff", "#5fd068"]
    ))
    fig_bar.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#e8f1f2",
        yaxis_title="Unit Terjual",
        height=380,
        margin=dict(t=20, b=20)
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.caption(
        "Sebanyak 27.616 EV terjual pada Q1 2025, naik dari 19.260 EV di periode yang sama tahun lalu (+43,4%).")

with col_right:
    st.markdown('<span class="section-badge">2</span> **Perkembangan Kendaraan Listrik di Indonesia (2011–2024)**', unsafe_allow_html=True)
    filtered_trend = trend_df[(trend_df["Tahun"] >= tahun_range[0]) & (
        trend_df["Tahun"] <= tahun_range[1])]
    fig_line = px.area(
        filtered_trend, x="Tahun", y="Penjualan EV",
        markers=True
    )
    fig_line.update_traces(line_color="#5fd068",
                           fillcolor="rgba(95,208,104,0.25)")
    fig_line.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#e8f1f2",
        yaxis_title="Unit Terjual",
        height=380,
        margin=dict(t=20, b=20)
    )
    st.plotly_chart(fig_line, use_container_width=True)
    st.caption(
        "Geser slider di sidebar untuk menyaring rentang tahun yang ditampilkan.")

st.markdown("---")

# ============== ROW 3: FAKTOR PENDORONG + TREN SAAT INI ==============
col3a, col3b = st.columns([1, 1])

with col3a:
    st.markdown('<span class="section-badge">3</span> **Faktor Pendorong Kenaikan Penjualan EV**',
                unsafe_allow_html=True)
    for f in faktor_pendorong:
        st.markdown(f"✅ {f}")

with col3b:
    st.markdown('<span class="section-badge">4</span> **Tren Kendaraan Listrik Saat Ini**',
                unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📊 Pangsa Pasar EV", "🚙 Merek EV Populer"])
    with tab1:
        fig_pie = px.pie(
            pangsa_df, names="Kategori", values="Persentase",
            color="Kategori",
            color_discrete_map={"EV": "#5fd068", "Non-EV": "#3a4a5e"},
            hole=0.45
        )
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#e8f1f2",
            height=320,
            margin=dict(t=10, b=10)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        st.caption("EV mencapai sekitar 18% dari total penjualan kendaraan baru pada 2025. Lebih dari 75% penjualan mobil listrik Indonesia berasal dari Cina.")
    with tab2:
        st.markdown("Merek EV yang ramai masuk pasar Indonesia:")
        chip_cols = st.columns(len(merek_ev))
        for c, m in zip(chip_cols, merek_ev):
            c.markdown(f"**🔋 {m}**")
        st.info("Harga EV semakin terjangkau dibanding beberapa tahun sebelumnya.")

st.markdown("---")

# ============== ROW 4: INFRASTRUKTUR + TANTANGAN ==============
col4a, col4b = st.columns([1, 1])

with col4a:
    st.markdown('<span class="section-badge">5</span> **Infrastruktur EV di Indonesia**',
                unsafe_allow_html=True)
    for p in infrastruktur_poin:
        st.markdown(f"⚡ {p}")

with col4b:
    st.markdown('<span class="section-badge">6</span> **Tantangan yang Masih Dihadapi**',
                unsafe_allow_html=True)
    if tantangan_pilih:
        for t in tantangan_pilih:
            with st.expander(f"⚠️ {t}"):
                st.write(tantangan[t])
    else:
        st.warning("Pilih minimal satu tantangan di sidebar untuk ditampilkan.")

st.markdown("---")

# ============== ROW 5: ROADMAP ==============
st.markdown('<span class="section-badge">7</span> **Masa Depan Kendaraan Listrik (Roadmap 2025–2030)**',
            unsafe_allow_html=True)
roadmap_cols = st.columns(len(roadmap_df))
icons = ["📈", "🏭", "🔋", "🌏"]
for col, (_, row), icon in zip(roadmap_cols, roadmap_df.iterrows(), icons):
    with col:
        st.markdown(f"### {icon} {row['Tahun']}")
        st.write(row["Milestone"])

st.markdown("---")
st.caption("""
Sumber:

1. PwC Indonesia. (2025, November 25). Indonesia’s EV market grew by 49%.
https://www.pwc.com/id/en/media-centre/press-release/2025/english/indonesia-ev-market-grew-by-49.html

2. Indonesia’s EV market shows strong growth despite broader industry challenges. (2025, June 17).
https://www.pwc.com/id/en/media-centre/press-release/2025/english/indonesias-ev-market-shows-strong-growth-despite-broader-industry-challenges.html

3. PwC Indonesia. (2025, June 17). Indonesia’s EV market shows strong growth despite broader industry challenges.
https://www.pwc.com/id/en/media-centre/press-release/2025/english/indonesias-ev-market-shows-strong-growth-despite-broader-industry-challenges.html
""")
