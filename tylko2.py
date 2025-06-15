#lista6

import unicodedata

#usuwanie polskich znaków
def usun_polskie_znaki(tekst):
    return ''.join(
        c for c in unicodedata.normalize('NFD', tekst)
        if unicodedata.category(c) != 'Mn' )


#zadanie 1
#a

#funkcja obliczająca klasyczną odległość Hamminga
#liczy ile znaków różni się między dwoma ciągami tej samej długości
def Hamminga_odleglosc(s1, s2):
    if len(s1) != len(s2):  # ciągi muszą być tej samej długości
        raise ValueError("Ciągi muszą być tej samej długości")


    odleglosc = 0
    for i in range(len(s1)): # zliczamy ile razy znaki na tych samych pozycjach się różnią
        if s1[i] != s2[i]:
            odleglosc += 1
    return odleglosc


#b

#funkcja modyfikująca odległość Hamminga z uwzględnieniem sąsiedztwa klawiatury
#sąsiadujące litery mają wagę 1, inne 2
def modyfikowana_Hamminga(s1, s2):
    if len(s1) != len(s2): # ciągi muszą być tej samej długości
        raise ValueError("Ciągi muszą być tej samej długości")

    klawiatura = { #litery obok siebie
        'q': {'w', 'a'}, 'w': {'q', 'e', 's'}, 'e': {'w', 'r', 'd'},
        'r': {'e', 't', 'f'}, 't': {'r', 'y', 'g'}, 'y': {'t', 'u', 'h'},
        'u': {'y', 'i', 'j'}, 'i': {'u', 'o', 'k'}, 'o': {'i', 'p', 'l'},
        'p': {'o'},
        'a': {'q', 's', 'z'}, 's': {'a', 'w', 'd', 'x'},
        'd': {'s', 'e', 'f', 'c'}, 'f': {'d', 'r', 'g', 'v'},
        'g': {'f', 't', 'h', 'b'}, 'h': {'g', 'y', 'j', 'n'},
        'j': {'h', 'u', 'k', 'm'}, 'k': {'j', 'i', 'l'},
        'l': {'k', 'o'},
        'z': {'a', 'x'}, 'x': {'z', 's', 'c'},
        'c': {'x', 'd', 'v'}, 'v': {'c', 'f', 'b'}, 'b': {'v', 'g', 'n'},
        'n': {'b', 'h', 'm'}, 'm': {'n', 'j'} }

    s1 = s1.lower()
    s2 = s2.lower()
    odleglosc = 0

    for i in range(len(s1)):

        if s1[i] == s2[i]:
            continue

        if s2[i] in klawiatura.get(s1[i], set()):
            odleglosc += 1
        else:
            odleglosc += 2

    return odleglosc


#c

#przykładowy słownik 100 słów
#różne długości słów, polskie rzeczowniki i produkty

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


#funkcja znajduje najbardziej podobne słowa ze słownika na podstawie odległości Hamminga (zmodyfikowanej)
def znajdz_podobne_slowa(slowo_wejsciowe):

    slowo_norm = usun_polskie_znaki(slowo_wejsciowe).lower()

    #czy jest dokładnie w słowniku
    for slowo in slownik:
        if usun_polskie_znaki(slowo).lower() == slowo_norm:
            return "OK"

    podobne = []
    for slowo in slownik:
        slowo_slownikowe = usun_polskie_znaki(slowo).lower()

        if len(slowo_norm) != len(slowo_slownikowe):
            continue  # tylko słowa tej samej długości
        odl = Hamminga_odleglosc(slowo_norm, slowo_slownikowe)

        podobne.append((odl, slowo))

    podobne.sort()

    if podobne: #jesli lista nie jest pusta
        najlepsze = []
        for _, slowo in podobne[:3]:
            najlepsze.append(slowo)
        return najlepsze
    else:
        return ["Brak podobnych słów"]

if __name__ == "__main__":
    print("Zadanie_1a: ")
    s1 = "mama"
    s2 = "nawa"
    print(s1, s2)
    print("Hamminga odległość:", Hamminga_odleglosc(s1, s2))  # 3

    print("\nZadanie 1b: ")
    print(s1, s2)
    print("Modyfikowana Hamminga:", modyfikowana_Hamminga("mama", "nawa"))  # 3

    print("\nZadanie 1c: ")
    slowo_wejsciowe="mamaa"
    print(slowo_wejsciowe)
    print("Podobne słowa:", znajdz_podobne_slowa(slowo_wejsciowe))  # ['mama', 'tata', 'nawa']
