import requests
import re
API_GATEWAY = "https://asciified.thelicato.io/api/v2/"
def get_title(text: str, font: str = "Pagga") -> str:
    """
    In : text:str, font:str (="Pagga")
    Out : title_str:str
    Simple util for generating ascii titles using an external web api
    """
    text = text.strip().replace(" ", "+") # Mets au format web de l'api
    url = f"{API_GATEWAY}ascii?text={text}&font={font}" # URL
    r = requests.get(url) # Envoie requete
    r.raise_for_status() # Raise le status
    return r.text # Renvoie le titre
def sequence_matcher(a: str, b: str) -> float:
    """
    In : a:str, b:str
    Out : float
    Compares two strings and returns a float represening their similarity
    # Algo de comparaison de strs par recursion
    # ratcliff-obershelp-string-similarity
    # On peut rempalcer par une comparaison simple (a == b)
    # Mais on a de meilleurs résultats avec ce méthode
    # NB: s'éxécute plus lentement que ==
    """
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    lcs = dp[m][n]
    return (2 * lcs) / (m + n) if (m + n) > 0 else 1.0
def nettoyer_vers(vers: str):
    vers = vers.lower().strip()
    ponctuation = ",;.!?«»\":()''…-—"
    s = ""
    for c in vers:
        if c not in ponctuation:
            s += c
    return s
SIMPLY_DICT = {
    "é": "E", "er": "E", "ez": "E", "et": "E", "ée": "E", "ees": "E",
    "ait": "E", "ais": "E", "aient": "E",
    "ou": "U", "oux": "U",
    "in": "IN", "ain": "IN", "eins": "IN", "un": "IN", "ien": "IN",
    "on": "ON", "ons": "ON",
    "an": "AN", "en": "AN", "amp": "AN",
    "eu": "EU", "eux": "EU", "oeu": "EU",
    "i": "I", "is": "I", "it": "I",
    "o": "O", "ot": "O", "aut": "O", "eau": "O",
    "u": "Y", "ue": "Y", "ues": "Y", "ieux": "Y", "ieu": "Y"
}
def simplify_vowels(v):
    return SIMPLY_DICT[v] if v in SIMPLY_DICT else v
VOYELLES = "aeiouyàâäéèêëîïôöùûüÿœ"
def terminaison_phonetique(vers: str) -> str:
    vers = nettoyer_vers(vers) # Virer les spec cars
    if not vers:
        return "" # Ne pas traiter les vers qi sonnt "vides"
    vers = re.sub(r"(e?s?|ent)$", "", vers) # Virer les lettres ùmuettes
    m = re.search(r"[{}]+[^{}]*$".format(VOYELLES, VOYELLES), vers)
    # Je ne sais plus exactment mais cette ligne importante
    if m:
        end = m.group(0)
        m2 = re.match(r"([{}]+)(.*)".format(VOYELLES), end)
        if m2:
            v = m2.group(1)
            c = m2.group(2)
            return simplify_vowels(v) + c
        return end
    return vers[-3:] # Renvoie la terminaison des vers
def rimes(poem_data) -> list:
    """
    In: poem_data:dict (poem data)
    Out: res:list
    List containing all rimes
    """
    def rime_proche(x, y, seuil=0.6):
        return sequence_matcher(x, y) >= seuil
    res = []
    for strophe in poem_data["content"]:
        term = [terminaison_phonetique(v) for v in strophe]
        if len(term) >= 4:
            a, b, c, d = term[:4]
            if rime_proche(a, b) and rime_proche(c, d):
                sch = "AABB"
            elif rime_proche(a, d) and rime_proche(b, c):
                sch = "ABBA"
            elif rime_proche(a, c) and rime_proche(b, d):
                sch = "ABAB"
            else:
                sch = "non reconnu"
        else:
            sch = "non reconnu"
        res.append(sch)
    return res
def rime_finale(sch:list) -> str:
    """
    In: sch:list (quantité de rimes par rime dans un texte)
    Out: max(total,key=total.get) (Rime la plus représentée (except "non reconnu"))
    """
    total = {}
    for i in sch:
        if i not in total:
            total[i]=1
        else:
            total[i]+=1
    total["non reconnu"]=0
    print(total)
    return max(total,key=total.get)
    # Erreur syntaxique de l'IDE mais fonctionne qd même