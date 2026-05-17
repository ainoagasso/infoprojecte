from aircraft import *

class BarcelonaAP:
    def __init__(self, code=""):
        self.code = code
        self.Terminal = []

class Terminal:
    def __init__(self, name=""):
        self.name = name
        self.BoardingArea = []
        self.ICAO = []

class BoardingArea:
    def __init__(self, name="", type=""):
        self.name = name
        self.type = type
        self.Gate = []

class Gate:
    def __init__(self, name="", occupancy=False, aircraft_id=""):
        self.name = name
        self.occupancy = occupancy
        self.aircraft_id = aircraft_id

Fin = open("LEBL.txt", "r")
line = Fin.readline()
while line != "":
    parts = line.split()
    if parts[0] == "Terminal":
        Terminalname = parts[1]
        n_areas = int(parts[2])
    elif parts[0] == "Area":
        Areaname = parts[1]
        Sch = parts[2]
        init_gate = int(parts[4])
        end_gate = int(parts[6])
    else:
        ICAO = parts[0]
        n_terminals = int(parts[1])
    line = Fin.readline()
Fin.close()

def SetGates(area, init_gate, end_gate, prefix):
    if end_gate <= init_gate:
        return -1
    area.Gate = []
    k = init_gate
    while k <= end_gate:
        name = prefix + str(k)
        g = Gate(name, False, "")
        area.Gate.append(g)
        k = k + 1
    return area.Gate

def LoadAirlines(terminal, t_name):
    try:
        Fin = open(t_name + "_Airlines.txt", "r")
    except FileNotFoundError:
        print("No s'ha trobat el fitxer", t_name, "_Airlines.txt")
        return -1
    terminal.ICAO = []
    line = Fin.readline()
    while line != "":
        line = line.strip()
        if line != "":  # Comprovem que no sigui una línia buida
            parts = line.split()
            codi_ICAO = parts[-1]
            terminal.ICAO.append(codi_ICAO)
        line = Fin.readline()
    Fin.close()
    return terminal.ICAO

def LoadAirportStructure(filename):
    airport_structure = []
    try:
        file = open(filename, "r")
    except FileNotFoundError:
        print("No s'ha trobat el fitxer", filename)
    for line in file:
        line = line.strip()
        if line:
            parts = line.split()
            t_id = parts[0].strip()
            z_id = parts[1].strip()
            trobada = False

            for t in airport_structure:
                if t[0] == t_id:
                    trobada = True
                    terminal = t
            if not trobada:
                terminal = [t_id, []]
                airport_structure.append(terminal)
            zona_trobada = False
            for z in terminal[1]:
                if z[0] == z_id:
                    zona_trobada = True
            if not zona_trobada:
                terminal[1].append([z_id, []])
                SetGates(airport_structure, t_id, z_id, z_id)
    file.close()
    airport_structure = LoadAirlines(airport_structure, "Airlines.txt")
    return airport_structure

def GateOccupancy(bcn):
    llista_estat = []
    t = 0
    while t < len(bcn.Terminal):
        terminal_actual = bcn.Terminal[t]
        a = 0
        while a < len(terminal_actual.BoardingArea):
            area_actual = terminal_actual.BoardingArea[a]
            g = 0
            while g < len(area_actual.Gate):
                porta = area_actual.Gate[g]
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

import tkinter as tk

def DibuixarPlanoTerminal(bcn, canvas_tk):
    canvas_tk.delete("all")

    # el passadís principal de la T1
    canvas_tk.create_rectangle(50, 20, 700, 40, fill="#1a5276")  # Blau fosc
    canvas_tk.create_text(30, 30, text="T1", font=("Arial", 14, "bold"))

    # boarding areas
    if len(bcn.Terminal) == 0: return
    t1 = bcn.Terminal[0]

    x_area = 100
    a = 0
    while a < len(t1.BoardingArea):
        area = t1.BoardingArea[a]

        # Dibuixem el braç vertical de l'àrea
        canvas_tk.create_rectangle(x_area, 40, x_area + 20, 250, fill="#1a5276")
        canvas_tk.create_text(x_area + 10, 270, text=area.name, font=("Arial", 10, "bold"))

        # Dibuixem les portes a banda i banda del braç
        y_porta = 60
        g = 0
        while g < len(area.Gate):
            porta = area.Gate[g]
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

                y_porta += 40  # Baixem només cada dues portes per no amuntegar

            g = g + 1
            if y_porta > 230: break  # Perquè no se surti del dibuix

        x_area += 150  # Separem la següent àrea (T1BAa, T1BAb...)
        a += 1

def DibuixarGraficSenzill(llista_portes, canvas_tk):
    canvas_tk.delete("all")  # Netejar abans de dibuixar

    if len(llista_portes) == 0:
        canvas_tk.create_text(200, 100, text="No hi ha portes per mostrar")
        return

    x = 10
    y_top = 30
    amplada_barra = 25
    espai = 10
    alcada_max = 120

    k = 0
    while k < len(llista_portes):
        porta = llista_portes[k]

        # Color según estado
        color = "green"
        if porta["status"] == "occupied":
            color = "red"

        # Dibuixem el rectangle
        canvas_tk.create_rectangle(x, y_top, x + amplada_barra, y_top + alcada_max, fill=color)

        # Text del nom de la porta a sota
        canvas_tk.create_text(x + amplada_barra / 2, y_top + alcada_max + 20, text=porta["name"], angle=90, font=("Arial", 8))

        x = x + amplada_barra + espai
        k += 1

