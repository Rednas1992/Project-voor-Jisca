from flask import Flask, redirect, url_for, render_template, request
import sqlite3


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
#####
#####
##### Nieuwe code start ###
# Functie om alle mensen uit de database op te halen
def haal_mensen_op():
    conn = sqlite3.connect('techmensenba.db')
    cursor = conn.cursor()

    cursor.execute("SELECT voornaam, achternaam FROM mensen")
    resultaten = cursor.fetchall()

    conn.close()

    return resultaten

# Functie om een persoon aan de database toe te voegen
def voeg_persoon_toe(voornaam, achternaam):
    conn = sqlite3.connect('techmensenba.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO mensen (voornaam, achternaam) VALUES (?, ?)", (voornaam, achternaam))

    conn.commit()
    conn.close()

# Functie om een persoon uit de database te verwijderen
def verwijder_persoon(voornaam, achternaam):
    conn = sqlite3.connect('techmensenba.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM mensen WHERE voornaam=? AND achternaam=?", (voornaam, achternaam))

    conn.commit()
    conn.close()

@app.route('/techmensen')
def techmensen(): ### hier maak ik wijzeging in het nieuwe script ###
    mensen = haal_mensen_op()
    return render_template('techmensen.html', mensen=mensen)

@app.route('/toevoegen', methods=['POST'])
def toevoegen():
    voornaam = request.form['voornaam']
    achternaam = request.form['achternaam']

    voeg_persoon_toe(voornaam, achternaam)

    return redirect('/')

@app.route('/verwijderen', methods=['POST'])
def verwijderen():
    voornaam = request.form['voornaam']
    achternaam = request.form['achternaam']

    verwijder_persoon(voornaam, achternaam)

    return redirect('/')
#####
#####
##### nieuwe code einde ###

if __name__ == "__main__":
    app.run()