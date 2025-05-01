import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Inicializar Flask
app = Flask(__name__)
CORS(app)

# Configura las credenciales para acceder a Google Sheets
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

# Ruta del archivo de credenciales JSON
credenciales = 'credenciales.json'

# Autenticación con la API de Google Sheets
credentials = ServiceAccountCredentials.from_json_keyfile_name(credenciales, scope)
client = gspread.authorize(credentials)

# Abre la hoja de cálculo usando el ID de la hoja
SHEET_ID = 'TU_ID_DE_HOJA_DE_CÁLCULO_AQUÍ'
sheet = client.open_by_key(SHEET_ID).sheet1  # Usa la primera hoja

# Ruta principal
@app.route('/')
def index():
    return jsonify({"mensaje": "Servidor Flask está corriendo."})

# Ruta para obtener los nombres de los estudiantes
@app.route('/nombres', methods=['GET'])
def obtener_nombres():
    # Obtén los nombres de la segunda columna de la hoja
    nombres = sheet.col_values(2)[1:]  # Excluye el encabezado
    return jsonify(nombres)

# Ruta para obtener las evaluaciones
@app.route('/evaluaciones', methods=['GET'])
def obtener_evaluaciones():
    # Obtén los datos de las evaluaciones (autoevaluaciones y coevaluaciones)
    data = sheet.get_all_records()  # Devuelve todos los registros como lista de diccionarios
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
