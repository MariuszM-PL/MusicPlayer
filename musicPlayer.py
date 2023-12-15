
# Importowanie modułu Tkinter, który umożliwia tworzenie interfejsu graficznego
import tkinter as tk
# Importowanie modułów filedialog, END, StringVar, Menu z modułu Tkinter aby mieć wybór plików
# plus menu kontekstowe do usuwania piosenek z listboxa
from tkinter import filedialog, StringVar, Menu
# Importowanie modułu ImageTk i Image z biblioteki PIL (Python Imaging Library) aby wczytać obrazki do przycisków
from PIL import ImageTk, Image
# Importowanie modułu os do interakcji z systemem operacyjnym aby wskazać folder z muzyką
import os
# Wyłączenie wiadomości domyślnej z modułu Pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
# Importowanie modułu mixer z biblioteki Pygame do obsługi dźwięku
from pygame import mixer
# Importowanie modułu time do obsługi czasu piosenki
import time

# Zmienna globalna do przechowywania bieżącego czasu
current_time_seconds = 0
# Zmienna globalna do przechowywania czasu rozpoczęcia odtwarzania
start_time = 0
# Zmienną globalna do przechowywania bieżącego indeksu
current_index = 0
# Lista do przechowywania piosenek wczytanych
songs = []


def create_button(image_path, command, row, column):
    # Otwieranie obrazka z ścieżki przekazanej jako argument
    img = Image.open(image_path)
    # Dostosowywanie rozmiaru obrazka do 50x50 pikseli
    img = img.resize((50, 50))
    # Konwersja obrazka do obiektu PhotoImage dla Tkinter
    img = ImageTk.PhotoImage(img)
    # Tworzenie przycisku Tkinter z obrazkiem, ustawienie parametrów
    btn = tk.Button(buttonframe, width=50, height=40, image=img, padx=50, font="Ivy 10", command=command, bd=0,
                    highlightthickness=0)
    # Umieszczenie przycisku w oknie grid o określonym rzędzie i kolumnie
    btn.grid(row=row, column=column)
    # Zachowanie referencji do obiektu PhotoImage, aby uniknąć problemów z garbage collector'em
    btn.image = img
    # Zwrócenie utworzonego przycisku
    return btn


def play_music():
    # Odtwarzanie wybranego utworu
    play_selected_song()


def play_selected_song(index=None):
    global current_index, start_time
    # Pobranie zaznaczonego indeksu z listboxa lub przekazanego indeksu jako argument
    if index is not None:
        selected_index = index
    else:
        selected_index = listbox.curselection()
    # Sprawdza, czy zmienna selected_index jest liczbą całkowitą
    if isinstance(selected_index, int):
        current_index = selected_index
    # Jeśli selected_index nie jest liczbą całkowitą, ale istnieje (nie jest puste)
    elif selected_index:
        current_index = selected_index[0]
    # Jeśli selected_index nie jest ani liczbą całkowitą, ani nie istnieje
    else:
        current_index = 0
    # Pobranie ścieżki do wybranego utworu
    running = songs[current_index]
    # Ustawienie etykiety 'running_song' na nazwę artysty i tytuł wybranego utworu
    running_song['text'] = extract_artist_title(os.path.basename(running))
    # Wczytanie wybranego utworu i rozpoczęcie odtwarzania
    mixer.music.load(running)
    # Ustaw bieżący czas na zero
    start_time = 0
    # Ustaw aktualny czas dla funkcji mixer.music.play()
    mixer.music.play(start=start_time)
    # Ustawienie głośności na podstawie aktualnej wartości suwaka głośności
    set_volume(volume_bar.get())
    # Rozpoczęcie aktualizacji czasu trwania utworu
    update_current_time()


def extract_artist_title(file_name):
    # Wyodrębnienie artysty i tytułu z nazwy pliku
    parts = file_name.split(" - ")  # Podzielenie nazwy pliku na części, używając separatora " - "
    if len(parts) >= 2:  # Sprawdzenie, czy są przynajmniej dwie części
        artist, title = parts[0], parts[1].split(".")[
            0]  # Wyodrębnienie artysty i tytułu, eliminując rozszerzenie pliku
        return f"{artist} - {title}"  # Zwrócenie sformatowanego tekstu "Artysta - Tytuł"
    else:
        return file_name  # Jeśli nie można wyodrębnić artysty i tytułu, zwróć oryginalną nazwę pliku


