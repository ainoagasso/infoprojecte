import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import airport as ap
import aircraft as ar
import LEBL as lbl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

canvas_terminals=[]
gates_ui = []
selected_gate = None
list_airports = []
aircrafts=[]
bcn=None
departures=[]
simulation_running = False
simulation_paused=False
current_time = 0

#pestanya petita al posicionar-se sobre una gate
class Tooltip:
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None

    def show(self, text, x, y):
        self.hide()
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")

        label = tk.Label(tw,text=text,bg="#ffffe0",fg="black",font=("Segoe UI", 9),justify="left",relief="solid",borderwidth=1)
        label.pack()

    def hide(self):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None


def actualitzar_pantalla():
    llista = [llista_airports, llista_airports2, llista_airports3]
    i = 0
    while i < len(llista):
        llista[i].delete(0, tk.END)

        k = 0
        while k < len(list_airports):
            airport = list_airports[k]
            estat = "Schengen" if airport.schengen else "non-Schengen"
            text = (f"{airport.ICAO} - "f"{airport.latitude:.4f} - "f"{airport.longitude:.4f} - "f"{estat}")

            llista[i].insert(tk.END, text)
            k = k + 1

        i = i + 1


def actualitzar_pantalla2():
    llista = [llista_aircrafts, llista_aircrafts2, llista_aircrafts3]
    i = 0
    while i < len(llista):
        llista[i].delete(0, tk.END)

        k = 0
        while k < len(aircrafts):
            aircraft = aircrafts[k]

            text = aircraft.id + " - " + aircraft.company + " - " + aircraft.airport + " - " + aircraft.time

            llista[i].insert(tk.END, text)
            k = k + 1

        i = i +1

def actualitzar_status(text, color, tab=None):
    if tab is None:
        labels = [status_label, status_label2, status_label3]
    else:
        labels = [tab]

    for lbl in labels:
        lbl.config(text=text, fg=color)

def actualitzar_pantalla3():
    llista=[llista_departures,llista_departures2,llista_departures3]

    i = 0
    while i < len(llista):
        llista[i].delete(0,tk.END)
        k=0
        while k < len(departures):
            d = departures[k]

            text = d.id + " - " + d.company + " - " + d.destination + " - " + d.departure_time
            llista[i].insert(tk.END, text)
            k=k+1
        i += 1


def boto_carregar():
    global list_airports
    ruta = filedialog.askopenfilename()
    if ruta:
        noves = ap.LoadAirports(ruta)
        list_airports.clear()
        list_airports.extend(noves)
        actualitzar_pantalla()
        actualitzar_status("Airports loaded: " + str(len(list_airports)), "green")
    else:
        actualitzar_status("Please enter a filename to load", "red")

def boto_carregar_arrivals():
    global aircrafts
    ruta = filedialog.askopenfilename()
    if ruta:
        aircrafts = ar.LoadArrivals(ruta)
        actualitzar_pantalla2()
        actualitzar_status("Flights loaded: " + str(len(aircrafts)), "green")
    else:
        actualitzar_status("Please enter a filename to load", "red")


def boto_carregar_lebl():
    global bcn
    ruta = filedialog.askopenfilename()
    try:
        bcn = lbl.LoadAirportStructure(ruta)
        if bcn != -1:
            actualitzar_status("Estructura LEBL carregada correctament", "green")
            return
        else:
            actualitzar_status("Error en carregar l'estructura LEBL", "red")
    except Exception as e:
        actualitzar_status("Error: " + str(e), "red")

def boto_carregar_departures():
    global departures
    ruta = filedialog.askopenfilename()
    if ruta:
        departures = ar.LoadDepartures(ruta)
        actualitzar_pantalla3()
        actualitzar_status(
            f"Departures loaded: {len(departures)}",
            "green"
        )
    else:

        actualitzar_status(
            "Error loading departures",
            "red"
        )

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
            actualitzar_status("Aeroport afegit", "green")
        except ValueError:
            actualitzar_status("Error: Lat/Lon han de ser números", "red")
        except Exception as e:
            actualitzar_status("Error al guardar l'aeroport", "red")

    tk.Button(f_nova, text="Guardar", command=guardar_nou).pack(pady=5)

def boto_guardar_aeroports():
    global list_airports
    fitxer_desti = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Fitxers de text", "*.txt"), ("Tots els fitxers", "*.*")],
        title="Guardar llista d'aeroports schengen")

    if fitxer_desti:
        resultat = ap.SaveSchengenAirports(list_airports, fitxer_desti)

        if resultat == 0:
            actualitzar_status("Aeroports schengen guardats amb èxit", "green")
        else:
            actualitzar_status("No s'ha pogut guardar el fitxer", "red")


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
            actualitzar_status("Vols guardats amb èxit", "green")
        else:
            actualitzar_status("No s'ha pogut guardar el fitxer", "red")


