from faker import Faker
import psycopg2
import random

import vereinsmitglieder
from create_all_tables import table_creator
from vereine import club_list, lizenzen, altersklasse, spielklasse, strafen
from vereine import strafen, ansetzungskreise, mitgliederplz

conn = psycopg2.connect(
     database = 'test',
     user = 'postgres',
     password = '12',
     host = 'localhost',
     port = '5433'
)

print('connected to db')
# Auswahlwerkzeug für den Zugriff auf die Daten der DB
cur = conn.cursor()

# Werkzeug zum Aufrufen von fake Methoden
fake = Faker(['de_DE'])

# anlegen der Abgabedatei
script = open('neuWI20C_Gruppe4.sql', 'w')

cur.execute(table_creator)

# Vereinsmitglieder
clubmembers = []
i = 1
for row in range(1, 800):
     mitgl = vereinsmitglieder.create_vereinsmitgl(i)
     if mitgl == None:
          pass
     else:
          # mitgliedsnr =mitgl[0]
          vereins_id = mitgl[1]
          vorname = mitgl[2]
          nachname = mitgl[3]
          geb_datum = mitgl[4]
          straße = mitgl[5]
          hausnr = mitgl[6]
          plz = mitgl[7]
          telefon = mitgl[8]
          mail = mitgl[9]

          mitgliederplz.append(plz)
          mitgliederplz.append(plz)

          membercmd = (
               f"INSERT INTO Vereinsmitglieder (Vereinsid, Vorname, Nachname,"
               f" Geburtstag, Strasse, Hausnummer, Plz, Telnr, Email) VALUES (" 
               f"'{vereins_id}', '{vorname}', '{nachname}', '{geb_datum}',"
               f" '{straße}', '{hausnr}', '{plz}', '{telefon}', '{mail}')"
               )
          clubmembers.append(f"{membercmd};\n")
          cur.execute(membercmd)
          conn.commit()
     i += 1
     
mitgliederplz_set = []
for value in set(mitgliederplz):
     mitgliederplz_set.append(value)

for club in club_list:
     cmd = f"INSERT INTO Vereine (vereinsname) VALUES ('{club}')"
     script.write(f"{cmd};\n")
     cur.execute(cmd)
     conn.commit()
script.write('\n')

#Schleife für Tabelle Ansetzungskreise
a = 0
for value in range(1,len(ansetzungskreise)-1):
     cmd = (
          f"INSERT INTO Ansetzungskreise (AkID, Name) "
          f"VALUES('{value}','{ansetzungskreise[a]}')"
     )
     script.write(f"{cmd};\n")
     cur.execute(cmd)
     conn.commit()
     a += 1
script.write('\n')

#PLZ
cur.execute(f"SELECT * FROM Ansetzungskreise")
ansetzungskr = cur.fetchall()
i= 0
for postcode in mitgliederplz_set:
     ak = ansetzungskr[random.randint(0,len(ansetzungskr)-1)]
     cmd = (
          f"INSERT INTO PLZ (PLZ, AkID, Ort)VALUES('"
          f"{postcode}','{ak[0]}', "
          f"'{fake.city()}')"
          )
     try:
          cur.execute(cmd)
          script.write(f"{cmd};\n")
     except:
          cur.execute('rollback')
          continue
     conn.commit()
     i+=1
script.write('\n')

# Vereinsmitglieder an richtiger Stelle ins Script sqldok. schreiben
for member in clubmembers:
     script.write(f"{member};\n")
script.write('\n')

#Mitglieder in Trainer, Spieler und Schiris aufteilen
cur.execute(f"SELECT * FROM Vereinsmitglieder")
mitgl = cur.fetchall()

spieler = []
trainer = []
schiris = []

for tup in mitgl:
     mitglnr = tup[0]
     if (tup[0] % 8) == 0:
          trainer.append(
               f"INSERT INTO Trainer (MitgliedsNr, Trainerlizenz) VALUES"
               f"('{mitglnr}','{lizenzen[random.randint(0,3)]}')"
          )
     elif (tup[0] % 5) == 0:
          spieler.append(f"INSERT INTO Spieler (MitgliedsNr) VALUES({mitglnr})")
          cur.execute(f"SELECT * FROM PLZ")
          plz = cur.fetchall()
          lehrgem = plz[random.randint(1,50)]
          date_lehrgem = fake.date_this_year()
          schiris.append(
               f"INSERT INTO Schiedsrichter (Mitgliedsnr, Lehrgemeinschaft, Jahresprüfung,"
               f" höchsteSpielklasseLeitung, höchsteAltersklasseLeitung, AkIDLeitung) "
               f"VALUES ('{tup[0]}', '{lehrgem[2]}', '{date_lehrgem}',"
               f" '{spielklasse[random.randint(0,6)]}', '{altersklasse[random.randint(0,5)]}',"
               f" {lehrgem[1]})"
          )
     else:
          spieler.append(f"INSERT INTO Spieler (MitgliedsNr) VALUES({mitglnr})")
script.write('\n')

#Spieler in script schreiben und ind db eintragen
for phrase in spieler:
     script.write(f"{phrase};\n")
     cur.execute(phrase)
script.write('\n')

#Spieler in script schreiben
for phrase in trainer:
     script.write(f"{phrase};\n")
     cur.execute(phrase)
script.write('\n')

