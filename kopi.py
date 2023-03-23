import sqlite3 as sq


def buy_tickets():
    con = sq.connect("prosjekt.db")
    cursor = con.cursor()
    print("Login for å få kjøpt billetter:")
    navn = input("Navn: ")
    epost = input("Epost: ")
    if valid_customer(navn, epost) == False:
            raise Exception("Du har ikke registrert deg i kunderegisteret.")

    #LEGG INN KODE HER HÅKON

    #få metode for å få inn alle e finne ledige billetter for en oppgitt strekning 
    #på en ønsket togrute og kjøpe de billettene hen ønsker
    #ledigeBilletter=
    
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
    if AntallBilletter > ledigeBilletter:
        raise Exception("Det er ikke så mange billetter som er tilgjengelig på denne delstrekningen.")
    bestillingsdato = date.today().strftime("%m/%d/%Y")
    #bestillingstid = 

    
def kjop(dato, startstasjon, sluttstasjon, plass):
    con = sq.connect("prosjekt.db")
    cursor = con.cursor()

    #Input flyttes ut av funksjonen
    # dato = input("Hvilken dato vil du reise? ")
    # startstasjon = input("Hvor reiser du fra? ")
    # sluttstasjon = input("Hvor vil du reise til? ")
    # plass = input("Seng eller sete? ")
    
    #Finner ledige senger
    if plass.lower() == "seng":

        ledigeSenger=[]
        brukerretning=retning(startstasjon, sluttstasjon)
        cursor.execute('''SELECT SLPT.togreiseID, SLPT.vognID, SLPT.sengNR, SLPT.ledig, T.togruteID, T.dato, Tt.jernbanestasjonsnavn, Tt.avgangstid, Togrute.hovedretning
                FROM SengLedigPåTogreise as SLPT INNER JOIN Togreise as T
                on SLPT.togreiseID = T.togreiseID
                INNER JOIN Togrutetabell as Tt
                on Tt.togruteID = T.togruteID
                INNER JOIN Togrute
                on T.togruteID = Togrute.ruteID
                WHERE ((T.dato = ? AND ledig = 1) AND jernbanestasjonsnavn = ?) AND Togrute.hovedretning = ?;''', (dato, startstasjon, brukerretning))
        sengePlasser = cursor.fetchall()

        for i in range(0,len(sengePlasser)-1,2):
            if sengePlasser[i][3]==1 and sengePlasser[i+1][3]:
                ledigeSenger.append(sengePlasser[i])
                ledigeSenger.append(sengePlasser[i+1])
        
        if len(ledigeSenger)==0:
            print(f"Ingen ledige senger fra {startstasjon} {dato}")
        else:
            print("Ledige sengeplasser:")
            for seng in ledigeSenger:
                print(f"Sengnummer {seng[2]} i kupenummer {(seng[2]+1)//2} på togreise {seng[0]} fra {seng[6]} {dato} {seng[7]}")

    #Finner ledige sitteplasser  
    else:
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
                        if ledigSete!=None:
                            seteLedigPaaDelstrekning.append(ledigSete[0][1])

                    if sorted(seteLedigPaaDelstrekning)==finneDelstrekninger(startstasjon, sluttstasjon):
                        ledigeSeterPaaValgtTogreise.append(ledigSete)
        
        for ledigSetePaaTogreise in ledigeSeterPaaValgtTogreise:
            print(f"Ledig sete nr {ledigSetePaaTogreise[0][3]} i vogn {ledigSetePaaTogreise[0][2]} på togreise {ledigSetePaaTogreise[0][0]}")


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

#Funksjon som tar inn ønsket start- og sluttstasjon med dato og tid for en reise,
#og returner liste med togreiseIDer som kan kjøre valgt rute. (Nesten kopi av hentTogreiser) 
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


