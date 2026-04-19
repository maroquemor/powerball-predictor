import sqlite3
from collections import Counter

NOMBRE_DB = 'powerball.db'

def analizar_frecuencias(limite=100):
    """Cuenta las frecuencias de números blancos y powerball en los últimos 'limite' sorteos."""
    conn = sqlite3.connect(NOMBRE_DB)
    c = conn.cursor()
    c.execute('''
        SELECT white_1, white_2, white_3, white_4, white_5, powerball
        FROM draws ORDER BY draw_date DESC LIMIT ?
    ''', (limite,))
    filas = c.fetchall()
    conn.close()

    contador_blancas = Counter()
    contador_power = Counter()

    for fila in filas:
        for i in range(5):
            contador_blancas[fila[i]] += 1
        contador_power[fila[5]] += 1

    return contador_blancas, contador_power

def sugerir_numeros():
    """Devuelve una combinación sugerida: 5 blancas + 1 powerball."""
    blancas_freq, power_freq = analizar_frecuencias(limite=200)
    
    # Tomar los 5 números blancos más frecuentes
    mas_comunes_blancas = [num for num, _ in blancas_freq.most_common(5)]
    mas_comunes_blancas.sort()
    
    # Tomar el powerball más frecuente
    powerball_sugerido = power_freq.most_common(1)[0][0]
    
    return mas_comunes_blancas, powerball_sugerido

def obtener_calientes_frios():
    """Devuelve listas de números calientes y fríos (todos los sorteos)."""
    conn = sqlite3.connect(NOMBRE_DB)
    c = conn.cursor()
    c.execute('SELECT white_1, white_2, white_3, white_4, white_5, powerball FROM draws')
    filas = c.fetchall()
    conn.close()

    contador_blancas = Counter()
    contador_power = Counter()

    for fila in filas:
        for i in range(5):
            contador_blancas[fila[i]] += 1
        contador_power[fila[5]] += 1

    # Calientes: los 10 más frecuentes
    calientes_blancas = [num for num, _ in contador_blancas.most_common(10)]
    calientes_power = [num for num, _ in contador_power.most_common(5)]

    # Fríos: números que nunca han salido (o los menos frecuentes)
    todos_blancas = set(range(1, 70))
    todos_power = set(range(1, 27))
    
    aparecidos_blancas = set(contador_blancas.keys())
    aparecidos_power = set(contador_power.keys())

    frios_blancas = list(todos_blancas - aparecidos_blancas)
    frios_power = list(todos_power - aparecidos_power)

    if not frios_blancas:
        frios_blancas = [num for num, _ in contador_blancas.most_common()[-10:]]
    if not frios_power:
        frios_power = [num for num, _ in contador_power.most_common()[-5:]]

    return {
        'calientes_blancas': calientes_blancas,
        'calientes_power': calientes_power,
        'frios_blancas': frios_blancas[:10],
        'frios_power': frios_power[:5]
    }
