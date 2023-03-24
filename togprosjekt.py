import sqlite3 as sq
import re
from datetime import date, datetime

#c) Funksjon som tar inn en jernbanestasjon og en ukedag og viser alle tog som 
#går innom denne stasjonen på denne dagen. 
def hentTogruterUkedagStasjon(stasjon, ukedag):
    con = sq.connect('prosjekt.db')
    cursor = con.cursor()
    cursor.execute('''SELECT * FROM
        (SELECT ruteID, startstasjon, endestasjon, hovedretning, operatør, ankomsttid, avgangstid FROM
        (SELECT togruteID, ankomsttid, avgangstid
        FROM Togrutetabell
        WHERE jernbanestasjonsnavn=?)
        INNER JOIN Togrute ON togruteID=ruteID)
        NATURAL JOIN Avgangsdager
        WHERE dag=?''', (stasjon, ukedag))
    rows = cursor.fetchall()

    if len(rows)==0:
        print(f"Det er ingen togruter som går gjennom {stasjon} på {ukedag}.")
    else: 
        print(f"Togruter som går innom {stasjon} på {ukedag}:")
        for row in rows:
            #Hvis ankomsttid er NULL, bruk avgangstid:
            if row[5]==None: 
                print(f'RuteID: {row[0]} fra {row[1]} til {row[2]} kl {row[6]}')
            #Hvis avgangstid er NULL, bruk ankomsttid:
            else:
                print(f'RuteID: {row[0]} fra {row[1]} til {row[2]} kl {row[5]}')
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
    print(f"Kundenummeret ditt er: {kundenummer}")
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
def buyTickets(dato, startstasjon, sluttstasjon, plass, navn, epost):
    
    #få metode for å få inn alle e finne ledige billetter for en oppgitt strekning 
    #på en ønsket togrute og kjøpe de billettene hen ønsker

    con = sq.connect('prosjekt.db')
    cursor = con.cursor()
    cursor.execute("SELECT kundeNR FROM Kunde WHERE navn = ? AND epost = ?", (navn, epost))
    kundeNR = cursor.fetchone()[0]
    cursor.execute("SELECT * FROM Bestilling")
    rows = cursor.fetchall()
    if rows == None:
        ordreNR = 1
    else:
        ordreNR = len(rows) + 1

    antallBilletter=0

    first=True
    while True:
        togreiseID, vognID, plassNR = kjop(dato, startstasjon, sluttstasjon, plass, ordreNR)
        
        #Hvis bruker har valgt gyldig ledig plass for første gang, så lager en bestilling/kundeordre.
        if (togreiseID!=None and vognID!=None and plassNR!=None and first==True):
            cursor.execute('''INSERT INTO Bestilling VALUES (?, ?)''', (kundeNR, ordreNR))
            first=False

        if (togreiseID!=None and vognID!=None and plassNR!=None):            
            #Finn bestillingsdato
            feilbestillingsdato = date.today().strftime("%d/%m/%Y")
            bestillingstid = str(datetime.now().hour) + ":" + str(datetime.now().minute)
            splittet = feilbestillingsdato.split("/")
            bestillingsdato = ""
            for element in splittet:
                if len(element) > 2:
                    bestillingsdato += element
                else:
                    bestillingsdato += element + "."

            #Finn billettID
            cursor.execute("SELECT * FROM BillettKjøp")
            rows = cursor.fetchall()
            if rows == None:
                billettID = 1
            else:
                billettID = len(rows) + 1

            #Opprett billett og billettkjøp
            cursor.execute('''INSERT INTO Billett VALUES (?, ?, ?, ?)''', (billettID, startstasjon, sluttstasjon, dato))
            cursor.execute('''INSERT INTO BillettKjøp VALUES (?, ?)''', (billettID, ordreNR))

            #Når billettkjøpet har blitt registrert må de aktuelle setene/sengene bli gjort om til 
            #å ikke være ledig lengre 
            if plass.lower() == "seng":
                cursor.execute('''INSERT INTO ReservertSengeplass VALUES (?, ?, ?)''', (billettID, plassNR, vognID))
                cursor.execute('''UPDATE SengLedigPåTogReise SET ledig = False 
                                WHERE sengNR=? and vognID=? and togreiseID=?''', (plassNR, vognID, togreiseID))
            
            elif plass.lower() == "sete":
                delstrekningsIDer = finneDelstrekninger(startstasjon, sluttstasjon)
                cursor.execute('''INSERT INTO ReservertSeteplass VALUES (?, ?, ?)''', (billettID, plassNR, vognID))
                for delstrekningsID in delstrekningsIDer:
                    cursor.execute('''UPDATE SeteLedigPåDelstrekning SET ledig = False
                                    WHERE seteNR=? and vognID=? and togreiseID=? and delstrekningsID=?''', (plassNR, vognID, togreiseID, delstrekningsID))
            con.commit()
            antallBilletter+=1

        else:
            print("FEIL")

        nybillett=input("Kjøpe ny billett i ordre? (y/n)")
        if (nybillett=="n"):
            if antallBilletter>0:
                print(f"Du kjøpte {antallBilletter} billetter med ordrenummer {ordreNR}")
                cursor.execute('''INSERT INTO Kundeordre VALUES (?, ?, ?, ?)''', (antallBilletter, ordreNR, bestillingsdato, bestillingstid))
                con.commit()
            else: 
                print("Ingen billetter kjøpt, avbryter ordre.")
            break
    con.close()

