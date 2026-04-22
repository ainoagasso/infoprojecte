import tkinter as tk
from tkinter import filedialog
import airport as ap
import aircraft as ar




airports = []
aircrafts=[]

def actualitzar_pantalla():
    llista_airports.delete(0, tk.END) # Esborra tota la llista de la pantalla
    i = 0
    while i < len(airports):
        if airports[i].schengen==True:
            estat="Schengen"
        else:
            estat="No Schengen"
        text = airports[i].ICAO + " - " + str(round(airports[i].latitude,4)) + " - " + str(round(airports[i].longitude,4)) + " - " + estat
        llista_airports.insert(tk.END, text)
        i = i + 1

def actualitzar_pantalla2():
    llista_aircrafts.delete(0, tk.END)
    i=0
    while i < len(aircrafts):
        text=aircrafts[i].id + " - " + aircrafts[i].company + " - " + aircrafts[i].airport + " - " + aircrafts[i].time
        llista_aircrafts.insert(tk.END, text)
        i = i + 1


def boto_carregar():
    global airports
    ruta = filedialog.askopenfilename()
    if ruta:
        airports = ap.LoadAirports(ruta)
        actualitzar_pantalla()
        label_result.config(text="Airports loaded: " +
str(len(airports)), fg="green")
    else:
        label_result.config(text="Please enter a filename to load", fg="red")

def boto_carregar_arrivals():
    global aircrafts
    ruta = filedialog.askopenfilename()
    if ruta:
        aircrafts = ar.LoadArrivals(ruta)
        actualitzar_pantalla2()
        label_result.config(text="Flights loaded: " +
                                 str(len(aircrafts)), fg="green")
    else:
        label_result.config(text="Please enter a filename to load", fg="red")

def boto_afegir():
    f_nova = tk.Toplevel(finestra)
    f_nova.title("Nou Aeroport")
    f_nova.geometry("300x400")

    tk.Label(f_nova, text="Codi ICAO:").pack()
    e_icao = tk.Entry(f_nova)
    e_icao.pack(pady=5)

    tk.Label(f_nova, text="Latitud:").pack()
    e_lat = tk.Entry(f_nova)
    e_lat.pack(pady=5)

    tk.Label(f_nova, text="Longitud:").pack()
    e_lon = tk.Entry(f_nova)
    e_lon.pack(pady=5)

    def guardar_nou():
        try:
            nou = ap.Airport(e_icao.get().upper(), float(e_lat.get()), float(e_lon.get()))
            ap.AddAirport(airports, nou)
            actualitzar_pantalla()
            f_nova.destroy()
        except:
            label_result.config(text="Error in airport data",fg="red")

    tk.Button(f_nova, text="Guardar", command=guardar_nou).pack(pady=5)

def boto_guardar_aeroports():
    global airports
    fitxer_desti = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Fitxers de text", "*.txt"), ("Tots els fitxers", "*.*")],
        title="Guardar llista d'aeroports schengen"
    )

    if fitxer_desti:
        resultat = ap.SaveSchengenAirports(airports, fitxer_desti)

        if resultat == 0:
            label_result.config(text="Aeroports schengen guardats amb èxit", fg="green")
        else:
            label_result.config(text="No s'ha pogut guardar el fitxer", fg="red")

def boto_guardar_vols():
    global aircrafts
    fitxer_desti = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Fitxers de text", "*.txt"), ("Tots els fitxers", "*.*")],
        title="Guardar llista de vols"
    )

    if fitxer_desti:
        resultat = ar.SaveFlights(aircrafts, fitxer_desti)

        if resultat == 0:
            label_result.config(text="Vols guardats amb èxit", fg="green")
        else:
            label_result.config(text="No s'ha pogut guardar el fitxer", fg="red")


def boto_eliminar():
    # Mirem quin element ha marcat l'usuari amb el ratolí
    index = llista_airports.curselection()
    if index:
        posicio = index[0]
        codi = airports[posicio].ICAO
        ap.RemoveAirport(airports, codi)
        actualitzar_pantalla()

def boto_schengen():
    i = 0
    while i < len(airports):
        ap.SetSchengen(airports[i])
        i = i + 1
    actualitzar_pantalla()
    label_result.config(text="Schengen updated", fg="green")

def boto_grafic():
    ap.PlotAirports(airports)

def boto_mapa():
    ap.MapAirports(airports)

def PlotArrivalsButton():
    if len(airports) == 0:
        label_result.config(text="Load airports first")
        return
    ar.PlotArrivals(aircrafts)

def PlotAirlinesButton():
    if len(airports) == 0:
        label_result.config(text="Load airports first")
        return
    ar.PlotAirlines(aircrafts)

