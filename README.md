# agents-lab — plaidoyer documenté, produit en boucle

Atelier de production de documents de plaidoyer **chiffrés et sourcés**, pour
l'association **Cévennes 2050**.

Le principe : on écrit un objectif précis et vérifiable dans `GOAL.md`, puis un
agent travaille par itérations jusqu'à l'atteindre, en gardant ses notes d'une
passe à l'autre. Ce qui sort n'est pas une opinion mise en forme, mais un
document où chaque chiffre porte sa source et son millésime.

**Premier livrable :** `Plaidoyer_logement_Cevennes2050.pdf` — l'ampleur des
logements non occupés à l'année à Lasalle et Saint-Jean-du-Gard (Gard), à partir
des données INSEE, avec des leviers d'action communaux.

## Contenu

| Fichier | Rôle |
|---|---|
| `GOAL.md` | l'objectif : but, public visé, sources admises, critères de réussite, limites connues |
| `CLAUDE.md` | les règles de travail de l'agent — la première étant qu'un chiffre sans source n'existe pas |
| `ecc-loop.sh` | la boucle : relance l'agent sur l'objectif jusqu'à `MAX_RUNS`, sur une branche dédiée |
| `generate_pdf.py` | la mise en forme du document (matplotlib) |
| `Plaidoyer_logement_Cevennes2050.pdf` | le livrable |

## Réutiliser ce travail

**C'est fait pour.** Si votre commune connaît la même tension — beaucoup de
résidences secondaires ou de logements vacants, peu de logement permanent
abordable — le plus utile n'est pas le PDF lui-même mais la méthode :

1. Reprenez `GOAL.md` et remplacez les communes, les codes INSEE et les chiffres.
2. Gardez les **critères de réussite** : c'est ce qui empêche un document de
   plaidoyer de dériver vers l'approximation.
3. Gardez surtout la section « limites connues ». Un document qui signale ses
   propres angles morts se défend mieux devant un élu qu'un document qui n'en a
   apparemment aucun.

Les sources utilisées (INSEE, DVF/DGFiP, LOVAC/CEREMA) sont publiques et
couvrent toutes les communes françaises.

## Licence

Deux licences, selon la nature des fichiers :

- **Documents, notes et livrables** (`*.md`, `*.pdf`) —
  [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.fr), texte
  intégral dans [`LICENSE`](LICENSE).
  Vous pouvez les reprendre, les adapter et les diffuser, y compris à des fins
  commerciales, à condition de créditer Cévennes 2050 et d'indiquer si vous
  avez apporté des modifications.

- **Scripts** (`ecc-loop.sh`, `generate_pdf.py`) —
  [MIT](LICENSE-MIT). Faites-en ce que vous voulez.

**Exception : le logo et le nom « Cévennes 2050 » ne sont pas couverts.** Ils
identifient l'association et restent sa propriété. Reprenez la méthode et les
données, pas la signature — remplacez le logo par le vôtre.

Les données INSEE, DVF et CEREMA citées relèvent de leurs licences respectives
(licence ouverte Etalab pour l'essentiel) et restent attribuables à leurs
producteurs.
