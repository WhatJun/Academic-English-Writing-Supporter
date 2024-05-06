"""
Author: Wenjun ZHU
Start_Date: 2024/04/21
First_Release: 2024/05/

Intro:学術的な英単語を集め、復習するための単語帳です。
        さらに、英語で学術論文を書くときに、この単語帳を利用して、相応しい英単語を調べることができます。
        
Pages: 単語の暗記用のためのページ〇
単語を調べ、単語帳に入れるページ〇
日本語から辞書およびネットからヒットする単語を検索するページ〇
辞書の単語を確認でき、またいらない単語を削除できるページ〇

Functions: 
辞書の単語をアルファベット順と入れた順で並び替えることができるようにする〇
単語をどれくらい覚えているかをテストするためのページ(in future)
意味的に近い言葉の連想(学習ずみのword2vecモデルに基づく)〇起動するのに時間がかかるが
検索エンジンが選択できる(in future)
検索言語が選択できる(in future)
ヒット語がWLにある場合に色変する(in progress)
"""

import csv 
import random
import tkinter as tk
import pandas as pd
from search import Search
from search2 import SearchAcademicWord
from tkinter import ttk
from IPython.display import display

# CSVファイルのパス
wordPATH = "./wordfile/wordList.csv"


class VocabularyApp:
    # main pageのクラス
    
    def __init__(self, master):
        self.master = master 
        self.master.title("英単語学習") 
        self.master.geometry("900x500+300+150") # ウィンドウサイズと開始位置の設定
        self.master.configure(bg="#FFFFFF") # ウィンドウの背景色
        
        self.load_words() # 単語の読み込み
        self.current_index = -1  # 現在の単語のインデックス
        self.create_widgets() # GUIウィジェットの作成
        self.next_word() # 次の単語を表示

    def load_words(self):
        # CSVファイルから英単語などを読み込む
        self.words = []
        with open(wordPATH, newline = "", encoding = "utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader) # 一行目を飛ばす
            for row in reader:
                self.words.append(row)
        #単語の提示順番をシャフルする
        random.shuffle(self.words)

    def create_widgets(self):
        # GUIの設定
        
        # ラベルやボタンの作成と配置
        self.textWord = tk.Label(self.master, bg="#FFFFFF", font=("Times New Roman", 36))
        self.textMeaning = tk.Label(self.master, bg="#FFFFFF", font=("YU Gothic", 24))
        self.textMeaning2 = tk.Label(self.master, bg="#FFFFFF", font=("YU Gothic", 24))
        self.textMeaning3 = tk.Label(self.master, bg="#FFFFFF", font=("YU Gothic", 24))
        self.textPron = tk.Label(self.master, bg="#FFFFFF", font=("Helvetica", 24))
        self.buttonShow = tk.Button(self.master, text="Show", font=12,width=20, command=self.show_hint)
        self.buttonNext = tk.Button(self.master, text="Next", font=12, width=20, command=self.next_word)
        self.buttonWinSP = tk.Button(self.master, text="Search(En→日)", font=10, width=20, command=self.open_winSP)
        self.buttonWinSP2 = tk.Button(self.master, text="Search(Academic)", font=10, width=20, command=self.open_winSP2)
        self.buttonWinWL = tk.Button(self.master, text="Word List", font=10, width=20, command=self.open_winWL)
        self.buttonExit = tk.Button(self.master, text="Exit", font=12, width=20,command=self.master.quit)
                
        self.textWord.pack()
        self.textPron.pack()
        self.textMeaning.pack()
        self.textMeaning2.pack()
        self.textMeaning3.pack()
        self.buttonShow.pack()
        self.buttonNext.pack()
        self.buttonWinSP.pack()
        self.buttonWinSP2.pack()
        self.buttonWinWL.pack()
        self.buttonExit.place(x=650, y=450)
    
    def show_hint(self):
        # 意味と発音を表示する関数
        
        # 表示色を変更することで実現
        self.textMeaning.config(fg="#000000")
        self.textMeaning2.config(fg="#000000")
        self.textMeaning3.config(fg="#000000")
        self.textPron.config(fg="#000000")

    def next_word(self):
        # 次の単語を表示させるための関数
        
        self.current_index += 1
        if self.current_index < len(self.words):
            word, meaning, pron, meaning2, meaning3 = self.words[self.current_index]
            self.textWord.config(text=word)
            self.textMeaning.config(text=meaning, fg="#FFFFFF")
            self.textMeaning2.config(text=meaning2, fg="#FFFFFF")
            self.textMeaning3.config(text=meaning3, fg="#FFFFFF")
            self.textPron.config(text=pron, fg="#FFFFFF")
        else:
            # 全部終わったときのメッセージ
            self.textWord.config(text="Finsihed!")
            
    def open_winSP(self):
        # 検索用のウィンドウを開く
        
        self.buttonWinSP = tk.Toplevel(self.master)
        self.app = SearchPage(self.buttonWinSP)
    
    def open_winSP2(self):
        # academic英語を検索するページを開く
        
        self.buttonWinSP2 = tk.Toplevel(self.master)
        self.app = SearchPageAW(self.buttonWinSP2)
        
    def open_winWL(self):
        # 辞書のウィンドウを開く
        
        self.buttonWinWL = tk.Toplevel(self.master)
        self.app = WordListPage(self.buttonWinWL)
        

class SearchPage:
    # 検索ウィンドウのクラス
    
    def __init__(self, master):
        
        self.master = master 
        self.master.title("英単語検索&記録")
        self.master.geometry("500x300+300+300")
        self.master.configure(bg="#FFFFFF")
        
        self.create_widgets()
        self.search = Search()
        
    def create_widgets(self):
        # GUIの設定
        
        # ラベルやボタンの作成と配置
        self.labelSearchWord = tk.Label(self.master, text="検索する単語：", bg="#FFFFFF", font=("Meiryo", 15), anchor=tk.CENTER)
        self.searchBox = tk.Entry(self.master, bg="#f5c6ef", font=20) # 検索語を入力する場所
        self.labelSearchOnset = tk.Label(self.master, text="↲", bg="#FFFFFF", font=("Meiryo", 15), anchor=tk.CENTER)
        self.labelMean = tk.Label(self.master, text="意味：", bg="#FFFFFF", font=("Meiryo", 15), anchor=tk.CENTER)
        self.searchResults = tk.Text(self.master, bg="#d5f5ee",width=25, height=5, font=10) # 検索結果の意味を提示する場所
        self.labelPron = tk.Label(self.master, text="発音：", bg="#FFFFFF", font=("Meiryo", 15), anchor=tk.CENTER)
        self.searchPron = tk.Text(self.master, bg="#d5f5ee", width=20, height=1, font=10) #検索結果の発音を提示する場所
        self.ButtonADD = tk.Button(self.master, text="記録", font=8, width=18, command=self.addWord)
        self.buttonExit = tk.Button(self.master, text="Exit", font=8, width=18, command=self.quit_win)
    
        self.labelSearchWord.grid(row=0, column=0)
        self.searchBox.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=10)
        self.labelSearchOnset.grid(row=0, column=2)
        self.searchBox.bind("<Return>", self._search) #検索をonsetするための設定
        self.labelMean.grid(row=1, column=0)
        self.searchResults.grid(row=1, column=1, columnspan=2, sticky=tk.W, padx=5,pady=5)
        self.labelPron.grid(row=2, column=0)
        self.searchPron.grid(row=2,column=1,columnspan=2, sticky=tk.W, padx=5,pady=5)
        self.ButtonADD.place(x=100, y=250)
        self.buttonExit.place(x=300, y=250)
        
    def _search(self, event="<Return>"):
        # 検索関数
        
        #結果を乗せる変数
        self.mean = ""
        self.pron = ""
        
        # 結果テキストボックスに文字が含まれていたときクリアする
        if self.searchResults.get("1.0", tk.END):
            self.searchResults.delete("1.0", tk.END)
            
        if self.searchPron.get("1.0", tk.END):
            self.searchPron.delete("1.0", tk.END)
        
        # 検索ボックスから入力を取得
        searchWord = self.searchBox.get()
        
        # 検索語とcsvファイルのパスを渡す
        self.search.set_word(searchWord)
        self.search.set_csv(wordPATH)
        
        # 検索語がWLにあるか否かで分岐
        if self.search.if_in_list():
            # 保存した意味と発音を返す
            self.mean, self.pron = self.search.get_mean()
            self.mean += "（すでに保存済み）"
        else:
            # 検索した意味と発音を返す
            self.mean, self.pron=self.search.search()
        
        # 結果ボックスに意味を格納
        self.searchResults.insert("1.0", self.mean)
        self.searchPron.insert("1.0", self.pron)
        
    def addWord(self):
        # 検索語をWLに格納するための関数
        
        # WordListのデータフレームを取得
        WL = pd.read_csv(wordPATH)
        
        if self.searchBox.get() not in WL["words"].values:
            # 検索語がWLにない場合
            
            means = self.mean.split("、") #searchから渡された意味を「、」ごとに分割し、means_listに格納する
           
            # meansが少なくとも3つの要素があるように
            while len(means) < 3:
                means.append("")
            
            # 新しいWLに格納する語の各要素を列ラベルに対応し整合する
            new_word = pd.DataFrame([[self.searchBox.get(),means[0],self.pron,means[1],means[2]]], columns=WL.columns)
            
            # 新しい語の列をWLの一番最後に挿入した新しいWLを作る
            new_WL = pd.concat([WL, new_word], ignore_index=True)
            
            # 新しいWLをWLに導出する
            new_WL.to_csv(wordPATH, index=False)
            
            #WLに格納したことのフィードバック
            self.searchResults.insert("end", "\n記録しました", "blueTag")
            self.searchResults.tag_config("blueTag", foreground="blue")
        else: # 検索語がすでにWLにあった場合
            self.searchResults.insert("end", "もうすでに辞書に入っています", "redTag")
            self.searchResults.tag_config("redTag", foreground="red")
        
    def quit_win(self):
        # windowを閉じる関数
        self.master.destroy()            


