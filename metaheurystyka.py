import copy
import csv
import random
import math

initial_temperature = 1000
cooling_rate = 0.95
num_iterations = 100000

iloscTur = 18
dlugoscTrasy = 6
indeksGlowicy = 12
indeksBramki = 2
indeksBramkiPrzeciwnika = 22

def import_matrix_from_csv(file_path, delimiter=','):
    matrix = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file, delimiter=delimiter)
        for row in csv_reader:
            matrix.append(row)
    return matrix

dostepneRuchy = import_matrix_from_csv("adjacency_matrix.csv")
print(dostepneRuchy)


solution = {
    "calaTrasaWMacierzy": [[]],
    "calaTrasaWMacierzyBramkaZero": [[[]]],
    "calaTrasaWMacierzyBramkaJeden": [[[]]],
    "zeroTrasaOdBramkiDoPunktu": [[]],
    "zeroTrasaOdBramkiDoPunktuPoWyzerowaniu": [[]],
    "zeroOstatniIndeksTrasyOdBramki": [],
    "zeroOstatniIndeksTrasyOdBramkiPoUwzglednieniuTur": [],
    "zeroIsZeroBramka": [[]],
    "jedenTrasaOdBramkiDoPunktu": [],
    "jedenTrasaOdBramkiDoPunktuPoWyzerowaniu": [],
    "jedenOstatniIndeksTrasyOdBramki": [],
    "jedenOstatniIndeksTrasyOdBramkiPoUwzglednieniuTur": [],
    "jedenIsZeroBramkaPrzeciwnik": [],
    "trasaWTurzePoWyzerowaniu": [],
    "trasaWTurze": [],
    "ostatniIndeksTrasyWTurze": [],
    "ostatniaTura": 0,
    "isZero": [],
    "odwiedzoneWierzcholkiNaPrzestrzeniTur": [],
    "iloscOdwiedzinDanegoWierzcholkaWDanejTurze": [],
    "czyjaTura": [],
    "temp": []
}


def calaTrasaDlugosc2(ostatniIndeksTrasyWTurze):
    suma = 0
    for d in ostatniIndeksTrasyWTurze:
        suma += d
    return suma

def zeroOdlegloscDoBramki(zeroOstatniIndeksTrasyOdBramkiPoUwzglednieniuTur):
    suma = 0
    for d in zeroOstatniIndeksTrasyOdBramkiPoUwzglednieniuTur:
        suma += d
    return suma

def jedenOdlegloscDoBramki(jedenOstatniIndeksTrasyOdBramkiPoUwzglednieniuTur):
    suma = 0
    for d in jedenOstatniIndeksTrasyOdBramkiPoUwzglednieniuTur:
        suma += d
    return suma


def objective_function(solution):
    wynik = 99999999999 - calaTrasaDlugosc2(solution["ostatniIndeksTrasyWTurze"]) + 10 * zeroOdlegloscDoBramki(solution["zeroOstatniIndeksTrasyOdBramkiPoUwzglednieniuTur"]) + 10 * jedenOdlegloscDoBramki(solution["jedenOstatniIndeksTrasyOdBramkiPoUwzglednieniuTur"]) + 99 - solution["ostatniaTura"]

    if (solution["czyjaTura"][0] != 1):
        wynik += 10000

    if (solution["ostatniIndeksTrasyWTurze"][0] != 1):
        wynik += 100

    if (solution["ostatniIndeksTrasyWTurze"][1] != 1):
        wynik += 100

    if (solution["trasaWTurze"][0][0] != indeksGlowicy):
        wynik += 10000000

    if (solution["ostatniaTura"] < 1):
        wynik += 100

    if (solution["ostatniaTura"] > iloscTur):
        wynik += 100

    for k in range(0,iloscTur):
        for g in range(0, dlugoscTrasy):
            if solution["odwiedzoneWierzcholkiNaPrzestrzeniTur"][k][solution["trasaWTurzePoWyzerowaniu"][k][g]] == (k <=  solution["ostatniaTura"] and g <= solution["ostatniIndeksTrasyWTurze"][k]):
                returnValue = True
            else:
                wynik += 100

    for k in range(0,iloscTur):
        for i in range(0, 24):
            sum_condition = sum(solution["odwiedzoneWierzcholkiNaPrzestrzeniTur"][g][i] >= 1 for g in range(k))

            if (solution["iloscOdwiedzinDanegoWierzcholkaWDanejTurze"][k][i] ==  sum_condition):
                returnValue = True
            else:
                wynik += 100
    for k in range(iloscTur):
        for i in range(dlugoscTrasy):
            temp_value = solution["isZero"][k][i] * (
            solution["iloscOdwiedzinDanegoWierzcholkaWDanejTurze"][k][solution["trasaWTurzePoWyzerowaniu"][k][i]]) >= 1
            if solution["temp"][k][i] != temp_value:
                wynik += 100

    for k in range(1, iloscTur):
        for i in range(dlugoscTrasy):
            temp_value = i < solution["ostatniIndeksTrasyWTurze"][k]
            if solution["temp"][k][i] != temp_value:
                wynik += 99999999

    for i in range(iloscTur):
        for j in range(dlugoscTrasy):
            temp_value = solution["czyjaTura"][i] * solution["trasaWTurzePoWyzerowaniu"][i][j]
            if temp_value == indeksBramki:
                wynik += 999999

    for i in range(iloscTur):
        zeroOstatniIndeksTrasyOdBramkiPoUwzglednieniuTur_value = ((1 - solution["czyjaTura"][i]) *
                                                                  solution["zeroOstatniIndeksTrasyOdBramki"][i]) * (
                                                                             solution["ostatniaTura"] > i)
        if zeroOstatniIndeksTrasyOdBramkiPoUwzglednieniuTur_value != \
                solution["zeroOstatniIndeksTrasyOdBramkiPoUwzglednieniuTur"][i]:
            wynik += 999

    for i in range(iloscTur):
        if  solution["jedenOstatniIndeksTrasyOdBramkiPoUwzglednieniuTur"][i] != (
                solution["czyjaTura"][i] *  solution["jedenOstatniIndeksTrasyOdBramki"][i]) * ( solution["ostatniaTura"] > i):
            wynik += 9999

    for i in range(iloscTur):
        for j in range(dlugoscTrasy):
            if solution["trasaWTurzePoWyzerowaniu"][i][j] != solution["isZero"][i][j] * solution["trasaWTurze"][i][j]:
                wynik += 9999999999999

    for i in range(iloscTur):
        for j in range(dlugoscTrasy - 1):
            lhs = solution["calaTrasaWMacierzy"][solution["trasaWTurzePoWyzerowaniu"][i][j]][
                solution["trasaWTurzePoWyzerowaniu"][i][j + 1]]
            rhs = sum(solution["trasaWTurzePoWyzerowaniu"][k][g] == solution["trasaWTurzePoWyzerowaniu"][i][j] and
                      solution["trasaWTurzePoWyzerowaniu"][k][g + 1] == solution["trasaWTurzePoWyzerowaniu"][i][j + 1]
                      for k in range(iloscTur) for g in range(dlugoscTrasy - 1))
            if lhs != rhs:
                wynik += 99999

    # Constraint 2
    for i in range(iloscTur):
        for j in range(1, dlugoscTrasy):
            lhs = solution["calaTrasaWMacierzy"][solution["trasaWTurzePoWyzerowaniu"][i][j - 1]][
                solution["trasaWTurzePoWyzerowaniu"][i][j]]
            rhs = sum(solution["trasaWTurzePoWyzerowaniu"][k][g] == solution["trasaWTurzePoWyzerowaniu"][i][j] and
                      solution["trasaWTurzePoWyzerowaniu"][k][g - 1] == solution["trasaWTurzePoWyzerowaniu"][i][j - 1]
                      for k in range(iloscTur) for g in range(1, dlugoscTrasy))
            if lhs != rhs:
                wynik += 9999

    # Constraint 3
    for i in range(iloscTur):
        for j in range(dlugoscTrasy - 1):
            lhs = solution["calaTrasaWMacierzyBramkaZero"][i][solution["zeroTrasaOdBramkiDoPunktuPoWyzerowaniu"][i][j]][
                solution["zeroTrasaOdBramkiDoPunktuPoWyzerowaniu"][i][j + 1]]
            rhs = sum(solution["zeroTrasaOdBramkiDoPunktuPoWyzerowaniu"][i][j] ==
                      solution["zeroTrasaOdBramkiDoPunktuPoWyzerowaniu"][i][g] and
                      solution["zeroTrasaOdBramkiDoPunktuPoWyzerowaniu"][i][j + 1] ==
                      solution["zeroTrasaOdBramkiDoPunktuPoWyzerowaniu"][i][g + 1] for g in range(dlugoscTrasy - 1))
            if lhs != rhs:
                wynik += 994453

    # Constraint 4
    for i in range(iloscTur):
        for j in range(1, dlugoscTrasy):
            lhs = \
            solution["calaTrasaWMacierzyBramkaZero"][i][solution["zeroTrasaOdBramkiDoPunktuPoWyzerowaniu"][i][j - 1]][
                solution["zeroTrasaOdBramkiDoPunktuPoWyzerowaniu"][i][j]]
            rhs = sum(solution["zeroTrasaOdBramkiDoPunktuPoWyzerowaniu"][i][j] ==
                      solution["zeroTrasaOdBramkiDoPunktuPoWyzerowaniu"][i][g] and
                      solution["zeroTrasaOdBramkiDoPunktuPoWyzerowaniu"][i][j - 1] ==
                      solution["zeroTrasaOdBramkiDoPunktuPoWyzerowaniu"][i][g - 1] for g in range(1, dlugoscTrasy))
            if lhs != rhs:
                wynik += 41231

    # Constraint 5
    for i in range(iloscTur):
        for j in range(dlugoscTrasy - 1):
            lhs = \
            solution["calaTrasaWMacierzyBramkaJeden"][i][solution["jedenTrasaOdBramkiDoPunktuPoWyzerowaniu"][i][j]][
                solution["jedenTrasaOdBramkiDoPunktuPoWyzerowaniu"][i][j + 1]]
            rhs = sum(solution["jedenTrasaOdBramkiDoPunktuPoWyzerowaniu"][i][j] ==
                      solution["jedenTrasaOdBramkiDoPunktuPoWyzerowaniu"][i][g] and
                      solution["jedenTrasaOdBramkiDoPunktuPoWyzerowaniu"][i][j + 1] ==
                      solution["jedenTrasaOdBramkiDoPunktuPoWyzerowaniu"][i][g + 1] for g in range(dlugoscTrasy - 1))
            if lhs != rhs:
                wynik += 4324234

    # Constraint 6
    for i in range(iloscTur):
        for j in range(1, dlugoscTrasy):
            lhs = \
            solution["calaTrasaWMacierzyBramkaJeden"][i][solution["jedenTrasaOdBramkiDoPunktuPoWyzerowaniu"][i][j - 1]][
                solution["jedenTrasaOdBramkiDoPunktuPoWyzerowaniu"][i][j]]
            rhs = sum(solution["jedenTrasaOdBramkiDoPunktuPoWyzerowaniu"][i][j] ==
                      solution["jedenTrasaOdBramkiDoPunktuPoWyzerowaniu"][i][g] and
                      solution["jedenTrasaOdBramkiDoPunktuPoWyzerowaniu"][i][j - 1] ==
                      solution["jedenTrasaOdBramkiDoPunktuPoWyzerowaniu"][i][g - 1] for g in range(1, dlugoscTrasy))
            if lhs != rhs:
                wynik += 342342

    for i in range(1, 25):
        for j in range(1, 25):
            if solution["calaTrasaWMacierzy"][i][j] > 1:
                wynik += 342342

    # Constraint 2
    for i in range(1, 25):
        if solution["calaTrasaWMacierzy"][i][0] > 1:
            wynik += 342342

    # Constraint 3
    for i in range(1, 25):
        if solution["calaTrasaWMacierzy"][0][i] > 1:
            wynik += 342342

    # Constraint 4
    for i in range(1, 25):
        for j in range(1, 25):
            if solution["calaTrasaWMacierzy"][i][j] + solution["calaTrasaWMacierzy"][j][i] > 1:
                wynik += 4342342

    # Constraint 5
    for i in range(1, 25):
        if solution["calaTrasaWMacierzy"][i][0] + solution["calaTrasaWMacierzy"][0][i] > 1:
            wynik += 4342342

    for k in range(iloscTur):
        for i in range(1, 25):
            for j in range(1, 25):
                if solution["calaTrasaWMacierzyBramkaZero"][k][i][j] > 1:
                    wynik += 42342

    # Constraint 2
    for k in range(iloscTur):
        for i in range(1, 25):
            if solution["calaTrasaWMacierzyBramkaZero"][k][i][0] > 1:
                wynik += 342342

    # Constraint 3
    for k in range(iloscTur):
        for i in range(1, 25):
            for j in range(1, 25):
                if solution["calaTrasaWMacierzyBramkaZero"][k][i][j] + solution["calaTrasaWMacierzyBramkaZero"][k][j][
                    i] > 1:
                    wynik += 342342

    # Constraint 4
    for k in range(iloscTur):
        for i in range(1, 25):
            if solution["calaTrasaWMacierzyBramkaZero"][k][i][0] + solution["calaTrasaWMacierzyBramkaZero"][k][0][
                i] > 1:
                wynik += 54343

    # Constraint 5
    for k in range(iloscTur):
        for i in range(1, 25):
            for j in range(1, 25):
                if solution["calaTrasaWMacierzyBramkaJeden"][k][i][j] > 1:
                    wynik += 342

    # Constraint 6
    for k in range(iloscTur):
        for i in range(1, 25):
            if solution["calaTrasaWMacierzyBramkaJeden"][k][i][0] > 1:
                wynik += 5433

    # Constraint 7
    for k in range(iloscTur):
        for i in range(1, 25):
            for j in range(1, 25):
                if solution["calaTrasaWMacierzyBramkaJeden"][k][i][j] + solution["calaTrasaWMacierzyBramkaJeden"][k][j][
                    i] > 1:
                    wynik += 432435

    # Constraint 8
    for k in range(iloscTur):
        for i in range(1, 25):
            if solution["calaTrasaWMacierzyBramkaJeden"][k][i][0] + solution["calaTrasaWMacierzyBramkaJeden"][k][0][
                i] > 1:
                wynik += 342342

    # Constraint 9
    for i in range(iloscTur - 1):
        if solution["trasaWTurze"][i + 1][0] != solution["trasaWTurze"][i][solution["ostatniIndeksTrasyWTurze"][i]]:
            wynik += 53242324

    # Constraint 10
    for i in range(iloscTur - 1):
        if solution["czyjaTura"][i + 1] != 1 - solution["czyjaTura"][i]:
            wynik += 532432

    # Constraint 11
    for k in range(iloscTur):
        for i in range(dlugoscTrasy-1):
            if dostepneRuchy[solution["trasaWTurze"][k][i]][solution["trasaWTurze"][k][i + 1]] == 0:
                wynik += 43243623400000

    # Constraint 12
    for i in range(iloscTur):
        if solution["zeroTrasaOdBramkiDoPunktu"][i][0] != solution["trasaWTurze"][i][solution["ostatniIndeksTrasyWTurze"][i]]:
            wynik += 43243623400000

    # Constraint 13
    for k in range(iloscTur):
        for i in range(dlugoscTrasy-1):
            if dostepneRuchy[solution["zeroTrasaOdBramkiDoPunktu"][k][i]][
                solution["zeroTrasaOdBramkiDoPunktu"][k][i + 1]] == 0:
                wynik += 43243623400000

    # Constraint 14
    for i in range(iloscTur):
        if solution["zeroTrasaOdBramkiDoPunktu"][i][solution["zeroOstatniIndeksTrasyOdBramki"][i]] != indeksBramki:
            wynik += 432423

    # Constraint 15
    for i in range(iloscTur):
        for j in range(dlugoscTrasy):
            if solution["zeroTrasaOdBramkiDoPunktuPoWyzerowaniu"][i][j] != solution["zeroIsZeroBramka"][i][j] * \
                    solution["zeroTrasaOdBramkiDoPunktu"][i][j]:
                wynik += 3231231

    # Constraint 16
    for i in range(iloscTur):
        if solution["jedenTrasaOdBramkiDoPunktu"][i][0] != solution["trasaWTurze"][i][solution["ostatniIndeksTrasyWTurze"][i]]:
            wynik += 23123
    # Constraint 17
    for k in range(iloscTur):
        for i in range(dlugoscTrasy-1):
            if dostepneRuchy[solution["jedenTrasaOdBramkiDoPunktu"][k][i]][
                solution["jedenTrasaOdBramkiDoPunktu"][k][i + 1]] == 0:
                wynik += 43243623400000

    # Constraint 18
    for i in range(iloscTur):
        if solution["jedenTrasaOdBramkiDoPunktu"][i][solution["jedenOstatniIndeksTrasyOdBramki"][i]] != indeksBramkiPrzeciwnika:
            wynik += 231231

    # Constraint 19
    for i in range(iloscTur):
        for j in range(dlugoscTrasy):
            if solution["jedenTrasaOdBramkiDoPunktuPoWyzerowaniu"][i][j] != solution["jedenIsZeroBramkaPrzeciwnik"][i][
                j] * solution["jedenTrasaOdBramkiDoPunktu"][i][j]:
                wynik += 231231

    for i in range(iloscTur):
        if solution["ostatniIndeksTrasyWTurze"][i] <= 0:
            wynik += 321312

    # Constraint 2
    for i in range(iloscTur):
        if solution["ostatniIndeksTrasyWTurze"][i] > dlugoscTrasy:
            wynik += 31231231

    # Constraint 3
    for i in range(iloscTur):
        if solution["zeroOstatniIndeksTrasyOdBramki"][i] > dlugoscTrasy:
            wynik += 5342342

    # Constraint 4
    for i in range(iloscTur):
        if solution["jedenOstatniIndeksTrasyOdBramki"][i] > dlugoscTrasy:
            wynik += 4342342

    # Constraint 5
    for i in range(iloscTur):
        for j in range(dlugoscTrasy):
            if solution["isZero"][i][j] != ((i <= solution["ostatniaTura"]) and (j <= solution["ostatniIndeksTrasyWTurze"][i])):
                wynik += 342342

    # Constraint 6
    for i in range(iloscTur):
        for j in range(dlugoscTrasy):
            if solution["zeroIsZeroBramka"][i][j] != (
                    solution["czyjaTura"][i] == 0 and (j <= solution["zeroOstatniIndeksTrasyOdBramki"][i])):
                wynik += 43423

    # Constraint 7
    for i in range(iloscTur):
        for j in range(dlugoscTrasy):
            if solution["jedenIsZeroBramkaPrzeciwnik"][i][j] != (
                    solution["czyjaTura"][i] == 1 and (j <= solution["jedenOstatniIndeksTrasyOdBramki"][i])):
                wynik += 4342632



    return wynik;




def generate_initial_solution():

    calaTrasaWMacierzy = [[random.randint(0, 1) for j in range(25)] for i in range(25)]

    # Generate initial solution for calaTrasaWMacierzyBramkaZero
    calaTrasaWMacierzyBramkaZero = [[[random.randint(0, 1) for j in range(25)] for i in range(25)] for k in
                                    range(iloscTur )]

    # Generate initial solution for calaTrasaWMacierzyBramkaJeden
    calaTrasaWMacierzyBramkaJeden = [[[random.randint(0, 1) for j in range(25)] for i in range(25)] for k in
                                     range(iloscTur )]

    # Generate initial solution for zeroTrasaOdBramkiDoPunktu
    zeroTrasaOdBramkiDoPunktu = [[random.randint(0, 24) for j in range(dlugoscTrasy)] for i in range(iloscTur)]

    # Generate initial solution for zeroTrasaOdBramkiDoPunktuPoWyzerowaniu
    zeroTrasaOdBramkiDoPunktuPoWyzerowaniu = [[random.randint(0, 24) for j in range(dlugoscTrasy)] for i in
                                              range(iloscTur )]

    # Generate initial solution for zeroOstatniIndeksTrasyOdBramki
    zeroOstatniIndeksTrasyOdBramki = [random.randint(0, dlugoscTrasy-1) for i in range(iloscTur )]

    # Generate initial solution for zeroOstatniIndeksTrasyOdBramkiPoUwzglednieniuTur
    zeroOstatniIndeksTrasyOdBramkiPoUwzglednieniuTur = [random.randint(0, dlugoscTrasy-1) for i in range(iloscTur)]

    # Generate initial solution for zeroIsZeroBramka
    zeroIsZeroBramka = [[random.randint(0, 1) for j in range(dlugoscTrasy)] for i in range(iloscTur )]

    # Generate initial solution for jedenTrasaOdBramkiDoPunktu
    jedenTrasaOdBramkiDoPunktu = [[random.randint(0, 24) for j in range(dlugoscTrasy)] for i in range(iloscTur)]

    # Generate initial solution for jedenTrasaOdBramkiDoPunktuPoWyzerowaniu
    jedenTrasaOdBramkiDoPunktuPoWyzerowaniu = [[random.randint(0, 24) for j in range(dlugoscTrasy)] for i in
                                               range(iloscTur)]

    # Generate initial solution for jedenOstatniIndeksTrasyOdBramki
    jedenOstatniIndeksTrasyOdBramki = [random.randint(0, dlugoscTrasy-1) for i in range(iloscTur)]

    # Generate initial solution for jedenOstatniIndeksTrasyOdBramkiPoUwzglednieniuTur
    jedenOstatniIndeksTrasyOdBramkiPoUwzglednieniuTur = [random.randint(0, dlugoscTrasy-1) for i in range(iloscTur )]

    # Generate initial solution for jedenIsZeroBramkaPrzeciwnik
    jedenIsZeroBramkaPrzeciwnik = [[random.randint(0, 1) for j in range(dlugoscTrasy)] for i in range(iloscTur )]

    # Generate initial solution for trasaWTurzePoWyzerowaniu
    trasaWTurzePoWyzerowaniu = [[random.randint(0, 24) for j in range(dlugoscTrasy)] for i in range(iloscTur )]

    # Generate initial solution for trasaWTurze
    trasaWTurze = [[random.randint(0, 24) for j in range(dlugoscTrasy)] for i in range(iloscTur)]

    # Generate initial solution for ostatniIndeksTrasyWTurze
    ostatniIndeksTrasyWTurze = [random.randint(1, dlugoscTrasy-1) for i in range(iloscTur )]

    # Generate initial solution for ostatniaTura
    ostatniaTura = random.randint(0, iloscTur)

    # Generate initial solution for isZero
    isZero = [[random.randint(0, 1) for j in range(dlugoscTrasy)] for i in range(iloscTur )]

    # Generate initial solution for odwiedzoneWierzcholkiNaPrzestrzeniTur
    odwiedzoneWierzcholkiNaPrzestrzeniTur = [[random.randint(0, 1) for j in range(25)] for i in range(iloscTur)]
    print(odwiedzoneWierzcholkiNaPrzestrzeniTur)

    # Generate initial solution for iloscOdwiedzinDanegoWierzcholkaWDanejTurze
    iloscOdwiedzinDanegoWierzcholkaWDanejTurze = [[random.randint(0, 24) for j in range(25)] for i in range(iloscTur)]
    # Generate initial solution for czyjaTura
    czyjaTura = [random.randint(0, 1) for i in range(iloscTur )]

    # Generate initial solution for temp
    temp = [[random.randint(0, 1) for j in range(dlugoscTrasy)] for i in range(iloscTur )]

    # Store the initial solution in a dictionary
    solution = {
        "calaTrasaWMacierzy": calaTrasaWMacierzy,
        "calaTrasaWMacierzyBramkaZero": calaTrasaWMacierzyBramkaZero,
        "calaTrasaWMacierzyBramkaJeden": calaTrasaWMacierzyBramkaJeden,
        "zeroTrasaOdBramkiDoPunktu": zeroTrasaOdBramkiDoPunktu,
        "zeroTrasaOdBramkiDoPunktuPoWyzerowaniu": zeroTrasaOdBramkiDoPunktuPoWyzerowaniu,
        "zeroOstatniIndeksTrasyOdBramki": zeroOstatniIndeksTrasyOdBramki,
        "zeroOstatniIndeksTrasyOdBramkiPoUwzglednieniuTur": zeroOstatniIndeksTrasyOdBramkiPoUwzglednieniuTur,
        "zeroIsZeroBramka": zeroIsZeroBramka,
        "jedenTrasaOdBramkiDoPunktu": jedenTrasaOdBramkiDoPunktu,
        "jedenTrasaOdBramkiDoPunktuPoWyzerowaniu": jedenTrasaOdBramkiDoPunktuPoWyzerowaniu,
        "jedenOstatniIndeksTrasyOdBramki": jedenOstatniIndeksTrasyOdBramki,
        "jedenOstatniIndeksTrasyOdBramkiPoUwzglednieniuTur": jedenOstatniIndeksTrasyOdBramkiPoUwzglednieniuTur,
        "jedenIsZeroBramkaPrzeciwnik": jedenIsZeroBramkaPrzeciwnik,
        "trasaWTurzePoWyzerowaniu": trasaWTurzePoWyzerowaniu,
        "trasaWTurze": trasaWTurze,
        "ostatniIndeksTrasyWTurze": ostatniIndeksTrasyWTurze,
        "ostatniaTura": ostatniaTura,
        "isZero": isZero,
        "odwiedzoneWierzcholkiNaPrzestrzeniTur": odwiedzoneWierzcholkiNaPrzestrzeniTur,
        "iloscOdwiedzinDanegoWierzcholkaWDanejTurze": iloscOdwiedzinDanegoWierzcholkaWDanejTurze,
        "czyjaTura": czyjaTura,
        "temp": temp
    }
    return solution

# Generate a neighboring solution by perturbing the current solution

def generate_neighboring_solution(solution):
    new_solution = copy.deepcopy(solution)

    # Randomly select a key from the solution dictionary
    random_key = random.choice(list(new_solution.keys()))

    # Generate a new value for the selected key
    if random_key == "calaTrasaWMacierzy":
        new_value = [[random.randint(0, 1) for j in range(25)] for i in range(25)]
    elif random_key == "calaTrasaWMacierzyBramkaZero":
        new_value = [[[random.randint(0, 1) for j in range(25)] for i in range(25)] for k in range(iloscTur )]
    elif random_key == "calaTrasaWMacierzyBramkaJeden":
        new_value = [[[random.randint(0, 1) for j in range(25)] for i in range(25)] for k in range(iloscTur)]
    elif random_key == "zeroTrasaOdBramkiDoPunktu":
        new_value = [[random.randint(0, 24) for j in range(dlugoscTrasy)] for i in range(iloscTur )]
    elif random_key == "zeroTrasaOdBramkiDoPunktuPoWyzerowaniu":
        new_value = [[random.randint(0, 24) for j in range(dlugoscTrasy)] for i in range(iloscTur)]
    elif random_key == "zeroOstatniIndeksTrasyOdBramki":
        new_value = [random.randint(0, dlugoscTrasy-1) for i in range(iloscTur )]
    elif random_key == "zeroOstatniIndeksTrasyOdBramkiPoUwzglednieniuTur":
        new_value = [random.randint(0, dlugoscTrasy-1) for i in range(iloscTur)]
    elif random_key == "zeroIsZeroBramka":
        new_value = [[random.randint(0, 1) for j in range(dlugoscTrasy)] for i in range(iloscTur )]
    elif random_key == "jedenTrasaOdBramkiDoPunktu":
        new_value = [[random.randint(0, 24) for j in range(dlugoscTrasy)] for i in range(iloscTur )]
    elif random_key == "jedenTrasaOdBramkiDoPunktuPoWyzerowaniu":
        new_value = [[random.randint(0, 24) for j in range(dlugoscTrasy)] for i in range(iloscTur )]
    elif random_key == "jedenOstatniIndeksTrasyOdBramki":
        new_value = [random.randint(0, dlugoscTrasy-1) for i in range(iloscTur )]
    elif random_key == "jedenOstatniIndeksTrasyOdBramkiPoUwzglednieniuTur":
        new_value = [random.randint(0, dlugoscTrasy-1) for i in range(iloscTur )]
    elif random_key == "jedenIsZeroBramkaPrzeciwnik":
        new_value = [[random.randint(0, 1) for j in range(dlugoscTrasy)] for i in range(iloscTur )]
    elif random_key == "trasaWTurzePoWyzerowaniu":
        new_value = [[random.randint(0, 24) for j in range(dlugoscTrasy)] for i in range(iloscTur )]
    elif random_key == "trasaWTurze":
        new_value = [[random.randint(0, 24) for j in range(dlugoscTrasy)] for i in range(iloscTur )]
    elif random_key == "ostatniIndeksTrasyWTurze":
        new_value = [random.randint(0, dlugoscTrasy-1) for i in range(iloscTur )]
    elif random_key == "ostatniaTura":
        new_value = random.randint(0, iloscTur)
    elif random_key == "isZero":
        new_value = [[random.randint(0, 1) for j in range(dlugoscTrasy)] for i in range(iloscTur )]
    elif random_key == "odwiedzoneWierzcholkiNaPrzestrzeniTur":
        new_value = [[random.randint(0, 1) for j in range(25)] for i in range(iloscTur )]
    elif random_key == "iloscOdwiedzinDanegoWierzcholkaWDanejTurze":
        new_value = [[random.randint(0, 10) for j in range(25)] for i in range(iloscTur )]
    elif random_key == "czyjaTura":
        new_value = [random.randint(0, 1) for i in range(iloscTur )]
    elif random_key == "temp":
        new_value = [[random.randint(0, 1) for j in range(dlugoscTrasy)] for i in range(iloscTur )]
    new_solution[random_key] = new_value

    return new_solution
# Calculate the acceptance probability based on the current and neighboring solutions
def acceptance_probability(current_evaluation, neighboring_evaluation, temperature):
    if neighboring_evaluation < current_evaluation:
        return 1.0
    return math.exp((current_evaluation - neighboring_evaluation) / temperature)

# Simulated Annealing algorithm
def simulated_annealing():
    # Initialize the current solution and temperature
    current_solution = generate_initial_solution()
    print(current_solution)
    current_evaluation = objective_function(current_solution)
    print(current_evaluation)

    temperature = initial_temperature

    # Iterate until the termination condition is met
    for _ in range(num_iterations):
        # Generate a neighboring solution
        neighboring_solution = generate_neighboring_solution(current_solution)
        neighboring_evaluation = objective_function(neighboring_solution)
        print(neighboring_evaluation)
        # Determine whether to accept the neighboring solution
        acceptance_prob = acceptance_probability(current_evaluation, neighboring_evaluation, temperature)
        if random.random() < acceptance_prob:
            current_solution = neighboring_solution
            current_evaluation = neighboring_evaluation

        # Update the temperature
        temperature *= cooling_rate

    return current_solution

# Run the simulated annealing algorithm and get the best solution
best_solution = simulated_annealing()

# Print the best solution and its evaluation
print("Best Solution:", best_solution["trasaWTurzePoWyzerowaniu"])
print("Best Evaluation:", objective_function(best_solution))