def update_current_time():
    global current_time_seconds
    # Sprawdzenie, czy muzyka jest nadal odtwarzana
    if mixer.music.get_busy():
        # Jeśli muzyka jest odtwarzana, pobierz aktualny czas
        current_time_seconds = mixer.music.get_pos() // 1000
        # Aktualizacja etykiety z aktualnym czasem piosenki
        current_time_label['text'] = f"Aktualny czas: {time.strftime('%M:%S', time.gmtime(current_time_seconds))}"
        current_time_label.after(1000, update_current_time)


def pause_music():
    # Wstrzymanie odtwarzania muzyki
    mixer.music.pause()


def continue_music():
    # Kontynuacja odtwarzania muzyki po wstrzymaniu
    mixer.music.unpause()
    # Odświeża aktualny czas piosenki jaki był w momencie pauzy
    update_current_time()


def reset_current_time():
    # Resetuje label z aktualnym czasem piosenki
    current_time_label['text'] = "Aktualny czas: 00:00"


def stop_music():
    # Zatrzymanie odtwarzania muzyki
    mixer.music.stop()
    # Zresetowanie czasu aktualnej piosenki
    reset_current_time()


def next_song():
    # Ustalenie, że zmienna current_index jest zmienną globalną
    global current_index
    # Sprawdzenie, czy zwiększenie current_index o 1 nie wykracza poza zakres listy songs
    if current_index + 1 < len(songs):
        # Jeśli warunek jest spełniony, zwiększ current_index o 1
        current_index += 1
        # Wydrukowanie indeksu bieżącego utworu w celach informacyjnych
        print(f"Indeks piosenki z listboxa (następnej): {current_index}")
        # Wywołanie funkcji odtwarzającej wybrany utwór, przekazując nowy indeks
        play_selected_song(index=current_index)
        # Pobranie ścieżki do następnego utworu
        playing = songs[current_index]
        # Wczytanie i odtworzenie następnego utworu
        mixer.music.load(playing)
        mixer.music.play()
        # Wyczyszczenie listboxa przed dodaniem nowych elementów
        listbox.delete(0, tk.END)
        # Aktualizacja listy utworów w listboxie
        show()
        # Ustawienie zaznaczenia na aktualny indeks w listboxie
        listbox.select_set(current_index)
        # Ustawienie etykiety z aktualnie odtwarzanym utworem na nazwę artysty i tytuł
        running_song['text'] = extract_artist_title(os.path.basename(playing))
        # Rozpoczęcie aktualizacji czasu trwania utworu po przejściu do następnego utworu
        update_current_time()


def previous_song():
    # Ustalenie, że zmienna current_index jest zmienną globalną
    global current_index
    # Sprawdzenie, czy zmniejszenie current_index o 1 nie wykracza poniżej 0
    if current_index - 1 >= 0:
        # Jeśli warunek jest spełniony, zmniejsz current_index o 1
        current_index -= 1
        # Wydrukowanie indeksu bieżącego utworu w celach informacyjnych
        print(f"Indeks piosenki z listboxa (poprzedniej): {current_index}")
        # Wywołanie funkcji odtwarzającej wybrany utwór, przekazując nowy indeks
        play_selected_song(index=current_index)
        # Pobranie ścieżki do poprzedniego utworu
        playing = songs[current_index]
        # Wczytanie i odtworzenie poprzedniego utworu
        mixer.music.load(playing)
        mixer.music.play()
        # Wyczyszczenie listboxa przed dodaniem nowych elementów
        listbox.delete(0, tk.END)
        # Aktualizacja listy utworów w listboxie
        show()
        # Ustawienie zaznaczenia na aktualny indeks w listboxie
        listbox.select_set(current_index)
        # Ustawienie etykiety z aktualnie odtwarzanym utworem na nazwę artysty i tytuł
        running_song['text'] = extract_artist_title(os.path.basename(playing))
        # Rozpoczęcie aktualizacji czasu trwania utworu po przejściu do poprzedniego utworu
        update_current_time()