def boto_eliminar():
    # Mirem quin element ha marcat l'usuari amb el ratolí
    index = llista_airports.curselection()
    if index:
        posicio = index[0]
        codi = list_airports[posicio].ICAO
        ap.RemoveAirport(list_airports, codi)
        actualitzar_pantalla()
        actualitzar_status("Aeroport eliminat", "green")
    else:
        actualitzar_status("Selecciona un aeroport", "red")

def boto_schengen():
    i = 0
    while i < len(list_airports):
        ap.SetSchengen(list_airports[i])
        i = i + 1
    actualitzar_pantalla()
    actualitzar_status("Schengen updated", "green")

def boto_grafic():
    figura=ap.PlotAirports(list_airports)
    incrustar_grafic(figura)
    actualitzar_status("Gràfic Schengen/No Schengen ensenyat", "green")

def boto_mapa():
    ap.MapAirports(list_airports)
    actualitzar_status("Aeroports en Google Earth ensenyats", "green")

def PlotArrivalsButton():
    if len(list_airports) == 0:
        actualitzar_status("Carrega aeroports primer", "red")
        return
    figura=ar.PlotArrivals(aircrafts)
    incrustar_grafic(figura)
    actualitzar_status("Gràfic d'aterratges durant el dia ensenyat", "green")

def PlotAirlinesButton():
    if len(list_airports) == 0:
        actualitzar_status("Carrega aeroports primer", "red")
        return
    figura=ar.PlotAirlines(aircrafts)
    incrustar_grafic(figura)
    actualitzar_status("Gràfic de vols per aerolínia ensenyat", "green")

def PlotFlightsTypeButton():
    if len(list_airports) == 0:
        actualitzar_status("Load airports first", "red")
        return
    figura=ar.PlotFlightsType(aircrafts)
    incrustar_grafic(figura)
    actualitzar_status("Gràfic arrivades des de Schengen ensenyat", "green")

def boto_mapa2():
    ar.MapFlights(aircrafts, list_airports)
    actualitzar_status("Trajectòries a Barcelona a Google Earth ensenyades", "green")

def ShowLongDistanceButton():
    global aircrafts
    global list_airports
    if len(list_airports) == 0:
        actualitzar_status("Load airports first", "red")
        return

    aircrafts = ar.LongDistanceArrivals(aircrafts,list_airports)
    actualitzar_pantalla2()
    actualitzar_status("Long distance flights shown: " + str(len(aircrafts)), "green")

def incrustar_grafic(figura):
    frames = [frame_grafic, frame_grafic2, visual_panel]
    i = 0
    while i < len(frames):
        frame = frames[i]
        # 1. Netegem el frame per si ja hi havia un gràfic abans
        for widget in frame.winfo_children():
            widget.destroy()

        # 2. Creem el "Canvas" (el llenç) de Matplotlib per a Tkinter
        canvas = FigureCanvasTkAgg(figura, master=frame)
        canvas.draw()

        # 3. Col·loquem el gràfic dins del frame
        canvas.get_tk_widget().pack(fill="both", expand=True)
        i = i + 1


def boto_assignar_gate(): #jo la treuria
    global bcn
    global aircrafts
    if bcn==None:
        actualitzar_status("Primer carrega LEBL", "red")
        return
    if not aircrafts:
        actualitzar_status("No hi ha vols carregats per assignar", "red")
        return

    index = llista_aircrafts3.curselection()
    if not index:
        actualitzar_status("Selecciona un vol","red")
        return
    posicio = index[0]
    avio = aircrafts[posicio]
    resultat=lbl.AssignGate(bcn,avio)
    if resultat == -1:
        actualitzar_status("No hi ha gates disponibles", "red")
    else:
        actualitzar_status("Gate assignada a " + avio.id, "green")
        ocupacio=lbl.GateOccupancy(bcn)
        for widget in visual_panel.winfo_children():
            widget.destroy()

        canvas = tk.Canvas(frame_grafic3, width=800, height=500, bg="white")
        canvas.pack(fill="both", expand=True)


def boto_mostrar_gates():
    if bcn is None:
        actualitzar_status("Primer carrega LEBL", "red")
        return

    canvas_terminals.clear()

    frames = [frame_grafic, frame_grafic2, visual_panel]
    gates_ui.clear()

    for frame in frames:

        for widget in frame.winfo_children():
            widget.destroy()

        container = tk.Frame(frame)
        container.pack(fill="both", expand=True)

        v_scroll = tk.Scrollbar(container, orient="vertical")
        v_scroll.pack(side="right", fill="y")

        h_scroll = tk.Scrollbar(container, orient="horizontal")
        h_scroll.pack(side="bottom", fill="x")

        canvas = tk.Canvas(
            container,
            bg="white",
            xscrollcommand=h_scroll.set,
            yscrollcommand=v_scroll.set
        )

        canvas.pack(side="left", fill="both", expand=True)

        v_scroll.config(command=canvas.yview)
        h_scroll.config(command=canvas.xview)

        lbl.DibuixarPlanoTerminal(bcn, canvas, gates_ui)

        canvas.bind("<Button-1>", detectar_click_gate)
        canvas.bind("<Button-3>", detectar_click_gate)
        canvas.bind("<Motion>", detectar_hover_gate)
        canvas.bind("<Leave>", lambda e: tooltip.hide())

        canvas_terminals.append(canvas)

    actualitzar_status("Mostrant terminals i gates", "green")

