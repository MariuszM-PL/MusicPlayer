# Importing the Tkinter module for creating a graphical interface
import tkinter as tk
# Importing filedialog, END, StringVar, Menu modules from Tkinter for file selection
# plus context menu for removing songs from the listbox
from tkinter import filedialog, StringVar, Menu
# Importing the ImageTk and Image modules from the PIL (Python Imaging Library) to load images into buttons
from PIL import ImageTk, Image
# Importing the os module for interaction with the operating system to specify the music folder
import os
# Turning off the default message from the Pygame module
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
# Importing the mixer module from the Pygame library for sound handling
from pygame import mixer
# Importing the time module for handling song duration
import time

# Global variable to store the current time
current_time_seconds = 0
# Global variable to store the start time of playback
start_time = 0
# Global variable to store the current index
current_index = 0
# List to store loaded songs
songs = []


def create_button(image_path, command, row, column):
    # Opening the image from the provided path
    img = Image.open(image_path)
    # Adjusting the image size to 50x50 pixels
    img = img.resize((50, 50))
    # Converting the image to a PhotoImage object for Tkinter
    img = ImageTk.PhotoImage(img)
    # Creating a Tkinter button with the image, setting parameters
    btn = tk.Button(buttonframe, width=50, height=40, image=img, padx=50, font="Ivy 10", command=command, bd=0,
                    highlightthickness=0)
    # Placing the button in the grid with a specified row and column
    btn.grid(row=row, column=column)
    # Keeping a reference to the PhotoImage object to avoid garbage collector issues
    btn.image = img
    # Returning the created button
    return btn


def play_music():
    # Playing the selected song
    play_selected_song()


def play_selected_song(index=None):
    global current_index, start_time
    # Getting the selected index from the listbox or the provided index as an argument
    if index is not None:
        selected_index = index
    else:
        selected_index = listbox.curselection()
    # Checking if the selected_index variable is an integer
    if isinstance(selected_index, int):
        current_index = selected_index
    # If selected_index is not an integer but exists (not empty)
    elif selected_index:
        current_index = selected_index[0]
    # If selected_index is neither an integer nor exists
    else:
        current_index = 0
    # Getting the path to the selected song
    running = songs[current_index]
    # Setting the 'running_song' label to the artist and title of the selected song
    running_song['text'] = extract_artist_title(os.path.basename(running))
    # Loading the selected song and starting playback
    mixer.music.load(running)
    # Setting the current time to zero
    start_time = 0
    # Setting the current time for the mixer.music.play() function
    mixer.music.play(start=start_time)
    # Setting the volume based on the current volume slider value
    set_volume(volume_bar.get())
    # Starting the update of the song duration
    update_current_time()


def extract_artist_title(file_name):
    # Extracting the artist and title from the file name
    parts = file_name.split(" - ")  # Splitting the file name into parts using the separator " - "
    if len(parts) >= 2:  # Checking if there are at least two parts
        artist, title = parts[0], parts[1].split(".")[0]  # Extracting the artist and title, removing the file extension
        return f"{artist} - {title}"  # Returning the formatted text "Artist - Title"
    else:
        return file_name  # If unable to extract the artist and title, return the original file name


def update_current_time():
    global current_time_seconds
    # Checking if the music is still playing
    if mixer.music.get_busy():
        # If the music is playing, get the current time
        current_time_seconds = mixer.music.get_pos() // 1000
        # Updating the label with the current song time
        current_time_label['text'] = f"Current time: {time.strftime('%M:%S', time.gmtime(current_time_seconds))}"
        current_time_label.after(1000, update_current_time)


def pause_music():
    # Pausing the music playback
    mixer.music.pause()


def continue_music():
    # Resuming music playback after pause
    mixer.music.unpause()
    # Refreshing the current song time that was present at the time of pause
    update_current_time()


def reset_current_time():
    # Resetting the label with the current song time
    current_time_label['text'] = "Current time: 00:00"


def stop_music():
    # Stopping music playback
    mixer.music.stop()
    # Resetting the time of the current song
    reset_current_time()


