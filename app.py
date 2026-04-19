from flask import Flask, render_template
import analyzer
import database
import sqlite3

app = Flask(__name__)

# Crear las tablas en la base de datos si no existen
database.crear_tablas()

@app.route('/')
def index():
    # Obtener números sugeridos basados en frecuencia
    blancas, powerball = analyzer.sugerir_numeros()

    # Obtener números calientes y fríos
    stats = analyzer.obtener_calientes_frios()

    # Contar cuántos sorteos hay en la base de datos
    conn = sqlite3.connect(database.NOMBRE_DB)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM draws')
    total = c.fetchone()[0]
    conn.close()

    return render_template('index.html',
                           blancas=blancas,
                           powerball=powerball,
                           stats=stats,
                           total=total)

if __name__ == '__main__':
    app.run(debug=True)
