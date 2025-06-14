#lista6

import unicodedata

#zadanie 3
#a
#najdłuższy wspólny podciąg bez przerw (substring)
def najdluzszy_wspolny_podciag_bez_przerw(s1, s2):
    dl1, dl2 = len(s1), len(s2)

    dp = [[0] * (dl2 + 1) for _ in range(dl1 + 1)]
    max_dlugosc = 0

    for i in range(1, dl1 + 1):
        for j in range(1, dl2 + 1):

            if s1[i - 1] == s2[j - 1]:

                dp[i][j] = dp[i - 1][j - 1] + 1

                max_dlugosc = max(max_dlugosc, dp[i][j])
            else:
                dp[i][j] = 0
    return max_dlugosc

#b
#najdłuższy wspólny podciąg z przerwami (subsequence)
def najdluzszy_wspolny_podciag_z_przerwami(s1, s2):
    dl1, dl2 = len(s1), len(s2)

    dp = [ [0] * (dl1 + 1) for _ in range(dl2 + 1)]

    for i in range(1, dl2 + 1):

        for j in range(1, dl1 + 1):

            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1

            else:
                dp[i][j] = max( dp[i - 1][j] , dp[i][j - 1] )

    return dp[dl2][dl1]

#d
#odległość Levenshteina – liczba operacji potrzebna do przekształcenia jednego ciągu w drugi
def Levenshteina_odleglosc(s1, s2):
    m, n = len(s1), len(s2)

    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            koszt = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,      #wsunięcie
                dp[i][j - 1] + 1,      #wstawienie
                dp[i - 1][j - 1] + koszt  #zamiana
            )

    return dp[m][n]

if __name__ == "__main__":
    print("\nZadanie_3a: ")
    s1="konwaliab"
    s2="zawalinab"
    print(s1,s2)
    print("Najdłuższy wspólny podciąg ciągły:", najdluzszy_wspolny_podciag_bez_przerw(s1, s2))  # 4

    print("\nZadanie_3b: ")
    s1="ApqBCrDeFt"
    s2="tABuCoDewxFyz"
    print(s1, s2)
    print("Najdłuższy wspólny podciąg:", najdluzszy_wspolny_podciag_z_przerwami(s1,s2))  # 6

    print("\nZadanie_3d: ")
    s1 = "kitten"
    s2 = "sitting"
    print(s1, s2)
    print("Levenshteina odległość:", Levenshteina_odleglosc(s1,s2))  # 3