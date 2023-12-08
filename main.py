import os
import tkinter as tk
import pygame
import threading

class MusicPlayer:
    def __init__(self, root, rootpath):
        self.root = root
        self.rootpath = rootpath
        self.file_paths = self.load_tracks()
        self.current_track = 0

        pygame.init()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)

        self.create_widgets()

        # Lancer le thread pour surveiller les événements de fin de musique
        threading.Thread(target=self.music_event_listener).start()

    def load_tracks(self):
        return [file for file in os.listdir(self.rootpath) if file.endswith(".mp3")]

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Player de Musique", font=("DS.DIGIT.TTF", 18), bg="#8400ff", fg="white")
        self.label.pack(pady=10)

        self.listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, font=("DS.DIGIT.TTF", 14), height=10, fg='cyan', bg='black')
        for file_path in self.file_paths:
            self.listbox.insert(tk.END, file_path)
        self.listbox.pack(pady=10)

        control_frame = tk.Frame(self.root, bg="#8400ff")
        control_frame.pack(pady=10)

        prev_button = tk.Button(control_frame, text='Prev', borderwidth=1, command=self.play_prev)
        prev_button.grid(row=0, column=0, padx=10)

        stop_button = tk.Button(control_frame, text='Stop', borderwidth=1, command=self.stop_song)
        stop_button.grid(row=0, column=1, padx=10)

        play_button = tk.Button(control_frame, text='Play', borderwidth=1, command=self.play_selected)
        play_button.grid(row=0, column=2, padx=10)

        pause_button = tk.Button(control_frame, text='Pause', borderwidth=1, command=self.pause_song)
        pause_button.grid(row=0, column=3, padx=10)

        next_button = tk.Button(control_frame, text='Next', borderwidth=1, command=self.play_next)
        next_button.grid(row=0, column=4, padx=10)

    def play_track(self, track_index):
        file_path = os.path.join(self.rootpath, self.file_paths[track_index])
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

    def play_prev(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            self.current_track = selected_index[0] - 1
            if self.current_track < 0:
                self.current_track = len(self.file_paths) - 1
            self.play_track(self.current_track)

    def stop_song(self):
        pygame.mixer.music.stop()
        self.listbox.select_clear(0, tk.END)

    def play_selected(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            self.current_track = selected_index[0]
            self.play_track(self.current_track)

    def pause_song(self):
        if pygame.mixer.music.get_busy():
            if pygame.mixer.music.get_pos() > 0:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()

    def play_next(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            self.current_track = selected_index[0] + 1
            if self.current_track >= len(self.file_paths):
                self.current_track = 0
            self.play_track(self.current_track)

    def music_event_listener(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    
                    self.play_next()

if __name__ == "__main__":
    rootpath = "./music/"
    root = tk.Tk()
    root.title("Player Music")
    root.geometry('650x550')
    root.config(bg="#8400ff")

    app = MusicPlayer(root, rootpath)
    root.mainloop()