def boto_assignar_tots():
    global bcn
    global aircrafts

    if bcn is None:
        actualitzar_status("Primer carrega LEBL", "red")
        return

    if len(aircrafts) == 0:
        actualitzar_status("No hi ha vols carregats", "red")
        return

    assignats = 0
    no_assignats = 0

    i = 0
    while i < len(aircrafts):

        avio = aircrafts[i]
        resultat = lbl.AssignGate(bcn, avio)

        if resultat == -1:
            no_assignats += 1
        else:
            assignats += 1

        i += 1

    actualitzar_status(f"Assignats: {assignats} | Sense gate: {no_assignats}", "green")

def boto_assignacio_intelligent():
    global bcn, aircrafts, canvas_terminal

    if bcn is None:
        actualitzar_status("Carrega LEBL primer", "red")
        return

    assignats, no_assignats = lbl.IntelligentAssign(bcn, aircrafts)

    actualitzar_status(
        f"Smart assignació → OK: {assignats} | Fail: {no_assignats}",
        "green")
    refrescar_canvas()


#les que venen a continuació son per assignar manualment
def detectar_click_gate(event):
    canvas=event.widget
    x=canvas.canvasx(event.x)
    y=canvas.canvasy(event.y)

    for (x1, y1, x2, y2, gate, rect) in gates_ui:
        if x1 <= x <= x2 and y1 <= y <= y2:

            #clic dret = menú
            if event.num == 3:
                obrir_menu_gate(event, gate)
            return

def obrir_menu_gate(event, gate):
    menu = tk.Menu(finestra, tearoff=0)

    if gate.occupancy:
        menu.add_command(
            label="Desocupar gate",
            command=lambda: desocupar_gate(gate)
        )
    else:
        menu.add_command(
            label="Assignar vol seleccionat",
            command=lambda: AssignGateManual(gate)
        )

    menu.post(event.x_root, event.y_root)

def desocupar_gate(gate):
    gate.occupancy = False
    gate.aircraft_id = ""
    gate.aircraft=None

    actualitzar_status(f"Gate {gate.name} buidada", "orange")

    refrescar_canvas()

def AssignGateManual(gate):
    global aircrafts
    idx = llista_aircrafts.curselection() or llista_aircrafts2.curselection() or llista_aircrafts3.curselection()

    if not idx:
        actualitzar_status("Selecciona un vol primer", "red")
        return

    avio = aircrafts[idx[0]]

    # validació Schengen si existeix
    if hasattr(gate, "type"):
        if gate.type == "Schengen" and not getattr(avio, "Schengen", True):
            actualitzar_status("No compatible Schengen", "red")
            return
        if gate.type == "non-Schengen" and getattr(avio, "Schengen", True):
            actualitzar_status("No compatible Schengen", "red")
            return

    if gate.occupancy:
        actualitzar_status("La gate ja està ocupada", "red")
        return
    gate.occupancy = True
    gate.aircraft_id = avio.id
    gate.aircraft = avio

    refrescar_canvas()

def refrescar_canvas():
    global canvas_terminals

    gates_ui.clear()

    for canvas in canvas_terminals:
        gates_ui.clear()
        canvas.delete("all")

        lbl.DibuixarPlanoTerminal(bcn,canvas,gates_ui)
        canvas.config(scrollregion=canvas.bbox("all"))


#per canviar gate de color si passem el cursor per sobre
def detectar_hover_gate(event):
    global hovered_gate
    canvas=event.widget

    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    found = None

    for (x1, y1, x2, y2, gate, rect_id) in gates_ui:
        if x1 <= x <= x2 and y1 <= y <= y2:
            found = (gate, rect_id)
            break

    # si canviem de gate
    if found != hovered_gate:

        # restaurar anterior
        if hovered_gate:
            gate_old, rect_old = hovered_gate
            color = "#e74c3c" if gate_old.occupancy else "#2ecc71"
            canvas.itemconfig(rect_old, fill=color)

        hovered_gate = found

        if found:
            gate, rect_id = found

            # highlight
            canvas.itemconfig(rect_id, fill="#f1c40f")

            # tooltip text
            if gate.occupancy and gate.aircraft:
                avio = gate.aircraft

                text = (
                    f"Gate: {gate.name}\n"
                    f"Status: Ocupada\n\n"
                    f"Flight ID: {avio.id}\n"
                    f"Companyia: {avio.company}\n"
                    f"Origen: {avio.airport}\n"
                    f"Hora: {avio.time}"
                )

            else:

                text = (
                    f"Gate: {gate.name}\n"
                    f"Status: Lliure"
                )

            tooltip.show(text, event.x_root + 10, event.y_root + 10)
        else:
            tooltip.hide()