# Funkcja do wybierania plików MP3
def browse_files():
    # Otwórz okno dialogowe do wyboru plików MP3 i pobierz wybrane ścieżki do plików
    file_paths = filedialog.askopenfilenames(filetypes=[("MP3 files", "*.mp3")])
    if file_paths:
        # Zmiana bieżącego katalogu na katalog, w którym znajduje się pierwszy wybrany plik
        os.chdir(os.path.dirname(file_paths[0]))
        # Przypisanie ścieżek z piosenek do globalnej listy songs
        global songs
        songs = list(file_paths)
        # Wyczyszczenie listboxa przed dodaniem nowych elementów
        listbox.delete(0, tk.END)
        # Aktualizacja listy utworów w listboxie
        show()


def remove_selected_song():
    # Usuwanie wybranego utworu z listboxa poprzez menu kontekstowe
    global current_index
    selected_index = listbox.curselection()
    if selected_index:
        # Usunięcie zaznaczonego utworu z listy
        songs.pop(selected_index[0])
        # Wyczyszczenie listboxa przed dodaniem nowych elementów
        listbox.delete(0, tk.END)
        # Aktualizacja listy utworów w listboxie
        show()
        # Jeśli usuwany utwór jest przed obecnie odtwarzanym, zmniejszenie bieżącego indeksu
        if selected_index[0] < current_index:
            current_index -= 1
        # Jeśli usuwany utwór jest obecnie odtwarzany, zatrzymanie odtwarzania
        elif selected_index[0] == current_index:
            mixer.music.stop()
        # Wczytanie i odtworzenie poprzedniego utworu
        if current_index >= 0 and current_index < len(songs):
            # Sprawdzenie, czy bieżący indeks mieści się w zakresie dostępnych utworów
            playing = songs[current_index]
            # Wczytanie i odtworzenie utworu na podstawie bieżącego indeksu
            mixer.music.load(playing)
            mixer.music.play()
            # Zaznaczenie utworu na liście utworów
            listbox.select_set(current_index)
            # Ustawienie etykiety z aktualnie odtwarzanym utworem na nazwę pliku
            running_song['text'] = playing
            # Ustawienie głośności na podstawie aktualnej wartości suwaka
            set_volume(volume_bar.get())
            # Rozpoczęcie aktualizacji czasu trwania utworu po przejściu do poprzedniego utworu
            update_current_time()
        else:
            # Jeśli nie ma więcej utworów, zresetowanie bieżącego indeksu
            current_index = 0


def set_volume(value):
    # Ustawienie głośności na podstawie wartości suwaka
    volume = int(value)
    # Ustawienie głośności od 0.0 do 1.0
    mixer.music.set_volume(volume / 100)


def show():
    # Ustalenie, że zmienna current_index jest zmienną globalną
    global current_index

    # Pętla przechodząca przez elementy listy songs razem z ich indeksami
    for i, song_path in enumerate(songs):
        # Pobranie długości utworu za pomocą funkcji get_song_length
        song_length = get_song_length(song_path)
        # Formatowanie długości utworu do postaci MM:SS
        formatted_length = time.strftime('%M:%S', time.gmtime(song_length))
        # Wyodrębnienie nazwy utworu z pełnej ścieżki
        song_name = os.path.basename(song_path)
        # Utworzenie tekstu etykiety zawierającej nazwę utworu i jego długość w formacie MM:SS
        label_text = f"{song_name} - {formatted_length}"
        # Sprawdzenie, czy indeks (i) jest mniejszy niż liczba elementów w listboxie
        if i < listbox.size():
            # Jeśli etykieta już istnieje, zaktualizuj jej tekst
            listbox.itemconfig(i, {'text': label_text})
        else:
            # W przeciwnym razie, utwórz nową etykietę
            listbox.insert(tk.END, label_text)
        # Zaznacz aktualny utwór w listboxie
        if i == current_index:
            # Zaznaczenie elementu o indeksie i w listboxie
            listbox.select_set(i)


def get_song_length(song_path):
    # Pobranie długości utworu
    return mixer.Sound(song_path).get_length()


# Główne okno aplikacji
window = tk.Tk() # Tworzenie głównego okna aplikacji
window.geometry("450x650")  # Ustawienie rozmiaru okna głównego
window.title("Music Player")  # Ustawienie tytułu okna głównego
window.configure(background="#FDCA40")  # Ustawienie koloru tła okna głównego
window.resizable(width=False, height=False)  # Uniemożliwienie zmiany rozmiaru okna głównego

