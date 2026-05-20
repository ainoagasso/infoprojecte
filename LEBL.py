from aircraft import *

class BarcelonaAP:
    def __init__(self, code=""):
        self.code = code
        self.terminals = []

class Terminal:
    def __init__(self, name=""):
        self.name = name
        self.boarding_areas = []
        self.airlines = []

class BoardingArea:
    def __init__(self, name="", type=""):
        self.name = name
        self.type = type
        self.gates = []

class Gate:
    def __init__(self, name=""):
        self.name = name
        self.occupancy = False
        self.aircraft_id = ""



def SetGates(area, init_gate, end_gate, prefix):

    if end_gate <= init_gate:
        return -1

    area.gates = []
    i=init_gate
    while i <= end_gate:

        gate_name = prefix + str(i)
        gate = Gate(gate_name)
        area.gates.append(gate)

        i = i + 1

    return 0

def LoadAirlines(terminal, t_name):
    filename = t_name + "_Airlines.txt"
    try:
        Fin = open(filename, "r")
    except FileNotFoundError:
        print("No s'ha trobat el fitxer", filename)
        return -1

    terminal.airlines = []
    line = Fin.readline()
    while line != "":
        line = line.strip()
        if line != "":
            parts = line.split()
            codi_ICAO = parts[-1]
            terminal.airlines.append(codi_ICAO)
        line = Fin.readline()
    Fin.close()
    return 0

def LoadAirportStructure(filename):
    try:
        Fin = open(filename, "r")
    except FileNotFoundError:
        print("No s'ha trobat el fitxer", filename)
        return -1

    first_line = Fin.readline()
    parts = first_line.split()
    airport_code = parts[0]
    bcn = BarcelonaAP(airport_code)

    line = Fin.readline()

    while line != "":
        parts = line.split()
        if parts[0] == "Terminal":
            terminal_name = parts[1]
            n_areas = int(parts[2])
            terminal = Terminal(terminal_name)
            LoadAirlines(terminal, terminal_name)
            i = 0
            while i < n_areas:
                line = Fin.readline()
                parts = line.split()
                area_name = parts[1]
                area_type = parts[2]
                init_gate = int(parts[4])
                end_gate = int(parts[6])
                area = BoardingArea(area_name, area_type)
                prefix = terminal_name + area_name
                SetGates(area, init_gate, end_gate, prefix)
                exists = False
                for a in terminal.boarding_areas:
                    if a.name == area.name:
                        exists = True
                if not exists:
                    terminal.boarding_areas.append(area)

                i = i + 1
            bcn.terminals.append(terminal)

        line = Fin.readline()

    Fin.close()
    return bcn

def GateOccupancy(bcn):
    llista_estat = []
    t = 0
    while t < len(bcn.terminals):
        terminal_actual = bcn.terminals[t]
        a = 0
        while a < len(terminal_actual.boarding_areas):
            area_actual = terminal_actual.boarding_areas[a]
            g = 0
            while g < len(area_actual.gates):
                porta = area_actual.gates[g]
                estat = "free"
                id_avio = ""
                if porta.occupancy == True:
                    estat = "occupied"
                    id_avio = porta.aircraft_id

                # Creem un diccionari o llista amb la info de la porta
                info_porta = {
                    "name": porta.name,
                    "status": estat,
                    "aircraft_id": id_avio
                }

                llista_estat.append(info_porta)
                g = g + 1
            a = a + 1
        t = t + 1

    return llista_estat


def IsAirlineInTerminal(terminal, name):
    if name == "":
        return "Error nom buit"
    if len(terminal.airlines) == 0:
        return False
    i = 0
    while i < len(terminal.airlines):
        if terminal.airlines[i] == name:
            return True
        i = i + 1
    return False


def SearchTerminal(bcn, name):
    t = 0
    while t < len(bcn.terminals):
        terminal_ara = bcn.terminals[t]
        resultat = IsAirlineInTerminal(terminal_ara, name)
        if resultat == True:
            return terminal_ara.name

        t = t + 1
    return ""


def AssignGate (bcn,aircraft):
    T=SearchTerminal(bcn,aircraft.company)
    if T=="":
        return -1

    terminal_obj = None
    i = 0
    while i < len(bcn.terminals):
        if bcn.terminals[i].name == T:
            terminal_obj = bcn.terminals[i]
        i = i + 1
    if terminal_obj == None:
        return -1

    schengen=False
    i=0
    while i<len(EsSc) and not schengen:
        A_id=aircraft.airport[0:2]
        if EsSc[i]==A_id:
            schengen=True
        else:
            i=i+1

    encontrado=False
    n=0
    while n<len(terminal_obj.boarding_areas) and not encontrado:
        area = terminal_obj.boarding_areas[n]
        area_correcta = False

        if schengen and area.type == "Schengen":
            area_correcta = True

        if not schengen and area.type == "No-Schengen":
            area_correcta = True

        if area_correcta:
            k=0
            while k<len(area.gates) and not encontrado:
                if area.gates[k].occupancy==False:
                    encontrado=True
                    area.gates[k].occupancy=True
                    area.gates[k].aircraft_id=aircraft.id
                else:
                    k=k+1
        n=n+1
    if encontrado:
        return 0

    return -1


