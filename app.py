from flask import Flask, render_template
import analyzer
import database
import sqlite3
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Asegurar que la BD esté lista
    database.inicializar_base_datos()
    
    blancas, powerball = analyzer.sugerir_numeros()
    stats = analyzer.obtener_calientes_frios()
    
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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)