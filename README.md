# proyecto-final-gestion-datos

Repositorio para el proyecto final de la clase de **Gestión de Datos** (Departamento de Ingeniería de Sistemas, Universidad de los Andes).

**Caso de estudio:** Monitoreo de reputación de marca Davivienda usando datos de quejas y sanciones de fuentes oficiales colombianas.

---

## Cómo reproducir los datos

Los datos utilizados en este proyecto se descargan automáticamente desde el portal **[datos.gov.co](https://www.datos.gov.co/)** (datos abiertos del gobierno colombiano) mediante el cuaderno `00_Extraccion_datos_gov.ipynb`.

### Requisitos

- **Python 3.7+** o acceso a **Google Colab**
- Librerías: `pandas`, `requests` (ya vienen instaladas en Colab)

### Opción 1: Google Colab (recomendado)

1. Abre el cuaderno en Colab:
   - Ve a [colab.research.google.com](https://colab.research.google.com/)
   - Sube o abre `00_Extraccion_datos_gov.ipynb`

2. *(Opcional)* Configura tu token de acceso (acelera las descargas):
   - Regístrate en [datos.gov.co](https://www.datos.gov.co/)
   - Copia tu token desde "App Tokens"
   - En Colab: 🔑 **Secrets** → Agregar secreto → `SOCRATA_APP_TOKEN` → Pega tu token

3. Ejecuta el cuaderno:
   - **Runtime** → **Run all** (Ctrl + F9)
   - Los datos se guardarán en `datos/raw/`
   - Descárgalos desde la carpeta **Files**

### Opción 2: En tu máquina (Windows, Mac, Linux)

1. **Instala Jupyter y dependencias:**
   ```bash
   pip install jupyter pandas requests
   ```

2. *(Opcional)* **Configura el token:**
   - Copia `.env.example` a `.env`
   - Edita `.env` y añade tu token:
     ```
     SOCRATA_APP_TOKEN=tu_token_aqui
     ```

3. **Ejecuta el cuaderno:**
   ```bash
   jupyter notebook 00_Extraccion_datos_gov.ipynb
   ```
   - Dentro de Jupyter: **Kernel** → **Restart & Run All**

### Datasets descargados

El cuaderno descarga tres datasets principales:

| Dataset | Fuente | Período | Propósito |
|---|---|---|---|
| `quejas_sfc.csv` | Superintendencia Financiera | 2010–2022 | Quejas principales contra Davivienda |
| `quejas_smartsupervision.csv` | SFC (Smartsupervision) | 2023–2026 | Continuación con datos geográficos |
| `sanciones_sic.csv` | SIC | 2013–2026 | Sanciones del sector financiero (contexto) |
| `metadatos.json` | Generado | — | Hashes SHA-256, filtros aplicados, fechas |

Todos se guardan en **`datos/raw/`** sin transformaciones.

### Consideraciones importantes

- **Sin token:** Las descargas funcionan, pero con límite de velocidad (30 req/min). Pueden tardar más si hay mucho volumen.
- **Token gratuito:** No tiene costo, se obtiene en [datos.gov.co](https://www.datos.gov.co/) tras registrarse.
- **Huecos de datos:** Se han identificado gaps en la serie temporal (ej., 2022-Q2 a Q4 para Davivienda). Se documentan en `metadatos.json`.
- **Validación:** Todos los archivos incluyen hash SHA-256 para verificar integridad.

--- 