def kjop(dato, startstasjon, sluttstasjon, plass, ordreNummer):
    con = sq.connect("prosjekt.db")
    cursor = con.cursor()

    #Finner ledige senger
    if plass.lower() == "seng":

        ledigeSenger=[]
        brukerretning=retning(startstasjon, sluttstasjon)
        #Henter ut togreiser som går riktig retning på riktig dato fra riktig startstasjon
        cursor.execute('''SELECT SLPT.togreiseID, SLPT.vognID, SLPT.sengNR, SLPT.ledig, T.togruteID, T.dato, Tt.jernbanestasjonsnavn, Tt.avgangstid, Togrute.hovedretning
                FROM SengLedigPåTogreise as SLPT INNER JOIN Togreise as T
                on SLPT.togreiseID = T.togreiseID
                INNER JOIN Togrutetabell as Tt
                on Tt.togruteID = T.togruteID
                INNER JOIN Togrute
                on T.togruteID = Togrute.ruteID
                WHERE ((T.dato = ?) AND jernbanestasjonsnavn = ?) AND Togrute.hovedretning = ?;''', (dato, startstasjon, brukerretning))
        sengePlasser = cursor.fetchall()

        #Sjekker at begge senger er ledige i sovekupeen for at de skal vises som ledige. 
        for i in range(0,(len(sengePlasser))-1,2):
            cursor.execute('''SELECT RS.sengNR, RS.vognID, B.ordreNR, T.togreiseID, T.dato, RS.billettID
                            FROM ReservertSengeplass as RS 
                            NATURAL JOIN BillettKjøp as B
                            INNER JOIN Vognoppsett as V on RS.vognID = V.vognID
                            INNER JOIN Togreise as T on V.ruteID = T.togruteID
                            WHERE T.dato=? and RS.sengNr=? and RS.vognID=? and T.togreiseID=?''', (sengePlasser[i][5], sengePlasser[i][2], sengePlasser[i][1], sengePlasser[i][0]))
            ordreSeng=cursor.fetchall()
            # print(ordreSeng, ordreNummer)
            print(sengePlasser[i])
            print(sengePlasser[i+1])

            #Sjekker om sengen har et ordrenummer knyttet til seg, og om det er samme som i nåværende ordre.
            #Hvis det er nåværende ordre kan begge senger i kupeen bestilles. 
            if (len(ordreSeng)!=0):
                if (ordreNummer==ordreSeng[0][2]):
                    print("LIIIIIK")
                    if (sengePlasser[i][2]%2==1):
                        if sengePlasser[i+1][3]==1:
                            ledigeSenger.append(sengePlasser[i+1])
                    elif (sengePlasser[i][2]%2==0):
                        if sengePlasser[i-1][3]==1:
                            ledigeSenger.append(sengePlasser[i-1])
            
            #Hvis ordrenummer ikke er knyttet til plassen, så må vi sjekke om begge 
            #senger i kupeen er ledig for at de kan bestilles. 
            else:
                if sengePlasser[i][3]==1 and sengePlasser[i+1][3]:
                    ledigeSenger.append(sengePlasser[i])
                    ledigeSenger.append(sengePlasser[i+1])
            
        
        if len(ledigeSenger)==0:
            print(f"Ingen ledige senger fra {startstasjon} {dato}")
            return None, None, None
        else:
            print("Ledige sengeplasser:")
            for seng in ledigeSenger:
                print(f"Sengnummer {seng[2]} i kupenummer {(seng[2]+1)//2} i vogn nummer {seng[1]} på togreise {seng[0]} fra {seng[6]} {dato} {seng[7]}")


        #Lar kunden velge seng og lagrer variable
        valgtTogreise = int(input("Velg togreise: "))
        gyldigTogreise = False
        for seng in ledigeSenger:
            if seng[0] == valgtTogreise:
                gyldigTogreise = True
                print(f"Sengnummer {seng[2]} i kupenummer {(seng[2]+1)//2} i vogn nummer {seng[1]} på togreise {seng[0]} fra {seng[6]} {dato} {seng[7]}")

        if gyldigTogreise:
            valgtVogn = int(input("Velg vognNR: "))
            gyldigVogn = False
            for seng in ledigeSenger:
                if seng[0] == valgtTogreise and seng[1] == valgtVogn:
                    gyldigVogn = True
                    print(f"Sengnummer {seng[2]} i kupenummer {(seng[2]+1)//2} i vogn nummer {seng[1]} på togreise {seng[0]} fra {seng[6]} {dato} {seng[7]}")

            if gyldigVogn:
                valgtSeng = int(input("Velg sengNR: "))
                gyldigSeng = False
                for seng in ledigeSenger:
                    if seng[0] == valgtTogreise and seng[1] == valgtVogn and seng[2] == valgtSeng:
                        gyldigSeng = True
                        print("HURRA!")
                if not(gyldigSeng):
                    print("Ikke gyldig sengNR")
                    return None, None, None

            else:
                print("Ikke gyldig vognNR")
                return None, None, None
        else:
            print("Ikke gyldig togreise")
            return None, None, None

        return valgtTogreise, valgtVogn, valgtSeng
    
    #Finner ledige sitteplasser  
    elif plass.lower() == "sete":
        ledigeSeterPaaValgtTogreise=[]
        for togreiseID in hentTogreiseIDer(startstasjon, sluttstasjon, dato, "00:00"):
            cursor.execute('''SELECT DISTINCT vognID
                            FROM SeteIVogn NATURAL JOIN Vognoppsett
                            INNER JOIN Togreise ON ruteID=togruteID
                            WHERE (togreiseID=?) and dato=?''', (togreiseID, dato))
            vognIDer = cursor.fetchall()

            for vognID in vognIDer:
                cursor.execute('''SELECT DISTINCT seteNR
                                FROM SeteIVogn NATURAL JOIN Vognoppsett
                                INNER JOIN Togreise ON ruteID=togruteID
                                WHERE (togreiseID=?) and dato=? and vognID=?''', (togreiseID, dato, vognID[0]))
                seteIDer = cursor.fetchall()

                for seteNR in seteIDer:
                    seteLedigPaaDelstrekning=[]

                    for delstrekingID in finneDelstrekninger(startstasjon, sluttstasjon):
                        cursor.execute('''SELECT * 
                                        FROM SeteLedigPåDelstrekning INNER JOIN Togreise
                                        on SeteLedigPåDelstrekning.togreiseID = Togreise.togreiseID
                                        WHERE (Togreise.dato = ? and SeteLedigPåDelstrekning.togreiseID=? and vognID=? AND seteNR=? AND delstrekningsID=? and ledig = 1)''', (dato, togreiseID, vognID[0], seteNR[0], delstrekingID))
                        ledigSete = cursor.fetchall()
                        if ledigSete!=[]:
                            seteLedigPaaDelstrekning.append(ledigSete[0][1])

                    if sorted(seteLedigPaaDelstrekning)==finneDelstrekninger(startstasjon, sluttstasjon):
                        ledigeSeterPaaValgtTogreise.append(ledigSete)
        
        for ledigSetePaaTogreise in ledigeSeterPaaValgtTogreise:
            print(f"Ledig sete nr {ledigSetePaaTogreise[0][3]} i vogn {ledigSetePaaTogreise[0][2]} på togreise {ledigSetePaaTogreise[0][0]}")
    
        #Lar kunden velge sete og lagrer variable
        valgtTogreise = int(input("Velg togreise: "))
        gyldigTogreise = False
        for ledigSetePaaTogreise in ledigeSeterPaaValgtTogreise:
            if ledigSetePaaTogreise[0][0] == valgtTogreise:
                gyldigTogreise = True
                print(f"Ledig sete nr {ledigSetePaaTogreise[0][3]} i vogn {ledigSetePaaTogreise[0][2]} på togreise {ledigSetePaaTogreise[0][0]}")

        if gyldigTogreise:
            valgtVogn = int(input("Velg vognNR: "))
            gyldigVogn = False
            for ledigSetePaaTogreise in ledigeSeterPaaValgtTogreise:
                if ledigSetePaaTogreise[0][0] == valgtTogreise and ledigSetePaaTogreise[0][2] == valgtVogn:
                    gyldigVogn = True
                    print(f"Ledig sete nr {ledigSetePaaTogreise[0][3]} i vogn {ledigSetePaaTogreise[0][2]} på togreise {ledigSetePaaTogreise[0][0]}")

            if gyldigVogn:
                valgtSete = int(input("Velg seteNR: "))
                gyldigSete = False
                for ledigSetePaaTogreise in ledigeSeterPaaValgtTogreise:
                    if ledigSetePaaTogreise[0][0] == valgtTogreise and ledigSetePaaTogreise[0][2] == valgtVogn and ledigSetePaaTogreise[0][3] == valgtSete:
                        gyldigSete = True
                        print("HURRA!")
                if not(gyldigSete):
                    print("Ikke gyldig seteNR")
                    return None, None, None

            else:
                print("Ikke gyldig vognNR")
                return None, None, None
        else:
            print("Ikke gyldig togreise")
            return None, None, None

        return valgtTogreise, valgtVogn, valgtSete
    

