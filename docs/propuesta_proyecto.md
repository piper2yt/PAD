# Entrega 1: Propuesta de Proyecto Final

**Institución:** ITESO, Universidad Jesuita de Guadalajara  
**Materia:** Programación para el Análisis de Datos (PAD)  
**Nombre del equipo:** Lavanderia de Datos  
**Documento original:** [`Entrega_1_Proyecto_Final_Programacion_para_Analisis_de_Datos.docx`](Entrega_1_Proyecto_Final_Programacion_para_Analisis_de_Datos.docx)

---

## 1. Integrantes del equipo

- José Antonio Alvaro Zavala
- Diego Barba Villalobos
- Alonso Ángel Gallardo Vargas
- Evelyn Sofía Ibáñez Martínez
- Sergio Murillo Adabache
- Gustavo Gael Pérez Jiménez

---

## 2. Tema propuesto

**Análisis de Transacciones Financieras.**

---

## 3. Objetivo preliminar

Crear gráficas y dashboards para responder preguntas críticas dentro del contexto del negocio, visualizando la información de manera eficiente y concisa, y construir modelos de machine learning para predecir si una transacción bancaria pudiese llegar a ser fraudulenta.

---

## 4. Base de datos candidata

- **Nombre:** Transactions Fraud Datasets (ComputingVictor) — *Financial Transactions Dataset: Analytics*
- **Fuente en Kaggle:** https://www.kaggle.com/datasets/computingvictor/transactions-fraud-datasets?select=transactions_data.csv

El dataset contiene información de transacciones bancarias, tarjetas de crédito/débito y datos demográficos de clientes, organizado en los siguientes archivos:

| Archivo | Descripción |
| :--- | :--- |
| `transactions_data.csv` | Registros de transacciones individuales (monto, fecha, hora, tipo de chip, comercio, ciudad, estado, código de comerciante `mcc` y errores). |
| `cards_data.csv` | Detalles de las tarjetas emitidas por usuario (marca de tarjeta, tipo de tarjeta, límite de crédito, fecha de apertura de cuenta). |
| `users_data.csv` | Perfil demográfico y financiero de los clientes (edad, género, ingresos anuales, deuda total, score crediticio y ubicación). |
| `mcc_codes.json` | Catálogo descriptivo de giros comerciales según su código *Merchant Category Code* (`mcc`). |
| `train_fraud_labels.json` | Etiquetas de fraude asociadas a cada transacción (`transaction_id`), necesarias para análisis y predicción de fraude. |

---

## 5. Preguntas base de investigación y ubicación en el repositorio

Cada pregunta cuenta con su propio apartado en `notebooks_preguntas/` para trabajar de forma ordenada y evitar conflictos entre integrantes:

| # | Pregunta de investigación | Apartado en el repositorio |
| :-: | :--- | :--- |
| **1** | ¿Cómo podemos predecir si una transacción específica es fraudulenta utilizando el historial transaccional previo y los patrones de comportamiento del cliente? | [`notebooks_preguntas/pregunta_1_prediccion_fraude/`](../notebooks_preguntas/pregunta_1_prediccion_fraude/pregunta_1_prediccion_fraude.ipynb) |
| **2** | ¿Cuál es el porcentaje total de las transacciones fraudulentas vs legítimas, cuál es el monto promedio por sucursal? | [`notebooks_preguntas/pregunta_2_fraude_y_sucursales/`](../notebooks_preguntas/pregunta_2_fraude_y_sucursales/pregunta_2_fraude_y_sucursales.ipynb) |
| **3** | Teniendo en cuenta los datos demográficos y el perfil financiero de un usuario, ¿qué límite de crédito le asignaría normalmente un banco, y qué usuarios tienen un límite excesivo o insuficiente en relación con esa cifra? | [`notebooks_preguntas/pregunta_3_limite_credito/`](../notebooks_preguntas/pregunta_3_limite_credito/pregunta_3_limite_credito.ipynb) |

Adicionalmente, las preguntas exploratorias y notas de series de tiempo levantadas en el pizarrón se agrupan en:
- [`notebooks_preguntas/exploracion_pizarron/`](../notebooks_preguntas/exploracion_pizarron/exploracion_relaciones_y_series.ipynb)
- Modelo relacional y avance de cruces entre tablas: [`docs/relaciones_tablas.md`](relaciones_tablas.md)
