import random
import os
import datetime
import csv
import sys
import tkinter as tk
from WordTestGUI_Result import Frame_result
import WordTestGUI_Globals as gloVal
import platform


class Frame_testing(tk.Frame):
    def __init__(self,master,**kwargs):
        tk.Frame.__init__(self,master)
       
        passData = kwargs['passData']
        self.App = kwargs['App']

        # Presetから、passData(辞書型)として流れてきた情報を展開
        self.amount = passData['amount']
        self.mode = passData['mode']
        self.time = passData['time']
        self.ExtractWordlist = passData['ExtractWordlist']
        self.ExtractWordlist_length = passData['ExtractWordlist_length']
        self.DatabaseName = passData['DatabaseName']
        self.Problems = passData['Problems']
        self.Process = 0    #テストの進捗．Process = amount -1 となったとき，テストは終わる．
        self.correctAnswer = 0
        self.point = 0
        #第一問の選択肢配列を生成
        self.Choise = self.MakeChoise(self.Problems[0][4])

        master.title("Word Test (Testing...)")
        self.Image_Background = tk.PhotoImage(file = 'figure/Testing_bg.gif')
        self.Label_background = tk.Label(self, image = self.Image_Background)
        self.Label_background.pack()

        Button_back = tk.Button(master=self,text="HOME",width=5,bg = gloVal.Dark_Red,fg = "black",command=self.master.backToHome,
                                highlightbackground = 'black',highlightthickness = 1)
        Button_back.place(relwidth=0.1, relheight= 0.05, relx= 0.90, rely=0.003)
        
    
        self.Label_Problem = tk.Label(self,text = self.Problems[self.Process][(self.mode)%2],bg='white',font =("Arial Black",30,"bold","roman","normal","normal")) 
        self.Label_Problem.place(relwidth=0.65, relheight= 0.1, relx= 0.1, rely=0.05)

        self.Buttons = []
        bx = 0.25
        by = 0.22
        bxp = -0.025
        byp = 0.08
        for i in range(gloVal.NumberOfChoise):
            if platform.system() == 'Darwin':

                self.Buttons.append(tk.Button(self, text = self.Choise[i],font =("Arial Black",20,"bold","roman","normal","normal"),command = self.callback_PushAnswer(i),
                                            fg = 'white',highlightbackground = 'black',highlightthickness = 30))
            else:
  
                self.Buttons.append(tk.Button(self, text = self.Choise[i],font =("Arial Black",20,"bold","roman","normal","normal"),command = self.callback_PushAnswer(i),
                                            bg = 'white',fg = 'black'))
                                            
            self.Buttons[i].place(relwidth=0.5, relheight= 0.028, relx= bx + (bxp*i), rely=by + (byp*i))

        self.img1 = tk.PhotoImage(file = 'figure/number/0_mini.gif')
        self.img2 = tk.PhotoImage(file = 'figure/number/0_mini.gif')
        self.img3 = tk.PhotoImage(file = 'figure/number/1_mini.gif')
        self.Label_Count1 = tk.Label(master = self,image = self.img1,highlightthickness=0)
        self.Label_Count2 = tk.Label(master = self,image = self.img2,highlightthickness=0)
        self.Label_Count3 = tk.Label(master = self,image = self.img3,highlightthickness=0)
        self.Label_Count1.place(relwidth = 0.1,relheight = 0.1142,relx = 0.62,rely = 0.83)
        self.Label_Count2.place(relwidth = 0.1,relheight = 0.1142,relx = 0.73,rely = 0.8)
        self.Label_Count3.place(relwidth = 0.1,relheight = 0.1142,relx = 0.84,rely = 0.77)

    def MakeChoise(self,Word_or_Idiom):
        ChoiseWordArray = []

        for i in range(gloVal.NumberOfChoise):
            flag = True
            while(flag):
                num = random.randint(0,self.ExtractWordlist_length)
                # 単語か熟語か一致した時，
                if (self.ExtractWordlist[num][4] == self.Problems[self.Process][4]):
                     # 選択肢に重複がなく かつ 正解選択肢がこの時点で入らない という条件を満たすとき，
                    if (not(self.ExtractWordlist[num][(self.mode+1)%2] in ChoiseWordArray)) and (self.ExtractWordlist[num][(self.mode+1)%2] != self.Problems[self.Process][(self.mode+1)%2]):
                        # ランダムに選ばれた選択肢を採用する．
                        ChoiseWordArray.append(self.ExtractWordlist[num][(self.mode+1)%2])
                        flag = False

        # 選択肢のうちひとつを正解選択肢に差し替える．
        correct = random.randint(0,gloVal.NumberOfChoise-1)
        ChoiseWordArray[correct] = self.Problems[self.Process][(self.mode+1)%2]
        self.correctAnswer = correct
        return ChoiseWordArray

    def callback_PushAnswer(self,number):
        def PushAnswer():
        
            #正解ボタンだった場合は，クリアチェッカをTrueにする．
            if (self.correctAnswer == number):
                self.Problems[self.Process][2] = True
                self.point += 1
            self.Process = self.Process + 1

            if self.Process >= self.amount:
                # 採点結果を辞書型に格納する
                d = {'Problems':self.Problems, 'mode':self.mode, 'DatabaseName':self.DatabaseName,'point':self.point,'performance':None}

                from tkinter_gifplay import gifanime_onFrame
                #満点の場合、
                if self.point == self.amount:
                    if self.amount >= 50:
                        #特殊演出
                        d['performance'] = 'superperfect'
                        dic = {'path':'figure/Testing2Result_superperfect_shift.gif','nextframe':'Result','ratio':40,
                        'App':self.App, 'passData':d}
                        return self.master.change(gifanime_onFrame,**dic)
                    else:
                        #特殊演出
                        d['performance'] = 'perfect'
                        dic = {'path':'figure/Testing2Result_perfect_shift.gif','nextframe':'Result','ratio':20,
                        'App':self.App, 'passData':d}
                        return self.master.change(gifanime_onFrame,**dic)
            
                # リザルト画面に遷移する
                #self.master.backToStart()
                else:
                    dic = {'path':'figure/Testing2Result_shift.gif','nextframe':'Result','ratio':40,
                    'App':self.App, 'passData':d}
                    return self.master.change(gifanime_onFrame,**dic)
            else:
                #選択肢を生成しなおす．このときCorrectAnswerも更新される．
                self.Choise = self.MakeChoise(self.Problems[self.Process][4])
                
                self.Label_Problem['text'] = self.Problems[self.Process][self.mode%2]
                #選択肢をボタンに反映する．
                for i in range(gloVal.NumberOfChoise):
                    self.Buttons[i]['text'] = self.Choise[i]

                num = self.Process + 1
                num3 = int(num%10)
                num2 = int((num%100)/10)
                num1 = int((num%1000)/100)
                img1 = tk.PhotoImage(file = 'figure/number/%s_mini.gif'%num1)
                img2 = tk.PhotoImage(file = 'figure/number/%s_mini.gif'%num2)
                img3 = tk.PhotoImage(file = 'figure/number/%s_mini.gif'%num3)
                self.Label_Count1.configure(image=img1)
                self.Label_Count1.image=img1
                self.Label_Count2.configure(image=img2)
                self.Label_Count2.image=img2
                self.Label_Count3.configure(image=img3)
                self.Label_Count3.image=img3
        return PushAnswer
