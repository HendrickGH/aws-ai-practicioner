#!/usr/bin/env python3
"""Valida los cuatro bancos de preguntas contra el blueprint AIF-C01.

Uso:  python3 build/validar.py
Salida: un renglón por comprobación. Termina con código 1 si algo falla.
"""
import collections
import json
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DOMINIOS_ESPERADOS = {1: 13, 2: 16, 3: 18, 4: 9, 5: 9}          # pesos 20/24/28/14/14
TAREAS_ESPERADAS = {"1.1": 4, "1.2": 5, "1.3": 4, "2.1": 8, "2.2": 4, "2.3": 4,
                    "3.1": 8, "3.2": 6, "3.3": 1, "3.4": 3, "4.1": 5, "4.2": 4,
                    "5.1": 5, "5.2": 4}
FUERA_DE_ALCANCE = ["Amazon Pinpoint", "Amazon SES", "AppFlow", "Amazon MQ", "Amazon SWF",
                    "Amazon MSK", "Keyspaces", "QLDB", "Lightsail", "Elastic Beanstalk",
                    "App Runner", "AWS Support", "Amazon Chime", "AWS Supply Chain",
                    "Wickr", "CloudSearch", "Image Builder", "ROSA"]
VOSEO = re.compile(r"\b(vos|ten[eé]s|pod[eé]s|quer[eé]s|sab[eé]s|hac[eé]s|and[aá]|mir[aá]|laburo)\b", re.I)

fallos = []


def revisar(cond, mensaje):
    print(("[OK]   " if cond else "[FALLA] ") + mensaje)
    if not cond:
        fallos.append(mensaje)


def respuesta_correcta(q):
    if q["type"] in ("mc", "mr"):
        return " || ".join(q["options"][i] for i in q["answers"])
    if q["type"] == "order":
        return " → ".join(q["items"])
    return " || ".join(p[1] for p in q["pairs"])


def validar_examen(ruta):
    print(f"\n== {ruta.name} ==")
    qs = json.loads(ruta.read_text(encoding="utf-8"))
    revisar(len(qs) == 65, f"65 preguntas (hay {len(qs)})")
    revisar([q["id"] for q in qs] == list(range(1, 66)), "ids 1..65 únicos y en orden")

    dom = collections.Counter(q["domain"] for q in qs)
    revisar({d: dom[d] for d in sorted(dom)} == DOMINIOS_ESPERADOS,
            f"dominios {dict(sorted(dom.items()))}")
    tar = collections.Counter(q["task"] for q in qs)
    revisar(set(tar) == set(TAREAS_ESPERADAS),
            f"las 14 task statements cubiertas ({len(tar)} distintas)")
    desvios = {t: tar.get(t, 0) - TAREAS_ESPERADAS[t] for t in TAREAS_ESPERADAS}
    fuera_de_rango = {t: d for t, d in desvios.items() if abs(d) > 2}
    print(f"       distribución: {dict(sorted(tar.items()))}")
    if desvios and any(desvios.values()):
        print(f"       desvío vs. objetivo de autoría: { {t: d for t, d in desvios.items() if d} }")
    revisar(not fuera_de_rango and sum(tar.values()) == 65,
            "conteo por task statement dentro de ±2 del objetivo")

    for q in qs:
        n = q["id"]
        if q["type"] == "mc":
            revisar(len(q["options"]) == 4 and len(q["answers"]) == 1, f"#{n} mc: 4 opciones y 1 correcta")
        elif q["type"] == "mr":
            revisar(len(q["options"]) == 5 and 2 <= len(q["answers"]) <= 3,
                    f"#{n} mr: 5 opciones y 2-3 correctas")
        elif q["type"] == "order":
            revisar(3 <= len(q["items"]) <= 5, f"#{n} order: 3-5 elementos")
        elif q["type"] == "match":
            l = [p[0] for p in q["pairs"]]
            r = [p[1] for p in q["pairs"]]
            revisar(3 <= len(q["pairs"]) <= 7 and len(set(l)) == len(l) and len(set(r)) == len(r),
                    f"#{n} match: 3-7 pares sin repetidos")
        else:
            revisar(False, f"#{n} tipo desconocido: {q['type']}")

        texto = q["stem"] + " " + " ".join(map(str, q.get("options", [])))
        if VOSEO.search(texto):
            revisar(False, f"#{n} posible voseo o regionalismo")
        if any(s in respuesta_correcta(q) for s in FUERA_DE_ALCANCE):
            revisar(False, f"#{n} servicio fuera de alcance como respuesta correcta")

    repetidos = [s for s, c in collections.Counter(q["stem"] for q in qs).items() if c > 1]
    revisar(not repetidos, f"sin enunciados duplicados ({len(repetidos)} encontrados)")


def main():
    for id_examen in "ABCD":
        validar_examen(RAIZ / "banco" / f"preguntas.exam{id_examen}.json")
    print()
    if fallos:
        print(f"RESULTADO: {len(fallos)} comprobación(es) fallida(s)")
        return 1
    print("RESULTADO: todas las comprobaciones pasaron")
    return 0


if __name__ == "__main__":
    sys.exit(main())