def next_song():
    # Ensuring that the current_index variable is a global variable
    global current_index
    # Checking if increasing current_index by 1 does not exceed the range of the songs list
    if current_index + 1 < len(songs):
        # If the condition is met, increase current_index by 1
        current_index += 1
        # Printing the index of the current song for informational purposes
        print(f"Index of the song from the listbox (next): {current_index}")
        # Calling the function to play the selected song, passing the new index
        play_selected_song(index=current_index)
        # Getting the path to the next song
        playing = songs[current_index]
        # Loading and playing the next song
        mixer.music.load(playing)
        mixer.music.play()
        # Clearing the listbox before adding new items
        listbox.delete(0, tk.END)
        # Updating the list of songs in the listbox
        show()
        # Setting the selection to the current index in the listbox
        listbox.select_set(current_index)
        # Setting the label with the currently playing song to the artist and title
        running_song['text'] = extract_artist_title(os.path.basename(playing))
        # Starting the update of the song duration after moving to the next song
        update_current_time()


def previous_song():
    # Ensuring that the current_index variable is a global variable
    global current_index
    # Checking if decreasing current_index by 1 does not go below 0
    if current_index - 1 >= 0:
        # If the condition is met, decrease current_index by 1
        current_index -= 1
        # Printing the index of the current song for informational purposes
        print(f"Index of the song from the listbox (previous): {current_index}")
        # Calling the function to play the selected song, passing the new index
        play_selected_song(index=current_index)
        # Getting the path to the previous song
        playing = songs[current_index]
        # Loading and playing the previous song
        mixer.music.load(playing)
        mixer.music.play()
        # Clearing the listbox before adding new items
        listbox.delete(0, tk.END)
        # Updating the list of songs in the listbox
        show()
        # Setting the selection to the current index in the listbox
        listbox.select_set(current_index)
        # Setting the label with the currently playing song to the artist and title
        running_song['text'] = extract_artist_title(os.path.basename(playing))
        # Starting the update of the song duration after moving to the previous song


# Function for selecting MP3 files
def browse_files():
    # Open a file dialog for choosing MP3 files and get the selected file paths
    file_paths = filedialog.askopenfilenames(filetypes=[("MP3 files", "*.mp3")])
    if file_paths:
        # Change the current directory to the directory containing the first selected file
        os.chdir(os.path.dirname(file_paths[0]))
        # Assign the paths from the songs to the global list songs
        global songs
        songs = list(file_paths)
        # Clearing the listbox before adding new items
        listbox.delete(0, tk.END)
        # Updating the list of songs in the listbox
        show()


def remove_selected_song():
    # Removing the selected song from the listbox through the context menu
    global current_index
    selected_index = listbox.curselection()
    if selected_index:
        # Removing the selected song from the list
        songs.pop(selected_index[0])
        # Clearing the listbox before adding new items
        listbox.delete(0, tk.END)
        # Updating the list of songs in the listbox
        show()
        # If the removed song is before the currently playing one, decrease the current index
        if selected_index[0] < current_index:
            current_index -= 1
        # If the removed song is currently playing, stop playback
        elif selected_index[0] == current_index:
            mixer.music.stop()
        # Loading and playing the previous song
        if current_index >= 0 and current_index < len(songs):
            # Checking if the current index is within the range of available songs
            playing = songs[current_index]
            # Loading and playing the song based on the current index
            mixer.music.load(playing)
            mixer.music.play()
            # Selecting the song in the list of songs
            listbox.select_set(current_index)
            # Setting the label with the currently playing song to the file name
            running_song['text'] = playing
            # Setting the volume based on the current slider value
            set_volume(volume_bar.get())
            # Starting the update of the song duration after moving to the previous song
            update_current_time()
        else:
            # If there are no more songs, reset the current index
            current_index = 0


def set_volume(value):
    # Setting the volume based on the slider value
    volume = int(value)
    # Setting the volume from 0.0 to 1.0
    mixer.music.set_volume(volume / 100)


