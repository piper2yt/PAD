"""Módulo base para la limpieza y procesamiento de datos del proyecto PAD.

Equipo: Lavanderia de Datos
Entradas esperadas:  data/raw_data/
Salidas esperadas:   data/procesamiento_data/
Referencia de cruces: docs/relaciones_tablas.md

REGLA DE DOCUMENTACION DEL EQUIPO (OBLIGATORIA):
Por cada cambio que hagan en el código o módulo que añadan, escriban un
comentario para entender qué es lo que hace su código / función, por qué
decidieron implementar esta solución, etc.

Formato sugerido para comentar cada función o bloque nuevo:
    # Autor: <tu nombre>
    # Qué hace: <descripción breve de la transformación o limpieza>
    # Por qué se implementó así: <criterio técnico o de negocio elegido>
    # Entradas / Salidas: <columnas o archivos que recibe y genera>
"""

# -----------------------------------------------------------------------------
# 1. IMPORTACIONES Y RUTAS DEL PROYECTO
# -----------------------------------------------------------------------------
# Por cada cambio que hagan en el código o módulo que añadan, escriban un
# comentario para entender qué es lo que hace su código / función, por qué
# decidieron implementar esta solución, etc.
#
# Sugerencia: definir rutas relativas a la raíz del repositorio hacia
# `data/raw_data/` (lectura) y `data/procesamiento_data/` (escritura).

# Autor: Diego Barba Villalobos
# Qué hace: <descripción breve de la transformación o limpieza>
# Por qué se implementó así: <criterio técnico o de negocio elegido>
# Entradas / Salidas: <columnas o archivos que recibe y genera>
import pandas as pd
raw_data_path = 'data/raw_data'
process_data = 'data/procesamiento_data'

# -----------------------------------------------------------------------------
# 2. CARGA DE DATOS CRUDOS (data/raw_data/)
# -----------------------------------------------------------------------------
# Espacio para funciones de carga de:
# - transactions_data.csv (considerar lectura por bloques o columnas necesarias)
# - cards_data.csv
# - users_data.csv
# - mcc_codes.json
# - train_fraud_labels.json
# Recuerda comentar qué hace cada función y por qué se implementó de esa forma.

user_data = pd.read_csv(raw_data_path+'/users_data.csv')
card_data = pd.read_csv(raw_data_path+'/cards_data.csv')
transcations_data = pd.read_csv(raw_data_path+'/transactions_data.csv')
mcc_codes = pd.read_json(raw_data_path+'/mcc_codes.json',typ='series').to_frame()
fraud_labes = pd.read_json(raw_data_path+'/train_fraud_labels.json')

# -----------------------------------------------------------------------------
# 3. LIMPIEZA Y TRANSFORMACION DE COLUMNAS
# -----------------------------------------------------------------------------
# Espacio para limpieza de datos, por ejemplo:
# - Conversión de columnas monetarias con signo '$' a formato numérico.
# - Conversión de fechas (`date`, `acct_open_date`) y filtrado de ventana
#   temporal (5 años: 2014-2019 según lo acordado en el pizarrón).
# - Tratamiento de valores nulos, duplicados y tipos de datos.
# Por cada regla de limpieza que añadan, escriban un comentario explicando
# qué hace y por qué tomaron esa decisión.

# Cambiar columnas para mejor Indexacion
mcc_codes.rename(columns={0:'category'},inplace=True)
mcc_codes.rename_axis('Code',inplace=True)
fraud_labes.rename(columns={'target':'fraud'},inplace=True)
fraud_labes.rename_axis('Code',inplace=True)

# Cambiar transcations_data["amount"] a float
transcations_data['amount'] = pd.to_numeric(transcations_data["amount"].str.replace("$", "", regex=False), errors="coerce")

# Agregar ONLINE a 'merchant_state' y para 'zip' hacerlo 0, para cuando 'merchant_city' es ONLINE
transcations_data.loc[transcations_data['merchant_city'] == 'ONLINE', ['merchant_state']] = 'ONLINE'
transcations_data.loc[transcations_data['merchant_city'] == 'ONLINE', ['zip']] = 0

# -----------------------------------------------------------------------------
# 4. INTEGRACION DE TABLAS (SEGUN docs/relaciones_tablas.md)
# -----------------------------------------------------------------------------
# Espacio para unir tablas mediante sus llaves (`client_id`, `card_id`, `mcc`,
# `transaction_id`) si el equipo decide generar tablas ya integradas en
# `data/procesamiento_data/`.
# Documenta con comentarios qué tipo de unión (left, inner, etc.) elegiste y por qué.

# Agregar 'purchase_category' a transcations_data
mcc_dict = mcc_codes['category'].to_dict()
transcations_data["purchase_category"] = transcations_data["mcc"].map(mcc_dict)

# Agregar 'is_fraud' a transcations_data
id_fraud = fraud_labes[fraud_labes["fraud"]=="Yes"].index
transcations_data["is_fraud"] = transcations_data["id"].isin(id_fraud)

# -----------------------------------------------------------------------------
# 5. EXPORTACION DE DATOS PROCESADOS (data/procesamiento_data/)
# -----------------------------------------------------------------------------
# Espacio para guardar los archivos limpios en `data/procesamiento_data/`
# (por ejemplo en formato .csv o .parquet, ignorados automáticamente por Git).
# Comenta qué archivos se generan y qué notebook de `notebooks_preguntas/` los consume.
