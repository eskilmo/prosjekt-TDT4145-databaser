# TogreiseID 1,2,3,4,5,6
# respektiv ruteID: 1-1, 2-2, 3-3, 4-1, 5-2, 6-3
# for hver togreise registrer delstrekninger

# 1: Trondheim - Bodø: delstrekning 1,2,3,4,5
# 2: Trondheim - Bodø: delstrekning 1,2,3,4,5
# 3: Mo i Rana - Trondheim delstrekning 1,2,3


# INSERT INTO SeteLedigPåDelstrekning (togreiseID, DelstrekningsID, vognID, seteNR, ledig) VALUES ()

for i in range(1,7):
    if (i == 3 or i == 6):
        for x in range(1,4):
            print(f'''INSERT INTO SeteLedigPåDelstrekning (togreiseID, DelstrekningsID, vognID, seteNR, ledig) VALUES ({i}, {x}, {1}, {1}, {True})''')
    else:
        for j in range(1,6):
            print(f'''INSERT INTO SeteLedigPåDelstrekning (togreiseID, DelstrekningsID, vognID, seteNR, ledig) VALUES ({i}, {j}, {1}, {1}, {True})''')