from flask import Flask, redirect, url_for, render_template, request
import sqlite3
from datetime import datetime, date
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    # Voeg hier je eigen inloglogica toe
    # Controleer of de gebruikersnaam en het wachtwoord geldig zijn

    if username == "admin" and password == "admin":
        return redirect(url_for("techmensen"))
    
    elif username == "oudenaarde" and password == "oudenaarde":
        return redirect(url_for("oudenaarde"))
    
    else:
        return redirect(url_for("nietgelukt"))

@app.route("/gelukt")
def gelukt():
    return render_template("gelukt.html")

@app.route("/nietgelukt")
def nietgelukt():
    return render_template("nietgelukt.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

def haal_mensen_op():
    conn = sqlite3.connect('techmensenba.db')
    cursor = conn.cursor()

    cursor.execute("SELECT voornaam, achternaam, locatie, geboortedatum FROM mensen")
    resultaten = cursor.fetchall()

    conn.close()

    return resultaten

def voeg_persoon_toe(voornaam, achternaam, locatie, geboortedatum):
    conn = sqlite3.connect('techmensenba.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO mensen (voornaam, achternaam, locatie, geboortedatum) VALUES (?, ?, ?, ?)",
                   (voornaam, achternaam, locatie, geboortedatum))

    conn.commit()
    conn.close()

def verwijder_persoon(voornaam, achternaam, locatie, geboortedatum):
    conn = sqlite3.connect('techmensenba.db')
    cursor = conn.cursor()

    print(f"Te verwijderen persoon: {voornaam}, {achternaam}, {locatie}, {geboortedatum}")

    cursor.execute("DELETE FROM mensen WHERE voornaam=? AND achternaam=? AND locatie=? AND geboortedatum=?",
                   (voornaam, achternaam, locatie, geboortedatum))

    conn.commit()
    conn.close()

@app.route('/oudenaarde')
def oudenaarde():
    mensen = haal_mensen_op()
    return render_template('oudenaarde.html', mensen=mensen)

@app.route('/techmensen')
def techmensen():
    mensen = haal_mensen_op()
    return render_template('techmensen.html', mensen=mensen)

@app.route('/toevoegen', methods=['POST'])
def toevoegen():
    voornaam = request.form['voornaam']
    achternaam = request.form['achternaam']
    locatie = request.form['locatie']
    geboortedatum = request.form['geboortedatum']

    print(f"Ontvangen gegevens voor toevoegen: {voornaam}, {achternaam}, {locatie}, {geboortedatum}")

    voeg_persoon_toe(voornaam, achternaam, locatie, geboortedatum)

    return redirect('/techmensen')

@app.route('/toevoegen_oudenaarde', methods=['POST'])
def toevoegen_oudenaarde():
    voornaam = request.form['voornaam']
    achternaam = request.form['achternaam']
    locatie = request.form['locatie']
    geboortedatum = request.form['geboortedatum']

    print(f"Ontvangen gegevens voor toevoegen: {voornaam}, {achternaam}, {locatie}, {geboortedatum}")

    voeg_persoon_toe(voornaam, achternaam, locatie, geboortedatum)

    return redirect('/oudenaarde')

@app.route('/verwijderen', methods=['POST'])
def verwijderen():
    voornaam = request.form['voornaam']
    achternaam = request.form['achternaam']
    locatie = request.form['locatie']
    geboortedatum = request.form['geboortedatum']

    verwijder_persoon(voornaam, achternaam, locatie, geboortedatum)

    return redirect('/techmensen')

@app.route('/filteren', methods=['POST'])
def filteren():
    locatie_filter = request.form.get('locatieFilter')

    mensen = haal_mensen_op()

    gefilterde_mensen = []

    for persoon in mensen:
        if locatie_filter == '' or persoon[2] == locatie_filter:
            gefilterde_mensen.append(persoon)

    return render_template('techmensen.html', mensen=gefilterde_mensen)

@app.route('/filteren_oudenaarde', methods=['POST'])
def filteren_oudenaarde():
    locatie_filter = request.form.get('locatieFilter')

    mensen = haal_mensen_op()

    gefilterde_mensen = []

    for persoon in mensen:
        if locatie_filter == '' or persoon[2] == locatie_filter:
            gefilterde_mensen.append(persoon)

    return render_template('oudenaarde.html', mensen=gefilterde_mensen)

@app.route('/vertrek_doorgestuurd_oudenaarde', methods=['POST'])
def vertrek_doorgestuurd_oudenaarde():
    locatie_filter = "Oudenaarde"
    huidige_datum = date.today().strftime("%Y-%m-%d")
    oudenaarde_datum_tabel = "oudenaarde_" + huidige_datum.replace("-", "_")
    
    # Filter de gegevens op locatie "Oudenaarde"
    mensen = haal_mensen_op()
    gefilterde_mensen = [persoon + ("", "") for persoon in mensen if persoon[2] == locatie_filter]
    
    # Maak verbinding met de database
    conn = sqlite3.connect('techmensenba.db')
    cursor = conn.cursor()

    # Controleer of de tabel al bestaat
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (oudenaarde_datum_tabel,))
    tabel_bestaat = cursor.fetchone()

    if tabel_bestaat:
        # Update de bestaande tabel
        for i, persoon in enumerate(gefilterde_mensen):
            voornaam, achternaam, locatie, geboortedatum, status, opmerkingen = persoon
            status_key = request.form.get(f"status_{i}")  # Unieke identificatie voor status
            opmerkingen_key = request.form.get(f"opmerkingen_{i}")  # Unieke identificatie voor opmerkingen
            cursor.execute("UPDATE {} SET status=?, opmerkingen=? WHERE voornaam=? AND achternaam=? AND locatie=? AND geboortedatum=?".format(oudenaarde_datum_tabel),
                           (status_key, opmerkingen_key, voornaam, achternaam, locatie, geboortedatum))
    else:
        # Maak een nieuwe tabel aan
        cursor.execute("CREATE TABLE {} (voornaam TEXT, achternaam TEXT, locatie TEXT, geboortedatum TEXT, status TEXT, opmerkingen TEXT)".format(oudenaarde_datum_tabel))
        # Voeg de gefilterde gegevens toe aan de nieuwe tabel
        cursor.executemany("INSERT INTO {} VALUES (?, ?, ?, ?, ?, ?)".format(oudenaarde_datum_tabel), gefilterde_mensen)

    # Sla de wijzigingen op en sluit de databaseverbinding
    conn.commit()
    conn.close()

    return redirect('/oudenaarde')

if __name__ == "__main__":
    app.run()
