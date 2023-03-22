CREATE table Jernbanestasjon (
    navn VARCHAR(40) NOT NULL,
    moh FLOAT,
    CONSTRAINT jernbanestrekning_PK PRIMARY KEY (navn));

CREATE table Banestrekning (
    navn VARCHAR(40) NOT NULL,
    startstasjon VARCHAR(40) NOT NULL,
    endestasjon VARCHAR(40) NOT NULL,
    fremdriftsenergi VARCHAR(20),
    CONSTRAINT banestrekning_PK PRIMARY KEY (navn)
    CONSTRAINT banestrekning_FK1 FOREIGN KEY (startstasjon) REFERENCES Jernbanestasjon(navn) ON UPDATE CASCADE ON DELETE NO ACTION, 
    CONSTRAINT banestrekning_FK2 FOREIGN KEY (endestasjon) REFERENCES Jernbanestasjon(navn) ON UPDATE CASCADE ON DELETE NO ACTION);

CREATE table Delstrekning (
    delstrekningsID INTEGER NOT NULL,
    lengde INTEGER,
    sportype VARCHAR(20),
    startstasjon VARCHAR(40) NOT NULL,
    sluttstasjon VARCHAR(40) NOT NULL,
    CONSTRAINT delstrekning_PK PRIMARY KEY (delstrekningsID),
    CONSTRAINT delstrekning_FK1 FOREIGN KEY (startstasjon) REFERENCES Jernbanestasjon(navn) ON UPDATE CASCADE ON DELETE NO ACTION, 
    CONSTRAINT delstrekning_FK2 FOREIGN KEY (sluttstasjon) REFERENCES Jernbanestasjon(navn) ON UPDATE CASCADE ON DELETE NO ACTION);

CREATE table BestårAv (
    banestrekningsnavn VARCHAR(40) NOT NULL,
    delstrekningsID INTEGER NOT NULL,
    CONSTRAINT bestårav_PK PRIMARY KEY (banestrekningsnavn, delstrekningsID), 
    CONSTRAINT bestårav_FK1 FOREIGN KEY (banestrekningsnavn) REFERENCES Banestrekning(navn) ON UPDATE CASCADE ON DELETE NO ACTION, 
    CONSTRAINT bestårav_FK2 FOREIGN KEY (delstrekningsID) REFERENCES Delstrekning(delstrekningsID) ON UPDATE CASCADE ON DELETE NO ACTION);

CREATE table Togrute (
    ruteID INTEGER NOT NULL,
    startstasjon VARCHAR(40) NOT NULL,
    endestasjon VARCHAR(40) NOT NULL,
    hovedretning VARCHAR(20),
    operatør VARCHAR(40) NOT NULL,
    CONSTRAINT togrute_PK PRIMARY KEY (ruteID),
    CONSTRAINT togrute_FK1 FOREIGN KEY (startstasjon) REFERENCES Jernbanestasjon(navn) ON UPDATE CASCADE ON DELETE NO ACTION, 
    CONSTRAINT togrute_FK2 FOREIGN KEY (endestasjon) REFERENCES Jernbanestasjon(navn) ON UPDATE CASCADE ON DELETE NO ACTION,
    CONSTRAINT togrute_FK3 FOREIGN KEY (operatør) REFERENCES Operatør(navn) ON UPDATE CASCADE ON DELETE CASCADE);

CREATE table DelstrekningPåTogrute (
    ruteID INTEGER NOT NULL,
    delstrekningsID INTEGER NOT NULL,
    CONSTRAINT delstrekningpåtogrute_PK PRIMARY KEY (ruteID, delstrekningsID), 
    CONSTRAINT delstrekningpåtogrute_FK1 FOREIGN KEY (ruteID) REFERENCES Togrute(ruteID) ON UPDATE CASCADE ON DELETE NO ACTION, 
    CONSTRAINT delstrekningpåtogrute_FK2 FOREIGN KEY (delstrekningsID) REFERENCES Delstrekning(delstrekningsID) ON UPDATE CASCADE ON DELETE NO ACTION);


CREATE table Togreise (
	togreiseID INTEGER NOT NULL,
    togruteID INTEGER NOT NULL, 
    dato VARCHAR(10) NOT NULL,
	CONSTRAINT togreise_PK PRIMARY KEY (togreiseID),
    CONSTRAINT togreise_FK1 FOREIGN KEY (togruteID) REFERENCES Togrute(ruteID) ON UPDATE CASCADE ON DELETE CASCADE);

CREATE table Avgangsdager (
    ruteID INTEGER NOT NULL,
    dag VARCHAR(20) NOT NULL,
    CONSTRAINT avgangsdager_PK PRIMARY KEY (ruteID, dag),
	CONSTRAINT avgangsdager_FK1 FOREIGN KEY (ruteID) REFERENCES Togrute(ruteID) ON UPDATE CASCADE ON DELETE CASCADE);

CREATE table Ruter (
    togruteID INTEGER NOT NULL,
    banestrekningsnavn VARCHAR(40) NOT NULL,
    CONSTRAINT ruter_PK PRIMARY KEY (togruteID),
    CONSTRAINT ruter_FK FOREIGN KEY (banestrekningsnavn) REFERENCES Banestrekning(navn) ON UPDATE CASCADE ON DELETE CASCADE);

CREATE table Togrutetabell (
    togruteID INTEGER NOT NULL,
    jernbanestasjonsnavn VARCHAR(40) NOT NULL,
    ankomsttid VARCHAR(10),
    avgangstid VARCHAR(10),
    StasjonNR INTEGER,
    CONSTRAINT togrutetabell_PK PRIMARY KEY (togruteID, jernbanestasjonsnavn),
    CONSTRAINT togrutetabell_FK1 FOREIGN KEY (togruteID) REFERENCES Togrute(ruteID) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT togrutetabell_FK2 FOREIGN KEY (jernbanestasjonsnavn) REFERENCES Jernbanestasjon(navn) ON UPDATE CASCADE ON DELETE CASCADE);

CREATE table Vogn (
    vognID INTEGER NOT NULL,
    vognNR INTEGER,
    navn VARCHAR(40),
    CONSTRAINT vogn_PK PRIMARY KEY (vognID));

CREATE table Vognoppsett (
    vognID INTEGER NOT NULL,
    ruteID INTEGER NOT NULL,
    CONSTRAINT vognoppsett_PK PRIMARY KEY (vognID),
	CONSTRAINT vognoppsett_FK1 FOREIGN KEY (vognID) REFERENCES Vogn(vognID) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT vognoppsett_FK2 FOREIGN KEY (ruteID) REFERENCES Togrute(ruteID) ON UPDATE CASCADE ON DELETE CASCADE);

CREATE table Sittevogn (
    vognID INTEGER NOT NULL,
    antallStolrader INTEGER,
    antallSeterPrRad INTEGER,
    CONSTRAINT sittevogn_PK PRIMARY KEY (vognID),
	CONSTRAINT sittevogn_FK1 FOREIGN KEY (vognID) REFERENCES Vogn(vognID) ON UPDATE CASCADE ON DELETE CASCADE);

CREATE table Sovevogn (
    vognID INTEGER NOT NULL,
    antallSovekupeer INTEGER,
    CONSTRAINT sovevogn_PK PRIMARY KEY (vognID),
	CONSTRAINT sovevogn_FK1 FOREIGN KEY (vognID) REFERENCES Vogn(vognID) ON UPDATE CASCADE ON DELETE CASCADE);
	
CREATE table Sete (
	seteNR INTEGER NOT NULL,
	CONSTRAINT sete_PK PRIMARY KEY (seteNR));
	
CREATE table SeteIVogn (
	vognID INTEGER NOT NULL,
	seteNR INTEGER NOT NULL,
	CONSTRAINT seteivogn_PK PRIMARY KEY (vognID, seteNR),
	CONSTRAINT seteivogn_FK1 FOREIGN KEY (vognID) REFERENCES Sittevogn(vognID) ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT seteivogn_FK2 FOREIGN KEY (seteNR) REFERENCES Sete(seteNR) ON UPDATE CASCADE ON DELETE NO ACTION);
	
CREATE table SengIVogn (
	vognID INTEGER NOT NULL,
    sengNR INTEGER NOT Null,
	CONSTRAINT sengivogn_PK PRIMARY KEY (vognID, sengNR),
	CONSTRAINT sengivogn_FK1 FOREIGN KEY (vognID) REFERENCES Sovevogn(VognID) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT sengivogn_FK2 FOREIGN KEY (sengNR) REFERENCES Seng(sengNR) ON UPDATE CASCADE ON DELETE NO ACTION);

CREATE table Seng (
	sengNR INTEGER NOT NULL,
	CONSTRAINT seng_PK PRIMARY KEY (sengNR));

CREATE table VognerTilgjengelig (
	vognID INTEGER NOT NULL,
	operatørNavn VARCHAR(40) NOT NULL,
	CONSTRAINT vognertilgjengelig_PK PRIMARY KEY (vognID),
	CONSTRAINT vognertilgjengelig_FK1 FOREIGN KEY (vognID) REFERENCES Vogn(vognID) ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT vognertilgjengelig_FK2 FOREIGN KEY (operatørNavn) REFERENCES Operatør(navn) ON UPDATE CASCADE ON DELETE CASCADE);

CREATE table Operatør (
	antallVogner INTEGER,
	navn VARCHAR(40) NOT NULL,
	CONSTRAINT operatør_PK PRIMARY KEY (navn));

CREATE table RuteOperatør (
	ruteID INTEGER NOT NULL,
	operatørNavn VARCHAR(40) NOT NULL,
	CONSTRAINT ruteoperatør_PK PRIMARY KEY (ruteID),
	CONSTRAINT ruteoperatør_FK1 FOREIGN KEY (operatørNavn) REFERENCES Operatør(navn) ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT ruteoperatør_FK2 FOREIGN KEY (ruteID) REFERENCES Togrute(ruteID) ON UPDATE CASCADE ON DELETE CASCADE);