import tkinter as tk
def DibuixarPlanoTerminal(bcn, canvas_tk):
    canvas_tk.delete("all")

    # el passadís principal de la T1
    canvas_tk.create_rectangle(50, 20, 800, 40, fill="#1a5276")  # Blau fosc
    canvas_tk.create_text(30, 30, text="T1", font=("Arial", 14, "bold"))

    # boarding areas
    if len(bcn.terminals) == 0:
        return
    t1 = bcn.terminals[0]

    x_area = 100
    a = 0
    while a < len(t1.boarding_areas):
        area = t1.boarding_areas[a]

        # Dibuixem el braç vertical de l'àrea
        altura = 50 + len(area.gates) * 30
        canvas_tk.create_rectangle(x_area, 40, x_area + 20, altura, fill="#1a5276")
        canvas_tk.create_text(x_area + 10, 270, text=area.name, font=("Arial", 10, "bold"))

        # Dibuixem les portes a banda i banda del braç
        y_porta = 60
        g = 0
        while g < len(area.gates):
            porta = area.gates[g]
            color = "green" if not porta.occupancy else "red"

            # Si l'índex és parell, a l'esquerra. Si és senar, a la dreta.
            if g % 2 == 0:
                # Porta a l'esquerra
                canvas_tk.create_line(x_area, y_porta, x_area - 20, y_porta, width=3)
                canvas_tk.create_rectangle(x_area - 40, y_porta - 5, x_area - 20, y_porta + 5, fill=color)
                canvas_tk.create_text(x_area - 30, y_porta - 10, text=porta.name, font=("Arial", 6))
                if porta.occupancy:  # Si està ocupada, posem el nom de l'avió
                    canvas_tk.create_text(x_area - 60, y_porta, text=porta.aircraft_id, font=("Arial", 7))
            else:
                # Porta a la dreta
                canvas_tk.create_line(x_area + 20, y_porta, x_area + 40, y_porta, width=3)
                canvas_tk.create_rectangle(x_area + 40, y_porta - 5, x_area + 60, y_porta + 5, fill=color)
                # Posem el nom de la porta (ex: T1BAaG1)
                canvas_tk.create_text(x_area + 50, y_porta - 10, text=porta.name, font=("Arial", 6))
                if porta.occupancy:  # Si està ocupada, posem el nom de l'avió
                    canvas_tk.create_text(x_area + 80, y_porta, text=porta.aircraft_id, font=("Arial", 7))

                y_porta += 60  # Baixem només cada dues portes per no amuntegar

            g = g + 1


        x_area += 150  # Separem la següent àrea (T1BAa, T1BAb...)
        a += 1

    canvas_tk.update_idletasks()
    canvas_tk.config(scrollregion=canvas_tk.bbox("all"))

def DibuixarGraficSenzill(llista_portes, canvas_tk):
    canvas_tk.delete("all")  # Netejar abans de dibuixar

    if len(llista_portes) == 0:
        canvas_tk.create_text(200, 100, text="No hi ha portes per mostrar")
        return

    amplada_barra = 20
    espai = 10
    alcada_max = 120
    x1 = 10
    x2 = 10

    k = 0
    while k < len(llista_portes):
        porta = llista_portes[k]

        # Color según estado
        color = "green"
        if porta["status"] == "occupied":
            color = "red"
        if porta["name"][0:2]=="T1":
            y_top=30
            # Dibuixem el rectangle
            canvas_tk.create_rectangle(x1, y_top, x1 + amplada_barra, y_top + alcada_max, fill=color)
            # Text del nom de la porta a sota
            canvas_tk.create_text(x1 + amplada_barra/2, y_top + alcada_max + 20, text=porta["name"], angle=90, font=("Arial", 8))

            x1 = x1 + 30
        else:
            y_top = 300
            canvas_tk.create_rectangle(x2, y_top, x2 + amplada_barra, y_top + alcada_max, fill=color)
            canvas_tk.create_text(x2 + amplada_barra / 2, y_top + alcada_max + 20, text=porta["name"], angle=90,
                                  font=("Arial", 8))
            x2 = x2 + 30

        k += 1

    canvas_tk.update_idletasks()
    canvas_tk.config(scrollregion=canvas_tk.bbox("all"))


