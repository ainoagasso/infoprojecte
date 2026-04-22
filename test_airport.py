
from airport import *

airports = LoadAirports("Airports.txt")

airport_existe = Airport ("LECC", 43.297445, 2.0832941,False)
print(len(airports))


AddAirport(airports,airport_existe)
print(len(airports))

for airport in airports:
    SetSchengen(airport)


RemoveAirport(airports,"BIKF")
print(len(airports))

SaveSchengenAirports(airports, 'SchengenAirports.txt')

PlotAirports(airports)


MapAirports(airports)







