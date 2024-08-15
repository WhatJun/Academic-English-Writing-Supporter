# reference:以下を参考にここの検索機能を実現した
# 【Python】検索機能付きの英単語帳を作ってみた【Tkinter】by @kaito2140(かいとくん) url:https://qiita.com/kaito2140/items/9aa809a8b5e7c6088381 


import requests
import pandas as pd
from bs4 import BeautifulSoup
 
# 検索エンジン名
SEARCH_ENGINE = "https://ejje.weblio.jp/content/"

# 表示する意味の個数
MEAN_NUM = 3

class Search:
    def __init__(self):
    # 英単語を検索・単語帳に英単語を追加するクラス

        # 読み込む辞書のパスをリセット
        self.path = None
        
        # 読み込んだ辞書をリセット
        self.wl = None
        
        # 検索する英単語のリセット
        self.word = None
        
    def set_word(self, word):
        # 検索する英単語を格納する関数
        # 引数: word
        self.word = word
    
    def if_in_list(self):
        # 検索した英単語がすでにWLに入っているかを確認する関数
        
        if self.word in self.wl.index.values:
            return True
        else:
            return False
    

    def get_mean(self):
        #検索語がすでにWLにある場合、meanとpronにWLのものを代入する
        mean = self.wl.at[self.word, "meaning"]
        pron = self.wl.at[self.word, "pron"]
        return mean, pron
    
    def set_csv(self, path):
        self.path = path
        
        self.wl = pd.read_csv(path)
        self.wl.set_index("words", inplace=True)
    
    def search(self):
        #ネット検索用関数
        #サイトにつながるかどうかを確認する
        try:
            search_word = SEARCH_ENGINE + self.word
            url = requests.get(search_word)
        except:
            errorMessage = "error1, 翻訳サイトにつながりません"
            return errorMessage, "error"
        
        #単語の意味と発音を調べて返す
        try:
            #意味を取得
            soup = BeautifulSoup(url.text, "html.parser")
            mean = soup.find(class_="content-explanation ej").get_text().strip().split("、")[:MEAN_NUM]
            mean ="、".join(mean)
            try: 
            #発音を取得
                pron = soup.find(class_="phoneticEjjeDesc").get_text()
            except:
                return mean, "発音が記録されず"
        except:
            errorMessage = "error2, 単語が存在しません"
            return errorMessage, "error"

        return mean, pron
        
        
    
    
