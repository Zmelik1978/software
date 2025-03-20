from __future__ import division
import json
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
import time
from termcolor import colored
import os
from tkinter import Tk, Label, Entry, Button, StringVar, filedialog, messagebox

file_path = os.path.join(os.path.dirname(__file__), "tezaurus.json")
with open(file_path, 'r') as myfile:
    data=myfile.read()
slovnik = json.loads(data)

def start_analysis():
    global zadej, vypnuoutPC, question
    zadej = file_var.get()
    vypnuoutPC = shutdown_var.get()
    question = graph_var.get()
    if not zadej:
        messagebox.showerror("Chyba", "Zadejte jméno výstupního xlsx souboru")
        return
    root.destroy()

root = Tk()
root.title("Tezaurus Sentiment Analysis")

Label(root, text="Zadejte jméno výstupního xlsx souboru:").grid(row=0, column=0, padx=10, pady=5)
file_var = StringVar()
Entry(root, textvariable=file_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Má se počítač po skončení úlohy vypnout? (A/N):").grid(row=1, column=0, padx=10, pady=5)
shutdown_var = StringVar()
Entry(root, textvariable=shutdown_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Vygenerovat graf? (A/N):").grid(row=2, column=0, padx=10, pady=5)
graph_var = StringVar()
Entry(root, textvariable=graph_var).grid(row=2, column=1, padx=10, pady=5)

Button(root, text="Spustit analýzu", command=start_analysis).grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()

start_time = time.time()

a = open(filedialog.askopenfilename(title="Vyberte soubor", filetypes=[("Text Files", "*.txt")]), encoding='utf-8')
a_cist = a.read()
a_cist.lower()
text=a_cist.split()

N = len(text)


dictus = {}

dictus_k_tisku = dict()

# VYHLEDÁ LEMMA, A POKUD JE VE VALUE IN SLOVNIK, PAK JEJ ZAŘADÍ DO DOCTUS+SOOUČET LEMMATU V SOUBORU
for key in slovnik:
    for value in slovnik[key]:                      # zde jsem na úrovni value v 'slovnik'
        for i in text:
            if i in value:
                dictus[i] = text.count(value)       # do slovníku 'dictus' přidám jako lemma [i], které se shoduje s value jako KEY a jako VALUE přidám kolikrát se lemma v souboru (načtené TXT) vyskytuje 


s1 = []
s2 = []

for a, b in slovnik.items():
    for i in text:
        if i in b:
            s1.append(a)
            s2.append(i)
        else:
            pass

s1 = list(map(lambda x: x.replace("LÁSKA", 'LOVE (LÁSKA):'), s1))
s1 = list(map(lambda x: x.replace("ŠPATNOST", 'WRONGNESS (ŠPATNOST):'), s1))
s1 = list(map(lambda x: x.replace("VESELOST", 'CHEERFULNESS (VESELOST):'), s1))
s1 = list(map(lambda x: x.replace("TOUHA", 'DESIRE (TOUHA):'), s1))
s1 = list(map(lambda x: x.replace("ZÁRMUTEK", 'MATCH (ZÁRMUTEK):'), s1))
s1 = list(map(lambda x: x.replace("NEPŘÍJEMNOST", 'UNPLESANTNESS (NEPŘÍJEMNOST):'), s1))
s1 = list(map(lambda x: x.replace("RADOST", 'HAPPINESS (RADOST):'), s1))
s1 = list(map(lambda x: x.replace("PŘÍJEMNOST", 'PLESANTNESS (PŘÍJEMNOST):'), s1))
s1 = list(map(lambda x: x.replace("ROZMRZELOST", 'CRANKINESS (ROZRMZELOST):'), s1))
s1 = list(map(lambda x: x.replace("ÚŽAS", 'AMAZEMENT (ÚŽAS):'), s1))
s = list(map(lambda x: x.replace("SPOKOJENOST", 'SATISFACTION (SPOKOJENOST):'), s1))
s = list(map(lambda x: x.replace("NELÍTOSTNOST", 'UNFORGIVENESS (NELÍTOSTNOST):'), s))
s1 = list(map(lambda x: x.replace("ÚCTA", 'RESPECT (ÚCTA):'), s1))
s1 = list(map(lambda x: x.replace("ZALÍBENÍ", 'LIKING (ZALÍBENÍ):'), s1))
s1 = list(map(lambda x: x.replace("OBEZŘETNOST", 'PRUDENCE (OBEZŘETNOST):'), s1))
s1 = list(map(lambda x: x.replace("ZÁVIST", 'ENVY (ZÁVIST):'), s1))
s1 = list(map(lambda x: x.replace("STRACH", 'FEAR (STRACH):'), s1))
s1 = list(map(lambda x: x.replace("ZLOST", 'ANGER (ZLOST):'), s1))
s1 = list(map(lambda x: x.replace("SOUCIT", 'SYMPHATY (SOUCIT):'), s1))
s1 = list(map(lambda x: x.replace("VULGÁRNOST", 'VULGARITY (VULGÁRNOST):'), s1))
s1 = list(map(lambda x: x.replace("VDĚČNOST", 'GRATEFULNESS (VDĚČNOST):'), s1))
s1 = list(map(lambda x: x.replace("NEVZRUŠENOST", 'UNEXCITEDNESS (NEVZRUŠENOST):'), s1))
s1 = list(map(lambda x: x.replace("SKROMNOST", 'MODESTY (SKROMNOST):'), s1))
s1 = list(map(lambda x: x.replace("KRÁSA", 'BEAUTY (KRÁSA):'), s1))
s1 = list(map(lambda x: x.replace("NEÚCTA", 'DISRESPECT (NEÚCTA):'), s1))
s1 = list(map(lambda x: x.replace("NUDA", 'BOREDOM (NUDA):'), s1))
s1 = list(map(lambda x: x.replace("LHOSTEJNOST", 'INDIFFERETNESS (LHOSTEJNOST):'), s1))
s1 = list(map(lambda x: x.replace("NECITLIVOST", 'INSENSITIVITY (NECITLIVOST):'), s1))
s1 = list(map(lambda x: x.replace("NESPOKOJENOST", 'DISSATISFACTION (NESPOKOJENOST):'), s1))
s1 = list(map(lambda x: x.replace("ODPUŠTĚNÍ", 'FORGIVENESS (ODPUŠTĚNÍ):'), s1))
s1 = list(map(lambda x: x.replace("OBLIBA", 'POPULARITY (OBLIBA):'), s1))
s1 = list(map(lambda x: x.replace("ODVAHA", 'COURAGE (ODVAHA):'), s1))
s1 = list(map(lambda x: x.replace("POPUDLIVOST", 'IRRITABILITY (POPUDLIVOST):'), s1))
s1 = list(map(lambda x: x.replace("OŠKLIVOST", 'UGLINESS (OŠKLIVOST):'), s1))
s1 = list(map(lambda x: x.replace("OKÁZALOST", 'OSTENTATIOUSNESS (OKÁZALOST):'), s1))
s1 = list(map(lambda x: x.replace("POKORA", 'HUMBLENESS (POKORA):'), s1))
s1 = list(map(lambda x: x.replace("KULTIVOVANOST", 'SOPHISTICATION (KULTIVOVANOST):'), s1))
s1 = list(map(lambda x: x.replace("PŘITÍŽENÍ", 'WORSENING (PŘITÍŽENÍ):'), s1))
s1 = list(map(lambda x: x.replace("SKLÍČENOST", 'DEPRESION (SKLÍČENOST):'), s1))
s1 = list(map(lambda x: x.replace("PROKLETÍ", 'CURSE (PROKLETÍ):'), s1))
s1 = list(map(lambda x: x.replace("NELIBOST", 'DISLIKE (NELIBOST):'), s1))
s1 = list(map(lambda x: x.replace("NEROZVÁŽNOST", 'INDISCRETION (NEROZVÁŽNOST):'), s1))
s1 = list(map(lambda x: x.replace("ÚLEVA", 'RELIEF (ÚLEVA):'), s1))
s1 = list(map(lambda x: x.replace("PÝCHA", 'PRIDE (PÝCHA):'), s1))
s1 = list(map(lambda x: x.replace("DRZOST", 'AROGANCE (DRZOST):'), s1))
s1 = list(map(lambda x: x.replace("NENÁVIST", 'HATRED (NENÁVIST):'), s1))
s1 = list(map(lambda x: x.replace("CITLIVOST", 'SENSITIVITY (CITLIVOST):'), s1))
s1 = list(map(lambda x: x.replace("BEZNADĚJ", 'DESPAIR (BEZNADĚJ):'), s1))
s1 = list(map(lambda x: x.replace("NEPŘEKVAPENOST", 'UNSURPRISINGNESS (NEPŘEKVAPENOST):'), s1))
s1 = list(map(lambda x: x.replace("SPOLEČENSKOST", 'SOCIABILITY (SPOLEČENSKOST):'), s1))
s1 = list(map(lambda x: x.replace("ZBABĚLOST", 'COWARDICE (ZBABĚLOST):'), s1))
s1 = list(map(lambda x: x.replace("ODČINĚNÍ", 'REPENTANCE (ODČINĚNÍ):'), s1))
s1 = list(map(lambda x: x.replace("MARNIVOST", 'VANITY (MARNIVOST):'), s1))
s1 = list(map(lambda x: x.replace("NEVDĚČNOST", 'UNGRATEFULNESS (NEVDĚČNOST):'), s1))
s1 = list(map(lambda x: x.replace("FORMÁLNOST", 'FORMALITY (FORMÁLNOST):'), s1))
s1 = list(map(lambda x: x.replace("ŽÁRLIVOST", 'JEALOUSY (ŽÁRLIVOST):'), s1))
s1 = list(map(lambda x: x.replace("FILANTROPIE", 'PHILANTROPY (FILANTROPIE):'), s1))
s1 = list(map(lambda x: x.replace("MISANTROPIE", 'MISANTROPY (MISANTROPIE):'), s1))
s1 = list(map(lambda x: x.replace("NEFORMÁLNOST", 'NONFORMALITY (NEFORMÁLNOST):'), s1))
s1 = list(map(lambda x: x.replace("UCTIVOST", 'RESPECTFULNESS (UCTIVOST):'), s1))


df = pd.DataFrame({
    "slovo": s1,
    "hodnoty": s2
})

df.to_excel("C:/Users/Richard Změlík/Desktop/output.xlsx")  


# dict 'slov' obsahuje všechna témata jako KEY
slov = {
    "LÁSKA": 0,
    "CITLIVOST":0, 
    "PŘÍJEMNOST":0,
    "RADOST":0,
    "SPOKOJENOST":0,
    "ODPUŠTĚNÍ":0,
    "SOUCIT":0, 
    "ODVAHA":0,
    "KRÁSA":0, 
    "SKROMNOST":0, 
    "SPOLEČENSKOST":0,
    "ÚLEVA":0, 
    "VESELOST":0,
    "ODČINĚNÍ":0,
    "ÚCTA":0,
    "OBEZŘETNOST":0, 
    "OBLIBA":0,
    "FILANTROPIE": 0,
    "POKORA": 0, 
    "TOUHA":0,
    "UCTIVOST": 0,
    "ZALÍBENÍ": 0,
    "KULTIVOVANOST": 0,
    "VDĚČNOST":0,

    "NECITLIVOST":0, 
    "NEPŘÍJEMNOST":0, 
    "ZÁRMUTEK":0,
    "NELÍTOSTNOST":0,
    "NEVDĚČNOST":0, 
    "BEZNADĚJ":0,
    "STRACH":0,
    "ZBABĚLOST":0,
    "NEROZVÁŽNOST":0,
    "NUDA":0,
    "OŠKLIVOST":0,
    "NESPOKOJENOST":0,
    "PŘITÍŽENÍ":0,
    "SKLÍČENOST":0,
    "NEÚCTA":0,
    "ZÁVIST":0,
    "ŽÁRLIVOST":0, 
    "LHOSTEJNOST":0, 
    "NELIBOST":0, 
    "MISANTROPIE": 0, 
    "POPUDLIVOST": 0, 
    "ROZMRZELOST": 0, 
    "ŠPATNOST": 0,
    "PÝCHA": 0, 
    "DRZOST": 0,  
    "MARNIVOST": 0,  
    "NENÁVIST": 0, 
    "PROKLETÍ": 0, 
    "ZLOST": 0,  
    "VULGÁRNOST": 0,
    "OKÁZALOST":0,  

    "NEVZRUŠENOST":0,
    "NEPŘEKVAPENOST":0,
    "FORMÁLNOST":0,
    "NEFORMÁLNOST":0,
    "ÚŽAS":0, 
}     

for key in slovnik:                                 # znovu iteruji přes dict 'slovnik', protže se potřebuji dosta k jeho VALUE
    for value in slovnik[key]:                      # jsem u VALUE
            for k, v in dictus.items():             # pro KEY a VALUE v dict 'dictus'
                if k == value:                      # když KEY v 'dictus' odpovídá VALUE v dict 'slovnik'
                    total = 0                       # potřebuji součet všech číslených hodnot VALUE ve slovníku 'dictus'; zadám proměnnou total = 0
                    total = total + v               # k 0 přičtu hodnotu VALUE v 'dictus'
                    slov[key] += total              # do dict 'slov' zanesu KEY z dict 'slovnik' a číslenou hodotu total, která je součtem 


                else:
                    pass

# převod slovníku "slov" na dva listy
klic = []
hodnotaAF = []
hodnotaRF = []
for key, value in slov.items():
    aklic = key
    ahodnota = value
    klic.append(aklic)
    hodnotaAF.append(ahodnota)

for i in hodnotaAF:
    rf = (i/N)*1000000   
    hodnotaRF.append(round(rf, 2)) 

# Seřazení dat podle RF sestupně
sorted_indices = sorted(range(len(hodnotaRF)), key=lambda i: hodnotaRF[i], reverse=True)
klic = [klic[i] for i in sorted_indices]
hodnotaAF = [hodnotaAF[i] for i in sorted_indices]
hodnotaRF = [hodnotaRF[i] for i in sorted_indices]

data2 = {
    "SLOVO": klic,
    "AF": hodnotaAF,
    "RF": hodnotaRF
}

file_path_table = os.path.join(os.path.dirname(__file__), f"{zadej}.xlsx")
tb2 = pd.DataFrame(data2)
tb2.to_excel(file_path_table, f"{zadej}.xlsx")

if question == "A":
    # horizontální graf
    plt.barh(klic, hodnotaRF, color="blue")
    plt.title('{}'.format(zadej))
    plt.xlabel('i.p.m.')
    plt.gca().invert_yaxis()  # Obrácení osy Y pro sestupné řazení

    # Přidání hodnot RF jako popisky
    for index, value in enumerate(hodnotaRF):
        plt.text(value, index, str(value), va='center', ha='left', fontsize=8)

    plt.show()
elif question == "N":
    pass
else:
    pass


end_time = time.time()

total_time = (end_time-start_time)/60

print(colored("Celkový čas", "green"), colored(round(total_time, 2), "green"), colored("min.", "green"))

if vypnuoutPC.upper() == "A":
    messagebox.showinfo("Informace", "Počítač se nyní vypne.")
    os.system('shutdown -s')
elif vypnuoutPC.upper() == "N":
    messagebox.showinfo("Informace", "Úloha dokončena bez vypnutí počítače.")
else:
    pass