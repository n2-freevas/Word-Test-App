import random
import os
import datetime
import csv
import sys
import tkinter as tk
import WordTestGUI_Globals as gloVal


class Frame_result(tk.Frame):
    def __init__(self,master,**kwargs):
        tk.Frame.__init__(self,master)
        

        # Testingから得られた結果を取得する
        passData = kwargs['passData']
        self.App = kwargs['App']
        performance = passData['performance']

        self.Label_background = tk.Label(self)
        self.ShowBackground(performance)
        master.title("Word Test (Result)")
            
        Problems = passData['Problems']
        mode = passData['mode']
        DatabaseName = passData['DatabaseName']
        point = int(passData['point'])
        point = 5
        

        Results= self.MakeResult(Problems,mode,DatabaseName)

        Button_back = tk.Button(master=self,text="HOME",bg = gloVal.Dark_Red,fg = "black",command=self.master.backToHome,
                                highlightbackground = 'black',highlightthickness = 1)
        Button_back.place(relwidth=0.1, relheight= 0.05, relx= 0.90, rely=0.003)


        #スクロールバーの作成
        scroll = tk.Scrollbar(self)
        #スクロールバーの配置を決める
        scroll.place(relwidth = 0.012,relheight=0.4 ,relx = 0.988, rely = 0.5)

        #データ
        list_value=tk.StringVar()
        list_value.set(Results)

        self.Label_Count1 = tk.Label(master = self,highlightthickness=0)
        self.Label_Count2 = tk.Label(master = self,highlightthickness=0)
        self.Label_Count3 = tk.Label(master = self,highlightthickness=0)
        self.img = tk.PhotoImage(file = 'figure/number/pt.gif')
        self.Label_pt = tk.Label(master = self,highlightthickness=0,image = self.img) 
        self.ShowPoint(point) # This func include packer for them
        
        #リストボックスの作成
        listbox=tk.Listbox(self,listvariable=list_value,selectmode="single",yscrollcommand=scroll.set,
                            highlightbackground = gloVal.Wine_Red,highlightthickness = 2)
        listbox.place(relwidth = 0.76,relheight = 0.4,relx = 0.228,rely = 0.5)

        #部品の動きをスクロールバーに反映させる
        scroll["command"]=listbox.yview
        
        
    def ShowBackground(self,perform):
        if perform == 'superperfect':
            self.Image_Background = tk.PhotoImage(file = 'figure/Result_perfect_bg.gif')
        elif perform == 'perfect':
            self.Image_Background = tk.PhotoImage(file = 'figure/Result_perfect_bg.gif')
        else:
            self.Image_Background = tk.PhotoImage(file = 'figure/Result_bg.gif')
        
        self.Label_background = tk.Label(self, image = self.Image_Background)
        self.Label_background.pack()

    def ShowPoint(self,point):

        num3 = int(point%10) #一の位
        img3 = tk.PhotoImage(file = 'figure/number/wine_%s.gif'%num3)
        self.Label_Count3.configure(image=img3)
        self.Label_Count3.image=img3
        if len(str(point)) > 1:
            num2 = int((point%100)/10) #十の位
            img2 = tk.PhotoImage(file = 'figure/number/wine_%s.gif'%num2)
            self.Label_Count2.configure(image=img2)
            self.Label_Count2.image=img2
        if len(str(point)) > 2:    
            num1 = int((point%1000)/100) #百の位
            img1 = tk.PhotoImage(file = 'figure/number/wine_%s.gif'%num1)
            self.Label_Count1.configure(image=img1)
            self.Label_Count1.image=img1
        
        if len(str(point)) == 1:
            self.Label_Count3.place(relwidth = 0.2,relheight = 0.285,relx = 0.44,rely = 0.1)
            self.Label_pt.place(relwidth = 0.15,relheight= 0.0714, relx=0.65,rely=0.3136)
        if len(str(point)) == 2:
            self.Label_Count2.place(relwidth = 0.2,relheight = 0.285,relx = 0.33,rely = 0.088)
            self.Label_Count3.place(relwidth = 0.2,relheight = 0.285,relx = 0.55,rely = 0.127)
            self.Label_pt.place(relwidth = 0.15,relheight= 0.0714, relx=0.75,rely=0.3406)
        if len(str(point)) == 3:
            self.Label_Count1.place(relwidth = 0.2,relheight = 0.285,relx = 0.22,rely = 0.077)
            self.Label_Count2.place(relwidth = 0.2,relheight = 0.285,relx = 0.44,rely = 0.1)
            self.Label_Count3.place(relwidth = 0.2,relheight = 0.285,relx = 0.66,rely = 0.123)
            self.Label_pt.place(relwidth = 0.15,relheight= 0.0714, relx=0.71,rely=0.405)


    # リザルト文字列を返すとともに，csvファイルに結果を出力する関数
    def MakeResult(self,array,mode,name):
        results = ''
        length = len(array)

        # 問題文の中で最大長のテキストを検索
        maxlen = 0
        for i in range(length):
            if(maxlen < len(array[i][mode%2])):
                maxlen = len(array[i][mode%2])
        for i in range(length):

            text=''
            text = ('Q'+str(i+1).rjust(3,'0')+':')
            if (array[i][2] == True):
                text = text + ' [ ○ ]'
            else:
                text = text + ' [ × ]'
            text = text + ((' : ')+ array[i][mode%2]+' / '+array[i][(mode+1)%2])
            
            
            results = results + text + '\n'
        
        # csvファイルに書き込む
        date = datetime.datetime.now()
        csv_file_name = "Results/Log/["+ str(name) +"]_Result({0:%Y%m%d%H%M%S}).csv".format(date)
        with open(csv_file_name, 'w',newline="",encoding = 'utf-8') as f:
            writer = csv.writer(f)
            for i in range(length):
                if array[i][2] == True:
                    clear = '○'
                else:
                    clear = '×'
                writer.writerow([array[i][3],array[i][mode%2],clear,array[i][(mode+1)%2],array[i][4]])


        return results.replace(" ","　")