# Title Frame
title_frame = tk.Frame(window, pady=10, bg="#31393C")  # Utworzenie ramki dla tytułu
title_frame.columnconfigure(0, weight=1)  # Konfiguracja kolumny ramki
title_label = tk.Label(title_frame, text="🎵     Music Player    🎵", font=('Comic Sans MS', 18, "bold"), fg="#FDCA40", bg="#31393C", padx=175, pady=10)  # Utworzenie etykiety tytułu
title_label.grid(row=0, column=0)  # Umieszczenie etykiety w ramce

# Name Song Frame
name_song_frame = tk.Frame(window, pady=20, bg="#FDCA40")  # Utworzenie ramki dla nazwy utworu
running_song = tk.Label(name_song_frame, text="Tytuł utworu", font=("Comic Sans MS", 11, "bold"), width=50, pady=20, bg="#31393C", fg="#FDCA40", anchor=tk.CENTER)  # Utworzenie etykiety nazwy utworu
running_song.grid(row=1, column=0)  # Umieszczenie etykiety w ramce

# Playlist Frame
playlist_frame = tk.Frame(window, pady=10, bg="#FDCA40")  # Utworzenie ramki dla listy odtwarzania
playlist_frame.columnconfigure(1, weight=1)  # Konfiguracja kolumny ramki

# Poziomy Scrollbar w playliście
xscrollbar = tk.Scrollbar(playlist_frame, orient="horizontal")  # Utworzenie poziomego paska przewijania
xscrollbar.grid(row=3, column=0, sticky="ew")  # Umieszczenie paska przewijania w ramce

