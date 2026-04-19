from flask import Flask, render_template
import analyzer
import database
import sqlite3
import os

app = Flask(__name__)

# ¡Importante! Inicializar la base de datos al arrancar
database.inicializar_base_datos()

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
from flask import Flask, render_template
import analyzer
import database
import sqlite3
import os  # <-- Añade esta línea

app = Flask(__name__)
database.crear_tablas()

# ... (tus rutas y lógica existente) ...

if __name__ == '__main__':
    # Modifica estas líneas:
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
