'use strict';

const test = require('node:test');
const assert = require('node:assert');
const { dedupeContacts } = require('./dedup');

test('supprime les doublons d\'email', () => {
  const list = [
    { nom: 'Dupont', prenom: 'Jean', email: 'jean@example.com' },
    { nom: 'Dupond', prenom: 'Jeanne', email: 'jean@example.com' },
    { nom: 'Martin', prenom: 'Paul', email: 'paul@example.com' },
  ];
  const result = dedupeContacts(list);
  assert.strictEqual(result.length, 2);
  assert.strictEqual(result[0].prenom, 'Jean');
  assert.strictEqual(result[1].email, 'paul@example.com');
});

test('ignore la casse des emails', () => {
  const list = [
    { nom: 'A', prenom: 'a', email: 'Contact@Example.com' },
    { nom: 'B', prenom: 'b', email: 'contact@example.com' },
    { nom: 'C', prenom: 'c', email: 'CONTACT@EXAMPLE.COM' },
  ];
  const result = dedupeContacts(list);
  assert.strictEqual(result.length, 1);
  assert.strictEqual(result[0].nom, 'A');
});

test('gere une liste vide', () => {
  assert.deepStrictEqual(dedupeContacts([]), []);
});
