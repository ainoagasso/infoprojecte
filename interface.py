import tkinter as tk
from tkinter import filedialog
import airport as ap
import aircraft as ar
import LEBL as lbl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt



list_airports = []
aircrafts=[]
bcn=None


def actualitzar_pantalla():
    global list_airports
    llista_airports.delete(0, tk.END) # Esborra tota la llista de la pantalla
    mida=len(list_airports)
    i = 0
    while i < mida:
        aero=list_airports[i]
        if aero.schengen==True:
            estat="Schengen"
        else:
            estat="No Schengen"
        try:
            lat_neta = round(float(aero.latitude), 4)
            lon_neta = round(float(aero.longitude), 4)
        except:
            # Si no es pot convertir, utilitzem el valor tal qual
            lat_neta = aero.latitude
            lon_neta = aero.longitude
        text = str(aero.ICAO) + " - " + str(lat_neta) + " - " + str(lon_neta) + " - " + estat
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
    global list_airports
    ruta = filedialog.askopenfilename()
    if ruta:
        noves = ap.LoadAirports(ruta)
        list_airports.clear()
        list_airports.extend(noves)
        actualitzar_pantalla()
        label_result.config(text="Airports loaded: " +
str(len(list_airports)), fg="green")
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

def boto_carregar_lebl():
    global bcn
    ruta = filedialog.askopenfilename()
    try:
        bcn = lbl.LoadAirportStructure(ruta)
        if bcn != -1:
            label_result.config(text="Estructura LEBL carregada correctament", fg="green")
        else:
            label_result.config(text="Error en carregar l'estructura LEBL", fg="red")
    except Exception as e:
        label_result.config(text="Error: " + str(e), fg="red")
    for t in bcn.terminals:
        print(t.name)
        print(len(t.boarding_areas))

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
        global list_airports
        try:
            codi_escrit = e_icao.get().upper().strip()
            lat_escrita = e_lat.get()
            lon_escrita = e_lon.get()

            es_schengen = ap.IsSchengenAirport(codi_escrit)


            nou = ap.Airport(codi_escrit, float(lat_escrita), float(lon_escrita), es_schengen)

            ap.AddAirport(list_airports, nou)

            actualitzar_pantalla()
            f_nova.destroy()
            label_result.config(text="Aeroport afegit", fg="green")
        except ValueError:
            label_result.config(text="Error: Lat/Lon han de ser números", fg="red")
        except Exception as e:
            label_result.config(text="Error al guardar l'aeroport", fg="red")

    tk.Button(f_nova, text="Guardar", command=guardar_nou).pack(pady=5)

def boto_guardar_aeroports():
    global list_airports
    fitxer_desti = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Fitxers de text", "*.txt"), ("Tots els fitxers", "*.*")],
        title="Guardar llista d'aeroports schengen"
    )

    if fitxer_desti:
        resultat = ap.SaveSchengenAirports(list_airports, fitxer_desti)

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
        codi = list_airports[posicio].ICAO
        ap.RemoveAirport(list_airports, codi)
        actualitzar_pantalla()
        label_result.config(text="Aeroport eliminat", fg="green")
    else:
        label_result.config(text="Selecciona un aeroport", fg="red")

def boto_schengen():
    i = 0
    while i < len(list_airports):
        ap.SetSchengen(list_airports[i])
        i = i + 1
    actualitzar_pantalla()
    label_result.config(text="Schengen updated", fg="green")

def boto_grafic():
    figura=ap.PlotAirports(list_airports)
    incrustar_grafic(figura)
    label_result.config(text="Gràfic Schengen/No Schengen ensenyat", fg="green")

def boto_mapa():
    ap.MapAirports(list_airports)
    label_result.config(text="Aeroports en Google Earth ensenyats", fg="green")

def PlotArrivalsButton():
    if len(list_airports) == 0:
        label_result.config(text="Load airports first")
        return
    figura=ar.PlotArrivals(aircrafts)
    incrustar_grafic(figura)
    label_result.config(text="Gràfic d'aterratges durant el dia ensenyat'", fg="green")

def PlotAirlinesButton():
    if len(list_airports) == 0:
        label_result.config(text="Load airports first")
        return
    figura=ar.PlotAirlines(aircrafts)
    incrustar_grafic(figura)
    label_result.config(text="Gràfic de vols per aerolínia ensenyat", fg="green")

def PlotFlightsTypeButton():
    if len(list_airports) == 0:
        label_result.config(text="Load airports first")
        return
    figura=ar.PlotFlightsType(aircrafts)
    incrustar_grafic(figura)
    label_result.config(text="Gràfic arrivades des de Schengen ensenyat",fg="green")

def boto_mapa2():
    ar.MapFlights(aircrafts, list_airports)
    label_result.config(text="Trajectòries a Barcelona a Google Earth ensenyades",fg="green")