#Hjelpefunksjoner

def retning(startstasjon, sluttstasjon): 
    con = sq.connect('prosjekt.db')
    cursor = con.cursor()
    cursor.execute('''SELECT stasjonNR FROM Togrutetabell
            WHERE togruteID=1 and (jernbanestasjonsnavn=?)''', (startstasjon,))
    startStasjonNr=int(cursor.fetchall()[0][0])
    cursor.execute('''SELECT stasjonNR FROM Togrutetabell
            WHERE togruteID=1 and (jernbanestasjonsnavn=?)''', (sluttstasjon,))
    sluttStasjonNr=int(cursor.fetchall()[0][0])
    if startStasjonNr<sluttStasjonNr:
        return "med"
    else: 
        return "mot"

def hentTogreiseIDer(startstasjon, sluttstasjon, dato, tid):
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
        return False

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

    togreiseIDer=[]
    for togreise in sortertTogreiserFraStasjonEtterDato:
        togreiseIDer.append(togreise[1])
    con.close()
    return togreiseIDer

def finneDelstrekninger(startstasjon, sluttstasjon):
    brukerretning = retning(startstasjon, sluttstasjon)
    con = sq.connect('prosjekt.db')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Delstrekning")
    rows = cursor.fetchall()

    delstrekninger = []
    if brukerretning == "med":
        i = 3
        for delstrekning in rows:
            if delstrekning[i] == startstasjon:
                delstrekninger.append(delstrekning[0])
            elif delstrekning[i+1] == sluttstasjon:
                delstrekninger.append(delstrekning[0])
    else:
        i = 4
        for delstrekning in rows:
            if delstrekning[i] == startstasjon:
                delstrekninger.append(delstrekning[0])
            elif delstrekning[i-1] == sluttstasjon:
                delstrekninger.append(delstrekning[0])

    if len(delstrekninger) > 1:
        if delstrekninger[1] - delstrekninger[0] > 1:
            start = delstrekninger[0] + 1
            slutt = delstrekninger[1]
            for i in range(start, slutt):
                delstrekninger.append(i)
            delstrekninger.sort()
        
    return delstrekninger



