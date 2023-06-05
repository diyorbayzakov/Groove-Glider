from tkinter import *
from pygame import mixer
from tkinter import filedialog
import tkinter as tk
import random
import tkinter.ttk as ttk
from mutagen.mp3 import MP3
import os

# ---------------------------- Initialization -----------------------------#

mixer.init()
root = Tk()
root.title("Groove Glider")
root.configure(bg="#202020")

repeat = False

light_icon = "☀︎"
dark_icon = "🌙"

light_bg_colour = "#F3BCC8"
dark_bg_colour = "#202020"

# ---------------------------- Sub Programs ----------------------------- #

# Go to the previous song

def prev_song():
    prev_s = song_box.curselection()
    prev_s = prev_s[0] - 1 if prev_s[0] != 0 else song_box.size() - 1

    song = song_box.get(prev_s)
    mixer.music.load(song)
    mixer.music.play()

    song_box.selection_clear(0, END)
    song_box.activate(prev_s)
    song_box.selection_set(prev_s, last=None)

    update_song_info(song)

# Go to the next song

def forward_song():
    next_s = song_box.curselection()
    next_s = next_s[0] + 1 if next_s[0] != song_box.size() - 1 else 0

    song = song_box.get(next_s)
    mixer.music.load(song)
    mixer.music.play()

    song_box.selection_clear(0, END)
    song_box.activate(next_s)
    song_box.selection_set(next_s, last=None)

    update_song_info(song)

# Shows how far you are into the song and how long the song is

def update_song_info(song):
    global song_length, song_length_str
    audio = MP3(song)
    song_length = int(audio.info.length)
    mins, secs = divmod(song_length, 60)
    song_length_str = f"{mins}:{secs:02d}"
    song_duration_label['text'] = song_length_str

# Plays the song

def play_song():
    global song_length, song_length_str
    song = song_box.get(ACTIVE)
    mixer.music.load(song)
    mixer.music.play(loops=0)
    song_state['text'] = "Playing"

    audio = MP3(song)
    song_length = int(audio.info.length)
    mins, secs = divmod(song_length, 60)
    song_length_str = f"{mins}:{secs:02d}"

    if repeat:
        mixer.music.play(loops=-1)
    else:
        mixer.music.play(loops=0)

    song_duration_label['text'] = song_length_str

# Pauses the song

def pause_song():
    if song_state['text'] == "Playing":
        mixer.music.pause()
        song_state['text'] = "Paused"
    else:
        mixer.music.unpause()
        song_state['text'] = "Playing"

# Stops the song

def stop_song():
    mixer.music.stop()
    song_box.selection_clear(ACTIVE)
    song_state['text'] = "Paused"

# Opens one song

def open_file():
    song = filedialog.askopenfilename(initialdir='tracks/', title="Choose a song!", filetypes=(("mp3 Files", "*.mp3"),))
    if song:
        song_filename = os.path.basename(song)
        song_box.insert(END, song_filename)

# Opens multiple songs (playlist)

def open_folder():
    songs = filedialog.askopenfilenames(initialdir='tracks/', title="Choose songs!", filetypes=(("mp3 Files", "*.mp3"),))
    if songs:
        for song in songs:
            song_filename = os.path.basename(song)
            song_box.insert(END, song_filename)

# Allows user to change volume  

def set_volume(value):
    volume = float(value) / 100
    mixer.music.set_volume(volume)

# Stops music when window closed
    
def on_closing():
    stop_song()
    root.destroy()

# Shuffles the playlist

def shuffle_playlist():
    current_selection = song_box.curselection()
    playlist = list(song_box.get(0, END))
    random.shuffle(playlist)
    song_box.delete(0, END)
    for song in playlist:
        song_box.insert(END, song)
    if current_selection:
        song_box.selection_set(current_selection[0])
        
# Allows repeat functionality

