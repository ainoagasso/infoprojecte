from airport import *

class Aircraft:
    def __init__(self, id="", company="", airport="", time="",destination="",departure_time="",delay_minutes="",delay=""):
        self.id = id
        self.company = company
        self.airport = airport
        self.time = time
        self.destination=destination
        self.departure_time=departure_time
        self.delay_minutes=delay_minutes
        self_delay=delay


def LoadArrivals (Filename):
   try:
       Fin=open(Filename)
       linea=Fin.readline()
       Arrivals=[]
       while linea!="":
           trozos=linea.split()
           if trozos[0]=="AIRCRAFT":
               linea=Fin.readline()
               continue
           elif len(trozos)!=4:
               linea=Fin.readline()
               continue


           id=trozos[0]
           airport=trozos[1]
           time=trozos[2]
           company=trozos[3]


           parts=time.split(':')
           if len(parts)!=2:
               linea=Fin.readline()
               continue


           hores=int(parts[0])
           minuts=int(parts[1])


           if hores < 0 or hores >= 24 or minuts < 0 or minuts >= 60:
               linea=Fin.readline()
               continue


           a=Aircraft(id,company,airport,time)
           Arrivals.append(a)
           linea=Fin.readline()
       Fin.close()


   except FileNotFoundError:
       return []
   return Arrivals


def PlotArrivals(aircrafts):
    fig,ax=plt.subplots(figsize=(10, 5))
    if len(aircrafts)==0:
        print("LLista buida")
        return
    i=0
    count=[0]*24
    while i<len(aircrafts):
        time=aircrafts[i].time
        trozos=time.split(':')
        hores=int(trozos[0])
        count[hores]=count[hores]+1
        i=i+1
    X=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]

    ax.bar(X, count, color='skyblue')

    ax.set_xlabel("Hora del dia")
    ax.set_ylabel("Nombre d'aterratges")
    ax.set_title("Freqüència d'arribades per franja horària")

   # Marquem totes les hores a sota perquè es llegeixin bé
    ax.set_xticks(X)
    fig.tight_layout()
    return fig

def SaveFlights(aircrafts,filename):
   if len(aircrafts)==0:
       return -1
   Fout = open(filename, "w")
   Fout.write("AIRCRAFT ORIGIN ARRIVAL AIRLINE\n")
   i=0
   while i<len(aircrafts):
       if aircrafts[i].id=="":
           id="-"
       else:
           id=aircrafts[i].id
       if aircrafts[i].airport=="":
           airport="-"
       else:
           airport=aircrafts[i].airport
       if aircrafts[i].time=="":
           time="-"
       else:
           time=aircrafts[i].time
       if aircrafts[i].company=="":
           company="-"
       else:
           company=aircrafts[i].company
       linea=id+" "+airport+" "+time+" "+company
       Fout.write(linea+"\n")
       i=i+1
   Fout.close()
   return 0

def PlotAirlines(aircrafts):
    fig,ax = plt.subplots(figsize=(14,6))
    if len(aircrafts)==0:
        print("Llista buida")
        return -1
    i=0
    X=[]
    Y=[]
    while i<len(aircrafts):
        company=aircrafts[i].company
        k=0
        encontrado=False
        while k<len(X) and not encontrado:
            if company==X[k]:
                encontrado=True
            else:
                k=k+1
        if not encontrado:
            X.append(company)
            Y.append(1)
        else:
            Y[k]=Y[k]+1
        i=i+1

    ax.bar(X,Y)
    ax.set_title("Nombre de vols per companyia aèria")
    ax.set_xlabel("Companyia")
    ax.set_ylabel("Freqüència")

    fig.tight_layout()
    ax.tick_params(axis='x', rotation=90,labelsize=6)


    return fig

import matplotlib.pyplot as plt


EsSc=['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH', 'BI','LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']


def PlotFlightsType(aircrafts):
    fig,ax = plt.subplots()
    if len(aircrafts) == 0:
        print("Error: La llista d'aeronaus està buida.")
        return
    schengen_count=0
    noschengen_count=0
    i=0
    while i<len(aircrafts):
        j = 0
        trobat=False
        while j<len(EsSc) and not trobat:
            if aircrafts[i].airport[0:2]==EsSc[j]:
                trobat=True
            else:
                j+=1
        if trobat:
            schengen_count+=1
        else:
            noschengen_count+=1
        i+=1
    ax.bar("Tipus de vol", schengen_count, label="Schengen",color="green")
    ax.bar("Tipus de vol", noschengen_count, label="non-Schengen",color="red",alpha=0.8, bottom=schengen_count)
    ax.set_ylabel("Nombre de vols")
    ax.set_xlabel("Origen")
    ax.legend()
    fig.tight_layout()
    return fig



