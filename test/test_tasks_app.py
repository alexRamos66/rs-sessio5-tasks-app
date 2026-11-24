"""Tests d'integració dels escenaris GS-01, GS-02, GS-03, GS-04 i GS-05."""

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


RUTA_SRC = Path(__file__).resolve().parent.parent / "src"


@pytest.fixture
def projecte_temporal(tmp_path):
    directori_src = tmp_path / "src"
    directori_src.mkdir()
    for nom in ("models.py", "tasks_app.py"):
        shutil.copy(RUTA_SRC / nom, directori_src / nom)
    return tmp_path


def executar(projecte_temporal, *arguments):
    resultat = subprocess.run(
        [sys.executable, "src/tasks_app.py", *arguments],
        cwd=projecte_temporal,
        capture_output=True,
        text=True,
        check=True,
    )
    return resultat.stdout.strip()


def escriure_registres(projecte_temporal, registres):
    directori_dades = projecte_temporal / "data"
    directori_dades.mkdir(exist_ok=True)
    fitxer = directori_dades / "tasks.json"
    fitxer.write_text(
        json.dumps(registres, ensure_ascii=False), encoding="utf-8"
    )
    return fitxer


def test_gs01_creacio_tasca(projecte_temporal):
    sortida = executar(
        projecte_temporal, "add", "--title", "Pràctica 1", "--subject", "RS"
    )

    assert sortida == "Tasca [ID: 1] creada amb èxit"
    fitxer = projecte_temporal / "data" / "tasks.json"
    registres = json.loads(fitxer.read_text(encoding="utf-8"))
    assert registres == [
        {
            "id": 1,
            "titol": "Pràctica 1",
            "assignatura": "RS",
            "estat": "pendent",
            "data_limit": None,
        }
    ]


def test_gs02_llistat_buit(projecte_temporal):
    sortida = executar(projecte_temporal, "list")

    assert sortida == "Registre de tasques buit."
    fitxer = projecte_temporal / "data" / "tasks.json"
    assert json.loads(fitxer.read_text(encoding="utf-8")) == []


def test_gs03_llistat_amb_registres(projecte_temporal):
    escriure_registres(
        projecte_temporal,
        [
            {
                "id": 1,
                "titol": "Pràctica 1",
                "assignatura": "RS",
                "estat": "pendent",
            },
            {
                "id": 2,
                "titol": "Examen parcial",
                "assignatura": "SO",
                "estat": "pendent",
            },
        ],
    )

    sortida = executar(projecte_temporal, "list")

    assert sortida == (
        "[1] Pràctica 1 (RS) - estat: pendent\n"
        "[2] Examen parcial (SO) - estat: pendent"
    )


def test_gs04_creacio_fitxer_dades(projecte_temporal):
    fitxer = projecte_temporal / "data" / "tasks.json"
    assert not fitxer.exists()

    sortida = executar(projecte_temporal, "list")

    assert sortida == "Registre de tasques buit."
    assert fitxer.exists()
    assert json.loads(fitxer.read_text(encoding="utf-8")) == []


def test_gs05_identificadors_consecutius(projecte_temporal):
    fitxer = escriure_registres(
        projecte_temporal,
        [
            {
                "id": 1,
                "titol": "Pràctica 1",
                "assignatura": "RS",
                "estat": "pendent",
            },
            {
                "id": 2,
                "titol": "Examen parcial",
                "assignatura": "SO",
                "estat": "pendent",
            },
        ],
    )

    sortida = executar(
        projecte_temporal, "add", "--title", "Lliurament P5", "--subject", "RS"
    )

    assert sortida == "Tasca [ID: 3] creada amb èxit"
    registres = json.loads(fitxer.read_text(encoding="utf-8"))
    assert len(registres) == 3
    assert registres[2] == {
        "id": 3,
        "titol": "Lliurament P5",
        "assignatura": "RS",
        "estat": "pendent",
        "data_limit": None,
    }
