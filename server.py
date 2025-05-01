import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# Inicializar Flask
app = Flask(__name__)
CORS(app)

# Configura el alcance para acceder a Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    'https://www.googleapis.com/auth/spreadsheets',
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Cargar credenciales desde la variable de entorno
credentials_json = os.getenv('GOOGLE_CREDENTIALS')

if credentials_json is None:
    raise ValueError("La variable de entorno 'GOOGLE_CREDENTIALS' no está definida.")

credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    json.loads(credentials_json), scope
)
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
    nombres = sheet.col_values(2)[1:]  # Excluye el encabezado
    return jsonify(nombres)

# Ruta para obtener las evaluaciones
@app.route('/evaluaciones', methods=['GET'])
def obtener_evaluaciones():
    data = sheet.get_all_records()
    return jsonify(data)

# Ruta para mostrar una página HTML (si usas index.html)
@app.route("/pagina")
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)