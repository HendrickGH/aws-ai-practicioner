# Feature: Nivel difícil (2 exámenes nuevos)

## Objetivo

Dividir el simulador AIF-C01 en dos niveles:
- **Fácil**: los 4 exámenes actuales (A–D).
- **Difícil**: 2 exámenes nuevos (E, F), 65 preguntas cada uno, con preguntas más
  robustas (escenarios largos, múltiples restricciones) y opciones más ambiguas entre sí.

## Problema

Las 260 preguntas actuales son sólidas pero de **reconocimiento**: una pista del enunciado
elimina dos opciones y la correcta suele ser la única "sensata". No discriminan a quien ya
está cerca del corte de 700. Falta un nivel que obligue a **sintetizar** y a distinguir
matices entre opciones todas plausibles.

## Por qué

El examen real mezcla preguntas fáciles con otras donde dos opciones son técnicamente
defendibles y hay que elegir la **mejor**. Practicar solo con reconocimiento infla la
confianza. Un nivel difícil prepara mejor para los 700+.

## Alcance

- 2 bancos nuevos: `banco/preguntas.examE.json` y `banco/preguntas.examF.json` (65 c/u).
- Mismo blueprint AIF-C01 v1.1 y mismos pesos 13/16/18/9/9.
- Campo `level` (`facil`/`dificil`) en el modelo de exámenes.
- UI de inicio agrupada por nivel; textos y README actualizados.
- `validar.py` y `construir.py` extendidos a 6 bancos.

**Fuera de alcance**: cambiar los 4 bancos fáciles existentes; tocar el motor de
historial/almacenamiento (ya funciona con `examId` genérico); soporte de otros idiomas.

## Especificación de "difícil" (contrato de autoría)

1. **Enunciado (stem)**: escenario de 2–4 frases con DOS o más restricciones/compromisos.
   Debe forzar síntesis, no reconocimiento. Contexto realista de negocio/técnico. No
   revelar la respuesta en el enunciado.
2. **Opciones**: TODAS plausibles. Ninguna se descarta por absurda. Cada distractor
   representa un error conceptual real y común (no una opción tonta). En `mc`, al menos
   dos opciones deben ser genuinamente cercanas ("mejor respuesta").
3. **Explicación (`explain`)**: por qué la correcta es correcta Y por qué falla al menos el
   distractor tentador. 2–4 frases.
4. **Integración entre dominios**: ~20% de las preguntas cruzan 2+ dominios/tareas.
5. **Idioma**: español neutro, sin voseo ni regionalismos. Nombres de servicios de AWS en
   inglés con el término en español entre paréntesis en su primera aparición. Evitar la
   lista de servicios fuera de alcance.
6. **Tipos**: `mc` (4 opciones, 1 correcta), `mr` (5 opciones, 2–3 correctas),
   `order` (3–5 elementos), `match` (3–7 pares, sin repetidos).

### Objetivos de blueprint por examen (exactos)

| Dominio | Preguntas | Desglose por tarea |
| --- | --- | --- |
| 1 · Fundamentos IA/ML | 13 | 1.1=4, 1.2=5, 1.3=4 |
| 2 · Fundamentos IA generativa | 16 | 2.1=8, 2.2=4, 2.3=4 |
| 3 · Aplicaciones de modelos fundacionales | 18 | 3.1=8, 3.2=6, 3.3=1, 3.4=3 |
| 4 · IA responsable | 9 | 4.1=5, 4.2=4 |
| 5 · Seguridad, cumplimiento y gobernanza | 9 | 5.1=5, 5.2=4 |

### Mezcla de tipos por examen (objetivo ~52/6/4/3)

| Lote (dominio) | mc | mr | order | match |
| --- | --- | --- | --- | --- |
| 1 (1.x) | 11 | 1 | 1 | — |
| 2 (2.x) | 13 | 2 | — | 1 |
| 3 (3.x) | 13 | 2 | 2 | 1 |
| 4 (4.x) | 7 | 1 | — | 1 |
| 5 (5.x) | 8 | — | 1 | — |

## Ejemplos que fijan la vara

### Ejemplo 1 — mc, "mejor respuesta", cruza dominios 3 + 5

