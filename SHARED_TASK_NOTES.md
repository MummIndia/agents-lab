# Notes partagees entre iterations

## Fait
- `dedup.js` cree : exporte `dedupeContacts(list)`, sans dependance externe.
  - Dedup par email insensible a la casse (trim + toLowerCase).
  - Conserve le premier contact rencontre pour chaque email.
  - Robuste : liste non-tableau -> `[]`, contacts sans email valide ignores.
- `dedup.test.js` cree avec `node:test` natif. 3 tests :
  - doublons d'email supprimes
  - casse ignoree
  - liste vide geree
- `node --test` -> 3 pass / 0 fail (vert).

## Reste a faire
- Rien. Objectif entierement atteint et verifie.