#h)

def getPurchasehistory(kundeNR):
    con = sq.connect('prosjekt.db')
    cursor = con.cursor()
    cursor.execute('''SELECT b.billettID, o.ordreNR, o.bestillingsDato, o.bestillingsTid, b.startstasjon, b.endestasjon, b.avgangsdato, rp.seteNR, 
    rp.vognID, sp.sengNR, sp.vognID FROM Bestilling c JOIN Kundeordre o ON c.ordreNR = o.ordreNR JOIN BillettKjøp t ON o.ordreNR = t.ordreNR 
    JOIN Billett b on t.billettID = b.billettID LEFT JOIN ReservertSetePlass rp on rp.billettID = b.billettID 
    LEFT JOIN ReservertSengeplass sp on sp.billettID = b.billettID WHERE c.kundeNR = ?''', (kundeNR,))
    
    rows = cursor.fetchall()
    if rows== None:
        raise Exception("Du har ingen kjøp enda.")
    print(f"Kjøpshistorikken til kundenummer {kundeNR} er:\n")
    for row in rows:
        if row[7] != None:
            print(f'BilettID: {row[0]} | OrdreNR: {row[1]} | Bestillingsdato: {row[2]} | Bestillingstid: {row[3]}\nStartstasjon: {row[4]} | Endestasjon: {row[5]} | Avgangsdato: {row[6]} | SeteNr: {row[7]} | VognID: {row[8]}')
        else:
            print(f'BilettID: {row[0]} | OrdreNR: {row[1]} | Bestillingsdato: {row[2]} | Bestillingstid: {row[3]}\nStartstasjon: {row[4]} | Endestasjon: {row[5]} | Avgangsdato: {row[6]} | SengNr: {row[9]} | VognID: {row[10]}')
        print('\n')
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
        dato = input("Dato (på format DD.MM.YYYY): ")
        tid = input("Tid (på format HH:MM): ")
        hentTogreise(startstasjon,sluttstasjon,dato,tid)
    
    elif valg == "C" or valg == "c":
        registrateCustomer()
    
    
    elif valg == "D" or valg == "d":
        print("Login for å få kjøpt billetter:")
        print("(Du må være en registrert kunde i kunderegisteret.)")
        navn = input("Navn: ")
        epost = input("Epost: ")
        if validCustomer(navn, epost) == False:
            raise Exception("Navn og epost matcher ikke med en kunde i kunderegisteret.")
        con = sq.connect('prosjekt.db')
        cursor = con.cursor()
        cursor.execute("SELECT DISTINCT dato FROM Togreise")
        rows = cursor.fetchall()
        dato = input("Hvilken dato vil du reise? ")
        datoer = []
        for row in rows:
            datoer.append(row[0])
        if dato not in datoer:
            raise Exception("Ingen avganger denne datoen")
        startstasjon = input("Hvor reiser du fra? ")
        sluttstasjon = input("Hvor vil du reise til? ")
        plass = input("Seng eller sete? ")
        buyTickets(dato, startstasjon, sluttstasjon, plass, navn, epost)
    
    
    elif valg == "E" or valg == "e":
        kundeNR= int(input("KundeNR: "))
        getPurchasehistory(kundeNR)
    
    else:
        raise Exception("Du må velge en av de oppgitte bokstavene.")

launch()




    