CREATE table Kunde (
	kundeNR INTEGER NOT NULL,
	mobilNR INTEGER NOT NULL,
    epost VARCHAR(50),
    navn VARCHAR(40),
	CONSTRAINT kunde_PK PRIMARY KEY (kundeNR));

CREATE table Bestilling (
	kundeNR INTEGER NOT NULL,
	ordreNR INTEGER NOT NULL,
	CONSTRAINT bestilling_PK PRIMARY KEY (kundeNR, ordreNR),
    CONSTRAINT bestilling_FK1 FOREIGN KEY (kundeNR) REFERENCES Kunde(kundeNR) ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT bestilling_FK2 FOREIGN KEY (ordreNR) REFERENCES Kundeordre(ordreNR) ON UPDATE CASCADE ON DELETE CASCADE);


CREATE table Kundeordre (
	antallBilletter INTEGER NOT NULL,
	ordreNR INTEGER NOT NULL,
    bestillingsDato VARCHAR(10) NOT NULL,
    bestillingsTid VARCHAR(10) NOT NULL,
	CONSTRAINT kundeordre_PK PRIMARY KEY (ordreNR));


CREATE table BillettKjøp (
    billettID INTEGER NOT NULL,
    ordreNR INTEGER NOT NULL,
    CONSTRAINT billett_PK PRIMARY KEY (billettID),
    CONSTRAINT billett_FK1 FOREIGN KEY (billettID) REFERENCES Billett(billettID) ON UPDATE NO ACTION ON DELETE CASCADE, 
    CONSTRAINT billett_FK2 FOREIGN KEY (ordreNR) REFERENCES Kundeordre(ordreNR) ON UPDATE NO ACTION ON DELETE CASCADE);

CREATE table Billett (
    billettID INTEGER NOT NULL,
    startstasjon VARCHAR(40) NOT NULL,
    endestasjon VARCHAR(40) NOT NULL,
    avgangsdato VARCHAR(10) NOT NULL,
    CONSTRAINT billett_PK PRIMARY KEY (billettID),
    CONSTRAINT billett_FK1 FOREIGN KEY (startstasjon) REFERENCES Jernbanestasjon(navn) ON UPDATE CASCADE ON DELETE CASCADE, 
    CONSTRAINT billett_FK2 FOREIGN KEY (endestasjon) REFERENCES Jernbanestasjon(navn) ON UPDATE CASCADE ON DELETE CASCADE);

CREATE table ReservertSengeplass (
    billettID INTEGER NOT NULL,
    sengNR INTEGER NOT NULL,
    vognID INTEGER NOT NULL,
    CONSTRAINT reservertsengeplass_PK PRIMARY KEY (billettID),
    CONSTRAINT reservertseteplass_FK1 FOREIGN KEY (billettID) REFERENCES Billett(billettID) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT reservertseteplass_FK2 FOREIGN KEY (sengNR, vognID) REFERENCES SengIVogn(sengNR, vognID) ON UPDATE CASCADE ON DELETE CASCADE);

CREATE table ReservertSetePlass (
    billettID INTEGER NOT NULL,
    seteNR INTEGER NOT NULL,
    vognID INTEGER NOT NULL,
    CONSTRAINT reservertseteplass_PK PRIMARY KEY (billettID),
    CONSTRAINT reservertseteplass_FK1 FOREIGN KEY (billettID) REFERENCES Billett(billettID) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT reservertseteplass_FK2 FOREIGN KEY (seteNR, vognID) REFERENCES SeteIVogn(seteNR, vognID) ON UPDATE CASCADE ON DELETE CASCADE);

CREATE table SengLedigPåTogReise (
	togreiseID INTEGER NOT NULL,
    vognID INTEGER NOT NULL,
    sengNR INTEGER NOT NULL,
    ledig BOOLEAN,
	CONSTRAINT sengledigpåtogreise_PK PRIMARY KEY (togreiseID, vognID, sengNR),
    CONSTRAINT sengledigpåtogreise_FK1 FOREIGN KEY (togreiseID) REFERENCES Togreise(togreiseID) ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT sengledigpåtogreise_FK2 FOREIGN KEY (vognID, sengNR) REFERENCES SengIVogn(vognID, sengNR) ON UPDATE CASCADE ON DELETE CASCADE);

CREATE table SeteLedigPåDelstrekning (
	togreiseID INTEGER NOT NULL,
	delstrekningsID INTEGER NOT NULL,
    vognID INTEGER NOT NULL,
    seteNR INTEGER NOT NULL,
    ledig BOOLEAN,
	CONSTRAINT seteledigpådelstrekning_PK PRIMARY KEY (togreiseID, delstrekningsID, vognID, seteNR),
	CONSTRAINT seteledigpådelstrekning_FK1 FOREIGN KEY (togreiseID) REFERENCES Togreise(togreiseID) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT seteledigpådelstrekning_FK2 FOREIGN KEY (delstrekningsID) REFERENCES Delstrekning(delstrekningsID) ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT seteledigpådelstrekning_FK3 FOREIGN KEY (vognID, seteNR) REFERENCES SeteIVogn(vognID, seteNR) ON UPDATE CASCADE ON DELETE CASCADE);
	




	

	


	






