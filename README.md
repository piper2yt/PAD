# Programación para el Análisis de Datos (PAD) — Análisis de Transacciones Financieras

Repositorio del equipo **Lavanderia de Datos** para la materia **Programación para el Análisis de Datos (PAD)** (ITESO, Universidad Jesuita de Guadalajara), estructurado en **Python** (con soporte opcional para **SQLite**).

---

## Equipo e Integrantes

**Equipo:** Lavanderia de Datos

- José Antonio Alvaro Zavala
- Diego Barba Villalobos
- Alonso Ángel Gallardo Vargas
- Evelyn Sofía Ibáñez Martínez
- Sergio Murillo Adabache
- Gustavo Gael Pérez Jiménez

---

## Acerca del proyecto y del dataset

**Tema:** Análisis de Transacciones Financieras.  
**Objetivo preliminar:** Crear gráficas y dashboards para responder preguntas críticas dentro del contexto del negocio, visualizando la información de manera eficiente y concisa, y construir modelos de machine learning para predecir si una transacción bancaria pudiese llegar a ser fraudulenta.

- Propuesta completa (Entrega 1): [`docs/propuesta_proyecto.md`](docs/propuesta_proyecto.md) (incluye copia del documento original `.docx`).
- Relaciones entre tablas y avance del modelo relacional: [`docs/relaciones_tablas.md`](docs/relaciones_tablas.md) (diagrama ER, llaves de cruce, ventana `2014-2019` y foto del pizarrón).

