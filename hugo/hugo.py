import json
import utils

def get_poem_data(poem_id):
    with open(f"contemplations/{poem_id}.json", encoding="utf-8") as f:
        data = json.load(f)
    return data

def afficher_poeme(poem_id):
    with open(f"contemplations/{poem_id}.json", encoding="utf-8") as f:
        data = json.load(f)
    print(utils.get_title(data["name"]))
    for strophe in data["content"]:
        print()
        for vers in strophe:
            print(vers)

def occurrence(poem_id, mot):
    mot = mot.lower()
    with open(f"contemplations/{poem_id}.json", encoding="utf-8") as f:
        data = json.load(f)
    n = 0
    for strophe in data["content"]:
        for vers in strophe:
            for word in vers.lower().split():
                if word != mot:continue
                n += 1
    presence = data["name"] if n>0 else None
    return n,presence

def occurence_totale(mot):
    res = 0
    for livre in range(1,7):
        for poeme in range(1,29):
            try:
                occ,title = occurrence(f"{livre}/P{poeme}",mot)
                print(title)
                res+=occ
            except:
                ...
    return res

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

# afficher_poeme("1/P1")
# print(occurrence("1/P1", "ne"))
# rimes = utils.rimes(get_poem_data("1/P1"))
# print(utils.rime_finale(rimes))*

# print(occurence_totale("dieu"))
print(occurence_titre("Le"))