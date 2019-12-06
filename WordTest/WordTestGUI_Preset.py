import os
import random
import csv
import tkinter as tk
import tkinter.ttk as ttk
from WordTestGUI_Testing import Frame_testing
import WordTestGUI_Globals as gloVal
from tkinter import messagebox


''' DEFINE '''
relx_def = 0.17
rely_def = 0.38

class Frame_preset(tk.Frame):

    def __init__(self, master=None, **kwargs):
        
        self.App = kwargs['App']

        tk.Frame.__init__(self, master)
        master.title("Sanaru(Anjo):WordTest (Presetting...)")
        self.Image_Background = tk.PhotoImage(file = 'figure/Preset_bg.gif')
        self.Label_background = tk.Label(self, image = self.Image_Background)
        self.Label_background.pack()
        
        # 設定の初期値
        self.start , self.end, self.amount, self.path_No= self.ExtractIdentify()
        self.ExtactWordlist_length = 0
        self.ExtractWordlist = []
        
        # 「戻る」ボタンをフレームの右上に設置する
        self.Button_home = tk.Button(master=self,text="HOME",width=5,bg = "#00a4e4",fg = "#b40000",
                    command=self.master.backToHome,font =("Arial Black",20,"bold","roman","normal","normal"))
        

        # 単語DBを選択するドロップダウンボックスを設置
        self.DB_Combo = ttk.Combobox(master = self, state = 'readonly',font =("Arial Black",12,"bold","roman","normal","normal"))
        self.DB_Combo['values'] = (gloVal.Word_Databases)
        self.DB_Combo.current(self.path_No)
        


        # 開始番号と終了番号の入力を促す説明を設置する．
        self.Label_title = tk.Label(master = self, text=u'■ Please inport Test range．',
                                    bg = gloVal.Back_color,font =("Arial Black",15,"bold","roman","normal","normal"))
        

        #開始番号入力欄
        self.EditBox_start = tk.Entry(master = self,bg = 'white',width= 7)
        self.EditBox_start.insert(tk.END,self.start)
        

        #文字列「から」
        self.Label_start_end = tk.Label(master = self, text=u'~',
                                bg=gloVal.Back_color,font =("Arial Black",15,"bold","roman","normal","normal"))
        
        
        #終了番号入力欄
        self.EditBox_end = tk.Entry(master = self,bg = 'white',width = 7)
        self.EditBox_end.insert(tk.END,self.end)
        

        #　問題数の入力を促す説明文を表示する
        self.Label_amount = tk.Label(master = self, text=u'■ How many questions you want to ?',
                                    bg=gloVal.Back_color,font =("Arial Black",15,"bold","roman","normal","normal"))
        

        # 問題数入力欄
        self.EditBox_amount = tk.Entry(master = self,width=7)
        self.EditBox_amount.insert(tk.END,self.amount)
        

        #　文字列「問」
        self.Label_amount2 = tk.Label(master = self, text=u' questions',bg=gloVal.Back_color,
                                    font =("Arial Black",15,"bold","roman","normal","normal"))
        

        # 英和/和英モードを切り替えるチェックボックスを設置する．
        self.Val_mode = tk.BooleanVar()
        self.Val_mode.set(False)
        self.Check_mode = tk.Checkbutton(master = self, text = u'Mode change : Jap > Eng',variable = self.Val_mode,
                                        bg=gloVal.Back_color,font =("Arial Black",15,"bold","roman","normal","normal"))
        

        # 制限時間モードに切り替えるチェックボックスと，制限時間(秒)の設定欄を設置する．
        self.Val_time = tk.BooleanVar()
        self.Val_time.set(False)
        self.Check_time = tk.Checkbutton(master = self, text = u'Set up a time limit :',variable = self.Val_time,
                                        bg=gloVal.Back_color,font =("Arial Black",15,"bold","roman","normal","normal"))
        
        self.EditBox_time = tk.Entry(master = self,width=7)
        self.Label_time = tk.Label(master = self, text = u' s',width=1,bg=gloVal.Back_color,
                                    font =("Arial Black",15,"bold","roman","normal","normal"))
        

        # スタートボタンを設置する
        self.Test_Launch_Button = tk.Button(master = self, text=u'START',command = self.gotoTesting,bg=gloVal.Accent_Red,
                                        highlightbackground = gloVal.Wine_Red,highlightthickness = 3,font =("Arial Black",20,"bold","roman","normal","normal"))
       
       # コピーライトを描画する
        Label_copyright = tk.Label(self, text = gloVal.copyright,bg=gloVal.Back_color)

        self.Button_home.place(relwidth=0.15, relheight= 0.05, relx= 0.85, rely=0)
        self.DB_Combo.place(relwidth=0.6, relheight= 0.033, relx= relx_def, rely=rely_def)

        self.Label_title.place(relx=relx_def+0.02, rely=rely_def + 0.05)
        self.EditBox_start.place(relheight= 0.06, relx=relx_def+0.05, rely=rely_def+0.09)
        self.Label_start_end.place(relx=relx_def+0.21, rely=rely_def+0.1)
        self.EditBox_end.place(relheight= 0.06, relx=relx_def+0.27, rely=rely_def+0.09)
        
        self.Label_amount.place(relx=relx_def+0.02, rely=rely_def + 0.17)
        self.EditBox_amount.place(relheight= 0.06, relx=relx_def+0.05, rely=rely_def + 0.21)
        self.Label_amount2.place(relx=relx_def+0.2, rely=rely_def+0.22)

        self.Check_mode.place(relx=relx_def+0.02, rely=rely_def + 0.30)

        self.Check_time.place(relx=relx_def+0.02, rely=rely_def + 0.36)
        self.EditBox_time.place(relheight= 0.06, relx=relx_def + 0.4, rely=rely_def + 0.35)
        self.Label_time.place(relx=relx_def+0.55, rely=rely_def + 0.36)
        
        self.Test_Launch_Button.place(relwidth=0.6, relheight= 0.08, relx= 0.2, rely=0.85)
        
        Label_copyright.place(relx = 0,rely=0.95)

    def ExtractIdentify(self):
        with open("identify/identify.csv",'r',encoding="utf-8_sig") as f:
            l_pre = [s.strip() for s in f.readlines()]
            l = l_pre[0].split(',')
            return l[0], l[1], l[2], l[3]

    def SaveIdentify(self,s,e,a,path):
        with open("identify/identify.csv", 'w',newline="",encoding = 'utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([str(s),str(e),str(a),str(path)])

    def ExtractProblemsData(self,path):
    
        # 単語データベースpathから単語情報(英単語，その和訳)を抽出する．
        with open(path,'r',encoding="utf-8_sig") as f:
            l = [s.strip() for s in f.readlines()]
            lenl = len(l)
            # 元データの全長を返す
            self.ExtactWordlist_length = lenl
        f.close()
        returnl = [[0 for i in range(5)] for j in range(lenl)]
        for i in range(lenl):
            wordandJap = l[i].split(',')
            
            # 単語リストの構造を，[英単語,和訳,クリアチェッカ] とする
            returnl[i][0] = wordandJap[1]   # English
            returnl[i][1] = wordandJap[2]   # Japanese
            returnl[i][2] = False           # Clear checker
            returnl[i][3] = wordandJap[0]   # WordNumber
            returnl[i][4] = wordandJap[3]   # Word(0) or Idiom(1)?
        
   
        # 抽出データと，抽出データの長さを返す
        self.ExtractWordlist = returnl

    def MakeProblems(self,Allwordlist,start,end,amount):
        # 単語リストをstart,endに応じて切り出し，pre_wordlistに格納する
        pre_wordlist = []
        Problems = []
        for i in range(start-1,end):
            pre_wordlist.append(Allwordlist[i])
        
        # pre_wordlistの要素をシャッフルする．
        random.shuffle(pre_wordlist)
        # pre_wordlistの先頭から数えてamountの分だけ,wordlistに格納する．
        for i in range(amount):
            Problems.append(pre_wordlist[i])
        # wordlistを返す
        return Problems

    def gotoTesting(self):
        # start, end, amount , mode : int
        # time : boolean
        DB = self.DB_Combo.get()
        s = int(self.EditBox_start.get())
        e = int(self.EditBox_end.get())
        a = int(self.EditBox_amount.get())
        m = int(0) # modeはFalse(英和) = 0，True(和英) = 1とここで定義変換する．
        if self.Val_mode.get():
            m = int(1)
        t = self.Val_time.get()
        
        # ドロップダウンリストで選択した単語帳のパスを検索し，問題を生成する
        path = gloVal.Word_Databases.index(DB)
        self.ExtractProblemsData(gloVal.Word_Databases_path[path])
        self.SaveIdentify(s,e,a,path)

        # 各設定値が正当でない場合はアラートを出すのみに抑える．
        if s == '' or e =='':
            messagebox.showerror('ERROR','テスト範囲が入力されていません')
        elif (s <= 0)or(s > self.ExtactWordlist_length):
            messagebox.showerror('ERROR','テスト範囲(開始番号) の番号が0以下，あるいは大きすぎます．\n指定した単語帳の単語収録数は '+str(self.ExtactWordlist_length)+' です．\nそれよりも小さい数字を指定してください．')
        elif (e <= 0)or(e > self.ExtactWordlist_length):
            messagebox.showerror('ERROR','テスト範囲(終了番号) の番号が0以下，あるいは大きすぎます．\n指定した単語帳の単語収録数は '+str(self.ExtactWordlist_length)+' です．\nそれよりも小さい数字を指定してください．')
        elif a == '':
            messagebox.showerror('ERROR','問題数が入力されていません')
        elif a > 999:
            messagebox.showerror('ERROR','申し訳ありませんが、\n問題数は999以下でお願いします。')
        elif s > e:
            messagebox.showerror('ERROR','テスト範囲の設定に問題があります\n開始番号(左) が終了番号(右) よりも小さくなるようにしてください')
        elif (e-s+1) < a:
            messagebox.showerror('ERROR','指定されたテスト範囲に対して，問題数が多すぎます\n (テスト範囲内の単語数) ≧ (問題数) になるようにしてください')
        #　設定値にエラーがない場合は，テスト画面に移行する．
        else:
            #抽出データとその長さを取得
            EWl = self.ExtractWordlist
            EWl_length = self.ExtactWordlist_length

            #問題として出題する問題集を作成する
            Ploblems = self.MakeProblems(EWl, s,e,a)
            # 設定値と，問題集をすべて辞書として纏める
            d = {'amount':a, 'mode':m, 'time':t, 'Problems':Ploblems,'ExtractWordlist':EWl,
                'ExtractWordlist_length':EWl_length,'DatabaseName':DB}
            dic = {'path':'figure/Preset2Testing_shift.gif','nextframe':'Testing','ratio':30,
                'App':self.App, 'passData':d}
            #frameを更新するchange関数に，テスト画面frameと，先ほどの辞書を返す．
            #相互インポートを防止するため、ここでgif_animeを定義
            from tkinter_gifplay import gifanime_onFrame
            return self.master.change(gifanime_onFrame,**dic)