def show():
    # Ensuring that the current_index variable is a global variable
    global current_index

    # Loop through the elements of the songs list along with their indices
    for i, song_path in enumerate(songs):
        # Getting the length of the song using the get_song_length function
        song_length = get_song_length(song_path)
        # Formatting the song length to the MM:SS format
        formatted_length = time.strftime('%M:%S', time.gmtime(song_length))
        # Extracting the song name from the full path
        song_name = os.path.basename(song_path)
        # Creating the text of the label containing the song name and its length in the MM:SS format
        label_text = f"{song_name} - {formatted_length}"
        # Checking if the index (i) is less than the number of elements in the listbox
        if i < listbox.size():
            # If the label already exists, update its text
            listbox.itemconfig(i, {'text': label_text})
        else:
            # Otherwise, create a new label
            listbox.insert(tk.END, label_text)
        # Select the current song in the listbox
        if i == current_index:
            # Selecting the element at index i in the listbox
            listbox.select_set(i)


def get_song_length(song_path):
    # Getting the length of the song
    return mixer.Sound(song_path).get_length()


# Main application window
window = tk.Tk()  # Creating the main application window
window.geometry("450x650")  # Setting the size of the main window
window.title("Music Player")  # Setting the title of the main window
window.configure(background="#FDCA40")  # Setting the background color of the main window
window.resizable(width=False, height=False)  # Preventing resizing of the main window

# Title Frame
title_frame = tk.Frame(window, pady=10, bg="#31393C")  # Creating a frame for the title
title_frame.columnconfigure(0, weight=1)  # Configuring the column of the frame
title_label = tk.Label(title_frame, text="🎵     Music Player    🎵", font=('Comic Sans MS', 18, "bold"), fg="#FDCA40", bg="#31393C", padx=175, pady=10)  # Creating the title label
title_label.grid(row=0, column=0)  # Placing the label in the frame

# Name Song Frame
name_song_frame = tk.Frame(window, pady=20, bg="#FDCA40")  # Creating a frame for the song name
running_song = tk.Label(name_song_frame, text="Tytuł utworu", font=("Comic Sans MS", 11, "bold"), width=50, pady=20, bg="#31393C", fg="#FDCA40", anchor=tk.CENTER)  # Creating the label for the song name
running_song.grid(row=1, column=0)  # Placing the label in the frame

# Playlist Frame
playlist_frame = tk.Frame(window, pady=10, bg="#FDCA40")  # Creating a frame for the playlist
playlist_frame.columnconfigure(1, weight=1)  # Configuring the column of the frame

# Horizontal Scrollbar in the playlist
xscrollbar = tk.Scrollbar(playlist_frame, orient="horizontal")  # Creating a horizontal scrollbar
xscrollbar.grid(row=3, column=0, sticky="ew")  # Placing the scrollbar in the frame

