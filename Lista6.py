#lista6

from collections import defaultdict


#zadanie 1
#a


# funkcja obliczająca klasyczną odległość Hamminga
# liczy ile znaków różni się między dwoma ciągami tej samej długości
def hamming_distance(s1, s2):
    if len(s1) != len(s2):  # ciągi muszą być tej samej długości
        raise ValueError("Ciągi muszą być tej samej długości")
    # zliczamy ile razy znaki na tych samych pozycjach się różnią
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))


#b


# funkcja modyfikująca odległość Hamminga z uwzględnieniem sąsiedztwa klawiatury
# sąsiadujące litery mają wagę 1, inne 2
def modified_hamming(s1, s2):
    if len(s1) != len(s2):
        raise ValueError("Ciągi muszą być tej samej długości")

    # mapa sąsiedztwa klawiszy na klawiaturze QWERTY
    keyboard = {
        'q': {'w', 'a'}, 'w': {'q', 'e', 's'}, 'e': {'w', 'r', 'd'},
        'r': {'e', 't', 'f'}, 't': {'r', 'y', 'g'}, 'y': {'t', 'u', 'h'},
        'u': {'y', 'i', 'j'}, 'i': {'u', 'o', 'k'}, 'o': {'i', 'p', 'l'},
        'p': {'o'}, 'a': {'q', 's', 'z'}, 's': {'a', 'w', 'd', 'x'},
        'd': {'s', 'e', 'f', 'c'}, 'f': {'d', 'r', 'g', 'v'},
        'g': {'f', 't', 'h', 'b'}, 'h': {'g', 'y', 'j', 'n'},
        'j': {'h', 'u', 'k', 'm'}, 'k': {'j', 'i', 'l'},
        'l': {'k', 'o'}, 'z': {'a', 'x'}, 'x': {'z', 's', 'c'},
        'c': {'x', 'd', 'v'}, 'v': {'c', 'f', 'b'}, 'b': {'v', 'g', 'n'},
        'n': {'b', 'h', 'm'}, 'm': {'n', 'j'}
    }

    distance = 0
    # porównujemy znaki z małych liter
    for c1, c2 in zip(s1.lower(), s2.lower()):
        if c1 == c2:
            continue  # identyczne znaki nie zwiększają odległości
        if c2 in keyboard.get(c1, set()):
            distance += 1  # sąsiednie znaki
        else:
            distance += 2  # różne znaki
    return distance


#c


# przykładowy słownik 100 słów
# różne długości słów, polskie rzeczowniki i produkty
# (skrócony komentarz, pełna lista poniżej)

dictionary = [
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


# funkcja znajduje najbardziej podobne słowa ze słownika na podstawie odległości Hamminga (zmodyfikowanej)
def find_similar_words(input_word):
    if input_word in dictionary:
        return "OK"  # słowo istnieje w słowniku

    similar = []
    for word in dictionary:
        if len(word) == len(input_word):  # tylko słowa tej samej długości
            dist = modified_hamming(input_word, word)
            similar.append((dist, word))

    # sortujemy po odległości
    similar.sort()
    return [word for _, word in similar[:3]]  # zwracamy 3 najlepsze


#zadanie 2
#a

# częstości liter dla 3 języków (procentowy udział liter)
freq = {
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


vowels = {'a', 'e', 'i', 'o', 'u', 'y'}  # zestaw samogłosek



#b

# funkcja zamienia tekst na procentowy rozkład liter
def text_to_freq(text):
    text = ''.join([c.lower() for c in text if c.isalpha()])  # tylko litery, małe
    total = len(text) or 1  # zabezpieczenie przed 0
    freq_dict = defaultdict(float)
    for c in text:
        freq_dict[c] += 1
    for c in freq_dict:
        freq_dict[c] = (freq_dict[c] / total) * 100
    return freq_dict


# funkcja porównuje rozkład liter z językiem
# im mniejsza suma różnic, tym bliżej

def compare_freq(text_freq, lang_freq):
    distance = 0
    all_letters = set(text_freq.keys()).union(lang_freq.keys())
    for letter in all_letters:
        distance += abs(text_freq.get(letter, 0) - lang_freq.get(letter, 0))
    return distance


# funkcja rozpoznająca język na podstawie częstości liter
def detect_language(text):
    text_freq = text_to_freq(text)
    min_dist = float('inf')
    best_lang = ''
    for lang in freq:
        dist = compare_freq(text_freq, freq[lang])
        if dist < min_dist:
            min_dist = dist
            best_lang = lang
    return best_lang.capitalize()


#c

# funkcja uproszczona - zlicza tylko samogłoski i spółgłoski
def simplified_freq(text):
    text = ''.join([c.lower() for c in text if c.isalpha()])
    total = len(text) or 1
    vowels_count = sum(1 for c in text if c in vowels)
    return (vowels_count / total * 100, (total - vowels_count) / total * 100)


# procentowe udziały samogłosek i spółgłosek dla języków
lang_simplified = {
    'polish': (38.5, 61.5),
    'english': (39.9, 60.1),
    'german': (37.2, 62.8)
}


# funkcja wykrywa język używając tylko samogłosek/spółgłosek
def detect_language_simplified(text):
    text_vowels, text_consonants = simplified_freq(text)
    min_dist = float('inf')
    best_lang = ''
    for lang, (v, c) in lang_simplified.items():
        dist = abs(text_vowels - v) + abs(text_consonants - c)
        if dist < min_dist:
            min_dist = dist
            best_lang = lang
    return best_lang.capitalize()


#zadanie 3
#a

# najdłuższy wspólny podciąg bez przerw (substring)
def longest_common_substring(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    max_len = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                max_len = max(max_len, dp[i][j])
            else:
                dp[i][j] = 0
    return max_len


#b

# najdłuższy wspólny podciąg z przerwami (subsequence)
def longest_common_subsequence(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]


#d

# odległość Levenshteina – liczba operacji potrzebna do przekształcenia jednego ciągu w drugi
def levenshtein_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost
            )
    return dp[m][n]

if __name__ == "__main__":
    print("Zadanie_1a: ")
    print("Hamming:", hamming_distance("mama", "nawa"))  # wynik: 3
    print("\nZadanie 1b: ")
    print("Modified Hamming:", modified_hamming("mama", "nawa"))  # wynik: 3 lub inny, zależnie od mapy
    print("\nZadanie 1c: ")
    print("Podobne słowa:", find_similar_words("maaa"))  # np. ['mama', 'nawa', 'tata']

    print("\nZadanie_2b: ")
    tekst = "Litwo ojczyzno moja ty jesteś jak zdrowie"
    print("Język:", detect_language(tekst))  # Polish
    print("Język uproszczony:", detect_language_simplified(tekst))  # Polish

    print("\nZadanie_3a: ")
    print("LCSubstring:", longest_common_substring("konwalia", "zawalina"))  # 4
    print("\nZadanie_3b: ")
    print("LCS:", longest_common_subsequence("ApqBCrDeFt", "tABuCoDewxFyz"))  # 6
    print("\nZadanie_3d: ")
    print("Levenshtein:", levenshtein_distance("kitten", "sitting"))  # 3
