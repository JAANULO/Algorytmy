# lista6

from collections import defaultdict
import unicodedata
import random

# Funkcja usuwająca polskie znaki diakrytyczne
def usun_polskie_znaki(tekst):
    return ''.join(
        c for c in unicodedata.normalize('NFD', tekst)
        if unicodedata.category(c) != 'Mn'
    )

# Zadanie 1a: Odległość Hamminga
def Hamminga_odleglosc(s1, s2):
    if len(s1) != len(s2):
        raise ValueError("Ciągi muszą być tej samej długości")
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

# Zadanie 1b: Modyfikowana odległość Hamminga z uwzględnieniem klawiatury
def modyfikowana_Hamminga(s1, s2):
    if len(s1) != len(s2):
        raise ValueError("Ciągi muszą być tej samej długości")

    # Rozszerzona mapa klawiatury QWERTY
    klawiatura = {
        'q': {'w', 'a', 's'}, 'w': {'q', 'e', 's', 'a'}, 'e': {'w', 'r', 'd', 's'},
        'r': {'e', 't', 'f', 'd'}, 't': {'r', 'y', 'g', 'f'}, 'y': {'t', 'u', 'h', 'g'},
        'u': {'y', 'i', 'j', 'h'}, 'i': {'u', 'o', 'k', 'j'}, 'o': {'i', 'p', 'l', 'k'},
        'p': {'o', 'l'}, 'a': {'q', 's', 'z', 'w'}, 's': {'a', 'w', 'd', 'x', 'z', 'e'},
        'd': {'s', 'e', 'f', 'c', 'x', 'r'}, 'f': {'d', 'r', 'g', 'v', 'c', 't'},
        'g': {'f', 't', 'h', 'b', 'v', 'y'}, 'h': {'g', 'y', 'j', 'n', 'b', 'u'},
        'j': {'h', 'u', 'k', 'm', 'n', 'i'}, 'k': {'j', 'i', 'l', 'm', 'o'},
        'l': {'k', 'o', 'p'}, 'z': {'a', 'x'}, 'x': {'z', 's', 'c'},
        'c': {'x', 'd', 'v'}, 'v': {'c', 'f', 'b'}, 'b': {'v', 'g', 'n'},
        'n': {'b', 'h', 'm'}, 'm': {'n', 'j'}
    }

    odleglosc = 0
    for c1, c2 in zip(s1.lower(), s2.lower()):
        if c1 == c2:
            continue

        # Obsługa przypadkowego wciśnięcia Alt (losowy koszt 1-2)
        if random.random() < 0.1:  # 10% szans na przypadkowe wciśnięcie Alt
            odleglosc += random.randint(1, 2)
            continue

        if c1 in klawiatura and c2 in klawiatura[c1]:
            odleglosc += 1
        else:
            odleglosc += 2

    return odleglosc

# Zadanie 1c: Słownik i wyszukiwanie podobnych słów
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
    "szynka", "kiełbasa", "jajko", "sok", "woda", "herbata", "kawa", "piwo", "wino"
]

def znajdz_podobne_slowa(slowo_wejsciowe):
    # Sprawdź czy słowo istnieje w słowniku (bez ogonków)
    slowo_bez_ogonkow = usun_polskie_znaki(slowo_wejsciowe).lower()
    for slowo in slownik:
        if usun_polskie_znaki(slowo).lower() == slowo_bez_ogonkow:
            return "OK"

    # Oblicz odległość Levenshteina do wszystkich słów
    podobne = []
    for slowo in slownik:
        s1 = usun_polskie_znaki(slowo_wejsciowe).lower()
        s2 = usun_polskie_znaki(slowo).lower()
        odleglosc = Levenshteina_odleglosc(s1, s2)
        podobne.append((odleglosc, slowo))

    # Posortuj i zwróć 3 najbardziej podobne
    podobne.sort()
    return [slowo for _, slowo in podobne[:3]]

# Zadanie 2: Częstość znaków
czestosci = {
    'polski': {
        'a': 8.91, 'b': 1.47, 'c': 3.96, 'd': 3.25, 'e': 7.66,
        'f': 0.30, 'g': 1.42, 'h': 1.08, 'i': 8.21, 'j': 2.28,
        'k': 3.51, 'l': 2.10, 'm': 2.80, 'n': 5.52, 'o': 7.75,
        'p': 3.13, 'q': 0.14, 'r': 4.69, 's': 4.32, 't': 3.98,
        'u': 2.50, 'v': 0.04, 'w': 4.65, 'x': 0.02, 'y': 3.76, 'z': 5.64
    },
    'angielski': {
        'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253, 'e': 12.702,
        'f': 2.228, 'g': 2.015, 'h': 6.094, 'i': 6.966, 'j': 0.153,
        'k': 0.772, 'l': 4.025, 'm': 2.406, 'n': 6.749, 'o': 7.507,
        'p': 1.929, 'q': 0.095, 'r': 5.987, 's': 6.327, 't': 9.056,
        'u': 2.758, 'v': 0.978, 'w': 2.360, 'x': 0.150, 'y': 1.974, 'z': 0.074
    },
    'niemiecki': {
        'a': 6.51, 'b': 1.89, 'c': 3.06, 'd': 5.08, 'e': 17.40,
        'f': 1.66, 'g': 3.01, 'h': 4.76, 'i': 7.55, 'j': 0.27,
        'k': 1.21, 'l': 3.44, 'm': 2.53, 'n': 9.78, 'o': 2.51,
        'p': 0.79, 'q': 0.02, 'r': 7.00, 's': 7.27, 't': 6.15,
        'u': 4.35, 'v': 0.67, 'w': 1.89, 'x': 0.03, 'y': 0.04, 'z': 1.13
    }
}

