"""FIFA World Cup 2026 — Prediction App"""

import streamlit as st
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import io

st.set_page_config(
    page_title="WC 2026 · My Prediction",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""<style>
.main .block-container {padding-top:1.2rem;padding-bottom:2rem;}
.stTabs [data-baseweb="tab-list"] {background:#0d1117;padding:4px;border-radius:8px;gap:4px;}
.stTabs [data-baseweb="tab"] {border-radius:6px;color:#8b949e;padding:6px 16px;}
.stTabs [aria-selected="true"] {background:#161b22;color:#f0f6fc;font-weight:600;}
h1 {font-size:1.7rem!important;margin-bottom:0!important;}
h2 {font-size:1.1rem!important;}
</style>""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
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

PLAYERS = [
    "— scegli —",
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
    "— scegli —",
    "Lamine Yamal (ESP · 2007)", "Pau Cubarsí (ESP · 2007)",
    "Warren Zaïre-Emery (FRA · 2006)", "Endrick (BRA · 2006)",
    "Mathys Tel (FRA · 2005)", "Leny Yoro (FRA · 2005)",
    "Kobbie Mainoo (ENG · 2005)", "Arda Güler (TUR · 2005)",
    "Alejandro Garnacho (ARG · 2004)", "Savinho (BRA · 2004)",
    "Gavi (ESP · 2004)", "João Neves (POR · 2004)", "Rico Lewis (ENG · 2004)",
    "Jamal Musiala (GER · 2003)", "Florian Wirtz (GER · 2003)",
    "Xavi Simons (NED · 2003)",
]

EMPTY = "— scegli —"

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

# (idx, r16_a, r16_b, venue)
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

# (idx, r8_a, r8_b, venue)
QF = [
    (0, 0, 1, "11 lug · Atlanta"),
    (1, 2, 3, "11 lug"),
    (2, 4, 5, "10 lug"),
    (3, 6, 7, "9 lug"),
]

# (idx, qf_a, qf_b, venue)
SF = [
    (0, 0, 1, "15 lug · Atlanta"),
    (1, 2, 3, "14 lug · Dallas"),
]

# ── Session state ─────────────────────────────────────────────────────────────
def _init():
    for grp, teams in GROUPS.items():
        for pos in range(4):
            k = f"g_{grp}_{pos}"
            if k not in st.session_state:
                st.session_state[k] = teams[pos]
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
    return st.session_state.get(f"g_{g}_{pos}", GROUPS[g][pos])

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
    """Render a match row: venue + teams + winner selectbox."""
    is_third = (t2 is None)
    if is_third:
        opts = dedup([EMPTY] + (thirds_pool or []) + ([t1] if t1 else []))
        t2_label = "Miglior 3ª"
    else:
        opts = dedup([EMPTY, t1, t2 or "?"])
        t2_label = t2 or "?"

    if not opts[0] == EMPTY:
        opts = [EMPTY] + opts

    curr = st.session_state.get(state_key, EMPTY)
    if curr not in opts:
        curr = EMPTY

    c1, c2 = st.columns([4, 2])
    with c1:
        st.caption(venue)
        st.markdown(f"**{t1 or '?'}** vs **{t2_label}**")
        if is_third and thirds_pool:
            st.caption("Possibili terze: " + ", ".join(thirds_pool[:4]) + ("…" if len(thirds_pool) > 4 else ""))
    with c2:
        st.selectbox("Vincitore", opts, index=opts.index(curr),
                     key=state_key, label_visibility="collapsed")

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

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# 🏆 FIFA World Cup 2026 · My Prediction")
st.caption("USA · Canada · Messico  |  11 giugno – 19 luglio 2026  |  48 squadre · 104 partite")
st.divider()

tab_g, tab_b, tab_a, tab_s = st.tabs(["📋  Gironi", "⚔️  Tabellone", "🌟  Premi", "📸  Salva"])

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 1 — GIRONI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_g:
    st.subheader("Fase a Gironi — Classifica Prevista")
    st.caption("Seleziona l'ordine dal 1° al 4° per ogni gruppo. I primi due avanzano direttamente.")

    POS_LABELS = ["🥇 1°", "🥈 2°", "🥉 3°", "4°"]
    group_list = list(GROUPS.keys())

    for row_start in range(0, 12, 4):
        cols = st.columns(4)
        for ci in range(4):
            gi = row_start + ci
            if gi >= 12:
                break
            grp = group_list[gi]
            teams = GROUPS[grp]
            with cols[ci]:
                st.markdown(f"**GRUPPO {grp}**")
                for pos in range(4):
                    st.selectbox(
                        POS_LABELS[pos],
                        options=teams,
                        key=f"g_{grp}_{pos}",
                        label_visibility="visible",
                    )
        st.markdown("")

    st.divider()
    st.subheader("🥉 Migliori Terze (8 di 12)")
    st.caption(
        "Nel formato a 48 squadre le 8 migliori terze avanzano ai sedicesimi. "
        "Seleziona le 8 che pensi si qualificheranno."
    )
    third_teams = [grp_team(g, 2) for g in group_list]
    sel = st.multiselect(
        "Scegli le 8 migliori terze",
        options=third_teams,
        key="thirds",
    )
    n = len(sel)
    if n > 8:
        st.error(f"⚠️ Massimo 8 terze. Hai selezionato {n}.")
    elif n < 8:
        st.info(f"Seleziona ancora {8 - n} squadra/e.")
    else:
        st.success("✅ 8 migliori terze selezionate!")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 2 — TABELLONE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_b:
    thirds_pool = [t for t in st.session_state.get("thirds", []) if t != EMPTY][:8]

    # ── Sedicesimi ───────────────────────────────────────────────
    with st.expander("⚔️  Sedicesimi di Finale  (32 → 16)", expanded=True):
        st.caption("Scegli il vincitore di ogni partita.")
        left, right = st.columns(2)
        for idx, s1, s2, venue in R16:
            t1 = slot_team(s1)
            t2 = slot_team(s2)
            col = left if idx < 8 else right
            with col:
                match_widget(f"r16_{idx}", venue, t1, t2, thirds_pool if s2 == "3?" else None)
                st.markdown("")

    # ── Ottavi ──────────────────────────────────────────────────
    r16_w = get_winners("r16", 16)
    with st.expander("🔥  Ottavi di Finale  (16 → 8)", expanded=False):
        st.caption("Popola i Sedicesimi prima per vedere i nomi automaticamente.")
        left, right = st.columns(2)
        for idx, a, b, venue in R8:
            t1 = r16_w[a] if r16_w[a] != EMPTY else f"Vinc. S{a+1}"
            t2 = r16_w[b] if r16_w[b] != EMPTY else f"Vinc. S{b+1}"
            opts = dedup([EMPTY, t1, t2])
            curr = st.session_state.get(f"r8_{idx}", EMPTY)
            if curr not in opts:
                curr = EMPTY
            col = left if idx < 4 else right
            with col:
                c1, c2 = st.columns([4, 2])
                with c1:
                    st.caption(venue)
                    st.markdown(f"**{t1}** vs **{t2}**")
                with c2:
                    st.selectbox("Vinc.", opts, index=opts.index(curr),
                                 key=f"r8_{idx}", label_visibility="collapsed")
                st.markdown("")

    # ── Quarti ──────────────────────────────────────────────────
    r8_w = get_winners("r8", 8)
    with st.expander("⚡  Quarti di Finale  (8 → 4)", expanded=False):
        cols = st.columns(2)
        for idx, a, b, venue in QF:
            t1 = r8_w[a] if r8_w[a] != EMPTY else f"Vinc. O{a+1}"
            t2 = r8_w[b] if r8_w[b] != EMPTY else f"Vinc. O{b+1}"
            opts = dedup([EMPTY, t1, t2])
            curr = st.session_state.get(f"qf_{idx}", EMPTY)
            if curr not in opts:
                curr = EMPTY
            with cols[idx % 2]:
                c1, c2 = st.columns([4, 2])
                with c1:
                    st.caption(venue)
                    st.markdown(f"**{t1}** vs **{t2}**")
                with c2:
                    st.selectbox("Vinc.", opts, index=opts.index(curr),
                                 key=f"qf_{idx}", label_visibility="collapsed")
                st.markdown("")

    # ── Semifinali ──────────────────────────────────────────────
    qf_w = get_winners("qf", 4)
    with st.expander("🌟  Semifinali  (4 → 2)", expanded=False):
        cols = st.columns(2)
        for idx, a, b, venue in SF:
            t1 = qf_w[a] if qf_w[a] != EMPTY else f"Vinc. Q{a+1}"
            t2 = qf_w[b] if qf_w[b] != EMPTY else f"Vinc. Q{b+1}"
            opts = dedup([EMPTY, t1, t2])
            curr = st.session_state.get(f"sf_{idx}", EMPTY)
            if curr not in opts:
                curr = EMPTY
            with cols[idx]:
                c1, c2 = st.columns([4, 2])
                with c1:
                    st.caption(venue)
                    st.markdown(f"**{t1}** vs **{t2}**")
                with c2:
                    st.selectbox("Vinc.", opts, index=opts.index(curr),
                                 key=f"sf_{idx}", label_visibility="collapsed")
                st.markdown("")

    # ── Finali ──────────────────────────────────────────────────
    sf_w = get_winners("sf", 2)
    with st.expander("🏆  Finali", expanded=True):
        col_f, col_3 = st.columns(2)

        # Finale
        ft1 = sf_w[0] if sf_w[0] != EMPTY else "Vinc. SF1"
        ft2 = sf_w[1] if sf_w[1] != EMPTY else "Vinc. SF2"
        fopts = dedup([EMPTY, ft1, ft2])
        fcurr = st.session_state.get("champion", EMPTY)
        if fcurr not in fopts:
            fcurr = EMPTY
        with col_f:
            st.markdown("**🏆 FINALE** · 19 luglio · MetLife Stadium, New Jersey")
            c1, c2 = st.columns([4, 2])
            with c1:
                st.markdown(f"**{ft1}** vs **{ft2}**")
            with c2:
                st.selectbox("Campione", fopts, index=fopts.index(fcurr),
                             key="champion", label_visibility="collapsed")

        # 3° posto
        l1 = sf_loser(0)
        l2 = sf_loser(1)
        t3opts = dedup([EMPTY, l1, l2])
        t3curr = st.session_state.get("third_pl", EMPTY)
        if t3curr not in t3opts:
            t3curr = EMPTY
        with col_3:
            st.markdown("**🥉 FINALE 3° POSTO** · 18 luglio · Miami")
            c1, c2 = st.columns([4, 2])
            with c1:
                st.markdown(f"**{l1}** vs **{l2}**")
            with c2:
                st.selectbox("3° posto", t3opts, index=t3opts.index(t3curr),
                             key="third_pl", label_visibility="collapsed")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 3 — PREMI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_a:
    st.subheader("🌟 Premi Individuali")
    st.caption("Le tue previsioni per i premi individuali del Mondiale 2026.")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("#### 🏅 Miglior Giocatore")
        bp = st.session_state.get("best_player", EMPTY)
        st.selectbox("Miglior Giocatore", PLAYERS,
                     index=PLAYERS.index(bp) if bp in PLAYERS else 0,
                     key="best_player", label_visibility="collapsed")

    with c2:
        st.markdown("#### ⚽ Capocannoniere")
        ts = st.session_state.get("top_scorer", EMPTY)
        st.selectbox("Capocannoniere", PLAYERS,
                     index=PLAYERS.index(ts) if ts in PLAYERS else 0,
                     key="top_scorer", label_visibility="collapsed")

    with c3:
        st.markdown("#### 🌱 Miglior Under 23")
        bu = st.session_state.get("best_u23", EMPTY)
        st.selectbox("Miglior U23", U23_PLAYERS,
                     index=U23_PLAYERS.index(bu) if bu in U23_PLAYERS else 0,
                     key="best_u23", label_visibility="collapsed")

    st.caption("Non trovi il giocatore? Digita il nome direttamente nella casella.")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# IMAGE GENERATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BG    = '#0d1117'
CARD  = '#161b22'
LINE  = '#30363d'
BLUE  = '#58a6ff'
GREEN = '#3fb950'
GOLD  = '#d4a017'
TEXT  = '#e6edf3'
MUTED = '#8b949e'

def pill(ax, x, y, w, h, text, color=TEXT, bg=CARD, border=LINE, fontsize=7, bold=False):
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                          facecolor=bg, edgecolor=border, linewidth=0.6, zorder=2)
    ax.add_patch(rect)
    if text and text != EMPTY:
        short = text[:15]
        ax.text(x + w / 2, y + h / 2, short, ha='center', va='center',
                fontsize=fontsize, color=color,
                fontweight='bold' if bold else 'normal', zorder=3)
    else:
        ax.text(x + w / 2, y + h / 2, '?', ha='center', va='center',
                fontsize=fontsize, color=MUTED, zorder=3)


def generate_image() -> bytes:
    r16_w  = get_winners("r16", 16)
    r8_w   = get_winners("r8", 8)
    qf_w   = get_winners("qf", 4)
    sf_w   = get_winners("sf", 2)
    champ  = st.session_state.get("champion", EMPTY)
    third  = st.session_state.get("third_pl", EMPTY)
    bp     = st.session_state.get("best_player", EMPTY)
    ts     = st.session_state.get("top_scorer", EMPTY)
    bu     = st.session_state.get("best_u23", EMPTY)

    fig = plt.figure(figsize=(20, 28), facecolor=BG)

    # ── 1. Header ────────────────────────────────────────────────
    ax_h = fig.add_axes([0, 0.965, 1, 0.035])
    ax_h.set_facecolor(BLUE)
    ax_h.axis('off')
    ax_h.text(0.5, 0.5, '🏆  FIFA WORLD CUP 2026  ·  MY PREDICTION',
              ha='center', va='center', fontsize=17, fontweight='bold',
              color='white', transform=ax_h.transAxes)

    # ── 2. Groups ────────────────────────────────────────────────
    # 3 rows × 4 cols grid, occupies y=[0.60, 0.960]
    gkeys = list(GROUPS.keys())
    g_top = 0.960
    g_bot = 0.600
    cell_w = 0.245
    cell_h = (g_top - g_bot) / 3 - 0.005

    POS_COLORS = [GOLD, GREEN, MUTED, MUTED]
    POS_LABELS_IMG = ['1°', '2°', '3°', '4°']

    for gi, grp in enumerate(gkeys):
        col = gi % 4
        row = gi // 4
        lx = col * 0.25 + 0.005
        ly = g_top - (row + 1) * (cell_h + 0.008)
        ax = fig.add_axes([lx, ly, cell_w, cell_h])
        ax.set_facecolor(CARD)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        for s in ax.spines.values():
            s.set_edgecolor(LINE)
            s.set_linewidth(0.5)
        ax.text(0.5, 0.90, f'GRUPPO {grp}', ha='center', va='center',
                fontsize=9, fontweight='bold', color=BLUE)
        for pos in range(4):
            team = grp_team(grp, pos)
            yy = 0.72 - pos * 0.18
            ax.text(0.06, yy, POS_LABELS_IMG[pos], ha='left', va='center',
                    fontsize=7.5, color=POS_COLORS[pos], fontweight='bold')
            ax.text(0.26, yy, team[:16], ha='left', va='center',
                    fontsize=7.5, color=TEXT if pos < 2 else MUTED)

    # ── 3. Bracket ──────────────────────────────────────────────
    # Occupies y=[0.115, 0.595]
    ax_br = fig.add_axes([0, 0.115, 1, 0.480])
    ax_br.set_facecolor(BG)
    ax_br.set_xlim(0, 100)
    ax_br.set_ylim(0, 100)
    ax_br.axis('off')

    ax_br.text(50, 97, '⚔️  TABELLONE — FASE AD ELIMINAZIONE DIRETTA',
               ha='center', va='center', fontsize=12, fontweight='bold', color=BLUE)

    # Column x centers and headers
    col_info = [
        (10,  "SEDICESIMI"),
        (27,  "OTTAVI"),
        (44,  "QUARTI"),
        (61,  "SEMIFINALI"),
        (83,  "FINALE"),
    ]
    for cx, name in col_info:
        ax_br.text(cx, 92, name, ha='center', va='center',
                   fontsize=8, color=MUTED, fontweight='bold')
        ax_br.plot([cx - 7, cx + 7], [90, 90], color=LINE, lw=0.4)

    PW, PH = 13, 3.8  # pill width, height

    def draw_col(teams, cx, start_y, step, color=TEXT, bg=CARD, border=LINE, fontsize=7, bold=False):
        for i, t in enumerate(teams):
            y = start_y - i * step
            pill(ax_br, cx - PW / 2, y - PH / 2, PW, PH, t, color, bg, border, fontsize, bold)

    # Sedicesimi: 2 sub-cols (L: 0-7, R: 8-15)
    left_16 = [r16_w[i] for i in range(8)]
    right_16 = [r16_w[i] for i in range(8, 16)]
    draw_col(left_16, 5, 85, 10)
    draw_col(right_16, 16, 85, 10)

    # Ottavi: 2 sub-cols (L: 0-3, R: 4-7)
    left_8 = [r8_w[i] for i in range(4)]
    right_8 = [r8_w[i] for i in range(4, 8)]
    draw_col(left_8, 22, 80, 20)
    draw_col(right_8, 32, 80, 20)

    # Quarti: 2 sub-cols (0-1, 2-3)
    draw_col(qf_w[:2], 39, 70, 40)
    draw_col(qf_w[2:], 49, 70, 40)

    # Semifinali
    draw_col(sf_w[:1], 56, 50, 40, color=GOLD, border=GOLD, bold=True)
    draw_col(sf_w[1:], 67, 50, 40, color=GOLD, border=GOLD, bold=True)

    # Arrow to final
    ax_br.annotate("", xy=(73, 50), xytext=(70, 50),
                   arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.5))

    # Champion box
    cx_final = 85
    rect_champ = FancyBboxPatch((cx_final - 10, 38), 20, 24,
                                 boxstyle="round,pad=0.5",
                                 facecolor='#1a2e1a', edgecolor=GOLD, linewidth=2.5, zorder=2)
    ax_br.add_patch(rect_champ)
    ax_br.text(cx_final, 60, '🏆', ha='center', va='center', fontsize=22, zorder=3)
    ax_br.text(cx_final, 54, 'CAMPIONE', ha='center', va='center',
               fontsize=8, color=GOLD, fontweight='bold', zorder=3)
    champ_disp = champ if champ and champ != EMPTY else '?'
    ax_br.text(cx_final, 48, champ_disp[:18], ha='center', va='center',
               fontsize=11, color=GOLD, fontweight='bold', zorder=3)
    third_disp = third if third and third != EMPTY else '?'
    ax_br.text(cx_final, 42, f"🥉  3° posto: {third_disp[:14]}", ha='center', va='center',
               fontsize=8, color=MUTED, zorder=3)

    # ── 4. Awards ───────────────────────────────────────────────
    ax_aw = fig.add_axes([0, 0.04, 1, 0.07])
    ax_aw.set_facecolor(CARD)
    ax_aw.set_xlim(0, 1)
    ax_aw.set_ylim(0, 1)
    ax_aw.axis('off')
    ax_aw.plot([0, 1], [0.97, 0.97], color=BLUE, lw=1.5)

    awards = [
        ("🏅  MIGLIOR GIOCATORE", bp),
        ("⚽  CAPOCANNONIERE", ts),
        ("🌱  MIGLIOR UNDER 23", bu),
    ]
    for i, (label, val) in enumerate(awards):
        xi = (i + 0.5) / 3
        ax_aw.text(xi, 0.75, label, ha='center', va='center',
                   fontsize=8, color=MUTED, fontweight='bold')
        disp = val if val and val != EMPTY else '—'
        ax_aw.text(xi, 0.38, disp[:26], ha='center', va='center',
                   fontsize=10, color=TEXT, fontweight='bold')

    # ── 5. Footer ───────────────────────────────────────────────
    ax_f = fig.add_axes([0, 0, 1, 0.04])
    ax_f.set_facecolor(BG)
    ax_f.axis('off')
    ax_f.text(0.5, 0.6, 'FIFA World Cup 2026  ·  USA · Canada · Messico  ·  11 giu – 19 lug 2026',
              ha='center', va='center', fontsize=8, color=MUTED)
    ax_f.plot([0.1, 0.9], [0.9, 0.9], color=LINE, lw=0.5)

    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=140, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 4 — SALVA
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_s:
    st.subheader("📸 Salva la tua Prediction")
    st.caption("Genera l'immagine e scaricala per condividerla su LinkedIn o Instagram.")

    champion = st.session_state.get("champion", EMPTY)
    third_pl = st.session_state.get("third_pl", EMPTY)
    bp       = st.session_state.get("best_player", EMPTY)
    ts       = st.session_state.get("top_scorer", EMPTY)
    bu       = st.session_state.get("best_u23", EMPTY)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("🏆 Campione del Mondo", champion if champion != EMPTY else "—")
        st.metric("🥉 3° Posto", third_pl if third_pl != EMPTY else "—")
    with c2:
        st.metric("🏅 Miglior Giocatore", bp if bp != EMPTY else "—")
        st.metric("⚽ Capocannoniere", ts if ts != EMPTY else "—")
    with c3:
        st.metric("🌱 Miglior U23", bu if bu != EMPTY else "—")
        thirds_ok = len([t for t in st.session_state.get("thirds", []) if t != EMPTY])
        st.metric("🥉 Terze qualificate", f"{thirds_ok}/8")

    st.divider()

    if st.button("🎨 Genera Immagine", type="primary", use_container_width=True):
        with st.spinner("Generando l'immagine..."):
            img_bytes = generate_image()
        st.image(img_bytes, use_container_width=True)
        st.download_button(
            label="⬇️  Scarica PNG",
            data=img_bytes,
            file_name="wc2026_my_prediction.png",
            mime="image/png",
            use_container_width=True,
        )
        st.success("✅ Pronta! Condividi su LinkedIn con l'hashtag #WorldCup2026")
