import sqlite3
import csv
import os
import requests

NOMBRE_DB = '/tmp/powerball.db' if os.environ.get('RENDER') else 'powerball.db'
URL_CSV = 'https://data.ny.gov/api/views/d6yy-54nr/rows.csv?accessType=DOWNLOAD'
RUTA_CSV = '/tmp/powerball_numbers.csv' if os.environ.get('RENDER') else 'data/powerball_numbers.csv'

def descargar_csv():
    os.makedirs(os.path.dirname(RUTA_CSV), exist_ok=True)
    if not os.path.exists(RUTA_CSV):
        print(f"Descargando datos históricos desde {URL_CSV}...")
        response = requests.get(URL_CSV)
        response.raise_for_status()
        with open(RUTA_CSV, 'wb') as f:
            f.write(response.content)
        print("Descarga completada.")

def crear_tablas():
    conn = sqlite3.connect(NOMBRE_DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS draws (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            draw_date TEXT UNIQUE NOT NULL,
            white_1 INTEGER,
            white_2 INTEGER,
            white_3 INTEGER,
            white_4 INTEGER,
            white_5 INTEGER,
            powerball INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def cargar_csv():
    conn = sqlite3.connect(NOMBRE_DB)
    c = conn.cursor()
    with open(RUTA_CSV, 'r', encoding='utf-8') as f:
        lector = csv.reader(f)
        next(lector)
        for fila in lector:
            try:
                fecha = fila[0]
                nums = fila[1].strip().split()
                if len(nums) != 6:
                    continue
                w1, w2, w3, w4, w5, pb = map(int, nums)
                c.execute('''
                    INSERT OR IGNORE INTO draws
                    (draw_date, white_1, white_2, white_3, white_4, white_5, powerball)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (fecha, w1, w2, w3, w4, w5, pb))
            except Exception as e:
                print(f"Error en fila {fila}: {e}")
    conn.commit()
    conn.close()
    print("¡Datos cargados exitosamente!")

def inicializar_base_datos():
    descargar_csv()
    crear_tablas()
    cargar_csv()

if __name__ == '__main__':
    inicializar_base_datos()