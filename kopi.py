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

    
con = sq.connect("prosjekt.db")
cursor = con.cursor()

dato = input("Hvilken dato vil du reise? ")
startstasjon = input("Hvor reiser du fra? ")
sluttstasjon = input("Hvor vil du reise til? ")
plass = input("Seng eller sete? ")


if plass.lower() == "seng":
    cursor.execute('''SELECT * 
                    FROM SengLedigPåTogreise INNER JOIN Togreise
                    on SengLedigPåTogreise.togreiseID = Togreise.togreiseID
                    WHERE (Togreise.dato = ? AND ledig = 1)''', (dato,))
    rows = cursor.fetchall()
    print(rows)


else:
    cursor.execute('''SELECT * 
                    FROM SeteLedigPåDelstrekning INNER JOIN Togreise
                    on SeteLedigPåDelstrekning.togreiseID = Togreise.togreiseID
                    WHERE (Togreise.dato = ? AND ledig = 1)''', (dato,))
    rows = cursor.fetchall()
    print(rows)


SELECT SLPT.togreiseID, SLPT.vognID, SLPT.sengNR, SLPT.ledig, T.togruteID, T.dato, Tt.jernbanestasjonsnavn, Tt.avgangstid
FROM SengLedigPåTogreise as SLPT INNER JOIN Togreise as T
on SLPT.togreiseID = T.togreiseID
INNER JOIN Togrutetabell as Tt
on Tt.togruteID = T.togruteID
WHERE (T.dato = "03.04.2023" AND ledig = 1);