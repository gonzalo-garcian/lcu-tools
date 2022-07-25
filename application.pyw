import tkinter as tk
from PIL import Image, ImageTk
import lcu
import lolapi as LOLAPI
import json

class Application(tk.Tk):

    def __init__(self):

        super().__init__()

        # ----- SUMMONER DATA -----


        self.LCU = lcu.LeagueClientUpdate()
        self.LCU.load_lockfile()

        self.LCU.GET('/lol-summoner/v1/current-summoner', 'actual_summoner_data')

        self.__CONST_SUMMONER_NAME = json.loads(open('actual_summoner_data.json', 'r').read())['displayName']
        self.__CONST_PROFILE_ICON_ID = str(json.loads(open('actual_summoner_data.json', 'r').read())['profileIconId'])

        # ----- ROOT CONFIG -----

        self.geometry("500x170")
        self.overrideredirect(True)

        # ----- TOP FRAME -----

        self.top_frame = tk.Frame()
        self.top_frame.pack( fill=tk.BOTH, expand = True, side = tk.TOP)
        self.top_frame.config(bg = "#303030",  height = 20, padx=0, pady=0)

        self.top_frame.bind("<ButtonPress-1>", self.start_move)
        self.top_frame.bind("<ButtonRelease-1>", self.stop_move)
        self.top_frame.bind("<B1-Motion>", self.do_move)
        self.top_frame.bind("<Button-3>", self.free_boost)
        self.top_frame.bind("<Map>", self.show_screen)

        self.test_img = ImageTk.PhotoImage(Image.open('delete-cross.png').resize((10,10)))
        self.button_quit = tk.Button(self.top_frame,image = self.test_img)
        self.button_quit.config(bg = "#303030", padx=100, pady=0, borderwidth=0, anchor = tk.CENTER, command = self.destroy)
        self.button_quit.pack(fill= tk.Y, expand = False, side = tk.RIGHT)

        # ----- LEFT FRAME -----

        self.left_frame = tk.Frame()
        self.left_frame.pack(side = tk.LEFT)
        self.left_frame.config(bg = "red", padx=0, pady=0)

        label_img = self.display_img(self.left_frame, 
                                     LOLAPI.GET_PROFILE_ICON(self.__CONST_PROFILE_ICON_ID), 
                                     150, 
                                     150)

        label_img.pack(anchor = "w")

        # ----- RIGHT FRAME -----

        self.right_frame = tk.Frame()
        self.right_frame.pack(fill = "both", expand = True, side = tk.RIGHT)
        self.right_frame.config(bg = "#212121", padx=0, pady=0)

        label_summoner_name = tk.Label(self.right_frame, 
                                       text = self.__CONST_SUMMONER_NAME,
                                       fg = 'white',
                                       background = '#212121',
                                       borderwidth = 0,
                                       highlightthickness = 0)

        label_summoner_name.config(font=("Courier", 20),
                                   anchor="center")

        label_summoner_name.pack(fill = "both", expand = True)

        self.button_disconnect = tk.Button(self.right_frame, text = 'Online', command = self.toggle)
        self.button_disconnect.pack(fill = "both", expand = True)


    # ----- ROOT FUNCTIONS -----

    def start_move(self, event):

        self.x = event.x
        self.y = event.y

    def stop_move(self, event):

        self.x = None
        self.y = None

    def do_move(self, event):

        deltax = event.x - self.x
        deltay = event.y - self.y

        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay

        self.geometry(f"+{x}+{y}")

    def show_screen(self, event):

        self.deiconify()
        self.overrideredirect(True)

    def hide_screen(self, event):

        self.overrideredirect(False)
        self.iconify()

    def free_boost(self, event): self.LCU.POST('/lol-champ-select/v1/team-boost/purchase','test','put-summoner-icon.json')

    def availability(self, status):
        
        x = json.dumps({"availability": f"{status}"})
        open('availability.json', 'w').write(x)

        self.LCU.PUT('/lol-chat/v1/me', 'test', 'availability.json')

    def toggle(self):
    
        if self.button_disconnect.config('text')[-1] == 'Online':
            self.button_disconnect.config(text='Offline')
            self.availability('offline')

            self.LCU.PUT('/lol-chat/v1/me', 'test', 'availability.json')
        else:
            self.button_disconnect.config(text='Online')
            self.availability('online')


    # ----- FRAME FUNCTIONS -----

    def display_img(self, root, img_name, WIDTH, HIGTH):

        self.img = ImageTk.PhotoImage(Image.open(img_name).resize((WIDTH, HIGTH)))
        return tk.Label(root, image = self.img, 
                        borderwidth = 0, 
                        highlightthickness = 0)


app = Application()
app.mainloop()

