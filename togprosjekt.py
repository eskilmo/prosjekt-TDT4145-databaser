import sqlite3 as sq
import re
from datetime import date, datetime

#c) Funksjon som tar inn en jernbanestasjon og en ukedag og viser alle tog som 
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

#d) Funksjon som tar inn en jernbanestasjon og en ukedag og viser alle tog som 
#går innom denne stasjonen på denne dagen. 
def hentTogreise(startstasjon, sluttstasjon, dato, tid):
    con = sq.connect('prosjekt.db')
    cursor = con.cursor()
    cursor.execute('''SELECT togruteID FROM Togrutetabell
        WHERE jernbanestasjonsnavn=? or jernbanestasjonsnavn=?
        GROUP BY togruteID
        HAVING count(jernbanestasjonsnavn)=2''', (startstasjon, sluttstasjon))
    rows = cursor.fetchall()
    print(f"Togruter som går fra {startstasjon} til {sluttstasjon} etter {dato} kl {tid}:")

    #Finner og lagrer alle togreiser som kjører mellom start og slutt (må sjekke om de går riktig vei). 
    gyldigeTogruteIDer=[]
    for row in rows:
        togruteID = row[0]
        
        #Spørring for å finne startstasjon sitt StasjonNr
        cursor.execute('''SELECT * FROM Togrutetabell
        WHERE togruteID=? and jernbanestasjonsnavn=?''', (togruteID, startstasjon))
        rows2 = cursor.fetchall()
        forsteStasjonNr=rows2[0][4]

        #Spørring for å finne sluttstasjon sitt StasjonNr
        cursor.execute('''SELECT * FROM Togrutetabell
        WHERE togruteID=? and jernbanestasjonsnavn=?''', (togruteID, sluttstasjon))
        rows3 = cursor.fetchall()
        sisteStasjonNr=rows3[-1][4]

        if forsteStasjonNr>=sisteStasjonNr:
            continue
        else:
            gyldigeTogruteIDer.append(togruteID)

    if len(gyldigeTogruteIDer)==0:
        print(f"Ingen togruter fra {startstasjon} til {sluttstasjon}")
        return None

    tekst=""
    first=True
    for ruteID in gyldigeTogruteIDer:
        if first:
            tekst+=f"ruteID={ruteID}"
            first=False
        else:
            tekst+=f" OR ruteID={ruteID}"
                                
    #Togreiser som går fra startstasjon til sluttstasjon (blir egentlig ikke sortert skikkelig etter dato):
    cursor.execute(f'''SELECT ruteID, togreiseID, dato, jernbanestasjonsnavn AS startstasjon, avgangstid FROM Togrute
                        INNER JOIN Togreise ON ruteID=Togreise.togruteID
                        INNER JOIN Togrutetabell ON ruteID=Togrutetabell.togruteID
                        WHERE ({tekst}) AND jernbanestasjonsnavn=?
                        ''', (startstasjon,))
    rows4 = cursor.fetchall()

    #Printer kun ut de reisene som går etter gitt dato og klokkeslett (men kan få "feil" med nattog).
    togreiserFraStasjonEtterDato=[]
    for row in rows4:
        datoPaaTogreise=row[2]
        tidPaaTogreise=row[4]
        if dato1_før_dato2(dato, datoPaaTogreise):
            togreiserFraStasjonEtterDato.append(row)
        elif (dato==datoPaaTogreise) and tid1_før_tid2(tid, tidPaaTogreise):
            togreiserFraStasjonEtterDato.append(row)

    if len(togreiserFraStasjonEtterDato)==0:
        print(f"Ingen togruter fra {startstasjon} til {sluttstasjon} etter {dato} {tid}")
        return None

    #Sorter listen basert på hvilken dato og klokkeslett de gyldige avgangene går. 
    mellomListe=[]
    for togreise in togreiserFraStasjonEtterDato:
        datoTogreise=togreise[2]
        tidTogreise=togreise[4]
        #Omgjør dato og tid til datetime. 
        mellomListe.append((togreise[0], togreise[1], togreise[2], togreise[4], datetime.strptime(datoTogreise + " " + tidTogreise, '%d.%m.%Y %H:%M')))

    #Sorter basert på datetime verdien. 
    sortertTogreiserFraStasjonEtterDato = sorted(mellomListe, key=lambda x: x[4])

    for togreise in sortertTogreiserFraStasjonEtterDato:
        print("TogruteID:", togreise[0], "TogreiseID:", togreise[1], "Dato:", togreise[2], "Kl:", togreise[3])

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

