import sqlite3

def voeg_persoon_toe(voornaam, achternaam):
    conn = sqlite3.connect('techmensenBA.db')
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS mensen (voornaam TEXT, achternaam TEXT)")
    cursor.execute("INSERT INTO mensen (voornaam, achternaam) VALUES (?, ?)", (voornaam, achternaam))

    conn.commit()
    conn.close()

voeg_persoon_toe("Sander", "Busselot")
voeg_persoon_toe("Jonathan", "Busselot")
