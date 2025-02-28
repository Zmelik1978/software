from termcolor import colored
import pyphen
from nltk.tokenize import word_tokenize, sent_tokenize
import pandas as pd
pd.set_option('display.max_columns', None, 'display.max_rows', None)
import os
import codecs
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import simpledialog
import webbrowser

# Funkce pro zobrazení informačního dialogu
def show_info():
    info_text = (
        "This program calculates the readability of text files in the selected directory.\nEnter the absolute path to the directory on the Desktop. You don't need to change the slashes.\n\nThe readability of the text is determined by this choosen measures:\n\n1. Flesch Reading Ease\n2. Flesch-Kincaid Grade Level\n3. Gunning Fog Index\n\nFor more information and calculatiing this meassures visit this website:\nhttps://www.korpusprozy.com/corpus_structure.html\n\nThe results are saved as an Excel file into the folder ReadibilityText on your Desktop and and graphs are created.\n\nThe program also creates text files with data for the graphs.\n\n ")

    tk.messagebox.showinfo("Info", info_text)

# Vytvoření GUI pro zadání názvu adresáře
root = tk.Tk()
root.title("Readibility of Texts")

root.geometry("450x350")

# Vytvoření menu
menu = tk.Menu(root)
root.config(menu=menu)

# Přidání položky "Info" do menu
info_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Info", menu=info_menu)
info_menu.add_command(label="Show Info", command=show_info)

header_label = tk.Label(root, text="Readibility of Texts", font=("Helvetica", 16))
header_label.pack(pady=20)

# Vstupní pole pro zadání cesty
cesta_label = tk.Label(root, text="Enter the absolute path to the \"ReadabilityText\" directory on you Desktop")
cesta_label.pack(pady=5)
cesta_entry = tk.Entry(root, width=50)
cesta_entry.pack(pady=5)

# Vstupní pole pro zadání názvu adresáře
zadej_label = tk.Label(root, text="Enter the name of the directory where you have the text files")
zadej_label.pack(pady=5)
zadej_entry = tk.Entry(root, width=50)
zadej_entry.pack(pady=5)

def get_inputs():
    global cesta, zadej
    cesta = cesta_entry.get()
    zadej = zadej_entry.get()
    root.destroy()  # Zavření okna po zadání vstupů
    main()  # Spuštění hlavní logiky po zadání vstupů

submit_button = tk.Button(root, text="Submit", command=get_inputs)
submit_button.pack(pady=10)

author = tk.Label(root, text="© Richard Změlík\n\nversion 1.0", font=("Helvetica", 8))
author.pack(pady=30)

root.mainloop()

def main():
    name = []
    value1 = []
    value2 = []
    value3 = []
    text_size = []

    directory_path = os.path.join(rf"{cesta}\ReadibilityText\{zadej}")

    def flesch_reading_ease(file_path):
        """
        Implements Flesch reading ease formula:
        206.835 - 1.015 * (total words / total sentences) - 84.6 * (total syllables / total words)
        """
        dic = pyphen.Pyphen(lang='cs')
        with codecs.open(file_path, 'r', 'utf-8') as file:
            text = file.read()
        total_words = len(word_tokenize(text))
        total_sentences = len(sent_tokenize(text))
        total_syllables = sum([len(dic.inserted(word).split('-')) for word in word_tokenize(text)])
        
        return round(206.835 - 1.015 * (total_words / total_sentences) - 84.6 * (total_syllables / total_words), 4)

    def flesch_kincaid_grade_level(file_path):
        """
        Implements Flesch-Kincaid Grade Level formula:
        0.39 * (total words / total sentences) + 11.8 * (total syllables / total words) - 15.59
        """
        dic = pyphen.Pyphen(lang='cs')
        with codecs.open(file_path, 'r', 'utf-8') as file:
            text = file.read()
        total_words = len(word_tokenize(text))
        text_size.append(total_words)
        total_sentences = len(sent_tokenize(text))
        total_syllables = sum([len(dic.inserted(word).split('-')) for word in word_tokenize(text)])
        return round(0.39 * (total_words / total_sentences) + 11.8 * (total_syllables / total_words) - 15.59, 4)

    def gunning_fog_index(file_path):
        """
        Implements Gunning Fog Index formula:
        0.4 * ((total words / total sentences) + 100 * (total complex words / total words))
        """
        dic = pyphen.Pyphen(lang='cs')
        with codecs.open(file_path, 'r', 'utf-8') as file:
            text = file.read()
        total_words = len(word_tokenize(text))
        total_sentences = len(sent_tokenize(text))
        total_complex_words = 0
        for word in word_tokenize(text):
            if len(dic.inserted(word).split('-')) >= 3:
                total_complex_words += 1
        return round(0.4 * ((total_words / total_sentences) + 100 * (total_complex_words / total_words)), 4)

    def process_directory(directory_path):
        """Funkce, která zpracuje všechny textové soubory v adresáři."""
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                name.append(filename)  # Přidání názvu souboru do seznamu name
                value1.append(flesch_reading_ease(file_path))
                value2.append(flesch_kincaid_grade_level(file_path))
                value3.append(gunning_fog_index(file_path))

    process_directory(directory_path)

    data = {
        "NAME": name,
        "FLESCH_READING_EASE": value1,
        "FLESCH_KINCAID_GRADE_LEVEL": value2,
        "GUNNING_FOG_INDEX": value3,
        "TEXT_SIZE": text_size
    }
    df = pd.DataFrame(data).sort_values(by="FLESCH_READING_EASE", ascending=False)
    print(df)

    df.to_excel(os.path.join(rf"{cesta}\ReadibilityText\{zadej} - text readibility.xlsx"))

    df_flesch_reading_ease_text_size = df[["FLESCH_READING_EASE", "TEXT_SIZE", "NAME"]]
    df_flesch_kincaid_grade_level_text_size = df[["FLESCH_KINCAID_GRADE_LEVEL", "TEXT_SIZE", "NAME"]]
    df_gunning_fog_index_text_size = df[["GUNNING_FOG_INDEX", "TEXT_SIZE", "NAME"]]

    list_flesch_reading_ease_text_size = " ".join([f"{{x: {b['TEXT_SIZE']}, y: {b['FLESCH_READING_EASE']}, name: removeTxtExtension ('{b['NAME']}')}}," for _, b in df_flesch_reading_ease_text_size.iterrows()])
    list_flesch_kincaid_grade_level_text_size = " ".join([f"{{x: {b['TEXT_SIZE']}, y: {b['FLESCH_KINCAID_GRADE_LEVEL']}, name: removeTxtExtension ('{b['NAME']}')}}," for _, b in df_flesch_kincaid_grade_level_text_size.iterrows()])
    list_gunning_fog_index_text_size = " ".join([f"{{x: {b['TEXT_SIZE']}, y: {b['GUNNING_FOG_INDEX']}, name: removeTxtExtension ('{b['NAME']}')}}," for _, b in df_gunning_fog_index_text_size.iterrows()])

    with open(os.path.join(rf"{cesta}\ReadibilityText\{zadej} - text readibility - Flesch Reading Ease vs. Text Size.txt"), "w", encoding="UTF-8") as file:
        file.write(list_flesch_reading_ease_text_size)
    with open(os.path.join(rf"{cesta}\ReadibilityText\{zadej} - text readibility - Flesch-Kincaid Grade Level vs. Text Size.txt"), "w", encoding="UTF-8") as file:
        file.write(list_flesch_kincaid_grade_level_text_size)
    with open(os.path.join(rf"{cesta}\ReadibilityText\{zadej} - text readibility - Gunning Fog Index vs. Text Size.txt"), "w", encoding="UTF-8") as file:
        file.write(list_gunning_fog_index_text_size)

    # Vytvoření grafů
    plt.figure(figsize=(10, 10))

    # Vytvoření subgrafů
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 10))

    # První subgraf: Text Size vs. Flesch Reading Ease
    ax1.plot(df["TEXT_SIZE"], df["FLESCH_READING_EASE"], 'o', color='red')
    ax1.set_xlabel("Text Size")
    ax1.set_ylabel("Flesch Reading Ease")
    ax1.set_title("Text Size vs. Flesch Reading Ease")
    ax1.grid()

    # Přidání názvů textů jako popisky pro první subgraf
    for i, txt in enumerate(df["NAME"]):
        ax1.annotate(txt, (df["TEXT_SIZE"].iloc[i], df["FLESCH_READING_EASE"].iloc[i]))

    # Druhý subgraf: Text Size vs. Flesch-Kincaid Grade Level
    ax2.plot(df["TEXT_SIZE"], df["FLESCH_KINCAID_GRADE_LEVEL"], 's', color='blue')
    ax2.set_xlabel("Text Size")
    ax2.set_ylabel("Flesch-Kincaid Grade Level")
    ax2.set_title("Text Size vs. Flesch-Kincaid Grade Level")
    ax2.grid()

    # Přidání názvů textů jako popisky pro druhý subgraf
    for i, txt in enumerate(df["NAME"]):
        ax2.annotate(txt, (df["TEXT_SIZE"].iloc[i], df["FLESCH_KINCAID_GRADE_LEVEL"].iloc[i]))

    # Třetí subgraf: Text Size vs. Flesch Reading Ease
    ax3.plot(df["FLESCH_KINCAID_GRADE_LEVEL"], df["FLESCH_READING_EASE"], 'x', color='green')
    ax3.set_xlabel("Flasch-Kincaid Grade Level")
    ax3.set_ylabel("Flesch Reading Ease")
    ax3.set_title("Flasch-Kincaid Grade Level vs. Flesch Reading Ease")
    ax3.grid()

    # Přidání názvů textů jako popisky pro třetí subgraf
    for i, txt in enumerate(df["NAME"]):
        ax3.annotate(txt, (df["FLESCH_KINCAID_GRADE_LEVEL"].iloc[i], df["FLESCH_READING_EASE"].iloc[i]))

    # Čtvrtý subgraf: Text Size vs. Gunning Fog Index
    ax4.plot(df["TEXT_SIZE"], df["GUNNING_FOG_INDEX"], 'd', color='purple')
    ax4.set_xlabel("Text Size")
    ax4.set_ylabel("Gunning Fog Index")
    ax4.set_title("Text Size vs. Gunning Fog Index")
    ax4.grid()

    # Přidání názvů textů jako popisky pro čtvrtý subgraf
    for i, txt in enumerate(df["NAME"]):
        ax4.annotate(txt, (df["TEXT_SIZE"].iloc[i], df["GUNNING_FOG_INDEX"].iloc[i]))

    plt.tight_layout()
    plt.show()

# Spuštění hlavní funkce
if __name__ == "__main__":
    main()