def boto_plot_ocupacio():

    global bcn
    global aircrafts

    if bcn is None:
        actualitzar_status("Carrega LEBL primer", "red")
        return

    figura = lbl.PlotDayOccupancy(bcn, aircrafts)

    incrustar_grafic(figura)

    actualitzar_status(
        "Ocupació diària de terminals calculada",
        "green")

def boto_mostrar_hora():

    global bcn
    global aircrafts

    hora = entry_hora.get()

    lbl.ResetGates(bcn)
    lbl.AssignNightGates(bcn, aircrafts)

    lbl.AssignGatesAtTime(
        bcn,
        aircrafts,
        hora
    )

    refrescar_canvas()

    actualitzar_status(
        f"Ocupació mostrada per les {hora}",
        "green"
    )

def boto_merge():

    global aircrafts
    global departures

    aircrafts = ar.MergeMovements(aircrafts,departures)

    actualitzar_pantalla2()

    actualitzar_status(
        f"Movements merged: {len(aircrafts)}",
        "green")

def boto_night():

    global bcn
    global aircrafts

    resultat = lbl.AssignNightGates(bcn,aircrafts)

    if resultat == -1:

        actualitzar_status(
            "No night aircraft",
            "red")

    else:

        actualitzar_status(
            "Night gates assigned",
            "green")

        refrescar_canvas()

def boto_play_simulation():
    global simulation_running, simulation_paused, current_time

    if bcn is None:
        actualitzar_status("Carrega LEBL primer", "red")
        return

    simulation_running = True
    simulation_paused = False
    current_time = 0

    simulate_step()

def boto_pause_resume():
    global simulation_paused

    if not simulation_running:
        actualitzar_status("Simulació no iniciada", "red")
        return

    simulation_paused = not simulation_paused

    if simulation_paused:
        actualitzar_status("Simulació en pausa", "orange")
    else:
        actualitzar_status("Simulació reanudada", "green")
        simulate_step()

def simulate_step():
    global current_time, simulation_running, simulation_paused

    if not simulation_running:
        return
    if simulation_paused:
        return

    # 1. si acabem el dia
    if current_time > 24 * 60:
        actualitzar_status("Simulació acabada", "green")
        simulation_running = False
        return

    # 2. hora actual
    hour = current_time // 60
    time_str = f"{hour:02d}:00"

    # 3. assignació dinàmica
    lbl.AssignGatesAtTime(bcn, aircrafts, time_str)

    # 4. refrescar visuals
    refrescar_canvas()

    actualitzar_status(f"Simulant hora: {time_str}", "blue")

    # 5. avançar temps
    current_time += 60

    # 6. repetir automàticament
    finestra.after(400, simulate_step)

def format_massa(kg):
   # Mostrem tones si el nombre és gran; si no, kg
   if kg >= 1000:
       return f"{kg/1000:.2f} t".replace(".", ",")
   return f"{kg:.0f} kg"




def mostrar_emissions(event):
    seleccio = llista_aircrafts.curselection() or llista_aircrafts2.curselection() or llista_aircrafts3.curselection()
    if not seleccio:
        return


    if len(list_airports) == 0:
        label_emissions.config(
            text="Carrega primer la llista d'aeroports per calcular l'impacte.",fg="#b9770e")
        punt_emissions.config(bg="#f4f6f7")
        return


    avio = aircrafts[seleccio[0]]
    dades = ar.FlightEmissions(avio, list_airports)


    if dades is None:
        label_emissions.config(
            text="Origen " + avio.airport + " no trobat a la llista d'aeroports.",
            fg="#b9770e")
        punt_emissions.config(bg="#f4f6f7")
        return


    dist = dades["distancia"]
    fuel = dades["combustible"]
    co2 = dades["co2"]


    km_cotxe = co2 / 0.12
    arbres = co2 / 21.0
   # Semàfor segons el CO2 total del vol
    if co2 < 15000:
        color = "#27ae60"   # verd  (vol curt)
    elif co2 < 35000:
        color = "#e67e22"   # ambre (vol mitjà)
    else:
        color = "#c0392b"   # vermell (vol llarg / molt contaminant)
    punt_emissions.config(bg=color)


    text = (
        "Vol " + avio.id + "  (" + avio.airport + " -> LEBL)\n"
        + "Distància:    " + f"{dist:,.0f} km".replace(",", ".") + "\n"
        + "Combustible:  " + format_massa(fuel) + "\n"
        + "CO2 emès:     " + format_massa(co2) + "\n"
        + "≈ " + f"{km_cotxe:,.0f}".replace(",", ".") + " km amb cotxe  ·  "
        + f"{arbres:,.0f}".replace(",", ".") + " arbres/any")
    label_emissions.config(text=text, fg="#1a5276")


