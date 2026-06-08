"""FIFA World Cup 2026 — Prediction App v2"""

import streamlit as st
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import io
import base64
import os
try:
    from streamlit_sortables import sort_items as _sort_items
    HAS_SORTABLES = True
except ImportError:
    HAS_SORTABLES = False


@st.cache_data
def _logo_b64() -> str:
    path = os.path.join(os.path.dirname(__file__), "assets", "wc2026_logo.webp")
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

st.set_page_config(
    page_title="WC 2026 · My Prediction",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""<style>
/* === BACKGROUND === */
.stApp { background: #0A1628 !important; }
header[data-testid="stHeader"] { background: #0A1628 !important; box-shadow: none !important; }
section[data-testid="stSidebar"] { background: #050d1a !important; }

/* === BLOCK CONTAINER === */
.main .block-container {
    padding-top: 0.8rem;
    padding-bottom: 2rem;
    background: transparent;
}

/* === TABS === */
.stTabs [data-baseweb="tab-list"] {
    background: #162032;
    padding: 5px 6px;
    border-radius: 12px;
    gap: 4px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    color: white !important;
    padding: 8px 22px;
    font-weight: 600;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg,#1DE9B6,#00BFA5) !important;
    color: #0A1628 !important;
    font-weight: 800;
}

/* === EXPANDERS === */
[data-testid="stExpander"] {
    background: rgba(22,32,50,0.95) !important;
    border-radius: 14px !important;
    border: 2px solid rgba(29,233,182,0.3) !important;
    margin-bottom: 12px;
}
[data-testid="stExpander"] details summary p {
    color: #F0F6FC !important;
    font-weight: 700 !important;
}
[data-testid="stExpander"] details summary svg { fill: #1DE9B6 !important; }

/* === TYPOGRAPHY === */
h1 { font-size:2.2rem !important; color:#1DE9B6 !important; font-weight:900 !important; }
h2 { font-size:1.3rem !important; color:#1DE9B6 !important; font-weight:700 !important; }
h3 { font-size:1.1rem !important; color:#1DE9B6 !important; font-weight:600 !important; }
p, .stMarkdown p { color: #F0F6FC !important; }
label, .stSelectbox label { color: #F0F6FC !important; font-weight: 600 !important; }
.stCaption p { color: rgba(240,246,252,0.55) !important; font-size: 0.82rem !important; }

/* === SELECTBOXES === */
[data-baseweb="select"] > div:first-child {
    background: #162032 !important;
    border: 1.5px solid rgba(29,233,182,0.3) !important;
    border-radius: 8px !important;
}
[data-baseweb="select"] span { color: #F0F6FC !important; font-weight: 500; }

/* === MULTISELECT === */
[data-baseweb="tag"] {
    background: #1DE9B6 !important;
    border-radius: 6px !important;
}
[data-baseweb="tag"] span { color: #0A1628 !important; }

/* === METRICS === */
[data-testid="metric-container"] {
    background: rgba(22,32,50,0.95);
    border-radius: 12px;
    padding: 14px 16px;
    border-left: 4px solid #1DE9B6;
    box-shadow: 0 2px 12px rgba(0,0,0,0.3);
}
[data-testid="metric-container"] label { color: rgba(240,246,252,0.6) !important; font-weight:600 !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #F0F6FC !important; font-weight: 900 !important;
}

/* === BUTTONS === */
.stButton > button {
    background: #1DE9B6 !important;
    color: #0A1628 !important;
    font-weight: 800 !important;
    border: none !important;
    border-radius: 10px !important;
    letter-spacing: 0.5px;
}
.stButton > button:hover {
    background: linear-gradient(135deg,#D4A017,#FFD700) !important;
    color: #0A1628 !important;
}
/* Thirds grid - secondary (unselected) */
.stButton > button[kind="secondary"] {
    background: #162032 !important;
    color: #F0F6FC !important;
    font-weight: 600 !important;
    border: 1px solid rgba(29,233,182,0.25) !important;
    min-height: 78px !important;
    white-space: pre-wrap !important;
    font-size: 12px !important;
    line-height: 1.5 !important;
}
.stButton > button[kind="secondary"]:hover {
    background: rgba(29,233,182,0.12) !important;
    border-color: rgba(29,233,182,0.6) !important;
    color: #1DE9B6 !important;
}
/* Thirds grid - primary (selected) */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg,#1DE9B6,#00BFA5) !important;
    color: #0A1628 !important;
    font-weight: 800 !important;
    border: 2px solid #FFD700 !important;
    min-height: 78px !important;
    white-space: pre-wrap !important;
    font-size: 12px !important;
    line-height: 1.5 !important;
}
[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg,#D4A017,#FFD700) !important;
    color: #0A1628 !important;
    font-weight: 800 !important;
    border: none !important;
    border-radius: 10px !important;
}

/* === DIVIDER === */
hr { border-color: rgba(29,233,182,0.2) !important; border-width: 1.5px !important; }

/* === ALERTS === */
[data-baseweb="notification"] { border-radius: 10px !important; }
</style>""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
EMPTY = "— scegli —"

FLAGS = {
    'Messico': '🇲🇽', 'Sudafrica': '🇿🇦', 'Corea del Sud': '🇰🇷', 'Rep. Ceca': '🇨🇿',
    'Canada': '🇨🇦', 'Bosnia': '🇧🇦', 'Qatar': '🇶🇦', 'Svizzera': '🇨🇭',
    'Brasile': '🇧🇷', 'Marocco': '🇲🇦', 'Haiti': '🇭🇹', 'Scozia': 'SC',
    'USA': '🇺🇸', 'Paraguay': '🇵🇾', 'Australia': '🇦🇺', 'Turchia': '🇹🇷',
    'Germania': '🇩🇪', 'Curaçao': '🇨🇼', "Costa d'Avorio": '🇨🇮', 'Ecuador': '🇪🇨',
    'Olanda': '🇳🇱', 'Giappone': '🇯🇵', 'Svezia': '🇸🇪', 'Tunisia': '🇹🇳',
    'Belgio': '🇧🇪', 'Egitto': '🇪🇬', 'Iran': '🇮🇷', 'Nuova Zelanda': '🇳🇿',
    'Spagna': '🇪🇸', 'Capo Verde': '🇨🇻', 'Arabia Saudita': '🇸🇦', 'Uruguay': '🇺🇾',
    'Francia': '🇫🇷', 'Senegal': '🇸🇳', 'Iraq': '🇮🇶', 'Norvegia': '🇳🇴',
    'Argentina': '🇦🇷', 'Algeria': '🇩🇿', 'Austria': '🇦🇹', 'Giordania': '🇯🇴',
    'Portogallo': '🇵🇹', 'RD Congo': '🇨🇩', 'Uzbekistan': '🇺🇿', 'Colombia': '🇨🇴',
    'Inghilterra': 'IN', 'Croazia': '🇭🇷', 'Ghana': '🇬🇭', 'Panama': '🇵🇦',
}


FLAG_CODES = {
    'Messico': 'mx', 'Sudafrica': 'za', 'Corea del Sud': 'kr', 'Rep. Ceca': 'cz',
    'Canada': 'ca', 'Bosnia': 'ba', 'Qatar': 'qa', 'Svizzera': 'ch',
    'Brasile': 'br', 'Marocco': 'ma', 'Haiti': 'ht', 'Scozia': 'gb-sct',
    'USA': 'us', 'Paraguay': 'py', 'Australia': 'au', 'Turchia': 'tr',
    'Germania': 'de', 'Curaçao': 'cw', "Costa d'Avorio": 'ci', 'Ecuador': 'ec',
    'Olanda': 'nl', 'Giappone': 'jp', 'Svezia': 'se', 'Tunisia': 'tn',
    'Belgio': 'be', 'Egitto': 'eg', 'Iran': 'ir', 'Nuova Zelanda': 'nz',
    'Spagna': 'es', 'Capo Verde': 'cv', 'Arabia Saudita': 'sa', 'Uruguay': 'uy',
    'Francia': 'fr', 'Senegal': 'sn', 'Iraq': 'iq', 'Norvegia': 'no',
    'Argentina': 'ar', 'Algeria': 'dz', 'Austria': 'at', 'Giordania': 'jo',
    'Portogallo': 'pt', 'RD Congo': 'cd', 'Uzbekistan': 'uz', 'Colombia': 'co',
    'Inghilterra': 'gb-eng', 'Croazia': 'hr', 'Ghana': 'gh', 'Panama': 'pa',
}


def flag(team: str) -> str:
    return FLAGS.get(team, '')


def flag_img(team: str, size: int = 24) -> str:
    code = FLAG_CODES.get(team, '')
    if not code:
        return f'<span style="font-size:{size}px;">{FLAGS.get(team, "")}</span>'
    return (f'<img src="https://flagcdn.com/w40/{code}.png" height="{size}" '
            f'style="border-radius:2px;vertical-align:middle;" '
            f'onerror="this.replaceWith(document.createTextNode(\'{FLAGS.get(team, "")}\')">')


def fmt(team: str) -> str:
    if not team or team == EMPTY:
        return team or EMPTY
    f = FLAGS.get(team, '')
    return f"{f} {team}" if f else team


# team → group letter (derived from GROUPS below, used for thirds seeding)
TEAM_GROUP: dict = {}

GROUPS = {
    'A': ['Messico', 'Sudafrica', 'Corea del Sud', 'Rep. Ceca'],
    'B': ['Canada', 'Qatar', 'Svizzera', 'Bosnia'],
    'C': ['Brasile', 'Marocco', 'Haiti', 'Scozia'],
    'D': ['USA', 'Paraguay', 'Australia', 'Turchia'],
    'E': ['Germania', 'Curaçao', "Costa d'Avorio", 'Ecuador'],
    'F': ['Olanda', 'Giappone', 'Svezia', 'Tunisia'],
    'G': ['Belgio', 'Egitto', 'Iran', 'Nuova Zelanda'],
    'H': ['Spagna', 'Capo Verde', 'Arabia Saudita', 'Uruguay'],
    'I': ['Francia', 'Senegal', 'Iraq', 'Norvegia'],
    'J': ['Argentina', 'Algeria', 'Austria', 'Giordania'],
    'K': ['Portogallo', 'RD Congo', 'Uzbekistan', 'Colombia'],
    'L': ['Inghilterra', 'Croazia', 'Ghana', 'Panama'],
}

# Build reverse mapping team → group
TEAM_GROUP.update({t: g for g, teams in GROUPS.items() for t in teams})

# ── Thirds seeding  (official 2026 WC eligible-groups per "3?" slot) ─────────
_SLOT_ELIGIBLE = {
    0:  frozenset('CEFKI'),   # vs 1A  — Mexico City
    1:  frozenset('BEHIJ'),   # vs 1L  — Atlanta
    4:  frozenset('DEFHJ'),   # vs 1B  — Vancouver
    5:  frozenset('AEHIL'),   # vs 1K  — Kansas City
    8:  frozenset('BCGKL'),   # vs 1D  — San Francisco
    9:  frozenset('AEFIJ'),   # vs 1G  — Seattle
    14: frozenset('ABCGJ'),   # vs 1E  — Boston
    15: frozenset('BCDFL'),   # vs 1I  — New Jersey
}
_THIRD_SLOT_ORDER = [0, 1, 4, 5, 8, 9, 14, 15]


def compute_thirds_seeding(thirds_pool: list) -> dict:
    """Assign 8 thirds to R16 slots using official eligible-groups table.
    Greedy minimum-options-first (most constrained slot assigned first).
    Returns: {r16_slot_idx: team_name}
    """
    if not thirds_pool:
        return {}
    q_grps = [TEAM_GROUP.get(t, '') for t in thirds_pool]
    eligible = {
        s: _SLOT_ELIGIBLE[s] & frozenset(q_grps)
        for s in _THIRD_SLOT_ORDER
    }
    assignment: dict = {}
    used: set = set()
    for _ in range(min(len(thirds_pool), 8)):
        ranked = sorted(
            [(len(eligible[s] - used), s) for s in _THIRD_SLOT_ORDER if s not in assignment]
        )
        if not ranked:
            break
        _, slot = ranked[0]
        avail = eligible[slot] - used
        if not avail:
            avail = frozenset(q_grps) - used
        if not avail:
            break
        grp = sorted(avail)[0]
        assignment[slot] = grp
        used.add(grp)
    grp2team = {TEAM_GROUP.get(t, ''): t for t in thirds_pool}
    return {s: grp2team[g] for s, g in assignment.items() if g in grp2team}


PLAYERS = [
    EMPTY,
    "Erling Haaland (NOR)", "Kylian Mbappé (FRA)", "Vinícius Jr. (BRA)",
    "Harry Kane (ENG)", "Darwin Núñez (URU)", "Lamine Yamal (ESP)",
    "Endrick (BRA)", "Julián Álvarez (ARG)", "Bukayo Saka (ENG)",
    "Raphinha (BRA)", "Cody Gakpo (NED)", "Luis Díaz (COL)",
    "Jeremy Doku (BEL)", "Rafael Leão (POR)", "Cristiano Ronaldo (POR)",
    "Takefusa Kubo (JPN)", "Christian Pulisic (USA)", "Kaoru Mitoma (JPN)",
    "Alejandro Garnacho (ARG)", "Jude Bellingham (ENG)", "Pedri (ESP)",
    "Gavi (ESP)", "Federico Valverde (URU)", "Kevin De Bruyne (BEL)",
    "Luka Modrić (CRO)", "Phil Foden (ENG)", "Cole Palmer (ENG)",
    "Dani Olmo (ESP)", "Frenkie de Jong (NED)", "Jamal Musiala (GER)",
    "Florian Wirtz (GER)", "João Neves (POR)", "Warren Zaïre-Emery (FRA)",
    "Xavi Simons (NED)", "Alexis Mac Allister (ARG)", "Enzo Fernández (ARG)",
    "Antoine Griezmann (FRA)", "Bernardo Silva (POR)", "Bruno Fernandes (POR)",
    "Arda Güler (TUR)", "Virgil van Dijk (NED)", "Joško Gvardiol (CRO)",
    "Achraf Hakimi (MAR)", "Mateo Kovačić (CRO)", "Youssef En-Nesyri (MAR)",
    "Rodrigo Bentancur (URU)", "James Rodríguez (COL)", "Romelu Lukaku (BEL)",
]

U23_PLAYERS = [
    EMPTY,
    "Lamine Yamal (ESP · 2007)", "Pau Cubarsí (ESP · 2007)",
    "Warren Zaïre-Emery (FRA · 2006)", "Endrick (BRA · 2006)",
    "Mathys Tel (FRA · 2005)", "Leny Yoro (FRA · 2005)",
    "Kobbie Mainoo (ENG · 2005)", "Arda Güler (TUR · 2005)",
    "Alejandro Garnacho (ARG · 2004)", "Savinho (BRA · 2004)",
    "Gavi (ESP · 2004)", "João Neves (POR · 2004)", "Rico Lewis (ENG · 2004)",
    "Jamal Musiala (GER · 2003)", "Florian Wirtz (GER · 2003)",
    "Xavi Simons (NED · 2003)",
]

# (idx, slot1, slot2, venue)
R16 = [
    (0,  "1A", "3?", "1 lug · Città del Messico"),
    (1,  "1L", "3?", "1 lug · Atlanta"),
    (2,  "1C", "2F", "29 giu · Houston"),
    (3,  "2E", "2I", "30 giu · Dallas"),
    (4,  "1B", "3?", "3 lug · Vancouver"),
    (5,  "1K", "3?", "4 lug · Kansas City"),
    (6,  "1J", "2H", "3 lug · Miami"),
    (7,  "2D", "2G", "3 lug · Dallas"),
    (8,  "1D", "3?", "2 lug · San Francisco"),
    (9,  "1G", "3?", "1 lug · Seattle"),
    (10, "2K", "2L", "3 lug · Toronto"),
    (11, "1H", "2J", "2 lug · Los Angeles"),
    (12, "2A", "2B", "28 giu · Los Angeles"),
    (13, "1F", "2C", "30 giu · Monterrey"),
    (14, "1E", "3?", "29 giu · Boston"),
    (15, "1I", "3?", "30 giu · New Jersey"),
]

R8 = [
    (0, 0, 1,   "5 lug"),
    (1, 2, 3,   "5 lug"),
    (2, 4, 5,   "7 lug"),
    (3, 6, 7,   "7 lug"),
    (4, 8, 9,   "6 lug"),
    (5, 10, 11, "6 lug"),
    (6, 12, 13, "4 lug"),
    (7, 14, 15, "4 lug"),
]

QF = [
    (0, 0, 1, "11 lug · Atlanta"),
    (1, 2, 3, "11 lug"),
    (2, 4, 5, "10 lug"),
    (3, 6, 7, "9 lug"),
]

SF = [
    (0, 0, 1, "15 lug · Atlanta"),
    (1, 2, 3, "14 lug · Dallas"),
]

# ── Session state ─────────────────────────────────────────────────────────────
def _init():
    for grp, teams in GROUPS.items():
        key = f"g_{grp}_order"
        if key not in st.session_state:
            order = []
            for pos in range(4):
                old = f"g_{grp}_{pos}"
                if old in st.session_state and st.session_state[old] not in order:
                    order.append(st.session_state[old])
            for t in teams:
                if t not in order:
                    order.append(t)
            st.session_state[key] = order[:4]
    if "thirds" not in st.session_state:
        st.session_state.thirds = []
    for prefix, n in [("r16", 16), ("r8", 8), ("qf", 4), ("sf", 2)]:
        for i in range(n):
            if f"{prefix}_{i}" not in st.session_state:
                st.session_state[f"{prefix}_{i}"] = EMPTY
    for k in ("champion", "third_pl", "best_player", "top_scorer", "best_u23"):
        if k not in st.session_state:
            st.session_state[k] = EMPTY


_init()

# ── Helpers ───────────────────────────────────────────────────────────────────
def grp_team(g, pos):
    order = st.session_state.get(f"g_{g}_order", GROUPS[g])
    return order[pos] if pos < len(order) else GROUPS[g][pos]


def slot_team(slot):
    if slot == "3?":
        return None
    return grp_team(slot[1], int(slot[0]) - 1)


def get_winners(prefix, n):
    return [st.session_state.get(f"{prefix}_{i}", EMPTY) for i in range(n)]


def dedup(lst):
    seen, out = set(), []
    for x in lst:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def match_widget(state_key, venue, t1, t2, thirds_pool=None):
    is_third = (t2 is None)
    if is_third:
        opts = dedup([EMPTY] + (thirds_pool or []) + ([t1] if t1 else []))
        t2_label = "Miglior 3ª"
    else:
        opts = dedup([EMPTY, t1, t2 or "?"])
        t2_label = fmt(t2) if t2 and t2 != "?" else (t2 or "?")

    if not opts or opts[0] != EMPTY:
        opts = [EMPTY] + [o for o in opts if o != EMPTY]

    curr = st.session_state.get(state_key, EMPTY)
    if curr not in opts:
        curr = EMPTY

    c1, c2 = st.columns([4, 2])
    with c1:
        st.caption(f"📍 {venue}")
        t1_d = fmt(t1) if t1 else "?"
        st.markdown(f"**{t1_d}** vs **{t2_label}**")
        if is_third and thirds_pool:
            pool_s = "  ".join(fmt(t) for t in thirds_pool[:4])
            extra = "…" if len(thirds_pool) > 4 else ""
            st.caption(f"Possibili 3ª: {pool_s}{extra}")
    with c2:
        st.selectbox(
            "Vincitore", opts,
            index=opts.index(curr),
            key=state_key,
            label_visibility="collapsed",
            format_func=fmt,
        )


def sf_loser(sf_idx):
    _, qf_a, qf_b, _ = SF[sf_idx]
    qf_winners = get_winners("qf", 4)
    t1 = qf_winners[qf_a] if qf_winners[qf_a] != EMPTY else f"Vinc. Q{qf_a+1}"
    t2 = qf_winners[qf_b] if qf_winners[qf_b] != EMPTY else f"Vinc. Q{qf_b+1}"
    w = st.session_state.get(f"sf_{sf_idx}", EMPTY)
    if w == t1:
        return t2
    if w == t2:
        return t1
    return f"Perdente SF{sf_idx+1}"


def group_card_html(grp):
    pos_colors = ['#FFD700', '#E8E8E8', '#CD7F32', 'rgba(255,255,255,0.35)']
    pos_labels = ['1°', '2°', '3°', '4°']
    rows = ""
    for pos in range(4):
        team = grp_team(grp, pos)
        img = flag_img(team, 18)
        sep = "border-bottom:1px solid rgba(255,255,255,0.07);" if pos < 3 else ""
        opacity = "1" if pos < 2 else "0.6"
        fw = "700" if pos < 2 else "400"
        rows += (
            f'<div style="display:flex;align-items:center;padding:7px 10px;{sep}opacity:{opacity}">'
            f'<span style="color:{pos_colors[pos]};font-weight:700;font-size:11px;min-width:22px;">{pos_labels[pos]}</span>'
            f'<span style="margin:0 6px 0 2px;display:inline-flex;align-items:center;">{img}</span>'
            f'<span style="color:white;font-size:12px;font-weight:{fw};">{team}</span>'
            f'</div>'
        )
    return (
        f'<div style="background:#162032;border-radius:10px;overflow:hidden;'
        f'border:1.5px solid rgba(29,233,182,0.4);margin-bottom:6px;">'
        f'<div style="background:linear-gradient(135deg,#1DE9B6,#00BFA5);'
        f'padding:6px 10px;display:flex;justify-content:space-between;align-items:center;">'
        f'<span style="font-size:14px;font-weight:900;color:#0A1628;letter-spacing:1px;">GRUPPO {grp}</span>'
        f'<span style="font-size:16px;color:#0A1628;font-weight:900;">{grp}</span>'
        f'</div>{rows}</div>'
    )


# ── Header ────────────────────────────────────────────────────────────────────
_logo = _logo_b64()
_logo_tag = (
    f'<img src="data:image/webp;base64,{_logo}" '
    f'style="height:90px;width:auto;object-fit:contain;filter:drop-shadow(0 2px 8px rgba(0,0,0,0.5));">'
    if _logo else '<div style="font-size:52px;line-height:1;">🏆</div>'
)
st.markdown(
    '<div style="background:linear-gradient(135deg,#0A1628 0%,#162032 100%);'
    'border-radius:16px;padding:20px 28px;margin-bottom:18px;'
    'border:2px solid #D4A017;display:flex;align-items:center;gap:18px;">'
    f'{_logo_tag}'
    '<div>'
    '<div style="font-size:22px;font-weight:900;color:#FFD700;letter-spacing:2px;">'
    'FIFA WORLD CUP 2026</div>'
    '<div style="font-size:13px;color:rgba(255,255,255,0.65);margin-top:5px;">'
    'USA · Canada · Messico &nbsp;|&nbsp; 11 giugno – 19 luglio 2026 &nbsp;|&nbsp; 48 squadre · 104 partite'
    '</div></div></div>',
    unsafe_allow_html=True,
)

tab_g, tab_b, tab_a, tab_s = st.tabs(["📋  Gironi", "⚔️  Tabellone", "🌟  Premi", "📸  Salva"])

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 1 — GIRONI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_g:
    st.subheader("Fase a Gironi — Classifica Prevista")
    st.caption("Trascina le nazionali per riordinare la classifica del girone.")

    group_list = list(GROUPS.keys())

    for row_start in range(0, 12, 4):
        cols = st.columns(4)
        for ci in range(4):
            gi = row_start + ci
            if gi >= 12:
                break
            grp = group_list[gi]
            with cols[ci]:
                # Visual card (reads current order from session state)
                st.markdown(group_card_html(grp), unsafe_allow_html=True)
                # Drag-to-reorder
                current = list(st.session_state.get(f"g_{grp}_order", GROUPS[grp]))
                lbl2team = {f"{flag(t)} {t}": t for t in GROUPS[grp]}
                items = [f"{flag(t)} {t}" for t in current]
                if HAS_SORTABLES:
                    new_items = _sort_items(items, key=f"sort_{grp}", direction="vertical")
                    if new_items and new_items != items:
                        new_order = [lbl2team[l] for l in new_items if l in lbl2team]
                        if len(new_order) == 4:
                            st.session_state[f"g_{grp}_order"] = new_order
                            st.rerun()
                else:
                    # Fallback: up/down buttons
                    for pos, t in enumerate(current):
                        c1, c2, c3 = st.columns([6, 1, 1])
                        c1.write(f"{['🥇','🥈','🥉','4°'][pos]} {flag(t)} {t}")
                        if pos > 0 and c2.button("▲", key=f"up_{grp}_{pos}"):
                            current[pos], current[pos-1] = current[pos-1], current[pos]
                            st.session_state[f"g_{grp}_order"] = current
                            st.rerun()
                        if pos < 3 and c3.button("▼", key=f"dn_{grp}_{pos}"):
                            current[pos], current[pos+1] = current[pos+1], current[pos]
                            st.session_state[f"g_{grp}_order"] = current
                            st.rerun()
        st.markdown("")

    st.divider()

    # ── Migliori Terze ────────────────────────────────────────────────────────
    st.subheader("🥉 Migliori Terze (8 di 12)")
    st.caption(
        "Nel formato a 48 squadre le 8 migliori terze avanzano ai sedicesimi. "
        "Seleziona le 8 che pensi si qualificheranno."
    )

    third_teams_by_grp = [(g, grp_team(g, 2)) for g in group_list]

    cols4 = st.columns(4)
    for gi, (grp, t) in enumerate(third_teams_by_grp):
        is_sel = t in st.session_state.get("thirds", [])
        btn_type = "primary" if is_sel else "secondary"
        check = "✅ " if is_sel else ""
        emoji = flag(t)
        label = f"{check}GRP {grp}\n{emoji}  {t}"
        with cols4[gi % 4]:
            if st.button(label, key=f"third_{grp}", use_container_width=True, type=btn_type):
                cur = list(st.session_state.get("thirds", []))
                if t in cur:
                    cur.remove(t)
                elif len(cur) < 8:
                    cur.append(t)
                st.session_state["thirds"] = cur
                st.rerun()

    n_sel = len(st.session_state.get("thirds", []))
    if n_sel > 8:
        st.error(f"⚠️ Massimo 8 terze. Hai selezionato {n_sel}.")
    elif n_sel < 8:
        st.info(f"Clicca le squadre per selezionarle — ancora {8 - n_sel} da scegliere.")
    else:
        st.success("✅ 8 migliori terze selezionate!")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 2 — TABELLONE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_b:
    thirds_pool = [t for t in st.session_state.get("thirds", []) if t != EMPTY][:8]
    _seeding    = compute_thirds_seeding(thirds_pool)

    def third_for(r16_idx):
        return _seeding.get(r16_idx)

    def _sp(px):
        if px > 0:
            st.markdown(f'<div style="height:{px}px"></div>', unsafe_allow_html=True)

    def mkc(key, t1, t2, venue=""):
        winner = st.session_state.get(key, EMPTY)
        valid  = [t for t in [t1, t2] if t and t != EMPTY]
        if winner not in valid:
            if winner != EMPTY:
                st.session_state[key] = EMPTY
            winner = EMPTY
        if venue:
            short_v = venue.split("·")[0].strip()
            st.markdown(
                f'<div style="font-size:7px;color:rgba(29,233,182,0.4);'
                f'text-align:center;margin-bottom:1px;line-height:1.2;">{short_v}</div>',
                unsafe_allow_html=True,
            )
        for team, slot in [(t1, "_a"), (t2, "_b")]:
            if team and team != EMPTY:
                is_w = winner == team
                nm   = (team[:10] + ".") if len(team) > 11 else team
                lbl  = f"{flag(team)} {nm}"
                if st.button(lbl, key=f"{key}{slot}",
                             type="primary" if is_w else "secondary",
                             use_container_width=True):
                    st.session_state[key] = EMPTY if winner == team else team
                    st.rerun()
            else:
                st.markdown(
                    '<div style="background:rgba(255,255,255,0.03);border:1px dashed '
                    'rgba(255,255,255,0.1);border-radius:5px;padding:8px 0;'
                    'text-align:center;font-size:8px;color:rgba(255,255,255,0.2);'
                    'margin:1px 0;">?</div>',
                    unsafe_allow_html=True,
                )
        st.markdown('<div style="height:3px"></div>', unsafe_allow_html=True)

    _SLOT_LEGEND = {
        0:  'C/E/F/K/I', 1:  'B/E/H/I/J',
        4:  'D/E/F/H/J', 5:  'A/E/H/I/L',
        8:  'B/C/G/K/L', 9:  'A/E/F/I/J',
        14: 'A/B/C/G/J', 15: 'B/C/D/F/L',
    }

    # Compute all winners
    r16_w = get_winners("r16", 16)
    r8_w  = get_winners("r8",   8)
    qf_w  = get_winners("qf",   4)
    sf_w  = get_winners("sf",   2)

    # Progress banner
    champ      = st.session_state.get("champion", EMPTY)
    filled_r16 = sum(1 for w in r16_w if w != EMPTY)
    filled_r8  = sum(1 for w in r8_w  if w != EMPTY)
    filled_qf  = sum(1 for w in qf_w  if w != EMPTY)
    filled_sf  = sum(1 for w in sf_w  if w != EMPTY)
    champ_html = (
        f'<span style="font-size:16px;">🏆</span>'
        f'<span style="color:#FFD700;font-weight:900;margin-left:6px;">{fmt(champ)}</span>'
    ) if champ != EMPTY else ""
    st.markdown(
        f'<div style="display:flex;align-items:center;flex-wrap:wrap;gap:10px;'
        f'background:#162032;border-radius:10px;padding:10px 14px;margin-bottom:8px;'
        f'border:1px solid rgba(29,233,182,0.2);">'
        f'<span style="color:rgba(240,246,252,0.45);font-size:10px;font-weight:700;">PROGRESSO</span>'
        f'<span style="color:#F0F6FC;font-size:10px;">S16 <b style="color:#1DE9B6">{filled_r16}/16</b></span>'
        f'<span style="color:#F0F6FC;font-size:10px;">R8 <b style="color:#1DE9B6">{filled_r8}/8</b></span>'
        f'<span style="color:#F0F6FC;font-size:10px;">QF <b style="color:#1DE9B6">{filled_qf}/4</b></span>'
        f'<span style="color:#F0F6FC;font-size:10px;">SF <b style="color:#1DE9B6">{filled_sf}/2</b></span>'
        f'{champ_html}</div>',
        unsafe_allow_html=True,
    )
    if len(thirds_pool) < 8:
        st.info(f"⚠️ Seleziona le 8 migliori terze nel tab Gironi ({len(thirds_pool)}/8).")

    # Stage-label header row
    _COL_W      = [3, 2.5, 2, 1.8, 2.5, 1.8, 2, 2.5, 3]
    _HDR_LABELS = [
        "SEDICESIMI", "OTTAVI", "QUARTI", "SEMIF.", "",
        "SEMIF.", "QUARTI", "OTTAVI", "SEDICESIMI",
    ]
    for col, lbl in zip(st.columns(_COL_W), _HDR_LABELS):
        with col:
            st.markdown(
                f'<div style="text-align:center;font-size:8px;font-weight:900;'
                f'color:#1DE9B6;letter-spacing:0.8px;padding:3px 0 4px;'
                f'border-bottom:2px solid rgba(29,233,182,0.35);margin-bottom:4px;'
                f'min-height:18px;">{lbl}</div>',
                unsafe_allow_html=True,
            )

    # Bracket: 9 columns
    H = 100
    (c_r16l, c_r8l, c_qfl, c_sfl,
     c_fin,
     c_sfr, c_qfr, c_r8r, c_r16r) = st.columns(_COL_W)

    r16_info = {idx: (s1, s2, v) for idx, s1, s2, v in R16}

    def _r16(col, idx):
        s1, s2, venue = r16_info[idx]
        t1 = slot_team(s1)
        if s2 == "3?":
            assigned = third_for(idx)
            caption  = f"3ª {_SLOT_LEGEND.get(idx, '')}" if not assigned else ""
            with col:
                mkc(f"r16_{idx}", t1, assigned,
                    venue + (f" · {caption}" if caption else ""))
        else:
            with col:
                mkc(f"r16_{idx}", t1, slot_team(s2), venue)

    # Left R16 (0-7)
    for i in range(8):
        _r16(c_r16l, i)

    # Left R8 (0-3)
    with c_r8l:
        _sp(H // 2)
        for i, (idx, a, b, venue) in enumerate(R8[:4]):
            t1 = r16_w[a] if r16_w[a] != EMPTY else None
            t2 = r16_w[b] if r16_w[b] != EMPTY else None
            mkc(f"r8_{idx}", t1, t2, venue)
            if i < 3:
                _sp(H)
        _sp(H // 2)

    # Left QF (0-1)
    with c_qfl:
        _sp(3 * H // 2)
        for i, (idx, a, b, venue) in enumerate(QF[:2]):
            t1 = r8_w[a] if r8_w[a] != EMPTY else None
            t2 = r8_w[b] if r8_w[b] != EMPTY else None
            mkc(f"qf_{idx}", t1, t2, venue)
            if i == 0:
                _sp(3 * H)
        _sp(3 * H // 2)

    # Left SF (0)
    with c_sfl:
        _sp(7 * H // 2)
        idx0, a0, b0, v0 = SF[0]
        mkc(f"sf_{idx0}",
            qf_w[a0] if qf_w[a0] != EMPTY else None,
            qf_w[b0] if qf_w[b0] != EMPTY else None,
            v0)

    # FINALE + TERZO POSTO (center)
    with c_fin:
        ft1 = sf_w[0] if sf_w[0] != EMPTY else None
        ft2 = sf_w[1] if sf_w[1] != EMPTY else None
        l1  = sf_loser(0)
        l2  = sf_loser(1)
        _sp(7 * H // 2 - 18)
        st.markdown(
            '<div style="text-align:center;background:linear-gradient(150deg,#8a6800,#FFD700);'
            'border-radius:8px;padding:5px 4px;margin-bottom:5px;">'
            '<span style="color:#0A1628;font-size:9px;font-weight:900;letter-spacing:1px;">'
            '🏆 FINALE · 19 LUG</span></div>',
            unsafe_allow_html=True,
        )
        mkc("champion", ft1, ft2)
        st.markdown(
            '<div style="border-top:1px solid rgba(205,127,50,0.35);margin:8px 0 5px;'
            'text-align:center;padding-top:5px;font-size:8px;font-weight:700;'
            'color:#CD7F32;letter-spacing:0.8px;">🏅 TERZO POSTO · 18 LUG</div>',
            unsafe_allow_html=True,
        )
        mkc("third_pl",
            l1 if not l1.startswith("Perdente") else None,
            l2 if not l2.startswith("Perdente") else None)

    # Right SF (1)
    with c_sfr:
        _sp(7 * H // 2)
        idx1, a1, b1, v1 = SF[1]
        mkc(f"sf_{idx1}",
            qf_w[a1] if qf_w[a1] != EMPTY else None,
            qf_w[b1] if qf_w[b1] != EMPTY else None,
            v1)

    # Right QF (2-3)
    with c_qfr:
        _sp(3 * H // 2)
        for i, (idx, a, b, venue) in enumerate(QF[2:]):
            t1 = r8_w[a] if r8_w[a] != EMPTY else None
            t2 = r8_w[b] if r8_w[b] != EMPTY else None
            mkc(f"qf_{idx}", t1, t2, venue)
            if i == 0:
                _sp(3 * H)
        _sp(3 * H // 2)

    # Right R8 (4-7)
    with c_r8r:
        _sp(H // 2)
        for i, (idx, a, b, venue) in enumerate(R8[4:]):
            t1 = r16_w[a] if r16_w[a] != EMPTY else None
            t2 = r16_w[b] if r16_w[b] != EMPTY else None
            mkc(f"r8_{idx}", t1, t2, venue)
            if i < 3:
                _sp(H)
        _sp(H // 2)

    # Right R16 (8-15)
    for i in range(8, 16):
        _r16(c_r16r, i)

# TAB 3 — PREMI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_a:
    st.subheader("🌟 Premi Individuali")
    st.caption("Le tue previsioni per i premi individuali del Mondiale 2026.")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            '<div style="background:#0A1628;border-radius:12px;padding:10px 14px;'
            'border:1.5px solid #D4A017;margin-bottom:8px;text-align:center;">'
            '<span style="color:#FFD700;font-size:22px;">🏅</span>'
            '<div style="color:#FFD700;font-weight:800;font-size:13px;margin-top:4px;">'
            'MIGLIOR GIOCATORE</div></div>',
            unsafe_allow_html=True,
        )
        bp = st.session_state.get("best_player", EMPTY)
        st.selectbox(
            "Miglior Giocatore", PLAYERS,
            index=PLAYERS.index(bp) if bp in PLAYERS else 0,
            key="best_player",
            label_visibility="collapsed",
        )

    with c2:
        st.markdown(
            '<div style="background:#0A1628;border-radius:12px;padding:10px 14px;'
            'border:1.5px solid #D4A017;margin-bottom:8px;text-align:center;">'
            '<span style="color:#FFD700;font-size:22px;">⚽</span>'
            '<div style="color:#FFD700;font-weight:800;font-size:13px;margin-top:4px;">'
            'CAPOCANNONIERE</div></div>',
            unsafe_allow_html=True,
        )
        ts = st.session_state.get("top_scorer", EMPTY)
        st.selectbox(
            "Capocannoniere", PLAYERS,
            index=PLAYERS.index(ts) if ts in PLAYERS else 0,
            key="top_scorer",
            label_visibility="collapsed",
        )

    with c3:
        st.markdown(
            '<div style="background:#0A1628;border-radius:12px;padding:10px 14px;'
            'border:1.5px solid #D4A017;margin-bottom:8px;text-align:center;">'
            '<span style="color:#FFD700;font-size:22px;">🌱</span>'
            '<div style="color:#FFD700;font-weight:800;font-size:13px;margin-top:4px;">'
            'MIGLIOR UNDER 23</div></div>',
            unsafe_allow_html=True,
        )
        bu = st.session_state.get("best_u23", EMPTY)
        st.selectbox(
            "Miglior U23", U23_PLAYERS,
            index=U23_PLAYERS.index(bu) if bu in U23_PLAYERS else 0,
            key="best_u23",
            label_visibility="collapsed",
        )

    st.caption("Non trovi il giocatore? Digita il nome direttamente nella casella.")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# IMAGE GENERATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IMG_BG    = '#0A1628'
IMG_CARD  = '#162032'
IMG_LINE  = '#2d3f5a'
IMG_TEAL  = '#1DE9B6'
IMG_GOLD  = '#D4A017'
IMG_TEXT  = '#F0F6FC'
IMG_MUTED = '#8b949e'


def pill(ax, x, y, w, h, text, color=IMG_TEXT, bg=IMG_CARD, border=IMG_LINE,
         fontsize=7, bold=False):
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                          facecolor=bg, edgecolor=border, linewidth=0.6, zorder=2)
    ax.add_patch(rect)
    if text and text != EMPTY:
        short = text[:16]
        ax.text(x + w / 2, y + h / 2, short, ha='center', va='center',
                fontsize=fontsize, color=color,
                fontweight='bold' if bold else 'normal', zorder=3)
    else:
        ax.text(x + w / 2, y + h / 2, '?', ha='center', va='center',
                fontsize=fontsize, color=IMG_MUTED, zorder=3)


def generate_image(output_format: str = "jpeg") -> bytes:
    r16_win = get_winners("r16", 16)
    r8_win  = get_winners("r8", 8)
    qf_win  = get_winners("qf", 4)
    sf_win  = get_winners("sf", 2)
    champ   = st.session_state.get("champion", EMPTY)
    third   = st.session_state.get("third_pl", EMPTY)
    bp      = st.session_state.get("best_player", EMPTY)
    ts      = st.session_state.get("top_scorer", EMPTY)
    bu      = st.session_state.get("best_u23", EMPTY)

    fig = plt.figure(figsize=(20, 28), facecolor=IMG_BG)

    # Header
    ax_h = fig.add_axes([0, 0.965, 1, 0.035])
    ax_h.set_facecolor(IMG_TEAL)
    ax_h.axis('off')
    ax_h.text(0.5, 0.5, '🏆  FIFA WORLD CUP 2026  ·  MY PREDICTION',
              ha='center', va='center', fontsize=17, fontweight='bold',
              color=IMG_BG, transform=ax_h.transAxes)

    # Groups grid (3 rows × 4 cols)
    gkeys = list(GROUPS.keys())
    g_top, g_bot = 0.960, 0.600
    cell_w = 0.245
    cell_h = (g_top - g_bot) / 3 - 0.005
    POS_COLORS_IMG = [IMG_GOLD, '#d0d0d0', '#cd7f32', IMG_MUTED]
    POS_LABELS_IMG = ['1°', '2°', '3°', '4°']

    for gi, grp in enumerate(gkeys):
        col = gi % 4
        row = gi // 4
        lx = col * 0.25 + 0.005
        ly = g_top - (row + 1) * (cell_h + 0.008)
        ax = fig.add_axes([lx, ly, cell_w, cell_h])
        ax.set_facecolor(IMG_CARD)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        for s in ax.spines.values():
            s.set_edgecolor(IMG_GOLD)
            s.set_linewidth(0.8)
        ax.text(0.5, 0.90, f'GRUPPO {grp}', ha='center', va='center',
                fontsize=9, fontweight='bold', color=IMG_TEAL)
        for pos in range(4):
            team = grp_team(grp, pos)
            f = flag(team)
            yy = 0.72 - pos * 0.18
            ax.text(0.06, yy, POS_LABELS_IMG[pos], ha='left', va='center',
                    fontsize=7.5, color=POS_COLORS_IMG[pos], fontweight='bold')
            ax.text(0.24, yy, f"{f} {team[:14]}", ha='left', va='center',
                    fontsize=7, color=IMG_TEXT if pos < 2 else IMG_MUTED)

    # Bracket
    ax_br = fig.add_axes([0, 0.115, 1, 0.480])
    ax_br.set_facecolor(IMG_BG)
    ax_br.set_xlim(0, 100)
    ax_br.set_ylim(0, 100)
    ax_br.axis('off')
    ax_br.text(50, 97, '⚔️  TABELLONE — FASE AD ELIMINAZIONE DIRETTA',
               ha='center', va='center', fontsize=12, fontweight='bold', color=IMG_TEAL)

    col_info = [
        (10, "SEDICESIMI"), (27, "OTTAVI"), (44, "QUARTI"),
        (61, "SEMIFINALI"), (83, "FINALE"),
    ]
    for cx, name in col_info:
        ax_br.text(cx, 92, name, ha='center', va='center',
                   fontsize=8, color=IMG_MUTED, fontweight='bold')
        ax_br.plot([cx - 7, cx + 7], [90, 90], color=IMG_LINE, lw=0.4)

    PW, PH = 13, 3.8

    def draw_col(teams, cx, start_y, step, color=IMG_TEXT, bg=IMG_CARD,
                 border=IMG_LINE, fontsize=7, bold=False):
        for i, t in enumerate(teams):
            y = start_y - i * step
            pill(ax_br, cx - PW / 2, y - PH / 2, PW, PH, t,
                 color, bg, border, fontsize, bold)

    draw_col([r16_win[i] for i in range(8)],  5,  85, 10)
    draw_col([r16_win[i] for i in range(8, 16)], 16, 85, 10)
    draw_col([r8_win[i] for i in range(4)],  22, 80, 20)
    draw_col([r8_win[i] for i in range(4, 8)], 32, 80, 20)
    draw_col(qf_win[:2], 39, 70, 40)
    draw_col(qf_win[2:], 49, 70, 40)
    draw_col(sf_win[:1], 56, 50, 40, color=IMG_GOLD, border=IMG_GOLD, bold=True)
    draw_col(sf_win[1:], 67, 50, 40, color=IMG_GOLD, border=IMG_GOLD, bold=True)

    ax_br.annotate("", xy=(73, 50), xytext=(70, 50),
                   arrowprops=dict(arrowstyle="->", color=IMG_GOLD, lw=1.5))

    cx_final = 85
    rect_champ = FancyBboxPatch(
        (cx_final - 10, 38), 20, 24, boxstyle="round,pad=0.5",
        facecolor='#0f2a1a', edgecolor=IMG_GOLD, linewidth=2.5, zorder=2,
    )
    ax_br.add_patch(rect_champ)
    ax_br.text(cx_final, 60, '🏆', ha='center', va='center', fontsize=22, zorder=3)
    ax_br.text(cx_final, 54, 'CAMPIONE', ha='center', va='center',
               fontsize=8, color=IMG_GOLD, fontweight='bold', zorder=3)
    champ_disp = champ if champ and champ != EMPTY else '?'
    f_c = flag(champ_disp) if champ_disp != '?' else ''
    ax_br.text(cx_final, 47, f"{f_c} {champ_disp[:16]}", ha='center', va='center',
               fontsize=10, color=IMG_GOLD, fontweight='bold', zorder=3)
    third_disp = third if third and third != EMPTY else '?'
    f_t = flag(third_disp) if third_disp != '?' else ''
    ax_br.text(cx_final, 41, f"🥉 3°: {f_t} {third_disp[:12]}", ha='center', va='center',
               fontsize=8, color=IMG_MUTED, zorder=3)

    # Awards bar
    ax_aw = fig.add_axes([0, 0.04, 1, 0.07])
    ax_aw.set_facecolor(IMG_CARD)
    ax_aw.set_xlim(0, 1)
    ax_aw.set_ylim(0, 1)
    ax_aw.axis('off')
    ax_aw.plot([0, 1], [0.97, 0.97], color=IMG_TEAL, lw=1.5)

    awards = [
        ("🏅  MIGLIOR GIOCATORE", bp),
        ("⚽  CAPOCANNONIERE", ts),
        ("🌱  MIGLIOR UNDER 23", bu),
    ]
    for i, (label, val) in enumerate(awards):
        xi = (i + 0.5) / 3
        ax_aw.text(xi, 0.75, label, ha='center', va='center',
                   fontsize=8, color=IMG_MUTED, fontweight='bold')
        disp = val if val and val != EMPTY else '—'
        ax_aw.text(xi, 0.38, disp[:26], ha='center', va='center',
                   fontsize=10, color=IMG_TEXT, fontweight='bold')

    # Footer
    ax_f = fig.add_axes([0, 0, 1, 0.04])
    ax_f.set_facecolor(IMG_BG)
    ax_f.axis('off')
    ax_f.text(0.5, 0.6,
              'FIFA World Cup 2026  ·  USA · Canada · Messico  ·  11 giu – 19 lug 2026',
              ha='center', va='center', fontsize=8, color=IMG_MUTED)
    ax_f.plot([0.1, 0.9], [0.9, 0.9], color=IMG_LINE, lw=0.5)

    buf = io.BytesIO()
    fig.savefig(buf, format=output_format, dpi=140, bbox_inches='tight', facecolor=IMG_BG)
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 4 — SALVA
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_s:
    st.subheader("📸 Salva la tua Prediction")
    st.caption("Genera l'immagine e scaricala per condividerla su LinkedIn o Instagram.")

    # ── Gather results ─────────────────────────────────────────────
    _sf_w     = get_winners("sf", 2)
    champion  = st.session_state.get("champion", EMPTY)
    third_pl  = st.session_state.get("third_pl", EMPTY)
    runner_up = next((t for t in _sf_w if t != EMPTY and t != champion), EMPTY)
    bp        = st.session_state.get("best_player", EMPTY)
    ts        = st.session_state.get("top_scorer", EMPTY)
    bu        = st.session_state.get("best_u23", EMPTY)

    def _pn(team):
        if team == EMPTY:
            return "—"
        return f"{flag_img(team, 22)} {team}"

    # ── Podio ──────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div style="display:flex;align-items:flex-end;justify-content:center;
                    gap:10px;margin:28px 0 20px;">
          <div style="text-align:center;flex:1;">
            <div style="font-size:30px;margin-bottom:6px;">🥈</div>
            <div style="font-size:14px;font-weight:700;color:#e0e0e0;
                        margin-bottom:10px;min-height:42px;">{_pn(runner_up)}</div>
            <div style="background:linear-gradient(160deg,#6b6b6b,#c0c0c0);
                        border-radius:10px 10px 0 0;height:90px;
                        display:flex;align-items:center;justify-content:center;">
              <span style="color:#fff;font-size:26px;font-weight:900;">2°</span>
            </div>
          </div>
          <div style="text-align:center;flex:1;">
            <div style="font-size:38px;margin-bottom:6px;">🏆</div>
            <div style="font-size:16px;font-weight:900;color:#FFD700;
                        margin-bottom:10px;min-height:42px;">{_pn(champion)}</div>
            <div style="background:linear-gradient(160deg,#a07800,#FFD700);
                        border-radius:10px 10px 0 0;height:140px;
                        display:flex;align-items:center;justify-content:center;
                        box-shadow:0 0 24px rgba(255,215,0,0.45);">
              <span style="color:#0A1628;font-size:34px;font-weight:900;">1°</span>
            </div>
          </div>
          <div style="text-align:center;flex:1;">
            <div style="font-size:30px;margin-bottom:6px;">🥉</div>
            <div style="font-size:14px;font-weight:700;color:#c8986a;
                        margin-bottom:10px;min-height:42px;">{_pn(third_pl)}</div>
            <div style="background:linear-gradient(160deg,#5c3410,#cd7f32);
                        border-radius:10px 10px 0 0;height:60px;
                        display:flex;align-items:center;justify-content:center;">
              <span style="color:#fff;font-size:22px;font-weight:900;">3°</span>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Premi individuali ──────────────────────────────────────────
    st.markdown(
        '<div style="text-align:center;color:#1DE9B6;font-weight:800;font-size:12px;'
        'letter-spacing:1.5px;margin-bottom:14px;">🌟  PREMI INDIVIDUALI</div>',
        unsafe_allow_html=True,
    )
    a1, a2, a3 = st.columns(3)
    with a1:
        st.metric("🏅 Miglior Giocatore", bp if bp != EMPTY else "—")
    with a2:
        st.metric("⚽ Capocannoniere", ts if ts != EMPTY else "—")
    with a3:
        st.metric("🌱 Miglior U23", bu if bu != EMPTY else "—")

    st.divider()

    if st.button("🎨 Genera Immagine", type="primary", use_container_width=True):
        with st.spinner("Generando l'immagine..."):
            st.session_state["_img_jpg"] = generate_image("jpeg")
            st.session_state["_img_pdf"] = generate_image("pdf")

    if "_img_jpg" in st.session_state:
        dl1, dl2 = st.columns(2)
        with dl1:
            st.download_button(
                label="⬇️  Scarica JPG",
                data=st.session_state["_img_jpg"],
                file_name="wc2026_my_prediction.jpg",
                mime="image/jpeg",
                use_container_width=True,
            )
        with dl2:
            st.download_button(
                label="📄  Scarica PDF",
                data=st.session_state["_img_pdf"],
                file_name="wc2026_my_prediction.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        st.success("✅ Pronta! Condividi con l'hashtag #WorldCup2026 #FIFA2026")
