import csv
import turtle
from pathlib import Path

DEBUG_INFO = False # Additional debug infos during run time (switch)

header_a = []   # Array of header values
alldata = []    # Matrix (array of arrays) of csv data entries
header_index = {} # Header Index Dictionary
header_dict = {} # Header Dictionary

# [P] CSV Datei lesen => Werte weiterverarbeiten
# [TODO] Was macht das header_a Objekt, was alldata?
def read_csv_file(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        rownum = 1
        for row in reader:
            if rownum == 1: 
                header = row[0]
                header_a = header.split(";")
                # if DEBUG_INFO:
                #     print("Header:")
                #     print(header_a)
            else:
                data = row[0]
                data_a = data.split(";")
                # if DEBUG_INFO: 
                #     print("Data/rownum =", rownum)
                #     print(data_a)
                alldata.append(data_a)
            rownum += 1

    return header_a, alldata

# [P] Sucht Position von gesuchter Gr��e (Spalte)
def get_index(header_a, search_term='Liefermenge'):
    for i in range(len(header_a)):
        if header_a[i] == search_term:
            break
    header_index[search_term] = i
    return header_index

# [P] Sortiert Titel in Array
def create_header_dict(header_a):
    for i in range(len(header_a)):
        header_dict[header_a[i]] = i
    return header_dict

# [P] Formatierungen
def german_to_english_float(germfloat_string):
    # if DEBUG_INFO: print("germfloat before transform: ", germfloat_string)
    if "." in germfloat_string: germfloat_string = germfloat_string.replace(".", "")
    if "," in germfloat_string: germfloat_string = germfloat_string.replace(",", ".")
    # if DEBUG_INFO: print("germfloat after transform: ", germfloat_string)
    return germfloat_string


def calc_mean_by_index(alldata, search_term='Liefermenge'):
    # len(alldata) gibt uns die Anzahl der Datenzeilen in der CSV-Datei
    # header_index[search_term] liefert den Spaltenindex f�r den gesuchten Term (search_term) innerhalb der CSV-Datei
    # alldata[i] liefert die i-te Datenzeile 
    # alldata[i][j] liefert den j-ten Wert (Spalte j) der i-ten Datenzeile 
    
    # Nun m�sssen wir �ber alle Zeilen der CSV-Datei iterieren (Schleife!),
    # um dort alle Werten aufzusummieren, die dem Spaltenindex j f�r den gesuchten Term entsprechen: 
    # float(alldata[i][j])

    # Der Durchschnitt ist die Summe aller Werte geteilt durch die Anzahl aller Datenzeilen 
    # Dieser Durchschnitt wird per return als Ausgabewert der Funktion �bergeben

    # hier folgt ihr Code ...



def calc_weighted_mean_by_index(min, alldata, search_term='Liefermenge'):
    mean = 0
    # Der gewichtete Durchschnitt summiert lediglich �ber solche Werte, die �ber dem Minimum (min) liegen
    # Ansonsten erfolgt die Berechnung des Durchschnitts analog zu calc_mean_by_index()

    # hier folgt ihr Code ...
    
    return mean

def weighted_sum(alldata, prod_gruppe='101', search_term='Produktgruppe'):
    sum = 0

    # hier folgt ihr Code ...

    return sum

# Generell blockgraph definitions
def draw_bar(t, height):
    """ Get turtle t to draw one bar, of height. """
    t.begin_fill()           # Added this line
    t.left(90)
    t.forward(height)
    t.write("  "+ str(height))
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
    wn.bgcolor("lightgreen")

    tess = turtle.Turtle()       # Create tess and set some attributes
    tess.color("blue", "red")
    tess.pensize(3)
    # tess.setx(0)
    # tess.sety(0)

    turtle_array = []
    num_rows = len(alldata)
    if DEBUG_INFO: print("num_rows", num_rows)
    # header_index[search_term] liefert der Index f�r den gesuchten Term
    index = header_index[search_term]
    if DEBUG_INFO: print("index: ", index)
    # Wir m�ssen �ber alle Zeilen der CSV-Datei suchen: alldata[i]
    # Und dort nach Werten suchen, die dem Index f�r den gesuchten Term entsprechen: float(alldata[i][index]
    for i in range(num_rows):
        if DEBUG_INFO: 
            print("alldata[",i,"]: ", alldata[i])
            print("alldata[",i,"][",index,"]: ", float(alldata[i][index]))
        turtle_array.append(float(alldata[i][index]))
    print("turtle array: ", turtle_array)
    
    for a in turtle_array:
        draw_bar(tess, a)

    wn.mainloop()


# __main__
# Einlesen und Parsen der CSV-Datei von filename
data_folder = Path(r"D:\Lehre\Sem 1\Python") # [P] �ndern: Pfad zur Datei in deinem Verzeichnis, am Besten in gleichen Ordner, dann reicht Dateiname mit Endung
filename = data_folder / "100_Pivot_Grunddaten.csv"
header_a, alldata = read_csv_file(filename)
header_dict = create_header_dict(header_a)

if DEBUG_INFO: 
    print("--- Start debug infos ---")
    print("Kopfzeile: ", header_a)
    print("... header_dict: ", header_dict)
    print("Datenzeilen: ", alldata)
    print("--- End debug infos ---")

    # [P] Hier gibt er sein Men� auf der Konsole aus und liest Eingabe ein
while True:
    # [P] String gibt an, welche Gr��en gesucht sind
    search_nr = int(input("""Welchen der folgenden Terme wollen Sie untersuchen?
    1: (gew.) Durchschnitt von Bestellmenge
    2: (gew.) Durchschnitt von Liefermenge 
    3: (gew.) Durchschnitt von Wert 
    4: gew. Summe von Produktgruppe
    9: Exit 
    >>> """))

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
    header_index = get_index(header_a, search_term)

    if search_nr in (1, 2, 3):
        # a. Berechnung und Ausgabe des Mittelwerts f�r alle Werte des gesuchten Terms
        mean = calc_mean_by_index(alldata, search_term)
        print("Durchschnittliche {0}: {1:6.2f}".format(search_term, mean))

        # b. Berechnung und Ausgabe des gewichteten Mittelwerts f�r alle Werte des gesuchten Terms
        min = 400
        min = int(input("Geben Sie ein Minimum zur Berechnung des gew. MW ein: "))
        if min <= 0:
            print("Das Minimum muss gr��er als 0 sein. Setze Minimum auf 400!")
            min = 400 # setting default value

        # weighted_mean = calc_weighted_mean_by_index(min, alldata, search_term='Liefermenge')
        weighted_mean = calc_weighted_mean_by_index(min, alldata, search_term)
        print("Gewichtete durchschnittliche {0} f�r min: {1:6.2f} = {2:6.2f}".format(search_term, min, weighted_mean))

        # c. Graph zeichnen
        if input("Zugeh�rigen Graph zeichnen (y/n)? ") == "y":
            print("Starting turtle graph ...")
            draw_csv_graph(alldata, search_term)

    elif search_nr == 4:
        # Summe aller Werte f�r eine gesuchte Produktgruppe 
        prod_gruppe = input("Welchen Produktnummer wollen Sie untersuchen? (101, 199, 201, etc.) ")
        sum = weighted_sum(alldata, prod_gruppe='101', search_term='Produktgruppe')
        print("Summe aller Werte f�r Produktnummer {0}: {1:6.2f}".format(prod_gruppe, sum))

    print("\n---------------------\n")