> **stem**: "Una fintech quiere lanzar un asistente que resuma conversaciones de soporte
> con un modelo fundacional. Las transcripciones contienen datos de clientes que no deben
> salir de la región. El equipo ya tiene un endpoint de Amazon Bedrock aprovisionado con
> throughput comprometido y una VPC sin acceso público. ¿Cuál es la opción MÁS adecuada
> para invocar el modelo cumpliendo el requisito de residencia de datos?"
>
> **options**:
> 1. "Usar el endpoint aprovisionado a través de una VPC endpoint de interfaz y desactivar el enrutamiento público del modelo."
> 2. "Cambiar a inferencia on-demand para que las respuestas viajen con cifrado TLS 1.2."
> 3. "Enviar las transcripciones a un modelo en otra región con menor latencia y cifrarlas con una AWS KMS key."
> 4. "Entrenar un modelo propio con los datos en la región y servirlo en la red pública de la VPC."
>
> **answers**: [0]
>
> **explain**: "Una VPC endpoint de interfaz mantiene el tráfico dentro de la VPC y evita
> la exposición a internet, cumpliendo la residencia de datos. La opción on-demand no
> resuelve la residencia y cruza la red pública; mover los datos a otra región la
> incumple; y entrenar un modelo propio es desproporcionado cuando ya hay un endpoint."

### Ejemplo 2 — mr, cruza dominios 2 + 4

> **stem**: "Una empresa publica resúmenes de noticias generados por IA para el público
> general. Quiere minimizar el riesgo de salida dañina y cumplir lineamientos de IA
> responsable. ¿Cuáles DOS medidas son las más apropiadas para el lanzamiento?"
>
> **options**:
> 1. "Aplicar Guardrails de Amazon Bedrock para filtrar contenido tóxico y revelación de datos sensibles en inferencia."
> 2. "Usar red-teaming con un grupo diverso de probadores antes del lanzamiento y reevaluar periódicamente."
> 3. "Entrenar el modelo con un corpus mayor de noticias para eliminar por completo cualquier salida indeseada."
> 4. "Publicar las salidas sin intervención humana para que el público confíe en que el modelo es objetivo."
> 5. "Omitir los registros de transparencia para no exponer las limitaciones del modelo."
>
> **answers**: [0, 1]
>
> **explain**: "Los Guardrails filtran contenido no deseado en inferencia y el red-teaming
> evalúa de forma adversa antes y después del lanzamiento. Entrenar con más datos no
> garantiza eliminar salidas indeseadas; ocultar la intervención o los límites del modelo
> va contra la transparencia y la IA responsable."

## Restricciones de contenido

- Lista de servicios **fuera de alcance** (no usar como respuesta correcta): Amazon
  Pinpoint, Amazon SES, AppFlow, Amazon MQ, Amazon SWF, Amazon MSK, Keyspaces, QLDB,
  Lightsail, Elastic Beanstalk, App Runner, AWS Support, Amazon Chime, AWS Supply Chain,
  Wickr, CloudSearch, Image Builder, ROSA.
- Prohibido voseo/regionalismos: `vos`, `tenés`, `podés`, `querés`, `sabés`, `hacés`,
  `andá`, `mirá`, `laburo`, etc.
- Sin enunciados duplicados dentro del mismo banco.
- `id` de 1 a 65, únicos y en orden.

## Checklist

- [x] T1 · `banco/preguntas.examE.json` — 65 preguntas difíciles, blueprint completo.
- [x] T2 · `banco/preguntas.examF.json` — 65 preguntas difíciles, blueprint completo.
- [x] T3 · `build/validar.py` — valida 6 bancos (A–F) y añade comprobaciones de dificultad.
- [x] T4 · `build/construir.py` — campo `level` + exámenes E y F.
- [x] T5 · `build/plantilla.html` — agrupar por nivel en inicio + corregir textos.
- [x] T6 · `README.md` — documentar los 2 niveles.
- [x] T7 · Reconstruir y validar `index.html`.

## Criterios de aceptación

1. `python3 build/validar.py` pasa para los 6 bancos (exit 0).
2. `python3 build/construir.py` regenera `index.html` sin errores.
3. La vista de inicio agrupa exámenes bajo "Nivel fácil" (4) y "Nivel difícil" (2).
4. Revisión manual de muestra: los distractores de las preguntas E/F son plausibles y la
   correcta exige un matiz, no una pista obvia.

## Verificación aplicable

- `python3 build/validar.py` (estructural + blueprint + dificultad).
- `python3 build/construir.py` (build).
- Lectura estructural de `index.html` resultante (marcador reemplazado, nivel presente).

## Progreso

- [x] Completado: bancos E y F autorados y validados; plumbing, plantilla y README actualizados; `index.html` reconstruido (390 preguntas). Verificación: `validar.py` exit 0 y `construir.py` sin errores.