#Schiris in script schreiben
for phrase in schiris:
     script.write(f"{phrase};\n")
     cur.execute(phrase)
script.write('\n')

#Mannschaften
count= 0
while count < 7:
     for vereinsid in range(39):
          cmd = (
               f"INSERT INTO Mannschaften (VereinsID, Spielklasse, "
               f"Altersklasse, Rang) VALUES ({vereinsid},"
               f"'{spielklasse[count]}', '{altersklasse[random.randint(0,5)]}',"
               f" '{random.randint(1,8)}')"
               )
          script.write(f"{cmd};\n")
          cur.execute(cmd)
     count += 1
script.write('\n')

#Ansetzer
cur.execute(f"SELECT * FROM Schiedsrichter")
ansetzer = cur.fetchall()
for ans in ansetzer:
     if (ans[0] % 5) == 0:
          cur.execute(f"SELECT * FROM PLZ")
          plz = cur.fetchall()
          lehrgem = mitgliederplz_set[random.randint(1,len(mitgliederplz_set)-1)]
          cmd = (
               f"INSERT INTO Ansetzer (AusweisNr, höchsteSpielklasseAnsetzung, "
               f"höchsteAltersklasseAnsetzung, AkIDAnsetzung) VALUES ({ans[1]}, "
               f"'{spielklasse[random.randint(0,6)]}', "
               f"'{altersklasse[random.randint(0,5)]}', '{lehrgem}')"
          )
          script.write(f"{cmd};\n")
          try:
               cur.execute(cmd)
               script.write(f"{cmd};\n")
          except:
               cur.execute('rollback')
               continue
          conn.commit()
script.write('\n')

#Favoriten
cur.execute(f"SELECT * FROM Schiedsrichter")
schiedsrichter = cur.fetchall()
f = 0
while f < 3:
     for sr in schiedsrichter:
          cmd = (
               f"INSERT INTO Favoriten (HauptSr_AusweisNr, AssistentSr_AusweisNr)"
               f" VALUES ({sr[1]}, '{random.randint(1,len(schiedsrichter))}')"
          )
          try:
               cur.execute(cmd)
               script.write(f"{cmd};\n")
          except:
               cur.execute('rollback')
               continue
          conn.commit()
     f += 1
script.write('\n')

#Freitermine
days_off = 0
while days_off < 8:
     for sr in schiedsrichter:
          if (days_off % 4) == 0:
               cmd = (
                      f"INSERT INTO Freitermine (Sr_AusweisNr, Datum, Startzeit) VALUES ({sr[1]},"
                      f" '{fake.future_date(+375)}','{str(fake.time()).replace('-',':')}')"
                     )
          else :
               cmd = (
                      f"INSERT INTO Freitermine (Sr_AusweisNr, Datum) VALUES ({sr[1]},"
                      f"'{fake.future_date(+375)}')"
                     )
          try:
               cur.execute(cmd)
               script.write(f"{cmd};\n")
          except:
               cur.execute('rollback')
               continue
          conn.commit()
     days_off += 1
script.write('\n')

#Spiele
print('working on "Spiele"')
#selfjoin mit bedingungen
cur.execute(
     f"select distinct * from mannschaften as a, mannschaften as b "
     f"where a.mannschaftsid != b.mannschaftsid and a.spielklasse"
     f" = b.spielklasse and a.altersklasse = b.altersklasse"
     )
spielpartner = cur.fetchall()
cur.execute(f"SELECT * FROM PLZ")
plz = cur.fetchall()
for partner in spielpartner:
     plz = plz[random.randint(0, len(plz)-1)]
     heim = partner[0]
     gast = partner[5]
     cmd = (
          f"INSERT INTO Spiele (HeimmannschaftID, GastmannschaftID,"
          f" Strasse, Hausnummer, PLZ, Platzname, Datum, Startzeit) "
          f"VALUES ({heim}, {gast}, "
          f"'{fake.street_name()}', '{random.randint(1,150)}', "
          f"'{plz[0]}', 'KR', "
          f"'{fake.date_this_year()}', '{fake.time()}' )"
          )
     try:
          cur.execute(cmd)
          script.write(f"{cmd};\n")
     except:
          cur.execute('rollback')
          continue
     conn.commit()
print('finished "Spiele"')
script.write('\n')

#Strafe
print('working on "PersönlicheStrafen"')
cur.execute(f"SELECT * FROM Mannschaften")
mannschaften = cur.fetchall()
m = 0
while m < 2:
     for mannsch in mannschaften:
          cur.execute(f"SELECT * FROM Spiele")
          Spiele = cur.fetchall()
          Spiel = Spiele[random.randint(1,len(Spiele)-1)]
          script.write( 
               f"INSERT INTO PersönlicheStrafen (SpielID, Zeitpunkt, Typ, MannschaftsID)"
               f" VALUES ('{Spiel[0]}', '{fake.time()}',"
               f"'{strafen[random.randint(0,3)]}', {Spiel[random.randint(1,2)]})"
          )
          script.write(f"{cmd};\n")
          try:
               cur.execute(cmd)
               script.write(f"{cmd};\n")
          except:
               cur.execute('rollback')
               continue
          conn.commit()
     m += 1
print('finished "PersönlicheStrafen"')

# Ansetzungen ausgelassen

cur.close()
conn.close()
script.close()