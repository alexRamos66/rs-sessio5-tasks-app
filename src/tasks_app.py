"""Aplicació CLI per gestionar tasques acadèmiques."""

import argparse
import json
import os
from datetime import date, datetime
from pathlib import Path

try:
    from models import Task
except ImportError:
    from src.models import Task


RUTA_DADES = Path(__file__).resolve().parent.parent / "data" / "tasks.json"


def obtenir_data_actual():
    valor = os.environ.get("TASKS_AVUI")
    if valor is not None:
        try:
            return datetime.strptime(valor, "%Y-%m-%d").date()
        except ValueError:
            pass
    return date.today()


def carregar_tasques():
    RUTA_DADES.parent.mkdir(parents=True, exist_ok=True)
    if not RUTA_DADES.exists():
        desar_tasques([])
        return []
    try:
        dades = json.loads(RUTA_DADES.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        dades = []
    if not isinstance(dades, list):
        dades = []
    return [Task.from_dict(registre) for registre in dades]


def desar_tasques(tasques):
    RUTA_DADES.parent.mkdir(parents=True, exist_ok=True)
    contingut = json.dumps(
        [tasca.to_dict() for tasca in tasques], ensure_ascii=False, indent=2
    )
    RUTA_DADES.write_text(contingut + "\n", encoding="utf-8")


def afegir_tasca(titol, assignatura):
    tasques = carregar_tasques()
    nou_id = max((tasca.id for tasca in tasques), default=0) + 1
    tasques.append(Task(nou_id, titol, assignatura))
    desar_tasques(tasques)
    print(f"Tasca [ID: {nou_id}] creada amb èxit")


def llistar_tasques():
    tasques = carregar_tasques()
    if not tasques:
        print("Registre de tasques buit.")
        return
    for tasca in tasques:
        print(tasca)


def main():
    parser = argparse.ArgumentParser(description="Gestor de tasques acadèmiques.")
    subcomandes = parser.add_subparsers(dest="comanda", required=True)

    afegir = subcomandes.add_parser("add", help="Afegeix una nova tasca")
    afegir.add_argument("--title", required=True, help="Títol de la tasca")
    afegir.add_argument("--subject", required=True, help="Assignatura de la tasca")

    subcomandes.add_parser("list", help="Mostra totes les tasques")

    arguments = parser.parse_args()
    if arguments.comanda == "add":
        afegir_tasca(arguments.title, arguments.subject)
    elif arguments.comanda == "list":
        llistar_tasques()


if __name__ == "__main__":
    main()
