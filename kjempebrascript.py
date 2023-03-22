# TogreiseID 1,2,3,4,5,6
# respektiv ruteID: 1-1, 2-2, 3-3, 4-1, 5-2, 6-3
# for hver togreise registrer delstrekninger

# 1: Trondheim - Bodø: delstrekning 1,2,3,4,5
# 2: Trondheim - Bodø: delstrekning 1,2,3,4,5
# 3: Mo i Rana - Trondheim delstrekning 1,2,3


# INSERT INTO SeteLedigPåDelstrekning (togreiseID, DelstrekningsID, vognID, seteNR, ledig) VALUES ()

for i in range(1,7):
    for j in range():
        if (i == 3 or i == 6):
            break
        print(f'''INSERT INTO SeteLedigPåDelstrekning (togreiseID, DelstrekningsID, vognID, seteNR, ledig) VALUES ({i}, {j}, {}, {}, {True})''')