import streamlit as st
import time
from logic import MultiQueueTol

def load_css():
    with open("style.css", "r", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

st.set_page_config(
    page_title="Sistem Antrian Tol",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)
load_css()

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

# HEADER
st.markdown('<div class="hero-title">🛣️ Sim<span class="hero-accent">Tol</span> — Sistem Antrian Tol</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Multi-Queue Toll Simulation · Struktur Data</div>', unsafe_allow_html=True)
st.markdown('<div class="subhead"><div></div><div class="hero-subsub">by Irwansyah, Shafira, Ismail, Rizqi</div></div>', unsafe_allow_html=True)

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
                plat_bersih = plat.strip().upper()
                gate = st.session_state.tol.masuk_tol(plat_bersih)
                st.session_state.total_masuk += 1
                add_log(f"{plat_bersih} masuk ke Gerbbang {gate}","success")
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
            if result is not None:
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