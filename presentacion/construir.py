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


def visibles(fuente):
    secciones = re.findall(r'<section class="(slide[^"]*)">(.*?)</section>', fuente, flags=re.S)
    return [(n, cuerpo) for n, (clases, cuerpo) in enumerate(secciones, start=1) if "oculta" not in clases.split()], len(secciones)


def reparto(diapositivas):
    turnos = []
    for n, cuerpo in diapositivas:
        orador = re.search(r'data-orador="([^"]+)"', cuerpo).group(1)
        hablado = re.findall(r"<p>(\(.*?)</p>", cuerpo, flags=re.S)
        palabras = sum(len(texto(p).split()) for p in hablado)
        seccion = re.search(r'<span class="seccion"><b>\d+</b> · ([^<]+)</span>', cuerpo)
        if turnos and turnos[-1]["orador"] == orador:
            turnos[-1]["hasta"] = n
            turnos[-1]["palabras"] += palabras
            if seccion and seccion.group(1) not in turnos[-1]["temas"]:
                turnos[-1]["temas"].append(seccion.group(1))
        else:
            turnos.append({"orador": orador, "desde": n, "hasta": n, "palabras": palabras,
                           "temas": [seccion.group(1)] if seccion else []})
    filas = ["| Turno | Presenta | Diapositivas | Contenido | Tiempo aprox. |", "|---|---|---|---|---|"]
    for i, t in enumerate(turnos, start=1):
        temas = ", ".join(t["temas"]) or "Portada y cierre"
        filas.append(f"| {i} | **{t['orador']}** | {t['desde']}–{t['hasta']} | {temas} | {t['palabras'] / 135:.1f} min |")
    return filas


