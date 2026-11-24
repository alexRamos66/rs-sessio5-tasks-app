"""Tests d'integració dels escenaris GS-01 a GS-17."""

import json
import os
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


def executar_amb_error(projecte_temporal, *arguments):
    return subprocess.run(
        [sys.executable, "src/tasks_app.py", *arguments],
        cwd=projecte_temporal,
        capture_output=True,
        text=True,
    )


def executar_amb_avui(projecte_temporal, *arguments):
    resultat = subprocess.run(
        [sys.executable, "src/tasks_app.py", *arguments],
        cwd=projecte_temporal,
        capture_output=True,
        text=True,
        check=True,
        env={**os.environ, "TASKS_AVUI": "2026-11-24"},
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


def test_gs06_creacio_tasca_amb_data_limit(projecte_temporal):
    sortida = executar(
        projecte_temporal,
        "add",
        "--title",
        "Pràctica 5",
        "--subject",
        "RS",
        "--due",
        "2026-12-15",
    )

    assert sortida == "Tasca [ID: 1] creada amb èxit"
    fitxer = projecte_temporal / "data" / "tasks.json"
    registres = json.loads(fitxer.read_text(encoding="utf-8"))
    assert registres == [
        {
            "id": 1,
            "titol": "Pràctica 5",
            "assignatura": "RS",
            "estat": "pendent",
            "data_limit": "2026-12-15",
        }
    ]


def test_gs07_creacio_tasca_amb_data_limit_no_valida(projecte_temporal):
    fitxer = escriure_registres(projecte_temporal, [])

    resultat = executar_amb_error(
        projecte_temporal,
        "add",
        "--title",
        "Pràctica 5",
        "--subject",
        "RS",
        "--due",
        "2026-13-45",
    )

    assert resultat.returncode != 0
    assert resultat.stdout.strip() == (
        "Error: data límit no vàlida (format esperat: AAAA-MM-DD)"
    )
    assert json.loads(fitxer.read_text(encoding="utf-8")) == []


def test_gs08_modificacio_atributs_tasca(projecte_temporal):
    fitxer = escriure_registres(
        projecte_temporal,
        [
            {
                "id": 1,
                "titol": "Practica 1",
                "assignatura": "SO",
                "estat": "pendent",
                "data_limit": None,
            }
        ],
    )

    sortida = executar(
        projecte_temporal,
        "edit",
        "--id",
        "1",
        "--title",
        "Pràctica 1",
        "--subject",
        "RS",
        "--due",
        "2026-12-01",
    )

    assert sortida == "Tasca [ID: 1] modificada amb èxit"
    registres = json.loads(fitxer.read_text(encoding="utf-8"))
    assert registres == [
        {
            "id": 1,
            "titol": "Pràctica 1",
            "assignatura": "RS",
            "estat": "pendent",
            "data_limit": "2026-12-01",
        }
    ]


def test_gs09_modificacio_estat_no_valid(projecte_temporal):
    fitxer = escriure_registres(
        projecte_temporal,
        [
            {
                "id": 1,
                "titol": "Pràctica 1",
                "assignatura": "RS",
                "estat": "pendent",
                "data_limit": None,
            }
        ],
    )
    contingut_original = fitxer.read_bytes()

    resultat = executar_amb_error(
        projecte_temporal, "edit", "--id", "1", "--status", "acabada"
    )

    assert resultat.returncode != 0
    assert resultat.stdout.strip() == (
        "Error: estat no vàlid (valors permesos: pendent, completada)"
    )
    assert fitxer.read_bytes() == contingut_original


def test_gs10_modificacio_tasca_inexistent(projecte_temporal):
    fitxer = escriure_registres(
        projecte_temporal,
        [
            {
                "id": 1,
                "titol": "Pràctica 1",
                "assignatura": "RS",
                "estat": "pendent",
                "data_limit": None,
            }
        ],
    )
    contingut_original = fitxer.read_bytes()

    resultat = executar_amb_error(
        projecte_temporal, "edit", "--id", "99", "--title", "Nou títol"
    )

    assert resultat.returncode != 0
    assert resultat.stdout.strip() == "Error: no existeix cap tasca amb ID 99"
    assert fitxer.read_bytes() == contingut_original


def test_gs11_marcar_tasca_completada(projecte_temporal):
    fitxer = escriure_registres(
        projecte_temporal,
        [
            {
                "id": 1,
                "titol": "Pràctica 1",
                "assignatura": "RS",
                "estat": "pendent",
                "data_limit": None,
            }
        ],
    )

    sortida = executar(projecte_temporal, "done", "--id", "1")

    assert sortida == "Tasca [ID: 1] completada"
    registres = json.loads(fitxer.read_text(encoding="utf-8"))
    assert registres == [
        {
            "id": 1,
            "titol": "Pràctica 1",
            "assignatura": "RS",
            "estat": "completada",
            "data_limit": None,
        }
    ]


def test_gs12_marcar_completada_tasca_inexistent(projecte_temporal):
    fitxer = escriure_registres(
        projecte_temporal,
        [
            {
                "id": 1,
                "titol": "Pràctica 1",
                "assignatura": "RS",
                "estat": "pendent",
                "data_limit": None,
            }
        ],
    )
    contingut_original = fitxer.read_bytes()

    resultat = executar_amb_error(projecte_temporal, "done", "--id", "99")

    assert resultat.returncode != 0
    assert resultat.stdout.strip() == "Error: no existeix cap tasca amb ID 99"
    assert fitxer.read_bytes() == contingut_original


def test_gs13_llistat_data_llunyana(projecte_temporal):
    escriure_registres(
        projecte_temporal,
        [
            {
                "id": 1,
                "titol": "Pràctica 5",
                "assignatura": "RS",
                "estat": "pendent",
                "data_limit": "2026-12-15",
            }
        ],
    )

    sortida = executar_amb_avui(projecte_temporal, "list")

    assert sortida == (
        "[1] Pràctica 5 (RS) - estat: pendent - límit: 2026-12-15"
    )


def test_gs14_llistat_tasca_caducada(projecte_temporal):
    escriure_registres(
        projecte_temporal,
        [
            {
                "id": 1,
                "titol": "Pràctica 1",
                "assignatura": "RS",
                "estat": "pendent",
                "data_limit": "2026-11-20",
            }
        ],
    )

    sortida = executar_amb_avui(projecte_temporal, "list")

    assert sortida == (
        "[1] Pràctica 1 (RS) - estat: pendent - límit: 2026-11-20 [CADUCADA]"
    )


def test_gs15_llistat_tasca_urgent(projecte_temporal):
    escriure_registres(
        projecte_temporal,
        [
            {
                "id": 1,
                "titol": "Examen parcial",
                "assignatura": "SO",
                "estat": "pendent",
                "data_limit": "2026-11-27",
            }
        ],
    )

    sortida = executar_amb_avui(projecte_temporal, "list")

    assert sortida == (
        "[1] Examen parcial (SO) - estat: pendent - límit: 2026-11-27 [URGENT]"
    )


def test_gs16_limits_periode_urgencia(projecte_temporal):
    escriure_registres(
        projecte_temporal,
        [
            {
                "id": 1,
                "titol": "A",
                "assignatura": "RS",
                "estat": "pendent",
                "data_limit": "2026-11-24",
            },
            {
                "id": 2,
                "titol": "B",
                "assignatura": "RS",
                "estat": "pendent",
                "data_limit": "2026-11-30",
            },
            {
                "id": 3,
                "titol": "C",
                "assignatura": "RS",
                "estat": "pendent",
                "data_limit": "2026-12-01",
            },
        ],
    )

    sortida = executar_amb_avui(projecte_temporal, "list")

    assert sortida == (
        "[1] A (RS) - estat: pendent - límit: 2026-11-24 [URGENT]\n"
        "[2] B (RS) - estat: pendent - límit: 2026-11-30 [URGENT]\n"
        "[3] C (RS) - estat: pendent - límit: 2026-12-01"
    )


def test_gs17_sense_indicadors_completades_i_sense_data(projecte_temporal):
    escriure_registres(
        projecte_temporal,
        [
            {
                "id": 1,
                "titol": "A",
                "assignatura": "RS",
                "estat": "completada",
                "data_limit": "2026-11-20",
            },
            {
                "id": 2,
                "titol": "B",
                "assignatura": "RS",
                "estat": "pendent",
                "data_limit": None,
            },
        ],
    )

    sortida = executar_amb_avui(projecte_temporal, "list")

    assert sortida == (
        "[1] A (RS) - estat: completada - límit: 2026-11-20\n"
        "[2] B (RS) - estat: pendent"
    )
