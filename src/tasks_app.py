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


def es_data_valida(text):
    if not isinstance(text, str):
        return False
    if len(text) != 10 or text[4] != "-" or text[7] != "-":
        return False
    try:
        date.fromisoformat(text)
    except ValueError:
        return False
    return True


def carregar_tasques(crear_fitxer=True):
    if not RUTA_DADES.exists():
        if crear_fitxer:
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


def afegir_tasca(titol, assignatura, data_limit=None):
    if data_limit is not None and not es_data_valida(data_limit):
        print("Error: data límit no vàlida (format esperat: AAAA-MM-DD)")
        raise SystemExit(1)
    tasques = carregar_tasques()
    nou_id = max((tasca.id for tasca in tasques), default=0) + 1
    tasques.append(Task(nou_id, titol, assignatura, data_limit=data_limit))
    desar_tasques(tasques)
    print(f"Tasca [ID: {nou_id}] creada amb èxit")


def completar_tasca(id):
    tasques = carregar_tasques(crear_fitxer=False)
    trobada = next((tasca for tasca in tasques if tasca.id == id), None)
    if trobada is None:
        print(f"Error: no existeix cap tasca amb ID {id}")
        raise SystemExit(1)
    trobada.estat = "completada"
    desar_tasques(tasques)
    print(f"Tasca [ID: {id}] completada")


def editar_tasca(id, titol=None, assignatura=None, data_limit=None, estat=None):
    if data_limit is not None and not es_data_valida(data_limit):
        print("Error: data límit no vàlida (format esperat: AAAA-MM-DD)")
        raise SystemExit(1)
    if estat is not None and estat not in ("pendent", "completada"):
        print("Error: estat no vàlid (valors permesos: pendent, completada)")
        raise SystemExit(1)
    tasques = carregar_tasques(crear_fitxer=False)
    trobada = next((tasca for tasca in tasques if tasca.id == id), None)
    if trobada is None:
        print(f"Error: no existeix cap tasca amb ID {id}")
        raise SystemExit(1)
    if titol is not None:
        trobada.titol = titol
    if assignatura is not None:
        trobada.assignatura = assignatura
    if data_limit is not None:
        trobada.data_limit = data_limit
    if estat is not None:
        trobada.estat = estat
    desar_tasques(tasques)
    print(f"Tasca [ID: {id}] modificada amb èxit")


def llistar_tasques():
    tasques = carregar_tasques()
    if not tasques:
        print("Registre de tasques buit.")
        return
    for tasca in tasques:
        linia = str(tasca)
        if tasca.data_limit is not None:
            linia += f" - límit: {tasca.data_limit}"
        print(linia)


def main():
    parser = argparse.ArgumentParser(description="Gestor de tasques acadèmiques.")
    subcomandes = parser.add_subparsers(dest="comanda", required=True)

    afegir = subcomandes.add_parser("add", help="Afegeix una nova tasca")
    afegir.add_argument("--title", required=True, help="Títol de la tasca")
    afegir.add_argument("--subject", required=True, help="Assignatura de la tasca")
    afegir.add_argument("--due", help="Data límit de la tasca (AAAA-MM-DD)")

    subcomandes.add_parser("list", help="Mostra totes les tasques")

    done = subcomandes.add_parser("done", help="Marca una tasca com a completada")
    done.add_argument("--id", type=int, required=True, help="ID de la tasca")

    editar = subcomandes.add_parser("edit", help="Modifica els atributs d'una tasca")
    editar.add_argument("--id", type=int, required=True, help="ID de la tasca")
    editar.add_argument("--title", help="Nou títol de la tasca")
    editar.add_argument("--subject", help="Nova assignatura de la tasca")
    editar.add_argument("--due", help="Nova data límit (AAAA-MM-DD)")
    editar.add_argument("--status", help="Nou estat (pendent o completada)")

    arguments = parser.parse_args()
    if arguments.comanda == "add":
        afegir_tasca(arguments.title, arguments.subject, arguments.due)
    elif arguments.comanda == "list":
        llistar_tasques()
    elif arguments.comanda == "done":
        completar_tasca(arguments.id)
    elif arguments.comanda == "edit":
        editar_tasca(
            arguments.id,
            titol=arguments.title,
            assignatura=arguments.subject,
            data_limit=arguments.due,
            estat=arguments.status,
        )


if __name__ == "__main__":
    main()