finestra = tk.Tk()
finestra.title("Sistema de l'aeroport")
finestra.state("zoomed")


# =====================================================================
#  TEMA VISUAL  (nomes estetica - NO canvia cap funcionalitat)
#  Paleta "blau aviacio + blanc". Tota la logica queda exactament igual.
# =====================================================================
C_CHROME = "#e9eff5"         # fons de tots els panells
C_PRIMARY = "#1f6aa5"        # blau dels botons
C_PRIMARY_HOVER = "#2980b9"  # blau en passar el ratoli per sobre
C_PRIMARY_DARK = "#15466b"   # blau fosc (titols)
C_HEAD = "#15466b"           # titols dels LabelFrame
C_BORDER = "#c2d2e3"
FONT_HEAD = ("Segoe UI", 10, "bold")
FONT_BTN = ("Segoe UI", 9, "bold")

finestra.configure(bg=C_CHROME)

# Valors per defecte: tambe afecten finestres creades despres (ex: "Nou Aeroport")
finestra.option_add("*Button.background", C_PRIMARY)
finestra.option_add("*Button.foreground", "white")
finestra.option_add("*Button.activeBackground", C_PRIMARY_HOVER)
finestra.option_add("*Button.activeForeground", "white")
finestra.option_add("*Button.relief", "flat")
finestra.option_add("*Button.borderWidth", 0)
finestra.option_add("*Button.font", "{Segoe UI} 9 bold")
finestra.option_add("*Button.cursor", "hand2")
finestra.option_add("*Entry.relief", "flat")
finestra.option_add("*Entry.background", "white")
finestra.option_add("*Toplevel.background", C_CHROME)

# Estil de les pestanyes (ttk Notebook)
_style_tema = ttk.Style()
try:
    _style_tema.theme_use("clam")
except Exception:
    pass
_style_tema.configure("TNotebook", background=C_CHROME, borderwidth=0)
_style_tema.configure("TNotebook.Tab", background="#d6e2ef",
                      foreground=C_PRIMARY_DARK, padding=(26, 10),
                      font=("Segoe UI", 11, "bold"), borderwidth=0)
_style_tema.map("TNotebook.Tab",
                background=[("selected", C_PRIMARY)],
                foreground=[("selected", "white")])


def _aplicar_tema(w):
    # Recorre tots els ginys i NOMES en canvia l'aparenca (mai el comportament)
    cls = w.winfo_class()
    try:
        if cls == "Button":
            w.configure(bg=C_PRIMARY, fg="white", activebackground=C_PRIMARY_HOVER,
                        activeforeground="white", relief="flat", bd=0,
                        font=FONT_BTN, cursor="hand2", highlightthickness=0)
            w.bind("<Enter>", lambda e: e.widget.configure(bg=C_PRIMARY_HOVER))
            w.bind("<Leave>", lambda e: e.widget.configure(bg=C_PRIMARY))
        elif cls == "Labelframe":
            cur_fg = str(w.cget("foreground"))
            if cur_fg in ("", "black", "#000000", "SystemButtonText", "SystemWindowText"):
                w.configure(fg=C_HEAD)
            w.configure(bg=C_CHROME, font=FONT_HEAD)
        elif cls == "Frame":
            if str(w.cget("bg")) == "#ecf0f1":   # els dashboards -> blancs
                w.configure(bg="white")
            else:
                w.configure(bg=C_CHROME)
        elif cls == "Label":
            if str(w.cget("bg")) == "#ecf0f1":
                w.configure(bg="white")
            else:
                w.configure(bg=C_CHROME)
        elif cls == "Listbox":
            w.configure(bg="white", relief="flat", bd=0, highlightthickness=1,
                        highlightbackground=C_BORDER, highlightcolor=C_BORDER)
        elif cls == "Entry":
            w.configure(relief="flat", bg="white", highlightthickness=1,
                        highlightbackground=C_BORDER)
    except tk.TclError:
        pass
    for fill in w.winfo_children():
        _aplicar_tema(fill)
# (la crida a _aplicar_tema es fa al final, just abans de mainloop)

tooltip = Tooltip(finestra)
hovered_gate=None

style=ttk.Style()
style.configure("TNotebook.Tab",padding=(30, 10),   # (ancho, alto)
    font=("Arial", 12, "bold"))

notebook = ttk.Notebook(finestra)
notebook.pack(fill="both", expand=True)

tab_airports=tk.Frame(notebook)
tab_aircrafts=tk.Frame(notebook)
tab_lebl=tk.Frame(notebook)

notebook.add(tab_airports, text="Airport")
notebook.add(tab_aircrafts, text="Flights")
notebook.add(tab_lebl, text="LEBL")



#DEFINIR VARIABLES I POSAR NOM ALS DIFERENTS APARTATS
#Part airport
status_bar = tk.LabelFrame(tab_airports,text="Status",font=("Arial",11,"bold"))
status_bar.pack(side="bottom",fill="x",expand=False,ipady=10)