samogloski = {'a', 'e', 'i', 'o', 'u', 'y'}

def tekst_na_czestosc(tekst):
    tekst = usun_polskie_znaki(tekst).lower()
    tekst = ''.join(c for c in tekst if c.isalpha())
    lacznie = len(tekst) or 1
    czestosci_dict = defaultdict(float)
    for c in tekst:
        czestosci_dict[c] += 1
    for c in czestosci_dict:
        czestosci_dict[c] = (czestosci_dict[c] / lacznie) * 100
    return dict(czestosci_dict)

def porownaj_czestosc(czestosci_tekstu, czestosci_jezyk):
    odleglosc = 0
    wszystkie_litery = set(czestosci_tekstu.keys()) | set(czestosci_jezyk.keys())
    for litera in wszystkie_litery:
        odleglosc += abs(czestosci_tekstu.get(litera, 0) - czestosci_jezyk.get(litera, 0))
    return odleglosc

def wykryj_jezyk(tekst):
    czestosci_tekstu = tekst_na_czestosc(tekst)
    min_odleglosc = float('inf')
    najlepszy_jezyk = ''
    for jezyk, czest in czestosci.items():
        odleglosc = porownaj_czestosc(czestosci_tekstu, czest)
        if odleglosc < min_odleglosc:
            min_odleglosc = odleglosc
            najlepszy_jezyk = jezyk
    return najlepszy_jezyk.capitalize()

# Zadanie 2c: Uproszczona analiza
def uproszczona_czestosc(tekst):
    tekst = usun_polskie_znaki(tekst).lower()
    tekst = ''.join(c for c in tekst if c.isalpha())
    lacznie = len(tekst) or 1
    liczba_samoglosek = sum(1 for c in tekst if c in samogloski)
    return (liczba_samoglosek / lacznie * 100, (lacznie - liczba_samoglosek) / lacznie * 100)

jezyk_uproszczony = {
    'polski': (38.5, 61.5),
    'angielski': (39.9, 60.1),
    'niemiecki': (37.2, 62.8)
}

def wykryj_jezyk_uproszczony(tekst):
    samogloski_proc, spolgloski_proc = uproszczona_czestosc(tekst)
    min_odleglosc = float('inf')
    najlepszy_jezyk = ''
    for jezyk, (s, sp) in jezyk_uproszczony.items():
        odleglosc = abs(samogloski_proc - s) + abs(spolgloski_proc - sp)
        if odleglosc < min_odleglosc:
            min_odleglosc = odleglosc
            najlepszy_jezyk = jezyk
    return najlepszy_jezyk.capitalize()

# Zadanie 3: Odległości edycyjne
# Złożoność obliczeniowa: O(m*n) dla wszystkich funkcji

# Zadanie 3a: Najdłuższy wspólny podciąg ciągły
def najdluzszy_wspolny_podciag_ciagly(s1, s2):
    m, n = len(s1), len(s2)
    # DP: O(m*n) pamięci i czasu
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    max_dlugosc = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                max_dlugosc = max(max_dlugosc, dp[i][j])
            else:
                dp[i][j] = 0
    return max_dlugosc

# Zadanie 3b: Najdłuższy wspólny podciąg (z przerwami)
def najdluzszy_wspolny_podciag(s1, s2):
    m, n = len(s1), len(s2)
    # DP: O(m*n) pamięci i czasu
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]

# Zadanie 3d: Odległość Levenshteina
def Levenshteina_odleglosc(s1, s2):
    m, n = len(s1), len(s2)
    # DP: O(m*n) pamięci i czasu
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            koszt = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,      # Usunięcie
                dp[i][j - 1] + 1,      # Wstawienie
                dp[i - 1][j - 1] + koszt  # Zamiana
            )
    return dp[m][n]

# Testowanie
if __name__ == "__main__":
    print("Zadanie_1a: ")
    s1="mama"
    s2="nawa"
    print(s1, s2)
    print("Hamminga odległość:", Hamminga_odleglosc(s1, s2))  # 3


    print("\nZadanie 1b: ")
    print("Modyfikowana Hamminga:", modyfikowana_Hamminga("mama", "nawa"))  # 3

    print("\nZadanie 1c: ")
    print("Podobne słowa:", znajdz_podobne_slowa("maaa"))   # ['mama', 'tata', 'nawa']
    print("Podobne słowa:", znajdz_podobne_slowa("płaszczkaa"))  # ['płaszczka' jeśli w słowniku]

    print("\nZadanie_2b: ")
    tekst = "Litwo ojczyzno moja ty jesteś jak zdrowie"
    print("Wykryty język:", wykryj_jezyk(tekst))  # Polski
    print("Wykryty język (uproszczony):", wykryj_jezyk_uproszczony(tekst))  # Polski

    print("\nZadanie_3a: ")
    print("Najdłuższy wspólny podciąg ciągły:", najdluzszy_wspolny_podciag_ciagly("konwalia", "zawalina"))  # 4

    print("\nZadanie_3b: ")
    print("Najdłuższy wspólny podciąg:", najdluzszy_wspolny_podciag("ApqBCrDeFt", "tABuCoDewxFyz"))  # 6

    print("\nZadanie_3d: ")
    print("Levenshteina odległość:", Levenshteina_odleglosc("kitten", "sitting"))  # 3