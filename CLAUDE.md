# Consignes de travail

Ce dépôt produit des documents argumentés à partir de données publiques :
des chiffres, des sources, des dates. Une erreur y coûte plus cher qu'ailleurs,
parce qu'un document remis à un élu ne se corrige pas après coup.

Ces consignes sont écrites autour de ce qui rate en pratique, pas autour de
bonnes intentions. Elles ralentissent volontairement le travail. Pour une tâche
triviale, garde ton jugement.

---

## Un chiffre sans source n'existe pas

C'est la règle qui prime sur toutes les autres.

- Aucune valeur ne doit apparaître dans un livrable sans qu'on puisse dire
  **d'où elle vient et de quand elle date**. Millésime compris : « INSEE RP2022 »
  n'est pas « INSEE ».
- Si un chiffre manque, il manque. On l'écrit. On ne comble pas un trou avec un
  ordre de grandeur plausible, et surtout pas avec une valeur reconstituée de
  mémoire.
- Une estimation reste une estimation, et elle est présentée comme telle, avec
  sa méthode.
- Ce qui est calculé se vérifie : les sous-totaux doivent redonner le total.
  Vérifie l'arithmétique avant de livrer, pas après.
- Les limites d'une donnée font partie de la donnée. Un échantillon faible, une
  série volatile, une catégorie qui recouvre mal la réalité : ça se signale dans
  le document, ça ne s'efface pas parce que ça affaiblit le propos.

## Dire ce qu'on ne sait pas

Le silence coûte plus cher que la question.

- Une consigne ambiguë se clarifie **avant** d'agir, pas après avoir produit
  quelque chose qu'il faudra jeter.
- Quand plusieurs lectures sont possibles, expose-les et demande. Ne tranche pas
  discrètement en espérant tomber juste.
- Une hypothèse implicite est une erreur en attente. Énonce-la.
- Si une approche plus simple existe, dis-le, même si ce n'est pas ce qui a été
  demandé. Contredire est utile ; obéir en sachant que c'est bancal ne l'est pas.

## Le périmètre demandé, rien de plus

Chaque ligne produite doit pouvoir se rattacher à une demande explicite.

- Pas de fonctionnalité « tant qu'à faire ».
- Pas d'abstraction pour un cas unique, pas de configuration que personne n'a
  réclamée, pas de gestion d'erreur pour des situations impossibles.
- On ne réécrit pas du code ou du texte voisin parce qu'on le ferait autrement.
  On épouse le style existant.
- Du code mort repéré au passage se **signale**, il ne se supprime pas de sa
  propre initiative.
- Ce que tes propres modifications rendent inutile — un import, une variable —
  se nettoie. Ce qui était déjà là ne te regarde pas.

Un bon test : si cent lignes en valaient trente, recommence.

## Vérifier, pas supposer

« Ça devrait marcher » n'est pas un état d'avancement.

Une tâche floue se transforme d'abord en critère observable :

| Demande | Objectif vérifiable |
|---|---|
| « le tableau est faux » | isoler l'écart sur une ligne précise, puis montrer que la somme retombe juste |
| « ajouter les données 2023 » | chaque valeur ajoutée porte sa source et son millésime, et les séries restent comparables |
| « rendre le document plus lisible » | un critère choisi d'avance — nombre de pages, densité des tableaux — plutôt qu'une impression |

Pour une tâche en plusieurs temps, annonce le plan et **ce qui prouvera** chaque
étape. Un critère solide permet de travailler en autonomie ; un critère mou
(« que ce soit propre ») oblige à revenir demander à chaque pas.

Ne déclare pas terminé ce que tu n'as pas constaté. Si une vérification n'a pas
pu être faite, dis laquelle et pourquoi.

---

**Ces consignes fonctionnent si** : les questions arrivent avant la production
et non après l'erreur, les diffs ne contiennent que ce qui était demandé, et
aucun chiffre publié ne reste orphelin de sa source.
