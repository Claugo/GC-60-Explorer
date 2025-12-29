# GC-60 Progetto ricerca numeri primi Dicembre 2025 
# Ricerca primi con il metodo di esclusione dei multipli del 3 e del 7
# Creare le sottoliste / aggiornato con nuova struttura dnella scrematura
# Aggiornato a pickle senza zeri utilizza numpy e numba per ottimizzare la scrematura
# ottimizzazione creazione liste
import time
from tkinter import messagebox
import pickle
import tkinter as tk
import numpy as np
from numba import njit

tempo = time.strftime("%H:%M:%S", time.localtime())
print("Test Programma con liste scremate dal 7 - CON NUMBA")
print()
start_time = time.monotonic()
ultimo_report = start_time


def stampa_lista_primi(lista_np):
    """Stampa la lista dei primi"""
    print(2, 3, 5, 7, end=" ")
    for i in range(len(lista_np)):
        r = i * 60 + 10
        for ii in range(16):
            if lista_np[i][ii] != 0:
                n_p = r + lista_np[i][ii]
                print(n_p, end=" ")


# Sottoliste originali
sottoliste = [
    [1, 3, 7, 9, 13, 19, 21, 27, 31, 33, 37, 0, 43, 49, 51, 57],
    [1, 3, 0, 9, 13, 19, 0, 27, 31, 33, 37, 39, 43, 0, 51, 57],
    [1, 0, 7, 9, 13, 19, 21, 27, 0, 33, 37, 39, 43, 49, 51, 57],
    [1, 3, 7, 9, 0, 19, 21, 0, 31, 33, 37, 39, 43, 49, 51, 57],
    [1, 3, 7, 0, 13, 19, 21, 27, 31, 33, 0, 39, 43, 49, 0, 57],
    [1, 3, 7, 9, 13, 0, 21, 27, 31, 0, 37, 39, 43, 49, 51, 57],
    [0, 3, 7, 9, 13, 19, 21, 27, 31, 33, 37, 39, 0, 49, 51, 0],
]

controllo = 0
# * Inserisci il numero in cui cercare i fattori primi
cerca_in = 9000000000
# ****************************************************
calcolo_sottoliste = cerca_in // 60 * 60
n_sottoliste = cerca_in // 60
if calcolo_sottoliste < cerca_in:
    n_sottoliste += 1

print(
    "tempo iniziale creazione lista",
    tempo,
    "  Ricerca su ",
    "{:,}".format(n_sottoliste * 60 + 10).replace(",", "."),
)

# ============================================================================
# OTTIMIZZAZIONE: Creazione lista veloce con numpy
# ============================================================================
# Converti sottoliste in numpy array
sottoliste_np = np.array(sottoliste, dtype=np.int32)

print("Creazione lista...")