status_label=tk.Label(status_bar, text="",anchor="w",justify="left",font=("Consolas",12),fg="black")
status_label.pack(fill="both",expand=True,padx=10,pady=5)


frame_esquerra = tk.Frame(tab_airports, bg="#f4f6f7")
frame_esquerra.pack(side="left", fill="both", expand=False, padx=5)

contenedor_centrat = tk.Frame(frame_esquerra)
contenedor_centrat.pack(anchor="center")

left_container = tk.Frame(frame_esquerra)
left_container.pack(fill="both", expand=True)


frame_airports = tk.LabelFrame(left_container, text="Airports")
frame_airports.pack(fill="both", expand=False, pady=5)
frame_aircrafts = tk.LabelFrame(left_container, text="Arrivals")
frame_aircrafts.pack(fill="both", expand=False, pady=5)
frame_departures = tk.LabelFrame(left_container, text="Departures")
frame_departures.pack(fill="both", expand=False, pady=5)


#Parts aircraft
status_bar2 = tk.LabelFrame(tab_aircrafts,text="Status",font=("Arial",11,"bold"))
status_bar2.pack(side="bottom", fill="x",expand=False,ipady=10)

status_label2=tk.Label(status_bar2, text="",anchor="w",justify="left",font=("Consolas",12),fg="black")
status_label2.pack(fill="both",expand=True,padx=10,pady=5)


frame_esquerra2 = tk.Frame(tab_aircrafts, bg="#f4f6f7")
frame_esquerra2.pack(side="left", fill="both", expand=False, padx=5)


contenedor_centrat2 = tk.Frame(frame_esquerra2)
contenedor_centrat2.pack(anchor="center")


left_container2 = tk.Frame(frame_esquerra2)
left_container2.pack(fill="both", expand=True)


frame_airports2 = tk.LabelFrame(left_container2, text="Airports")
frame_airports2.pack(fill="both", expand=False, pady=5)
frame_aircrafts2 = tk.LabelFrame(left_container2, text="Flights")
frame_aircrafts2.pack(fill="both", expand=False, pady=5)
frame_departures2 = tk.LabelFrame(left_container2, text="Departures")
frame_departures2.pack(fill="both", expand=False, pady=5)


#Part Lebl
status_bar3 = tk.LabelFrame(tab_lebl,text="Status",font=("Arial",11,"bold"))
status_bar3.pack(side="bottom", fill="x",expand=False,ipady=10)

status_label3=tk.Label(status_bar3, text="",anchor="w",justify="left",font=("Consolas",12),fg="black")
status_label3.pack(fill="both",expand=True,padx=10,pady=5)



frame_esquerra3 = tk.Frame(tab_lebl, bg="#f4f6f7")
frame_esquerra3.pack(side="left", fill="both", expand=False, padx=5)


contenedor_centrat3 = tk.Frame(frame_esquerra3)
contenedor_centrat3.pack(anchor="center")


left_container3 = tk.Frame(frame_esquerra3)
left_container3.pack(fill="both", expand=True)


frame_airports3 = tk.LabelFrame(left_container3, text="Airports")
frame_airports3.pack(fill="both", expand=False, pady=5)
frame_aircrafts3 = tk.LabelFrame(left_container3, text="Flights")
frame_aircrafts3.pack(fill="both", expand=False, pady=5)
frame_departures3 = tk.LabelFrame(left_container3, text="Departures")
frame_departures3.pack(fill="both", expand=False, pady=5)


#Part comú
llista_airports = tk.Listbox(frame_airports, width=40, height=10,bg="white", selectbackground="#3498db",font=("Consolas", 10))
llista_airports.pack(fill="both", expand=False)
llista_aircrafts = tk.Listbox(frame_aircrafts, width=40, height=10,bg="white", selectbackground="#e74c3c",font=("Consolas", 10))
llista_aircrafts.pack(fill="both", expand=False)
llista_departures = tk.Listbox(frame_departures,width=40,height=10,bg="white",selectbackground="#9b59b6",font=("Consolas", 10))
llista_departures.pack(fill="both", expand=False)

llista_airports2 = tk.Listbox(frame_airports2, width=40, height=10,bg="white", selectbackground="#3498db",font=("Consolas", 10))
llista_airports2.pack(fill="both", expand=False)
llista_aircrafts2 = tk.Listbox(frame_aircrafts2, width=40, height=10,bg="white", selectbackground="#e74c3c",font=("Consolas", 10))
llista_aircrafts2.pack(fill="both", expand=False)
llista_departures2 = tk.Listbox(frame_departures2,width=40,height=10,bg="white",selectbackground="#9b59b6",font=("Consolas", 10))
llista_departures2.pack(fill="both", expand=False)


