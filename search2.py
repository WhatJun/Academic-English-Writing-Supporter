'''
アルゴリズム:検索語の取得→その英語を検索→検索した英語と意味の近い単語を取得→WordListに保存されたものを優先に取り出す単語のリストを作る→各単語の意味を検索する→単語とその意味を渡す
'''

import numpy as np
import requests
import pandas as pd
from bs4 import BeautifulSoup
from gensim import models
# from IPython.display import display

model_path = "./wordvec/glove.6B.50d.txt"

model =  models.KeyedVectors.load_word2vec_format(model_path, binary=False)

SEARCH_ENGINE = "https://ejje.weblio.jp/content/" #日本語から英語を検索するための
# "https://www.deepl.com/ja/translator#ja/en/"

SEARCH_ENGINE2 = "https://ejje.weblio.jp/content/" #英語から日本語を検索するための

# 検索結果の数の設定
results_NUM = 5


class SearchAcademicWord:
    # 日本語から学術な英単語をWLとネットから検索できるためのクラス
    
    def __init__(self):
        self.path = None
        self.WL = None
        self.word = None
        self.en = None
             
    def set_csv(self, path):
        self.name = path
        self.WL = pd.read_csv(path)
        self.WL.set_index("words",inplace=True)
        
    def set_word(self, word):
        # 検索語の取得
        self.word = word
        
    def get_En(self):
        # 検索語（日本語）の英訳を取得
        self.en_in_WL = None
        self.en_from_net = None
        
        if self.word in self.WL[["meaning", "meaning2", "meaning3"]].values:
            # 検索語がすでにWLにある場合、そこから英語を取得
            resultRow = self.WL.query("meaning == @self.word or meaning2 == @self.word or meaning3 == @self.word").index.values
            # self.final_results = pd.concat([[self.final_results, resultRow]], ignore_index=True)
            self.en_in_WL = str(resultRow[0])
            self.en = self.en_in_WL
            
        else:
            # netから検索語の英語を取得
                search_word = SEARCH_ENGINE + self.word
                print("sw:"+ search_word)
                url = requests.get(search_word)
            
                soup = BeautifulSoup(url.text, "html.parser")
                self.en_from_net = soup.find(class_="content-explanation je").get_text().strip().split("、")[0].split("; ")[0]
                self.en_from_net ="".join(self.en_from_net)
                # self.en = soup.find(class_="dictLink featured").get_text()strip().split("、")[:1] deeplを使う場合
                # self.en = self.en[0].split("; ")[:1]
                self.en = self.en_from_net
                
        # print(f"en:{self.en}")
        
    def get_syn(self):
        # 言語モデルと通して、意味的に近い単語を10つ抽出
        
        self.syn_in_WL = []
        self.syn_from_net = []
        
        # 最初の検索用の英語を入れる
        if self.en_in_WL:
            self.syn_in_WL.append(self.en_in_WL)
        if self.en_from_net:
            self.syn_from_net.append(self.en_from_net)
        
        # 類似する単語のリストを取得
    
        # 検索語の英語に最も意味的に近い単語を、検索結果の数の2倍個取得
        most_similar_words = model.most_similar(self.en, topn=results_NUM*2)
        
        # すべてのタプルから単語部分だけを取り出す
        synonyms = [w for w, _ in most_similar_words]
    
         
        # synonyms_str = ', '.join(str(s) for s in synonyms)
        # print("syn:" + synonyms_str)
        
        # 意味的に近い単語の中からWLに保存されているものを優先的に結果単語リストに入れる
        for word in synonyms:
            if word in self.WL.index.values:
                self.syn_in_WL.append(word)
            else:    
                self.syn_from_net.append(word)
        # print(f"syninwl:{self.syn_in_WL}")
            
    def get_results(self):
        # 結果単語の意味を検索し、結果語と結果意味を渡す
          
        final_results = pd.DataFrame(columns=["words", "meanings", "tag"])
        
        if self.syn_in_WL:
            for syn_in in self.syn_in_WL:
                # 各同義語がWLにある行を取得
                
                resultRow = self.WL.query("words == @syn_in")
                # display(resultRow)
                
                # nanを消す
                resultRow = resultRow.fillna('')  
                
                def combine_meanings(*meanings):
                    # 3つの meanings を整合し、空の部分は無視して「、」が重複しないようにする関数
                    return '、'.join(filter(None, meanings))
                
                # 3つの意味を整合
                mean = combine_meanings(resultRow.iloc[0]["meaning"], resultRow.iloc[0]["meaning2"], resultRow.iloc[0]["meaning3"])
                
                # mean = resultRow["meaning"].astype(str) + "、" + resultRow["meaning2"].astype(str) + "、" + resultRow["meaning3"].astype(str)
                # print(f"mean:{mean}")
                
                # 同義語と意味からなるseriesを作成
                result = pd.DataFrame([[syn_in, mean, "red"]], columns=final_results.columns)
                # print("↓result")
                # display(result)
                
                # 最終結果に入れる
                final_results = pd.concat([final_results, result], ignore_index=True)
                
                if len(final_results["words"]) >= results_NUM:
                    break
        
        if self.syn_from_net:    
            # while len(self.final_results["words"]) <= results_NUM:
            for syn_out in self.syn_from_net:
                # print(len(final_results["words"]))
                search_word = SEARCH_ENGINE2 + syn_out
                url = requests.get(search_word) 
                try:
                    soup = BeautifulSoup(url.text, "html.parser")
                    mean = soup.find(class_="content-explanation ej").get_text().strip().split("、")[:3]
                    mean = "、".join(mean)
                    result = pd.DataFrame([[syn_out, mean, "no"]], columns=final_results.columns)
                    final_results = pd.concat([final_results, result], ignore_index=True)
                except:
                    errorMean = "単語の意味が見つかりません"
                    result = pd.DataFrame([[syn_out, errorMean, "no"]], columns=final_results.columns)
                    final_results = pd.concat([final_results, result], ignore_index=True)

                if len(final_results["words"]) >= results_NUM:
                    break
                
        return final_results