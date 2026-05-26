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
        self.aircraft=None


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

        if not schengen and area.type == "non-Schengen":
            area_correcta = True

        if area_correcta:
            k=0
            while k<len(area.gates) and not encontrado:
                if area.gates[k].occupancy==False:
                    encontrado=True
                    area.gates[k].occupancy=True
                    area.gates[k].aircraft_id=aircraft.id
                    area.gates[k].aircraft = aircraft
                else:
                    k=k+1
        n=n+1
    if encontrado:
        return 0

    return -1

#per no saturar una boarding area
def seleccionar_millor_gate(bcn, avio):
    schengen = False
    i = 0

    while i < len(EsSc) and not schengen:
        A_id = avio.airport[0:2]

        if EsSc[i] == A_id:
            schengen = True
        else:
            i += 1

    millor_gate = None
    millor_score = 10**9

    for terminal in bcn.terminals:
        for area in terminal.boarding_areas:
            for gate in area.gates:

                # 1. només gates lliures
                if gate.occupancy:
                    continue
                # 2. Schengen
                if area.type == "Schengen" and not schengen:
                    continue
                if area.type == "non-Schengen" and schengen:
                    continue

                score = 0
                # preferència per gates buides en àrees menys saturades
                ocupades_area = sum(1 for g in area.gates if g.occupancy)
                score += ocupades_area * 10

                # preferir terminals menys saturats
                ocupades_terminal = 0
                for a in terminal.boarding_areas:
                    ocupades_terminal += sum(1 for g in a.gates if g.occupancy)

                score += ocupades_terminal * 2

                # lleu penalització per distància "visual" (opcional)
                score += len(area.gates)

                # 4. millor gate
                if score < millor_score:
                    millor_score = score
                    millor_gate = gate

    return millor_gate

def ResetGates(bcn):
    for terminal in bcn.terminals:
        for area in terminal.boarding_areas:
            for gate in area.gates:
                gate.occupancy = False
                gate.aircraft_id = ""
                gate.aircraft=None

#si hi ha una boarding area amb moltes gates ocupades no l'assignarà allà
def IntelligentAssign(bcn, aircrafts):
    assignats = 0
    no_assignats = 0

    ResetGates(bcn)

    for avio in aircrafts:
        gate = seleccionar_millor_gate(bcn, avio)

        if gate is None:
            no_assignats += 1
            continue

        gate.occupancy = True
        gate.aircraft_id = avio.id
        assignats += 1
        gate.aircraft=avio

    return assignats, no_assignats

def DibuixarPlanoTerminal(bcn, canvas_tk, gates_ui):
    canvas_tk.delete("all")
    gates_ui.clear()
    # boarding areas
    if len(bcn.terminals) == 0:
        return

    x_terminal=50
    t = 0
    while t < len(bcn.terminals):

        terminal = bcn.terminals[t]

        # passadís principal
        amplada_terminal = len(terminal.boarding_areas) * 220

        canvas_tk.create_rectangle(x_terminal,20,x_terminal + amplada_terminal,40,fill="#1a5276", outline="")
        canvas_tk.create_text(x_terminal + amplada_terminal/2,10,text=terminal.name,font=("Segoe UI", 14, "bold"))

        x_area = x_terminal + 60
        a = 0
        while a < len(terminal.boarding_areas):
            area = terminal.boarding_areas[a]

        # Dibuixem el braç vertical de l'àrea
            altura = 90 + len(area.gates) * 32

            # Ombra boarding area
            canvas_tk.create_rectangle(x_area + 4,44,x_area + 24,altura + 4,fill="#5d6d7e",outline="")
            # Braç principal
            canvas_tk.create_rectangle(x_area,40,x_area + 20,altura,fill="#1a5276",outline="")
            # Nom area
            canvas_tk.create_text(x_area + 10,58,text=area.name,font=("Segoe UI", 10, "bold"),fill="white")

            y_porta = 85
            g = 0
            while g < len(area.gates):

                porta = area.gates[g]

                if porta.occupancy:
                    color = "#e74c3c" #vermell modern
                else:
                    color = "#2ecc71" #verd modern

                if g % 2 == 0:
                    # connexió esquerra
                    canvas_tk.create_line(x_area,y_porta,x_area - 35,y_porta,width=4,fill="#34495e")

                    # gate esquerra
                    rect=canvas_tk.create_rectangle(x_area - 90,y_porta - 10,x_area - 35,y_porta + 10,fill=color,outline="")
                    gates_ui.append((x_area - 90, y_porta - 10, x_area - 35, y_porta + 10, porta, rect))
                    canvas_tk.create_text(x_area - 62,y_porta - 18,text=porta.name,font=("Segoe UI", 7, "bold"))

                    # nom avió dins la gate
                    if porta.occupancy:
                        canvas_tk.create_text(x_area - 62,y_porta,text=porta.aircraft_id,font=("Segoe UI", 8, "bold"),fill="white")

                else:
                    # connexió dreta
                    canvas_tk.create_line(x_area + 20,y_porta,x_area + 55,y_porta,width=4,fill="#34495e")

                    # gate dreta
                    rect=canvas_tk.create_rectangle(x_area + 55,y_porta - 10,x_area + 110,y_porta + 10,fill=color,outline="")
                    gates_ui.append((x_area + 55, y_porta - 10, x_area + 110, y_porta + 10, porta, rect))
                    canvas_tk.create_text(x_area + 82,y_porta - 18,text=porta.name,font=("Segoe UI", 7, "bold"))

                    #nom avió dins de gate
                    if porta.occupancy:
                        canvas_tk.create_text(x_area + 82,y_porta,text=porta.aircraft_id,font=("Segoe UI", 8, "bold"),fill="white")

                    y_porta += 55
                g += 1

            x_area += 220  # Separem la següent àrea (T1BAa, T1BAb...)
            a += 1
        x_terminal += amplada_terminal +250
        t += 1

    canvas_tk.update_idletasks()
    canvas_tk.config(scrollregion=canvas_tk.bbox("all"))

def AssignNightGates(bcn,aircrafts):
    if len(aircrafts) == 0:
        return -1

    night= NightAircraft(aircrafts)
    if night == -1:
        return -1

    i=0
    while i < len(night):
        ac=night[i]
        sleep=Aircraft(ac.id, ac.company, "LEBL", "", ac.detination, ac.departure_time)
        AssignGate(bcn,sleep)
        i += 1

    return 0




