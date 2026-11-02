# Opciones de empresa para el Proyecto Final

Cada archivo describe **una empresa**: la imagen del modelo de datos (qué tablas se conectan, por qué campos y qué se trae de cada una), cómo se resuelve lo que pide `ProyectoFinal.pdf` y qué riesgos tiene. Los datos se verificaron en datos.gov.co el 2026-11-02.

| # | Empresa | Origen | Datos principales | Esfuerzo | Ajuste literal al PDF* | Potencia de datos |
|---|---|---|---|---|---|---|
| 1 | [Bancolombia](01_Bancolombia.md) | Fija (avance) | Quejas SFC 2010–2026 + tarjetas | Bajo | Medio | Alta |
| 2 | [Davivienda](02_Davivienda.md) | Fija (avance) | Quejas SFC 2019–2026 (más de 113 000 filas) | El más bajo (ya implementado) | Medio | Alta |
| 3 | [Seguros Bolívar](03_Seguros_Bolivar.md) | Pedida | Quejas SFC + primas por ramo (Formato 290) | Medio | Medio-alto | Media-alta |
| 4 | [Falabella](04_Falabella.md) | Alternativa | Sanciones SIC (14) + Banco Falabella | Medio | Alto | Baja-media |
| 5 | [Grupo Éxito](05_Grupo_Exito.md) | Alternativa | Sanciones SIC (35) + Tuya + Éxito Móvil | Medio | Alto | Media |

\* El PDF pide "una marca de ropa, de un producto tecnológico, de consumo o la que más les interese" y detectar "errores o mal servicio". Las opciones 4 y 5 son las únicas donde la marca es de consumo final y la SIC la sanciona por su nombre.

## Patrón común del modelo

Las cinco opciones usan la misma arquitectura, por lo que se puede cambiar de empresa sin rehacer el trabajo:

1. **`dim_marca`** (tabla puente manual): traduce la marca a cada forma de nombrarla en cada fuente.
2. Fuentes **principal y complementarias** descargadas con la API SODA y filtradas en el servidor.
3. **`eq_*`** (tabla de homologación manual): `producto` y `motivo` no coinciden entre las dos fuentes de quejas.
4. **`fact_reputacion_trimestral`**: tabla integrada de la que salen las variables derivadas y los gráficos.

## Qué hay de común en los datos (aplica a todas)

- `hjqv-fp48` (2010–2022) y `xyy7-rn7p` (2023–2026) son consecutivos y se unen por `(tipo_entidad, codigo_entidad)`.
- `h2jg-r3zg` (tarjetas, mensual desde 2015) se propone como nuevo denominador en las opciones con tarjeta; se une por `(tipoentidad, codigoentidad)` y no se ha usado todavía en el avance existente.
- Las columnas `quejas_*` vienen como texto: hay que convertirlas a número.
- Se repite el mismo patrón de calidad: 2022 incompleto y nomenclaturas distintas de `producto` y `motivo`.

## Recomendación

- **Si prima el plazo y el riesgo:** Davivienda, con Bancolombia como contraste. El trabajo de carga ya está hecho y la evidencia es abundante.
- **Si prima ajustarse a la letra del enunciado:** Grupo Éxito. Tiene una marca de consumo y datos suficientes para el análisis, a costa de una integración conceptual (por marca y trimestre) entre SIC y SFC.
- Falabella es más reconocible como marca de ropa y tecnología, pero con solo 14 sanciones la parte estadística queda débil.
- Seguros Bolívar es la mejor opción para una métrica de reputación "justa" (quejas por prima), con el mayor riesgo técnico en el Formato 290.

Esta recomendación es una opinión basada en los datos revisados; la decisión final depende de cuánto pese para el equipo la fidelidad al enunciado frente al riesgo de plazo.

## Pendiente de validar con el docente

- Si una marca financiera cumple el requisito de "marca de ropa, tecnología o consumo" (las opciones 1–3 asumen que sí, porque el PDF también admite "la que más les interese").
- Si se puede integrar por marca y periodo cuando no existe una llave común (opciones 4 y 5).
