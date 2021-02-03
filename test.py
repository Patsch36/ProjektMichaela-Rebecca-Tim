import csv
from pathlib import Path

DEBUG_INFO = False # Additional debug infos during run time (switch)

header_a = []   # Array of header values
alldata = []    # Matrix (array of arrays) of csv data entries
header_index = {} # Header Index Dictionary
header_dict = {} # Header Dictionary

# [P] CSV Datei lesen => Werte weiterverarbeiten
# TODO Was macht das header_a Objekt, was alldata?
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
    sum = 0.0

    for lines in range(len(alldata)):
        sum = sum + float(alldata[lines][header_index[search_term]])

    # for lines in alldata:
    #     sum = sum + float(lines[header_index[search_term]])

    mean = sum/(len(alldata))

    return mean


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



# __main__
# Einlesen und Parsen der CSV-Datei von filename1
filename = "100_Pivot_Grunddaten.CSV"
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

    print("\n---------------------\n")
