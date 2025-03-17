# tematická koncetrace textu
from collections import OrderedDict
import pandas as pd
pd.set_option('display.max_rows', None)
import matplotlib.pyplot as plt
import numpy as np
from tkinter import Text, Tk, Label, Entry, Button, filedialog, messagebox, Scrollbar, Canvas, Frame
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

def process_file():
    # Získání vstupu od uživatele
    zadej = entry.get()
    if not zadej:
        messagebox.showerror("Error", "Take a name of file!")
        return 

    try:
        # Získání velikosti grafu od uživatele
        try:
            width = float(width_entry.get())
            height = float(height_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Enter valid values for chart width and height!")
            return
        
        # filepath: c:\Users\Richard Změlík\Desktop\TK\tk.py
        file_path = os.path.join(os.path.dirname(__file__), "lemma", f"{zadej}.txt")
        with open(file_path, mode="r", encoding="UTF-8") as f:
            text = f.read()     

        # Segmentace souboru s lemmaty na slova
        text_split = text.split()

        slovo = []
        for i in text_split:
            slovo.append(i)

        # Počítání frekvence
        freq = []
        for i in text_split:
            freq.append(text_split.count(i))

        # Otevření souboru s morfologickými tagy
        file_path = os.path.join(os.path.dirname(__file__), "tag", f"{zadej}.txt")
        with open(file_path, mode="r", encoding="UTF-8") as f:
            tagy = f.read()

        tagy_split = tagy.split()

        tag = []
        for i in tagy_split:
            tag.append(i[0:1])

        data = {
            "WORD": slovo,
            "FREQ": freq,
            "TAG": tag
        }

        # Vytvoření tabulky
        tabulka = pd.DataFrame(data).sort_values(by=["FREQ"], ascending=False).drop_duplicates(subset=["WORD"]).reset_index(level=None, drop=False, inplace=False, col_level=0, col_fill='').drop("index", axis=1)

        file_path = os.path.join(os.path.dirname(__file__), f"{zadej}.xlsx")
        tabulka[["WORD", "FREQ"]].to_excel(file_path, index=False)
        messagebox.showinfo("Excel Saved", f"Data saved as {zadej}.xlsx")

        slovo = []
        af = []
        tagg = []


        
        for index, row in tabulka.iterrows():
            new_index = index + 1
            if new_index == row["FREQ"]:
                for index, row in tabulka.iterrows():
                    if index < new_index and row["TAG"] == "N":
                        slovo.append(row["WORD"])
                        af.append(row["FREQ"])
                        tagg.append(row["TAG"])
                    if index < new_index and row["TAG"] == "A":
                        slovo.append(row["WORD"])
                        af.append(row["FREQ"])
                        tagg.append(row["TAG"])
                    if index < new_index and row["TAG"] == "A":
                        slovo.append(row["WORD"])
                        af.append(row["FREQ"])
                        tagg.append(row["TAG"])
                    if index < new_index and row["TAG"] == "V":
                        slovo.append(row["WORD"])
                        af.append(row["FREQ"])
                        tagg.append(row["TAG"])


        if not slovo:
            messagebox.showinfo("Result", "No words found on the d boundary of the h-point.")
        else:
            # Zobrazení grafu v okně
            fig, ax = plt.subplots(figsize=(10, 15))
            ax.plot(slovo, af)
            ax.set_title(f"Thematic Concentration of {zadej}")
            ax.set_ylabel("Frequency")
            ax.set_xticks(range(len(slovo)))
            ax.set_xticklabels(slovo, rotation=45)

            # Uložení grafu jako PNG
            png_file_path = os.path.join(os.path.dirname(__file__), f"{zadej}_graph.png")
            fig.savefig(png_file_path, format="png", dpi=300)
            messagebox.showinfo("PNG Saved", f"Graph saved as {zadej}_graph.png")

            # Přidání mřížky
            ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)

            canvas = FigureCanvasTkAgg(fig, master=window)
            canvas.draw()
            canvas.get_tk_widget().pack()

    except FileNotFoundError:
        messagebox.showerror("Error", f"The file {zadej} was not found!")

def about():
        # Funkce pro zobrazení informace o aplikaci
        messagebox.showinfo("About", "Thematic Concentration of the Text\n© Richard Změlík, 2025 \n version 1.0")
def info():
        # Funkce pro zobrazení informace o aplikaci
        messagebox.showinfo("Info", "The program calculates the so-called thematic text concentration (TC), which shows which autosemantics are displayed above the so-called h-point. The h-point is a boundary that divides the rank frequency distribution into a region with a predominance of synsemantics a region where autosemantics appear. The purpose of TK is to filter out autosemantics above the h-point boundary. More here (https://www.czechency.org/slovnik/TEMATICK%C3%81%20KONCENTRACE%20TEXTU). \n\nThe folder contains both the file itself and the two components \"lemma\" and \"tag\". These folders contain TXT files (UTF-8 encoding) with the lemmas and morphological tags of the text. These files can be obtained by processing the plain text (UTF-8 encoding) using MorphoDita software (https://lindat.mff.cuni.cz/services/morphodita/). \n\nFor example, both folders contain TXT files with lemmata and tags of Alois Jirásek's novel F. L. Věk I.")

# Vytvoření hlavního okna
window = Tk()
window.title("Thematic Concentration of the Text")
window.geometry("650x800")

# Vytvoření menu
menu = Menu(window)
window.config(menu=menu)

# Přidání položky "Help" do menu
help_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=about)
help_menu.add_command(label="Info", command=info)

# Popisek a vstupní pole
label = Label(window, text="Enter the name of the lemma file:")
label.pack(pady=10)
label.pack(padx=5)

entry = Entry(window, width=40)
entry.pack()

# Popisek a vstupní pole pro šířku grafu
width_label = Label(window, text="Enter the width of the chart (in inches):")
width_label.pack(pady=10)

width_entry = Entry(window, width=10)
width_entry.pack()
width_entry.insert(0, "10")  # Výchozí hodnota

# Popisek a vstupní pole pro výšku grafu
height_label = Label(window, text="Enter the height of the chart (in inches):")
height_label.pack()

height_entry = Entry(window, width=15)
height_entry.pack()
height_entry.insert(0, "15")  # Výchozí hodnota

# Tlačítko pro zpracování souboru
button = Button(window, text="Submit", command=process_file, bg="grey", fg="white")
button.pack(pady=10)

# Popisek pro zobrazení stavu
label2 = Label(window, text="Be patient until the graph is generated. The length of the progress depends on the size of the text. \n The resulting graph and a table with frequency values will be saved in your TK folder.", font=("Arial", 9), fg="green")
label2.pack(pady=10)

autorization = Label(window, text="© Richard Změlík, 2025 \n version 1.0.1", font=("Arial", 8))
autorization.pack(pady=20)

# Spuštění hlavní smyčky
window.mainloop()
