import tkinter as tk
from tkinter import ttk, messagebox
import os

# Av Daniel, Melina och Sedat - Grupp 6

FILNAMN = "medicinlista.txt"

# ---------- Klasser ----------

class Medicin:

    def __init__(self, namn, substans, styrka, antal, pris):
        self.namn = namn
        self.substans = substans
        self.styrka = styrka
        self.__antal = antal  # Privat attribut
        self.__pris = pris    # Privat attribut

    def hamta_antal(self):
        return self.__antal

    def hamta_pris(self):
        return self.__pris

    def farg(self): # Färgkodar medicinen svart i listan (receptfri)
        return "ej_recept"

    def medicintyp(self):
        return "Ej receptbelagd"

    def skapa_dictionary(self):
        return {
            "namn": self.namn,
            "substans": self.substans,
            "styrka": self.styrka,
            "antal": self.__antal,
            "pris": self.__pris,
            "typ": self.medicintyp()
        }
        
# ---------- Arv ----------

# ReceptbelagdMedicin ärver allt från Medicin men ändrar beteende för typ och färg
class ReceptbelagdMedicin(Medicin):


    def medicintyp(self):  # Ändrar medicintypen till receptbelagd
        return "Receptbelagd"

    def farg(self):  # Färgkodar medicinen röd i listan (receptbelagd)
        return "recept"

# ---------- Filhantering ----------

def las_mediciner(): 
    if not os.path.exists(FILNAMN):  # Om filen inte finns, returnera tom lista
        return []

    lista = []

    try:
        with open(FILNAMN, "r", encoding="utf-8") as file: # Öppnar filen för läsning ("r")

            for rad in file:
                delar = rad.strip().split(";")  # Delar upp varje rad med semikolon

                namn, substans, styrka, antal, pris, typ = delar

                klass = ReceptbelagdMedicin if typ == "Receptbelagd" else Medicin   # Väljer rätt klass beroende på receptstatus
                lista.append(
                    klass(
                        namn,
                        substans,
                        styrka,
                        int(antal),      # Konvertera text till heltal
                        float(pris),     # Konvertera text till decimaltal
                    )
                )

        return lista

    except (ValueError, OSError):  # Felhantering om filen är skadad eller saknas
        messagebox.showerror("Fel", "Kunde inte läsa medicinlistan.")
        return []

def spara_mediciner():

    try:
        
        with open(FILNAMN, "w", encoding="utf-8") as file:  # Öppnar filen för skrivning ("w")
            
            for medicin in mediciner:  # Går igenom alla mediciner i listan
                
                data = medicin.skapa_dictionary()  # Hämtar data som dict
                
                file.write(     # Sparar informationen på en rad som separeras av semikolon
                    f"{data['namn']};"
                    f"{data['substans']};"
                    f"{data['styrka']};"
                    f"{data['antal']};"
                    f"{data['pris']};"
                    f"{data['typ']}\n"  
                )

    except OSError:
        messagebox.showerror("Fel", "Kunde inte spara filen.")

# ---------- Funktioner ----------

def rensa_falt():
    for entry in entries:  # Töm alla inmatningsfält
        entry.delete(0, tk.END)
    recept_var.set(False)  # Avmarkera kryssrutan

def lagg_till():

    namn = namn_entry.get()
    substans = substans_entry.get()
    styrka = styrka_entry.get()
    
    # Validera och konvertera inmatning
    try:
        antal = int(antal_entry.get())
        pris = float(pris_entry.get())
          
        if not all([namn, substans, styrka]) or antal < 0 or pris < 0:
            raise ValueError  # Visa felmeddelande om något saknas eller är negativt


    except ValueError:
        messagebox.showerror(
            "Fel",
            "Kontrollera att alla fält är korrekt ifyllda."
        )
        return

    # Väljer rätt klass beroende på kryssrutan
    klass = ReceptbelagdMedicin if recept_var.get() else Medicin 

    mediciner.append(
        klass(
            namn,
            substans,
            styrka,
            antal,
            pris,           
        )
    )
    rensa_falt()
    spara_mediciner()
    visa_mediciner()