def MapFlights(aircrafts, airports):


    if len(aircrafts) == 0:
        print("Error: La llista està buida")
        return

        # Buscar l'aeroport LEBL
    foundLEBL = False
    i = 0
    while i < len(airports) and foundLEBL == False:
        if airports[i].ICAO == "LEBL":
            lebl_longitude = airports[i].longitude
            lebl_latitude = airports[i].latitude
            foundLEBL = True
        i = i + 1

    if foundLEBL == False:
        print("Error: LEBL airport not found")
        return

    file = open("flights.kml", "w")

    file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    file.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    file.write("<Document>\n<name>Flights to LEBL</name>\n")


    file.write("<Style id=\"schengenStyle\">\n")
    file.write("<LineStyle>\n")
    file.write("<color>ff00ff00</color>\n")
    file.write("<width>2</width>\n")
    file.write("</LineStyle>\n")
    file.write("</Style>\n")

    file.write("<Style id=\"nonSchengenStyle\">\n")
    file.write("<LineStyle>\n")
    file.write("<color>ff0000ff</color>\n")
    file.write("<width>2</width>\n")
    file.write("</LineStyle>\n")
    file.write("</Style>\n")

    i = 0
    while i < len(aircrafts):
        origin_code = aircrafts[i].airport

        foundAirport = False
        j = 0
        while j < len(airports) and foundAirport == False:
            if airports[j].ICAO == origin_code:
                origin_longitude = airports[j].longitude
                origin_latitude = airports[j].latitude
                origin_schengen = airports[j].schengen
                foundAirport = True
            j = j + 1

        if foundAirport == True:
            file.write("<Placemark>\n")
            file.write("<name>" + aircrafts[i].id + "</name>\n")

            if origin_schengen == True:
                file.write("<styleUrl>#schengenStyle</styleUrl>\n")
            else:
                file.write("<styleUrl>#nonSchengenStyle</styleUrl>\n")

            file.write("<LineString>\n")
            file.write("<tessellate>1</tessellate>\n")
            file.write("<coordinates>\n")
            file.write(str(origin_longitude) + "," +
                       str(origin_latitude) + ",0 ")
            file.write(str(lebl_longitude) + "," +
                       str(lebl_latitude) + ",0\n")
            file.write("</coordinates>\n")
            file.write("</LineString>\n")
            file.write("</Placemark>\n")

        i = i + 1
    file.write("</Document>\n")
    file.write("</kml>\n")
    file.close()
    os.startfile("flights.kml")


import math


def HaversineDistance(lat1, lon1, lat2, lon2):
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distancia = 6371.0 * c
    return distancia

def LongDistanceArrivals(aircrafts,airports):
    long_distance_list = []
    lat_lebl = 41.297445
    lon_lebl = 2.0832941
    i = 0
    while i < len(aircrafts):
        codi_origen = aircrafts[i].airport
        j = 0
        encontrado = False
        lat_origen = 0.0
        lon_origen = 0.0
        while j < len(airports) and not encontrado:
            if airports[j].ICAO == codi_origen:
                lat_origen = airports[j].latitude
                lon_origen = airports[j].longitude
                encontrado = True
            else:
                j = j + 1
        if encontrado:
            dist = HaversineDistance(lat_lebl, lon_lebl, lat_origen, lon_origen)
            print(f"Vol {aircrafts[i].id} des de {codi_origen}: Distància = {dist}")
            if dist > 2000.0:
                long_distance_list.append(aircrafts[i])
        i = i + 1

    return long_distance_list

def LoadDepartures(filename):
    try:
        Fin=open(filename,"r")
        títols = Fin.readline()
        Departures=[]
        linea=Fin.readline()
        while linea != "":  # Llegeix el fitxer línia per línia
            parts = linea.strip().split()  # Separa per trossos
            if len(parts) != 4:
                linea = Fin.readline()
                continue

            id=parts[0]
            destination=parts[1]
            departure_time=parts[2]
            company=parts[3]
            trozos = departure_time.split(':')
            if len(trozos) != 2:
                linea = Fin.readline()
                continue
            try:
                hores = int(trozos[0])
                minuts = int(trozos[1])
            except ValueError:
                linea = Fin.readline()
                continue

            if hores < 0 or hores >= 24 or minuts < 0 or minuts >= 60:
                linea = Fin.readline()
                continue

            a = Aircraft(id,company,"","",destination,departure_time)
            Departures.append(a)  # Escriu la llista d'objectes amb el format que es vol
            linea = Fin.readline()
        Fin.close()
    except FileNotFoundError:
        return []
    return Departures


