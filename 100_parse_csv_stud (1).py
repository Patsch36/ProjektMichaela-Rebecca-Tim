import csv                                                                   # Import Daten aus meiner Excel
import turtle                                                                # Import Bibliothek
from pathlib import Path                                                     # Import Bibliothek

DEBUG_INFO = False # Additional debug infos during run time (switch)

header_a = []   # Array of header values                                     # oberste Zeile Excel/ Kopfzeile
alldata = []    # Matrix (array of arrays) of csv data entries               # Alle Daten/ Datenmatrix in Excel
header_index = {} # Header Index Dictionary                                  # Dictionary mit ausgewähltem Searchterm
header_dict = {} # Header Dictionary                                         # Dictionary Kopfzeile 


def read_csv_file(filename):                                                 
    with open(filename, newline='') as csvfile:                              # Öffnet die Datei 
        reader = csv.reader(csvfile)                                         # Erstellt "Leser" / liest Datei ein                                       
        rownum = 1                                                           # 1. "Numerische" Zeile
        for row in reader:                                                   # Schleife beginnt
            if rownum == 1:                                                  # 1 = Header; Wird nur einmal durchgeführt, da rownum nach erstem Durchlauf hochgezählt wird -> Else Zweig
                header = row[0]                                              # Def oberste Zeile = Kopf
                header_a = header.split(";")                                 # Spalten werden getrennt, "Substrings" in Headerliste gespeichert
                # if DEBUG_INFO:                                             # Es sind alle header enthalten
                #     print("Header:")
                #     print(header_a)
            else:
                data = row[0]                                                # Datenzeilen (Rest, ohne Header)
                data_a = data.split(";")                                     # Spalten werden wieder getrennt (einzeln betrachten)
                if DEBUG_INFO: 
                #     print("Data/rownum =", rownum)
                    print(data_a)
                alldata.append(data_a)                                      # Schleife endet wenn alle Daten enthalten
            rownum += 1                                                     # Daten in Alldata abspeichern

    return header_a, alldata                                                # header und Daten werden zurückgegeben


def get_index(header_a, search_term='Liefermenge'):             # Auswahl Spalte Liefermenge, sucht Position der Liefermenge (Größe)
    for i in range(len(header_a)):                              # Schleife, range bereich, len = Zeilenzahl, such so lang bist Searchterm gefunden
        if header_a[i] == search_term:                          # Position der Spalte berechnen (von 0 gezählt), legt Searchterm auf Zahl ab
            break
    header_index[search_term] = i                               # Dict: Liefermenge = i
    return header_index


def create_header_dict(header_a):                               # Dictionary aus der oberster Zeile                         
    for i in range(len(header_a)):                              # Schleife über ganze Länge des headers
        header_dict[header_a[i]] = i                            # jeder Header bekommt eine Nummer (ordnet Wort eine Zahl zu)
    return header_dict

# Schreibweise Deutsch in Englisch (Kommazahlen) = Formatierung => Kommas zu Punkte, damit Fließkommas mit Punkten
def german_to_english_float(germfloat_string):
    # if DEBUG_INFO: print("germfloat before transform: ", germfloat_string)
    if "." in germfloat_string: germfloat_string = germfloat_string.replace(".", "")
    if "," in germfloat_string: germfloat_string = germfloat_string.replace(",", ".")
    # if DEBUG_INFO: print("germfloat after transform: ", germfloat_string)
    return germfloat_string


def calc_mean_by_index(alldata, search_term='Liefermenge'):
    
    # len(alldata) gibt uns die Anzahl der Datenzeilen in der CSV-Datei
    # header_index[search_term] liefert den Spaltenindex für den gesuchten Term (search_term) innerhalb der CSV-Datei
    # alldata[i] liefert die i-te Datenzeile 
    # alldata[i][j] liefert den j-ten Wert (Spalte j) der i-ten Datenzeile 
    
    # Nun müsssen wir über alle Zeilen der CSV-Datei iterieren (Schleife!),
    # um dort alle Werten aufzusummieren, die dem Spaltenindex j für den gesuchten Term entsprechen: 
    # float(alldata[i][j])

    # Der Durchschnitt ist die Summe aller Werte geteilt durch die Anzahl aller Datenzeilen 
    # Dieser Durchschnitt wird per return als Ausgabewert der Funktion übergeben
    
    # ==========Unser Code=============================================================================================
    mean = 0                                                                       # Startwert vorgeben
    sum = 0
                                                                                   
    for line in range(0, len(alldata)):                                            # Schleife, range bereich von 0, len = Zeilenzahl  alldata= nur Daten, ohne header                                         
                                                                                   # line = Zeilen  Summe bzw. line erhöht sich automatisch um 1
        num = german_to_english_float(alldata[line][header_index[search_term]])    # Zahlen aus der richtigen Zelle formatieren (Alldata = 2 dimensionale Liste: 1. Line,  2.Spalte)
        sum = sum + float(num)                                                     # Daten werden aufsummiert

    mean = (float(sum) / len(alldata))                                             # Durchschnitt berechnen: Summe wird durch die Zeilenanzahl in der Liste all Data geteilt für Durchschnitt

    return mean                                                                    # Durchschnitt wird zurückgegeben
#=================================================================================================================================


def calc_weighted_mean_by_index(min, alldata, search_term='Liefermenge'):
    
    # Der gewichtete Durchschnitt summiert lediglich über solche Werte, die über dem Minimum (min) liegen
    # Ansonsten erfolgt die Berechnung des Durchschnitts analog zu calc_mean_by_index()

    # ==========Unser Code========================================================================================================
    mean = 0                                                                        # Startwert vorgeben
    count = 0
    sum = 0

    for line in range(len(alldata)):                                                # Schleife über Länge von alldata
        num = german_to_english_float(alldata[line][header_index[search_term]])     # Formatieren der Daten in Zelle
        if float(num) >= min:                                                       # Bedingung einführen: Wert in der Zelle muss höher oder gleich dem eingegebenen Minimum sein

            sum = sum + float(num)                                                  # Aufsummieren der gefundenen Werte
            count += 1                                                              # Hochzählen der gefundenen Werte
   
    mean = sum / count                                                              # gewichteter Mittelwert berechnen: Summe wird nur durch Anzahl der gefundenen Werte geteil
 
    return mean                                                                     # Gewichteter Durchschnitt zurückgeben
#==================================================================================================================================

def weighted_sum(alldata, prod_gruppe='101', search_term='Produktgruppe'):
   
    # gewichteter Mittelwert aus Produktgruppe (Suche nach bestimmten Wert)
    # hier folgt ihr Code ...
    
    # ========== Mein Code =======================================================================================================

    sum = 0                                                                         # Startwert vorgeben
   

    for line in range(0, len(alldata)):                                             # Schleife in Länge von alldata

        if alldata[line][header_index[search_term]] == prod_gruppe:                 # Bedingung: Werte aus Zelle der Spalte müssen gleich sein mit der Benutzereingabe der Produktgruppe
            num = german_to_english_float(alldata[line][9])                         # Formatieren
            sum = sum + float(num)                                                  # Summe der gefundenen Werte bilden

    return sum                                                                      # Summe zurückgeben
# ===================================================================================================================================

# Generell blockgraph definitions
def draw_bar(t, height):                                                             # festlegen wie turtle laufen soll
    """ Get turtle t to draw one bar, of height. """
    t.begin_fill()           # Added this line
    t.left(90)
    t.forward(height)                                                      
    t.write("  "+ str(height))                                                       # Beschriftung auf Graph
    t.right(90)
    t.forward(40)
    t.right(90)
    t.forward(height)
    t.left(90)
    t.end_fill()             # Added this line
    t.forward(10)

# Draw CSV values to graph 
# in form of a simple turtle graph
def draw_csv_graph(alldata, search_term='Liefermenge'):
    wn = turtle.Screen()         # Set up the window and its attributes
    wn.bgcolor("lightgreen")     # Backroundcolour = grün

    tess = turtle.Turtle()       # Create tess and set some attributes
    tess.color("blue", "red")    # Farben des Graphen
    tess.pensize(3)              # Schriftgröße des Graphen
    # tess.setx(0)
    # tess.sety(0)

    turtle_array = []                                                       # Speicherplatz, in dem Werte des Searchterms gespeichert werden
    num_rows = len(alldata)
    if DEBUG_INFO: print("num_rows", num_rows)
    # header_index[search_term] liefert der Index für den gesuchten Term
    index = header_index[search_term]
    if DEBUG_INFO: print("index: ", index)
    # Wir müssen über alle Zeilen der CSV-Datei suchen: alldata[i]
    # Und dort nach Werten suchen, die dem Index für den gesuchten Term entsprechen: float(alldata[i][index]
    for i in range(num_rows):
        if DEBUG_INFO: 
            print("alldata[",i,"]: ", alldata[i])
            print("alldata[",i,"][",index,"]: ", float(alldata[i][index]))
        turtle_array.append(float(alldata[i][index]))
    print("turtle array: ", turtle_array)
    
    for a in turtle_array:                                                  # Ausführen der Turtle
        draw_bar(tess, a)

    wn.mainloop()


