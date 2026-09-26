# Simuladores · AWS Certified AI Practitioner (AIF-C01)

Seis exámenes de práctica en español en dos niveles de dificultad, apegados al exam guide
oficial versión 1.1 (publicada el 30 de abril de 2026), que es la que agregó los objetivos
de IA agéntica.

## Qué es esto

- **390 preguntas** (6 exámenes × 65) en dos niveles: **fácil** (4 exámenes de
  reconocimiento) y **difícil** (2 exámenes con escenarios robustos y opciones ambiguas),
  escritas en español neutro, con los nombres de los servicios de AWS en inglés.
- **Pesos idénticos al examen real**: 13 / 16 / 18 / 9 / 9 preguntas para los dominios
  20% / 24% / 28% / 14% / 14%.
- **Los cuatro tipos de pregunta que usa AWS**: opción múltiple, respuesta múltiple,
  ordenamiento y emparejamiento.
- **Dos modos por examen**: simulacro cronometrado de 90 minutos (sin retroalimentación,
  como el examen real) y modo estudio sin límite, con la explicación inmediata después
  de cada respuesta.
- **Historial local**: cada intento terminado se guarda en el navegador con fecha, modo,
  correctas, puntaje escalado, duración y desglose por dominio. Incluye progresión,
  mejor puntaje por examen, precisión acumulada por dominio y respaldo en JSON.

## Cómo usarlo

Abre `index.html` con doble clic. Funciona sin servidor, sin internet y sin instalar nada.

Recomendaciones:

1. Usa **Chrome** para abrir el archivo. El historial usa `localStorage`, que en archivos
   locales funciona bien en Chrome; Safari y algunos visores embebidos lo bloquean. Si eso
   pasa, el simulador te avisa en pantalla y puedes usar el respaldo de exportar e importar.
2. El historial vive en **ese navegador y esa máquina**. Si cambias de equipo, exporta el
   JSON desde la vista de historial e impórtalo en el otro.
3. Ruta sugerida: el Examen 1 en modo simulacro para diagnóstico, los exámenes 2 y 3 en
   modo estudio (ahí la explicación es la que enseña) y el 4 como simulacro final. Cuando
   domines el nivel fácil, pasa a los exámenes 5 y 6 (nivel difícil): sus escenarios con
   restricciones múltiples y opciones ambiguas miden si de verdad estás listo para el 700.
   Después ataca el dominio que quede por debajo de 70% acumulado.

Atajos de teclado en el examen: `1`–`6` responden, `←` `→` navegan, `F` marca para repasar.

## Estructura

```
index.html                  Simulador completo: motor + las 390 preguntas embebidas.
                            Es el único archivo que necesitas para estudiar.
banco/
  preguntas.examA.json      Examen 1 (fácil), escenarios mixtos.
  preguntas.examB.json      Examen 2 (fácil), comercio, logística y retail.
  preguntas.examC.json      Examen 3 (fácil), servicios financieros y regulación.
  preguntas.examD.json      Examen 4 (fácil), salud, industria y sector público.
  preguntas.examE.json      Examen 5 (difícil), escenarios mixtos avanzados.
  preguntas.examF.json      Examen 6 (difícil), casos integrados multi-dominio.
build/
  plantilla.html            Motor del simulador con el marcador __EXAMS_JSON__.
  construir.py              Regenera index.html desde la plantilla y los bancos.
  validar.py                Valida los bancos contra el blueprint (pesos, tipos, formato).
```

## Reconstruir después de editar preguntas

```bash
python3 build/validar.py      # revisa los seis bancos
python3 build/construir.py    # regenera index.html
```

`construir.py` inyecta los bancos dentro de la plantilla, así que `index.html` sigue siendo
un archivo único y autocontenido. Si editas una pregunta en `banco/`, vuelve a correr los
dos comandos.

## Formato de una pregunta

```json
{"id": 1, "domain": 1, "task": "1.1", "type": "mc",
 "stem": "Enunciado del escenario...",
 "options": ["A", "B", "C", "D"], "answers": [0],
 "explain": "Por qué la correcta es correcta y por qué falla el distractor tentador."}
```

- `type`: `mc` (una correcta, 4 opciones), `mr` (2 o 3 correctas, 5 opciones),
  `order` (3 a 5 elementos en `items`, ya en el orden correcto),
  `match` (3 a 7 pares en `pairs`, cada par es `[enunciado, respuesta correcta]`).
- `task` es la task statement del blueprint a la que pertenece la pregunta. El simulador la
  usa para decirte exactamente qué repasar en la pantalla de resultados.
- `answers` son índices base cero sobre `options`.

## Advertencia honesta

Estas 390 preguntas son originales y están ancladas al exam guide oficial, pero **no están
revisadas ni avaladas por AWS**, y no son preguntas filtradas del examen real. Sirven como
banco de práctica serio y como diagnóstico, no como garantía de aprobar.

Los nombres de servicios y siglas se mantienen en inglés con el término en español entre
paréntesis, porque la traducción oficial puede usar palabras distintas. El exam guide
oficial en español (Latinoamérica) es la referencia para alinear vocabulario.
# aws-ai-practicioner
