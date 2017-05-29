import sqlite3

conn = sqlite3.connect('predictit.db')
cursor = conn.cursor()
questions=cursor.execute("SELECT * FROM questions")
lengths=[]

for question in questions:
    lengths.append(tuple([len(q) for q in question]))

for i in range(len(lengths[0])):
    print(i, max([l[i] for l in lengths]))


contract_vars=cursor.execute("SELECT * FROM contract_vars")
for var in contract_vars:
    print(var[2])

