import streamlit as st
import time
from logic import MultiQueueTol

st.set_page_config(
    page_title="Sistem Antrian Tol",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

* { font-family: 'Plus Jakarta Sans', sans-serif; }

.stApp {
    background: #07090F;
    color: #1a202c;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 3rem; max-width: 1200px; }

.hero-title {
    font-size: 2.2rem;
    font-weight: 700;
    color: #f0f4f8;
    margin-bottom: 0.2rem;
    letter-spacing: -0.03em;
}
.hero-accent { color: #2563eb; }
.hero-sub {
    font-size: 0.82rem;
    color: #94a3b8;
    margin-bottom: 2rem;
    font-weight: 500;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

.stat-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 1.2rem 1.4rem;
    border: 1px solid #e2e8f0;
    position: relative;
    overflow: hidden;
}
.stat-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 4px;
    border-radius: 0 0 16px 16px;
}
.stat-card.tol1::after { background: #3b82f6; }
.stat-card.tol2::after { background: #8b5cf6; }
.stat-card.tol3::after { background: #f59e0b; }
.stat-card.total::after { background: #10b981; }

.stat-label {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #94a3b8;
    margin-bottom: 0.4rem;
}
.stat-num {
    font-size: 2.4rem;
    font-weight: 700;
    line-height: 1;
    color: #1a202c;
}
.stat-card.tol1 .stat-num { color: #3b82f6; }
.stat-card.tol2 .stat-num { color: #8b5cf6; }
.stat-card.tol3 .stat-num { color: #f59e0b; }
.stat-card.total .stat-num { color: #10b981; }
.stat-desc { font-size: 0.75rem; color: #cbd5e1; margin-top: 0.35rem; }

.section-label {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    color: #94a3b8;
    margin-bottom: 0.9rem;
}

.lane {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 1.2rem;
    min-height: 260px;
}
.lane-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
    padding-bottom: 0.7rem;
    border-bottom: 1px solid #f1f5f9;
}
.lane-title { font-size: 0.82rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; }
.lane-badge {
    font-size: 0.68rem;
    padding: 0.18rem 0.55rem;
    border-radius: 999px;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
}
.lane.tol1 .lane-title { color: #2563eb; }
.lane.tol2 .lane-title { color: #7c3aed; }
.lane.tol3 .lane-title { color: #d97706; }
.lane.tol1 .lane-badge { background: #eff6ff; color: #2563eb; }
.lane.tol2 .lane-badge { background: #f5f3ff; color: #7c3aed; }
.lane.tol3 .lane-badge { background: #fffbeb; color: #d97706; }

.vehicle-chip {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 0.5rem 0.8rem;
    margin-bottom: 0.45rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    font-weight: 600;
    color: #334155;
    border-left: 3px solid;
}
.lane.tol1 .vehicle-chip { border-left-color: #3b82f6; }
.lane.tol2 .vehicle-chip { border-left-color: #8b5cf6; }
.lane.tol3 .vehicle-chip { border-left-color: #f59e0b; }
.vehicle-pos { font-size: 0.62rem; color: #cbd5e1; min-width: 1.2rem; }
.vehicle-icon { font-size: 0.95rem; }

.empty-lane {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 150px;
    color: #e2e8f0;
    font-size: 0.78rem;
    gap: 0.4rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 600;
}
.empty-icon { font-size: 1.8rem; opacity: 0.5; }

.log-container {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 1rem 1.4rem;
    max-height: 190px;
    overflow-y: auto;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
}
.log-entry { padding: 0.28rem 0; border-bottom: 1px solid #f8fafc; color: #94a3b8; }
.log-entry .log-time { color: #cbd5e1; margin-right: 0.8rem; }
.log-entry.success .log-msg { color: #059669; }
.log-entry.warning .log-msg { color: #d97706; }
.log-entry.info .log-msg { color: #2563eb; }

.stTextInput > label, .stSelectbox > label {
    color: #64748b !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.stTextInput input {
    background: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
    color: #1a202c !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.88rem !important;
}
.stSelectbox > div > div {
    background: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
    color: #1a202c !important;
}
div[data-testid="stForm"] {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 1.3rem 1.5rem;
}
.stButton > button {
    background: #f1f5f9 !important;
    color: #475569 !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    width: 100% !important;
    transition: all 0.15s !important;
}
.stButton > button:hover {
    background: #e2e8f0 !important;
    color: #1a202c !important;
}
.stFormSubmitButton > button {
    background: #2563eb !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    width: 100% !important;
}
.stFormSubmitButton > button:hover {
    background: #1d4ed8 !important;
}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #f8fafc; }
::-webkit-scrollbar-thumb { background: #e2e8f0; border-radius: 99px; }
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE ───────────────────────────────────────────────────────────
if "tol" not in st.session_state:
    st.session_state.tol = MultiQueueTol()
if "log" not in st.session_state:
    st.session_state.log = []
if "total_masuk" not in st.session_state:
    st.session_state.total_masuk = 0
if "total_keluar" not in st.session_state:
    st.session_state.total_keluar = 0


def add_log(msg: str, kind: str = "info"):
    ts = time.strftime("%H:%M:%S")
    st.session_state.log.insert(0, {"time": ts, "msg": msg, "kind": kind})
    if len(st.session_state.log) > 30:
        st.session_state.log.pop()


# ─── HEADER ─────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">🛣️ Sim<span class="hero-accent">Tol</span> — Sistem Antrian Tol</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Multi-Queue Toll Simulation · Struktur Data</div>', unsafe_allow_html=True)

# ─── STAT CARDS ─────────────────────────────────────────────────────────────
antrian = st.session_state.tol.lihat_antrian()
s1 = len(antrian["Tol 1"])
s2 = len(antrian["Tol 2"])
s3 = len(antrian["Tol 3"])
total_antri = s1 + s2 + s3

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="stat-card tol1">
        <div class="stat-label">Gate 1 — Antrean</div>
        <div class="stat-num">{s1}</div>
        <div class="stat-desc">kendaraan menunggu</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="stat-card tol2">
        <div class="stat-label">Gate 2 — Antrean</div>
        <div class="stat-num">{s2}</div>
        <div class="stat-desc">kendaraan menunggu</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="stat-card tol3">
        <div class="stat-label">Gate 3 — Antrean</div>
        <div class="stat-num">{s3}</div>
        <div class="stat-desc">kendaraan menunggu</div>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="stat-card total">
        <div class="stat-label">Total Aktif</div>
        <div class="stat-num">{total_antri}</div>
        <div class="stat-desc">Masuk: {st.session_state.total_masuk} · Keluar: {st.session_state.total_keluar}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── VISUALISASI LANE ────────────────────────────────────────────────────────
st.markdown('<div class="section-label">📊 Visualisasi Antrian Real-Time</div>', unsafe_allow_html=True)

ICONS = ["🚗", "🚌", "🚛", "🏎️", "🚐", "🚑", "🚒"]

def render_lane(nama, kelas, kendaraan_list):
    chips_html = ""
    if kendaraan_list:
        for i, k in enumerate(kendaraan_list):
            icon = ICONS[hash(k) % len(ICONS)]
            pos_label = "NEXT" if i == 0 else f"#{i+1}"
            chips_html += f"""
            <div class="vehicle-chip">
                <span class="vehicle-pos">{pos_label}</span>
                <span class="vehicle-icon">{icon}</span>
                <span>{k}</span>
            </div>"""
    else:
        chips_html = '<div class="empty-lane"><div class="empty-icon">🚦</div><div>Jalur Kosong</div></div>'

    return f"""
    <div class="lane {kelas}">
        <div class="lane-header">
            <span class="lane-title">⬤ {nama}</span>
            <span class="lane-badge">{len(kendaraan_list)} kendaraan</span>
        </div>
        {chips_html}
    </div>"""

c1, c2, c3 = st.columns(3)
with c1:
    st.html(render_lane("Gate 1", "tol1", antrian["Tol 1"]))
with c2:
    st.html(render_lane("Gate 2", "tol2", antrian["Tol 2"]))
with c3:
    st.html(render_lane("Gate 3", "tol3", antrian["Tol 3"]))

st.markdown("<br>", unsafe_allow_html=True)

# ─── KONTROL ────────────────────────────────────────────────────────────────
col_in, col_out = st.columns([1, 1], gap="large")

with col_in:
    st.markdown('<div class="section-label">🚗 Kendaraan Masuk</div>', unsafe_allow_html=True)
    with st.form("form_masuk", clear_on_submit=True):
        plat = st.text_input("Nomor Plat / ID Kendaraan", placeholder="Contoh: B 1234 ABC")
        submitted = st.form_submit_button("➕ Masukkan ke Antrian Terpendek")
        if submitted:
            if plat.strip():
                result = st.session_state.tol.masuk_tol(plat.strip().upper())
                st.session_state.total_masuk += 1
                add_log(result, "success")
                st.rerun()
            else:
                st.warning("Masukkan nomor plat terlebih dahulu.")

with col_out:
    st.markdown('<div class="section-label">✅ Kendaraan Keluar</div>', unsafe_allow_html=True)
    with st.form("form_keluar"):
        gate = st.selectbox("Pilih Gate", options=[1, 2, 3], format_func=lambda x: f"Gate {x}")
        keluar_btn = st.form_submit_button("⬅️ Proses Kendaraan Keluar")
        if keluar_btn:
            result = st.session_state.tol.keluar_tol(gate)
            if result != "Antrian kosong":
                st.session_state.total_keluar += 1
                add_log(f"{result} → keluar dari Gate {gate}", "warning")
            else:
                add_log(f"Gate {gate}: antrian kosong!", "info")
            st.rerun()

# ─── LOG AKTIVITAS ───────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-label">📋 Log Aktivitas</div>', unsafe_allow_html=True)

if st.session_state.log:
    entries_html = ""
    for entry in st.session_state.log:
        entries_html += f"""
        <div class="log-entry {entry['kind']}">
            <span class="log-time">{entry['time']}</span>
            <span class="log-msg">{entry['msg']}</span>
        </div>"""
    st.markdown(f'<div class="log-container">{entries_html}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="log-container"><div class="log-entry info"><span class="log-msg">Belum ada aktivitas. Masukkan kendaraan untuk memulai.</span></div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔄 Reset Semua Antrian"):
    st.session_state.tol = MultiQueueTol()
    st.session_state.log = []
    st.session_state.total_masuk = 0
    st.session_state.total_keluar = 0
    add_log("Sistem direset oleh operator.", "info")
    st.rerun()