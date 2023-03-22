#vognID 2 kjører kjører ruteID 2 med delstrekningsID 1,2,3,4,5

#togreiseID
for i in range(2, 6, 3):
    for j in range(1, 9):
        print(f'''INSERT INTO SengLedigPåTogreise (togreiseID, vognID, sengNR, ledig) VALUES ({i}, {2}, {j}, {True});''')
    