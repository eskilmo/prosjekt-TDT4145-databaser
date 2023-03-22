INSERT INTO Jernbanestasjon (navn, moh) VALUES ("Trondheim", 5.1);
INSERT INTO Jernbanestasjon (navn, moh) VALUES ("Steinkjer", 3.6);
INSERT INTO Jernbanestasjon (navn, moh) VALUES ("Mosjøen", 6.8);
INSERT INTO Jernbanestasjon (navn, moh) VALUES ("Mo i Rana", 3.5);
INSERT INTO Jernbanestasjon (navn, moh) VALUES ("Fauske", 34.0);
INSERT INTO Jernbanestasjon (navn, moh) VALUES ("Bodø", 4.1);

INSERT INTO Banestrekning (navn, startstasjon, endestasjon, fremdriftsenergi) VALUES ("Nordlandsbanen", "Trondheim", "Bodø", "Diesel");

INSERT INTO Delstrekning (delstrekningsID, lengde, sportype, startstasjon, sluttstasjon) VALUES (1, 120, "Dobbel", "Trondheim", "Steinkjer");
INSERT INTO Delstrekning (delstrekningsID, lengde, sportype, startstasjon, sluttstasjon) VALUES (2, 280, "Enkel", "Steinkjer", "Mosjøen");
INSERT INTO Delstrekning (delstrekningsID, lengde, sportype, startstasjon, sluttstasjon) VALUES (3, 90, "Enkel", "Mosjøen", "Mo i Rana");
INSERT INTO Delstrekning (delstrekningsID, lengde, sportype, startstasjon, sluttstasjon) VALUES (4, 170, "Enkel", "Mo i Rana", "Fauske");
INSERT INTO Delstrekning (delstrekningsID, lengde, sportype, startstasjon, sluttstasjon) VALUES (5, 60, "Enkel", "Fauske", "Bodø");

INSERT INTO BestårAv (banestrekningsnavn, delstrekningsID) VALUES ("Nordlandsbanen", 1);
INSERT INTO BestårAv (banestrekningsnavn, delstrekningsID) VALUES ("Nordlandsbanen", 2);
INSERT INTO BestårAv (banestrekningsnavn, delstrekningsID) VALUES ("Nordlandsbanen", 3);
INSERT INTO BestårAv (banestrekningsnavn, delstrekningsID) VALUES ("Nordlandsbanen", 4);
INSERT INTO BestårAv (banestrekningsnavn, delstrekningsID) VALUES ("Nordlandsbanen", 5);

INSERT INTO Operatør (antallVogner, navn) VALUES (5, "SJ");

INSERT INTO Togrute (ruteID, startstasjon, endestasjon, hovedretning, operatør) VALUES (1, "Trondheim", "Bodø", "med", "SJ");
INSERT INTO Togrute VALUES (2, "Trondheim", "Bodø", "med", "SJ");
INSERT INTO Togrute VALUES (3, "Mo i Rana", "Trondheim", "mot", "SJ");

INSERT INTO DelstrekningPåTogrute VALUES (1, 1);
INSERT INTO DelstrekningPåTogrute VALUES (1, 2);
INSERT INTO DelstrekningPåTogrute VALUES (1, 3);
INSERT INTO DelstrekningPåTogrute VALUES (1, 4);
INSERT INTO DelstrekningPåTogrute VALUES (1, 5);

INSERT INTO DelstrekningPåTogrute VALUES (2, 1);
INSERT INTO DelstrekningPåTogrute VALUES (2, 2);
INSERT INTO DelstrekningPåTogrute VALUES (2, 3);
INSERT INTO DelstrekningPåTogrute VALUES (2, 4);
INSERT INTO DelstrekningPåTogrute VALUES (2, 5);

INSERT INTO DelstrekningPåTogrute VALUES (3, 1);
INSERT INTO DelstrekningPåTogrute VALUES (3, 2);
INSERT INTO DelstrekningPåTogrute VALUES (3, 3);


INSERT INTO Togreise VALUES (1, 1, "03.04.2023");
INSERT INTO Togreise VALUES (2, 2, "03.04.2023");
INSERT INTO Togreise VALUES (3, 3, "03.04.2023");

