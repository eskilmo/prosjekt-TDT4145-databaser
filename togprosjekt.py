import sqlite3 as sq
import re
from datetime import date, datetime
 

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


#e) En bruker skal kunne registrere seg i kunderegisteret

def registrate_customer():
    con = sq.connect('prosjekt.db')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Kunde")
    rows = cursor.fetchall()
    if rows == None:
        kundenummer = 1
    else:
        kundenummer = len(rows) + 1
    navn = str(input("Navn: "))

    if len(navn)>40 or has_numbers(navn):
        raise Exception("Ugyldig navn.")
    
    pattern = re.compile("[^@]+@[^@]+\.[^@]+")
    epost = str(input("E-post: "))
    if len(epost)>50 or not pattern.match(epost):
        raise Exception("Ugyldig e-post.")
    
    tlf = str(input("Tlf nummer: "))
    if (len(tlf)!=8 or not tlf.isnumeric()):
        raise Exception("Ugyldig nummer.")
    
    cursor.execute("SELECT * FROM Kunde WHERE mobilNR = ? OR epost = ?", (tlf, epost))
    duplicates = cursor.fetchall()
    if duplicates != []:
        raise Exception("Tlf eller epost er allerede registrert i kunderegisteret.")
    
    cursor.execute("INSERT INTO Kunde (kundeNR, mobilNR, epost, navn) VALUES ( ?, ?, ?, ?)", (kundenummer, tlf, epost, navn))
    con.commit()
    con.close()

#kilde: https://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number
#Hjelpemetode for å sjekke om det er tall i navnet
def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

#Hjelpemetode til g) for å sjekke om kunden er registrert før billettkjøp
def valid_customer(navn,epost):
    con = sq.connect('prosjekt.db')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Kunde")
    rows = cursor.fetchall()
    for row in rows:
        if row[3]==navn and row[2]==epost:
            return True
    con.close()
    return False

def buy_tickets():
    print("Login for å få kjøpt billetter:")
    navn = input("Navn: ")
    epost = input("Epost: ")
    if valid_customer(navn, epost) == False:
            raise Exception("Du har ikke registrert deg i kunderegisteret.")
    #få metode for å få inn alle e finne ledige billetter for en oppgitt strekning 
    #på en ønsket togrute og kjøpe de billettene hen ønsker
    #ledigeBilletter=
    con = sq.connect('prosjekt.db')
    cursor = con.cursor()
    cursor.execute("SELECT kundNR FROM Kunde WHERE navn = ? AND epost = ?", (navn, epost))
    kundeNR = cursor.fetchone()[0]
    cursor.execute("SELECT * FROM Kundeordre")
    rows = cursor.fetchall()
    if rows == None:
        ordreNR = 1
    else:
        ordreNR = len(rows) + 1
    
    cursor.execute('''INSERT INTO Bestilling VALUES (?, ?)''', (kundeNR, ordreNR))
    antallBilletter = input("Hvor mange billetter vil du kjøpe?")
    if antallBilletter > ledigeBilletter:
        raise Exception("Det er ikke så mange billetter som er tilgjengelig på denne delstrekningen. Det er ")
    bestillingsdato = date.today().strftime("%d/%m/%Y")
    bestillingstid = datetime.now().hour + ":" + datetime.now().minute










