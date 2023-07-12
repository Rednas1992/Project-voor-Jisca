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

    cursor.execute("SELECT voornaam, achternaam, locatie, geboortedatum FROM mensen")
    resultaten = cursor.fetchall()

    conn.close()

    return resultaten

# Functie om een persoon aan de database toe te voegen
def voeg_persoon_toe(voornaam, achternaam, locatie, geboortedatum):
    conn = sqlite3.connect('techmensenba.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO mensen (voornaam, achternaam, locatie, geboortedatum) VALUES (?, ?, ?, ?)", (voornaam, achternaam, locatie, geboortedatum))

    conn.commit()
    conn.close()

# Functie om een persoon uit de database te verwijderen
def verwijder_persoon(voornaam, achternaam, locatie, geboortedatum):
    conn = sqlite3.connect('techmensenba.db')
    cursor = conn.cursor()
    
    print(f"Te verwijderen persoon: {voornaam}, {achternaam}, {locatie}, {geboortedatum}")

    cursor.execute("DELETE FROM mensen WHERE voornaam=? AND achternaam=? AND locatie=? AND geboortedatum=?", (voornaam, achternaam, locatie, geboortedatum))

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
    locatie = request.form['locatie']
    geboortedatum = request.form['geboortedatum']
    
    print(f"Ontvangen gegevens voor verwijderen: {voornaam}, {achternaam}, {locatie}, {geboortedatum}")

    voeg_persoon_toe(voornaam, achternaam, locatie, geboortedatum)

    return redirect('/techmensen')

@app.route('/verwijderen', methods=['POST'])
def verwijderen():
    voornaam = request.form['voornaam']
    achternaam = request.form['achternaam']
    locatie = request.form['locatie']
    geboortedatum = request.form ['geboortedatum']

    verwijder_persoon(voornaam, achternaam, locatie, geboortedatum)

    return redirect('/techmensen')
#####
#####
##### nieuwe code einde ###
@app.route('/filteren', methods=['POST'])
def filteren():
    locatie_filter = request.form.get('locatieFilter')

    mensen = haal_mensen_op()  # Haal de lijst met mensen op

    gefilterde_mensen = []

    for persoon in mensen:
        if locatie_filter == '' or persoon[2] == locatie_filter:
            gefilterde_mensen.append(persoon)

    return render_template('techmensen.html', mensen=gefilterde_mensen)



if __name__ == "__main__":
    app.run()