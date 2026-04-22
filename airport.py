class Airport:
   def __init__(self,ICAO,lat,lon,schengen):
       self.ICAO = ICAO
       self.latitude = lat
       self.longitude = lon
       self.schengen = schengen



EsSc=['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH', 'BI','LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']


def IsSchengenAirport(code):
    Schengen = False
    if code == " ":
        Schengen = False
    else:
        i = 0
        while i < len(EsSc) and not Schengen:
            if code[0:2] == EsSc[i]:
                Schengen = True
            else:
                i = i + 1
        return Schengen


def SetSchengen(airport):
    resultat = IsSchengenAirport(airport.ICAO)
    airport.schengen=resultat


def PrintAirport(airport):
    print("ICAO:", airport.ICAO)
    print("Latitude:", airport.latitude)
    print("Longitude:", airport.longitude)
    print("Schengen:", airport.schengen)


def LoadAirports(filename):
    aeroports=[]

    try:
        file=open(filename, "r")
    except FileNotFoundError:
        return aeroports

    file.readline()
    linea=file.readline()


    while linea != "":
        parts= linea.split()


        lat_text =parts[1]
        lon_text=parts[2]


        graus_lat=int(lat_text[1:3])
        minuts_lat=int(lat_text[3:5])
        segons_lat=int(lat_text[5:7])
        latitud = graus_lat + minuts_lat / 60 + segons_lat / 3600
        if lat_text[0]=="S":
            latitud=-latitud
        if len(lon_text) == 8:  # W0223620
            graus_lon = int(lon_text[1:4])
            minuts_lon = int(lon_text[4:6])
            segons_lon = int(lon_text[6:8])
            longitud = graus_lon + minuts_lon / 60 + segons_lon / 3600
        elif len(lon_text) == 7:  # E0031252
            graus_lon = int(lon_text[1:3])
            minuts_lon = int(lon_text[3:5])
            segons_lon = int(lon_text[5:7])
            longitud = graus_lon + minuts_lon / 60 + segons_lon / 3600
        if lon_text[0]=="W":
            longitud=-longitud

        nou=Airport(parts[0],latitud,longitud,SetSchengen)
        SetSchengen(nou)
        aeroports.append(nou)
        linea=file.readline()
    return aeroports




def SaveSchengenAirports(airports,filename):
    if len(airports)==0:
        return -1
    try:
        f=open(filename, "w")
        f.write("CODE LAT LON\n")

        i=0
        while i < len(airports):
            A=airports[i]
            if A.schengen==True:

                f.write(A.ICAO+" "+str(A.latitude)+" "+str(A.longitude)+"\n")
            i=i+1
        f.close()

    except:
        return -1

def AddAirport(airports,airport):
    i=0
    trobat=False
    while i < len(airports) and not trobat:
        if airports[i].ICAO == airport.ICAO:
            trobat=True
        i=i+1
    if not trobat:
        airports.append(airport)



def RemoveAirport(airports,code):
    i=0
    trobat=False
    while i < len(airports) and not trobat:
        if airports[i].ICAO == code:
            airports.remove(airports[i])
            trobat=True
        i=i+1


import os
import matplotlib.pyplot as plt

def PlotAirports(airports):
    schengen = 0
    noschengen = 0
    i = 0
    while i < len(airports):
        if airports[i].schengen:
            schengen = schengen + 1
        else:
            noschengen = noschengen + 1
        i = i + 1
    plt.bar(["Airports"],[schengen],label="Schengen")
    plt.bar(["Airports"],[noschengen],bottom=[schengen],label="No Schengen")
    plt.ylabel("Number of airports")
    plt.title("Schengen / No Schengen")
    plt.legend()
    plt.show()

def MapAirports(airports):
   f = open("airports.kml", "w")
   f.write("""<kml xmlns="http://www.opengis.net/kml/2.2">
   <Document>""")
   i=0
   while i < len(airports):
       if airports[i].schengen:
           icon="http://maps.google.com/mapfiles/kml/paddle/blu-circle.png"
       else:
           icon="http://maps.google.com/mapfiles/kml/paddle/ylw-circle.png"
       f.write(f"""
       <Placemark>
           <name> {airports[i].ICAO} </name>
           <Style>
               <IconStyle>
                   <Icon>
                       <href>{icon}</href>
                   </Icon>
               </IconStyle>
           </Style>
           <Point>
               <coordinates>{airports[i].longitude},{airports[i].latitude},0</coordinates>
           </Point>
       </Placemark>""")
       i=i+1
   f.write("</Document>\n</kml>")
   f.close()
   os.startfile("airports.kml")













