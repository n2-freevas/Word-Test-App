import tkinter as tk
import threading
from WordTestGUI_Preset import Frame_preset
from WordTestGUI_Remind import Frame_remind
from WordTestGUI_Option import Frame_option
from WordTestGUI_Testing import Frame_testing
from WordTestGUI_Result import Frame_result

class gifanime_onFrame(tk.Frame):
    def __init__(self, master=None,**animeinfo):
        
        tk.Frame.__init__(self, master)
        
        self.anime_path = animeinfo['path']
        self.nextframe = animeinfo['nextframe']
        if 'Numframe' in animeinfo:
            self.Numframe = animeinfo['Numframe']
        if 'ratio' in animeinfo:
            self.ratio = animeinfo['ratio']
        else:
            self.ratio = 25
       
        self.passData = animeinfo['passData']
        self.App = animeinfo['App']
        
        
        self.index = 1

        # 初期フレームを描画
        self.firstframe = tk.PhotoImage(file=self.anime_path,format="gif -index 0")
        self.Label_background = tk.Label(self,image= self.firstframe)
        self.Label_background.place(x=0,y=0)

        self.Play()
        
    """
    def load_frames(self,Numframe = None):
        #Read in all the frames of a multi-frame gif image.S
         
        if (Numframe == None): 
            while True:
                frameNo = len(self.anime_frames)  # number of next frame to read
                try:
                    frame = tk.PhotoImage(file=self.anime_path,
                                    format="gif -index %i" %frameNo)
        
                except tk.TclError:
                    break
                
                self.anime_frames.append(frame)
            self.anime_frames_len = len(self.anime_frames)

        elif (Numframe != None):
            for i in range(Numframe):
                try:
                    self.anime_frames.append(tk.PhotoImage(file=self.anime_path,
                                        format="gif -index %i" %i))
                except tk.TclError:
                    pass        
            self.anime_frames_len = Numframe
    """

    def Play(self):
        try:
            img = tk.PhotoImage(file=self.anime_path,
                                format="gif -index %i" %self.index)
            self.Label_background.configure(image = img)
            self.Label_background.image = img
            self.index += 1
            self.App.after(self.ratio,self.Play)
            
        except tk.TclError:
            self.App.after(1,self.changeNextFrame)
        

    def changeNextFrame(self):
        
        d = {'passData':self.passData, 'App':self.App}

        if self.nextframe == 'Preset':
            self.master.change(Frame_preset,**d)

        if self.nextframe == 'Option':
            self.master.change(Frame_option,**d)

        if self.nextframe == 'Testing':
            self.master.change(Frame_testing,**d)

        if self.nextframe == 'Result':
            self.master.change(Frame_result,**d)