import json
from utils import rime_finale, rimes, get_title

def get_poem_data(poem_id) -> dict:
    """
    Prends le "poeme_id:str" et renvoie un dictionnaire connetenant toutes ses informations. (voir format dans la DB)
    """
    with open(f"contemplations/{poem_id}.json", encoding="utf-8") as f:
        data = json.load(f)
    return data

def afficher_poeme(poem_id:str,higlight:str) -> None:
    """
    Affiche le poeme avec son titre en ASCII art et les higlights en rouge en utilisant des codes ANSI ESCAPE
    """
    with open(f"contemplations/{poem_id}.json", encoding="utf-8") as f:
        data = json.load(f)
    print(get_title(data["name"]))
    for strophe in data["content"]:
        for vers in strophe:
            vers:str = vers.replace(higlight+" ",f"\x1b[101m{higlight}\x1b[0m ")
            print(vers)

def occurrence(poem_id:str, mot:str) -> int:
    """
    Renvoie un int "n:int" représentant la quantité de fois que le mot "mot:str" apparait dans "poem_id:dtr" le poeme
    """
    with open(f"contemplations/{poem_id}.json", encoding="utf-8") as f:
        data = json.load(f)
    mot = mot.lower()
    n = 0
    for strophe in data["content"]:
        for vers in strophe:
            for word in vers.lower().split():
                if word != mot:continue
                n += 1
    return n

def occurence_totale(mot) -> int:
    "Cherche toute la DB pour un certain mot, print tout les poemes ayant le mot et renvoie la quantité de mots trouvés."
    mot = mot.lower()
    n = 0
    for livre in range(1,7):
        for poeme in range(1,29):
            try:
                with open(f"contemplations/{livre}∕P{poeme}.json", encoding="utf-8") as f:
                    data = json.load(f)
                for strophe in data["content"]:
                    for vers in strophe:
                        for word in vers.lower().split():
                            if word != mot:continue
                            n += 1
                if n>0:
                    print(data["name"])                
            except:
                ...
    return n

def occurence_titre(mot):
    """
    Print tous les titres contenant un certain mot dans leur titre et renvoie la quantité de mots découvets dans les titres.
    """
    mot = mot.lower()
    with open(f"contemplations/contemplations.json", encoding="utf-8") as f:
        data = json.load(f)
    n = 0
    for livre in range(1,7):
        for poeme in range(1,52):
            try:
                titre = data[str(livre)][f"P{poeme}"].lower()
                for word in titre.split():
                    if word != mot:continue
                    n += 1
                    print(f"{livre}P{poeme}  {titre}")
            except:
                ...
    return n

# EXEMPLE D'UTILISATION
if __name__ == "__main__":
    keyword = "le"
    poeme = "1/P1"

    # Afficher le poeme avec higlight  et titre puis donner la quantité de keywordss toruvés.
    afficher_poeme(poeme,keyword)
    print(f'il y as {occurrence("1/P1", keyword)} fois le mot {keyword} dans le poème "{poeme}"')

    # Afficher la construction du poeme (le type de ryme qu'il utilise)
    # rimes = rimes(get_poem_data("1/P5"))
    # print(rime_finale(rimes))

    # Chercherr dans tous les poemes le mot "dieu"
    # print(occurence_totale("dieu"))

    # Cherhcer dans tous les titres le mot "le"
    # print(occurence_titre("Le"))