def MergeMovements(arrivals, departures):
    if len(arrivals) == 0 or len(departures) == 0:
        return []

    planes = []
    DepUsats = set()

    def to_minutes(t):
        if ":" not in t:
            return None
        h, m = t.split(":")
        return int(h) * 60 + int(m)

    i = 0
    while i < len(arrivals):

        best_k = -1
        best_dep_time = None

        arr_time = to_minutes(arrivals[i].time)

        k = 0
        while k < len(departures):

            if arrivals[i].id == departures[k].id and arrivals[i].company == departures[k].company:

                dep_time = to_minutes(departures[k].departure_time)

                if arr_time is not None and dep_time is not None and arr_time < dep_time:

                    if best_dep_time is None or dep_time < best_dep_time:
                        best_dep_time = dep_time
                        best_k = k

            k += 1

        if best_k != -1:
            DepUsats.add(best_k)
            planes.append(Aircraft(
                arrivals[i].id,
                arrivals[i].company,
                arrivals[i].airport,
                arrivals[i].time,
                departures[best_k].destination,
                departures[best_k].departure_time
            ))
        else:
            planes.append(arrivals[i])

        i += 1

    n = 0
    while n < len(departures):
        if n not in DepUsats:
            planes.append(departures[n])
        n += 1

    return planes

def NightAircraft(aircrafts):
    if len(aircrafts) == 0:
        return -1

    night_list=[]
    i=0
    while i < len(aircrafts):
        ac=aircrafts[i]
        if ac.airport == "" and ac.time == "":
            night_list.append(ac)
        i += 1

    return night_list

CONSUM_FIX_KG = 800.0
CONSUM_PER_KM = 2.8
FACTOR_CO2 = 3.16


def FlightEmissions(aircraft, airports):
    lat_lebl = 41.297445
    lon_lebl = 2.0832941
    i = 0
    while i < len(airports):
        if airports[i].ICAO == "LEBL":
            lat_lebl = airports[i].latitude
            lon_lebl = airports[i].longitude
        i = i + 1


    lat_origen = None
    lon_origen = None
    j = 0
    while j < len(airports):
        if airports[j].ICAO == aircraft.airport:
            lat_origen = airports[j].latitude
            lon_origen = airports[j].longitude
        j = j + 1


    if lat_origen is None:
        return None


    distancia = HaversineDistance(lat_lebl, lon_lebl, lat_origen, lon_origen)
    combustible = CONSUM_FIX_KG + CONSUM_PER_KM * distancia
    co2 = combustible * FACTOR_CO2


    return {"distancia": distancia, "combustible": combustible, "co2": co2}

def AddDelay(aircraft, delay_minutes, delay_type):
    # Funció per afegir minuts de retras al arrival o departure #
    if aircraft is None:
        return -1
    if delay_minutes <= 0:
        return -1

    if delay_type == "arrival":
        if aircraft.time == "":
            return -1
        parts = aircraft.time.split(':')
    elif delay_type == "departure":
        if aircraft.departure_time == "":
            return -1
        parts = aircraft.departure_time.split(':')
    else:
        return -1

    if len(parts) != 2:
        return -1

    try:
        hours = int(parts[0])
        minutes = int(parts[1])
    except ValueError:
        return -1

    total_minutes = hours * 60 + minutes + delay_minutes

    if total_minutes >= 24 * 60:
        total_minutes = total_minutes % (24 * 60)
    # Aquest if serveix per retards que passin la mitja nit. Ex: 23:50 + :30, mostrarà 00:20 per comptes de 24:20 #
    new_hours = total_minutes // 60
    new_minutes = total_minutes % 60

    if new_minutes < 10:
        new_time = str(new_hours) + ":0" + str(new_minutes)
    else:
        new_time = str(new_hours) + ":" + str(new_minutes)

    if delay_type == "arrival":
        aircraft.time = new_time
    else:
        aircraft.departure_time = new_time
    try:
        aircraft.delay_minutes = int(aircraft.delay_minutes or 0) + delay_minutes
    except ValueError:
        aircraft.delay_minutes = delay_minutes
        # Això en serveix per afegir retards succesius, no només un de sol #
    aircraft.delay = True

    return 0

# test section
if __name__ == "__main__":
    airports = LoadAirports("Airports.txt")
    aircrafts = LoadArrivals("Arrivals.txt")
    i = 0
    while i < len(airports):
        SetSchengen(airports[i])
        i = i + 1

    print("Flights loaded:", len(aircrafts))
    PlotArrivals(aircrafts)
    SaveFlights(aircrafts, "output_arrivals.txt")
    PlotAirlines(aircrafts)
    PlotFlightsType(aircrafts)
    MapFlights(aircrafts, airports)
    longdistance = LongDistanceArrivals(aircrafts,airports)
    print("Long distance flights:", len(longdistance))
    departures = LoadDepartures("Departures.txt")
    print("Departures loaded:", len(departures))
    movements = MergeMovements(aircrafts, departures)
    print("Merged movements:", len(movements))



