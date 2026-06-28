# Notes partagees entre iterations

## Objectif
Produire `Plaidoyer_logement_Cevennes2050.pdf` — plaidoyer graphique sourcé (4–6 pages)
sur les logements non occupés à l'année à **Lasalle** et **Saint-Jean-du-Gard**, à
destination d'un élu, à l'image de l'association Cévennes 2050 (logo en en-tête).

## FAIT (itération 2 — 2026-06-28)
- Correction d'une **erreur de code INSEE** : Lasalle = **30140** (et non 30139, qui est
  Lanuéjols). Code postal de Lasalle = 30460 (à ne pas confondre).
- Données INSEE collectées et vérifiées via le Dossier complet (millésime **RP2023**,
  géographie au 01/01/2025). Arithmétique re-vérifiée (somme catégories = total). ✓

### Données vérifiées (à utiliser telles quelles — NE PAS réinventer)

**Lasalle (INSEE 30140) — RP2023**
- Total logements : 1 017
- Résidences principales : 628 (61,8 %)
- Résidences secondaires + occasionnels : 312 (30,7 %)
- Logements vacants : 77 (7,6 %)
- → Non occupés à l'année (RS + vacants) : 389 = **38,3 %**
- Population : 1 202 ; ménages : 628
- Logement HLM loué vide : 35 (5,6 % des RP)
- Revenu médian disponible (Filosofi) : 19 850 € ; taux de pauvreté : secret stat.
- Évolution 2017→2023 : total 960→1 017 ; RS 289→312 ; vacants 65→77

**Saint-Jean-du-Gard (INSEE 30269) — RP2023**
- Total logements : 1 881
- Résidences principales : 1 347 (71,6 %)
- Résidences secondaires + occasionnels : 269 (14,3 %)
- Logements vacants : 265 (14,1 %)
- → Non occupés à l'année (RS + vacants) : 534 = **28,4 %**
- Population : 2 586 ; ménages : 1 337
- Logement HLM loué vide : 45 (3,3 % des RP)
- Revenu médian disponible (Filosofi) : 21 770 € ; taux de pauvreté : 25,0 %

**Combiné (2 communes)** : total 2 898 ; non occupés à l'année 923 = **31,9 %**

**Références**
- France (1er janv. 2023, INSEE Focus 309, hors Mayotte) : RP 82 %, RS 10 %, vacants 8 %
  → non occupé à l'année ≈ **18 %**
- Gard (RP2023) : total 451 147 ; RP 79,2 %, RS 12,6 %, vacants 8,2 %
  → non occupé à l'année ≈ **20,8 %**

### Sources (URLs)
- INSEE Dossier complet Lasalle : https://www.insee.fr/fr/statistiques/2011101?geo=COM-30140
- INSEE Dossier complet Saint-Jean-du-Gard : https://www.insee.fr/fr/statistiques/2011101?geo=COM-30269
- INSEE Dossier complet Gard (DEP-30) : https://www.insee.fr/fr/statistiques/2011101?geo=DEP-30
- INSEE Focus 309 (parc France 2023) : https://www.insee.fr/fr/statistiques/7700305
- LOVAC/CEREMA & Zéro Logement Vacant : https://zerologementvacant.beta.gouv.fr/
- DVF (valeurs foncières) : https://app.dvf.etalab.gouv.fr/
- Loi « Le Meur » (meublés touristiques, 2024) : loi n° 2024-1039 du 19/11/2024 (legifrance.gouv.fr)

## FAIT (suite it.2) — OBJECTIF ATTEINT
- [x] PDF généré : `Plaidoyer_logement_Cevennes2050.pdf` (4 pages, ~150 Ko, PDF-1.4).
- [x] Script reproductible : `generate_pdf.py` (reportlab + matplotlib).
- [x] Contenu : en-tête logo + titre / 3 chiffres-clés / tableau comparatif (vs Gard
      & France) / graphique 1 (répartition parc) / graphique 2 (taux non-occupation) /
      mise en perspective marché (revenus, HLM, DVF) / angle mort meublés (loi Le Meur) /
      tendance 2017→2023 / limites méthodo / 5 leviers d'action / sources cliquables.
- [x] Vérifié visuellement page par page (rendu pdftoppm) : logo présent, mise en page
      propre, aucun débordement.
- [x] Arithmétique re-vérifiée par script : 628+312+77=1017 ; 1347+269+265=1881.
      **Correction d'un arrondi** : taux non-occupation Lasalle = **38,2 %** (et non 38,3 ;
      cohérent avec RP 61,8 %). Combiné = 31,8 %.
- [x] Typographie française (virgule décimale) appliquée au tableau.

## RESTE A FAIRE (améliorations optionnelles, non bloquantes)
- [ ] Affiner avec données DVF prix/m² réelles par commune si accessibles (actuellement
      traité qualitativement + renvoi à la base DVF, conformément aux limites du GOAL).
- [ ] Confirmer le millésime exact Filosofi du revenu médian (affiché « 2023 » par le
      dossier complet ; à recouper).
- [ ] Données d'évolution 2017→2023 pour Saint-Jean-du-Gard (seules celles de Lasalle
      ont été récupérées).

## NOTES METHODO
- Garder l'honnêteté statistique : petits effectifs, comptage Airbnb non public,
  DVF volatil, vacants nominatifs nécessitant convention LOVAC.
- Ne PAS confondre code INSEE et code postal pour Lasalle.
- Libs dispo : matplotlib 3.11.0, reportlab 5.0.0, PIL 12.2.0.