def ShowLongDistanceButton():
    global aircrafts
    global list_airports
    if len(list_airports) == 0:
        label_result.config(text="Load airports first")
        return

    aircrafts = ar.LongDistanceArrivals(aircrafts,list_airports)
    actualitzar_pantalla2()
    label_result.config(text="Long distance flights shown: " +
                             str(len(aircrafts)))

def incrustar_grafic(figura):
    # 1. Netegem el frame per si ja hi havia un gràfic abans
    for widget in frame_grafic.winfo_children():
        widget.destroy()

    # 2. Creem el "Canvas" (el llenç) de Matplotlib per a Tkinter
    canvas = FigureCanvasTkAgg(figura, master=frame_grafic)
    canvas.draw()

    # 3. Col·loquem el gràfic dins del frame
    canvas.get_tk_widget().pack(fill="both", expand=True)

def boto_assignar_gate():
    global bcn
    global aircrafts
    if bcn==None:
        label_result.config(text="Primer carrega LEBL", fg="red")
        return
    if not aircrafts:
        label_result.config(text="No hi ha vols carregats per assignar", fg="red")
        return

    index = llista_aircrafts.curselection()
    if not index:
        label_result.config(text="Selecciona un vol",fg="red")
        return
    posicio = index[0]
    avio = aircrafts[posicio]
    resultat=lbl.AssignGate(bcn,avio)
    if resultat == -1:
        label_result.config(text="No hi ha gates disponibles",fg="red")
    else:
        label_result.config(text="Gate assignada a " + avio.id, fg="green")
        ocupacio=lbl.GateOccupancy(bcn)
        for widget in frame_grafic.winfo_children():
            widget.destroy()

        canvas = tk.Canvas(frame_grafic, width=800, height=500, bg="white")
        canvas.pack(fill="both", expand=True)

        lbl.DibuixarGraficSenzill(ocupacio, canvas)