# __main__
# Einlesen und Parsen der CSV-Datei von filename
data_folder = Path(r"C:\Users\Michaela Scheich\Desktop\Informatik python")                # angepasst auf eigenen Ordner, wo Datei abgelegt ist
filename = data_folder / "100_Pivot_Grunddaten.csv"
header_a, alldata = read_csv_file(filename)
header_dict = create_header_dict(header_a)

if DEBUG_INFO: 
    print("--- Start debug infos ---")
    print("Kopfzeile: ", header_a)
    print("... header_dict: ", header_dict)
    print("Datenzeilen: ", alldata)
    print("--- End debug infos ---")

   # Anzeige  int = Nummern     input = Eingabe von Nutzer   search nr= Eingabenummer         # Benutzereingabe abfragen
while True:
    search_nr = int(input("""Welchen der folgenden Terme wollen Sie untersuchen?               
    1: (gew.) Durchschnitt von Bestellmenge
    2: (gew.) Durchschnitt von Liefermenge 
    3: (gew.) Durchschnitt von Wert 
    4: gew. Summe von Produktgruppe
    9: Exit 
    >>> """))

    # Fallunterscheidung 
    if search_nr == 1:
        search_term = 'Bestellmenge'
    elif search_nr == 2:
        search_term = 'Liefermenge'
    elif search_nr == 3:
        search_term = 'Wert'
    elif search_nr == 4:
        search_term = 'Produktgruppe'
    elif search_nr == 9:
        break
    else:
        print("Bitte korrekte Zahl eingeben!")
        break

    # Welche Index-Nummer hat der gesuchte Term innerhalb der CSV-Datei
    # Liste = header_a und Eingabewert in header_index enthalten
    header_index = get_index(header_a, search_term)

    if search_nr in (1, 2, 3):
        # a. Berechnung und Ausgabe des Mittelwerts für alle Werte des gesuchten Terms
        mean = calc_mean_by_index(alldata, search_term)                                                   # Ausgabe Durchschnitt
        print("Durchschnittliche {0}: {1:6.2f}".format(search_term, mean))                                # 0 = Searchterm  / 1 = Durchschnitt

        # b. Berechnung und Ausgabe des gewichteten Mittelwerts für alle Werte des gesuchten Terms
        min = 400               # Minimalwert 400, Festlegung eines Standartwertes
        min = int(input("Geben Sie ein Minimum zur Berechnung des gew. MW ein: "))                        # Minimum vom Benutzer abfragen
        if min <= 0:                                                                                      # Fallunterscheidung                                         
            print("Das Minimum muss größer als 0 sein. Setze Minimum auf 400!") 
            min = 400 # setting default value

        # weighted_mean = calc_weighted_mean_by_index(min, alldata, search_term='Liefermenge')
        weighted_mean = calc_weighted_mean_by_index(min, alldata, search_term)
        print("Gewichtete durchschnittliche {0} für min: {1:6.2f} = {2:6.2f}".format(search_term, min, weighted_mean))   # 0 = Searchterm  / 1 = gewichteter Durchschnitt

        # c. Graph zeichnen
        if input("Zugehörigen Graph zeichnen (y/n)? ") == "y":
            print("Starting turtle graph ...")
            draw_csv_graph(alldata, search_term)

    elif search_nr == 4:
        # Summe aller Werte für eine gesuchte Produktgruppe 
        prod_gruppe = input("Welchen Produktnummer wollen Sie untersuchen? (101, 199, 201, etc.) ")
        sum = weighted_sum(alldata, prod_gruppe, search_term='Produktgruppe')                           # Fehler, Standardinitialisierung '101' aufgehoben, damit Summe der abgefragten Produktgruppe
        print("Summe aller Werte für Produktnummer {0}: {1:6.2f}".format(prod_gruppe, sum))             # 0 = Produktgruppe / 1 = Summer der Werte der Produktgruppe

    print("\n---------------------\n")