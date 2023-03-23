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
        cursor.execute('''SELECT SLPT.togreiseID, SLPT.vognID, SLPT.sengNR, SLPT.ledig, T.togruteID, T.dato, Tt.jernbanestasjonsnavn, Tt.avgangstid
                FROM SengLedigPåTogreise as SLPT INNER JOIN Togreise as T
                on SLPT.togreiseID = T.togreiseID
                INNER JOIN Togrutetabell as Tt
                on Tt.togruteID = T.togruteID
                WHERE (T.dato = ? AND ledig = 1) AND jernbanestasjonsnavn="Trondheim";''', (dato,))
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