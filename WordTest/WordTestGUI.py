import os
import tkinter as tk
from WordTestGUI_Preset import Frame_preset
from WordTestGUI_Remind import Frame_remind
from WordTestGUI_Option import Frame_option
import WordTestGUI_Globals as gloVal
from tkinter_gifplay import gifanime_onFrame



class BaseWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry('500x700')
        self.resizable(0,0)
        self.frame = Frame_home(self)
        self.frame.pack(expand=True, fill="both")

    def change(self, frame,**kwargs):
        self.frame.pack_forget() # delete currrent frame
        self.frame = frame(self,**kwargs)
        self.frame.pack(expand=True, fill="both") # make new frame

    def backToHome(self):
        self.frame.pack_forget()
        self.frame = Frame_home(self)
        self.frame.pack(expand=True, fill="both")

class Frame_home(tk.Frame):
    
    def __init__(self, master=None, **kwargs):
        
        tk.Frame.__init__(self, master,bg = "#ffffff")
        master.title("Sanaru(Anjo):WordTest")
        
        

        self.img = tk.PhotoImage(file = 'figure/title.gif')
        Label_Title = tk.Label(master = self, width = 399, height = 119,image = self.img,
                                highlightthickness=0)
        Label_Title.pack(pady=40)

        if os.path.isfile('identify/name_id.csv'):
            self.img2 = tk.PhotoImage(file = 'figure/gototest.gif')
            self.Button_GoToPreset = tk.Button(master = self, width = 395, height = 115, image = self.img2,
                                        command = self.gotoPreset)
            self.Button_GoToPreset.bind("<Enter>",self.callback_entertest)
            self.Button_GoToPreset.bind("<Leave>",self.callback_leavetest)

            self.img3 = tk.PhotoImage(file = 'figure/gotoremind.gif')
            self.Button_GoToRemind = tk.Button(master = self, width = 395, height = 115,image = self.img3,
                                        command = self.gotoRemind)
            self.Button_GoToRemind.bind("<Enter>",self.callback_enterremind)
            self.Button_GoToRemind.bind("<Leave>",self.callback_leaveremind)

        else:
            self.img2 = tk.PhotoImage(file = 'figure/gototest_gray.gif')
            self.Button_GoToPreset = tk.Button(master = self, width = 395, height = 115, image = self.img2,state='disable')
        
            self.img3 = tk.PhotoImage(file = 'figure/gotoremind_gray.gif')
            self.Button_GoToRemind = tk.Button(master = self, width = 395, height = 115, image = self.img3, state='disable')

        self.Button_GoToPreset.pack(pady = 15)
        self.Button_GoToRemind.pack(pady = 15)

        self.img4 = tk.PhotoImage(file = 'figure/gotooption.gif')
        self.Button_GoToOption = tk.Button(master = self, width = 395, height = 115,image = self.img4,
                                        command = self.gotoOption)
        self.Button_GoToOption.bind("<Enter>",self.callback_enteroption)
        self.Button_GoToOption.bind("<Leave>",self.callback_leaveoption)
        self.Button_GoToOption.pack(pady = 15)

        self.Val_anime = tk.BooleanVar()
        self.Val_anime.set(True)
        self.Check_time = tk.Checkbutton(master = self, text = u'Play animation when Screen Transition',variable = self.Val_anime,
                                        bg=gloVal.Back_color,font =("Arial Black",15,"roman","normal","normal"))  
        self.Check_time.pack(side = tk.BOTTOM,anchor = tk.E)

    def callback_entertest(self,event):
        img = tk.PhotoImage(file = 'figure/gototest_move.gif')
        self.Button_GoToPreset.configure(image=img)
        self.Button_GoToPreset.image=img

    def callback_leavetest(self,event):
        img = tk.PhotoImage(file = 'figure/gototest.gif')
        self.Button_GoToPreset.configure(image=img)
        self.Button_GoToPreset.image=img
    
    def callback_enterremind(self,event):
        img = tk.PhotoImage(file = 'figure/gotoremind_move.gif')
        self.Button_GoToRemind.configure(image=img)
        self.Button_GoToRemind.image=img

    def callback_leaveremind(self,event):
        img = tk.PhotoImage(file = 'figure/gotoremind.gif')
        self.Button_GoToRemind.configure(image=img)
        self.Button_GoToRemind.image=img

    def callback_enteroption(self,event):
        img = tk.PhotoImage(file = 'figure/gotooption_move.gif')
        self.Button_GoToOption.configure(image=img)
        self.Button_GoToOption.image=img

    def callback_leaveoption(self,event):
        img = tk.PhotoImage(file = 'figure/gotooption.gif')
        self.Button_GoToOption.configure(image=img)
        self.Button_GoToOption.image=img
    
    def gotoPreset(self):
        if self.Val_anime.get():
            d = {'path':'figure/Home2Preset_shift.gif','nextframe':'Preset','ratio':15,'App':wordTestApp,'passData':None}
            return self.master.change(gifanime_onFrame,**d)
        else:
            return self.master.change(Frame_preset)

    def gotoRemind(self):
        return self.master.change(Frame_remind)

    def gotoOption(self):
        if self.Val_anime.get():
            d = {'path':'figure/Home2Option_shift.gif','nextframe':'Option','App':wordTestApp,'passData':None}
            return self.master.change(gifanime_onFrame,**d)
        else:
            return self.master.change(Frame_option)      

if __name__ == "__main__":
    wordTestApp = BaseWindow()
    wordTestApp.mainloop()