# Calcola quante ripetizioni del pattern di 7 sottoliste servono
n_ripetizioni = (n_sottoliste // 7) + 1

# Usa np.tile per ripetere il pattern, poi taglia alla dimensione esatta
# Questo è molto più veloce del loop Python
lista_np = np.tile(sottoliste_np, (n_ripetizioni, 1))[:n_sottoliste]

print(
    f"Liste create: {n_sottoliste:,} ({n_sottoliste * 16 * 4 / 1024**3:.2f} GB)".replace(
        ",", "."
    )
)

tempo = time.strftime("%H:%M:%S", time.localtime())
print("tempo finale creazione lista", tempo)
print()

tempo = time.strftime("%H:%M:%S", time.localtime())
print("tempo inizio scrematura lista", tempo)

# ****************************************************
# * SCREMATURA CON NUMBA
# ****************************************************
numero_partenza = 11
limite = int((n_sottoliste * 60 + 10) ** 0.5) + 1


@njit
def scremare_con_numba(lista_np, numero_partenza, limite, cerca_in):
    """
    Funzione di scrematura compilata con Numba
    Identica alla logica originale
    """
    len_lista = len(lista_np)

    for i in range(numero_partenza, limite, 2):
        if i % 3 == 0 or i % 5 == 0:
            continue

        ii = i

        while True:
            # Salta multipli di 3 e 5
            while ii % 3 == 0 or ii % 5 == 0:
                ii += 2

            n_prodotto = i * ii

            # Controlli di uscita
            if n_prodotto >= cerca_in + 60:
                break

            # Calcola posizione (come divmod originale)
            p_lista, p_numero = divmod(n_prodotto - 10, 60)

            if p_lista >= len_lista:
                break

            # Cerca e sostituisci con 0 (come originale)
            for idx in range(16):
                if lista_np[p_lista, idx] == p_numero:
                    lista_np[p_lista, idx] = 0
                    break

            ii += 2

    return lista_np


# Esegui la scrematura con Numba
lista_np = scremare_con_numba(lista_np, numero_partenza, limite, cerca_in)

tempo = time.strftime("%H:%M:%S", time.localtime())
print("tempo finale scrematura lista", tempo)


# ****************************************************
# SALVATAGGIO
# ****************************************************
def scegli_formato():
    scelta = {"valore": None}

    def seleziona(val):
        scelta["valore"] = val
        root.destroy()

    root = tk.Tk()
    root.title("Salvataggio risultati")
    root.attributes("-topmost", True)
    root.geometry("360x160")
    root.resizable(False, False)

    label = tk.Label(
        root,
        text="Calcolo terminato.\nScegli il formato di salvataggio:",
        font=("Arial", 11),
        pady=20,
    )
    label.pack()

    frame = tk.Frame(root)
    frame.pack(pady=10)

    tk.Button(
        frame, text="Salva in TESTO", width=14, command=lambda: seleziona("t")
    ).pack(side="left", padx=10)

    tk.Button(
        frame, text="Salva in PICKLE", width=14, command=lambda: seleziona("p")
    ).pack(side="right", padx=10)

    root.mainloop()
    return scelta["valore"]


scelta = scegli_formato()

if scelta == "t":
    with open("lista_test_numba.txt", "w") as file:
        for i in range(len(lista_np)):
            # Filtra gli zeri dalla sotto-lista
            numeri_primi = [int(n) for n in lista_np[i] if n != 0]

            if len(numeri_primi) == 0:
                continue

            elif len(numeri_primi) == 1:
                file.write(str(i * 60 + 10 + numeri_primi[0]) + "\n")

            else:
                lista_str = " ".join(map(str, numeri_primi))
                file.write(str(i * 60 + 10) + " " + lista_str + "\n")

    print("Salvataggio in formato testo completato.")

elif scelta == "p":
    # CORREZIONE: Mantieni TUTTE le sottoliste, anche quelle vuote
    # per preservare l'indice corretto
    lista_pickle = []
    sottoliste_non_vuote = 0
    ultimo_indice_non_vuoto = -1

    for i in range(len(lista_np)):
        sottolista = [int(n) for n in lista_np[i] if n != 0]
        # Aggiungi sempre, anche se vuota!
        lista_pickle.append(sottolista)

        if sottolista:
            sottoliste_non_vuote += 1
            ultimo_indice_non_vuoto = i

    with open("lista_test_numba.pkl", "wb") as file:
        pickle.dump(lista_pickle, file)

    print("Salvataggio in formato pickle completato.")
    print(f"Totale sottoliste salvate: {len(lista_pickle):,}".replace(",", "."))
    print(f"Sottoliste con primi: {sottoliste_non_vuote:,}".replace(",", "."))
    print(
        f"Ultimo indice con primi: {ultimo_indice_non_vuoto:,} → numero base: {ultimo_indice_non_vuoto * 60 + 10:,}".replace(
            ",", "."
        )
    )

else:
    print("Scelta non valida. Usa 't' per testo o 'p' per pickle.")

tempo = time.strftime("%H:%M:%S", time.localtime())
print()
print("Tempo finale totale", tempo)

stampa_lista = messagebox.askyesno(
    "Stampa", "Vuoi stampare a video la lista dei numeri primi trovati?"
)
if stampa_lista:
    stampa_lista_primi(lista_np)
else:
    print("Programma terminato lista a video non stampata")
