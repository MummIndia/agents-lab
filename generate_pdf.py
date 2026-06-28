# -*- coding: utf-8 -*-
"""
Génère le plaidoyer logement Cévennes 2050 (Lasalle & Saint-Jean-du-Gard).
Sortie : Plaidoyer_logement_Cevennes2050.pdf

Toutes les données chiffrées sont issues de sources publiques vérifiées
(INSEE Dossier complet RP2023, INSEE Focus 309). Voir SHARED_TASK_NOTES.md.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager  # noqa: F401

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image,
    Table, TableStyle, NextPageTemplate, PageBreak, KeepTogether, HRFlowable,
)

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "Logo CVN 2050.jpg")
OUT = os.path.join(HERE, "Plaidoyer_logement_Cevennes2050.pdf")
CH1 = os.path.join(HERE, "_chart_parc.png")
CH2 = os.path.join(HERE, "_chart_taux.png")

# ---------------------------------------------------------------- Palette
INK = colors.HexColor("#1A1A1A")     # noir du logo
GREEN = colors.HexColor("#2E5A3C")   # vert Cévennes (accent)
GREEN_L = colors.HexColor("#E5EDE6")
SAND = colors.HexColor("#F3ECDD")    # encadré parchemin
SAND_BORDER = colors.HexColor("#D8C9A8")
GREY = colors.HexColor("#5A5A5A")
GREY_L = colors.HexColor("#EFEFEF")
RED = colors.HexColor("#A8322A")     # alerte chiffre-clé

MPL_INK = "#1A1A1A"
MPL_GREEN = "#2E5A3C"
MPL_RS = "#C98A2B"      # résidences secondaires (ocre)
MPL_VAC = "#A8322A"     # vacants (terre rouge)
MPL_RP = "#2E5A3C"      # résidences principales (vert)
MPL_GREY = "#9A9A9A"

# ---------------------------------------------------------------- Données vérifiées (RP2023)
DATA = {
    "Lasalle": dict(total=1017, rp=628, rs=312, vac=77,
                    pop=1202, men=628, hlm=35, hlm_pct=5.6,
                    rev=19850, pauv=None),
    "Saint-Jean-du-Gard": dict(total=1881, rp=1347, rs=269, vac=265,
                               pop=2586, men=1337, hlm=45, hlm_pct=3.3,
                               rev=21770, pauv=25.0),
}
# Taux de non-occupation à l'année (RS+occ + vacants) / total
TAUX = {
    "Lasalle": 38.2,
    "Saint-Jean-du-Gard": 28.4,
    "Gard": 20.8,
    "France": 18.0,
}


def pct(part, total):
    return 100.0 * part / total


# ================================================================ GRAPHIQUES
def make_chart_parc():
    """Graphique 1 : composition du parc par commune (barres empilées horizontales)."""
    communes = ["Lasalle", "Saint-Jean-du-Gard"]
    rp = [DATA[c]["rp"] for c in communes]
    rs = [DATA[c]["rs"] for c in communes]
    vac = [DATA[c]["vac"] for c in communes]
    totals = [DATA[c]["total"] for c in communes]

    fig, ax = plt.subplots(figsize=(7.2, 2.9), dpi=200)
    y = range(len(communes))
    ax.barh(y, rp, color=MPL_RP, label="Résidences principales", height=0.55)
    ax.barh(y, rs, left=rp, color=MPL_RS,
            label="Résidences secondaires / occasionnelles", height=0.55)
    left2 = [rp[i] + rs[i] for i in range(len(communes))]
    ax.barh(y, vac, left=left2, color=MPL_VAC,
            label="Logements vacants", height=0.55)

    ax.set_yticks(list(y))
    ax.set_yticklabels(communes, fontsize=10, fontweight="bold")
    ax.invert_yaxis()
    ax.set_xlabel("Nombre de logements (parc total)", fontsize=9, color=MPL_INK)
    for spine in ("top", "right", "left"):
        ax.spines[spine].set_visible(False)
    ax.tick_params(axis="x", labelsize=8)

    # étiquettes valeur + %
    for i in range(len(communes)):
        t = totals[i]
        ax.text(rp[i] / 2, i, f"{rp[i]}\n{pct(rp[i], t):.0f}%",
                ha="center", va="center", color="white", fontsize=8, fontweight="bold")
        ax.text(rp[i] + rs[i] / 2, i, f"{rs[i]}\n{pct(rs[i], t):.0f}%",
                ha="center", va="center", color="white", fontsize=8, fontweight="bold")
        ax.text(rp[i] + rs[i] + vac[i] / 2, i, f"{vac[i]}\n{pct(vac[i], t):.0f}%",
                ha="center", va="center", color="white", fontsize=7.5, fontweight="bold")
        ax.text(t + 12, i, f"total {t}", ha="left", va="center",
                fontsize=8, color=MPL_GREY)

    ax.set_xlim(0, max(totals) * 1.12)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.42), ncol=3,
              fontsize=7.5, frameon=False)
    fig.tight_layout()
    fig.savefig(CH1, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def make_chart_taux():
    """Graphique 2 : taux de logements non occupés à l'année vs Gard & France."""
    labels = ["Lasalle", "Saint-Jean-\ndu-Gard", "Gard", "France"]
    vals = [TAUX["Lasalle"], TAUX["Saint-Jean-du-Gard"], TAUX["Gard"], TAUX["France"]]
    cols = [MPL_VAC, MPL_RS, MPL_GREY, MPL_GREY]

    fig, ax = plt.subplots(figsize=(7.2, 3.1), dpi=200)
    bars = ax.bar(labels, vals, color=cols, width=0.6)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.set_ylabel("Part des logements non occupés\nà l'année (%)", fontsize=9)
    ax.set_ylim(0, max(vals) * 1.25)
    ax.tick_params(axis="x", labelsize=9)
    ax.tick_params(axis="y", labelsize=8)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.8, f"{v:.1f} %",
                ha="center", va="bottom", fontsize=9.5, fontweight="bold")
    # ligne repère France
    ax.axhline(TAUX["France"], color=MPL_INK, lw=0.8, ls="--", alpha=0.5)
    ax.text(3.45, TAUX["France"] + 0.4, "moyenne France",
            ha="right", va="bottom", fontsize=7.5, color=MPL_INK, alpha=0.7)
    fig.tight_layout()
    fig.savefig(CH2, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ================================================================ STYLES
styles = getSampleStyleSheet()


def S(name, **kw):
    kw.setdefault("parent", styles["Normal"])
    return ParagraphStyle(name, **kw)


st_title = S("t", fontName="Helvetica-Bold", fontSize=19, leading=22, textColor=INK)
st_subtitle = S("st", fontName="Helvetica", fontSize=10.5, leading=14, textColor=GREEN)
st_kicker = S("k", fontName="Helvetica-Bold", fontSize=8.5, leading=11,
              textColor=GREEN, spaceAfter=2)
st_h = S("h", fontName="Helvetica-Bold", fontSize=13, leading=16, textColor=GREEN,
         spaceBefore=12, spaceAfter=5)
st_body = S("b", fontName="Helvetica", fontSize=9.7, leading=14, alignment=TA_JUSTIFY,
            textColor=INK, spaceAfter=5)
st_body_l = S("bl", parent=st_body, alignment=TA_LEFT)
st_li = S("li", parent=st_body, leftIndent=12, bulletIndent=2, spaceAfter=3)
st_small = S("sm", fontName="Helvetica", fontSize=7.6, leading=10, textColor=GREY)
st_source = S("src", fontName="Helvetica", fontSize=8, leading=11.5, textColor=GREY,
              leftIndent=10, bulletIndent=0)
st_box_lbl = S("blb", fontName="Helvetica", fontSize=8.2, leading=10.5, textColor=INK,
               alignment=TA_CENTER)
st_caption = S("cap", fontName="Helvetica-Oblique", fontSize=8, leading=11,
               textColor=GREY, spaceBefore=2, spaceAfter=8)


# ================================================================ COMPOSANTS
def keyfig_box(value, label, color=RED):
    p_val = Paragraph(value, S("kv", fontName="Helvetica-Bold", fontSize=21,
                               leading=23, textColor=color, alignment=TA_CENTER))
    p_lbl = Paragraph(label, st_box_lbl)
    t = Table([[p_val], [p_lbl]], colWidths=[52 * mm], rowHeights=[13 * mm, 13 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SAND),
        ("BOX", (0, 0), (-1, -1), 0.8, SAND_BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, 0), 6),
        ("BOTTOMPADDING", (0, 1), (-1, 1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def three_key_figures():
    boxes = [
        keyfig_box("38 %", "des logements de <b>Lasalle</b> ne sont pas occupés à l'année "
                           "(résidences secondaires + vacants)", RED),
        keyfig_box("28 %", "des logements de <b>Saint-Jean-du-Gard</b> ne sont pas "
                           "occupés à l'année", colors.HexColor("#B5701F")),
        keyfig_box("≈ 18 %", "moyenne nationale&nbsp;: les deux communes sont très "
                            "au-dessus", GREEN),
    ]
    t = Table([boxes], colWidths=[58 * mm, 58 * mm, 58 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def comparison_table():
    head = ["", "Lasalle", "Saint-Jean-\ndu-Gard", "Gard", "France"]
    L, S2 = DATA["Lasalle"], DATA["Saint-Jean-du-Gard"]
    rows = [
        head,
        ["Logements (parc total)", f"{L['total']:,}".replace(",", " "),
         f"{S2['total']:,}".replace(",", " "), "451 147", "37,8 M"],
        ["Résidences principales", f"{L['rp']} ({pct(L['rp'],L['total']):.1f} %)",
         f"{S2['rp']} ({pct(S2['rp'],S2['total']):.1f} %)", "79,2 %", "82 %"],
        ["Résidences secondaires / occ.", f"{L['rs']} ({pct(L['rs'],L['total']):.1f} %)",
         f"{S2['rs']} ({pct(S2['rs'],S2['total']):.1f} %)", "12,6 %", "10 %"],
        ["Logements vacants", f"{L['vac']} ({pct(L['vac'],L['total']):.1f} %)",
         f"{S2['vac']} ({pct(S2['vac'],S2['total']):.1f} %)", "8,2 %", "8 %"],
        ["NON occupés à l'année", f"{L['rs']+L['vac']} ({TAUX['Lasalle']:.1f} %)",
         f"{S2['rs']+S2['vac']} ({TAUX['Saint-Jean-du-Gard']:.1f} %)",
         f"{TAUX['Gard']:.1f} %", f"{TAUX['France']:.1f} %"],
        ["Revenu médian disponible /UC", "19 850 €", "21 770 €", "—", "—"],
        ["Logt HLM (part des rés. princ.)", "5,6 %", "3,3 %", "—", "≈ 17 %*"],
    ]

    cell_style = S("cell", fontName="Helvetica", fontSize=8.3, leading=10, textColor=INK)
    cell_b = S("cellb", fontName="Helvetica-Bold", fontSize=8.3, leading=10, textColor=INK)
    head_style = S("ch", fontName="Helvetica-Bold", fontSize=8.4, leading=10,
                   textColor=colors.white, alignment=TA_CENTER)
    data = []
    for i, r in enumerate(rows):
        new = []
        for j, c in enumerate(r):
            # virgule décimale française (sauf en-tête)
            if i > 0 and j > 0:
                c = str(c).replace(".", ",")
            if i == 0:
                new.append(Paragraph(str(c), head_style))
            elif j == 0:
                new.append(Paragraph(str(c), cell_b if i == 5 else cell_style))
            else:
                stl = cell_b if i == 5 else cell_style
                new.append(Paragraph(str(c), S("cc", parent=stl, alignment=TA_CENTER)))
        data.append(new)

    t = Table(data, colWidths=[46 * mm, 31 * mm, 31 * mm, 24 * mm, 24 * mm])
    ts = [
        ("BACKGROUND", (0, 0), (-1, 0), GREEN),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor("#D9D9D9")),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, GREEN),
        ("BACKGROUND", (0, 5), (-1, 5), GREEN_L),   # ligne NON occupés
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#CFCFCF")),
    ]
    for i in range(1, len(rows)):
        if i % 2 == 0 and i != 5:
            ts.append(("BACKGROUND", (0, i), (-1, i), GREY_L))
    t.setStyle(TableStyle(ts))
    return t


# ================================================================ DOCUMENT
def header_footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(GREEN)
    canvas.rect(0, 0, w, 6 * mm, stroke=0, fill=1)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(18 * mm, 2 * mm, "Association Cévennes 2050")
    canvas.drawRightString(w - 18 * mm, 2 * mm,
                           "Plaidoyer logement — Lasalle & Saint-Jean-du-Gard")
    canvas.drawCentredString(w / 2, 2 * mm, "%d" % doc.page)
    if doc.page > 1:
        canvas.setStrokeColor(SAND_BORDER)
        canvas.setLineWidth(0.6)
        canvas.line(18 * mm, h - 14 * mm, w - 18 * mm, h - 14 * mm)
        canvas.setFillColor(GREY)
        canvas.setFont("Helvetica", 7.5)
        canvas.drawString(18 * mm, h - 12 * mm, "CÉVENNES 2050")
    canvas.restoreState()


def build():
    make_chart_parc()
    make_chart_taux()

    doc = BaseDocTemplate(
        OUT, pagesize=A4,
        leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=16 * mm, bottomMargin=12 * mm,
        title="Plaidoyer logement — Cévennes 2050",
        author="Association Cévennes 2050",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin,
                  doc.width, doc.height, id="main")
    doc.addPageTemplates([PageTemplate(id="all", frames=[frame],
                                       onPage=header_footer)])

    el = []
    content_w = doc.width

    # ---- EN-TÊTE (logo + titre)
    logo = Image(LOGO, width=30 * mm, height=30 * mm)
    title_block = [
        Paragraph("ASSOCIATION CÉVENNES 2050", st_kicker),
        Paragraph("Le logement confisqué&nbsp;?", st_title),
        Paragraph("Plus d'un tiers du parc de Lasalle et de Saint-Jean-du-Gard "
                  "n'est pas occupé à l'année. État des lieux chiffré et leviers "
                  "d'action pour la commune.", st_subtitle),
    ]
    tb = Table([[logo, title_block]], colWidths=[34 * mm, content_w - 34 * mm])
    tb.setStyle(TableStyle([
        ("VALIGN", (0, 0), (0, 0), "MIDDLE"),
        ("VALIGN", (1, 0), (1, 0), "MIDDLE"),
        ("LEFTPADDING", (1, 0), (1, 0), 6),
        ("LEFTPADDING", (0, 0), (0, 0), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    el.append(tb)
    el.append(Spacer(1, 4))
    el.append(HRFlowable(width="100%", thickness=1.4, color=GREEN,
                         spaceBefore=4, spaceAfter=2))
    el.append(Paragraph("Note à l'attention de l'élu·e en charge du logement — "
                        "Données INSEE, recensement RP2023 (géographie 2025). "
                        "Document factuel, à vocation de plaidoyer.", st_small))
    el.append(Spacer(1, 8))

    # ---- LE CONSTAT EN UN COUP D'ŒIL
    el.append(Paragraph("Le constat en un coup d'œil", st_h))
    el.append(three_key_figures())
    el.append(Spacer(1, 8))
    el.append(Paragraph(
        "Sur nos deux communes, <b>923 logements sur 2 898</b> — soit près d'un tiers "
        "du parc — ne sont pas occupés à l'année&nbsp;: ce sont des résidences "
        "secondaires, des meublés de tourisme ou des logements vacants. Pendant ce "
        "temps, l'offre de logements permanents abordables reste sous tension "
        "(faible part de logement social, revenus médians inférieurs aux moyennes, "
        "taux de pauvreté élevé à Saint-Jean-du-Gard). Ce déséquilibre n'est pas une "
        "fatalité&nbsp;: la commune dispose de leviers concrets, détaillés en fin de note.",
        st_body))
    el.append(Spacer(1, 4))

    # ---- TABLEAU COMPARATIF
    el.append(Paragraph("Tableau comparatif", st_h))
    el.append(comparison_table())
    el.append(Paragraph(
        "Sources&nbsp;: INSEE, Dossier complet (recensement RP2023, géographie au "
        "01/01/2025) pour Lasalle (30140), Saint-Jean-du-Gard (30269) et le Gard&nbsp;; "
        "INSEE Focus n°309 pour la France (1<super>er</super> janvier 2023, hors Mayotte). "
        "Revenu médian&nbsp;: dispositif Filosofi. (*) Repère national indicatif de la "
        "part du parc locatif social.", st_caption))

    el.append(PageBreak())

    # ---- GRAPHIQUE 1
    el.append(Paragraph("Comment se répartit le parc de logements&nbsp;?", st_h))
    el.append(Image(CH1, width=content_w, height=content_w * 0.40))
    el.append(Paragraph(
        "À Lasalle, près d'un logement sur trois est une résidence secondaire (30,7 %). "
        "À Saint-Jean-du-Gard, le poids des logements vacants est particulièrement "
        "élevé (14,1 %, soit 265 logements), au-dessus de la moyenne du Gard (8,2 %) "
        "et de la France (8 %). Source&nbsp;: INSEE, RP2023.", st_caption))

    # ---- GRAPHIQUE 2
    el.append(Paragraph("Un parc nettement plus « inoccupé » qu'ailleurs", st_h))
    el.append(Image(CH2, width=content_w * 0.86, height=content_w * 0.86 * 0.43))
    el.append(Paragraph(
        "Part des logements non occupés à l'année (résidences secondaires et "
        "occasionnelles + logements vacants). Lasalle (38,2 %) et Saint-Jean-du-Gard "
        "(28,4 %) dépassent largement la moyenne du Gard (20,8 %) et la moyenne "
        "nationale (≈ 18 %). Source&nbsp;: INSEE, RP2023 et Focus n°309.", st_caption))

    el.append(Spacer(1, 4))

    # ---- MISE EN PERSPECTIVE MARCHÉ
    el.append(Paragraph("Mise en perspective&nbsp;: un marché tendu pour les habitants permanents",
                        st_h))
    el.append(Paragraph(
        "L'abondance de logements non occupés à l'année coexiste avec une difficulté "
        "réelle à se loger durablement. Le revenu médian disponible reste modeste "
        "(<b>19 850 €</b>/an par unité de consommation à Lasalle, <b>21 770 €</b> à "
        "Saint-Jean-du-Gard, Filosofi), et le taux de pauvreté atteint <b>25 %</b> à "
        "Saint-Jean-du-Gard. Dans le même temps, l'offre locative sociale est très "
        "réduite&nbsp;: seulement <b>5,6 %</b> des résidences principales à Lasalle et "
        "<b>3,3 %</b> à Saint-Jean-du-Gard relèvent du parc HLM, loin du repère "
        "national (≈ 17 %). La demande de résidences secondaires et de meublés "
        "touristiques tire par ailleurs les prix de l'immobilier vers le haut, les "
        "décorrélant des revenus locaux — un phénomène bien documenté dans les "
        "Cévennes. Les prix réels de transaction peuvent être objectivés commune par "
        "commune via la base publique <b>DVF</b> (demandes de valeurs foncières), à "
        "privilégier sur les estimations d'agrégateurs, peu fiables en milieu rural.",
        st_body))

    el.append(Spacer(1, 2))
    # ---- ANGLE MORT MEUBLÉS
    el.append(Paragraph("L'angle mort&nbsp;: les meublés de tourisme", st_h))
    el.append(Paragraph(
        "Le recensement INSEE classe un logement loué en meublé de tourisme tantôt en "
        "« résidence secondaire », tantôt en « logement vacant » selon les cas&nbsp;: "
        "il ne fournit pas de comptage spécifique des meublés type Airbnb par commune. "
        "Le nombre exact de meublés touristiques n'est donc pas une donnée publique "
        "directe. Il peut toutefois être objectivé localement grâce au <b>registre des "
        "déclarations en mairie</b>, désormais renforcé par la loi n°2024-1039 du "
        "19 novembre 2024 (dite « loi Le Meur »), qui élargit les pouvoirs des communes "
        "en matière d'enregistrement, de quotas et de changement d'usage. La part "
        "élevée de résidences secondaires constitue, à ce stade, le meilleur indicateur "
        "indirect de la pression touristique sur le logement.", st_body))

    el.append(Spacer(1, 2))
    # ---- TENDANCE
    el.append(Paragraph("Une tendance qui ne se corrige pas d'elle-même", st_h))
    el.append(Paragraph(
        "L'évolution récente confirme le déséquilibre. À Lasalle, entre les recensements "
        "2017 et 2023, le parc a gagné <b>57 logements</b> (de 960 à 1 017)&nbsp;: sur ce "
        "total, <b>+23 résidences secondaires</b> et <b>+12 logements vacants</b>, pour "
        "seulement <b>+22 résidences principales</b>. Autrement dit, plus de la moitié des "
        "logements nouvellement comptabilisés n'alimentent pas l'habitat permanent. Sans "
        "intervention publique, la dynamique du marché tend à reproduire, voire à "
        "accentuer, ce déséquilibre. Source&nbsp;: INSEE, RP2017 et RP2023.", st_body))

    el.append(Spacer(1, 6))

    # ---- LIMITES MÉTHODO
    el.append(Paragraph("Honnêteté méthodologique&nbsp;: ce que disent — et ne disent pas — les chiffres",
                        st_h))
    for b in [
        "<b>Petits effectifs.</b> Lasalle et Saint-Jean-du-Gard sont de petites communes&nbsp;: "
        "une variation de quelques dizaines de logements modifie sensiblement les "
        "pourcentages. Les données sont des estimations de recensement, à manier comme "
        "des ordres de grandeur robustes plutôt que comme des décomptes exacts.",
        "<b>Millésime.</b> Les chiffres communaux retenus sont issus du recensement "
        "RP2023 (géographie au 01/01/2025). Le repère national provient d'INSEE Focus "
        "n°309 (parc au 1<super>er</super> janvier 2023). Les comparaisons mélangent donc "
        "des sources cohérentes mais de portée différente.",
        "<b>Meublés touristiques.</b> Aucun comptage public commune par commune&nbsp;; "
        "estimation indirecte via les résidences secondaires et, à terme, via le "
        "registre de déclaration en mairie.",
        "<b>Logements vacants.</b> Leur localisation nominative n'est pas publique&nbsp;: "
        "elle nécessite une convention <b>LOVAC / CEREMA</b> (plateforme « Zéro Logement "
        "Vacant »), ouverte aux collectivités.",
        "<b>Prix immobiliers.</b> La base DVF donne les transactions réelles mais, vu le "
        "faible nombre de ventes annuelles, les médianes au m² sont volatiles d'une "
        "année à l'autre&nbsp;; les estimations d'agrégateurs sont peu fiables ici.",
    ]:
        el.append(Paragraph(b, st_li, bulletText="•"))
    el.append(Spacer(1, 4))

    # ---- PROPOSITIONS
    el.append(Paragraph("Cinq leviers actionnables au niveau communal", st_h))
    props = [
        ("1. Enregistrer et encadrer les meublés de tourisme",
         "Mettre en place l'enregistrement obligatoire avec numéro de déclaration, "
         "instaurer si besoin un régime d'autorisation de changement d'usage et des "
         "quotas, en s'appuyant sur la loi « Le Meur » (2024). Objectif&nbsp;: connaître "
         "le parc réel et préserver l'habitat permanent."),
        ("2. Mobiliser les logements vacants",
         "Conventionner avec le CEREMA pour accéder aux données LOVAC via la plateforme "
         "« Zéro Logement Vacant », contacter les propriétaires, orienter vers les aides "
         "à la rénovation et le conventionnement. 342 logements vacants recensés sur les "
         "deux communes&nbsp;: un gisement immédiat."),
        ("3. Développer une offre locative à l'année abordable",
         "Soutenir la production de logement social et de baux réels solidaires, mobiliser "
         "l'EPF Occitanie et les bailleurs sociaux. La part HLM (3–6 % des résidences "
         "principales) laisse une marge importante."),
        ("4. Fiscalité et levier foncier",
         "Activer les outils fiscaux à disposition (majoration de la taxe d'habitation sur "
         "les résidences secondaires en zone tendue lorsqu'elle est applicable, taxe sur "
         "les logements vacants), et utiliser le droit de préemption pour capter du foncier "
         "à vocation d'habitat permanent."),
        ("5. S'inspirer d'un précédent cévenol transposable",
         "Au Pont-de-Montvert (Lozère), commune où les résidences secondaires dépassent "
         "60 %, la municipalité a créé des logements locatifs sociaux pour maintenir une "
         "population à l'année face à la pression touristique. Un modèle d'action publique "
         "locale directement transposable."),
    ]
    for titre, txt in props:
        el.append(Paragraph(titre, S("ph", fontName="Helvetica-Bold", fontSize=10,
                                     leading=13, textColor=INK, spaceBefore=5, spaceAfter=1)))
        el.append(Paragraph(txt, st_body))

    el.append(Spacer(1, 6))
    el.append(HRFlowable(width="100%", thickness=0.8, color=SAND_BORDER, spaceAfter=4))

    # ---- SOURCES
    el.append(Paragraph("Sources", st_h))
    srcs = [
        "INSEE — Dossier complet, Lasalle (30140), recensement RP2023&nbsp;: "
        "insee.fr/fr/statistiques/2011101?geo=COM-30140",
        "INSEE — Dossier complet, Saint-Jean-du-Gard (30269), RP2023&nbsp;: "
        "insee.fr/fr/statistiques/2011101?geo=COM-30269",
        "INSEE — Dossier complet, département du Gard (30), RP2023&nbsp;: "
        "insee.fr/fr/statistiques/2011101?geo=DEP-30",
        "INSEE Focus n°309 — « 37,8 millions de logements en France au "
        "1<super>er</super> janvier 2023 »&nbsp;: insee.fr/fr/statistiques/7700305",
        "CEREMA / LOVAC — plateforme « Zéro Logement Vacant »&nbsp;: "
        "zerologementvacant.beta.gouv.fr",
        "DGFiP — Demandes de valeurs foncières (DVF)&nbsp;: app.dvf.etalab.gouv.fr",
        "Loi n°2024-1039 du 19 novembre 2024 (meublés de tourisme, « loi Le Meur »)&nbsp;: "
        "legifrance.gouv.fr",
    ]
    for s in srcs:
        el.append(Paragraph(s, st_source, bulletText="—"))

    el.append(Spacer(1, 8))
    el.append(Paragraph(
        "Document établi par l'association Cévennes 2050 à partir de données publiques. "
        "Les chiffres sont datés et sourcés&nbsp;; les limites statistiques sont "
        "signalées ci-dessus. Reproduction et diffusion libres.", st_small))

    doc.build(el)
    for f in (CH1, CH2):
        try:
            os.remove(f)
        except OSError:
            pass
    print("OK ->", OUT)


if __name__ == "__main__":
    build()
