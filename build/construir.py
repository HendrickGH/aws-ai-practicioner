#!/usr/bin/env python3
"""Regenera index.html a partir de build/plantilla.html y los bancos de banco/.

Uso:  python3 build/construir.py
"""
import json
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
PLANTILLA = RAIZ / "build" / "plantilla.html"
SALIDA = RAIZ / "index.html"
MARCADOR = "__EXAMS_JSON__"

EXAMENES = [
    ("A", "Examen 1 — Escenarios mixtos",
     "Empresas y equipos variados; cubre el blueprint completo sin un sector dominante.", "facil"),
    ("B", "Examen 2 — Comercio, logística y retail",
     "Tiendas, marketplaces, almacenes, catálogos y reparto de última milla.", "facil"),
    ("C", "Examen 3 — Servicios financieros y regulación",
     "Bancos, aseguradoras, fintech, auditoría, expedientes legales y cumplimiento.", "facil"),
    ("D", "Examen 4 — Salud, industria y sector público",
     "Hospitales, laboratorios, manufactura, energía, gobierno y universidades.", "facil"),
    ("E", "Examen 5 — Difícil · Escenarios mixtos avanzados",
     "Escenarios largos con restricciones múltiples; obliga a sintetizar conceptos de varios dominios.", "dificil"),
    ("F", "Examen 6 — Difícil · Casos integrados multi-dominio",
     "Situaciones reales que cruzan fundamentos, IA generativa, aplicaciones y gobernanza en un mismo caso.", "dificil"),
]


def cargar(id_examen: str) -> list:
    ruta = RAIZ / "banco" / f"preguntas.exam{id_examen}.json"
    preguntas = json.loads(ruta.read_text(encoding="utf-8"))
    if len(preguntas) != 65:
        raise SystemExit(f"{ruta.name}: se esperaban 65 preguntas, hay {len(preguntas)}")
    return preguntas


def main() -> None:
    plantilla = PLANTILLA.read_text(encoding="utf-8")
    if MARCADOR not in plantilla:
        raise SystemExit(f"La plantilla no contiene el marcador {MARCADOR}")

    examenes = [
        {"id": i, "name": n, "desc": d, "level": lv, "questions": cargar(i)}
        for i, n, d, lv in EXAMENES
    ]
    html = plantilla.replace(
        MARCADOR, json.dumps(examenes, ensure_ascii=False, separators=(",", ":"))
    )
    SALIDA.write_text(html, encoding="utf-8")
    print(f"index.html regenerado: {len(html):,} bytes, "
          f"{sum(len(e['questions']) for e in examenes)} preguntas")


if __name__ == "__main__":
    main()
