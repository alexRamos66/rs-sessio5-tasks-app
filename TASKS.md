# TASKS.md - Tasks_app

## Increment 1: MVP - Creació i Llistat de Tasques
Objectiu: Tenir una versió CLI funcional per afegir i consultar tasques en JSON.

### Tasques d'Execució:
- [x] Tasca 1.1: Crear estructura de directoris (`src/`, `test/`, `data/`) i fitxer `data/tasks.json` inicial. (Requisits RF-01 i RF-02) 
- [x] Tasca 1.2: Implementar model de dades `Task` a `src/models.py` amb mètodes de serialització JSON.
- [x] Tasca 1.3: Desenvolupar Tasks_app a `src/tasks_app.py` amb opcions `add` i `list`.(Requisits RF-03 i RF-04)
- [x] Tasca 1.4: Crear test d'integració a `test/test_tasks_app.py` segons els escenaris GS-01, GS-02 i GS-03.
- [x] Tasca 1.5: Validar execució amb OpenCode i verificar que tots els tests passen (`python3 -m pytest test`).
- [x] Tasca 1.6: Ampliar `test/test_tasks_app.py` amb els escenaris GS-04 (Requisit RF-02) i GS-05 (Requisit RF-03), i verificar que tots els tests passen (`python3 -m pytest test`).

## Increment 2: Data límit, edició, completar i indicadors
Objectiu: Ampliar la CLI amb data límit, modificació de tasques, comandament de completar i avisos `[CADUCADA]` / `[URGENT]` al llistat (SPECIFICATIONS v2.0).

### Tasques d'Execució:
- [x] Tasca 2.1: Ampliar el model `Task` a `src/models.py` amb el camp opcional `data_limit` (per defecte `None`), serialització JSON i compatibilitat amb registres antics sense el camp. (Model de dades v2.0)
- [x] Tasca 2.2: Afegir a `src/tasks_app.py` una funció que obtingui la data actual de la variable d'entorn `TASKS_AVUI` (format `AAAA-MM-DD`) o del rellotge del sistema. (Requisit RNF-01)
- [x] Tasca 2.3: Afegir l'opció `--due AAAA-MM-DD` al comandament `add`, amb validació de la data i el missatge d'error corresponent. (Requisits RF-05 i RF-06)
- [x] Tasca 2.4: Crear les proves dels escenaris GS-06 i GS-07 a `test/test_tasks_app.py` i verificar que passen. (Requisits RF-05 i RF-06)
- [x] Tasca 2.5: Implementar el comandament `done --id <ID>`, amb el missatge d'error per a ID inexistent. (Requisits RF-10 i RF-09)
- [x] Tasca 2.6: Crear les proves dels escenaris GS-11 i GS-12 i verificar que passen. (Requisits RF-10 i RF-09)
- [x] Tasca 2.7: Implementar el comandament `edit --id <ID>` amb les opcions `--title`, `--subject`, `--due` i `--status`, reutilitzant la validació de data i amb validació de l'estat i de l'ID. (Requisits RF-07, RF-08 i RF-09)
- [ ] Tasca 2.8: Crear les proves dels escenaris GS-08, GS-09 i GS-10 i verificar que passen. (Requisits RF-07, RF-08 i RF-09)
- [ ] Tasca 2.9: Modificar `list` perquè mostri la data límit (` - límit: AAAA-MM-DD`) de les tasques que en tenen, mantenint el format de la v1.0 per a les que no en tenen. (Requisit RF-11)
- [ ] Tasca 2.10: Afegir a `list` els indicadors `[CADUCADA]` i `[URGENT]` segons les regles de data i d'estat. (Requisits RF-12, RF-13 i RF-14)
- [ ] Tasca 2.11: Crear les proves dels escenaris GS-13, GS-14, GS-15, GS-16 i GS-17 (amb `TASKS_AVUI=2026-11-24`) i verificar que passen. (Requisits RF-11, RF-12, RF-13, RF-14 i RNF-01)
- [ ] Tasca 2.12: Executar tots els tests (`python3 -m pytest test`) i comprovar que els escenaris GS-01 a GS-05 de la v1.0 continuen passant (no regressió).
