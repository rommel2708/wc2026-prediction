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
    white-space: nowrap !important;
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
    white-space: nowrap !important;
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

/* === BRACKET: UNIFORM BUTTON HEIGHT === */
.stButton > button[kind="primary"], .stButton > button[kind="secondary"] {
    min-height: 36px !important;
    max-height: 36px !important;
    height: 36px !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    font-size: 11px !important;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}
/* Bracket: remove stButton wrapper vertical margin */
div[data-testid="stVerticalBlock"] .stButton {
    margin-top: 1px !important;
    margin-bottom: 1px !important;
}
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


# Formato: (nome, ruolo P/D/C/A, anno nascita, club)
PLAYERS_DB: dict = {
    'Algeria': [
        ('Riyad Mahrez','A',1991,'Al-Ahli'),('Mohamed Amoura','A',2000,'Wolfsburg'),
        ('Amine Gouiri','A',2000,'Marsiglia'),('Anis Hadj Moussa','A',2002,'Feyenoord'),
        ('Adil Boulbina','A',2003,'Al-Duhail'),('Nadhir Benbouali','A',2000,'Gyor'),
        ('Fares Ghedjemis','A',2002,'Frosinone'),('Ibrahim Maza','C',2005,'Leverkusen'),
        ('Houssem Aouar','C',1998,'Al-Ittihad'),('Nabil Bentaleb','C',1994,'Lilla'),
        ('Ramiz Zerrouki','C',1998,'Twente'),('Hicham Boudaoui','C',1999,'Nizza'),
        ('Fares Chaibi','C',2002,'Francoforte'),('Yacine Titraoui','C',2003,'Charleroi'),
        ('Aissa Mandi','D',1991,'Lilla'),('Ramy Bensebaini','D',1995,'Dortmund'),
        ('Rayan Ait-Nouri','D',2001,'Manchester City'),('Jaouen Hadjam','D',2003,'Young Boys'),
        ('Rafik Belghali','D',2002,'Hellas Verona'),('Zineddine Belaid','D',1999,'JS Kabylie'),
        ('Achref Abada','D',1999,'USM'),('Samir Chergui','D',1999,'Paris FC'),
        ('Luca Zidane','P',1998,'Granada'),('Oussama Benbot','P',1994,'USM'),
        ('Melvin Mastil','P',2000,'Stade Nyonnais'),('Mohamed Amine Tougai','D',2000,'Esperance'),
    ],
    'Arabia Saudita': [
        ('Salem Al-Dawsari','A',1991,'Al-Hilal'),('Firas Al-Buraikan','A',1999,'Al-Hilal'),
        ('Abdullah Al-Hamdan','A',1998,'Al-Shabab'),('Hattan Bahebri','A',1996,'Al-Ittihad'),
        ('Saleh Al-Shehri','A',1993,'Al-Hilal'),('Fahad Al-Muwallad','A',1994,'Al-Ittihad'),
        ('Mohammed Al-Marshoudi','A',1997,'Al-Fateh'),('Marcelinho','A',1989,'Al-Quadisiya'),
        ('Salman Al-Faraj','C',1989,'Al-Hilal'),('Mohammed Kanno','C',1996,'Al-Ittihad'),
        ('Haitham Asiri','C',1993,'Al-Hilal'),('Abdullah Madu','C',1998,'Al-Qadsiah'),
        ('Khalid Ayesh','C',1993,'Al-Hilal'),('Abdulrahman Al-Aboud','C',1997,'Al-Qadsiah'),
        ('Abdullah Radif','C',1994,'Al-Ittihad'),('Saud Abdulhamid','D',1999,'Roma'),
        ('Ali Al-Bulayhi','D',1989,'Al-Hilal'),('Hassan Tambakti','D',2000,'Al-Hilal'),
        ('Yasser Al-Shahrani','D',1992,'Al-Hilal'),('Mohamed Al-Breik','D',1994,'Al-Ittihad'),
        ('Sultan Al-Ghannam','D',1996,'Al-Hilal'),('Riyadh Sharahili','D',1995,'Al-Nassr'),
        ('Nawaf Boushal','D',1999,'Al-Hilal'),('Mohammed Al-Owais','P',1991,'Al-Hilal'),
        ('Nawaf Al-Aqidi','P',1991,'Al-Qadsiah'),('Abdulelah Al-Malki','P',1994,'Al-Feiha'),
    ],
    'Argentina': [
        ('Lionel Messi','A',1987,'Inter Miami'),('Lautaro Martinez','A',1997,'Inter'),
        ('Julian Alvarez','A',2000,'Atletico'),('Nicolas Gonzalez','A',1998,'Juventus'),
        ('Thiago Almada','A',2001,'Atletico'),('Jose Manuel Lopez','A',2000,'Palmeiras'),
        ('Nico Paz','A',2004,'Como'),('Alexis Mac Allister','C',1998,'Liverpool'),
        ('Enzo Fernandez','C',2001,'Chelsea'),('Rodrigo De Paul','C',1994,'Inter Miami'),
        ('Leandro Paredes','C',1994,'Boca Juniors'),('Giovani Lo Celso','C',1996,'Betis'),
        ('Exequiel Palacios','C',1998,'Leverkusen'),('Valentin Barco','C',2004,'Strasburgo'),
        ('Cristian Romero','D',1998,'Tottenham'),('Lisandro Martinez','D',1998,'Manchester United'),
        ('Nahuel Molina','D',1998,'Atletico'),('Nicolas Otamendi','D',1988,'Benfica'),
        ('Nicolas Tagliafico','D',1992,'Lione'),('German Pezzella','D',1991,'River Plate'),
        ('Gonzalo Montiel','D',1997,'River Plate'),('Facundo Medina','D',1999,'Marsiglia'),
        ('Emiliano Martinez','P',1992,'Aston Villa'),('Geronimo Rulli','P',1992,'Marsiglia'),
        ('Juan Musso','P',1994,'Atletico'),
    ],
    'Australia': [
        ('Mathew Leckie','A',1991,'Melbourne'),('Awer Mabil','A',1995,'Castellon'),
        ('Nestory Irankunda','A',2006,'Watford'),('Mohamed Toure','A',2004,'Norwich'),
        ('Nishan Velupillay','A',2001,'Melbourne'),('Tete Yengi','A',2000,'Machida'),
        ('Jackson Irvine','C',1993,'St. Pauli'),('Ajdin Hrustic','C',1996,'Heracles'),
        ('Cameron Devlin','C',1998,'Hearts'),('Connor Metcalfe','C',1999,'St. Pauli'),
        ("Aiden O'Neill",'C',1998,'New York City'),('Cristian Volpato','C',2003,'Sassuolo'),
        ('Paul Okon-Engstler','C',2005,'Sydney'),('Kai Trewin','C',2001,'New York City'),
        ('Harry Souttar','D',1998,'Leicester'),('Milos Degenek','D',1994,'APOEL'),
        ('Aziz Behich','D',1990,'Melbourne'),('Cameron Burgess','D',1995,'Swansea'),
        ('Alessandro Circati','D',2003,'Parma'),('Jordan Bos','D',2002,'Feyenoord'),
        ('Jason Geria','D',1993,'Albirex'),('Jacob Italiano','D',2001,'Grazer AK'),
        ('Lucas Herrington','D',2007,'Colorado'),('Maty Ryan','P',1992,'Levante'),
        ('Patrick Beach','P',2003,'Melbourne'),('Paul Izzo','P',1995,'Randers'),
    ],
    'Austria': [
        ('Marko Arnautovic','A',1989,'Stella Rossa'),('Michael Gregoritsch','A',1994,'Augusta'),
        ('Sasa Kalajdzic','A',1997,'LASK'),('Christoph Baumgartner','C',1999,'Lipsia'),
        ('Konrad Laimer','C',1997,'Bayern'),('Marcel Sabitzer','C',1994,'Dortmund'),
        ('Xaver Schlager','C',1997,'Lipsia'),('Romano Schmid','C',2000,'Brema'),
        ('Nicolas Seiwald','C',2001,'Lipsia'),('Carney Chukwuemeka','C',2003,'Dortmund'),
        ('Paul Wanner','C',2005,'PSV'),('Patrick Wimmer','C',2001,'Wolfsburg'),
        ('Florian Grillitsch','C',1995,'SC Braga'),('Alessandro Schopf','C',1994,'Wolfsberger'),
        ('David Alaba','D',1992,'Real Madrid'),('Kevin Danso','D',1998,'Tottenham'),
        ('Marco Friedl','D',1998,'Brema'),('Stefan Posch','D',1997,'Magonza'),
        ('Philipp Lienhart','D',1996,'Friburgo'),('David Affengruber','D',2001,'Elche'),
        ('Alexander Prass','D',2001,'Hoffenheim'),('Michael Svoboda','D',1998,'Venezia'),
        ('Phillipp Mwene','D',1994,'Magonza'),('Patrick Pentz','P',1997,'Brondby'),
        ('Alexander Schlager','P',1996,'Salisburgo'),('Florian Wiegele','P',2001,'Plzen'),
    ],
    'Belgio': [
        ('Romelu Lukaku','A',1993,'Napoli'),('Charles De Ketelaere','A',2001,'Atalanta'),
        ('Jeremy Doku','A',2002,'Manchester City'),('Leandro Trossard','A',1994,'Arsenal'),
        ('Dodi Lukebakio','A',1997,'Benfica'),('Alexis Saelemaekers','A',1999,'Milan'),
        ('Diego Moreira','A',2004,'Strasburgo'),('Matias Fernandez-Pardo','A',2005,'Lilla'),
        ('Kevin De Bruyne','C',1991,'Napoli'),('Amadou Onana','C',2001,'Aston Villa'),
        ('Youri Tielemans','C',1997,'Aston Villa'),('Nicolas Raskin','C',2001,'Glasgow Rangers'),
        ('Hans Vanaken','C',1992,'Bruges'),('Axel Witsel','C',1989,'Girona'),
        ('Timothy Castagne','D',1995,'Fulham'),('Zeno Debast','D',2003,'Sporting'),
        ('Maxim De Cupyer','D',2000,'Brighton'),('Koni De Winter','D',2002,'Milan'),
        ('Brandon Mechele','D',1993,'Bruges'),('Thomas Meunier','D',1991,'Lilla'),
        ('Arthur Theate','D',2000,'Francoforte'),('Nathan Ngoy','D',2003,'Lilla'),
        ('Joaquin Seys','D',2005,'Bruges'),('Thibaut Courtois','P',1992,'Real Madrid'),
        ('Senne Lammens','P',2002,'Manchester United'),('Mike Penders','P',2005,'Strasburgo'),
    ],
    'Bosnia': [
        ('Edin Dzeko','A',1986,'Schalke'),('Ermedin Demirovic','A',1998,'Stoccarda'),
        ('Samed Bazdar','A',2004,'Jagiellonia'),('Jovo Lukic','A',1998,'U Cluj'),
        ("Haris Tabakovic",'A',1994,"M'Gladbach"),('Amir Hadziahmetovic','C',1997,'Hull'),
        ('Ivan Sunjic','C',1996,'Pafos'),('Dzenis Burnic','C',1998,'Karlsruhe'),
        ('Ivan Basic','C',2002,'Astana'),('Armina Gigovic','C',2002,'Young Boys'),
        ('Benjamin Tahirovic','C',2003,'Brondby'),('Amar Memic','C',2001,'Plzen'),
        ('Esmir Bajraktarevic','C',2005,'PSV'),('Ermin Mahmic','C',2005,'Liberec'),
        ('Kerim Alajbegovic','C',2007,'Salisburgo'),('Sead Kolasinac','D',1993,'Atalanta'),
        ('Amar Dedic','D',2002,'Benfica'),('Dennis Hadzikadunoc','D',1998,'Sampdoria'),
        ('Nikola Katic','D',1996,'Schalke'),('Tarik Muharemovic','D',2003,'Sassuolo'),
        ('Nihad Mujakic','D',1998,'Gaziantep'),('Stjepan Radeljic','D',1997,'Rijeka'),
        ('Nidal Celik','D',2006,'Lens'),('Osman Hadzikic','P',1996,'Slaven'),
        ('Nikola Vasilj','P',1995,'St. Pauli'),('Martin Zlomislic','P',1998,'Rijeka'),
    ],
    'Brasile': [
        ('Vinicius Junior','A',2000,'Real Madrid'),('Raphinha','A',1996,'Barcellona'),
        ('Neymar','A',1992,'Santos'),('Endrick','A',2006,'Lione'),
        ('Gabriel Martinelli','A',2001,'Arsenal'),('Matheus Cunha','A',1999,'Manchester United'),
        ('Igor Thiago','A',2001,'Brentford'),('Luiz Henrique','A',2001,'Zenit'),
        ('Rayan','A',2006,'Bournemouth'),('Bruno Guimaraes','C',1997,'Newcastle'),
        ('Lucas Paqueta','C',1997,'Flamengo'),('Casemiro','C',1992,'Manchester United'),
        ('Fabinho','C',1993,'Al-Ittihad'),('Ederson Sousa','C',1999,'Atalanta'),
        ('Danilo Santos','C',2001,'Botafogo'),('Marquinhos','D',1994,'PSG'),
        ('Gabriel Magalhaes','D',1997,'Arsenal'),('Gleison Bremer','D',1997,'Juventus'),
        ('Leo Pereira','D',1996,'Flamengo'),('Roger Ibanez','D',1998,'Al-Ahli'),
        ('Alex Sandro','D',1991,'Flamengo'),('Danilo','D',1991,'Flamengo'),
        ('Douglas Santos','D',1994,'Zenit'),('Alisson','P',1992,'Liverpool'),
        ('Ederson','P',1993,'Fenerbahce'),('Weverton','P',1987,'Gremio'),
    ],
    'Canada': [
        ('Jonathan David','A',2000,'Juventus'),('Cyle Larin','A',1995,'Southampton'),
        ('Promise David','A',2001,'Union'),('Tani Oluwaseyi','A',2000,'Villarreal'),
        ('Stephen Eustaquio','C',1996,'LAFC'),('Tajon Buchanan','C',1999,'Villarreal'),
        ('Ismael Kone','C',2003,'Sassuolo'),('Mathieu Choiniere','C',1999,'LAFC'),
        ('Liam Millar','C',1996,'Hull'),('Jacob Shaffelburg','C',1999,'LAFC'),
        ('Jonathan Osorio','C',1992,'Toronto'),('Ali Ahmed','C',2000,'Norwich'),
        ('Nathan Saliba','C',2004,'Anderlecht'),('Marcelo Flores','C',2003,'Tigres'),
        ('Alphonso Davies','D',2000,'Bayern'),('Alistair Johnston','D',1998,'Celtic'),
        ('Moise Bombito','D',2000,'Nizza'),('Richie Laryea','D',1995,'Toronto'),
        ('Derek Cornelius','D',1997,'Glasgow Rangers'),('Joel Waterman','D',1996,'Chicago'),
        ('Alfie Jones','D',1997,'Middlesbrough'),('Niko Sigur','D',2003,'Hajduk'),
        ('Luc de Fougerolles','D',2005,'Dender'),('Dayne St. Clair','P',1997,'Inter Miami'),
        ('Maxime Crepeau','P',1994,'Orlando'),('Owen Goodman','P',2003,'Barnsley'),
    ],
    'Capo Verde': [
        ('Jovane Cabral','A',1998,'Estrela'),('Nuno da Costa','A',1991,'Basaksehir'),
        ('Dailon Livramento','A',2001,'Casa Pia'),('Garry Rodrigues','A',1990,'Apollon'),
        ('Willy Semedo','A',1994,'Omonia'),('Gilson Tavares','A',2001,'Akron'),
        ('Helio Varela','A',2002,'Maccabi Tel Aviv'),('Ryan Mendes','A',1990,'Igdir'),
        ('Jamiro Monteiro','C',1993,'Zwolle'),('Telmo Arcanjo','C',2001,'Guimaraes'),
        ('Deroy Duarte','C',1997,'Ludogorets'),('Laros Duarte','C',1997,'Puskas'),
        ('Kevin Pina','C',1997,'Krasnodar'),('Yannick Semedo','C',1995,'Farense'),
        ('Logan Costa','D',2001,'Villarreal'),('Steven Moreira','D',1994,'Columbus'),
        ('Roberto Lopes','D',1992,'Shamrock'),('Diney Borges','D',1995,'Al-Bataeh'),
        ('Sidny Lopes Cabral','D',2002,'Benfica'),('Joao Paulo','D',1998,'FCSB'),
        ('Wagner Pina','D',2002,'Trabzonspor'),('Kelvin Pires','D',2000,'SJK'),
        ('Stopira','D',1988,'Torreense'),('Vozinha','P',1986,'Chaves'),
        ('Marcio Rosa','P',1997,'Montana'),('Cj dos Santos','P',2000,'San Diego'),
    ],
    'Colombia': [
        ('Luis Diaz','A',1997,'Bayern'),('Cucho Hernandez','A',1999,'Betis'),
        ('Jhon Cordoba','A',1993,'Krasnodar'),('Luis Suarez','A',1997,'Sporting CP'),
        ('Andres Gomez','A',2002,'Vasco da Gama'),('James Rodriguez','C',1991,'Minnesota'),
        ('Jhon Arias','C',1997,'Palmeiras'),('Jefferson Lerma','C',1994,'Crystal Palace'),
        ('Richard Rios','C',2000,'Benfica'),('Jorge Carrascal','C',1998,'Flamengo'),
        ('Juan Fernando Quintero','C',1993,'River Plate'),('Kevin Castano','C',2000,'River Plate'),
        ('Jaminton Campaz','C',2000,'Rosario'),('Juan Portilla','C',1998,'Athletico'),
        ('Gustavo Puerta','C',2003,'Racing Santander'),('Davinson Sanchez','D',1996,'Galatasaray'),
        ('Daniel Munoz','D',1996,'Crystal Palace'),('Jhon Lucumi','D',1998,'Bologna'),
        ('Yerry Mina','D',1994,'Cagliari'),('Johan Mojica','D',1992,'Mallorca'),
        ('Santiago Arias','D',1992,'Independiente'),('Deiver Machado','D',1993,'Nantes'),
        ('Willer Ditta','D',1997,'Cruz Azul'),('David Ospina','P',1988,'Atletico Nacional'),
        ('Camilo Vargas','P',1989,'Atlas'),('Alvaro Montero','P',1995,'Velez'),
    ],
    'Corea del Sud': [
        ('Son Heung-min','A',1992,'LAFC'),('Cho Gue-sung','A',1998,'Midtjylland'),
        ('Oh Hyeon-gyu','A',2001,'Besiktas'),('Lee Kang-in','C',2001,'PSG'),
        ('Hwang Hee-chan','C',1996,'Wolverhampton'),('Hwang In-beom','C',1996,'Feyenoord'),
        ('Bae Jun-ho','C',2003,'Stoke'),('Eom Ji-sung','C',2002,'Swansea'),
        ('Lee Dong-gyeong','C',1997,'Ulsan'),('Lee Jae-sung','C',1992,'Magonza'),
        ('Paik Seung-ho','C',1997,'Birmingham'),('Yang Hyun-jun','C',2002,'Celtic'),
        ('Kim Jin-gyu','C',1997,'Jeonbuk'),('Kim Min-jae','D',1996,'Bayern'),
        ('Jens Castrop','D',2003,"M'Gladbach"),('Cho Yu-min','D',1996,'Sharjah'),
        ('Kim Moon-hwan','D',1995,'Daejeon'),('Lee Han-beom','D',2002,'Midtjylland'),
        ('Lee Ki-hyuk','D',2000,'Gangwon'),('Lee Tae-seok','D',2002,'Austria Vienna'),
        ('Seol Young-woo','D',1998,'Stella Rossa'),('Kim Tae-hyeon','D',2000,'Kashima'),
        ('Park Jin-seob','D',1995,'ZJ'),('Jo Hyeon-woo','P',1991,'Ulsan'),
        ('Kim Seung-gyu','P',1990,'FC Tokyo'),('Song Bum-keun','P',1997,'Jeonbuk'),
    ],
    "Costa d'Avorio": [
        ('Simon Adingra','A',2002,'Monaco'),('Nicolas Pepe','A',1995,'Villarreal'),
        ('Elye Wahi','A',2003,'Nizza'),('Ange-Yoan Bonny','A',2003,'Inter'),
        ('Amad Diallo','A',2002,'Manchester United'),('Oumar Diakite','A',2003,'Cercle'),
        ('Evann Guessand','A',2001,'Crystal Palace'),('Yan Diomande','A',2006,'Lipsia'),
        ('Bazoumana Toure','A',2006,'Hoffenheim'),('Franck Kessie','C',1996,'Al-Ahli'),
        ('Seko Fofana','C',1995,'FC Porto'),('Ibrahim Sangare','C',1997,'Nottingham'),
        ('Jean Michael Seri','C',1991,'Maribor'),('Parfait Guiagon','C',2001,'Charleroi'),
        ('Christ Inao Oulai','C',2006,'Trabzonspor'),('Ousmane Diomande','D',2003,'Sporting'),
        ('Odilon Kossounou','D',2001,'Atalanta'),('Evan Ndicka','D',1999,'Roma'),
        ('Emmanuel Agbadou','D',1997,'Besiktas'),('Wilfried Singo','D',2000,'Galatasaray'),
        ('Guela Doue','D',2002,'Strasburgo'),('Ghislain Konan','D',1995,'Gil Vicente'),
        ('Christopher Operi','D',1997,'Istanbul'),('Yahia Fofana','P',2000,'Rizespor'),
        ('Alban Lafont','P',1999,'Panathinaikos'),('Mohamed Kone','P',2002,'Charleroi'),
    ],
    'Croazia': [
        ('Andrej Kramaric','A',1991,'Hoffenheim'),('Ivan Perisic','A',1989,'PSV'),
        ('Ante Budimir','A',1991,'Osasuna'),('Petar Musa','A',1998,'Dallas'),
        ('Igor Matanovic','A',2003,'Friburgo'),('Marco Pasalic','A',2000,'Orlando'),
        ('Luka Modric','C',1985,'Milan'),('Mateo Kovacic','C',1994,'Manchester City'),
        ('Mario Pasalic','C',1995,'Atalanta'),('Nikola Vlasic','C',1997,'Torino'),
        ('Nikola Moro','C',1998,'Bologna'),('Martin Baturina','C',2003,'Como'),
        ('Luka Sucic','C',2002,'Real Sociedad'),('Petar Sucic','C',2003,'Inter'),
        ('Toni Fruk','C',2001,'Rijeka'),('Kristijan Jakic','C',1997,'Augusta'),
        ('Josko Gvardiol','D',2002,'Manchester City'),('Duje Caleta-Car','D',1996,'Real Sociedad'),
        ('Marin Pongracio','D',1997,'Fiorentina'),('Josip Stanisic','D',2000,'Bayern'),
        ('Josip Sutalo','D',2000,'Ajax'),('Martin Erlic','D',1998,'Midtjylland'),
        ('Luka Vuskovic','D',2007,'Amburgo'),('Dominik Livakovic','P',1995,'Dinamo Zagabria'),
        ('Dominik Kotarski','P',2000,'Copenhagen'),('Ivor Pandur','P',2000,'Hull'),
    ],
    'Curacao': [
        ('Tahith Chong','A',1999,'Sheffield'),('Sontje Hansen','A',2002,'Middlesbrough'),
        ('Kenji Gorre','A',1994,'Haifa'),('Jurgen Locadia','A',1993,'Miami'),
        ('Gervane Kastaneer','A',1996,'Terengganu'),('Brandley Kuwas','A',1992,'Volendam'),
        ('Jearl Margaritha','A',2000,'Beveren'),('Jeremy Antonisse','A',2002,'Kifisia'),
        ('Juninho Bacuna','C',1997,'Volendam'),('Leandro Bacuna','C',1991,'Igdir'),
        ('Kevin Felida','C',1999,'Den Bosch'),('Tyrese Noslin','C',2002,'Telstar'),
        ('Godfried Roemeratoe','C',1999,'Waalwijk'),("Ar'Jany Martha",'C',2003,'Rotherham'),
        ('Livano Comenencia','C',2004,'Zurigo'),('Riechedly Bazoer','D',1996,'Konyaspor'),
        ('Joshua Brenet','D',1994,'Kayserispor'),('Armando Obispo','D',1999,'PSV'),
        ('Sherel Floranus','D',1998,'Zwolle'),('Roshon Van Eijma','D',1998,'Waalwijk'),
        ('Shurandy Sambo','D',2001,'Sparta Rotterdam'),('Jurien Gaari','D',1993,'Abha'),
        ('Deveron Fonville','D',2003,'Nijmegen'),('Eloy Room','P',1989,'Miami'),
        ('Tyrick Bodak','P',2002,'Telstar'),('Trevor Doornbusch','P',1999,'Venlo'),
    ],
    'Ecuador': [
        ('Enner Valencia','A',1989,'Pachuca'),('Gonzalo Plata','A',2000,'Flamengo'),
        ('Jordy Caicedo','A',1997,'Huracan'),('Kevin Rodriguez','A',2000,'Union SG'),
        ('Nilson Angulo','A',2003,'Sunderland'),('Alan Minda','A',2003,'Atletico Mineiro'),
        ('Anthony Valencia','A',2003,'Anversa'),('Jeremy Arevalo','A',2005,'Stoccarda'),
        ('John Yeboah','A',2000,'Venezia'),('Moises Caicedo','C',2001,'Chelsea'),
        ('Jordy Alcivar','C',1999,'Independiente'),('Alan Franco','C',1998,'Atletico Mineiro'),
        ('Pedro Vite','C',2002,'UNAM'),('Denil Castillo','C',2004,'Midtjylland'),
        ('Kendry Paez','C',2007,'River Plate'),('Pervis Estupinan','D',1998,'Milan'),
        ('Piero Hincapie','D',2002,'Arsenal'),('Willian Pacho','D',2001,'PSG'),
        ('Felix Torres','D',1997,'Internacional'),('Angelo Preciado','D',1998,'Atletico Mineiro'),
        ('Jackson Porozo','D',2000,'Tijuana'),('Joel Ordonez','D',2004,'Bruges'),
        ('Yaimar Medina','D',2004,'Genk'),('Hernan Galindez','P',1987,'Huracan'),
        ('Moises Ramirez','P',2000,'Kifisia'),('Gonzalo Valle','P',1996,'LDU'),
    ],
    'Egitto': [
        ('Mohamed Salah','A',1992,'Liverpool'),('Omar Marmoush','A',1999,'Manchester City'),
        ('Mahmoud Hassan','A',1994,'Al Ahly'),('Ibrahim Adel','A',2001,'Nordsjaelland'),
        ('Haitham Hassan','A',2002,'Oviedo'),('Hamza Abdelkarim','A',2008,'Barcellona B'),
        ('Mostafa Mohamed','C',1997,'Pyramids'),('Ahmed Sayed','C',1996,'Al Ahly'),
        ('Emam Ashour','C',1998,'Al Ahly'),('Marwan Attia','C',1998,'Al Ahly'),
        ('Hamdi Fathi','C',1994,'Al-Wakrah'),('Muhannad Lashin','C',1996,'Pyramids'),
        ('Nabil Dunga','C',1996,'Al-Najma'),('Mahmoud Saber','C',2001,'Zed'),
        ('Mohamed Hany','D',1996,'Al Ahly'),('Yasser Ibrahim','D',1993,'Al Ahly'),
        ('Mohamed Abdelmonem','D',1999,'Nizza'),('Karim Hafez','D',1996,'Pyramids'),
        ('Rami Rabia','D',1993,'Al-Ain'),('Ahmed Fatouh','D',1998,'Zamalek'),
        ('Hossam Abdel Majid','D',2001,'Zamalek'),('Tarek Alaa','D',2002,'Zed'),
        ('Mohamed El Shenawy','P',1988,'Al Ahly'),('Mohamed Alaa','P',1999,'El Gouna'),
        ('Mostafa Shobeir','P',2000,'Al Ahly'),('El Mahdy Soliman','P',1987,'Zamalek'),
    ],
    'Francia': [
        ('Kylian Mbappe','A',1998,'Real Madrid'),('Marcus Thuram','A',1997,'Inter'),
        ('Ousmane Dembele','A',1997,'PSG'),('Bradley Barcola','A',2002,'PSG'),
        ('Jean-Philippe Mateta','A',1997,'Crystal Palace'),('Michael Olise','A',2001,'Bayern'),
        ('Maghnes Akliouche','A',2002,'Monaco'),('Rayan Cherki','A',2003,'Manchester City'),
        ('Desire Doue','A',2005,'PSG'),('Aurelien Tchouameni','C',2000,'Real Madrid'),
        ('Warren Zaire-Emery','C',2006,'PSG'),("N'Golo Kante",'C',1991,'Fenerbahce'),
        ('Adrien Rabiot','C',1995,'Milan'),('Manu Kone','C',2001,'Roma'),
        ('William Saliba','D',2001,'Arsenal'),('Jules Kounde','D',1998,'Barcellona'),
        ('Ibrahima Konate','D',1999,'Liverpool'),('Theo Hernandez','D',1997,'Al-Hilal'),
        ('Dayot Upamecano','D',1998,'Bayern'),('Lucas Hernandez','D',1996,'PSG'),
        ('Malo Gusto','D',2003,'Chelsea'),('Lucas Digne','D',1993,'Aston Villa'),
        ('Maxence Lacroix','D',2000,'Crystal Palace'),('Mike Maignan','P',1995,'Milan'),
        ('Brice Samba','P',1994,'Rennes'),('Robin Risser','P',2004,'Lens'),
    ],
    'Germania': [
        ('Florian Wirtz','A',2003,'Liverpool'),('Jamal Musiala','A',2003,'Bayern'),
        ('Kai Havertz','A',1999,'Arsenal'),('Leroy Sane','A',1996,'Galatasaray'),
        ('Maximilian Beier','A',2002,'Dortmund'),('Jamie Leweling','A',2001,'Stoccarda'),
        ('Deniz Undav','A',1996,'Stoccarda'),('Nick Woltemade','A',2002,'Newcastle'),
        ('Joshua Kimmich','C',1995,'Bayern'),('Leon Goretzka','C',1995,'Bayern'),
        ('Aleksandar Pavlovic','C',2004,'Bayern'),('Felix Nmecha','C',2000,'Bayern'),
        ('Angelo Stiller','C',2001,'Stoccarda'),('Pascal Gross','C',1991,'Brighton'),
        ('Nadiem Amiri','C',1996,'Mainz'),('Assan Ouedraogo','C',2006,'Lipsia'),
        ('Antonio Rudiger','D',1993,'Real Madrid'),('Jonathan Tah','D',1996,'Bayern'),
        ('Nico Schlotterbeck','D',1999,'Dortmund'),('David Raum','D',1998,'Lipsia'),
        ('Waldemar Anton','D',1996,'Dortmund'),('Malick Thiaw','D',2001,'Newcastle'),
        ('Nathaniel Brown','D',2003,'Francoforte'),('Manuel Neuer','P',1986,'Bayern'),
        ('Oliver Baumann','P',1990,'Hoffenheim'),('Alexander Nubel','P',1996,'Stoccarda'),
    ],
    'Ghana': [
        ('Inaki Williams','A',1994,'Athletic'),('Jordan Ayew','A',1991,'Leicester'),
        ('Antoine Semenyo','A',2000,'Manchester City'),('Kamaldeen Sulemana','A',2002,'Atalanta'),
        ('Abdul Fatawu','A',2004,'Leicester'),('Ernest Nuamah','A',2003,'Lione'),
        ('Christopher Bonsu Baah','A',2004,'Al-Qadsiah'),('Prince Adu','A',2003,'Plzen'),
        ('Brandon Thomas-Asante','A',1998,'Coventry'),('Thomas Partey','C',1993,'Villarreal'),
        ('Elisha Owusu','C',1997,'Auxerre'),('Augustine Boakye','C',2000,'Saint-Etienne'),
        ('Kwasi Sibo','C',1998,'Oviedo'),('Caleb Yirenkyi','C',2006,'Nordsjaelland'),
        ('Abdul Rahman Baba','D',1994,'PAOK'),('Alidu Seidu','D',2000,'Rennes'),
        ('Gideon Mensah','D',1998,'Auxerre'),('Abdul Mumin','D',1998,'Rayo'),
        ('Jerome Opoku','D',1998,'Basaksehir'),('Marvin Senaya','D',2001,'Auxerre'),
        ('Jonas Adjetey','D',2003,'Wolfsburg'),('Derrick Luckassen','D',1995,'Pafos'),
        ('Kojo Peprah Oppong','D',2004,'Nizza'),('Lawrence Ati Zigi','P',1996,'FC San Gallo'),
        ('Joseph Anang','P',2000,"St. Patrick's"),('Benjamin Asare','P',1992,'Hearts of Oak'),
    ],
    'Giappone': [
        ('Takefusa Kubo','C',2001,'Real Sociedad'),('Daizen Maeda','A',1997,'Celtic'),
        ('Ayase Ueda','A',1998,'Feyenoord'),('Koki Ogawa','A',1997,'Nijmegen'),
        ('Yuito Suzuki','A',2001,'Friburgo'),('Keisuke Goto','A',2005,'Sint-Truiden'),
        ('Kento Shiogai','A',2005,'Wolfsburg'),('Ritsu Doan','C',1998,'Francoforte'),
        ('Wataru Endo','C',1993,'Liverpool'),('Daichi Kamada','C',1996,'Crystal Palace'),
        ('Ao Tanaka','C',1998,'Leeds'),('Junya Ito','C',1993,'Genk'),
        ('Keito Nakamura','C',2000,'Reims'),('Kaishu Sano','C',2000,'Magonza'),
        ('Takehiro Tomiyasu','D',1998,'Ajax'),('Hiroki Ito','D',1999,'Bayern'),
        ('Ko Itakura','D',1997,'Ajax'),('Yukinari Sugawara','D',2000,'Brema'),
        ('Tsuyoshi Watanabe','D',1997,'Feyenoord'),('Shogo Taniguchi','D',1991,'Sint-Truiden'),
        ('Ayumu Seko','D',2000,'Le Havre'),('Junnosuke Suzuki','D',2003,'Copenhagen'),
        ('Yuto Nagatomo','D',1986,'FC Tokyo'),('Zion Suzuki','P',2002,'Parma'),
        ('Tomoki Hayakawa','P',1999,'Kashima'),('Keisuke Osako','P',1999,'Hiroshima'),
    ],
    'Giordania': [
        ('Musa Al-Taamari','A',1997,'Rennes'),('Ali Azaizeh','A',2004,'Al-Shabab'),
        ('Mahmoud Al-Mardi','A',1993,'Al-Hussein'),('Odeh Fakhoury','A',2005,'Pyramids'),
        ('Ali Olwan','A',2000,'Al-Sailiya'),('Ibrahim Sabra','A',2006,'NK Lokomotiva'),
        ('Nizar Al-Rashdan','C',1999,'Qatar'),('Noor Al-Rawabdeh','C',1997,'Selangor'),
        ('Amer Jamous','C',2002,'Al Zawraa'),('Ibrahim Saadeh','C',2000,'Al Karma'),
        ('Rajaei Ayed','C',1993,'Al-Hussein'),('Mohammad Al-Dawoud','C',1992,'Al-Wehdat'),
        ('Mohammad Abualnadi','D',2001,'Selangor'),('Husam Abu Dahab','D',2000,'Al Faisaly'),
        ('Yazan Al-Arab','D',1996,'FC Seul'),('Saed Al-Rosan','D',1997,'Al-Hussein'),
        ('Anas Badawi','D',1997,'Al Faisaly'),('Ehsan Haddad','D',1994,'Al-Hussein'),
        ('Abdallah Nasib','D',1994,'Al Zawraa'),('Saleem Obaid','D',1992,'Al-Hussein'),
        ('Mohammad Abu Hasheesh','D',1995,'Al Karma'),('Yazeed Abulaila','P',1993,'Al-Hussein'),
        ('Abdallah Al-Fakhouri','P',2000,'Al-Wehdat'),('Noureddin Bani Attiah','P',1993,'Al Faisaly'),
    ],
    'Haiti': [
        ('Wilson Isidor','A',2000,'Sunderland'),('Duckens Nazon','A',1994,'Esteghlal'),
        ('Derrick Etienne Jr.','A',1996,'Toronto'),('Frantzdy Pierrot','A',1995,'Rizespor'),
        ('Josue Casimir','A',2001,'Auxerre'),('Lenny Joseph','A',2000,'Ferencvaros'),
        ('Yassin Fortune','A',1999,'Vizela'),('Louicius Deedson','A',2001,'FC Dallas'),
        ('Ruben Providence','A',2001,'Almere'),('Jean-Ricner Bellegarde','C',1998,'Wolverhampton'),
        ('Danley Jean Jacques','C',2000,'Philadelphia'),('Leverton Pierre','C',1998,'Vizela'),
        ('Carl Sainte','C',2002,'El Paso'),('Dominique Simon','C',2000,'Tatran'),
        ('Woodensky Pierre','C',2004,'Violette'),('Jean-Kevin Duverne','D',1997,'Gent'),
        ('Hannes Delcroix','D',1999,'Lugano'),('Carlens Arcus','D',1996,'Angers'),
        ('Martin Experience','D',1999,'Nancy'),('Duke Lacroix','D',1993,'Switchbacks'),
        ('Ricardo Ade','D',1990,'LDU Quito'),('Wilguens Paugain','D',2001,'Zulte Waregem'),
        ('Keeto Thermoncy','D',2006,'Young Boys'),('Johny Placide','P',1988,'SC Bastia'),
        ('Josue Duverger','P',2000,'Cosmos Coblenza'),('Alexandre Pierre','P',2001,'Sochaux'),
    ],
    'Inghilterra': [
        ('Harry Kane','A',1993,'Bayern'),('Bukayo Saka','A',2001,'Arsenal'),
        ('Marcus Rashford','A',1997,'Barcellona'),('Ollie Watkins','A',1995,'Aston Villa'),
        ('Ivan Toney','A',1996,'Al-Ahli'),('Anthony Gordon','A',2001,'Newcastle'),
        ('Noni Madueke','A',2002,'Arsenal'),('Jude Bellingham','C',2003,'Real Madrid'),
        ('Declan Rice','C',1999,'Arsenal'),('Kobbie Mainoo','C',2005,'Manchester United'),
        ('Eberechi Eze','C',1998,'Arsenal'),('Elliot Anderson','C',2002,'Nottingham'),
        ('Morgan Rogers','C',2002,'Aston Villa'),('Jordan Henderson','C',1990,'Brentford'),
        ('John Stones','D',1994,'Manchester City'),('Marc Guehi','D',2000,'Manchester City'),
        ('Reece James','D',1999,'Chelsea'),('Ezri Konsa','D',1997,'Aston Villa'),
        ('Dan Burn','D',1992,'Newcastle'),('Tino Livramento','D',2002,'Newcastle'),
        ('Djed Spence','D',2000,'Tottenham'),('Jarell Quansah','D',2003,'Leverkusen'),
        ("Nico O'Reilly",'D',2005,'Manchester City'),('Jordan Pickford','P',1994,'Everton'),
        ('Dean Henderson','P',1997,'Crystal Palace'),('James Trafford','P',2002,'Manchester City'),
    ],
    'Iran': [
        ('Mehdi Taremi','A',1992,'Olympiacos'),('Ali Alipour','A',1995,'Persepolis'),
        ('Mehdi Ghayedi','A',1998,'Al-Nasr'),('Amirhossein Hosseinzadeh','A',2000,'Tractor'),
        ('Shahriar Moghanlou','A',1994,'Kalba'),('Dennis Dargahi','A',1997,'Standard'),
        ('Mohammad Mohebi','A',1998,'FC Rostov'),('Alireza Jahanbakhsh','C',1993,'Dender'),
        ('Saman Ghoddos','C',1993,'Kalba'),('Saeed Ezatolahi','C',1996,'Shabab'),
        ('Roozbeh Cheshmi','C',1993,'Esteghlal'),('Mehdi Torabi','C',1994,'Tractor'),
        ('Mohammad Ghorbani','C',2001,'Al-Wahda'),('Amirmohammad Razzaghinia','C',2006,'Esteghlal'),
        ('Ehsan Hajsafi','D',1990,'Sepahan'),('Milad Mohammadi','D',1993,'Persepolis'),
        ('Hossein Kanaani','D',1994,'Persepolis'),('Ali Nemati','D',1996,'Foolad'),
        ('Saleh Hardani','D',1998,'Esteghlal'),('Ramin Rezaeian','D',1990,'Foolad'),
        ('Shoja Khalilzadeh','D',1989,'Tractor'),('Arya Yousefi','D',2002,'Sepahan'),
        ('Danial Iri','D',2003,'Malavan'),('Alireza Beiranvand','P',1992,'Tractor'),
        ('Seyed Hossein Hosseini','P',1992,'Sepahan'),('Payam Niazmand','P',1995,'Persepolis'),
    ],
    'Iraq': [
        ('Aymen Hussein','A',1996,'Al-Karma'),('Mohanad Ali','A',2000,'Dibba'),
        ('Ali Jasim','A',2004,'Al-Najma'),('Marko Farji','A',2004,'Venezia'),
        ('Youssef Amyn','A',2003,'AEK'),('Ali Al-Hamad','A',2002,'Luton'),
        ('Ahmed Qasem','A',2003,'Nashville'),('Ali Yousif','A',1996,'Al-Talaba'),
        ('Zidane Iqbal','C',2003,'FC Utrecht'),('Amir Al-Ammari','C',1997,'KS Cracovia'),
        ('Ibrahim Bayesh','C',2000,'Al Dhafra'),('Zaid Ismail','C',2002,'Al Talaba'),
        ('Aimar Sher','C',2002,'Sarpsborg'),('Kevin Yakob','C',2000,'Aarhus'),
        ('Akam Hashim','D',1998,'Al-Zawraa'),('Mustafa Saadoon','D',2001,'Al Shorta'),
        ('Frans Putros','D',1993,'Persib'),('Merchas Doski','D',1999,'Plzen'),
        ('Rebin Sulaka','D',1992,'Port'),('Zaid Tahseen','D',2001,'Pakhtakor'),
        ('Ahmed Yahya','D',1995,'Al Shorta'),('Hussein Ali','D',2002,'Pogon'),
        ('Manaf Younis','D',1996,'Al Shorta'),('Jalal Hassan','P',1991,'Al-Zawraa'),
        ('Ahmed Basil','P',1996,'Al-Shorta'),('Fahad Talib','P',1994,'Al-Talaba'),
    ],
    'Marocco': [
        ('Achraf Hakimi','D',1998,'PSG'),('Brahim Diaz','A',1999,'Real Madrid'),
        ('Ayoub El Kaabi','A',1993,'Olympiacos'),('Abde Eazzalzouli','A',2001,'Betis'),
        ('Soufiane Rahmi','A',1996,'Al Ain'),('Chemsdine Talbi','A',2005,'Sunderland'),
        ('Gessime Yassine','A',2005,'Strasburgo'),('Ayoube Amaimouni','A',2004,'Francoforte'),
        ('Sofyan Amrabat','C',1996,'Betis'),('Azzedine Ounahi','C',2000,'Girona'),
        ('Bilal El Khannouss','C',2004,'Stoccarda'),('Ismael Saibari','C',2001,'PSV'),
        ('Neil El Aynaoui','C',2001,'Roma'),('Samir El Mourabet','C',2006,'Strasburgo'),
        ('Ayyoub Buaddi','C',2007,'Lilla'),('Nayef Aguerd','D',1996,'Marsiglia'),
        ('Noussair Mazraoui','D',1997,'Manchester United'),('Issa Diop','D',1997,'Fulham'),
        ('Anas Sah-Eddine','D',2002,'PSV'),('Chadi Riad','D',2003,'Crystal Palace'),
        ('Zakaria El Ouahdi','D',2001,'Genk'),('Redouane Halhal','D',2003,'Mechelen'),
        ('Youssef Belammari','D',1998,'Al Ahly'),('Yassine Bounou','P',1991,'Al-Hilal'),
        ('Ahmed Reda Tagnaouti','P',1996,'FAR'),('Munir Mohamedi','P',1989,'RS Berkane'),
    ],
    'Messico': [
        ('Santiago Gimenez','A',2001,'Milan'),('Raul Jimenez','A',1995,'Fulham'),
        ('Roberto Alvarado','A',1998,'Chivas'),('Julian Quinones','A',1997,'Al-Qadsiah'),
        ('Guillermo Martinez','A',1995,'UNAM'),('Alexis Vega','A',1997,'Toluca'),
        ('Armando Gonzalez','A',2003,'Chivas'),('Edson Alvarez','C',1997,'Fenerbahce'),
        ('Luis Chavez','C',1996,'Dinamo'),('Alvaro Fidalgo','C',1997,'Betis'),
        ('Orbellin Pineda','C',1996,'AEK'),('Luis Romo','C',1995,'Chivas'),
        ('Obed Vargas','C',2000,'Atletico'),('Cesar Huerta','C',2000,'Anderlecht'),
        ('Erik Lira','C',2000,'Cruz Azul'),('Brian Gutierrez','C',2003,'Chivas'),
        ('Gilberto Mora','C',2008,'Tijuana'),('Cesar Montes','D',1997,'Lokomotiv'),
        ('Johan Vasquez','D',1998,'Genoa'),('Jesus Gallardo','D',1994,'Toluca'),
        ('Israel Reyes','D',2000,'America'),('Jorge Sanchez','D',1997,'PAOK'),
        ('Mateo Chavez','D',2004,'AZ'),('Guillermo Ochoa','P',1985,'AEL'),
        ('Carlos Acevedo','P',1996,'Santos'),('Raul Rangel','P',2000,'Chivas'),
    ],
    'Norvegia': [
        ('Erling Braut Haaland','A',2000,'Manchester City'),('Alexander Sorloth','A',1995,'Atletico'),
        ('Jorgen Strand Larsen','A',2000,'Crystal Palace'),('Oscar Bobb','A',2003,'Fulham'),
        ('Jens Petter Hauge','A',1999,'Bodo/Glimt'),('Antonio Nusa','A',2005,'Lipsia'),
        ('Andreas Schjelderup','A',2004,'Benfica'),('Martin Odegaard','C',1998,'Arsenal'),
        ('Sander Berge','C',1998,'Fulham'),('Fredrik Aursnes','C',1995,'Benfica'),
        ('Kristian Thorstvedt','C',1999,'Sassuolo'),('Patrick Berg','C',1997,'Bodo/Glimt'),
        ('Morten Thorsby','C',1996,'Cremonese'),('Thelo Aasgaard','C',2002,'Glasgow Rangers'),
        ('Kristoffer Ajer','D',1998,'Brentford'),('Leo Ostigard','D',1999,'Genoa'),
        ('Julian Ryerson','D',1997,'Dortmund'),('Marcus Pedersen','D',2000,'Torino'),
        ('Fredrik Bjorkan','D',1998,'Bodo/Glimt'),('Torbjorn Heggem','D',1999,'Bologna'),
        ('Sondre Langas','D',2001,'Derby'),('David Moller Wolfe','D',2002,'Wolverhampton'),
        ('Henrik Falchener','D',2003,'Viking'),('Orjan Nyland','P',1990,'Siviglia'),
        ('Egil Selvik','P',1997,'Watford'),('Sander Tangvik','P',2002,'Amburgo'),
    ],
    'Nuova Zelanda': [
        ('Chris Wood','A',1991,'Nottingham'),('Kosta Barbarouses','A',1990,'Western Sydney'),
        ('Ben Waine','A',2001,'Port Vale'),('Jesse Randall','A',2002,'Auckland'),
        ('Marko Stamenic','C',2002,'Swansea'),('Alex Rufer','C',1996,'Wellington'),
        ('Joe Bell','C',1999,'Viking'),('Callum McCowatt','C',1999,'Silkeborg'),
        ('Ben Old','C',2002,'Saint-Etienne'),('Matthew Garbett','C',2002,'Peterborough'),
        ('Elijah Just','C',2000,'Motherwell'),('Sarpreet Singh','C',1999,'Wellington'),
        ('Ryan Thomas','C',1994,'PEC Zwolle'),('Lachlan Bayliss','C',2002,'Newcastle'),
        ('Michael Boxall','D',1988,'Minnesota'),('Tommy Smith','D',1990,'Braintree'),
        ('Liberato Cacace','D',2000,'Wrexham'),('Nando Pijnaker','D',1999,'Auckland'),
        ('Tim Payne','D',1994,'Wellington'),('Francis de Vries','D',1994,'Auckland'),
        ('Callan Elliot','D',1999,'Auckland'),('Tyler Bindon','D',2005,'Sheffield United'),
        ('Finn Surman','D',2003,'Portland'),('Max Crocombe','P',1993,'Millwall'),
        ('Michael Woud','P',1999,'Auckland'),('Alex Paulsen','P',2002,'Danzica'),
    ],
    'Olanda': [
        ('Cody Gakpo','A',1999,'Liverpool'),('Donyell Malen','A',1999,'Roma'),
        ('Memphis Depay','A',1994,'Corinthians'),('Bryan Brobbey','A',2002,'Sunderland'),
        ('Justin Kluivert','A',1999,'Bournemouth'),('Noa Lang','A',1999,'Galatasaray'),
        ('Wout Weghorst','A',1992,'Ajax'),('Frenkie de Jong','C',1997,'Barcellona'),
        ('Tijjani Reijnders','C',1998,'Manchester City'),('Teun Koopmeiners','C',1998,'Juventus'),
        ('Ryan Gravenberch','C',2002,'Liverpool'),('Mats Wieffer','C',1999,'Brighton'),
        ('Quinten Timber','C',2001,'Marsiglia'),('Guus Til','C',1997,'PSV'),
        ('Crysencio Summerville','C',2001,'West Ham'),('Marten de Roon','C',1991,'Atalanta'),
        ('Virgil van Dijk','D',1991,'Liverpool'),('Nathan Ake','D',1995,'Manchester City'),
        ('Denzel Dumfries','D',1996,'Inter'),('Micky van de Ven','D',2001,'Tottenham'),
        ('Jean Paul van Hecke','D',2000,'Brighton'),('Jorrel Hato','D',2006,'Chelsea'),
        ('Lutsharel Geertruida','D',2000,'Sunderland'),('Bart Verbruggen','P',2002,'Brighton'),
        ('Mark Flekken','P',1993,'Leverkusen'),('Robin Roefs','P',2003,'Sunderland'),
    ],
    'Panama': [
        ('Jose Fajardo','A',1993,'Universidad Catolica'),('Ismael Diaz','A',1997,'Leon'),
        ('Cecilio Waterman','A',1991,'Universidad Concepcion'),('Tomas Rodriguez','A',1999,'Saprissa'),
        ('Adalberto Carrasquilla','C',1998,'UNAM'),('Anibal Godoy','C',1990,'San Diego'),
        ('Alberto Quintero','C',1987,'Plaza'),('Yoel Barcenas','C',1993,'Mazatlan'),
        ('Carlos Harvey','C',2000,'Minnesota'),('Jose Luis Rodriguez','C',1998,'Juarez'),
        ('Cristian Martinez','C',1997,'Ironi'),('Cesar Yanis','C',1996,'Cobresal'),
        ('Azarias Londono','C',2001,'Universidad Catolica'),('Michael Amir Murillo','D',1996,'Besiktas'),
        ('Eric Davis','D',1991,'Plaza'),('Fidel Escobar','D',1995,'Saprissa'),
        ('Andres Andrade','D',1998,'LASK'),('Cesar Blackman','D',1998,'Bratislava'),
        ('Jose Cordoba','D',2001,'Norwich'),('Roderick Miller','D',1992,'Turan'),
        ('Jiovany Ramos','D',1997,'Puerto Cabello'),('Edgardo Farina','D',2001,'Pari Nizhny'),
        ('Jorge Gutierrez','D',1998,'La Guaira'),('Luis Mejia','P',1991,'Montevideo'),
        ('Orlando Mosquera','P',1994,'Al-Fayha'),('Cesar Samudio','P',1994,'Marathon'),
    ],
    'Paraguay': [
        ('Miguel Almiron','A',1994,'Atlanta'),('Antonio Sanabria','A',1996,'Cremonese'),
        ('Julio Enciso','A',2004,'Strasburgo'),('Ramon Sosa','A',1999,'Palmeiras'),
        ('Alex Arce','A',1995,'Independiente'),('Gabriel Avalos','A',1990,'Independiente'),
        ('Gustavo Caballero','A',2001,'Portsmouth'),('Isidro Pitta','A',1999,'RB Bragantino'),
        ('Diego Gomez','C',2003,'Brighton'),('Andres Cubas','C',1996,'Vancouver'),
        ('Matias Galarza','C',2002,'Atlanta'),('Damian Bobadilla','C',2001,'San Paolo'),
        ('Braian Ojeda','C',2000,'Orlando'),('Alejandro Gamarra','C',1995,'Al-Ain'),
        ('Mauricio Magalhaes','C',2001,'Palmeiras'),('Gustavo Gomez','D',1993,'Palmeiras'),
        ('Omar Alderete','D',1996,'Sunderland'),('Junior Alonso','D',1993,'Atletico Mineiro'),
        ('Fabian Balbuena','D',1991,'Gremio'),('Jose Canale','D',1996,'Lanus'),
        ('Juan Jose Caceres','D',2000,'Dinamo'),('Gustavo Velazquez','D',1991,'Cerro Porteno'),
        ('Alexandro Maidana','D',2005,'Talleres'),('Roberto Junior Fernandez','P',1988,'Cerro Porteno'),
        ('Gaston Olveira','P',1993,'Olimpia'),('Orlando Gill','P',2000,'San Lorenzo'),
    ],
    'Portogallo': [
        ('Cristiano Ronaldo','A',1985,'Al-Nassr'),('Rafael Leao','A',1999,'Milan'),
        ('Goncalo Ramos','A',2001,'PSG'),('Pedro Neto','A',2000,'Chelsea'),
        ('Joao Felix','A',1999,'Al-Nassr'),('Francisco Conceicao','A',2002,'Juventus'),
        ('Goncalo Guedes','A',1999,'Real Sociedad'),('Francisco Trincao','A',1999,'Sporting'),
        ('Bruno Fernandes','C',1994,'Manchester United'),('Bernardo Silva','C',1994,'Manchester City'),
        ('Vitinha','C',2000,'PSG'),('Ruben Neves','C',1997,'Al-Hilal'),
        ('Joao Neves','C',2004,'PSG'),('Samuel Costa','C',2000,'RCD Maiorca'),
        ('Ruben Dias','D',1997,'Manchester City'),('Nuno Mendes','D',2002,'PSG'),
        ('Joao Cancelo','D',1994,'Barcellona'),('Diogo Dalot','D',1999,'Manchester United'),
        ('Goncalo Inacio','D',2001,'Sporting'),('Matheus Nunes','D',1998,'Manchester City'),
        ('Nelson Semedo','D',1993,'Fenerbahce'),('Renato Veiga','D',2003,'Villarreal'),
        ('Tomas Araujo','D',2002,'Benfica'),('Diogo Costa','P',1999,'FC Porto'),
        ('Jose Sa','P',1993,'Wolverhampton'),('Rui Silva','P',1994,'Sporting'),
    ],
    'Qatar': [
        ('Akram Afif','A',1996,'Al-Sadd'),('Al Moez Ali','A',1996,'Al-Duhail'),
        ('Yusuf Abdurisag','A',1999,'Al-Wakrah'),('Edmilson Junior','A',1994,'Al-Duhail'),
        ('Mohammed Muntari','A',1993,'Al-Gharafa'),('Ahmed Alaaeldin','A',1993,'Al-Rayyan'),
        ('Hasan Al-Haydos','A',1990,'Al-Sadd'),('Ahmed Al-Janehi','A',2000,'Al-Gharafa'),
        ('Tahsin Mohammed','A',2006,'Al-Duhail'),('Assim Madibo','C',1996,'Al-Wakrah'),
        ('Karim Boudiaf','C',1990,'Al-Duhail'),('Ahmed Fathi','C',1993,'Al-Arabi'),
        ('Abdulaziz Hatim','C',1990,'Al-Rayyan'),('Jassem Gaber','C',2002,'Al-Rayyan'),
        ('Mohamed Al-Mannai','C',2003,'Al-Shamal'),('Sultan Al-Brake','D',1996,'Al-Duhail'),
        ('Lucas Mendes','D',1990,'Al-Wakrah'),('Pedro Miguel','D',1990,'Al-Sadd'),
        ('Boualem Khoukhi','D',1990,'Al-Sadd'),('Homam Al-Amin','D',1999,'CyD Leonesa'),
        ('Issa Laye','D',1997,'Al-Arabi'),('Al-Hashmi Al-Hussain','D',2003,'Al-Arabi'),
        ('Ayoub Al-Oui','D',2005,'Al-Gharafa'),('Meshaal Barsham','P',1998,'Al-Sadd'),
        ('Mahmoud Abunada','P',2000,'Al-Rayyan'),('Salah Zakaria','P',1999,'Al-Duhail'),
    ],
    'RD Congo': [
        ('Yoane Wissa','A',1996,'Newcastle'),('Cedric Bakambu','A',1991,'Betis'),
        ('Simon Banza','A',1996,'Al-Jazira'),('Theo Bongonda','A',1995,'Spartak'),
        ('Fiston Mayele','A',1994,'Pyramids'),('Gael Kakuta','C',1991,'AE Larisa'),
        ('Meschack Elia','C',1997,'Alanyaspor'),('Samuel Moutoussamy','C',1996,'Atromitos'),
        ('Brian Cipenga','C',1998,'Castellon'),('Edo Kayembe','C',1998,'Watford'),
        ('Nathanael Mbuku','C',2002,'Montpellier'),('Noah Sadiki','C',2004,'Sunderland'),
        ("Ngal'ayel Mukau",'C',2004,'Lilla'),('Charles Pickel','C',1997,'Espanyol'),
        ('Chancel Mbemba','D',1994,'Lilla'),('Aaron Wan-Bissaka','D',1997,'West Ham'),
        ('Arthur Masuaku','D',1993,'Lens'),('Dylan Batubinsika','D',1996,'AE Larisa'),
        ('Joris Kayembe','D',1994,'Genk'),('Steve Kapuadi','D',1998,'Widzew'),
        ('Rocky Bushiri','D',1999,'Hibernian'),('Gedeon Kalulu','D',1997,'Aris'),
        ('Alex Tuanzebe','D',1997,'Burnley'),('Matthieu Epolo','P',2005,'Standard'),
        ('Timothy Fayulu','P',1999,'FC Noah'),('Lionel Mpasi','P',1994,'Le Havre'),
    ],
    'Rep. Ceca': [
        ('Patrik Schick','A',1996,'Leverkusen'),('Adam Hlozek','A',2002,'Hoffenheim'),
        ('Jan Kuchta','A',1997,'Sparta'),('Tomas Chory','A',1995,'Slavia'),
        ('Mojmir Chytil','A',1999,'Slavia'),('Hugo Sochurek','C',2008,'Sparta'),
        ('Tomas Soucek','C',1995,'West Ham'),('Lukas Provod','C',1996,'Slavia'),
        ('Pavel Sulc','C',2000,'Lione'),('Michal Sadilek','C',1999,'Slavia'),
        ('Lukas Cerv','C',2001,'Plzen'),('Alexandr Sojka','C',2003,'Plzen'),
        ('Denis Visinsky','C',2003,'Plzen'),('Vladimir Darida','C',1990,'Hradec'),
        ('Vladimir Coufal','D',1992,'Hoffenheim'),('Tomas Holes','D',1993,'Slavia'),
        ('Ladislav Krejci','D',1999,'Wolverhampton'),('David Zima','D',2000,'Slavia'),
        ('Robin Hranac','D',2000,'Hoffenheim'),('David Doudera','D',1998,'Slavia'),
        ('Jaroslav Zeleny','D',1992,'Sparta'),('David Jurasek','D',2000,'Slavia'),
        ('Stepan Chaloupek','D',2003,'Slavia'),('Matej Kovar','P',2000,'PSV'),
        ('Jindrich Stanek','P',1996,'Slavia'),('Lukas Hornicek','P',2002,'Braga'),
    ],
    'Scozia': [
        ('Che Adams','A',1996,'Torino'),('Lyndon Dykes','A',1995,'Charlton'),
        ('Lawrence Shankland','A',1995,'Hearts'),('Ross Stewart','A',1996,'Southampton'),
        ('George Hirst','A',1999,'Ipswich'),('Scott McTominay','C',1996,'Napoli'),
        ('John McGinn','C',1994,'Aston Villa'),('Lewis Ferguson','C',1999,'Bologna'),
        ('Ryan Christie','C',1995,'Bournemouth'),('Kenny McLean','C',1992,'Norwich'),
        ('Ben Gannon-Doak','C',2005,'Bournemouth'),('Findlay Curtis','C',2006,'Kilmarnock'),
        ('Tyler Fletcher','C',2007,'Manchester United'),('Andrew Robertson','D',1994,'Liverpool'),
        ('Kieran Tierney','D',1997,'Celtic'),('Aaron Hickey','D',2002,'Brentford'),
        ('Grant Hanley','D',1991,'Hibernian'),('Jack Hendry','D',1995,'Al-Ettifaq'),
        ('Scott McKenna','D',1996,'Dinamo Zagabria'),('Anthony Ralston','D',1998,'Celtic'),
        ('Nathan Patterson','D',2001,'Everton'),('John Souttar','D',1996,'Glasgow Rangers'),
        ('Dominic Hyam','D',1995,'Wrexham'),('Craig Gordon','P',1982,'Hearts'),
        ('Angus Gunn','P',1996,'Nottingham'),('Liam Kelly','P',1996,'Glasgow Rangers'),
    ],
    'Senegal': [
        ('Sadio Mane','A',1992,'Al Nassr'),('Nicolas Jackson','A',2001,'Bayern'),
        ('Ismaila Sarr','A',1998,'Crystal Palace'),('Bamba Dieng','A',2000,'Lorient'),
        ('Assane Diao','A',2005,'Como'),('Iliman Ndiaye','A',2006,'Everton'),
        ('Ibrahim Mbaye','A',2008,'PSG'),('Cherif Ndiaye','A',1996,'Samsunspor'),
        ('Pape Matar Sarr','C',2002,'Tottenham'),('Lamine Camara','C',2004,'Monaco'),
        ('Idrissa Gueye','C',1989,'Everton'),('Pape Gueye','C',1999,'Villarreal'),
        ('Pathe Ciss','C',1994,'Rayo'),('Habib Diarra','C',2004,'Sunderland'),
        ('Bara Sapoko Ndiaye','C',2007,'Bayern'),('Kalidou Koulibaly','D',1991,'Al-Hilal'),
        ('Moussa Niakhate','D',1996,'Lione'),('Krepin Diatta','D',1999,'Monaco'),
        ('Ismail Jakobs','D',1999,'Galatasaray'),('Abdoulaye Seck','D',1992,'Haifa'),
        ('El Hadji Malick Diouf','D',2004,'West Ham'),('Antoine Mendy','D',2004,'Nizza'),
        ('Mamadou Sarr','D',2005,'Chelsea'),('Edouard Mendy','P',1992,'Al-Ahli'),
        ('Mory Diaw','P',1993,'Le Havre'),('Yehvann Diouf','P',1999,'Nizza'),
    ],
    'Spagna': [
        ('Lamine Yamal','A',2007,'Barcellona'),('Nico Williams','A',2002,'Athletic Bilbao'),
        ('Dani Olmo','A',1998,'Barcellona'),('Ferran Torres','A',2000,'Barcellona'),
        ('Mikel Oyarzabal','A',1997,'Real Sociedad'),('Borja Iglesias','A',1993,'Celta'),
        ('Yeremy Pino','A',2002,'Crystal Palace'),('Victor Munoz','A',2003,'Osasuna'),
        ('Rodri','C',1996,'Manchester City'),('Pedri','C',2002,'Barcellona'),
        ('Gavi','C',2004,'Barcellona'),('Mikel Merino','C',1996,'Arsenal'),
        ('Fabian Ruiz','C',1996,'PSG'),('Martin Zubimendi','C',1999,'Arsenal'),
        ('Alex Baena','C',2001,'Atletico'),('Pau Cubarsi','D',2007,'Barcellona'),
        ('Aymeric Laporte','D',1994,'Athletic Bilbao'),('Marc Cucurella','D',1998,'Chelsea'),
        ('Eric Garcia','D',2001,'Barcellona'),('Pedro Porro','D',1999,'Tottenham'),
        ('Alex Grimaldo','D',1995,'Leverkusen'),('Marcos Llorente','D',1995,'Atletico'),
        ('Marc Pubill','D',2003,'Atletico'),('Unai Simon','P',1997,'Athletic Bilbao'),
        ('David Raya','P',1995,'Arsenal'),('Joan Garcia','P',2001,'Barcellona'),
    ],
    'Sudafrica': [
        ('Lyle Foster','A',2000,'Burnley'),('Evidence Makgopa','A',2000,'Pirates'),
        ('Oswin Appollis','A',2001,'Pirates'),('Relebohile Mofokeng','A',2004,'Pirates'),
        ('Themba Zwane','A',1989,'Sundowns'),('Iqraam Rayners','A',1995,'Sundowns'),
        ('Thapelo Maseko','A',2003,'AEL'),('Tshepang Moremi','A',2000,'Pirates'),
        ('Teboho Mokoena','C',1997,'Sundowns'),('Jayden Adams','C',2001,'Sundowns'),
        ('Thalente Mbatha','C',2000,'Pirates'),('Sphephelo Sithole','C',1999,'Tondela'),
        ('Khuliso Mudau','D',1995,'Sundowns'),('Nkosinathi Sibisi','D',1995,'Pirates'),
        ('Aubrey Modiba','D',1995,'Sundowns'),('Kamogelo Sebelebele','D',2002,'Pirates'),
        ('Bradley Cross','D',2001,'Chiefs'),('Olwethu Makhanya','D',2004,'Philadelphia'),
        ('Mbekezeli Mbokazi','D',2005,'Chicago'),('Ime Okon','D',2004,'Hannover'),
        ('Samukele Kabini','D',2004,'Molde'),('Khulumani Ndamane','D',2004,'Sundowns'),
        ('Thabang Matuludi','D',1999,'Polokwane'),('Ronwen Williams','P',1992,'Sundowns'),
        ('Ricardo Goss','P',1994,'Siwelele'),('Song Sipho','P',1996,'Pirates'),
    ],
    'Svezia': [
        ('Viktor Gyokeres','A',1998,'Arsenal'),('Alexander Isak','A',1999,'Liverpool'),
        ('Anthony Elanga','A',2002,'Newcastle'),('Gustaf Nilsson','A',1997,'Bruges'),
        ('Taha Ali','A',1998,'Malmo'),('Alexander Bernhardsson','A',1998,'Holstein Kiel'),
        ('Lucas Bergvall','C',2006,'Tottenham'),('Yasin Ayari','C',2003,'Brighton'),
        ('Mattias Svanberg','C',1999,'Wolfsburg'),('Benjamin Nygren','C',2001,'Celtic'),
        ('Ken Sema','C',1993,'Pafos'),('Jesper Karlstrom','C',1995,'Udinese'),
        ('Elliot Stroud','C',2002,'Mjallby'),('Besfort Zeneli','C',2002,'Union SG'),
        ('Victor Lindelof','D',1994,'Aston Villa'),('Isak Hien','D',1999,'Atalanta'),
        ('Carl Starfelt','D',1995,'Celta'),('Gabriel Gudmundsson','D',1999,'Leeds'),
        ('Hjalmar Ekdal','D',1998,'Burnley'),('Eric Smith','D',1997,'St. Pauli'),
        ('Daniel Svensson','D',2002,'Dortmund'),('Herman Johansson','D',1997,'Dallas'),
        ('Viktor Johansson','P',1998,'Stoke'),('Gustaf Lagerbielke','P',2000,'SC Braga'),
        ('Jacob Widell Zetterstrom','P',1998,'Derby'),('Kristoffer Nordfeldt','P',1989,'AIK'),
    ],
    'Svizzera': [
        ('Breel Embolo','A',1997,'Rennes'),('Dan Ndoye','A',2000,'Nottingham'),
        ('Noah Okafor','A',2000,'Leeds'),('Zeki Amdouni','A',2000,'Burnley'),
        ('Ruben Vargas','A',1998,'Siviglia'),('Cedric Itten','A',1996,'Dusseldorf'),
        ('Granit Xhaka','C',1992,'Sunderland'),('Remo Freuler','C',1992,'Bologna'),
        ('Ardon Jashari','C',2002,'Milan'),('Djibril Sow','C',1997,'Siviglia'),
        ('Fabian Rieder','C',2002,'Augusta'),('Michel Aebischer','C',1997,'Pisa'),
        ('Denis Zakaria','C',1996,'Monaco'),('Christian Fassnacht','C',1993,'Young Boys'),
        ('Johan Manzambi','C',2005,'Friburgo'),('Manuel Akanji','D',1995,'Inter'),
        ('Ricardo Rodriguez','D',1992,'Betis'),("Nico Elvedi",'D',1996,"M'Gladbach"),
        ('Silvan Widmer','D',1993,'Magonza'),('Eray Comert','D',1998,'Valencia'),
        ('Miro Muheim','D',1998,'Amburgo'),('Aurele Amenda','D',2003,'Francoforte'),
        ('Luca Jaquez','D',2003,'Stoccarda'),('Gregor Kobel','P',1997,'Borussia'),
        ('Yvon Mvogo','P',1994,'Lorient'),('Marvin Keller','P',2002,'Young Boys'),
    ],
    'Tunisia': [
        ('Ellyes Skhiri','C',1995,'Francoforte'),('Elias Achouri','A',1999,'Copenhagen'),
        ('Firas Chaouat','A',1996,'Club Africain'),('Hazem Mastouri','A',1997,'Makhachkala'),
        ('Elias Saad','A',1999,'Hannover'),('Ismael Gharbi','A',2004,'Augusta'),
        ('Khalil Ayari','A',2005,'PGS U23'),('Rayan Elloumi','A',2007,'Vancouver'),
        ('Sebastian Tounekti','A',2002,'Celtic'),('Hannibal Mejbri','C',2003,'Burnley'),
        ('Mortadha Ben Ouanes','C',1994,'Kasimpasa'),('Anis Ben Slimane','C',2001,'Norwich'),
        ('Rani Khedira','C',1994,'Union Berlino'),('Hadj Mahmoud','C',2000,'Lugano'),
        ('Montassar Talbi','D',1998,'Lorient'),('Dylan Bronn','D',1995,'Servette'),
        ('Ali Abdi','D',1993,'Nizza'),('Yan Valery','D',1999,'Young Boys'),
        ('Omar Rekik','D',2001,'Maribor'),('Mohamed Amine Ben Hamida','D',1995,'Esperance'),
        ('Adem Arous','D',2004,'Kasimpasa'),('Raed Chikhaoui','D',2004,'US Monastir'),
        ('Moutaz Neffati','D',2004,'Norrkoping'),('Aymen Dahmen','P',1997,'CS Sfaxien'),
        ('Sabri Ben Hassan','P',1996,'ES Sahel'),('Abdelmouhib Chamakh','P',2001,'Club Africain'),
    ],
    'Turchia': [
        ('Arda Guler','A',2005,'Real Madrid'),('Kenan Yildiz','A',2005,'Juventus'),
        ('Kerem Akturkoglu','A',1998,'Fenerbahce'),('Baris Alper Yilmaz','A',2000,'Galatasaray'),
        ('Yunus Akgun','A',2000,'Galatasaray'),('Can Uzun','A',2005,'Francoforte'),
        ('Oguz Aydin','A',2000,'Fenerbahce'),('Deniz Gul','A',2004,'FC Porto'),
        ('Irfan Can Kahveci','A',1995,'Kasimpasa'),('Hakan Calhanoglu','C',1994,'Inter'),
        ('Orkun Kokcu','C',2000,'Besiktas'),('Salih Ozcan','C',1998,'Dortmund'),
        ('Kaan Ayhan','C',1994,'Galatasaray'),('Ismail Yuksek','C',1999,'Fenerbahce'),
        ('Ferdi Kadioglu','D',1999,'Brighton'),('Merih Demiral','D',1998,'Al-Ahli'),
        ('Zeki Celik','D',1997,'Roma'),('Caglar Soyuncu','D',1996,'Fenerbahce'),
        ('Abdulkerim Bardakci','D',1994,'Galatasaray'),('Samet Akaydin','D',1994,'Rizespor'),
        ('Ozan Kabak','D',2000,'Hoffenheim'),('Eren Elmali','D',2000,'Galatasaray'),
        ('Mert Muldur','D',1999,'Fenerbahce'),('Altay Bayindir','P',1998,'Manchester United'),
        ('Ugurcan Cakir','P',1996,'Galatasaray'),('Mert Gunok','P',1989,'Fenerbahce'),
    ],
    'Uruguay': [
        ('Darwin Nunez','A',1999,'Al-Hilal'),('Federico Vinas','A',1998,'Oviedo'),
        ('Rodrigo Aguirre','A',1994,'Tigres'),('Facundo Pellistri','C',2001,'Panathinaikos'),
        ('Federico Valverde','C',1998,'Real Madrid'),('Rodrigo Bentancur','C',1997,'Tottenham'),
        ('Manuel Ugarte','C',2001,'Manchester United'),('Giorgian de Arrascaeta','C',1994,'Flamengo'),
        ('Nicolas de la Cruz','C',1997,'Flamengo'),('Brian Rodriguez','C',2000,'America'),
        ('Maximiliano Araujo','C',2000,'Sporting'),('Agustin Canobbio','C',1998,'Fluminense'),
        ('Emiliano Martinez','C',1999,'Palmeiras'),('Rodrigo Zalazar','C',1999,'Braga'),
        ('Juan Manuel Sanabria','C',2000,'Real Salt Lake'),('Ronald Araujo','D',1999,'Barcellona'),
        ('Jose Maria Gimenez','D',1995,'Atletico'),('Mathias Olivera','D',1997,'Napoli'),
        ('Matias Vina','D',1997,'River Plate'),('Santiago Bueno','D',1998,'Wolverhampton'),
        ('Joaquin Piquerez','D',1998,'Palmeiras'),('Sebastian Caceres','D',1999,'America'),
        ('Guillermo Varela','D',1993,'Flamengo'),('Fernando Muslera','P',1986,'Estudiantes'),
        ('Sergio Rochet','P',1993,'Internacional'),('Santiago Mele','P',1997,'Monterrey'),
    ],
    'USA': [
        ('Christian Pulisic','A',1998,'Milan'),('Timothy Weah','A',2000,'Marsiglia'),
        ('Folarin Balogun','A',2001,'Monaco'),('Brendon Aaronson','A',2000,'Leeds'),
        ('Haji Wright','A',1998,'Coventry'),('Ricardo Papi','A',2003,'PSV'),
        ('Alejandro Zendejas','A',1998,'America'),('Tyler Adams','C',1999,'Bournemouth'),
        ('Weston McKennie','C',1998,'Juventus'),('Giovanni Reyna','C',2002,"M'Gladbach"),
        ('Cristian Roldan','C',1995,'Seattle'),('Mark Tillman','C',2002,'Leverkusen'),
        ('Sebastian Berhalter','C',2001,'Vancouver'),('Antonee Robinson','D',1997,'Fulham'),
        ('Sergino Dest','D',2000,'PSV'),('Chris Richards','D',2000,'Crystal Palace'),
        ('Miles Robinson','D',1997,'Cincinnati'),('Mark McKenzie','D',1999,'Tolosa'),
        ('Auston Trusty','D',1998,'Celtic'),('Joe Scally','D',2002,"M'Gladbach"),
        ('Maximilian Arfsten','D',2001,'Columbus'),('Alex Freeman','D',2004,'Villarreal'),
        ('Tim Ream','D',1987,'Charlotte'),('Matt Turner','P',1994,'New England'),
        ('Matt Freese','P',1998,'New York City'),('Chris Brady','P',2004,'Chicago'),
    ],
    'Uzbekistan': [
        ('Eldor Shomurodov','A',1995,'Basaksehir'),('Abbosbek Fayzullaev','A',2003,'Basaksehir'),
        ('Igor Sergeev','A',1993,'Persepolis'),('Dostonbek Khamdamov','A',1996,'Pakhtakor'),
        ('Azizbek Amanov','A',1997,'Dinamo Samarcanda'),('Oston Urunov','C',2000,'Persepolis'),
        ('Jaloliddin Masharipov','C',1993,'Esteghlal'),('Akmal Mozgovoy','C',1999,'Pakhtakor'),
        ('Odildzhon Khamrobekov','C',1996,'Tractor'),('Abdulla Abdullaev','C',1997,'Dibba'),
        ('Otabek Shukurov','C',1996,'Baniyas'),('Sherzod Esanov','C',2003,'FC Buxoro'),
        ('Jamshid Iskanderov','C',1993,'Neftchi'),('Abdukodir Khusanov','D',2004,'Manchester City'),
        ('Rustam Ashurmatov','D',1996,'Esteghlal'),('Khozhiakbar Alizhonov','D',1997,'Pakhtakor'),
        ('Sherzod Nasrullaev','D',1998,'Pakhtakor'),('Farrukh Sayfiev','D',1991,'Neftchi'),
        ('Avazbek Ulmasaliev','D',2000,'OKMK'),('Umar Eshmurodov','D',1992,'Nasaf'),
        ('Jakhongir Urozov','D',2004,'Dinamo Samarcanda'),('Bekhruz Karimov','D',2007,'Surkhon'),
        ('Utkir Yusupov','P',1991,'PFC Navbahor'),('Botirali Ergashev','P',1995,'Neftchi'),
        ('Abduvokhid Nematov','P',2001,'Nasaf'),
    ],
}


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
        label = f"{'✓ ' if is_sel else ''}{flag(t)} {t}"
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
                    '<div style="height:36px;display:flex;align-items:center;'
                    'justify-content:center;background:rgba(255,255,255,0.03);'
                    'border:1px dashed rgba(255,255,255,0.1);border-radius:5px;'
                    'font-size:8px;color:rgba(255,255,255,0.2);margin:1px 0;">?</div>',
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
    # H must equal the actual rendered height of mkc() for vertical centering to work.
    # Measured from screenshot at 50% zoom: 8 R16 matches span ~540 screen px
    # → 540*2 = 1080 CSS px / 8 matches = 135px per match (venue+2 slots+spacer+Streamlit gap)
    H = 136
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
    st.caption("Seleziona la nazione, poi scegli il giocatore per ogni premio.")

    _NATIONS   = sorted(PLAYERS_DB.keys())
    _EMPTY_NAT = "— scegli nazione —"
    _ROLE_COL  = {'P': '#1DE9B6', 'D': '#4CAF50', 'C': '#2196F3', 'A': '#FF5722'}

    def _player_table(players):
        rows = ""
        for nm, rl, yr, cl in players:
            age = 2026 - yr
            rc  = _ROLE_COL.get(rl, '#888')
            rows += (
                f'<tr>'
                f'<td style="padding:3px 6px;color:#F0F6FC;font-size:11px">{nm}</td>'
                f'<td style="padding:3px 4px;text-align:center">'
                f'<span style="background:{rc};color:#0A1628;border-radius:4px;'
                f'padding:1px 5px;font-size:9px;font-weight:700">{rl}</span></td>'
                f'<td style="padding:3px 4px;text-align:center;color:#F0F6FC;font-size:11px">{age}</td>'
                f'<td style="padding:3px 6px;color:rgba(240,246,252,0.55);font-size:10px">{cl}</td>'
                f'</tr>'
            )
        return (
            '<div style="background:#0A1628;border:1px solid rgba(29,233,182,0.2);'
            'border-radius:8px;overflow:hidden;margin-bottom:6px;">'
            '<div style="overflow-y:auto;max-height:200px;">'
            '<table style="width:100%;border-collapse:collapse;">'
            '<thead><tr style="background:#162032;position:sticky;top:0;">'
            '<th style="padding:5px 6px;text-align:left;color:#1DE9B6;font-size:9px;font-weight:700">NOME</th>'
            '<th style="padding:5px 4px;text-align:center;color:#1DE9B6;font-size:9px;font-weight:700">R</th>'
            '<th style="padding:5px 4px;text-align:center;color:#1DE9B6;font-size:9px;font-weight:700">ETÀ</th>'
            '<th style="padding:5px 6px;text-align:left;color:#1DE9B6;font-size:9px;font-weight:700">CLUB</th>'
            f'</tr></thead><tbody>{rows}</tbody>'
            '</table></div></div>'
        )

    def _award_col(col, title_html, award_key, nat_key, u23_only=False):
        with col:
            st.markdown(title_html, unsafe_allow_html=True)
            sel_nat = st.selectbox(
                "Nazione", [_EMPTY_NAT] + _NATIONS,
                key=nat_key, label_visibility="collapsed",
            )
            if sel_nat != _EMPTY_NAT:
                players = PLAYERS_DB.get(sel_nat, [])
                if u23_only:
                    players = [p for p in players if p[2] >= 2003]
                if players:
                    st.markdown(_player_table(players), unsafe_allow_html=True)
                    names = [EMPTY] + [p[0] for p in players]
                    cur   = st.session_state.get(award_key, EMPTY)
                    if cur not in names:
                        st.session_state[award_key] = EMPTY
                        cur = EMPTY
                    st.selectbox(
                        "Seleziona", names,
                        index=names.index(cur),
                        key=award_key, label_visibility="collapsed",
                    )
                else:
                    st.info("Nessun giocatore U23 disponibile per questa nazione.")
            else:
                st.markdown(
                    '<div style="text-align:center;padding:18px;color:rgba(240,246,252,0.4);'
                    'font-size:12px;border:1px dashed rgba(29,233,182,0.15);border-radius:8px;">'
                    '⬆️ Scegli una nazione</div>', unsafe_allow_html=True
                )

    c1, c2, c3 = st.columns(3)
    _award_col(
        c1,
        '<div style="background:#0A1628;border-radius:12px;padding:10px 14px;'
        'border:1.5px solid #D4A017;margin-bottom:8px;text-align:center;">'
        '<span style="color:#FFD700;font-size:22px;">\U0001f3c5</span>'
        '<div style="color:#FFD700;font-weight:800;font-size:13px;margin-top:4px;">'
        'MIGLIOR GIOCATORE</div></div>',
        "best_player", "nat_mg",
    )
    _award_col(
        c2,
        '<div style="background:#0A1628;border-radius:12px;padding:10px 14px;'
        'border:1.5px solid #D4A017;margin-bottom:8px;text-align:center;">'
        '<span style="color:#FFD700;font-size:22px;">⚽</span>'
        '<div style="color:#FFD700;font-weight:800;font-size:13px;margin-top:4px;">'
        'CAPOCANNONIERE</div></div>',
        "top_scorer", "nat_cc",
    )
    _award_col(
        c3,
        '<div style="background:#0A1628;border-radius:12px;padding:10px 14px;'
        'border:1.5px solid #D4A017;margin-bottom:8px;text-align:center;">'
        '<span style="color:#FFD700;font-size:22px;">\U0001f331</span>'
        '<div style="color:#FFD700;font-weight:800;font-size:13px;margin-top:4px;">'
        'MIGLIOR UNDER 23</div></div>',
        "best_u23", "nat_u23", u23_only=True,
    )

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
