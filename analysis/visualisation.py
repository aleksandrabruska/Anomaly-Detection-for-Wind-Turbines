import tkinter as tk
import pandas as pd
import matplotlib

matplotlib.use("TkAgg")  # Upewniamy się, że używamy backendu Tkinter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


def on_select(_):
    """
    Funkcja wywoływana przy zmianie wyboru w dropdown.
    Czyści poprzedni wykres i rysuje nowy dla wybranej kolumny.
    """
    selected_col = dropdown_var.get()
    fig.clear()  # Czyścimy poprzednią zawartość Figure
    ax = fig.add_subplot(111)

    # Rysujemy wykres wybranej kolumny (liniowy)
    df[selected_col].plot(ax=ax)

    ax.set_title(selected_col)
    ax.set_xlabel('Date and time')
    ax.set_ylabel(selected_col)
    ax.grid(True)

    # Odświeżenie płótna
    canvas.draw_idle()


# 1. Wczytaj CSV
#csv_file = f"Kelmarsh_SCADA_2021_3087\Turbine_Data_Kelmarsh_1_2021-01-01_-_2021-07-01_228.csv"
csv_file = f"..\Kelmarsh\Turbine_Data_Kelmarsh_1_2021-01-01_-_2021-07-01_228.csv"

df = pd.read_csv(
    csv_file,
    comment='#',           # pomijamy wiersze zaczynające się od '#'
    parse_dates=['Date and time'],  # konwertuj tę kolumnę na typ daty
    na_values=["NaN"],     # jawnie mówimy, że "NaN" to brakująca wartość
    header = 1              #inaczej wybiera mi nieprawidłowy wiwersz
)



# Ustaw index na datę i czas, jeśli chcesz rysować wykresy "time series"
df.set_index('Date and time', inplace=True)



# 2. Tworzymy główne okno
root = tk.Tk()
root.title("Wybór kolumny i wykres")
root.geometry("900x600")  # Ustawiamy początkowy rozmiar okna
root.resizable(True, True) # Możemy swobodnie zmieniać rozmiar okna

# 3. Dropdown (OptionMenu) – lista rozwijana z nazwami kolumn
dropdown_var = tk.StringVar(value=df.columns[0])  # domyślna wartość
dropdown = tk.OptionMenu(root, dropdown_var, *df.columns, command=on_select)
dropdown.config(width=50)  # opcjonalnie ustaw szerokość widgetu
dropdown.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

# 4. Kontener (Frame) na wykres, by łatwiej nim zarządzać
frame_plot = tk.Frame(root)
frame_plot.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# 5. Tworzymy obiekt Figure (Matplotlib) i osadzamy go w tkinter
fig = Figure(figsize=(5, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=frame_plot)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# 6. Dodajemy toolbar Matplotlib (nawigacja do zoomowania, przesuwania, zapisu)
toolbar = NavigationToolbar2Tk(canvas, frame_plot)
toolbar.update()
toolbar.pack(side=tk.BOTTOM, fill=tk.X)

# 7. Na starcie narysujmy domyślną kolumnę
on_select(None)

# 8. Uruchom główną pętlę zdarzeń tkinter
root.mainloop()