listbox = tk.Listbox(
    playlist_frame,  # Utworzenie listboxa w ramce playlist_frame
    selectmode="SINGLE",  # Ustawienie trybu zaznaczania na pojedyncze zaznaczenie
    font=("Comic Sans MS", 9, "bold"),  # Ustawienie czcionki
    height=8,  # Ustawienie liczby widocznych elementów na 8
    width=45,  # Ustawienie szerokości listboxa na 45
    bg="#31393C",  # Ustawienie koloru tła
    fg="#FDCA40",  # Ustawienie koloru tekstu
    highlightthickness=2,  # Ustawienie szerokości obramowania zaznaczonego elementu
    xscrollcommand=xscrollbar.set  # Połącz pasek przewijania z listboxem
)
listbox.grid(row=2, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")  # Umieszczenie listboxa w ramce
xscrollbar.config(command=listbox.xview)  # Ustawienie paska przewijania w poziomie

# Pionowy Scrollbar w playliście
# Utworzenie pionowego paska przewijania
scrollbar = tk.Scrollbar(playlist_frame, orient="vertical", command=listbox.yview, bg="#31393C")
scrollbar.grid(row=2, column=2, sticky="ns")  # Umieszczenie paska przewijania w ramce
listbox.config(yscrollcommand=scrollbar.set)  # Połącz pasek przewijania z listboxem w pionie

# Volume Frame
volume_frame = tk.Frame(window, bg="#FDCA40")  # Utworzenie ramki dla suwaka głośności
volume_bar = tk.Scale(volume_frame, from_=0, to=100, orient=tk.HORIZONTAL, font=("Comic Sans MS", 8, "bold"), label="Vol (%)", resolution=1, length=240, width=15, bg="#31393C", fg="#FDCA40", highlightthickness=0)  # Utworzenie suwaka głośności
volume_bar.set(100)  # Ustawienie początkowej wartości suwaka
volume_bar.grid(row=3, column=1, padx=(30, 0))  # Umieszczenie suwaka w ramce
volume_bar.config(command=lambda value: set_volume(value))  # Ustawienie funkcji obsługi zmiany wartości suwaka

# Current Song Time Frame
current_time_frame = tk.Frame(window, pady=10, bg="#FDCA40")  # Utworzenie ramki dla aktualnego czasu trwania utworu
current_time_label = tk.Label(current_time_frame, text="Aktualny czas: 00:00", font=("Comic Sans MS", 12, "bold"), bg="#FDCA40", fg="#31393C")  # Utworzenie etykiety aktualnego czasu
current_time_label.grid(row=0, column=0)  # Umieszczenie etykiety w siatce

# Buttons Frames
buttonframe = tk.Frame(window, pady=30, bg="#FDCA40")  # Utworzenie ramki dla przycisków
buttonframe.columnconfigure(0, weight=1)  # Konfiguracja kolumn ramki
play_btn = create_button('Icons/play.png', play_music, 4, 1)  # Utworzenie przycisku play
prev_btn = create_button('Icons/rewind.png', previous_song, 4, 0)  # Utworzenie przycisku poprzedniego utworu
next_btn = create_button('Icons/fast-forward.png', next_song, 4, 2)  # Utworzenie przycisku następnego utworu
pause_btn = create_button('Icons/pause.png', pause_music, 4, 3)  # Utworzenie przycisku pauzy
stop_btn = create_button('Icons/stop.png', stop_music, 4, 4)  # Utworzenie przycisku stop
continue_btn = create_button('Icons/continue.png', continue_music, 4, 5)  # Utworzenie przycisku kontynuacji

# Przycisk Przeglądaj
browse_img = Image.open('Icons/browse.png')  # Wczytanie obrazka dla przycisku Przeglądaj
browse_img = browse_img.resize((75, 75))  # Dostosowanie rozmiaru obrazka
browse_img = ImageTk.PhotoImage(browse_img)  # Konwersja obrazka do formatu obsługiwanego przez tkinter
# Utworzenie przycisku z obrazkiem i przypisanie funkcji obsługi
browse_btn = tk.Button(volume_frame, image=browse_img, command=browse_files, bd=0, highlightthickness=0)
# Umieszczenie przycisku w gridzie okna aplikacji
browse_btn.grid(row=3, column=0, padx=(0, 5))
# Zachowanie referencji do obrazka, aby uniknąć problemów z garbage collectorem
browse_btn.image = browse_img

# Przycisk Power-Off
exitframe = tk.Frame(window, pady=0, bg="#FDCA40")  # Utworzenie ramki dla przycisku wyjścia
exitframe.columnconfigure(0, weight=1)  # Konfiguracja kolumny ramki
exit_img = Image.open('Icons/exit.png')  # Wczytanie obrazka dla przycisku Wyjścia
exit_img = exit_img.resize((50, 50))  # Dostosowanie rozmiaru obrazka
exit_img = ImageTk.PhotoImage(exit_img)  # Konwersja obrazka do formatu obsługiwanego przez tkinter
exit_btn = tk.Button(exitframe, width=50, height=50, image=exit_img, padx=50, font="Ivy 10", command=window.destroy, bd=0, highlightthickness=0)  # Utworzenie przycisku z obrazkiem i przypisanie funkcji obsługi
exit_btn.grid(row=5, column=0)  # Umieszczenie przycisku w oknie
exit_btn.image = exit_img  # Zachowanie referencji do obrazka, aby uniknąć problemów z garbage collectorem


# Kliknięcie prawym przyciskiem myszy w listboxie, aby wyświetlić menu kontekstowe i usunąć wybrany utwór
listbox.bind("<Double-1>", lambda event: play_selected_song())
# Utworzenie menu kontekstowego
context_menu = Menu(window, tearoff=0)
# Dodanie opcji "Usuń zaznaczony" do menu
context_menu.add_command(label="Usuń zaznaczony", command=remove_selected_song)
# Przypisanie wyświetlania menu kontekstowego na prawy przycisk myszy
listbox.bind("<Button-3>", lambda event: context_menu.post(event.x_root, event.y_root))


# Załadowanie wszystkich framów z GUI do głównego okna aplikacji
# Dodanie ramki tytułowej do głównego okna
title_frame.pack()
# Dodanie ramki z nazwą odtwarzanego utworu do głównego okna
name_song_frame.pack()
# Dodanie ramki listboxa odtwarzania do głównego okna
playlist_frame.pack()
# Dodanie ramki suwaka głośności do głównego okna
volume_frame.pack()
# Dodanie ramki z aktualnym czasem trwania utworu do głównego okna
current_time_frame.pack()
# Dodanie ramki przycisków do głównego okna
buttonframe.pack()
# Dodanie ramki wyjścia do głównego okna
exitframe.pack()


# Wywołanie funkcji interującej listę songs[]
show()

# Inicjalizacja modułu dźwiękowego Pygame
mixer.init()

# Utworzenie zmiennej Tkinter typu StringVar, która będzie używana do przechowywania stanu aplikacji związanego z muzyką
music_state = StringVar()

# Uruchomienie głównej pętli zdarzeń Tkinter, która utrzymuje program w działaniu
window.mainloop()