INSERT INTO Togreise VALUES (4, 1, "04.04.2023");
INSERT INTO Togreise VALUES (5, 2, "04.04.2023");
INSERT INTO Togreise VALUES (6, 3, "04.04.2023");

INSERT INTO Vogn (vognID, vognNR, navn) VALUES (1, 1,"SJ-sittevogn1");
INSERT INTO Vogn (vognID, vognNR, navn) VALUES (3, 2,"SJ-sittevogn1");
INSERT INTO Vogn (vognID, vognNR, navn) VALUES (4, 1,"SJ-sittevogn1");
INSERT INTO Vogn (vognID, vognNR, navn) VALUES (2, 2,"SJ-sovevogn1");
INSERT INTO Vogn (vognID, vognNR, navn) VALUES (5, 1,"SJ-sittevogn1");

INSERT INTO Sittevogn (vognID, antallStolrader, antallSeterPrRad) VALUES (1, 3, 4);
INSERT INTO Sovevogn (vognID, antallSovekupeer) VALUES (2, 4);
INSERT INTO Sittevogn (vognID, antallStolrader, antallSeterPrRad) VALUES (3, 3, 4);                             
INSERT INTO Sittevogn (vognID, antallStolrader, antallSeterPrRad) VALUES (4, 3, 4);                    
INSERT INTO Sittevogn (vognID, antallStolrader, antallSeterPrRad) VALUES (5, 3, 4);

INSERT INTO Avgangsdager VALUES (1, "mandag");
INSERT INTO Avgangsdager VALUES (1, "tirsdag");
INSERT INTO Avgangsdager VALUES (1, "onsdag");
INSERT INTO Avgangsdager VALUES (1, "torsdag");
INSERT INTO Avgangsdager VALUES (1, "fredag");

INSERT INTO Avgangsdager VALUES (2, "mandag");
INSERT INTO Avgangsdager VALUES (2, "tirsdag");
INSERT INTO Avgangsdager VALUES (2, "onsdag");
INSERT INTO Avgangsdager VALUES (2, "torsdag");
INSERT INTO Avgangsdager VALUES (2, "fredag");
INSERT INTO Avgangsdager VALUES (2, "lørdag");
INSERT INTO Avgangsdager VALUES (2, "søndag");

INSERT INTO Avgangsdager VALUES (3, "mandag");
INSERT INTO Avgangsdager VALUES (3, "tirsdag");
INSERT INTO Avgangsdager VALUES (3, "onsdag");
INSERT INTO Avgangsdager VALUES (3, "torsdag");
INSERT INTO Avgangsdager VALUES (3, "fredag");

INSERT INTO Ruter (togruteID, banestrekningsnavn) VALUES (1, "Nordlandsbanen");
INSERT INTO Ruter (togruteID, banestrekningsnavn) VALUES (2, "Nordlandsbanen");
INSERT INTO Ruter (togruteID, banestrekningsnavn) VALUES (3, "Nordlandsbanen");

INSERT INTO Vognoppsett (ruteID, vognID) VALUES (1, 1); 
INSERT INTO Vognoppsett (ruteID, vognID) VALUES (1, 3);
INSERT INTO Vognoppsett (ruteID, vognID) VALUES (2, 4);
INSERT INTO Vognoppsett (ruteID, vognID) VALUES (2, 2);  
INSERT INTO Vognoppsett (ruteID, vognID) VALUES (3, 5);

INSERT INTO Seng (sengNR) VALUES (1);
INSERT INTO Seng (sengNR) VALUES (2);
INSERT INTO Seng (sengNR) VALUES (3);
INSERT INTO Seng (sengNR) VALUES (4);
INSERT INTO Seng (sengNR) VALUES (5);
INSERT INTO Seng (sengNR) VALUES (6);
INSERT INTO Seng (sengNR) VALUES (7);
INSERT INTO Seng (sengNR) VALUES (8);

INSERT INTO SengIVogn (vognID, sengNR) VALUES (2, 1);
INSERT INTO SengIVogn (vognID, sengNR) VALUES (2, 2);
INSERT INTO SengIVogn (vognID, sengNR) VALUES (2, 3);
INSERT INTO SengIVogn (vognID, sengNR) VALUES (2, 4);
INSERT INTO SengIVogn (vognID, sengNR) VALUES (2, 5);
INSERT INTO SengIVogn (vognID, sengNR) VALUES (2, 6);
INSERT INTO SengIVogn (vognID, sengNR) VALUES (2, 7);
INSERT INTO SengIVogn (vognID, sengNR) VALUES (2, 8);

