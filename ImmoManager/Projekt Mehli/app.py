from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DATABASE = 'immobilien.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Alle Immobilien als JSON abrufen
@app.route('/api/immobilien', methods=['GET'])
def get_immobilien():
    conn = get_db()
    immos = conn.execute('SELECT rowid, * FROM immobilien').fetchall()
    conn.close()
    return jsonify([dict(row) for row in immos])

# Immobilie per API hinzufügen (JSON)
@app.route('/api/immobilien', methods=['POST'])
def add_immobilie():
    data = request.json
    conn = get_db()

    query = '''
        INSERT INTO immobilien (
            Name, Bundesland, Stadt, Straße, PLZ,
            Latitude, Longitude, ID, Gebäudekategorie,
            Kurzbeschreibung, Beschreibung, "Preis (€)", "Bild-URL"
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    conn.execute(query, (
        data.get('Name'),
        data.get('Bundesland'),
        data.get('Stadt'),
        data.get('Straße'),
        data.get('PLZ'),
        data.get('Latitude'),
        data.get('Longitude'),
        data.get('ID'),
        data.get('Gebäudekategorie'),
        data.get('Kurzbeschreibung'),
        data.get('Beschreibung'),
        data.get('Preis (€)'),
        data.get('Bild-URL')
    ))
    conn.commit()
    conn.close()
    return jsonify({'status': 'hinzugefügt'}), 201

# Neue Immobilie über HTML-Formular anlegen
@app.route('/neu', methods=['GET', 'POST'])
def neues_formular():
    if request.method == 'POST':
        data = request.form

        conn = get_db()
        query = '''
            INSERT INTO immobilien (
                Name, Bundesland, Stadt, Straße, PLZ,
                Latitude, Longitude, ID, Gebäudekategorie,
                Kurzbeschreibung, Beschreibung, "Preis (€)", "Bild-URL"
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        conn.execute(query, (
            data.get('Name'),
            data.get('Bundesland'),
            data.get('Stadt'),
            data.get('Straße'),
            data.get('PLZ'),
            float(data.get('Latitude')),
            float(data.get('Longitude')),
            int(data.get('ID')),
            data.get('Gebäudekategorie'),
            data.get('Kurzbeschreibung'),
            data.get('Beschreibung'),
            float(data.get('Preis (€)')),
            data.get('Bild-URL')
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('get_immobilien'))

    return render_template("formular.html")

# Optionaler Start-Endpunkt
@app.route('/')
def home():
    return 'ImmoManager API läuft – verwende /neu für das HTML-Formular.'

if __name__ == '__main__':
    app.run(debug=True)
