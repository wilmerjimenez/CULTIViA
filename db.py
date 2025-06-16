import sqlite3

def init_db():
    conn = sqlite3.connect('cultivia.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS clima (
                        fecha TEXT, temp REAL, precipitacion REAL,
                        humedad REAL, spi REAL, spei REAL, alerta TEXT
                      )''')
    conn.commit()
    conn.close()

def guardar_dato(fecha, temp, precip, humedad, spi, spei, alerta):
    conn = sqlite3.connect('cultivia.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO clima VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (fecha, temp, precip, humedad, spi, spei, alerta))
    conn.commit()
    conn.close()