class WordListPage:
    #保存した単語を確認するページ
    
    def __init__(self, master):
        
        self.master = master 
        self.master.title("英単語辞書")
        self.master.geometry("1200x500+100+100") # ウィンドウサイズと開始位置の設定
        self.master.configure(bg="#FFFFFF") #windowの背景色

        self.state_ascending = False # ソートの順番の設定
        self.WL = pd.read_csv(wordPATH) # CSVから単語リストを読み込み、データフレームとしてself.WLに格納
        self.create_widgets() # ウィジェットの作成
        self.show_words() # 単語を表示

    def create_widgets(self):
        #右クリックメニューの設定
        self.menu = tk.Menu(self.master, tearoff=0, activebackground="#000000")
        self.menu.add_command(label="Delete", command=self.delete_Word)
        self.master.bind("<Button-3>", self.show_menu) # 右クリックによるメニュー表示をバインド
        
        #tableの設定
        frame = tk.Frame(self.master)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5) # フレームの設定と配置
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        
        self.tree = ttk.Treeview(frame) # Treeviewの作成
        self.tree.column("#0", width=50, stretch=tk.NO, anchor=tk.E) # 列設定
        self.tree.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S) # Treeviewの配置
        
        vscrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=lambda:self.tree.yview)
        self.tree.configure(yscrollcommand=vscrollbar.set) # スクロールバー設定
        vscrollbar.grid(row=0, column=1, sticky=tk.W + tk.E + tk.N + tk.S)
        
        self.tree["column"] = (1,2,3) # 列の設定
        self.tree["show"] = "headings" # ヘッダーのみ表示
        
        self.tree.heading(1, text="単語", command=self._sort) # 列のヘッダー
        self.tree.heading(2, text="発音")
        self.tree.heading(3, text="意味")
    
    def show_words(self):
        # 単語帳の内容を表示する関数
        
        # 既存の内容をクリア
        self.tree.delete(*self.tree.get_children())
        
        # データフレーム全体をコピーし、NaN を空文字列に
        wl_copy = self.WL.fillna('')  
            
        def combine_meanings(*meanings):
            # 3つの meanings を整合し、空の部分は無視して「、」が重複しないようにする関数
            return '、'.join(filter(None, meanings))

        # Treeview にデータを挿入
        for i in wl_copy.index:
            meaning_combined = combine_meanings(wl_copy["meaning"][i], wl_copy["meaning2"][i], wl_copy["meaning3"][i])
            self.tree.insert("", "end", values=(wl_copy["words"][i], wl_copy["pron"][i], meaning_combined))

    def _sort(self):
        # 単語の並び替え関数
        
        # 昇順と降順を切り替える
        self.state_ascending = not self.state_ascending
        
        # dataframeをsort
        self.WL = self.WL.sort_values(by="words", ascending=self.state_ascending)
        
        # sortしたdataframeを反映する
        self.show_words()

    def show_menu(self, e):
        # 右クリックメニューを表示する関数
        
        #マウスイベントが発生したxとyの座標に基づいてTreeViewウィジェットの特定の領域を識別、'heading', 'cell', 'tree', 'separator', 'nothing'を返す
        region = self.tree.identify_region(e.x, e.y)
        
        if region == "cell": # クリックされたのがセルの場合
            self.tree.selection_set(self.tree.identify_row(e.y)) # クリックされた行を選択
            self.menu.post(e.x_root, e.y_root) # メニューを表示
        
    def delete_Word(self):
        # 選択された単語を削除する関数
        
        selected_item = self.tree.selection() 
        index = self.tree.item(selected_item[0], "values")[0] # 選択されたアイテムのインデックス取得
        self.WL = self.WL[self.WL["words"] != index] # DataFrameから単語を削除
        self.tree.delete(selected_item) # Treeviewからアイテムを削除
        self.WL.to_csv(wordPATH, index=False) # 変更をCSVに保存