INSERT INTO Togrutetabell VALUES (1, "Trondheim", NULL, "07:49");
INSERT INTO Togrutetabell VALUES (1, "Steinkjer", NULL, "09:51");
INSERT INTO Togrutetabell VALUES (1, "Mosjøen", NULL, "13:20");
INSERT INTO Togrutetabell VALUES (1, "Mo i Rana", NULL, "14:31");
INSERT INTO Togrutetabell VALUES (1, "Fauske", NULL, "16:49");
INSERT INTO Togrutetabell VALUES (1, "Bodø", "17:34", NULL);

INSERT INTO Togrutetabell VALUES (2, "Trondheim", NULL, "23:05");
INSERT INTO Togrutetabell VALUES (2, "Steinkjer", NULL, "00:57");
INSERT INTO Togrutetabell VALUES (2, "Mosjøen", NULL, "04:41");
INSERT INTO Togrutetabell VALUES (2, "Mo i Rana", NULL, "05:55");
INSERT INTO Togrutetabell VALUES (2, "Fauske", NULL, "08:19");
INSERT INTO Togrutetabell VALUES (2, "Bodø", "09:05", NULL);

INSERT INTO Togrutetabell VALUES (3, "Mo i Rana", NULL, "08:11");
INSERT INTO Togrutetabell VALUES (3, "Mosjøen", NULL, "09:14");
INSERT INTO Togrutetabell VALUES (3, "Steinkjer", NULL, "12:31");
INSERT INTO Togrutetabell VALUES (3, "Trondheim", "14:13", NULL);

INSERT INTO RuteOperatør VALUES (1, "SJ");
INSERT INTO RuteOperatør VALUES (2, "SJ");
INSERT INTO RuteOperatør VALUES (3, "SJ");

INSERT INTO Sete (seteNR) VALUES (1);
INSERT INTO Sete (seteNR) VALUES (2);
INSERT INTO Sete (seteNR) VALUES (3);
INSERT INTO Sete (seteNR) VALUES (4);
INSERT INTO Sete (seteNR) VALUES (5);
INSERT INTO Sete (seteNR) VALUES (6);
INSERT INTO Sete (seteNR) VALUES (7);
INSERT INTO Sete (seteNR) VALUES (8);
INSERT INTO Sete (seteNR) VALUES (9);
INSERT INTO Sete (seteNR) VALUES (10);
INSERT INTO Sete (seteNR) VALUES (11);
INSERT INTO Sete (seteNR) VALUES (12);


INSERT INTO SeteIVogn (vognID,seteNR) VALUES (1,1);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (1,2);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (1,3);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (1,4);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (1,5);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (1,6);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (1,7);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (1,8);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (1,9);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (1,10);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (1,11);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (1,12);

INSERT INTO SeteIVogn (vognID,seteNR) VALUES (3,1);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (3,2);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (3,3);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (3,4);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (3,5);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (3,6);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (3,7);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (3,8);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (3,9);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (3,10);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (3,11);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (3,12);

INSERT INTO SeteIVogn (vognID,seteNR) VALUES (4,1);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (4,2);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (4,3);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (4,4);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (4,5);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (4,6);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (4,7);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (4,8);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (4,9);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (4,10);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (4,11);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (4,12);

INSERT INTO SeteIVogn (vognID,seteNR) VALUES (5,1);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (5,2);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (5,3);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (5,4);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (5,5);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (5,6);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (5,7);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (5,8);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (5,9);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (5,10);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (5,11);
INSERT INTO SeteIVogn (vognID,seteNR) VALUES (5,12);

INSERT INTO VognerTilgjengelig (vognID, operatørNavn) VALUES (1,"SJ");
INSERT INTO VognerTilgjengelig (vognID, operatørNavn) VALUES (2,"SJ");
INSERT INTO VognerTilgjengelig (vognID, operatørNavn) VALUES (3,"SJ");
INSERT INTO VognerTilgjengelig (vognID, operatørNavn) VALUES (4,"SJ");
INSERT INTO VognerTilgjengelig (vognID, operatørNavn) VALUES (5,"SJ");