Trabajamos con el dataset público de Kaggle **[Financial Transactions Dataset: Analytics](https://www.kaggle.com/datasets/computingvictor/transactions-fraud-datasets?resource=download)** (`computingvictor/transactions-fraud-datasets`), cuyos archivos principales son:

| Archivo | Formato | Descripción |
| :--- | :---: | :--- |
| `transactions_data.csv` | CSV | Registro detallado de transacciones (fecha, monto, cliente, tarjeta, comercio, ciudad, estado, `mcc`, canal de pago y errores). |
| `cards_data.csv` | CSV | Información de tarjetas de crédito y débito (marca, tipo, chip, límite de crédito, fecha de apertura). |
| `users_data.csv` | CSV | Datos demográficos y financieros de los clientes (edad, género, ubicación, ingresos, deuda total, score crediticio). |
| `mcc_codes.json` | JSON | Catálogo descriptivo de giros comerciales (*Merchant Category Codes*). |
| `train_fraud_labels.json` | JSON | Etiquetas binarias de fraude (`Yes` / `No`) vinculadas a cada transacción (`transaction_id`). |

> **Nota sobre archivos pesados:** Ningún archivo `.zip`, `.csv`, `.sqlite`, `.sqlite3`, `.db`, `.json` dentro de `data/` ni `.env` se sube al repositorio (están bloqueados en `.gitignore`). Cada integrante descarga el dataset localmente en `data/raw_data/` y guarda sus salidas procesadas localmente en `data/procesamiento_data/`.

---

## Preguntas base de investigación

| # | Pregunta base (Entrega 1) | Apartado en el repositorio |
| :-: | :--- | :--- |
| **1** | ¿Cómo podemos predecir si una transacción específica es fraudulenta utilizando el historial transaccional previo y los patrones de comportamiento del cliente? | [`notebooks_preguntas/pregunta_1_prediccion_fraude/`](notebooks_preguntas/pregunta_1_prediccion_fraude/pregunta_1_prediccion_fraude.ipynb) |
| **2** | ¿Cuál es el porcentaje total de las transacciones fraudulentas vs legítimas, cuál es el monto promedio por sucursal? | [`notebooks_preguntas/pregunta_2_fraude_y_sucursales/`](notebooks_preguntas/pregunta_2_fraude_y_sucursales/pregunta_2_fraude_y_sucursales.ipynb) |
| **3** | Teniendo en cuenta los datos demográficos y el perfil financiero de un usuario, ¿qué límite de crédito le asignaría normalmente un banco, y qué usuarios tienen un límite excesivo o insuficiente en relación con esa cifra? | [`notebooks_preguntas/pregunta_3_limite_credito/`](notebooks_preguntas/pregunta_3_limite_credito/pregunta_3_limite_credito.ipynb) |
| **Extra** | Exploración del pizarrón: series de tiempo (`2014-2019`), género vs. tipo de tarjeta (`Debit`/`Credit`) e ingreso anual vs. monto total transaccionado. | [`notebooks_preguntas/exploracion_pizarron/`](notebooks_preguntas/exploracion_pizarron/exploracion_relaciones_y_series.ipynb) |

---

## Estructura de carpetas

```text
PAD/
├── data/
│   ├── .gitkeep
│   ├── raw_data/                                   # Apartado "raw data": archivos originales de Kaggle sin modificar
│   │   └── .gitkeep
│   └── procesamiento_data/                         # Apartado "procesamiento data": datos limpios/procesados y proyecto.sqlite
│       └── .gitkeep
├── docs/                                           # Documentación del proyecto y avance de relaciones entre tablas
│   ├── img/
│   │   └── relaciones_tablas_pizarron.png          # Foto original del pizarrón con relaciones entre tablas
│   ├── Entrega_1_Proyecto_Final_Programacion_para_Analisis_de_Datos.docx
│   ├── propuesta_proyecto.md                       # Propuesta de Entrega 1 en Markdown
│   └── relaciones_tablas.md                        # Diagrama ER, llaves de cruce y notas de análisis
├── notebooks_preguntas/                            # Módulo donde va el código de los notebooks para responder las preguntas
│   ├── pregunta_1_prediccion_fraude/
│   │   └── pregunta_1_prediccion_fraude.ipynb      # Respuesta y modelado para la Pregunta 1
│   ├── pregunta_2_fraude_y_sucursales/
│   │   └── pregunta_2_fraude_y_sucursales.ipynb    # Respuesta y gráficas para la Pregunta 2
│   ├── pregunta_3_limite_credito/
│   │   └── pregunta_3_limite_credito.ipynb         # Respuesta y estimación para la Pregunta 3
│   └── exploracion_pizarron/
│       └── exploracion_relaciones_y_series.ipynb   # Exploración adicional y series de tiempo (2014-2019)
├── sql/
│   └── consultas.sql                               # Consultas SQLite de ejemplo comentadas en español (opcional)
├── src/                                            # Código fuente Python para limpieza y procesamiento de datos
│   ├── limpieza_datos.py                           # Apartado base para limpieza y transformación de datos
│   └── crear_db.py                                 # Script ETL opcional para generar proyecto.sqlite por bloques
├── .gitignore                                      # Reglas de exclusión de Python, datos locales y credenciales
├── LICENSE                                         # Licencia MIT (2026)
├── README.md                                       # Documentación y guía de inicio del proyecto
└── requirements.txt                                # Dependencias Python del proyecto
```

### ¿Qué va en cada apartado?
- **Raw Data (`data/raw_data/`)**: archivos originales descargados desde Kaggle (`transactions_data.csv`, `cards_data.csv`, `users_data.csv`, `mcc_codes.json`, `train_fraud_labels.json`). No se modifican manualmente.
- **Procesamiento Data (`data/procesamiento_data/`)**: archivos resultantes de la limpieza y transformación de datos (CSVs limpios, `.parquet` o `proyecto.sqlite` si utilizas SQLite).
- **Documentación y Relaciones (`docs/`)**: propuesta del proyecto (Entrega 1) y el apartado [`docs/relaciones_tablas.md`](docs/relaciones_tablas.md) para consultar en cualquier momento las relaciones entre tablas.
- **Limpieza y código de procesamiento (`src/`)**: scripts Python encargados de limpiar, filtrar y transformar los datos (`src/limpieza_datos.py`) o cargarlos en SQLite (`src/crear_db.py`, opcional).
- **Notebooks — Código para las preguntas (`notebooks_preguntas/`)**: carpetas separadas para cada pregunta base del documento y la exploración del pizarrón, listas para ir desarrollando el código paso a paso.

---

## Regla de comentarios del equipo

En todos los apartados de limpieza (`src/limpieza_datos.py`) y de respuestas a las preguntas (`notebooks_preguntas/`):

> Por cada cambio que hagan en el código o módulo que añadan, escriban un comentario para entender qué es lo que hace su código / función, por qué decidieron implementar esta solución, etc.

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

*(Opcional)* Para sincronizar tu fork con cambios del repositorio original, agrega el remoto `upstream`:

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

### 4. Descargar el dataset de Kaggle y colocar los archivos en `data/raw_data/`
1. Descarga el dataset desde Kaggle:  
   **https://www.kaggle.com/datasets/computingvictor/transactions-fraud-datasets?resource=download**
2. Descomprime el archivo `.zip` descargado.
3. Copia los archivos `.csv` (y los `.json`: `mcc_codes.json`, `train_fraud_labels.json`) directamente dentro de **`data/raw_data/`** sin borrar `.gitkeep`.

Tu carpeta `data/` local debería verse así:

```text
data/
├── .gitkeep
├── raw_data/
│   ├── .gitkeep
│   ├── cards_data.csv
│   ├── mcc_codes.json
│   ├── train_fraud_labels.json
│   ├── transactions_data.csv
│   └── users_data.csv
└── procesamiento_data/
    └── .gitkeep
```

### 5. (Opcional) Generar la base de datos SQLite (`data/procesamiento_data/proyecto.sqlite`)
Si vas a trabajar con **SQLite** (en lugar de leer los `.csv` directamente desde Python), ejecuta el script de carga por bloques desde la raíz del repositorio:

```bash
python src/crear_db.py
```

El script detectará automáticamente todos los `.csv` dentro de `data/raw_data/`, los leerá en bloques (*chunks*) de 100,000 filas por defecto para cuidar la memoria RAM y creará la base local `data/procesamiento_data/proyecto.sqlite`.

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

### Notebooks por pregunta (`notebooks_preguntas/`)
Con el entorno virtual activado, inicia Jupyter y abre el notebook correspondiente a tu pregunta:

```bash
jupyter notebook
```
*(También puedes usar `jupyter lab` o abrir los archivos `.ipynb` directamente en VS Code seleccionando el intérprete `.venv`.)*

### Consultas SQL en SQLite *(opcional)*
Si trabajas con `data/procesamiento_data/proyecto.sqlite`, el archivo `sql/consultas.sql` incluye consultas listas y comentadas en español. Puedes ejecutarlas con:
- **DB Browser for SQLite** (interfaz gráfica).
- La extensión **SQLite** / **SQLTools** en VS Code.
- La terminal con `sqlite3 data/procesamiento_data/proyecto.sqlite`.

---

## Buenas prácticas con Git

- Antes de hacer `git add` o `git commit`, revisa siempre `git status` para confirmar que **no** estás rastreando archivos pesados (`.csv`, `.zip`, `.sqlite`, `.sqlite3`, `.db`) ni archivos de credenciales (`.env`).
- No elimines los archivos `.gitkeep` dentro de `data/`, `data/raw_data/` ni `data/procesamiento_data/`: permiten que Git conserve las carpetas vacías en el repositorio remoto.
- Trabaja cada pregunta o cambio de limpieza en una rama dedicada (`git checkout -b pregunta-1/modelo-base`) y documenta en comentarios qué hace tu código y por qué elegiste esa solución.

---

## Licencia

Este proyecto se distribuye bajo la **Licencia MIT**. Consulta el archivo [`LICENSE`](LICENSE) para más detalles.