def toggle_repeat():
    global repeat
    repeat = not repeat
    if repeat:
        repeat_button.config(fg="#1DB954")
    else:
        repeat_button.config(fg="white")
    
# Updates the progress bar

def update_progress():
    if mixer.music.get_busy():
        current_time = mixer.music.get_pos() // 1000
        mins, secs = divmod(current_time, 60)
        current_time_str = f"{mins}:{secs:02d}"
        song_state['text'] = "Playing"
        song_current_label['text'] = current_time_str
        progress = (current_time / song_length) * 100
        progress_bar['value'] = progress

        if progress >= 100 and repeat:
            forward_song()
    else:
        song_state['text'] = "Paused"
        song_current_label['text'] = "0:00"
        progress_bar['value'] = 0
    root.after(200, update_progress)

# Allows theme switching

def switch_theme():
    current_theme = root.cget("bg")
    if current_theme == dark_bg_colour:
        light_theme()
    else:
        dark_theme()

# Dark theme settings

def dark_theme():
    root.config(bg=dark_bg_colour)

    song_state.config(bg=dark_bg_colour, fg="white")
    song_box.config(bg=dark_bg_colour, fg="white", selectbackground="#1DB954")
    song_current_label.config(bg=dark_bg_colour, fg="#1DB954")
    song_duration_label.config(bg=dark_bg_colour, fg="#1DB954")
    volume_label.config(bg=dark_bg_colour, fg="white")
    volume_slider.config(bg=dark_bg_colour, fg="#1DB954", troughcolor=dark_bg_colour, highlightbackground=dark_bg_colour)
    light_button.config(text=light_icon,bg=dark_bg_colour , fg="white", command=light_theme)
    openfile_button.config(bg=dark_bg_colour, fg="white")
    openfolder_button.config(bg=dark_bg_colour, fg="white")
    repeat_button.config(bg=dark_bg_colour)

    controls_frame.config(bg=dark_bg_colour)
    for button in controls_frame.winfo_children():
        if isinstance(button, tk.Button) and button != repeat_button:
            button.config(bg=dark_bg_colour, fg="white")

    master_frame.config(bg=dark_bg_colour)
    info_frame.config(bg=dark_bg_colour)
    file_frame.config(bg=dark_bg_colour)
    volume_frame.config(bg=dark_bg_colour)

    return "dark_mode"

# Light theme settings

def light_theme():
    root.config(bg=light_bg_colour)

    song_state.config(bg=light_bg_colour, fg="black")
    song_box.config(bg=light_bg_colour, fg="black", selectbackground="#1DB954")
    song_current_label.config(bg=light_bg_colour, fg="#FF4500")
    song_duration_label.config(bg=light_bg_colour, fg="#FF4500")
    volume_label.config(bg=light_bg_colour, fg="black")
    volume_slider.config(bg=light_bg_colour, fg="#FF4500", troughcolor=light_bg_colour, highlightbackground=light_bg_colour)
    light_button.config(text=dark_icon,bg=light_bg_colour, fg="black", command=dark_theme)
    openfile_button.config(bg=light_bg_colour, fg="#FF4500")
    openfolder_button.config(bg=light_bg_colour, fg="#FF4500")
    repeat_button.config(bg=light_bg_colour)

    controls_frame.config(bg=light_bg_colour)
    for button in controls_frame.winfo_children():
        if isinstance(button, tk.Button) and button != repeat_button:
            button.config(bg=light_bg_colour, fg="black")

    master_frame.config(bg=light_bg_colour)
    info_frame.config(bg=light_bg_colour)
    file_frame.config(bg=light_bg_colour)
    volume_frame.config(bg=light_bg_colour)

    return "light_mode"


# ---------------------------- Frames -----------------------------#

master_frame = Frame(root, bg="#202020")
master_frame.pack(pady=20)

info_frame = Frame(master_frame, bg="#202020")
info_frame.grid(row=0, column=0)

