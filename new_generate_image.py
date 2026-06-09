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
    nat_mg  = st.session_state.get("nat_mg",  EMPTY)
    nat_cc  = st.session_state.get("nat_cc",  EMPTY)
    nat_u23 = st.session_state.get("nat_u23", EMPTY)

    # (18, 29) ≈ 9:14.5 — leggermente meno di 9:16 ma elimina lo spazio vuoto
    fig = plt.figure(figsize=(18, 29), facecolor=IMG_BG)

    # ── Attribution strip ────────────────────────────────────
    ax_att = fig.add_axes([0, 0.965, 1, 0.035])
    ax_att.set_facecolor('#0d1e34'); ax_att.axis('off')
    ax_att.text(0.5, 0.72, 'Made by R.A.Frisoli  \xb7  Match & Data Analyst',
                ha='center', va='center', fontsize=9, fontweight='bold',
                color=IMG_TEAL, transform=ax_att.transAxes)
    ax_att.text(0.5, 0.25, 'prediction-wc2026.streamlit.app',
                ha='center', va='center', fontsize=8,
                color=IMG_GOLD, transform=ax_att.transAxes)

    # ── Header banner (fedele all'immagine: navy + bordo oro + logo + titolo + sottotitolo) ──
    ax_h = fig.add_axes([0.008, 0.904, 0.984, 0.066])
    ax_h.set_facecolor('#0d1a2e')
    ax_h.set_xlim(0, 1); ax_h.set_ylim(0, 1); ax_h.axis('off')
    ax_h.add_patch(FancyBboxPatch(
        (0.003, 0.04), 0.994, 0.920,
        boxstyle="round,pad=0.015",
        facecolor='none', edgecolor=IMG_GOLD,
        linewidth=2.8, zorder=5, transform=ax_h.transAxes, clip_on=False))
    # Logo trofeo (prova prima .png poi .webp)
    try:
        from PIL import Image as _PILImage
        _assets = os.path.join(os.path.dirname(__file__), "assets")
        _lp = next(
            p for p in [
                os.path.join(_assets, "wc2026_logo.png"),
                os.path.join(_assets, "wc2026_logo.webp"),
            ] if os.path.exists(p)
        )
        _ld = _np.array(_PILImage.open(_lp).convert("RGBA"), dtype=_np.uint8)
        # Rimuovi solo il bianco (margini PNG) — mantieni le "26"
        _ld[(_ld[:,:,0] > 215) & (_ld[:,:,1] > 215) & (_ld[:,:,2] > 215), 3] = 0
        # Converti il nero puro ("26") in oro per renderlo visibile sul banner scuro
        _dark = (_ld[:,:,0] < 15) & (_ld[:,:,1] < 15) & (_ld[:,:,2] < 15)
        _ld[_dark, 0] = 240; _ld[_dark, 1] = 178; _ld[_dark, 2] = 36
        ax_h.add_artist(AnnotationBbox(OffsetImage(_ld, zoom=0.09), (0.060, 0.50),
                                       frameon=False, zorder=4, clip_on=True))
    except Exception:
        pass
    # Titolo e sottotitolo centrati (x=0.50)
    ax_h.text(0.50, 0.66, 'FIFA WORLD CUP 2026', ha='center', va='center',
              fontsize=22, fontweight='black', color=IMG_GOLD,
              transform=ax_h.transAxes, zorder=4)
    ax_h.text(0.50, 0.26,
              'USA \xb7 Canada \xb7 Messico  |  11 giugno – 19 luglio 2026  |  48 squadre \xb7 104 partite',
              ha='center', va='center', fontsize=9, color='#8d9cb8',
              transform=ax_h.transAxes, zorder=4)

    # ── Groups: 4 rows \xd7 3 cols (compact) ─────────────────────
    gkeys  = list(GROUPS.keys())
    g_top, g_bot, gap = 0.902, 0.500, 0.007
    col_w  = 1 / 3
    cell_w = col_w - 0.014
    cell_h = (g_top - g_bot) / 4 - gap
    POS_C = [IMG_GOLD, '#d0d0d0', '#cd7f32', IMG_MUTED]
    POS_L = ['1\xb0', '2\xb0', '3\xb0', '4\xb0']
    for gi, grp in enumerate(gkeys):
        lx = (gi % 3) * col_w + 0.007
        ly = g_top - (gi // 3 + 1) * (cell_h + gap)
        ax = fig.add_axes([lx, ly, cell_w, cell_h])
        ax.set_facecolor(IMG_CARD); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
        for s in ax.spines.values():
            s.set_edgecolor(IMG_TEAL); s.set_linewidth(1.1)
        ax.text(0.5, 0.90, f'GRUPPO {grp}', ha='center', va='center',
                fontsize=10.5, fontweight='bold', color=IMG_TEAL)
        ax.plot([0.05,0.95],[0.80,0.80], color=IMG_TEAL, lw=0.5, alpha=0.4)
        for pos in range(4):
            team = grp_team(grp, pos)
            yy   = 0.68 - pos * 0.163
            ax.text(0.05, yy, POS_L[pos], ha='left', va='center',
                    fontsize=9, color=POS_C[pos], fontweight='bold')
            _place_flag(ax, team, (0.17, yy), zoom=0.44)
            ax.text(0.30, yy, team[:16], ha='left', va='center',
                    fontsize=9, fontweight='bold',
                    color=IMG_TEXT if pos < 2 else IMG_MUTED)

    # ── VERTICAL BRACKET ─────────────────────────────────────
    ax_br = fig.add_axes([0, 0.104, 1, 0.394])
    ax_br.set_facecolor(IMG_BG); ax_br.set_xlim(0,100); ax_br.set_ylim(0,100)
    ax_br.axis('off')
    ax_br.text(50, 99, 'TABELLONE — FASE AD ELIMINAZIONE DIRETTA',
               ha='center', va='top', fontsize=11, fontweight='bold', color=IMG_TEAL)

    PW, PH, PH2 = 10.5, 3.5, 1.75
    xs8 = [6.25, 18.75, 31.25, 43.75, 56.25, 68.75, 81.25, 93.75]
    xs4 = [12.5, 37.5, 62.5, 87.5]
    xs2 = [25.0, 75.0]
    xs1 = [50.0]

    Y_R16, Y_R8, Y_QF, Y_SF = 92.0, 79.5, 68.5, 59.0

    CHAMP_CY  = 48.0
    CHAMP_W   = 18.0   # solo campione dentro
    CHAMP_H   = 10.0
    CHAMP_TOP = CHAMP_CY + CHAMP_H / 2   # 53.0
    CHAMP_BOT = CHAMP_CY - CHAMP_H / 2   # 43.0

    Y_SF2, Y_QF2, Y_R8_2, Y_R16_2 = 35.0, 23.5, 12.5, 1.75

    def _ps(t, nw):
        if not t or t == EMPTY: return IMG_CARD, IMG_LINE, 0.5, IMG_MUTED, False
        if nw and t in nw:      return '#152b1c', IMG_TEAL, 1.8, IMG_TEXT, True
        if nw:                  return '#0e1820', '#1d2d3a', 0.4, '#3a5068', False
        return IMG_CARD, IMG_LINE, 0.5, IMG_TEXT, False

    def _ps_sf(t):
        cv = champ if champ and champ != EMPTY else None
        if not t or t == EMPTY: return IMG_CARD, IMG_LINE, 0.5, IMG_MUTED, False
        if cv and t == cv:      return '#1f1a00', IMG_GOLD, 2.0, IMG_GOLD, True
        if cv:                  return '#0e1820', '#1d2d3a', 0.4, '#3a5068', False
        return IMG_CARD, IMG_LINE, 0.5, IMG_TEXT, False

    def dpill(cx, cy, team, style):
        bg, bd, lw, col, bold = style
        ax_br.add_patch(FancyBboxPatch(
            (cx-PW/2, cy-PH2), PW, PH, boxstyle="round,pad=0.1",
            facecolor=bg, edgecolor=bd, linewidth=lw, zorder=2))
        if team and team != EMPTY:
            arr = _flag_arr(team)
            if arr is not None:
                _place_flag(ax_br, team, (cx-PW/2+1.6, cy), zoom=0.40, zorder=3)
                ax_br.text(cx-PW/2+3.6, cy, team[:12], ha='left', va='center',
                           fontsize=8, fontweight='bold', color=col, zorder=3)
            else:
                ax_br.text(cx, cy, team[:13], ha='center', va='center',
                           fontsize=8, fontweight='bold', color=col, zorder=3)
        else:
            ax_br.text(cx, cy, '?', ha='center', va='center',
                       fontsize=8, color=IMG_MUTED, zorder=3)

    def conn_down(xs_from, xs_to, yf_cy, yt_cy):
        yf = yf_cy - PH2; yt = yt_cy + PH2; yb = (yf+yt)/2
        for k, xm in enumerate(xs_to):
            xa, xb = xs_from[2*k], xs_from[2*k+1]
            for x_ in (xa, xb): ax_br.plot([x_,x_],[yf,yb],color=IMG_LINE,lw=0.5,zorder=1)
            ax_br.plot([xa,xb],[yb,yb],color=IMG_LINE,lw=0.5,zorder=1)
            ax_br.plot([xm,xm],[yb,yt],color=IMG_LINE,lw=0.5,zorder=1)

    def conn_up(xs_from, xs_to, yf_cy, yt_cy):
        yf = yf_cy + PH2; yt = yt_cy - PH2; yb = (yf+yt)/2
        for k, xm in enumerate(xs_to):
            xa, xb = xs_from[2*k], xs_from[2*k+1]
            for x_ in (xa, xb): ax_br.plot([x_,x_],[yf,yb],color=IMG_LINE,lw=0.5,zorder=1)
            ax_br.plot([xa,xb],[yb,yb],color=IMG_LINE,lw=0.5,zorder=1)
            ax_br.plot([xm,xm],[yb,yt],color=IMG_LINE,lw=0.5,zorder=1)

    def slbl(y, txt, sz=7.0):
        ax_br.text(50, y, txt, ha='center', va='center',
                   fontsize=sz, color=IMG_MUTED, fontweight='bold')

    nw = lambda lst: set(t for t in lst if t and t != EMPTY)
    NW_R8T = nw(r8_win[:4]); NW_R8B = nw(r8_win[4:])
    NW_QFT = nw(qf_win[:2]); NW_QFB = nw(qf_win[2:])
    NW_SFT = nw(sf_win[:1]); NW_SFB = nw(sf_win[1:])

    # ── TOP BRACKET ──────────────────────────────────────────
    slbl(96.5, '▾  SEDICESIMI  ▾', 7.5)
    for xi, t in zip(xs8, r16_win[:8]): dpill(xi, Y_R16, t, _ps(t, NW_R8T))
    conn_down(xs8, xs4, Y_R16, Y_R8)
    slbl(85.5, '▾  OTTAVI  ▾')
    for xi, t in zip(xs4, r8_win[:4]):  dpill(xi, Y_R8,  t, _ps(t, NW_QFT))
    conn_down(xs4, xs2, Y_R8, Y_QF)
    slbl(74.5, '▾  QUARTI  ▾')
    for xi, t in zip(xs2, qf_win[:2]):  dpill(xi, Y_QF,  t, _ps(t, NW_SFT))
    conn_down(xs2, xs1, Y_QF, Y_SF)
    slbl(64.5, '▾  SEMIFINALI  ▾')
    dpill(xs1[0], Y_SF, sf_win[0], _ps_sf(sf_win[0]))
    ax_br.plot([50,50],[Y_SF-PH2, CHAMP_TOP], color=IMG_GOLD, lw=1.2, zorder=1)

    # ── CHAMPION BOX (solo campione, centrato e grande) ──────
    cx = 50
    # Riquadro dorato
    ax_br.add_patch(FancyBboxPatch(
        (cx-CHAMP_W/2, CHAMP_BOT), CHAMP_W, CHAMP_H, boxstyle="round,pad=0.3",
        facecolor='#0f2a1a', edgecolor=IMG_GOLD, linewidth=2.5, zorder=2))
    # Glow esterno
    ax_br.add_patch(FancyBboxPatch(
        (cx-CHAMP_W/2-0.6, CHAMP_BOT-0.6), CHAMP_W+1.2, CHAMP_H+1.2,
        boxstyle="round,pad=0.3", facecolor='none',
        edgecolor=IMG_GOLD, linewidth=0.5, alpha=0.25, zorder=1))
    # "CAMPIONE" label centrato in cima al box
    ax_br.text(cx, CHAMP_TOP-1.5, 'CAMPIONE', ha='center', va='center',
               fontsize=8, color=IMG_GOLD, fontweight='bold', zorder=3)
    # Campione: bandiera grande + nome grande, centrati nel box
    cv = champ if champ and champ != EMPTY else None
    if cv:
        _place_flag(ax_br, cv, (cx-4.0, CHAMP_CY+0.5), zoom=0.60, zorder=3)
        ax_br.text(cx-1.0, CHAMP_CY+0.5, cv[:12], ha='left', va='center',
                   fontsize=10, fontweight='black', color=IMG_GOLD, zorder=3)
    else:
        ax_br.text(cx, CHAMP_CY, '?', ha='center', va='center',
                   fontsize=14, color=IMG_GOLD, fontweight='bold', zorder=3)

    # ── 3° POSTO: fuori dal box, a destra, più piccolo ───────
    third_cx = cx + CHAMP_W / 2 + 10  # a destra del box
    td = third if third and third != EMPTY else None
    # Piccolo label "3°" in alto
    ax_br.text(third_cx, CHAMP_TOP-1.5, '3\xb0 POSTO', ha='center', va='center',
               fontsize=6, color=IMG_MUTED, zorder=3)
    if td:
        _place_flag(ax_br, td, (third_cx-2.5, CHAMP_CY+0.5), zoom=0.38, zorder=3)
        ax_br.text(third_cx, CHAMP_CY+0.5, td[:10], ha='left', va='center',
                   fontsize=7.5, color=IMG_MUTED, fontweight='bold', zorder=3)
    else:
        ax_br.text(third_cx, CHAMP_CY, '?', ha='center', va='center',
                   fontsize=8, color=IMG_MUTED, zorder=3)

    # ── BOTTOM BRACKET ────────────────────────────────────────
    ax_br.plot([50,50],[CHAMP_BOT, Y_SF2+PH2], color=IMG_GOLD, lw=1.2, zorder=1)
    dpill(xs1[0], Y_SF2, sf_win[1], _ps_sf(sf_win[1]))
    conn_up(xs2, xs1, Y_QF2, Y_SF2)
    for xi, t in zip(xs2, qf_win[2:]):  dpill(xi, Y_QF2,  t, _ps(t, NW_SFB))
    conn_up(xs4, xs2, Y_R8_2, Y_QF2)
    for xi, t in zip(xs4, r8_win[4:]):  dpill(xi, Y_R8_2, t, _ps(t, NW_QFB))
    conn_up(xs8, xs4, Y_R16_2, Y_R8_2)
    for xi, t in zip(xs8, r16_win[8:]): dpill(xi, Y_R16_2, t, _ps(t, NW_R8B))

    # ── Awards bar (più grande e visibile) ───────────────────
    ax_aw = fig.add_axes([0, 0.022, 1, 0.082])
    ax_aw.set_facecolor(IMG_CARD); ax_aw.set_xlim(0,1); ax_aw.set_ylim(0,1); ax_aw.axis('off')
    ax_aw.plot([0,1],[0.97,0.97], color=IMG_TEAL, lw=2.5)
    for i, (lbl, val, nat) in enumerate([
        ("MIGLIOR GIOCATORE", bp, nat_mg),
        ("CAPOCANNONIERE",    ts, nat_cc),
        ("MIGLIOR UNDER 23",  bu, nat_u23),
    ]):
        xi = (i + 0.5) / 3
        ax_aw.text(xi, 0.85, lbl, ha='center', va='center',
                   fontsize=10, fontweight='bold', color=IMG_TEAL)
        ax_aw.text(xi, 0.60, (val if val and val != EMPTY else '—')[:28],
                   ha='center', va='center', fontsize=13, fontweight='bold', color=IMG_TEXT)
        if nat and nat != EMPTY:
            _place_flag(ax_aw, nat, (xi, 0.28), zoom=0.54)

    # ── Footer ────────────────────────────────────────────────
    ax_f = fig.add_axes([0, 0, 1, 0.022])
    ax_f.set_facecolor(IMG_BG); ax_f.axis('off')
    ax_f.plot([0.05,0.95],[0.88,0.88], color=IMG_TEAL, lw=0.5, alpha=0.4)
    ax_f.text(0.5, 0.38, 'prediction-wc2026.streamlit.app',
              ha='center', va='center', fontsize=9, color=IMG_MUTED)

    buf = io.BytesIO()
    # Nessun bbox_inches='tight' — la figura salva esattamente nelle dimensioni impostate
    fig.savefig(buf, format=output_format, dpi=150, facecolor=IMG_BG)
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()