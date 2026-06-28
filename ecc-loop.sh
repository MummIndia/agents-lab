#!/usr/bin/env bash
set -euo pipefail
MAX_RUNS="${1:-3}"
GOAL="${GOAL:-GOAL.md}"
BRANCH="${BRANCH:-agent/auto}"
NOTES="SHARED_TASK_NOTES.md"

command -v claude >/dev/null 2>&1 || { echo "ERREUR: claude introuvable."; exit 1; }
[ -d .git ] || { echo "ERREUR: pas un depot git. Lance: git init"; exit 1; }
[ -f "$GOAL" ] || { echo "ERREUR: objectif $GOAL introuvable."; exit 1; }

git config user.email >/dev/null 2>&1 || git config user.email "agent@sandbox.local"
git config user.name  >/dev/null 2>&1 || git config user.name  "agent-sandbox"

echo "Bascule sur la branche $BRANCH..."
git checkout -B "$BRANCH" >/dev/null 2>&1
[ -f "$NOTES" ] || printf '# Notes partagees entre iterations\n' > "$NOTES"

for i in $(seq 1 "$MAX_RUNS"); do
  if [ -f STOP ]; then echo "STOP detecte -> arret."; rm -f STOP; break; fi
  echo ""
  echo "=== Iteration $i / $MAX_RUNS ==="
  PROMPT="Objectif global : lis le fichier $GOAL.
Contexte des iterations precedentes : lis le fichier $NOTES.
Travaille UNE etape concrete vers l'objectif. Ecris/edite le code, lance les tests.
Mets a jour $NOTES (fait / reste a faire).
Si l'objectif est ENTIEREMENT atteint et verifie, ecris sur une ligne seule: OBJECTIF_ATTEINT
Ne cree pas de docs inutiles. Ne fais AUCUNE operation git. Reste dans /workspace."
  set +e
  OUT="$(claude -p "$PROMPT" --dangerously-skip-permissions --allowedTools "Read,Write,Edit,Bash,Grep,Glob" 2>&1)"
  set -e
  echo "$OUT" | tee "loop-iteration-$i.log"
  if echo "$OUT" | grep -q "OBJECTIF_ATTEINT"; then
    git add -A; git commit -m "agent: iteration $i (objectif atteint)" --allow-empty >/dev/null
    echo "Objectif atteint a l'iteration $i."; break
  fi
  git add -A; git commit -m "agent: iteration $i" --allow-empty >/dev/null
  echo "Iteration $i sauvegardee."
done

echo ""
echo "Inspecter : git log --oneline ; git diff main..$BRANCH"
echo "Garder    : git checkout main && git merge $BRANCH"
echo "Jeter     : git checkout main && git branch -D $BRANCH"