def boto_mostrar_gates():
    global bcn
    if bcn == None:
        label_result.config(text="Primer carrega LEBL",fg="red")
        return

    for widget in frame_grafic.winfo_children():
        widget.destroy()

    tk.Label(frame_grafic,text="Visualització Gates",font=("Arial",10,"bold")).pack()
    container = tk.Frame(frame_grafic)
    container.pack(fill="both", expand=True)

    #scroll bar
    scroll_x = tk.Scrollbar(container, orient="horizontal")
    scroll_x.pack(side="bottom", fill="x")

    scroll_y = tk.Scrollbar(container, orient="vertical")
    scroll_y.pack(side="right", fill="y")

    canvas = tk.Canvas(container,width=800,height=500,bg="white",xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

    canvas.pack(side="left", fill="both", expand=True)

    # connectar scrollbars
    scroll_x.config(command=canvas.xview)
    scroll_y.config(command=canvas.yview)

    lbl.DibuixarPlanoTerminal(bcn,canvas)
    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    label_result.config(text="Mostrant terminals i gates", fg="green")

def boto_ocupacio_gates():
    global bcn
    if bcn == None:
        label_result.config(text="Primer carrega LEBL",fg="red")
        return

    ocupacio = lbl.GateOccupancy(bcn)

    for widget in frame_grafic.winfo_children():
        widget.destroy()

    tk.Label(frame_grafic,text="Ocupació Gates",font=("Arial",10,"bold")).pack()
    container = tk.Frame(frame_grafic)
    container.pack(fill="both", expand=True)

    # scroll bar
    scroll_x = tk.Scrollbar(container, orient="horizontal")
    scroll_x.pack(side="bottom", fill="x")

    canvas = tk.Canvas(container, width=800, height=500, bg="white", xscrollcommand=scroll_x.set)
    canvas.pack(side="left", fill="both", expand=True)

    scroll_x.config(command=canvas.xview)

    lbl.DibuixarGraficSenzill(ocupacio, canvas)
    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    label_result.config(text="Ocupació mostrada",fg="green")


finestra = tk.Tk()
finestra.title("Interfaç")
finestra.geometry("1200x800")

frame_principal = tk.Frame(finestra)
frame_principal.pack(side="top",fill="both", padx=20,pady=20)

#missatges feedback

status_bar = tk.Frame(frame_principal, height=30, bg="#eaecee")
status_bar.pack(side="bottom", fill="x")
status_bar.pack_propagate(False)

label_result = tk.LabelFrame(status_bar,text="Status",font=("Arial", 10, "bold"),fg="black")
label_result.pack(fill="both", expand=True)

frame_esquerra = tk.Frame(frame_principal, bg="#f4f6f7")
frame_esquerra.pack(side="left", fill="both", expand=False, padx=5)


contenedor_centrat = tk.Frame(frame_esquerra)
contenedor_centrat.pack(anchor="center")

left_container = tk.Frame(frame_esquerra)
left_container.pack(fill="both", expand=True)

#

#PART AIRPORT

#primer rectangle
frame_airports = tk.LabelFrame(left_container, text="Airports")
frame_airports.pack(fill="both", expand=False, pady=5)
llista_airports = tk.Listbox(frame_airports, width=40, height=10,bg="white", selectbackground="#3498db",font=("Consolas", 10))
llista_airports.pack(fill="both", expand=False)


bloc1 = tk.LabelFrame(contenedor_centrat, text="Airports Management")
bloc1.pack(fill="x", padx=10, pady=5)

tk.Button(bloc1, text="Carregar fitxer aeroports", width=25, command=boto_carregar).grid(row=0, column=0,padx=3,pady=3,sticky="ew")
tk.Button(bloc1, text="Afegir aeroport", width=25,command=boto_afegir).grid(row=1, column=0,padx=3,pady=3,sticky="ew")
tk.Button(bloc1, text="Eliminar aeroport",width=25, command=boto_eliminar).grid(row=2, column=0,padx=3,pady=3,sticky="ew")

tk.Button(bloc1, text="Validar schengen",width=25, command=boto_schengen).grid(row=0, column=1,padx=3,pady=3,sticky="ew")
tk.Button(bloc1, text="Schengen/No Schengen", width=25,command=boto_grafic).grid(row=1, column=1,padx=3,pady=3,sticky="ew")
tk.Button(bloc1, text="Aeroports en Google Earth", width=25,command=boto_mapa).grid(row=2, column=1,padx=3,pady=3,sticky="ew")

#PART AIRCRAFT

#segon rectangle
frame_aircrafts = tk.LabelFrame(left_container, text="Flights")
frame_aircrafts.pack(fill="both", expand=True, pady=5)
llista_aircrafts = tk.Listbox(frame_aircrafts, width=40, height=15,bg="white", selectbackground="#e74c3c",font=("Consolas", 10))
llista_aircrafts.pack(fill="both", expand=True)


bloc2 = tk.LabelFrame(contenedor_centrat, text="Aircrafts Management")
bloc2.pack(fill="x", padx=10, pady=5)

tk.Button(bloc2, text="Carregar fitxer vols", width=25,command=boto_carregar_arrivals).grid(row=0, column=0,padx=3,pady=3,sticky="ew")
tk.Button(bloc2,text="Arrivades més llunyanes",width=25,command=ShowLongDistanceButton).grid(row=1, column=0,padx=3,pady=3,sticky="ew")
tk.Button(bloc2,text="Trajectòries a Barcelona",width=25,command=boto_mapa2).grid(row=2, column=0,padx=3,pady=3,sticky="ew")

tk.Button(bloc2,text="Freqüència d'aterratge/dia",width=25,command=PlotArrivalsButton).grid(row=0, column=1,padx=3,pady=3,sticky="ew")
tk.Button(bloc2,text="Nombre de vols per aerolínea", width=25,command=PlotAirlinesButton).grid(row=1, column=1,padx=3,pady=3,sticky="ew")
tk.Button(bloc2,text="Arrivant des de Schengen o no",width=25,command=PlotFlightsTypeButton).grid(row=2, column=1,padx=3,pady=3,sticky="ew")

bloc3 = tk.LabelFrame(contenedor_centrat, text="System")
bloc3.pack(fill="x", padx=10, pady=5)

tk.Button(bloc3,text="Guardar aeroports Schengen",width=25,command=boto_guardar_aeroports).grid(row=0, column=0,padx=3,pady=3,sticky="ew")
tk.Button(bloc3,text="Guardar vols",width=25,command=boto_guardar_vols).grid(row=0, column=1,padx=3,pady=3,sticky="ew")

#PART LEBL

bloc4 = tk.LabelFrame(contenedor_centrat, text="LEBL Gate Management")
bloc4.pack(fill="x", padx=10, pady=5)


tk.Button(bloc4,text="Carregar estructura LEBL",width=25,command=boto_carregar_lebl).grid(row=1,column=0,padx=3,pady=3,sticky="ew")
tk.Button(bloc4,text="Assignar gate al vol seleccionat",width=25,command=boto_assignar_gate).grid(row=1,column=1,padx=3,pady=3,sticky="ew")
tk.Button(bloc4,text="Mostrar terminals i gates",width=25,command=boto_mostrar_gates).grid(row=2,column=0,padx=3,pady=3,sticky="ew")
tk.Button(bloc4,text="Mostrar ocupació gates",width=25,command=boto_ocupacio_gates).grid(row=2,column=1,padx=3,pady=3,sticky="ew")


frame_grafic = tk.Frame(frame_principal, bg="white", width=550)
frame_grafic.pack(side="left", fill="both", expand=True, padx=15)
tk.Label(frame_grafic,text="Dashboard Visual",font=("Arial", 12, "bold"),bg="white").pack()



finestra.mainloop()