llista_airports3 = tk.Listbox(frame_airports3, width=40, height=10,bg="white", selectbackground="#3498db",font=("Consolas", 10))
llista_airports3.pack(fill="both", expand=False)
llista_aircrafts3 = tk.Listbox(frame_aircrafts3, width=40, height=10,bg="white", selectbackground="#e74c3c",font=("Consolas", 10))
llista_aircrafts3.pack(fill="both", expand=False)
llista_departures3 = tk.Listbox(frame_departures3,width=40,height=10,bg="white",selectbackground="#9b59b6",font=("Consolas", 10))
llista_departures3.pack(fill="both", expand=False)


#CO2
frame_emissions = tk.LabelFrame(left_container, text="Petjada ecològica del vol",fg="#1e8449", font=("Arial", 9, "bold"))
frame_emissions.pack(fill="x", expand=False, pady=5)

fila_emis = tk.Frame(frame_emissions)
fila_emis.pack(fill="x", padx=5, pady=3)

# Petit indicador de color (semàfor d'emissions)
punt_emissions = tk.Label(fila_emis, text="  ", bg="#f4f6f7", width=2)
punt_emissions.pack(side="left", padx=(0, 8))

label_emissions = tk.Label(fila_emis,text="Selecciona un vol per veure'n el combustible i el CO2.",justify="left", anchor="w", font=("Consolas", 9))
label_emissions.pack(side="left", fill="x")

frame_emissions2 = tk.LabelFrame(left_container2, text="Petjada ecològica del vol",fg="#1e8449", font=("Arial", 9, "bold"))
frame_emissions2.pack(fill="x", expand=False, pady=5)

fila_emis2 = tk.Frame(frame_emissions2)
fila_emis2.pack(fill="x", padx=5, pady=3)

# Petit indicador de color (semàfor d'emissions)
punt_emissions2 = tk.Label(fila_emis2, text="  ", bg="#f4f6f7", width=2)
punt_emissions2.pack(side="left", padx=(0, 8))

label_emissions2 = tk.Label(fila_emis2,text="Selecciona un vol per veure'n el combustible i el CO2.",justify="left", anchor="w", font=("Consolas", 9))
label_emissions2.pack(side="left", fill="x")

frame_emissions3 = tk.LabelFrame(left_container3, text="Petjada ecològica del vol",fg="#1e8449", font=("Arial", 9, "bold"))
frame_emissions3.pack(fill="x", expand=False, pady=5)

fila_emis3 = tk.Frame(frame_emissions3)
fila_emis3.pack(fill="x", padx=5, pady=3)

# Petit indicador de color (semàfor d'emissions)
punt_emissions3 = tk.Label(fila_emis3, text="  ", bg="#f4f6f7", width=2)
punt_emissions3.pack(side="left", padx=(0, 8))

label_emissions3 = tk.Label(fila_emis3,text="Selecciona un vol per veure'n el combustible i el CO2.",justify="left", anchor="w", font=("Consolas", 9))
label_emissions3.pack(side="left", fill="x")

# Quan se selecciona un vol a la llista, mostrem la seva petjada
llista_aircrafts.bind("<<ListboxSelect>>", mostrar_emissions)
llista_aircrafts2.bind("<<ListboxSelect>>", mostrar_emissions)
llista_aircrafts3.bind("<<ListboxSelect>>", mostrar_emissions)
#PART AIRPORTS


bloc1 = tk.LabelFrame(contenedor_centrat, text="Airports Management")
bloc1.pack(fill="x", padx=10, pady=5)




tk.Button(bloc1, text="Carregar fitxer aeroports", width=25, command=boto_carregar).grid(row=0, column=0,padx=3,pady=3,sticky="ew")
tk.Button(bloc1, text="Afegir aeroport", width=25,command=boto_afegir).grid(row=1, column=0,padx=3,pady=3,sticky="ew")
tk.Button(bloc1, text="Eliminar aeroport",width=25, command=boto_eliminar).grid(row=2, column=0,padx=3,pady=3,sticky="ew")




tk.Button(bloc1, text="Validar schengen",width=25, command=boto_schengen).grid(row=0, column=1,padx=3,pady=3,sticky="ew")
tk.Button(bloc1, text="Schengen/No Schengen", width=25,command=boto_grafic).grid(row=1, column=1,padx=3,pady=3,sticky="ew")
tk.Button(bloc1, text="Aeroports en Google Earth", width=25,command=boto_mapa).grid(row=2, column=1,padx=3,pady=3,sticky="ew")


frame_grafic = tk.Frame(tab_airports, bg="#ecf0f1", width=550)
frame_grafic.pack(side="left", fill="both", expand=True, padx=15)
tk.Label(frame_grafic,text="Dashboard Visual",font=("Arial", 12, "bold"),bg="#ecf0f1").pack()


#PART AIRCRAFT


bloc2 = tk.LabelFrame(contenedor_centrat2, text="Aircrafts Management")
bloc2.pack(fill="x", padx=10, pady=5)