def visa_mediciner():
    for rad in medicin_lista.get_children():  # Hämta alla rad-ID:n som finns i tabellen just nu 
        medicin_lista.delete(rad) # Tar bort rad från listan
    
    # Lägg till alla mediciner i tabellen/treeview
    for index in range(len(mediciner)):
        medicin = mediciner[index]
        medicin_lista.insert(
            "",
            tk.END,
            iid=index,  # Unikt ID för varje rad (används vid val)
            values=(
                medicin.namn,
                medicin.styrka,
                medicin.hamta_antal(),
                f"{medicin.hamta_pris()} kr",
                medicin.medicintyp()
            ),
            tags=medicin.farg()  # Används för färgkodning (recept/ej recept)
        )

def hamta_vald_medicin():
    vald = medicin_lista.selection()  # Hämtar den rad som är markerad (iid)
    return mediciner[int(vald[0])] if vald else None  # Returnerar vald medicin från listan eller "None" om ingen medicin är markerad

def ta_bort():

    medicin = hamta_vald_medicin()

    if not medicin:
        messagebox.showwarning("Fel", "Välj en medicin först.")
        return

    if messagebox.askyesno("Ta bort", f"Vill du ta bort {medicin.namn}?"):
        mediciner.remove(medicin)
        spara_mediciner() # Sparar den uppdaterade listan
        visa_mediciner() # Uppdaterar tabellen

# ---------- Start ----------

mediciner = las_mediciner()  # Läs in sparade mediciner vid start

root = tk.Tk()
root.title("Apotek 6 - Medicinregister")
root.geometry("850x650")
root.resizable(False, False)  # Lås fönsterstorleken

tk.Label(root, text="Apotek 6 - Medicinregister", font=("Arial", 20, "bold")).pack(pady=15)

# ---------- Formulär ----------

form = tk.Frame(root)
form.pack()

falt = ["Namn:", "Aktiv substans:", "Styrka:", "Antal:", "Pris:"]

entries = []

# Skapar etiketter och inmatningsfält för varje fält i formuläret
for rad, text in enumerate(falt):
    tk.Label(form, text=text).grid(row=rad, column=0, sticky="w", padx=5, pady=3)

    entry = tk.Entry(form, width=30)
    entry.grid(row=rad, column=1, padx=5, pady=3)
    entries.append(entry)

# Packar upp inmatningsfälten till separata variabler för att kunna använda dem senare
(
    namn_entry,
    substans_entry,
    styrka_entry,
    antal_entry,
    pris_entry,
) = entries  

# ---------- Receptstatus ----------

recept_var = tk.BooleanVar()  # Sparar om kryssrutan är markerad (True/False)

# Skapar en kryssruta där användaren kan välja om medicinen är receptbelagd
tk.Checkbutton(form, text="Receptbelagd medicin", variable=recept_var).grid(row=6, column=1, sticky="w", pady=5)

# ---------- Knappar ----------

knapp_frame = tk.Frame(root)
knapp_frame.pack(pady=10)

tk.Button(knapp_frame, text="Lägg till", command=lagg_till).grid(row=0, column=0, padx=5)

tk.Button(knapp_frame, text="Ta bort", command=ta_bort).grid(row=0, column=1, padx=5)

# ---------- Tabell/Treeview ----------

kolumner = ("namn", "styrka", "antal", "pris", "receptstatus")
rubriker = ("Namn", "Styrka", "Antal i lager", "Pris", "Receptstatus")

medicin_lista = ttk.Treeview(root, columns=kolumner, show="headings", height=12)

# Går igenom varje kolumn och dess rubrik för att skapa och formatera tabellen
for kolumn, rubrik in zip(kolumner, rubriker):
    medicin_lista.heading(kolumn, text=rubrik)
    medicin_lista.column(kolumn, width=150, anchor="center")

medicin_lista.pack(padx=20, pady=10)

# Färgkodning baserat på taggar ("recept" eller "ej_recept")
medicin_lista.tag_configure("recept", foreground="lightcoral")
medicin_lista.tag_configure("ej_recept", foreground="black")

visa_mediciner()  # Visar alla mediciner från fil i tabellen vid start

root.mainloop()