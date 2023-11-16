import os  # -> to select the mp3 files
import pickle # ->
import tkinter as tk # -> To create the GUI
from tkinter import filedialog # -> For loading the song folders
from tkinter import PhotoImage # -> To display iamges and icons
from pygame import mixer # -> To control music and audio controls


# Fonts using
# Segoe UI
# Segoe UI Semibold
# Segoe UI Light
# Segoe UI Symbol


class Player(tk.Frame): # tk.frame -> similar to root 
    def __init__(self,master):
        super().__init__(master)
        self.master = master
        self.pack()

        mixer.init()
        if os.path.exists("songList.dat"):
            with open("songList.dat","rb") as f:
                self.playList = pickle.load(f)
        else:
            self.playList = []

        self.current = 0
        self.paused = True
        self.played = False
        self.create_frames()
        self.track_widget()
        self.trackList_widgets()
        self.control_widget()


    def create_frames(self):
        # Song Track
        self.track = tk.LabelFrame(self,text="  Song Track",font= ("Segoe UI Semibold",15),bg="#262626",fg="#f5f5f5",bd=0,relief=tk.GROOVE)
        self.track.configure(width=400,height=300)
        self.track.grid(row=0,column=0)

        # Song Playlist
        self.trackPlayList = tk.LabelFrame(self,text=f" Playlist - {len(self.playList)}",font= ("Segoe UI Semibold",15),bg="#262626",fg="#f5f5f5",bd=0,relief=tk.GROOVE)
        self.trackPlayList.configure(width=300,height=410)
        self.trackPlayList.grid(row=0,column=1,rowspan=3,padx=10)

        # Song Controls
        self.controls = tk.LabelFrame(self,font= ("Segoe UI Semibold",15),bg="#262626",fg="#f5f5f5",bd=0,relief=tk.GROOVE)
        self.controls.configure(width=410,height=240)
        self.controls.grid(row=1,column=0,pady = 10)

    def track_widget(self):
        # Song Track Frame
        self.canvas = tk.Label(self.track,image=img)
        self.canvas.configure(width=390,height=299)
        self.canvas.grid(row=0,column=0)

        # Song Track Name
        self.songTrack = tk.Label(self.track,font= ("Segoe UI Semibold",15))
        self.songTrack["text"] = "MusicMate"
        self.songTrack.configure(width=30,height=1)
        self.songTrack.grid(row=1,column=0)
    def control_widget(self):

        # Mood Options
        mood_options = ['Happy', 'Meditation', 'Sad', 'Energetic']
        self.selected_mood = tk.StringVar(self.controls)
        self.selected_mood.set(mood_options[0])  # Set the default mood
        self.selected_mood.trace('w', self.retrieve_songs)  # Call function when mood changes

        # Create and place the Mood dropdown
        self.mood_dropdown = tk.OptionMenu(self.controls, self.selected_mood, *mood_options)
        # self.mood_dropdown["text"] = "Mood"
        self.mood_dropdown.config(bg="green", fg="#f5f5f5", font=10)
        self.mood_dropdown.grid(row=0, column=0, padx=10)


        # Previous Button
        self.prev = tk.Button(self.controls,image=prev)
        # Linking Command
        self.prev["command"] = self.prev_song
        self.prev.grid(row=0,column=1,padx=5)
        # Pause Button
        self.pause = tk.Button(self.controls,image=pause)
        # Linking Command
        self.pause["command"] = self.pause_song
        self.pause.grid(row=0,column=2,padx=5)
        # Next Button
        self.next_ = tk.Button(self.controls,image=next_)
        # Linking Command
        self.next_["command"] = self.next_song
        self.next_.grid(row=0,column=3,padx=5)

        # Volume Slider
        self.volume = tk.DoubleVar()
        self.slider = tk.Scale(self.controls,from_=0, to=100,orient=tk.HORIZONTAL)
        self.slider["variable"] = self.volume
        # Linking Command
        self.slider["command"] = self.change_volume
        self.slider.set(10)
        mixer.music.set_volume(0.1)
        self.slider.grid(row=0,column=4,padx=10)

    def trackList_widgets(self):
        self.scrollBar = tk.Scrollbar(self.trackPlayList,orient=tk.VERTICAL)
        self.scrollBar.grid(row=0,column=1,rowspan=5,sticky="ns")

        self.list = tk.Listbox(self.trackPlayList,selectmode = tk.SINGLE,yscrollcommand = self.scrollBar.set,selectbackground = "blue")
        self.enumerateSongs()
        self.list.config(height = 22)
        self.list.bind("<Double-1>",self.play_song)
        self.scrollBar.config(command=self.list.yview)
        self.list.grid(row=0,column = 0,rowspan=5)


        
    def enumerateSongs(self):
        for index,song in enumerate(self.playList):
            self.list.insert(index,os.path.basename(song))
    def retrieve_songs(self,*args):


    # PREVIOUS CODE
        # self.songList = []
        # directory = filedialog.askdirectory()
        # for root_,dirs,files in os.walk(directory):
        #     for file in files:
        #         if os.path.splitext(file)[1] == ".mp3":
        #             path = (root_+"/"+file).replace('\\',"/")
        #             # print(path)
        #             self.songList.append(path)

        # with open("songList.dat","wb") as f:
        #     pickle.dump(self.songList,f)
        # self.playList = self.songList
        # self.list.delete(0,tk.END)
        # self.trackPlayList["text"] = f" Playlist - {len(self.playList)}"
        # self.enumerateSongs()
        mood_folders = {
        'Happy': './Music/Happy',  # Replace with the actual paths to respective mood folders
        'Meditation': './Music/Meditation',
        'Sad': './Music/Happy',
        'Energetic': './Music/Relaxed'
        # Add more mood folders as needed
    }

        selected_mood = self.selected_mood.get()
        print(selected_mood)

        if selected_mood in mood_folders:
            directory = mood_folders[selected_mood]

            self.songList = []
            for root_, dirs, files in os.walk(directory):
                for file in files:
                    if os.path.splitext(file)[1] == ".mp3":
                        path = (root_ + "/" + file).replace('\\', "/")
                        self.songList.append(path)

            with open("songList.dat", "wb") as f:
                pickle.dump(self.songList, f)

            self.playList = self.songList
            self.list.delete(0, tk.END)
            self.trackPlayList["text"] = f" Playlist - {len(self.playList)}"
            self.enumerateSongs()
    def pause_song(self):
        if not self.paused:
            self.paused = True
            mixer.music.pause()
            self.pause["image"] = pause
        else:
            if self.played == False:
                self.play_song()
            self.paused = False
            mixer.music.unpause()
            self.pause["image"] = play
    def prev_song(self):
        if self.current>0:
            self.current -=1
        else:
            self.current = 0
        self.list.itemconfigure(self.current+1,bg="white",fg="#262626")
        self.play_song()
    def next_song(self):
        if self.current<(len(self.playList)-1):
            self.current +=1
        else:
            self.current = 0
        self.list.itemconfigure(self.current-1, bg="white",fg="#262626")
        self.play_song()
    def change_volume(self,event=None):
        self.v = self.volume.get()
        mixer.music.set_volume(self.v/100)
    def play_song(self,event=None):
        if event is not None:
            self.current= self.list.curselection()[0]
            for i in range(len(self.playList)):
                self.list.itemconfigure(i,fg="#262626",bg="#f5f5f5")
            # self.list.itemconfigure(self.current,bg="blue")
        mixer.music.load(self.playList[self.current])
        self.pause["image"] = play
        self.paused = False
        self.played = True
        self.songTrack["anchor"] = "w"
        self.songTrack["text"] = os.path.basename(self.playList[self.current])
        self.list.activate(self.current)
        self.list.itemconfigure(self.current,bg="#262626",fg="#f5f5f5")
        mixer.music.play()
# Creating the main window
root = tk.Tk()
# Creating window dimensions
root.geometry("700x500")
# Creating window name
root.wm_title("MusicMate")
# root.mainloop()


img = PhotoImage(file="./Assets/music.gif")
next_ = PhotoImage(file="./Assets/next.gif")
prev = PhotoImage(file="./Assets/previous.gif")
play = PhotoImage(file="./Assets/play.gif")
pause = PhotoImage(file="./Assets/pause.gif")
app = Player(master = root)
app.mainloop()

