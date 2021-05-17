#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 投稿のリストアップ


# In[ ]:


####################
# 
# モジュール
# 
####################

# 標準
import sys
import random

# 自作
sys.path.append('module')
import EasyScraping as es
import CreatorStudio as cs
import Instagram as ig


# In[ ]:


####################
# 
# シートから情報を取得
# 
####################

print("シートの情報を取得中")

# シートの認証
gc = es.sheet_auth()

# シートの設定値
sheet_key = "1kk42fCyWIAf7taxEp0zwI-P_5DruB0MYJYELx9kB3TE" # シートキー
sheet_name_list = "post_list" # post_listシート名
sheet_name_conf = "config" # configシート名
sheet_name_rival = "rivals" # rivalsシート名
sheets = gc.open_by_key(sheet_key)


# In[ ]:


# 競合のアカウントリストからランダムに3つ抽出
rival_sheet = sheets.worksheet(sheet_name_rival)
sheet_rival = rival_sheet.get_all_values() # シートの値
rivals = sheet_rival[1:]
rivals = random.sample(rivals,3)


# In[ ]:


# configシートの情報を取得
conf_sheet = sheets.worksheet(sheet_name_conf)
sheet_conf = conf_sheet.get_all_values() # シートの値
conf_val = {}
for conf in sheet_conf:
    conf_val[conf[0]] = conf[1] 


# In[ ]:


# post_listシートの情報を取得
list_sheet = sheets.worksheet(sheet_name_list)
sheet_list = list_sheet.get_all_values() # シートの値


# In[ ]:


# Chrome起動
driver = es.start_chrome(session=False, secret=True)


# In[ ]:


# インスタにログイン
bot_account = es.get_account_info("auto_bot_k1")
ig.login(driver, bot_account["name"], bot_account["pass"])


# In[ ]:


# ループ
for rival in rivals:

    # アカウントのプロフィール画面に遷移
    driver.get(rival[0])
    es.wait()

    # 下のログインを促すバナーを削除
    ig.delete_login_banner(driver)
    
    # 投稿一覧の要素
    xpath = "/html/body/div[1]/section/main/div/div/article/div[1]/div/div/div"
    posts = es.get_elms_by_xpath(driver, xpath)

    # 投稿のインデックス番号といいね数を取得
    post_info = ig.get_favo_from_posts(driver, posts)
    post_info = sorted(post_info, reverse=True, key=lambda x: x[1])  #[1]に注目してソート
    post_info = post_info[0:5] # エンゲージメントの高い5つに絞る

    # 投稿のURLを格納
    for val in post_info:
        # インデックスから投稿の要素を取得
        ind = val[0]
        post = posts[ind]

        # 投稿のURLを取得
        url = ig.get_post_url_from_post_list(post)
        val.append(url)
        
        
    # スプレッドシートに出力
    # post_listシートの情報を取得
    sheets = gc.open_by_key(sheet_key)
    list_sheet = sheets.worksheet(sheet_name_list)
    sheet_list = list_sheet.get_all_values() # シートの値

    len_list = len(sheet_list)
    len_col  = len(sheet_list[0])
    for ind,val in enumerate(post_info):
        # 書き換える行を選択
        row = list_sheet.range(len_list+ind+1, 1, len_list+ind+1, 3)

        # セル書き換え
        row[0].value = val[2]
        row[1].value = conf_val["post_text"]
        row[2].value = conf_val["post_tag"]
        list_sheet.update_cells(row) 


# In[ ]:


driver.quit()


# In[ ]:





# In[ ]:





# In[ ]:




