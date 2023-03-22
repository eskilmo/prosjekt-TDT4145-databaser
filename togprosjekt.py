import sqlite3 as sq

#Funksjon som tar inn en jernbanestasjon og en ukedag og viser alle tog som 
#går innom denne stasjonen på denne dagen. 
def hentTogruterUkedagStasjon(stasjon, ukedag):
    con = sq.connect('prosjekt.db')
    cursor = con.cursor()
    cursor.execute('''SELECT * FROM
        (SELECT ruteID, startstasjon, endestasjon, hovedretning, operatør FROM
        (SELECT togruteID
        FROM Togrutetabell
        WHERE jernbanestasjonsnavn=?)
        INNER JOIN Togrute ON togruteID=ruteID)
        NATURAL JOIN Avgangsdager
        WHERE dag=?''', (stasjon, ukedag))
    rows = cursor.fetchall()
    print(f"Togruter som går innom {stasjon} på {ukedag}:")
    for row in rows:
        print(row)
    con.close()

#hentTogruterUkedagStasjon("Bodø", "mandag")

#Funksjon som tar inn ønsket start- og sluttstasjon med dato og tid for en reise,
#og viser alle togreiser som går mellom stasjonene etter dette tidspunktet. 
def hentTogreise(startstasjon, sluttstasjon, dato, tid):
    con = sq.connect('prosjekt.db')
    cursor = con.cursor()
    cursor.execute('''SELECT togruteID FROM Togrutetabell
        WHERE jernbanestasjonsnavn=? or jernbanestasjonsnavn=?
        GROUP BY togruteID
        HAVING count(jernbanestasjonsnavn)=2''', (startstasjon, sluttstasjon))
    rows = cursor.fetchall()
    print(f"Togruter som går fra {startstasjon} til {sluttstasjon}:")

    #Finner og lagrer alle togreiser som kjører mellom start og slutt. 
    gyldigeTogruteIDer=[]
    for row in rows:
        togruteID = row[0]
        
        cursor.execute('''SELECT * FROM Togrutetabell
        WHERE togruteID=? and jernbanestasjonsnavn=?''', (togruteID, startstasjon))
        rows2 = cursor.fetchall()
        print(rows2[0])
        if rows2[0][2]==None:
            starttidspunkt=rows2[0][3]
        else: 
            starttidspunkt=rows2[0][2]

        cursor.execute('''SELECT * FROM Togrutetabell
        WHERE togruteID=? and jernbanestasjonsnavn=?''', (togruteID, sluttstasjon))
        rows2 = cursor.fetchall()
        if rows2[0][2]==None:
            slutttidspunkt=rows2[0][3]
        else:
            slutttidspunkt=rows2[0][2]

        if not tid1_før_tid2(starttidspunkt, slutttidspunkt):
            continue
            # raise Exception("feil")
        else:
            gyldigeTogruteIDer.append(togruteID)
            print("TOGRUTE SOM KJØRER:", togruteID)
        
    #for ruteID in gyldigeTogruteIDer:

    

    con.close()

#Hjelpefunksjon, sjekker om klokkeslett hh:mm er før klokkeslett hh:mm
def tid1_før_tid2(tid1, tid2):
    if tid1 == tid2:
        return True
    tid_liste1 = tid1.split(':')
    timer1 = int(tid_liste1[0])
    minutter1 = int(tid_liste1[1])
    tid_liste2 = tid2.split(':')
    timer2 = int(tid_liste2[0])
    minutter2 = int(tid_liste2[1])
    if timer1 > timer2:
        return False
    elif timer1==timer2 and minutter1 > minutter2:
        return False
    return True

hentTogreise("Trondheim", "Fauske", "03.04.2023", "00:00")