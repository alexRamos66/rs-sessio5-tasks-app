# AGENTS.md — Directives per a OpenCode

## Entorn i Stack Tècnic
- Llenguatge: Python 3.11+
- Interfície: Línia de comandes (CLI) amb mòdul `argparse` o `cmd`  
- Manteniment de Dades: Fitxer JSON local (`data/tasks.json`)
- Dates: només la llibreria estàndard (`datetime`). Format `AAAA-MM-DD`.

## Comandes de Desenvolupament
- Executar aplicació: `python3 src/tasks_app.py`
- Exemples: `python3 src/tasks_app.py add --title "Pràctica 5" --subject RS --due 2026-12-15`
  `python3 src/tasks_app.py edit --id 1 --status completada` · `python3 src/tasks_app.py done --id 1`
- Executar tots els tests: `python3 -m pytest test`
- Executar test únic: `python3 -m pytest test/test_tasks_app.py`
- Provar amb una data fixa: `TASKS_AVUI=2026-11-24 python3 src/tasks_app.py list`

## Convencions de Codi
- Estil: PEP8.
- Idioma del codi i comentaris: Català (mantenir consistència en noms de variables).
- Els missatges per pantalla han de ser exactament els de `SPECIFICATIONS.md`.
- Els errors es mostren amb el text exacte de l'especificació i el programa acaba amb codi de sortida diferent de zero.
- Els tests que depenen de la data han de fixar `TASKS_AVUI`; mai han de dependre del rellotge real.
- Els tests han de treballar amb un fitxer de dades temporal, mai amb el `data/tasks.json` real.

## Regles de Gestió de Tasques (`TASKS.md`)
1. Llegeix `TASKS.md` i identifica la següent tasca amb estat `[ ]`.
2. Canvia l'estat de la tasca actual a `[/]` abans d'iniciar la codificació.
3. Executa ÚNICAMENT una sola tasca per torn.
4. Verifica que el codi compleixi els requisits i escenaris Gherkin de `SPECIFICATIONS.md`.
5. Quan estigui completada i verificada, canvia l'estat a `[x]`.
6. Atura't i demana confirmació a l'usuari abans de passar a la següent tasca.
7. No facis `git commit` ni `git push`: ho fa l'usuari.

## Restriccions de Desenvolupament
- No instal·lis llibreries externes no autoritzades.
- No modifiquis fitxers de configuració fora de `src/` i `test/`
- No modifiquis `SPECIFICATIONS.md`; només l'usuari l'edita. De `TASKS.md` només canvia els símbols d'estat.
- No esborris ni reescriguis `data/tasks.json` amb dades de prova.
- No trencis els escenaris GS-01 a GS-05 de la v1.0 (no regressió).