#Hjelpefunksjon, sjekker om dato1 er før dato2
def dato1_før_dato2(dato1, dato2):
    if dato1==dato2:
        return False
    tid_liste1 = dato1.split('.')
    d1 = int(tid_liste1[0])
    m1 = int(tid_liste1[1])
    y1 = int(tid_liste1[2])
    tid_liste2 = dato2.split('.')
    d2 = int(tid_liste2[0])
    m2 = int(tid_liste2[1])
    y2 = int(tid_liste2[2])
    if y1 > y2:
        return False
    elif y1==y2 and m1 > m2:
        return False
    elif y1==y2 and m1==m2 and d1>d2:
        return False
    return True

hentTogreise("Trondheim", "Fauske", "03.04.2023", "00:00")


#e) En bruker skal kunne registrere seg i kunderegisteret

def registrateCustomer():
    con = sq.connect('prosjekt.db')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Kunde")
    rows = cursor.fetchall()
    if rows == None:
        kundenummer = 1
    else:
        kundenummer = len(rows) + 1
    
    print("Kan ikke inneholde tall.")
    navn = str(input("Navn: "))

    if len(navn)>40 or hasNumbers(navn):
        raise Exception("Ugyldig navn.")
    
    pattern = re.compile("[^@]+@[^@]+\.[^@]+")
    print("(Krav til epost er at det må være en @ og nøyaktig ett punktum etter @.)")
    epost = str(input("E-post: "))
    if len(epost)>50 or not pattern.match(epost):
        raise Exception("Ugyldig e-post.")
    
    print("(Nummeret må være 8 siffer langt.)")
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
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

#Hjelpemetode til g) for å sjekke om kunden er registrert før billettkjøp
def validCustomer(navn,epost):
    con = sq.connect('prosjekt.db')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Kunde")
    rows = cursor.fetchall()
    for row in rows:
        if row[3]==navn and row[2]==epost:
            return True
    con.close()
    return False
#g) 
def buyTickets():
    print("Login for å få kjøpt billetter:")
    print("(Du må være en registrert kunde i kunderegisteret.)")
    navn = input("Navn: ")
    epost = input("Epost: ")
    if validCustomer(navn, epost) == False:
            raise Exception("Navn og epost matcher ikke med en kunde i kunderegisteret.")
    
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
    antallBilletter = input("Hvor mange billetter vil du kjøpe? Du kan ikke kjøpe mer enn det som er ledig.")
    if antallBilletter > ledigeBilletter:
        raise Exception(f"Det er ikke så mange billetter som er tilgjengelig på denne delstrekningen. Det er {ledigeBilletter} ledige billetter igjen. ")
    bestillingsDato = date.today().strftime("%d/%m/%Y")
    feilbestillingstid = str(datetime.now().hour) + ":" + str(datetime.now().minute)
    splittet = bestillingsDato.split("/")
    bestillingsTid = ""
    for element in splittet:
        if len(element) > 2:
            bestillingsTid += element
        else:
            bestillingsTid += element + "."
    
    cursor.execute('''INSERT INTO Kundeordre VALUES (?, ?, ?, ?)''', (antallBilletter, ordreNR, bestillingsDato, bestillingsTid))
    cursor.execute("SELECT * FROM BillettKjøp")
    rows = cursor.fetchall()
    if rows == None:
        billettID = 1
    else:
        billettID = len(rows) + 1
    cursor.execute('''INSERT INTO BillettKjøp VALUES (?, ?)''', (billettID, ordreNR))
    #husk å legge til rett variabelnavn
    cursor.execute('''INSERT INTO Billett VALUES (?, ?, ?, ?)''', (billettID, startstasjon, endestasjon, avgangsdato))
    #når billettkjøpet har blitt registrert må de aktuelle setene/sengene bli gjort om til 
    # å ikke være ledig lengre 
    
    if plass.lower() == "seng":
        cursor.execute('''INSERT INTO ReservertSengeplass VALUES (?, ?, ?)''', (billettID, sengNR, vognID))
        cursor.execute('''UPDATE SengLedigPåTogReise SET ledig = False 
                        WHERE sengNR=? and vognID=? and togreiseID=1 and delstrekningsID=1''', (sengNR, vognID, togreiseID, delstrekningsID))
    
    else:
        cursor.execute('''INSERT INTO ReservertSeteplass VALUES (?, ?, ?)''', (billettID, seteNR, vognID))
        cursor.execute('''UPDATE SeteLedigPåDelstrekning SET ledig = False
                        WHERE seteNR=? and vognID=? and togreiseID=1 and delstrekningsID=1''', (seteNR, vognID, togreiseID, delstrekningsID))

    con.commit()
    con.close()


