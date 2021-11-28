
#Nog toevoegen indien nodig
import MySQLdb
from datetime import datetime
from datetime import date

#Definitie voor laatste toevoeging TE BETALEN. Mag "ergens in file" bij andere functies
def calculate_betalen(extra):
    hours = extra.hour
    minutes = extra.minute
    if minutes >=30:
        hours_total = hours +1 
        day = (extra.day) * 24
        hours_total = hours_total + day
        tebetalen = hours_total * parkeertarief
        tebetalen = round(tebetalen, 2)
        tebetalen = str(tebetalen)
        return tebetalen
    else:
        day = (extra.day) * 24
        tebetalen = (day + hours) * parkeertarief
        tebetalen = round(tebetalen, 2)
        tebetalen = str(tebetalen)
        return tebetalen


# Staat al in de file ; is extra voor testing
database = MySQLdb.connect(host="localhost", user="pi", passwd="raspberry", db="parkeergarage")
cursor = database.cursor()

# Test data. Nummerplaat en tijdstip STAAN AL IN DE PYTHON FILE! Enkel "vertrek" en parkeertarief toevoegen voor een "realistische tijd" die langer dan 2 minuten duurt
nummerplaat = "1-ABZ-456"

#Parkeerspot moet niet toegevoegd worden, = de waarde die komt vanuit de "LDR" = LOW -> = parking nummer # (enkel INT, geen STR. Parking = 1, of 2, of 3, maar niet "parking 1")
parkingspot = "3"
tijdstip=datetime.now()


#Enkel deze twee toevoegen aan python file; parkeertarief = te betalen bedrag en vertrek = "doen alsof auto later vertrekt"
parkeertarief = 2
vertrek = datetime(2021,11,29)
status_aankomst = "bezet"
status_vertrek = "beschikbaar"


#Eerste aanroeping in onze webpagina: voegt aankomst aan slagboom + nummerplaat toe aan DB
cursor.execute("INSERT INTO nrplaat(aankomst,nummerplaat) VALUE(%s, %s) ON DUPLICATE KEY UPDATE aankomst = CURRENT_TIMESTAMP", (tijdstip,nummerplaat))
database.commit()


# PER PARKEERPLAATS: voegt parkeerplaats toe in DB bij nummerplaat gescanned slagboom, daarnaast ook in de "parkingspot" DB om beschikbaarheid / parkeerplaats weer te geven
cursor.execute("UPDATE nrplaat SET parkingspot=%s  WHERE nummerplaat=%s", (parkingspot, nummerplaat))
cursor.execute("UPDATE parkingspot SET status=%s, aankomst=CURRENT_TIMESTAMP  WHERE parkingspot=%s", (status_aankomst, parkingspot))
database.commit()


# Einde parkeerbezoek - bij vertrek slagboom. Voegt vertrektijd bij nummerplaat toe in DB
cursor.execute("UPDATE nrplaat SET vertrek=%s  WHERE nummerplaat=%s", (vertrek, nummerplaat))
cursor.execute("UPDATE parkingspot SET status=%s, aankomst=CURRENT_TIMESTAMP WHERE parkingspot=%s", (status_vertrek, parkingspot))
database.commit()


# WERKT ENKEL ALS AANKOMST EN VERTREK IN DB STAAN (zie boven): berekent het "te betalen" bedrag ; helemaal achteraan
cursor.execute("SELECT aankomst, vertrek FROM nrplaat WHERE nummerplaat=%s", [nummerplaat])
data = cursor.fetchall()

try:
    for row in data:
        aankomen = row[0]
        vertrekken = row[1]
        print("aankomst = ", row[0], )
        print("vertrek = ", row[1])
        test = vertrekken - aankomen
        print(test)
        print("------------------------------------")
        newDate = datetime.strptime(str(test), "%H:%M:%S")
        hours = newDate.hour
        minutes = newDate.minute
        if minutes >=30:
            hours_total = hours +1
            print(hours_total)
            tebetalen = hours_total * parkeertarief
            tebetalen = round(tebetalen, 2)
            tebetalen = str(tebetalen)
            print(tebetalen)
        else:
            tebetalen = hours * parkeertarief
            tebetalen = round(tebetalen, 2)
            tebetalen = str(tebetalen)
            print(tebetalen)


except ValueError:
    try:
        oneday = datetime.strptime(str(test), "%d day, %H:%M:%S")
        print("There is one additional day.")
        tebetalen = calculate_betalen(oneday)
        print(tebetalen)


    except ValueError:
        days = datetime.strptime(str(test), "%d days, %H:%M:%S")
        print("There are more than 1 day.")
        tebetalen = calculate_betalen(days)
        print(tebetalen)


cursor.execute("UPDATE nrplaat SET tebetalen=%s  WHERE nummerplaat=%s", (tebetalen, nummerplaat))
database.commit()
