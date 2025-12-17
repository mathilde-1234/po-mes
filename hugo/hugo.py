import json
from utils import rime_finale, rimes, get_title

def get_poem_data(poem_id) -> dict:
    with open(f"contemplations/{poem_id}.json", encoding="utf-8") as f:
        data = json.load(f)
    return data

def afficher_poeme(poem_id:str,higlight:str) -> None:
    with open(f"contemplations/{poem_id}.json", encoding="utf-8") as f:
        data = json.load(f)
    print(get_title(data["name"]))
    for strophe in data["content"]:
        for vers in strophe:
            vers:str = vers.replace(higlight+" ",f"\x1b[101m{higlight}\x1b[0m ")
            print(vers)

def occurrence(poem_id:str, mot:str) -> int:
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



afficher_poeme("1/P1","le")
print(occurrence("1/P1", "le"))

# rimes = rimes(get_poem_data("1/P5"))
# print(rime_finale(rimes))

# print(occurence_totale("dieu"))
# print(occurence_titre("Le"))