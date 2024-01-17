import sqlite3
from datetime import datetime


conn = sqlite3.connect('csalad_adatbazis.db')
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS csalad (
        id INTEGER PRIMARY KEY,
        nev TEXT NOT NULL,
        szuletesi_datum TEXT NOT NULL,
        szuletesi_hely TEXT NOT NULL,
        anya_neve TEXT NOT NULL,
        apa_neve TEXT NOT NULL,
        elhalalozas_datum TEXT,
        elhalalozas_hely TEXT
    )
''')
conn.commit()

def adatbevitel():
    nev = input("Név: ")
    szuletesi_datum = input("Születési dátum (YYYY-MM-DD): ")
    szuletesi_hely = input("Születési hely: ")
    anya_neve = input("Anyja neve: ")
    apa_neve = input("Apja neve: ")
    elhalalozas_datum = input("Elhalálozás dátuma (ha nincs, üresen hagyható): ")
    elhalalozas_hely = input("Elhalálozás helye: ")

    cursor.execute('''
        INSERT INTO csalad (nev, szuletesi_datum, szuletesi_hely, anya_neve, apa_neve, elhalalozas_datum, elhalalozas_hely)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (nev, szuletesi_datum, szuletesi_hely, anya_neve, apa_neve, elhalalozas_datum, elhalalozas_hely))
    
    conn.commit()
    print("Adatok rögzítve.")

def adat_modositas():
    nev = input("Adja meg a módosítani kívánt személy nevét: ")

    mezok = ['nev', 'szuletesi_datum', 'szuletesi_hely', 'anya_neve', 'apa_neve', 'elhalalozas_datum', 'elhalalozas_hely']

    for i, mezo in enumerate(mezok, start=1):
        print(f"{i}. {mezo}")

    valasztott_mezo_index = int(input("Válassza ki a módosítani kívánt mező sorszámát: "))
    valasztott_mezo = mezok[valasztott_mezo_index - 1]

    uj_ertek = input(f"Adja meg az új értéket a(z) {valasztott_mezo} mezőhöz: ")

    cursor.execute(f'''
        UPDATE csalad
        SET {valasztott_mezo} = ?
        WHERE nev = ?
    ''', (uj_ertek, nev))

    conn.commit()
    print("Adatok módosítva.")

def adatvizualizacio():
    opcio = input("Válasszon opciót:\n1. Egy konkrét személy adatai\n2. Ki kinek a gyereke\n3. Kinek ki a gyermeke\n")
    
    if opcio == '1':
        nev = input("Adja meg a személy nevét: ")
        cursor.execute('SELECT * FROM csalad WHERE nev = ?', (nev,))
        adatok = cursor.fetchone()
        if adatok:
            print("A személy adatai:")
            print(f"ID: {adatok[0]}")
            print(f"Név: {adatok[1]}")
            print(f"Születési dátum: {adatok[2]}")
            print(f"Születési hely: {adatok[3]}")
            print(f"Anyja neve: {adatok[4]}")
            print(f"Apa neve: {adatok[5]}")
            print(f"Elhalálozás dátuma: {adatok[6]}" if adatok[6] else "Nincs elhalálozás")
            print(f"Elhalálozás helye: {adatok[7]}" if adatok[7] else "Nincs elhalálozás helye")
        else:
            print("Nincs adat a megadott névvel az adatbázisban.")

    elif opcio == '2':
        nev = input("Adja meg a gyerek nevét: ")
        cursor.execute('SELECT anya_neve, apa_neve FROM csalad WHERE nev = ? OR anya_neve = ? OR apa_neve = ?', (nev, nev, nev))
        szulok = cursor.fetchall()
        
        if szulok:
            print(f"{nev} szülői:")
            for anya, apa in szulok:
                print(f"- Anya: {anya}")
                print(f"- Apa: {apa}")

            cursor.execute('SELECT nev FROM csalad WHERE anya_neve = ? OR apa_neve = ?', (nev, nev))
            gyerekek = cursor.fetchall()

            if gyerekek:
                print(f"\n{nev} gyerekei:")
                for gyerek in gyerekek:
                    print(f"- {gyerek[0]}")
            else:
                print(f"{nev}nak nincsenek gyerekei az adatbázisban.")
        else:
            print("Nincs ilyen személy az adatbázisban.")

    elif opcio == '3':
        nev = input("Adja meg a szülő nevét: ")
        cursor.execute('SELECT nev FROM csalad WHERE anya_neve = ? OR apa_neve = ?', (nev, nev))
        gyerekek = cursor.fetchall()
        if gyerekek:
            print(f"{nev} gyermekei:")
            for gyerek in gyerekek:
                print(f"- {gyerek[0]}")
        else:
            print(f"{nev}nak nincsenek gyermekei az adatbázisban.")

    else:
        print("Érvénytelen opció.")


while True:
    print("\nVálasszon opciót:")
    print("1. Adatbevitel")
    print("2. Tárolt, de hibás adatok módosítása")
    print("3. Adatvizualizáció")
    print("4. Kilépés")

    valasztas = input("Adja meg a választott opció sorszámát: ")

    if valasztas == '1':
        adatbevitel()
    elif valasztas == '2':
        adat_modositas()
    elif valasztas == '3':
        adatvizualizacio()
    elif valasztas == '4':
        print("Kilépés...")
        break
    else:
        print("Érvénytelen opció. Kérem, válasszon újra.")


conn.close()
