#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 自動いいねツール


# In[2]:


# モジュール
import sys
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.path.append("module")
import EasyScraping as es
import Instagram as ig


# In[3]:


# 対象アカウント
accounts = [
    "auto_bot_k1",# テストアカウント
    "camp__film", # キャンプフィルム
    "bijo_film",  # 美女フィルム
    "ayano_bbj",  # コスメ（あやの）
]


# In[4]:


####################
# 
# テストコード（後で消す）
# 
####################

account = accounts[0]


# In[5]:


####################
# 
# 設定値取得
# 
####################

account_info = es.get_account_info(account) # アカウント情報

account_pass = account_info["pass"] # パスワード

profile_url  = ig.url_ig + '/' + account # プロフィールURL

al_info = account_info["automatic_like"]   # 自動いいねに関する情報
release_min    = al_info["release_min"]    # これ以上のフォローでフォロー解除する
release_follow = al_info["release_follow"] # 一回に解除するフォロー数


# In[7]:


####################
# 
# インスタグラムにログイン
# 
####################

# ヘッドレス化
# options = Options()
# options.add_argument('--headless');

# クローム起動
# driver = webdriver.Chrome(es.driver_path, options=options)
driver = webdriver.Chrome(es.driver_path)

# インスタグラムにログイン
ig.login(driver, account, account_pass)


# In[19]:


####################
# 
# フォロー解除
# 
####################
ig.al_release_follow(driver, profile_url, release_min, release_follow)


# In[11]:


import importlib
importlib.reload(es)
importlib.reload(ig)


# In[ ]:




