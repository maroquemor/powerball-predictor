import sqlite3
import csv
import os

NOMBRE_DB = 'powerball.db'

def crear_tablas():
    """Crea la tabla de sorteos si no existe."""
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

def cargar_csv(ruta_csv='data/powerball_numbers.csv'):
    """Carga los datos desde un archivo CSV a la base de datos."""
    if not os.path.exists(ruta_csv):
        print(f"ERROR: No se encontró el archivo {ruta_csv}")
        print("Por favor, descarga el CSV desde Data.gov y colócalo en la carpeta 'data'.")
        return

    conn = sqlite3.connect(NOMBRE_DB)
    c = conn.cursor()

    with open(ruta_csv, 'r', encoding='utf-8') as f:
        # El CSV de Data.gov tiene las columnas: Draw Date,Winning Numbers,Multiplier
        # "Winning Numbers" viene como "10 22 35 48 61 15" (5 blancas + powerball)
        lector = csv.reader(f)
        encabezado = next(lector)  # saltar encabezado
        
        for fila in lector:
            try:
                fecha = fila[0]
                numeros_str = fila[1]
                # Separar los números por espacio
                nums = numeros_str.strip().split()
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

if __name__ == '__main__':
    crear_tablas()
    cargar_csv()