controls_frame = Frame(master_frame, bg="#202020")
controls_frame.grid(row=1, column=0)

file_frame = Frame(master_frame, bg="#202020")
file_frame.grid(row=0, column=1, padx=20)

volume_frame = Frame(root, bg="#202020")
volume_frame.pack(pady=10)

# ---------------------------- Info frame layout -----------------------------#

song_state = Label(info_frame, width=60, text="Paused", font=("Arial", 14), bg="#202020", fg="white")
song_state.grid(row=0, column=0, pady=10)

song_box = Listbox(info_frame, width=61, selectbackground="#1DB954", font=("Arial", 12), bg="#121212", fg="white")
song_box.grid(row=1, column=0)

progress_bar = ttk.Progressbar(info_frame, orient=HORIZONTAL, length=400, mode='determinate')
progress_bar.grid(row=2, column=0, pady=10)

song_current_label = Label(info_frame, width=5, font=("Arial", 8), bg="#202020", fg="#1DB954")
song_current_label.place(x=85, y=253)

song_duration_label = Label(info_frame, width=5, font=("Arial", 8), bg="#202020", fg="#1DB954")
song_duration_label.place(x=545, y=253)

update_progress()

# -------------------------- Control frame layout ---------------------------#

back_button = Button(controls_frame, text="⏮", font=("Arial", 14), bg="#202020", fg="white", bd=0, command=prev_song)
back_button.grid(row=0, column=0, padx=10)

play_button = Button(controls_frame, text="▶", font=("Arial", 20), bg="#202020", fg="white", bd=0, command=play_song)
play_button.grid(row=0, column=4, padx=10)

pause_button = Button(controls_frame, text="II", font=("Arial", 14), bg="#202020", fg="white", bd=0, command=pause_song)
pause_button.grid(row=0, column=5, padx=10)

stop_button = Button(controls_frame, text="⬛", font=("Arial", 10), bg="#202020", fg="white", bd=0, command=stop_song)
stop_button.grid(row=0, column=3, padx=10)

next_button = Button(controls_frame, text="⏭", font=("Arial", 14), bg="#202020", fg="white", bd=0, command=forward_song)
next_button.grid(row=0, column=7, padx=10)

shuffle_button = Button(controls_frame, text="⇆", font=("Arial", 14), bg="#202020", fg="white", bd=0, command=shuffle_playlist)
shuffle_button.grid(row=0, column=2, padx=10)

repeat_button = Button(controls_frame, text="↻﻿", font=("Arial", 14), bg="#202020", fg="white", bd=0, command=toggle_repeat)
repeat_button.grid(row=0, column=6, padx=10)

# ---------------------------- File frame layout -----------------------------#

openfile_button = Button(file_frame, text="Open File", font=("Arial", 12), bg="#202020", fg="white", bd=0, command=open_file)
openfile_button.grid(row=0, column=0, padx=5)

openfolder_button = Button(file_frame, text="Open Folder", font=("Arial", 12), bg="#202020", fg="white", bd=0, command=open_folder)
openfolder_button.grid(row=1, column=0, pady=10)

# ---------------------------- Volume Control -----------------------------#

volume_label = Label(volume_frame, text="Volume", font=("Arial", 12), bg="#202020", fg="white")
volume_label.grid(row=0, column=0, padx=10)

volume_slider = Scale(volume_frame, from_=0, to=100, orient=HORIZONTAL, length=200, width=10, sliderlength=10, bg="#202020", fg="#1DB954", bd=0, highlightthickness=0, command=set_volume)
volume_slider.set(70)
volume_slider.grid(row=0, column=1, padx=10)

# Theme switcher button

light_button = Button(root, text=light_icon, font=("Arial", 12), bg="#202020", fg="white", bd=0, command=switch_theme)
light_button.place(x=780, y=10)

# Extra important stuff

root.protocol("WM_DELETE_WINDOW", on_closing)
root.after(200, update_progress)
root.mainloop()
