import tkinter as tk
import tkinter.ttk as ttk
import glob
import os
import datetime
import csv
from WordTestGUI_Testing import Frame_testing
from WordTestGUI_Preset import Frame_preset
import WordTestGUI_Globals as gloVal
import shutil

listbox_height = 0.68
listbox_width = 0.63
listbox_y = 0.3
relx_left = 0.05
relx_right = relx_left + listbox_width + 0.04


class Frame_remind(tk.Frame):
    
    def __init__(self, master=None):
        
        tk.Frame.__init__(self, master)
        master.title("Sanaru(Anjo):WordReminder")
        """
        self.Image_Background = tk.PhotoImage(file = 'figure/Preset_background.gif')
        self.Label_background = tk.Label(self, image = self.Image_Background)
        self.Label_background.place(x=0,y=0)
        """

        self.Reminder = []
        self.name = ''
        self.csv_file_name = ''

        Button_back = tk.Button(master=self,text="HOME",width=5,bg = "#00a4e4",fg = "#b40000",
                        command=self.master.backToHome,font =("Arial Black",20,"bold","roman","normal","normal"))
        Button_back.pack(anchor =tk.E)

        self.img = tk.PhotoImage(file = 'figure/gotoremind_move.gif')
        Label_RemindTitle = tk.Label(master = self, width = 399, height = 119,image = self.img)
        Label_RemindTitle.place(relx = 0, rely = 0)
        
        # Database select widget
        label_Combo = tk.Label(self, text=u' ■ Select a wordbank you want to know your results',
                                    font =("Arial Black",10,"bold","roman","normal","normal"))
        label_Combo.place(relx = relx_left , rely = 0.2)

        self.combo_wordbank = ttk.Combobox(master = self,state = 'readonly')
        self.combo_wordbank["values"] = gloVal.Word_Databases
        self.combo_wordbank.place(relx = relx_left,rely = 0.25)
        self.combo_wordbank.bind('<<ComboboxSelected>>',self.MakeRemindlist_UpNo)

        #スクロールバーの作成
        scroll = tk.Scrollbar(self,troughcolor = gloVal.Accent_Red)
        #スクロールバーの配置を決める
        scroll.place(relheight = listbox_height, relwidth = 0.025, relx = relx_left + listbox_width - 0.01, rely = listbox_y)

        #リストボックスの作成
        self.list_value=tk.StringVar()
        listbox = tk.Listbox(self,listvariable=self.list_value,selectmode="single",state = 'disable',
                            font =(u"Courier",15,"bold","roman","normal","normal"),yscrollcommand=scroll.set)
        listbox.place(relheight = listbox_height,relwidth = listbox_width,relx = relx_left,rely = listbox_y)
        #部品の動きをスクロールバーに反映させる
        scroll["command"]=listbox.yview

        Label_inorderof = tk.Label(master = self, text = u'Rearrange',font =(u"Courier",15,"bold","roman","normal","normal"))
        Label_inorderof.place(relx = relx_right, rely = listbox_y)

        self.Button_DownTtC = tk.Button(master=self,text="Ascending\nto correct",bg = "#00a4e4",fg = "black",highlightbackground = "Red",
                    command=self.MakeRimindList_DownTtC,font =("Arial Black",13,"bold","roman","normal","normal"),state = 'disable')
        self.Button_DownTtC.place(relwidth = 0.22,relx = relx_right+0.02, rely = listbox_y + 0.05)    

        self.Button_UpTtC = tk.Button(master=self,text="Descending\nto correct",bg = "#00a4e4",fg = "black",highlightbackground = "Blue",
                    command=self.MakeRimindList_UpTtC,font =("Arial Black",13,"bold","roman","normal","normal"),state = 'disable')
        self.Button_UpTtC.place(relwidth = 0.22,relx = relx_right+0.02, rely = listbox_y + 0.13)   

        self.Button_UpNo = tk.Button(master=self,text="Undo\nArrangement.",bg = "#00a4e4",fg = "black",highlightbackground = "Gray",
                    command=self.MakeRimindList_UpNo,font =("Arial Black",13,"bold","roman","normal","normal"),state = 'disable')
        self.Button_UpNo.place(relwidth = 0.22,relx = relx_right+0.02, rely = listbox_y + 0.21)   


        overcome_place = 0.35
        Label_SetTest = tk.Label(master = self, text = u'Overcome Weak',font =(u"Courier",15,"bold","roman","normal","normal"))
        self.EditBox_amount = tk.Entry(master = self,width=4)
        self.EditBox_amount.insert(tk.END,50)
        Label_problem = tk.Label(master = self, text = u'Problem',font =(u"Courier",12,"bold","roman","normal","normal"))
        self.Button_START = tk.Button(master=self,text="Remind Test\nSTART",bg = "#00a4e4",fg = "black",highlightbackground = "Blue",
                    command=self.LaunchRemindTest,font =("Arial Black",13,"bold","roman","normal","normal"),state = 'disable')
        Label_SetTest.place(relx = relx_right, rely = listbox_y + overcome_place)
        self.EditBox_amount.place(relx = relx_right+0.02, rely = listbox_y + overcome_place + 0.04)
        Label_problem.place(relx = relx_right + 0.12, rely = listbox_y + overcome_place + 0.0405)
        self.Button_START.place(relwidth = 0.22,relx = relx_right+0.02, rely = listbox_y + overcome_place + 0.09)   


    def MakeRemindlist_UpNo(self,event):
        self.name = self.combo_wordbank.get()
        self.csv_file_name = "Results/Statistics/"+ str(self.name) +"_Reminder.csv"
        # ドロップダウンリストで選択した単語帳に対応するリザルトを全検索(filename_correct)し、その中身を抽出(result)する
        DB_path = gloVal.Word_Databases_path[gloVal.Word_Databases.index(self.name)]
        DBname = '['+str(self.name)+']'
        filelist = ([os.path.basename(p) for p in glob.glob('Results/Log/*.csv', recursive=True)
                    if os.path.isfile(p)])
        filelist_correct = []
        for i in range(len(filelist)):
            if DBname in filelist[i]:
                filelist_correct.append(filelist[i])
        
        result = []
        for i in range(len(filelist_correct)):
            path = 'Results/Log/'+ str(filelist_correct[i])
            with open(path, 'r' ,encoding = "utf-8_sig") as f:
                l = [s.strip() for s in f.readlines()]
            f.close()
            for j in range(len(l)):
                l2 = l[j].split(',')
                result.append(l2)
        shutil.rmtree('Results/Log')
        # 全データベースを用いてリマインダを生成したのち、
        # リザルトから得た正誤をリマインダに当てはめる

        with open(DB_path,'r',encoding="utf-8_sig") as f:
            l = [s.strip() for s in f.readlines()]
        f.close()
        remind = [[0 for i in range(5)] for j in range(len(l))]
        for i in range(len(l)):
            wordandJap = l[i].split(',')
            
            # 単語リストの構造を，[No,英単語,和訳,クリアチェッカ,Word or Idiom] とする
            remind[i][0] = wordandJap[1]   # English
            remind[i][1] = wordandJap[2]   # Japanese
            remind[i][2] = 0               # The time of correct
            remind[i][3] = int(wordandJap[0])   # WordNumber
            remind[i][4] = wordandJap[3]   # Word(0) or Idiom(1)?

        #過去のリマインダが存在していれば、それのクリアチェッカを読み込んで現在のremindのクリアチェッカに格納する。

        if os.path.exists(self.csv_file_name):
            with open(self.csv_file_name,'r',encoding="utf-8_sig") as f:
                pre_reminder = [s.strip() for s in f.readlines()]
            f.close()
            for i in range(len(l)):
                pre_reminder_part = pre_reminder[i].split(',')
                remind[i][2] = int(pre_reminder_part[3])
            

        for i in range(len(result)):
            if result[i][2] == '○':
                remind[int(result[i][0])-1][2] += 1
        #Logを作り直す
        os.mkdir('Results/Log')
        self.Button_UpTtC['state'] = 'normal'
        self.Button_DownTtC['state'] = 'normal'
        self.Button_UpNo['state'] = 'normal'
        self.Reminder = remind
        self.MakeRemindFile(remind)
        self.MakeRemindStrings(self.Reminder)

    def MakeRimindList_UpTtC(self):
        self.Button_UpTtC['state'] = 'disable'
        remind = sorted(self.Reminder,key = lambda x: x[2])
        self.Reminder = remind
        self.MakeRemindStrings(self.Reminder)
        self.Button_UpTtC['state'] = 'normal'
        self.Button_START['state'] = 'normal'

    def MakeRimindList_DownTtC(self):
        self.Button_DownTtC['state'] = 'disable'
        remind = sorted(self.Reminder,key = lambda x: -x[2])
        self.Reminder = remind
        self.MakeRemindStrings(self.Reminder)
        self.Button_DownTtC['state'] = 'normal'
        self.Button_START['state'] = 'disable'

    def MakeRimindList_UpNo(self):
        self.Button_UpNo['state'] = 'disable'
        remind = sorted(self.Reminder,key = lambda x: x[3])
        self.Reminder = remind
        self.MakeRemindStrings(self.Reminder)
        self.Button_UpNo['state'] = 'normal'
        self.Button_START['state'] = 'disable'

    def MakeRemindStrings(self, remind):
        remindString = ''
        maxlen = 0
        for i in range(len(remind)):
            if len(remind[i][0]) > maxlen:
                maxlen = len(remind[i][0])
        for i in range(len(remind)):
            remindString = remindString + str(str(remind[i][3]).rjust(4,'0'))+ '.' + str(remind[i][0].ljust(maxlen+1,'-'))
            count = remind[i][2]   
            for j in range(int(count/100)):
                remindString = remindString + '★'
            for j in range(int((count%100)/10)):
                remindString = remindString + '◆'    
            for j in range((count%10)):
                remindString = remindString + '■'
            remindString = remindString + '\n'
        self.list_value.set(remindString)

    def MakeRemindFile(self, remind):
        
        with open(self.csv_file_name, 'w',newline="",encoding = 'utf-8') as f:
            writer = csv.writer(f)
            for i in range(len(remind)):
                writer.writerow([remind[i][3],remind[i][0],remind[i][1],remind[i][2],remind[i][4]])

    def ExtractProblemsData(self,path):
        
        # 単語データベースpathから単語情報(英単語，その和訳)を抽出する．
        with open(path,'r',encoding="utf-8_sig") as f:
            l = [s.strip() for s in f.readlines()]
            lenl = len(l)
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
        return returnl, lenl
    
    def MakeProblems(self,amount):

        problems = []
        for i in range(amount):
            problems.append(self.Reminder[i])
        return problems

    def LaunchRemindTest(self):
        
        a = int(self.EditBox_amount.get())
        # ドロップダウンリストで選択した単語帳のパスを検索し，問題を生成する
        DB = self.combo_wordbank.get()
        path = gloVal.Word_Databases.index(DB)
        EWl, EWl_length = self.ExtractProblemsData(gloVal.Word_Databases_path[path])
        Problems = self.MakeProblems(a)
        # 設定値と，問題集をすべて辞書として纏める
        d = {'amount':a, 'mode':0, 'time':False, 'Problems':Problems,'ExtractWordlist':EWl, 'ExtractWordlist_length':EWl_length,'DatabaseName':DB}
        #frameを更新するchange関数に，テスト画面frameと，先ほどの辞書を返す．
        return self.master.change(Frame_testing,**d)


    