class SearchPageAW:
    # 日本語から英語を検索するページ
    def __init__(self, master):
        
        self.master = master 
        self.master.title("Academic Search")
        self.master.geometry("500x500+500+100") # ウィンドウサイズと開始位置の設定
        self.master.configure(bg="#FFFFFF") #windowの背景色
        
        self.WL = pd.read_csv(wordPATH)
        self.create_widgets() # ウィジェットの作成
        self.search = SearchAcademicWord()
        
    def create_widgets(self):
        #右クリックメニューの設定
        # self.menu = tk.Menu(self.master, tearoff=0, activebackground="#000000")
        # self.menu.add_command(label="Save", command=self.save_word)
        # self.master.bind("<Button-3>", self.show_menu) # 右クリックによるメニュー表示をバインド
        
        self.labelSearchWord = tk.Label(self.master, text="検索する単語：", bg="#FFFFFF", font=("Meiryo", 15), anchor=tk.CENTER)
        self.searchBox = tk.Entry(self.master, bg="#f5c6ef", font=20) # 検索語を入力する場所
        self.searchBox.bind("<Return>", self._search)
        self.labelSearchOnset = tk.Label(self.master, text="↲", bg="#FFFFFF", font=("Meiryo", 15), anchor=tk.CENTER)
        
        self.labelSearchWord.pack() 
        self.searchBox.pack()
        self.labelSearchOnset.pack()
        
        #tableの設定
        frame = tk.Frame(self.master)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5) # フレームの設定と配置
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        
        self.tree = ttk.Treeview(frame) # Treeviewの作成
        self.tree.column("#0", width=50, stretch=tk.NO, anchor=tk.E) # 列設定
        self.tree.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S) # Treeviewの配置
        # vscrollbar = ttk.Scrollbar(self.master, orient=tk.VERTICAL, command=self.tree.yview)
        # self.tree.configure(yscrollcommand=vscrollbar.set) # スクロールバー設定
        # vscrollbar.grid(row=0, column=1, sticky=tk.W + tk.E + tk.N + tk.S)
        
        self.tree["column"] = (1,2) # 列の設定
        self.tree["show"] = "headings" # ヘッダーのみ表示
        
        self.tree.heading(1, text="単語") # 列のヘッダー
        self.tree.heading(2, text="意味")
        
    def _search(self, event="<Return>"):
        # 検索関数
        
        #結果を乗せる変数
        self.word = ""
        self.mean = ""
        
        # 検索ボックスから入力を取得
        searchWord = self.searchBox.get()
        
        # 検索語とcsvファイルのパスを渡す
        self.search.set_word(searchWord)
        self.search.set_csv(wordPATH)
        
        # 検索語から英訳を取得
        try:
            self.search.get_En()
        except:
            errorMessage = "検索語の英語が存在しないかネットにつながらりせん"
            self.tree.delete(*self.tree.get_children())
            self.tree.insert("", "end", values=(errorMessage, ""))
            return
        
        # 英訳から同義語を取得
        try:    
            self.search.get_syn()
        except:
            None
            
        # 同義語からその意味を調べ、結果に渡す
        results = self.search.get_results()

        display(results)
        
        # treeをリセット
        self.tree.delete(*self.tree.get_children()) 
        
        # 結果treeに英単語と意味を格納
        for i in results.index:
            self.tree.insert("", "end", values=(results["words"][i], results["meanings"][i]), tags=str(results["tag"][i]))
        self.tree.tag_configure("red", background="#ff0000")    
             
    # def show_menu(self, e):
    #     # 右クリックメニューを表示する関数
        
    #     # マウスイベントが発生したxとyの座標に基づいてTreeViewウィジェットの特定の領域を識別、'heading', 'cell', 'tree', 'separator', 'nothing'を返す
    #     region = self.tree.identify_region(e.x, e.y)
        
    #     if region == "cell": # クリックされたのがセルの場合
    #         self.tree.selection_set(self.tree.identify_row(e.y)) # クリックされた行を選択
    #         self.menu.post(e.x_root, e.y_root) # メニューを表示
    
    def save_word(self):
        None
    
        
# if __name__ == "__main__":
root = tk.Tk()
app = VocabularyApp(master=root)
root.mainloop()