tk.Button(bloc2, text="Carregar fitxer vols", width=25,command=boto_carregar_arrivals).grid(row=0, column=0,padx=3,pady=3,sticky="ew")
tk.Button(bloc2,text="Arrivades més llunyanes",width=25,command=ShowLongDistanceButton).grid(row=1, column=0,padx=3,pady=3,sticky="ew")
tk.Button(bloc2,text="Trajectòries a Barcelona",width=25,command=boto_mapa2).grid(row=2, column=0,padx=3,pady=3,sticky="ew")


tk.Button(bloc2,text="Freqüència d'aterratge/dia",width=25,command=PlotArrivalsButton).grid(row=0, column=1,padx=3,pady=3,sticky="ew")
tk.Button(bloc2,text="Nombre de vols per aerolínea", width=25,command=PlotAirlinesButton).grid(row=1, column=1,padx=3,pady=3,sticky="ew")
tk.Button(bloc2,text="Arrivant des de Schengen o no",width=25,command=PlotFlightsTypeButton).grid(row=2, column=1,padx=3,pady=3,sticky="ew")


bloc3 = tk.LabelFrame(contenedor_centrat2, text="System")
bloc3.pack(fill="x", padx=10, pady=5)


tk.Button(bloc3,text="Guardar aeroports Schengen",width=25,command=boto_guardar_aeroports).grid(row=0, column=0,padx=3,pady=3,sticky="ew")
tk.Button(bloc3,text="Guardar vols",width=25,command=boto_guardar_vols).grid(row=0, column=1,padx=3,pady=3,sticky="ew")


frame_grafic2 = tk.Frame(tab_aircrafts, bg="#ecf0f1", width=550)
frame_grafic2.pack(side="left", fill="both", expand=True, padx=15)
tk.Label(frame_grafic2,text="Dashboard Visual",font=("Arial", 12, "bold"),bg="#ecf0f1").pack()


#PART LEBL


bloc4 = tk.LabelFrame(contenedor_centrat3, text="LEBL Gate Management")
bloc4.pack(fill="x", padx=10, pady=5)

bloc5=tk.LabelFrame(contenedor_centrat3, text="Including Departures")
bloc5.pack(fill="x", padx=10, pady=5)


tk.Button(bloc4,text="Carregar estructura LEBL",width=25,command=boto_carregar_lebl).grid(row=0,column=0,padx=3,pady=3,sticky="ew")
tk.Button(bloc4,text="Assignar gate al vol seleccionat",width=25,command=boto_assignar_gate).grid(row=1,column=0,padx=3,pady=3,sticky="ew")
tk.Button(bloc4,text="Mostrar terminals i gates",width=25,command=boto_mostrar_gates).grid(row=0,column=1,padx=3,pady=3,sticky="ew")
tk.Button(bloc4,text="Assignar tots els vols",width=25,command=boto_assignacio_intelligent).grid(row=1,column=1,padx=3,pady=3,sticky="ew")


tk.Button(bloc5,text="Carregar departures",width=25,command=boto_carregar_departures).grid(row=0,column=0,padx=3,pady=3,sticky="ew")
tk.Button(bloc5,text="Plot ocupació dia",width=25,command=boto_plot_ocupacio).grid(row=0,column=1,padx=3,pady=3,sticky="ew")
tk.Button(bloc5,text="Merge Movements",width=25,command=boto_merge).grid(row=1,column=0,padx=3,pady=3,sticky="ew")
tk.Button(bloc5,text="Assignar night aircraft",width=25,command=boto_night).grid(row=1,column=1,padx=3,pady=3,sticky="ew")
tk.Label(bloc5, text="Hora (HH:MM)").grid(row=2,column=0,padx=3,pady=3)
entry_hora = tk.Entry(bloc5,width=10)
entry_hora.grid(row=2,column=1,padx=3,pady=3)
tk.Button(bloc5,text="Mostrar estat a aquesta hora",command=boto_mostrar_hora).grid(row=3,column=0,columnspan=2,padx=3,pady=3,sticky="ew")



frame_grafic3 = tk.Frame(tab_lebl, bg="#ecf0f1", width=550)
frame_grafic3.pack(side="left", fill="both", expand=True, padx=15)
tk.Label(frame_grafic3,text="Dashboard Visual",font=("Arial", 12, "bold"),bg="#ecf0f1").pack()
control_panel=tk.LabelFrame(frame_grafic3, text="Day Simulation")
control_panel.pack(fill="x",padx=10, pady=5)

visual_panel=tk.Frame(frame_grafic3, bg="#ecf0f1")
visual_panel.pack(fill="both", expand=True)
tk.Button(control_panel,text="Play Day Simulation",command=boto_play_simulation).grid(row=0,column=0,padx=3,pady=3,sticky="ew")
tk.Button(control_panel,text="Pause / Resume",command=boto_pause_resume).grid(row=0,column=1,padx=3,pady=3,sticky="ew")


# Apliquem el tema visual a tota la finestra (nomes aparenca, res funcional)
_aplicar_tema(finestra)

finestra.mainloop()