def PlotFlightsTypeButton():
    if len(airports) == 0:
        label_result.config(text="Load airports first")
        return
    ar.PlotFlightsType(aircrafts)

def boto_mapa2():
    ar.MapFlights(aircrafts, airports)

def ShowLongDistanceButton():
    global aircrafts
    global airports
    if len(airports) == 0:
        label_result.config(text="Load airports first")
        return

    aircrafts = ar.LongDistanceArrivals(aircrafts,airports)
    actualitzar_pantalla2()
    label_result.config(text="Long distance flights shown: " +
                             str(len(aircrafts)))






finestra = tk.Tk()
finestra.title("Interfaç")
finestra.geometry("1000x700")

frame_principal = tk.Frame(finestra)
frame_principal.pack(fill="both", expand=True, padx=20, pady=30)

frame_esquerra = tk.Frame(frame_principal)
frame_esquerra.pack(side="left",fill="y",expand=True,padx=20,pady=100)


#missatges feedback
label_result = tk.Label(finestra, text="", font=("Arial",10,"bold"),fg="black")
label_result.pack(padx=10, pady=10)

#PART AIRPORT

#primer rectangle
frame_airports = tk.Frame(frame_principal)
frame_airports.pack(side="left", fill="both", expand=True, padx=5)
tk.Label(frame_airports, text="Aeroports", font=("Arial", 10, "bold")).pack()
llista_airports = tk.Listbox(frame_airports, width=40, height=30)
llista_airports.pack(fill="both", expand=True)

bloc1 = tk.Frame(frame_esquerra)
bloc1.pack(fill="x", padx=35,pady=0)


tk.Button(bloc1, text="Carregar fitxer aeroports", command=boto_carregar).grid(row=0, column=0,padx=5,pady=5,sticky="ew")
tk.Button(bloc1, text="Afegir aeroport", command=boto_afegir).grid(row=1, column=0,padx=5,pady=5,sticky="ew")
tk.Button(bloc1, text="Eliminar aeroport", command=boto_eliminar).grid(row=2, column=0,padx=5,pady=5,sticky="ew")

tk.Button(bloc1, text="Validar schengen", command=boto_schengen).grid(row=0, column=1,padx=5,pady=5,sticky="ew")
tk.Button(bloc1, text="Schengen/No Schengen", command=boto_grafic).grid(row=1, column=1,padx=5,pady=5,sticky="ew")
tk.Button(bloc1, text="Aeroports en Google Earth", command=boto_mapa).grid(row=2, column=1,padx=5,pady=5,sticky="ew")

#PART AIRCRAFT

#segon rectangle
frame_aircrafts = tk.Frame(frame_principal)
frame_aircrafts.pack(side="left", fill="both", expand=True, padx=5)

tk.Label(frame_aircrafts, text="Vols", font=("Arial", 10, "bold")).pack()
llista_aircrafts = tk.Listbox(frame_aircrafts, width=40, height=30)
llista_aircrafts.pack(fill="both", expand=True)


bloc2 = tk.Frame(frame_esquerra)
bloc2.pack(fill="x",pady=(0,20))


tk.Button(bloc2, text="Carregar fitxer vols", command=boto_carregar_arrivals).grid(row=0, column=0,padx=5,pady=(40,5),sticky="ew")
tk.Button(bloc2,text="Arrivades més llunyanes",command=ShowLongDistanceButton).grid(row=1, column=0,padx=5,pady=5,sticky="ew")
tk.Button(bloc2,text="Trajectòries des de Barcelona",command=boto_mapa2).grid(row=2, column=0,padx=5,pady=5,sticky="ew")

tk.Button(bloc2,text="Freqüència d'aterratge durant el dia",command=PlotArrivalsButton).grid(row=0, column=1,padx=5,pady=(40,5),sticky="ew")
tk.Button(bloc2,text="Nombre de vols per aerolínea", command=PlotAirlinesButton).grid(row=1, column=1,padx=5,pady=5,sticky="ew")
tk.Button(bloc2,text="Arrivant des de Schengen o no",command=PlotFlightsTypeButton).grid(row=2, column=1,padx=5,pady=5,sticky="ew")

bloc3 = tk.Frame(frame_esquerra)
bloc3.pack(fill="x",padx=40,pady=10)

tk.Button(bloc3,text="Guardar aeroports Schengen",command=boto_guardar_aeroports).grid(row=0, column=0,padx=5,pady=5,sticky="ew")
tk.Button(bloc3,text="Guardar vols",command=boto_guardar_vols).grid(row=0, column=1,padx=5,pady=5,sticky="ew")

finestra.mainloop()



