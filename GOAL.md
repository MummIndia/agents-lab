# Objectif
Creer un petit utilitaire Node.js SANS dependance externe :
- un fichier dedup.js qui exporte une fonction dedupeContacts(list)
  prenant un tableau de contacts {nom, prenom, email} et renvoyant
  la liste sans doublons d'email (insensible a la casse).
- un fichier dedup.test.js utilisant le module natif node:test
  verifiant : doublons supprimes, casse ignoree, liste vide geree.

# Criteres de reussite
- la commande "node --test" passe au vert
- les doublons d'email et la casse sont bien geres