# TEST

# test LoadAirportStructure
def TestCarregaReal():
    aeroport = BarcelonaAP(code="LEBL")

    try:
        Fin = open("LEBL.txt", "r")
        line = Fin.readline()

        current_terminal = None

        while line != "":
            parts = line.split()
            if not parts:
                line = Fin.readline()
                continue

            if parts[0] == "Terminal":
                t_name = parts[1]
                # Creem l'objecte Terminal i l'afegim a l'aeroport
                current_terminal = Terminal(name=t_name)
                aeroport.Terminal.append(current_terminal)
                print(f"[*] Terminal detectada: {t_name}")

                # Intentem carregar les aerolínies d'aquesta terminal
                LoadAirlines(current_terminal, t_name)

            elif parts[0] == "Area":
                if current_terminal:
                    a_name = parts[1]
                    a_type = parts[2]  # Schengen/No-Schengen

                    nova_area = BoardingArea(name=a_name, type=a_type)
                    current_terminal.BoardingArea.append(nova_area)

                    # Generem les portes
                    try:
                        i_gate = int(parts[4])
                        e_gate = int(parts[6])
                        SetGates(nova_area, i_gate, e_gate, prefix="P")
                        print(f"    [+] Àrea: {a_name} ({a_type}) -> {len(nova_area.Gate)} portes creades.")
                    except (ValueError, IndexError):
                        print(f"    [!] Error en format de portes per a l'àrea {a_name}")
                else:
                    print("[!] Error: S'ha trobat una Àrea sense una Terminal definida prèviament.")

            else:
                print(f"[i] Info general: {parts}")

            line = Fin.readline()

        Fin.close()

        # --- VERIFICACIÓ FINAL ---
        print("\n" + "=" * 30)
        print("RESUM DE LA CÀRREGA")
        print("=" * 30)
        for t in aeroport.Terminal:
            print(f"\nTerminal: {t.name}")
            print(f"Aerolínies (ICAO): {t.ICAO}")
            for a in t.BoardingArea:
                noms_portes = [g.name for g in a.Gate]
                print(f"  └─ Àrea {a.name} [{a.type}]: {len(noms_portes)} portes ({noms_portes[0]}...{noms_portes[-1]})")

    except FileNotFoundError:
        print("ERROR: No s'ha trobat el fitxer LEBL.txt al directori actual.")
    except Exception as e:
        print(f"ERROR inesperat: {e}")

if __name__ == "__main__":
    TestCarregaReal()

# test GateOccupancy

meu_bcn = BarcelonaAP("LEBL")
t1 = Terminal("T1")
meu_bcn.Terminal.append(t1)
zona_a = BoardingArea("Zona A", "Schengen")
t1.BoardingArea.append(zona_a)

# Porta lliure
p1 = Gate("A01", occupancy=False, aircraft_id="")
# Porta ocupada
p2 = Gate("A02", occupancy=True, aircraft_id="VLG1234")

zona_a.Gate.append(p1)
zona_a.Gate.append(p2)

resultats = GateOccupancy(meu_bcn)

# 6. Mostrem els resultats
print("--- ESTAT DE LES PORTES ---")
i = 0
while i < len(resultats):
    porta_info = resultats[i]
    print("Porta: " + porta_info["name"])
    print("  Estat: " + porta_info["status"])
    if porta_info["status"] == "occupied":
        print("  Avió: " + porta_info["aircraft_id"])
    print("-" * 20)
    i = i + 1

# test interesting addition
def TestReal():
    # Creem l'aeroport
    bcn = BarcelonaAP("LEBL")
    t1 = Terminal("T1")
    bcn.Terminal.append(t1)

    # Creem 4 àrees
    noms_areas = ["T1BAa", "T1BAb", "T1BAc", "T1BAd"]
    i = 0
    while i < len(noms_areas):
        nova_area = BoardingArea(noms_areas[i])
        # Afegim 5 portes a cada àrea
        j = 1
        while j <= 5:
            esta_ocupada = (i == 0 and j == 4) or (i == 2 and j == 1)
            id_vuelo = "DALEN" if esta_ocupada else ""

            p = Gate(f"G{j}", occupancy=esta_ocupada, aircraft_id=id_vuelo)
            nova_area.Gate.append(p)
            j += 1

        t1.BoardingArea.append(nova_area)
        i += 1

    # Creem la finestra de test
    arrel = tk.Tk()
    arrel.title("Plànol d'Ocupació T1 - Barcelona")

    # Canvas
    canva = tk.Canvas(arrel, width=800, height=400, bg="white")
    canva.pack(padx=20, pady=20)

    DibuixarPlanoTerminal(bcn, canva)
    arrel.mainloop()

TestReal()