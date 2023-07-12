import sqlite3

def haal_mensen_op():
    conn = sqlite3.connect('techmensenBA.db')
    cursor = conn.cursor()

    cursor.execute("SELECT voornaam, achternaam FROM mensen")
    resultaten = cursor.fetchall()

    conn.close()

    return resultaten

mensen = haal_mensen_op()

for persoon in mensen:
    voornaam, achternaam = persoon
    print(f"Voornaam: {voornaam}, Achternaam: {achternaam}")
