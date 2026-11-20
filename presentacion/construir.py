"""Genera guion_presentador.md desde las notas de index.html y compila el PDF con Chrome sin interfaz."""
import html
import re
import subprocess
from pathlib import Path

AQUI = Path(__file__).resolve().parent
HTML = AQUI / "index.html"
PDF = AQUI / "ProyectoFinal_Presentacion.pdf"
CHROME = Path("C:/Program Files/Google/Chrome/Application/chrome.exe")


GLOSARIO = [
    ("Queja fundada", "Queja que se cerró a favor del cliente: el banco reconoce que el cliente tenía la razón."),
    ("Homologar", "Emparejar a mano categorías que dos fuentes nombran distinto (por ejemplo, el mismo producto con otro nombre)."),
    ("Puntos físicos", "Oficinas y cajeros del banco (canales 4 y 14). Sirven para comparar departamentos de distinto tamaño."),
    ("Vista minable", "La tabla final, lista para analizar: una fila por mes, departamento y producto."),
    ("Left join", "Unir dos tablas conservando todas las filas de la tabla base, aunque la otra no tenga pareja."),
    ("Índice relativo", "Cuánto subieron las quejas de un departamento frente a lo normal, comparado con lo que subió el país ese mes."),
    ("Regla de Tukey", "Regla estándar para detectar valores fuera de rango: marca lo que se aleja del 50 % central de los datos más de 1,5 veces el ancho de ese 50 %."),
    ("Periodo de arranque", "Enero a septiembre de 2023, cuando Smartsupervision apenas empezaba a reportar; no se evalúa."),
    ("Correlación", "Qué tanto se mueven juntas dos variables; va de −1 a 1, y cerca de 1 significa que suben juntas."),
    ("Mediana", "El valor del medio cuando se ordenan los datos; no se deja arrastrar por valores extremos como el promedio."),
    ("MAR", "Datos que faltan más en un grupo que en otro, según algo que sí se observa (aquí, la instancia que recibió la queja)."),
    ("CRISP-DM", "Metodología por fases para proyectos de datos; este hito cubre las tres primeras: negocio, datos y preparación."),
]


def texto(fragmento):
    fragmento = re.sub(r"</?b>", "**", fragmento)
    fragmento = re.sub(r"</?i>", "*", fragmento)
    sin_etiquetas = re.sub(r"<[^>]+>", "", fragmento)
    return html.unescape(re.sub(r"\s+", " ", sin_etiquetas)).strip()


def guion():
    fuente = HTML.read_text(encoding="utf-8")
    diapositivas = re.findall(r'<section class="slide[^"]*">(.*?)</section>', fuente, flags=re.S)
    lineas = [
        "# Guion del presentador",
        "",
        "Sustentación del proyecto final de Gestión de Datos: monitoreo de reputación de Banco Davivienda.",
        "Este archivo se genera desde las notas de `index.html` (tecla **N** en la presentación); para cambiar el guion, editen las notas y vuelvan a ejecutar `construir.py`.",
        "",
        "| Bloque | Tiempo | Diapositivas |",
        "|---|---|---|",
        "| Elevator pitch | 5 min | 1–2 |",
        "| Material técnico | 10 min | 3–22 |",
        "| Trabajo en equipo | 2 min | 23 |",
        "| Preguntas | 5 min | 24 |",
        "",
        "**Cómo usar este guion.** Cada diapositiva tiene tres partes: la **idea clave** (lo único que el público debe recordar), el texto para decir en voz alta y, a veces, un *si preguntan* con el detalle técnico. Lo de *si preguntan* no se dice en la presentación; es apoyo para la ronda de preguntas. No hace falta leer el texto palabra por palabra: basta con transmitir la idea clave y las cifras.",
        "",
        "## Glosario rápido",
        "",
        "| Término | En palabras simples |",
        "|---|---|",
        *[f"| {termino} | {definicion} |" for termino, definicion in GLOSARIO],
        "",
    ]
    for n, cuerpo in enumerate(diapositivas, start=1):
        titulo = re.search(r"<h1>(.*?)</h1>", cuerpo, flags=re.S)
        seccion = re.search(r'<span class="seccion">(.*?)</span>', cuerpo, flags=re.S)
        etiqueta = re.search(r'<div class="etiqueta">(.*?)</div>', cuerpo, flags=re.S)
        encabezado = texto((titulo or etiqueta).group(1))
        lineas.append(f"## {n}. {encabezado}")
        if seccion:
            lineas.append(f"*{texto(re.sub(r'</?b>', '', seccion.group(1)))}*")
        lineas.append("")
        notas = re.search(r'<aside class="notes">(.*?)</aside>', cuerpo, flags=re.S)
        for parrafo in re.findall(r"<p>(.*?)</p>", notas.group(1), flags=re.S):
            lineas.append(texto(parrafo))
            lineas.append("")
    (AQUI / "guion_presentador.md").write_text("\n".join(lineas), encoding="utf-8")
    return len(diapositivas)


ESTILO_GUION = """
@page{size:A4;margin:20mm 20mm 18mm}
body{font-family:"Segoe UI",Arial,sans-serif;font-size:10.5pt;line-height:1.5;color:#1A1D20}
h1{font-family:Georgia,serif;font-weight:400;font-size:24pt;margin:0 0 6pt;border-bottom:3px solid #E1111C;padding-bottom:6pt}
h2{font-family:Georgia,serif;font-weight:400;font-size:14.5pt;margin:20pt 0 2pt;break-after:avoid}
h2 + p em:only-child{color:#8A9097}
p{margin:0 0 7pt}
table{border-collapse:collapse;width:100%;margin:6pt 0 10pt;font-size:9.5pt}
tr{break-inside:avoid}
section{break-inside:avoid}
th{text-align:left;border-bottom:1.5px solid #1A1D20;padding:4pt 8pt 4pt 0}
td{border-bottom:1px solid #D9DBD6;padding:4pt 8pt 4pt 0;vertical-align:top}
strong{color:#1E3A5F}
code{font-size:9pt}
"""


def imprimir(origen, destino):
    subprocess.run([
        str(CHROME), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
        "--allow-file-access-from-files", "--virtual-time-budget=5000",
        f"--print-to-pdf={destino}", origen.as_uri(),
    ], check=True, capture_output=True)


def pdf():
    imprimir(HTML, PDF)


def pdf_guion():
    import markdown
    cuerpo = markdown.markdown((AQUI / "guion_presentador.md").read_text(encoding="utf-8"), extensions=["tables"])
    inicio, *diapositivas = re.split(r"(?=<h2>\d+\.)", cuerpo)
    cuerpo = inicio + "".join(f"<section>{d}</section>" for d in diapositivas)
    temporal = AQUI / "_guion.html"
    temporal.write_text(f'<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{ESTILO_GUION}</style></head>'
                        f"<body>{cuerpo}</body></html>", encoding="utf-8")
    try:
        imprimir(temporal, AQUI / "guion_presentador.pdf")
    finally:
        temporal.unlink()


if __name__ == "__main__":
    print("diapositivas en el guion:", guion())
    pdf()
    pdf_guion()
    print("PDF:", PDF, PDF.stat().st_size, "bytes")
    print("Guion PDF:", AQUI / "guion_presentador.pdf")