#h)

def getPurchasehistory(kundeNR):
    con = sq.connect('prosjekt.db')
    cursor = con.cursor()
    cursor.execute('''SELECT b.billettID, o.ordreNR, o.bestillingsDato, o.bestillingsTid, b.startstasjon, b.endestasjon, b.avgangsdato, rp.seteNR, 
    rp.vognID, sp.sengNR, sp.vognID FROM Bestilling c JOIN Kundeordre o ON c.ordreNR = o.ordreNR JOIN BillettKjøp t ON o.ordreNR = t.ordreNR 
    JOIN Billett b on t.billettID = b.billettID LEFT JOIN ReservertSetePlass rp on rp.billettID = b.billettID 
    LEFT JOIN ReservertSengeplass sp on sp.billettID = b.billettID WHERE c.kundeNR = 2''', (kundeNR))
    
    rows = cursor.fetchall()
    if rows== None:
        raise Exception("Du har ingen kjøp enda.")
    print(f"Kjøpshistorikken til kundenummer {kundeNR} er:")
    print("billettID\tordreNR\tbestillingsDato\tbestillingsTid\tstartstasjon\tendestasjon\tavgangsdato\tseteNR\tvognID\tsengNR\tvognID")
    for row in rows:
        print(row)
    con.close()
#mangler å få inn vognnr, setenr etc



#metode som skal kjøres når fila kjøres for at brukeren får valget om hvilken handling den vil gjøre
def launch():
    print('''\n\nA Hent togruter som er innom en stasjon på en ukedag.\nB Finn togruter fra start- til sluttstasjon\nC Registrer som ny kunde\nD Finn og kjøp billetter\nE Dine reiser\n\n''')
    valg = str(input("(Svar en av bokstavene over.)\nHvilken handling vil du gjøre?"))

    if valg == "A" or valg == "a":
        stasjon = input("Stasjon: ")
        dag = input("Dag: ").lower()
        hentTogruterUkedagStasjon(stasjon,dag)
    
    elif valg == "B" or valg == "b":
        startstasjon = input("Startstasjon: ")
        sluttstasjon = input("Sluttstasjon: ")
        dato = input("Dato: ")
        tid = input("Tid: ")
        hentTogreise(startstasjon,sluttstasjon,dato,tid)
    
    elif valg == "C" or valg == "c":
        registrateCustomer()
    
    
    elif valg == "D" or valg == "d":
        buyTickets()
    
    
    elif valg == "E" or valg == "E":
        kundeNR= input("KundeNR: ")
        getPurchasehistory(kundeNR)
    
    else:
        raise Exception("Du må velge en av de oppgitte bokstavene.")

launch()
    




    