listbox = tk.Listbox(
    playlist_frame,  # Creating a listbox in the playlist_frame
    selectmode="SINGLE",  # Setting the selection mode to single
    font=("Comic Sans MS", 9, "bold"),  # Setting the font
    height=8,  # Setting the number of visible items to 8
    width=45,  # Setting the width of the listbox to 45
    bg="#31393C",  # Setting the background color
    fg="#FDCA40",  # Setting the text color
    highlightthickness=2,  # Setting the width of the selected item border
    xscrollcommand=xscrollbar.set  # Connecting the horizontal scrollbar to the listbox
)
listbox.grid(row=2, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")  # Placing the listbox in the frame
xscrollbar.config(command=listbox.xview)  # Setting the horizontal scrollbar

# Vertical Scrollbar in the playlist
scrollbar = tk.Scrollbar(playlist_frame, orient="vertical", command=listbox.yview, bg="#31393C")  # Creating a vertical scrollbar
scrollbar.grid(row=2, column=2, sticky="ns")  # Placing the scrollbar in the frame
listbox.config(yscrollcommand=scrollbar.set)  # Connecting the vertical scrollbar to the listbox

# Volume Frame
volume_frame = tk.Frame(window, bg="#FDCA40")  # Creating a frame for the volume slider
volume_bar = tk.Scale(volume_frame, from_=0, to=100, orient=tk.HORIZONTAL, font=("Comic Sans MS", 8, "bold"), label="Vol (%)", resolution=1, length=240, width=15, bg="#31393C", fg="#FDCA40", highlightthickness=0)  # Creating the volume slider
volume_bar.set(100)  # Setting the initial value of the slider
volume_bar.grid(row=3, column=1, padx=(30, 0))  # Placing the slider in the frame
volume_bar.config(command=lambda value: set_volume(value))  # Setting the callback for value changes

# Current Song Time Frame
current_time_frame = tk.Frame(window, pady=10, bg="#FDCA40")  # Creating a frame for the current song time
current_time_label = tk.Label(current_time_frame, text="Aktualny czas: 00:00", font=("Comic Sans MS", 12, "bold"), bg="#FDCA40", fg="#31393C")  # Creating the label for the current time
current_time_label.grid(row=0, column=0)  # Placing the label in the grid

# Buttons Frames
buttonframe = tk.Frame(window, pady=30, bg="#FDCA40")  # Creating a frame for the buttons
buttonframe.columnconfigure(0, weight=1)  # Configuring the column of the frame
play_btn = create_button('Icons/play.png', play_music, 4, 1)  # Creating the play button
prev_btn = create_button('Icons/rewind.png', previous_song, 4, 0)  # Creating the previous song button
next_btn = create_button('Icons/fast-forward.png', next_song, 4, 2)  # Creating the next song button
pause_btn = create_button('Icons/pause.png', pause_music, 4, 3)  # Creating the pause button
stop_btn = create_button('Icons/stop.png', stop_music, 4, 4)  # Creating the stop button
continue_btn = create_button('Icons/continue.png', continue_music, 4, 5)  # Creating the continue button

# Browse Button
browse_img = Image.open('Icons/browse.png')  # Loading the image for the Browse button
browse_img = browse_img.resize((75, 75))  # Resizing the image
browse_img = ImageTk.PhotoImage(browse_img)  # Converting the image to a format supported by Tkinter
browse_btn = tk.Button(volume_frame, image=browse_img, command=browse_files, bd=0, highlightthickness=0)  # Creating the Browse button
browse_btn.grid(row=3, column=0, padx=(0, 5))  # Placing the button in the window
browse_btn.image = browse_img  # Keeping a reference to the image to avoid garbage collection

# Power-Off Button
exitframe = tk.Frame(window, pady=0, bg="#FDCA40")  # Creating a frame for the exit button
exitframe.columnconfigure(0, weight=1)  # Configuring the frame column
exit_img = Image.open('Icons/exit.png')  # Loading the image for the exit button
exit_img = exit_img.resize((50, 50))  # Adjusting the image size
exit_img = ImageTk.PhotoImage(exit_img)  # Converting the image to a format supported by Tkinter
exit_btn = tk.Button(exitframe, width=50, height=50, image=exit_img, padx=50, font="Ivy 10", command=window.destroy, bd=0, highlightthickness=0)  # Creating a button with an image and assigning a handling function
exit_btn.grid(row=5, column=0)  # Placing the button in the window
exit_btn.image = exit_img  # Keeping a reference to the image to avoid garbage collector issues


# Right-click in the listbox to display a context menu and remove the selected song
listbox.bind("<Double-1>", lambda event: play_selected_song())
# Creating a context menu
context_menu = Menu(window, tearoff=0)
# Adding "Remove Selected" option to the menu
context_menu.add_command(label="Remove Selected", command=remove_selected_song)
# Binding the display of the context menu to the right mouse button
listbox.bind("<Button-3>", lambda event: context_menu.post(event.x_root, event.y_root))
# Loading all GUI frames into the main application window
# Adding the title frame to the main window
title_frame.pack()
# Adding the frame with the name of the playing song to the main window
name_song_frame.pack()
# Adding the playlist frame to the main window
playlist_frame.pack()
# Adding the volume slider frame to the main window
volume_frame.pack()
# Adding the frame with the current song duration to the main window
current_time_frame.pack()
# Adding the button frame to the main window
buttonframe.pack()
# Adding the exit frame to the main window
exitframe.pack()

# Calling a function that iterates through the songs list
show()

# Initializing the Pygame sound module
mixer.init()

# Creating a Tkinter StringVar variable used to store the music-related application state
music_state = StringVar()

# Running the main Tkinter event loop that keeps the program running
window.mainloop()

