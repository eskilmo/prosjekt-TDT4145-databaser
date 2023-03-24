for i in range(1,7):
    if (i == 3 or i == 6):
        #delstrekningsID
        for x in range(1,4):
            #seteNR
            for k in range(1, 13):
                #vognID
                if (i == 1 or i == 4):
                    z = 1
                    print(f'''INSERT INTO SeteLedigPåDelstrekning (togreiseID, DelstrekningsID, vognID, seteNR, ledig) VALUES ({i}, {x}, {3}, {k}, {True});''')
                elif (i == 2 or i == 5):
                    z = 4
                elif (i == 3 or i == 6):
                    z = 5
                print(f'''INSERT INTO SeteLedigPåDelstrekning (togreiseID, DelstrekningsID, vognID, seteNR, ledig) VALUES ({i}, {x}, {z}, {k}, {True});''')   
    else:
        #delstrekningsID
        for j in range(1,6):
            #seteNr
            for h in range(1,13):
                #vognID
                if (i == 1 or i == 4):
                    z = 1
                    print(f'''INSERT INTO SeteLedigPåDelstrekning (togreiseID, DelstrekningsID, vognID, seteNR, ledig) VALUES ({i}, {j}, {3}, {h}, {True});''')
                elif (i == 2 or i == 5):
                    z = 4
                elif (i == 3 or i == 6):
                    z = 5
                print(f'''INSERT INTO SeteLedigPåDelstrekning (togreiseID, DelstrekningsID, vognID, seteNR, ledig) VALUES ({i}, {j}, {z}, {h}, {True});''')