def guion():
    fuente = HTML.read_text(encoding="utf-8")
    diapositivas, _ = visibles(fuente)
    lineas = [
        "# Guion del presentador",
        "",
        "Sustentación del proyecto final de Gestión de Datos: monitoreo de reputación de Banco Davivienda.",
        "Este archivo se genera desde las notas de `index.html` (tecla **N** en la presentación); para cambiar el guion, editen las notas y vuelvan a ejecutar `construir.py`.",
        "",
        "| Bloque | Tiempo | Diapositivas |",
        "|---|---|---|",
        "| Elevator pitch | 5 min | 1–8 |",
        "| Material técnico | 10 min | 9–32 |",
        "| Trabajo en equipo | 2 min | 33–34 |",
        "| Preguntas | 5 min | 35 |",
        "",
        "## Quién presenta qué",
        "",
        *reparto(diapositivas),
        "",
        "Fabian abre con el elevator pitch y cierra con el trabajo en equipo; David presenta la integración de datos y los resultados de la P2; Belky presenta la exploración, los resultados de la P1 y las conclusiones. Cada cambio de turno tiene una frase de *relevo* al final de la última diapositiva de quien entrega la palabra. El tiempo es aproximado, a 135 palabras por minuto.",
        "",
        "**El elevator pitch** sigue los siete pasos del video de ejemplo del enunciado: gancho, quiénes somos, problema, solución, beneficio, por qué nosotros y llamada a la acción. Lo presenta Fabian, en primera persona del plural y sin términos técnicos.",
        "",
        "**Cómo usar este guion.** Cada diapositiva tiene tres partes: la **idea clave** (lo único que el público debe recordar), el texto para decir en voz alta y, a veces, un *si preguntan* con el detalle técnico. Lo de *si preguntan* no se dice en la presentación; es apoyo para la ronda de preguntas. Debajo, **Para sustentar las cifras** explica cada número de la diapositiva: qué es, cómo se calculó y en qué sección del cuaderno está, para poder defenderlo si el docente pregunta. No hace falta leer el texto palabra por palabra: basta con transmitir la idea clave y las cifras.",
        "",
        "## Glosario rápido",
        "",
        "| Término | En palabras simples |",
        "|---|---|",
        *[f"| {termino} | {definicion} |" for termino, definicion in GLOSARIO],
        "",
    ]
    for n, cuerpo in diapositivas:
        titulo = re.search(r"<h1>(.*?)</h1>", cuerpo, flags=re.S)
        seccion = re.search(r'<span class="seccion">(.*?)</span>', cuerpo, flags=re.S)
        etiqueta = re.search(r'<div class="etiqueta">(.*?)</div>', cuerpo, flags=re.S)
        encabezado = texto((titulo or etiqueta).group(1))
        lineas.append(f"## {n}. {encabezado}")
        orador = re.search(r'data-orador="([^"]+)"', cuerpo).group(1)
        detalle = f" · {texto(re.sub(r'</?b>', '', seccion.group(1)))}" if seccion else ""
        lineas.append(f"**Presenta: {orador}**{detalle}")
        lineas.append("")
        notas = re.search(r'<aside class="notes"[^>]*>(.*?)</aside>', cuerpo, flags=re.S)
        for etiqueta, contenido in re.findall(r"<(p|h4|li)>(.*?)</\1>", notas.group(1), flags=re.S):
            if etiqueta == "li":
                lineas.append(f"- {texto(contenido)}")
                continue
            if lineas[-1].startswith("- "):
                lineas.append("")
            if contenido.startswith("<mark>"):
                lineas.append(f"<mark>{texto(contenido)}</mark>")
            else:
                lineas.append(f"**{texto(contenido)}**" if etiqueta == "h4" else texto(contenido))
            lineas.append("")
        if lineas[-1].startswith("- "):
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
li{break-inside:avoid;margin-bottom:3pt}
h2 + p{break-before:avoid}
th{text-align:left;border-bottom:1.5px solid #1A1D20;padding:4pt 8pt 4pt 0}
td{border-bottom:1px solid #D9DBD6;padding:4pt 8pt 4pt 0;vertical-align:top}
strong{color:#1E3A5F}
mark{background:#FFE45C;color:#1A1D20;padding:1pt 3pt}
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


ESTILO_VISUAL = """
@font-face{font-family:"IBM Plex Sans";src:url("fuentes/IBMPlexSans-latin.woff2") format("woff2");font-weight:100 700}
@font-face{font-family:"Source Serif 4";src:url("fuentes/SourceSerif4-latin.woff2") format("woff2");font-weight:200 900}
@page{size:A4;margin:14mm 16mm 12mm}
body{font-family:"IBM Plex Sans","Segoe UI",Arial,sans-serif;font-size:9.6pt;line-height:1.45;color:#1A1D20;margin:0}
section{break-after:page;position:relative}
section:last-child{break-after:auto}
.cabeza{display:grid;grid-template-columns:96mm 1fr;gap:7mm;align-items:start;padding-bottom:5mm;border-bottom:2px solid #E1111C;margin-bottom:5mm}
.cabeza img{width:96mm;display:block;border:1px solid #D9DBD6}
.num{font-family:"Source Serif 4",Georgia,serif;font-size:26pt;color:#E1111C;line-height:1}
.titulo{font-family:"Source Serif 4",Georgia,serif;font-size:13.5pt;line-height:1.2;margin:4pt 0 8pt}
.meta{font-size:8.3pt;letter-spacing:.08em;text-transform:uppercase;color:#5B6168;margin-bottom:8pt}
.meta b{color:#1A1D20}
.idea{font-size:9.6pt;border-left:3px solid #E1111C;padding-left:7pt}
h3{font-size:8pt;letter-spacing:.12em;text-transform:uppercase;color:#E1111C;margin:9pt 0 3pt;font-weight:600}
.decir{font-size:10.6pt;line-height:1.55}
.destacado{font-size:10.4pt;line-height:1.55;margin:4pt 0 8pt}
.destacado mark{background:#FFE45C;color:#1A1D20;padding:1pt 2pt;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.apoyo{color:#3A3F45}
ul.apoyo{font-size:8.7pt;line-height:1.38}
ul.apoyo li{margin-bottom:2pt}
.relevo{background:#F3F1EA;padding:5pt 8pt;margin-top:8pt}
ul{margin:0;padding-left:13pt}
li{margin-bottom:3pt}
li b{color:#1E3A5F}
.toca{display:flex;justify-content:space-between;align-items:baseline;background:#1A1D20;color:#fff;padding:6pt 10pt;margin-bottom:5mm}
.toca span{font-size:8pt;letter-spacing:.14em;text-transform:uppercase;color:#C9CBC5}
.toca b{font-family:"Source Serif 4",Georgia,serif;font-weight:500;font-size:17pt;letter-spacing:0}
.toca.Fabian{border-left:8pt solid #E1111C}.toca.David{border-left:8pt solid #1E3A5F}.toca.Belky{border-left:8pt solid #C9A227}
.recibe{border:1px dashed #8A9097;padding:5pt 8pt;margin-bottom:6pt;color:#3A3F45}
.portada-persona h1{font-family:"Source Serif 4",Georgia,serif;font-weight:500;font-size:30pt;margin:30mm 0 4pt;border-bottom:3px solid #E1111C;padding-bottom:6pt}
.portada-persona p{font-size:11pt;margin:0 0 8pt}
.portada-persona table{border-collapse:collapse;width:100%;margin-top:8mm;font-size:10.5pt}
.portada-persona th{text-align:left;border-bottom:1.5px solid #1A1D20;padding:5pt 8pt 5pt 0;font-size:8.5pt;letter-spacing:.1em;text-transform:uppercase;color:#5B6168}
.portada-persona td{border-bottom:1px solid #D9DBD6;padding:6pt 8pt 6pt 0}
"""
ORADORES = ["Fabian", "David", "Belky"]


def pdf_guion_visual():
    import base64
    import pymupdf

    fuente = HTML.read_text(encoding="utf-8")
    diapositivas, total = visibles(fuente)
    paginas = pymupdf.open(PDF)
    assert len(paginas) == len(diapositivas)
    limpio = lambda t: html.escape(texto(t)).replace("**", "")
    hojas, anterior, relevo_anterior = [], None, ""
    for (n, cuerpo), pagina in zip(diapositivas, paginas):
        imagen = base64.b64encode(pagina.get_pixmap(dpi=110).tobytes("png")).decode()
        titulo = re.search(r"<h1>(.*?)</h1>", cuerpo, flags=re.S)
        seccion = re.search(r'<span class="seccion"><b>\d+</b> · ([^<]+)</span>', cuerpo)
        notas = re.search(r'<aside class="notes"[^>]*>(.*?)</aside>', cuerpo, flags=re.S)
        orador = re.search(r'data-orador="([^"]+)"', cuerpo).group(1)
        idea, decir, preguntan, relevo, destacados = "", [], "", "", []
        for p in re.findall(r"<p>(.*?)</p>", notas.group(1), flags=re.S):
            if p.startswith("<b>Idea clave:</b>"):
                idea = limpio(p.replace("<b>Idea clave:</b>", ""))
            elif p.startswith("<i>Si preguntan:</i>"):
                preguntan = limpio(p.replace("<i>Si preguntan:</i>", ""))
            elif p.startswith("<mark>"):
                destacados.append(re.sub(r"<b>(.*?)</b>", r"<b>\1</b>", limpio(re.sub(r"</?mark>", "", p)).replace("Ejemplo para decirlo:", "<b>Ejemplo para decirlo:</b>", 1)))
            elif p.startswith("<i>Relevo:</i>"):
                relevo = limpio(p.replace("<i>Relevo:</i>", ""))
            else:
                decir.append(limpio(p))
        tiempo = re.match(r"\(([^)]*)\)\s*", decir[0]) if decir else None
        if tiempo:
            decir[0] = decir[0][tiempo.end():]
        bloques = [(texto(t), [re.sub(r"<b>(.*?)</b>", lambda m: f"<b>{html.escape(texto(m.group(1)))}</b>", li)
                               for li in re.findall(r"<li>(.*?)</li>", lista, flags=re.S)])
                   for t, lista in re.findall(r"<h4>(.*?)</h4>\s*<ul>(.*?)</ul>", notas.group(1), flags=re.S)]
        partes = [f'''<section>
  <div class="toca {orador}"><span>Le toca a</span><b>{orador}</b><span>Diapositiva {n} de {total}</span></div>
  <div class="cabeza"><img src="data:image/png;base64,{imagen}">
    <div><div class="num">{n:02d}</div>
      <div class="titulo">{limpio(titulo.group(1)) if titulo else "Portada"}</div>
      <div class="meta">Presenta <b>{orador}</b>{f" · {seccion.group(1)}" if seccion else ""}{f" · {html.escape(tiempo.group(1))}" if tiempo else ""}</div>
      <div class="idea">{idea}</div></div></div>
  <h3>Qué decir</h3>''']
        if anterior and anterior != orador and relevo_anterior:
            partes.append(f'<p class="recibe"><b>Recibes la palabra de {anterior}:</b> {relevo_anterior}</p>')
        partes += [f'<p class="decir">{d}</p>' for d in decir]
        partes += [f'<p class="destacado"><mark>{d}</mark></p>' for d in destacados]
        if relevo:
            partes.append(f'<p class="relevo"><b>Relevo:</b> {relevo}</p>')
        if preguntan:
            partes.append(f'<h3>Si preguntan</h3><p class="apoyo">{preguntan}</p>')
        for titulo_bloque, items in bloques:
            partes.append(f'<h3>{html.escape(titulo_bloque)}</h3><ul class="apoyo">' + "".join(f"<li>{c}</li>" for c in items) + "</ul>")
        partes.append("</section>")
        hojas.append({"n": n, "orador": orador, "html": "\n".join(partes), "seccion": seccion.group(1) if seccion else "",
                      "palabras": sum(len(d.split()) for d in decir)})
        anterior, relevo_anterior = orador, relevo

    def escribir(contenido, destino):
        temporal = AQUI / "_guion_visual.html"
        temporal.write_text(f'<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{ESTILO_VISUAL}</style></head>'
                            f"<body>{contenido}</body></html>", encoding="utf-8")
        try:
            imprimir(temporal, destino)
        finally:
            temporal.unlink()

    escribir("".join(h["html"] for h in hojas), AQUI / "guion_con_diapositivas.pdf")

    for persona in ORADORES:
        propias = [h for h in hojas if h["orador"] == persona]
        turnos = []
        for h in propias:
            if turnos and turnos[-1]["hasta"] == h["n"] - 1:
                turnos[-1]["hasta"] = h["n"]
                turnos[-1]["palabras"] += h["palabras"]
                if h["seccion"] and h["seccion"] not in turnos[-1]["temas"]:
                    turnos[-1]["temas"].append(h["seccion"])
            else:
                turnos.append({"desde": h["n"], "hasta": h["n"], "palabras": h["palabras"],
                               "temas": [h["seccion"]] if h["seccion"] else []})
        filas = "".join(f"<tr><td>{t['desde']}–{t['hasta']}</td><td>{', '.join(t['temas']) or 'Portada y cierre'}</td>"
                        f"<td>{t['palabras'] / 135:.1f} min</td></tr>" for t in turnos)
        total = sum(t["palabras"] for t in turnos) / 135
        portada = (f'<section class="portada-persona"><div class="toca {persona}"><span>Guion de</span><b>{persona}</b>'
                   f"<span>{len(propias)} diapositivas</span></div><h1>Guion de {persona}</h1>"
                   f"<p>Solo las diapositivas que te tocan, con lo que hay que decir, la frase con la que recibes la palabra, "
                   f"el relevo con el que la entregas y la explicación de cada cifra.</p>"
                   f"<p>Tiempo total aproximado: <b>{total:.1f} minutos</b> (a 135 palabras por minuto).</p>"
                   f"<table><tr><th>Diapositivas</th><th>Contenido</th><th>Tiempo</th></tr>{filas}</table></section>")
        escribir(portada + "".join(h["html"] for h in propias), AQUI / f"guion_{persona}.pdf")


if __name__ == "__main__":
    print("diapositivas en el guion:", guion())
    pdf()
    pdf_guion()
    pdf_guion_visual()
    print("PDF:", PDF, PDF.stat().st_size, "bytes")
    print("Guion PDF:", AQUI / "guion_presentador.pdf")
