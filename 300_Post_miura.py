#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 自動投稿_２


# In[34]:


####################
# 
# モジュール
# 
####################

# 標準
import sys

from selenium.webdriver.common.alert import Alert

# 自作
sys.path.append('module')
import EasyScraping as es
import CreatorStudio as cs
import Instagram as ig


# In[35]:


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
sheets = gc.open_by_key(sheet_key)

# configシートを連想配列に格納
sheet_conf = sheets.worksheet(sheet_name_conf).get_all_values() # シートの値
conf_val = {}
for conf in sheet_conf:
    conf_val[conf[0]] = conf[1] 


# 投稿リストから投稿の情報を取得する
list_sheet = sheets.worksheet(sheet_name_list)
sheet_list = list_sheet.get_all_values() # シートの値
post_val = {}
for ind,post in enumerate(sheet_list[0]):
    post_val[post] = sheet_list[1][ind]
    
# 投稿のリストが10個以下だったらLINEに通知
if(len(sheet_list)<12):
    es.send_line(f'{conf_val["account_id"]}の投稿リストが10個を切りました。')
    
print(f'投稿するアカウント：{conf_val["account_id"]}')


# In[36]:


####################
# 
# 投稿画像/動画を取得
# 
####################

print("投稿する画像/動画を取得中")

# Chrome起動
driver = es.start_chrome(headless=False, session=False)


# In[46]:


# 投稿画面にアクセス
driver.get(post_val["url"])
es.wait()


# In[47]:


# 画像/動画を保存
ig.save_file(driver)


# In[48]:


print("投稿する画像/動画の取得完了")


# In[49]:


####################
# 
# クリエイタースタジオにログイン
# 
####################

print('投稿の準備中')


# In[50]:


# クリエイタースタジオ起動
cs.start_up_cs(driver)


# In[51]:


# 投稿を作成ボタンクリック
cs.click_create_post(driver)

# 「Instagramフィードボタン」をクリック
cs.click_ig_feed(driver)


# In[52]:


# 投稿するアカウントを選択
cs.choice_post_account(driver, conf_val["account_id"])


# In[53]:


# 投稿文入力
cs.input_post_text(driver, post_val["text"])


# In[54]:


# ファイルのアップロード
cs.click_add_contents(driver)


# In[55]:


# タグ付け
cs.add_tag(driver, post_val["tag"])


# In[56]:


# Facebookに投稿をクリック
cs.check_facebook_post(driver)


# In[57]:


# 公開する
cs.click_publish(driver)


# In[58]:


print('投稿完了')


# In[59]:


# ブラウザを閉じる
driver.quit()


# In[60]:


# 引用した投稿をリストから削除
cs.remove_post_list(list_sheet)


# In[61]:


print("リストから投稿削除")
print('Click Enter')
input()


# In[ ]:





# In[ ]:




