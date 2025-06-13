#lista6

import unicodedata


#usuwanie polskich znaków
def usun_polskie_znaki(tekst):
    return ''.join(
        c for c in unicodedata.normalize('NFD', tekst)
        if unicodedata.category(c) != 'Mn' )

#c


# przykładowy słownik 100 słów
# różne długości słów, polskie rzeczowniki i produkty

slownik = [
    "mama", "tata", "dom", "kot", "pies", "nawa", "lampa", "krzesło",
    "książka", "komputer", "telefon", "szklanka", "okno", "drzwi", "samochód",
    "rower", "kwiat", "ławka", "ściana", "dach", "lato", "zima", "wiosna", "jesień",
    "śnieg", "deszcz", "słońce", "księżyc", "gwiazda", "morze", "góry", "las",
    "rzeka", "ptak", "ryba", "żaba", "wąż", "motyl", "pszczoła", "mrówka", "mysz",
    "krowa", "koń", "świnia", "kura", "kogut", "indyk", "kaczka", "gęś", "jabłko",
    "gruszka", "śliwka", "truskawka", "malina", "porzeczka", "winogrono", "banan",
    "pomarańcza", "cytryna", "mandarynka", "arbuz", "ananas", "marchewka", "ziemniak",
    "pomidor", "ogórek", "cebula", "czosnek", "papryka", "sałata", "kapusta", "kalafior",
    "brokuł", "dynia", "bakłażan", "szpinak", "rzodkiewka", "fasola", "groch", "soczewica",
    "ryż", "makaron", "chleb", "bułka", "ser", "mleko", "masło", "jogurt", "kefir",
    "szynka", "kiełbasa", "jajko", "sok", "woda", "herbata", "kawa", "piwo", "wino" ]

#zadanie 2
#a

# częstości liter dla 3 języków (procentowy udział liter)
czestosci_w_jezykach = {
    'polish': {
        'a': 8.91, 'b': 1.47, 'c': 3.96, 'd': 3.25, 'e': 7.66,
        'f': 0.30, 'g': 1.42, 'h': 1.08, 'i': 8.21, 'j': 2.28,
        'k': 3.51, 'l': 2.10, 'm': 2.80, 'n': 5.52, 'o': 7.75,
        'p': 3.13, 'q': 0.14, 'r': 4.69, 's': 4.32, 't': 3.98,
        'u': 2.50, 'v': 0.04, 'w': 4.65, 'x': 0.02, 'y': 3.76, 'z': 5.64
    },
    'english': {
        'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253, 'e': 12.702,
        'f': 2.228, 'g': 2.015, 'h': 6.094, 'i': 6.966, 'j': 0.153,
        'k': 0.772, 'l': 4.025, 'm': 2.406, 'n': 6.749, 'o': 7.507,
        'p': 1.929, 'q': 0.095, 'r': 5.987, 's': 6.327, 't': 9.056,
        'u': 2.758, 'v': 0.978, 'w': 2.360, 'x': 0.150, 'y': 1.974, 'z': 0.074
    },
    'german': {
        'a': 6.51, 'b': 1.89, 'c': 3.06, 'd': 5.08, 'e': 17.40,
        'f': 1.66, 'g': 3.01, 'h': 4.76, 'i': 7.55, 'j': 0.27,
        'k': 1.21, 'l': 3.44, 'm': 2.53, 'n': 9.78, 'o': 2.51,
        'p': 0.79, 'q': 0.02, 'r': 7.00, 's': 7.27, 't': 6.15,
        'u': 4.35, 'v': 0.67, 'w': 1.89, 'x': 0.03, 'y': 0.04, 'z': 1.13
    }
}

samogloski = {'a', 'e', 'i', 'o', 'u', 'y'}  # zestaw samogłosek

#b

# funkcja zamienia tekst na procentowy rozkład liter
def tekst_na_czestosc(tekst):

    #zamieniana z polskich znaków oraz na litery małe
    tekst = usun_polskie_znaki(tekst).lower()

    #usuwamy wszystko, co nie jest literą (np. cyfry, interpunkcja)
    tylko_litery = ""
    for znak in tekst:
        if znak.isalpha(): #tylko litery
            tylko_litery += znak


    #jeśli tekst pusty lub bez liter -> pusty wynik
    liczba_liter = len(tylko_litery)
    if liczba_liter == 0:
        return {}

    #liczenie, ile razy występuje każda litera
    licznik = {}
    for litera in tylko_litery:
        if litera in licznik:
            licznik[litera] += 1
        else:
            licznik[litera] = 1

    #oblicza procentowy udział każdej litery

    #czestosc = ilosc litery/ wszystkie  * 100
    czestosci = {}
    for litera in licznik:
        czestosci[litera] = (licznik[litera] / liczba_liter) * 100
    print(licznik)
    return czestosci

# Oblicza dystans między tekstem a profilem języka
# Używamy odległości Manhattan: suma bezwzględnych różnic procentowych dla każdej litery
def porownaj_czestosc(tekst, czestosci_jezyka):
    roznica = 0

    for litera in czestosci_jezyka:
        if litera in tekst:
            roznica += abs(tekst[litera] - czestosci_jezyka[litera])
        else:
            roznica += abs(0 - czestosci_jezyka[litera])

    return roznica


# Główna funkcja – rozpoznaje język tekstu na podstawie rozkładu liter
def wykryj_jezyk(tekst):

    czestosc = tekst_na_czestosc(tekst)
    najmniejszy = 9999999
    jezyk_najlepszy = ""

    for jezyk in czestosci_w_jezykach:

        roznica = porownaj_czestosc(czestosc, czestosci_w_jezykach[jezyk])
        if roznica < najmniejszy:
            najmniejszy = roznica
            jezyk_najlepszy = jezyk

    return (jezyk_najlepszy)
    #.capitalize()
#c

# funkcja uproszczona - zlicza tylko samogłoski i spółgłoski
def uproszczona_czestosc(tekst):
    tekst = ''.join(c for c in usun_polskie_znaki(tekst).lower() if c.isalpha())
    #male litery,bez polskich znaków

    ilosc_liter_wyrazie = len(tekst) # or 1

    liczba_samoglosek = sum(1 for c in tekst if c in samogloski)

    return (liczba_samoglosek / ilosc_liter_wyrazie * 100, (ilosc_liter_wyrazie - liczba_samoglosek) / ilosc_liter_wyrazie * 100)


# procentowe udziały samogłosek i spółgłosek dla języków
jezyk_uproszczony = {
    'polish': (38.5, 61.5),
    'english': (39.9, 60.1),
    'german': (37.2, 62.8)
}


# funkcja wykrywa język używając tylko samogłosek/spółgłosek
def wykryj_jezyk_uproszczony(tekst):

    najlepszy_jezyk = ''
    min_roznica = 9999
    samogloski_proc, spolgloski_proc = uproszczona_czestosc(tekst)

    for jezyk in jezyk_uproszczony:
        s, sp = jezyk_uproszczony[jezyk]
        #s- samogloski
        #sp spolgloski

        roznica = abs(samogloski_proc - s) + abs(spolgloski_proc - sp)

        if roznica < min_roznica:
            min_roznica = roznica
            najlepszy_jezyk = jezyk

    return najlepszy_jezyk.capitalize()



if __name__ == "__main__":
    print("\nZadanie_2b: ")
    tekst = "Ala ma kota"
    print(tekst)
    print("Wykryty język:", wykryj_jezyk(tekst))  # Polski

    print("\nZadanie_2c: ")
    print("Wykryty język (uproszczony):", wykryj_jezyk_uproszczony(tekst))  # Polski
