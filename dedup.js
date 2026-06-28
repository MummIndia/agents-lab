'use strict';

/**
 * Supprime les doublons d'email d'une liste de contacts.
 * La comparaison d'email est insensible a la casse.
 * Le premier contact rencontre pour un email donne est conserve.
 *
 * @param {Array<{nom: string, prenom: string, email: string}>} list
 * @returns {Array<{nom: string, prenom: string, email: string}>}
 */
function dedupeContacts(list) {
  if (!Array.isArray(list)) {
    return [];
  }

  const seen = new Set();
  const result = [];

  for (const contact of list) {
    if (!contact || typeof contact.email !== 'string') {
      continue;
    }
    const key = contact.email.trim().toLowerCase();
    if (seen.has(key)) {
      continue;
    }
    seen.add(key);
    result.push(contact);
  }

  return result;
}

module.exports = { dedupeContacts };
