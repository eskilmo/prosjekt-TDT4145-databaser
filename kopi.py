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

    
def kjop():
    con = sq.connect("prosjekt.db")
    cursor = con.cursor()

    # dato = input("Hvilken dato vil du reise? ")
    # startstasjon = input("Hvor reiser du fra? ")
    # sluttstasjon = input("Hvor vil du reise til? ")
    # plass = input("Seng eller sete? ")
    dato = "03.04.2023"
    startstasjon = "Trondheim"
    sluttstasjon = "Bodø"
    plass = "seng"

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
        
    else:
        cursor.execute('''SELECT * 
                        FROM SeteLedigPåDelstrekning INNER JOIN Togreise
                        on SeteLedigPåDelstrekning.togreiseID = Togreise.togreiseID
                        WHERE (Togreise.dato = ? AND ledig = 1)''', (dato,))
        rows = cursor.fetchall()
        print(rows)

kjop()


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
        

print(retning("Mo i Rana", "Bodø"))