import csv
import tkinter as tk
import tkinter.ttk as ttk
import WordTestGUI_Globals as gloVal


class Frame_option(tk.Frame):
    
    def __init__(self, master=None, **kwargs):
        
        tk.Frame.__init__(self, master)
        master.title("Sanaru(Anjo):WordTest (Option)")
        
        self.Image_Background = tk.PhotoImage(file = 'figure/Option_bg.gif')
        self.Label_background = tk.Label(self, image = self.Image_Background)
        self.Label_background.place(x=0,y=0)
        
        Button_back = tk.Button(master=self,text="HOME",width=5,bg = "#00a4e4",fg = "#b40000",
                    command=self.master.backToHome,font =("Arial Black",20,"bold","roman","normal","normal"))
        Button_back.pack(anchor = tk.E)

        self.Label_name = tk.Label(master = self, text = u'■ What is your name (English)?',
                                    font =("Arial Black",20,"bold","roman","normal","normal"))
        self.EditBox_name = tk.Entry(master = self,width = 20)
        self.Label_name.place(relx = 0.15, rely = 0.3)
        self.EditBox_name.place(relx =0.15 ,rely =0.35)

        self.Label_id = tk.Label(master = self, text = u'■ What is your Sanaru ID ?',
                                    font =("Arial Black",20,"bold","roman","normal","normal"))
        self.EditBox_id = tk.Entry(master = self,width = 9)
        self.Label_id.place(relx = 0.15, rely = 0.5)
        self.EditBox_id.place(relx =0.15 ,rely =0.55)

        Button_Enter = tk.Button(master = self,text = u' ENTER ', command = self.pushEnter, fg = '#b40000',
                                highlightbackground = gloVal.Dark_Red,highlightthickness = 3,font =("Arial Black",40,"bold","roman","normal","normal"))
        Button_Enter.pack(pady = 60,side = tk.BOTTOM)


    def pushEnter(self):
        name = str(self.EditBox_name.get())
        id = str(self.EditBox_id.get())

        if not(name.isalpha):
            tk.messagebox.showerror('ERROR','名前は、全て英字アルファベットで\n入力してください。')
        else:
            if (id.isdigit):
                with open("identify/name_id.csv", 'w',newline="",encoding = 'utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([name,id])
                f.close()
                tk.messagebox.showinfo('Autherize','情報が登録されました！')
                self.master.backToHome()
            elif (len(id)!=8):
                tk.messagebox.showerror('ERROR', 'IDが8桁ではありません。\n Sanaru IDを入力しなおしてください。')
            else:
                tk.messagebox.showerror('ERROR', 'IDの入力が正しくない可能性があります。\nもう一度入力し直してください。')

                
