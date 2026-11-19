# Programación Análisis de Datos (PAD) — Análisis de Transacciones Financieras

Repositorio base para la materia **Programación Análisis de Datos (PAD)**, diseñado como plantilla reproducible de análisis y ciencia de datos con **Python + SQLite**.

---

## Acerca del proyecto y del dataset

El objetivo de este proyecto es ingestar, consultar, explorar y analizar datos transaccionales bancarios a gran escala de manera local y eficiente sin saturar la memoria RAM, combinando procesamiento por bloques en **Python**, almacenamiento relacional ligero en **SQLite** y análisis exploratorio en **Jupyter Notebooks**.

Trabajamos con el dataset público de Kaggle **[Financial Transactions Dataset: Analytics](https://www.kaggle.com/datasets/computingvictor/transactions-fraud-datasets?resource=download)**, el cual reúne registros financieros de la década de 2010 orientados a análisis de comportamiento de clientes, patrones de gasto y detección de fraude. Sus archivos principales son:

| Archivo | Formato | Descripción |
| :--- | :---: | :--- |
| `transactions_data.csv` | CSV | Registro detallado de transacciones (fecha, monto, cliente, tarjeta, comercio, canal de pago y errores). Es el archivo más grande del dataset. |
| `cards_data.csv` | CSV | Información de tarjetas de crédito y débito (marca, tipo, chip, límite de crédito, fecha de apertura). |
| `users_data.csv` | CSV | Datos demográficos y financieros de los clientes (edad, género, ubicación, ingresos, deuda total, puntaje crediticio). |
| `mcc_codes.json` *(opcional)* | JSON | Catálogo de códigos de categoría comercial (*Merchant Category Codes*). |
| `train_fraud_labels.json` *(opcional)* | JSON | Etiquetas binarias de fraude para entrenamiento supervisado. |

> **Nota sobre archivos pesados:** Ningún archivo `.zip`, `.csv`, `.sqlite`, `.sqlite3`, `.db` ni `.env` se sube al repositorio (están bloqueados en `.gitignore`). Cada estudiante descarga el dataset localmente y genera su propia base `data/proyecto.sqlite`.

---

## Estructura de carpetas

```text
PAD/
├── data/
│   └── .gitkeep                # Mantiene la carpeta data/ versionada en Git (vacía en el repo)
├── notebooks/
│   └── 01_exploracion.ipynb    # Notebook inicial de EDA conectado a data/proyecto.sqlite
├── sql/
│   └── consultas.sql           # Consultas SQLite de ejemplo comentadas en español
├── src/
│   └── crear_db.py             # Script ETL que carga los .csv de data/ por bloques a SQLite
├── .gitignore                  # Reglas de exclusión de Python, datos locales y credenciales
├── LICENSE                     # Licencia MIT (2026)
├── README.md                   # Documentación y guía de inicio del proyecto
└── requirements.txt            # Dependencias Python del proyecto
```

---

## Guía paso a paso para compañeros de clase

Sigue estos pasos para crear tu propia copia del repositorio y dejar listo tu entorno local de trabajo.

### 1. Hacer Fork del repositorio
1. Ingresa al repositorio principal en GitHub: **`https://github.com/piper2yt/PAD`**.
2. Haz clic en el botón **Fork** (esquina superior derecha) para crear una copia bajo tu propia cuenta de GitHub.

### 2. Clonar tu Fork en tu computadora
Reemplaza `<tu-usuario>` por tu nombre de usuario de GitHub y ejecuta:

```bash
git clone https://github.com/<tu-usuario>/PAD.git
cd PAD
```

*(Opcional)* Si deseas mantener sincronizado tu fork con los cambios del repositorio original, agrega el remoto `upstream`:

```bash
git remote add upstream https://github.com/piper2yt/PAD.git
```

### 3. Crear el entorno virtual e instalar dependencias
Se recomienda aislar las librerías del proyecto en un entorno virtual (Python 3.10 o superior):

**Crear el entorno virtual:**
```bash
python -m venv .venv
```
*(En algunos sistemas macOS/Linux utiliza `python3 -m venv .venv`.)*

**Activar el entorno virtual:**
- **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
- **Windows (CMD):**
  ```cmd
  .venv\Scripts\activate.bat
  ```
- **macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```

**Instalar las dependencias desde `requirements.txt`:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Descargar el dataset de Kaggle y colocar los CSV en `data/`
1. Descarga el dataset desde Kaggle:  
   **https://www.kaggle.com/datasets/computingvictor/transactions-fraud-datasets?resource=download**
2. Descomprime el archivo `.zip` descargado.
3. Copia los archivos `.csv` (`transactions_data.csv`, `cards_data.csv`, `users_data.csv`) directamente dentro de la carpeta **`data/`** del repositorio (sin borrar `data/.gitkeep`).

Tu carpeta `data/` local debería verse así:

```text
data/
├── .gitkeep
├── cards_data.csv
├── transactions_data.csv
└── users_data.csv
```

### 5. Generar la base de datos SQLite (`data/proyecto.sqlite`)
Ejecuta el script de carga por bloques desde la raíz del repositorio:

```bash
python src/crear_db.py
```

El script detectará automáticamente todos los `.csv` dentro de `data/`, los leerá en bloques (*chunks*) de 100,000 filas por defecto para cuidar la memoria RAM y creará la base local `data/proyecto.sqlite`.

**Opciones útiles del script:**
- Ajustar el tamaño de bloque si tu equipo tiene poca RAM:
  ```bash
  python src/crear_db.py --chunksize 50000
  ```
- Crear índices automáticos sobre columnas clave (`id`, `client_id`, `card_id`, `date`, `mcc`) para acelerar consultas `JOIN`:
  ```bash
  python src/crear_db.py --crear-indices
  ```

---

## Primeros pasos con el análisis

### Análisis Exploratorio (EDA) en Jupyter
Con el entorno virtual activado, inicia Jupyter y abre `notebooks/01_exploracion.ipynb`:

```bash
jupyter notebook
```
*(También puedes usar `jupyter lab` o abrir el archivo `.ipynb` directamente en VS Code seleccionando el intérprete `.venv`.)*

### Consultas SQL en SQLite
El archivo `sql/consultas.sql` incluye consultas listas y comentadas en español (exploración de esquema, agregaciones por canal de pago, errores, estados, códigos MCC, series anuales y `JOIN` entre transacciones, tarjetas y clientes). Puedes ejecutarlas con:
- **DB Browser for SQLite** (interfaz gráfica).
- La extensión **SQLite** / **SQLTools** en VS Code.
- La terminal con `sqlite3 data/proyecto.sqlite`.

---

## Buenas prácticas con Git

- Antes de hacer `git add` o `git commit`, revisa siempre `git status` para confirmar que **no** estás rastreando archivos pesados (`.csv`, `.zip`, `.sqlite`, `.sqlite3`, `.db`) ni archivos de credenciales (`.env`).
- No elimines `data/.gitkeep`: permite que Git conserve la carpeta `data/` vacía en el repositorio remoto.
- Trabaja tus entregas o experimentos en ramas dedicadas (`git checkout -b analisis/mi-tema`).

---

## Licencia

Este proyecto se distribuye bajo la **Licencia MIT**. Consulta el archivo [`LICENSE`](LICENSE) para más detalles.
