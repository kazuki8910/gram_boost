#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 無期限アクセストークンを取得する


# In[ ]:


# モジュール
import requests


# In[ ]:


####################
# 
# 必要事項入力
# 
####################

# print("アプリIDを入力")
app_id = '807274826872028'
# app_id = input()
print("")

# print("app secretを入力")
app_secret = 'd8572d689cfdaf4c8f0c6992f6010ac6'
# app_secret = input()
print("")

print("短期アクセストークンを入力")
access_token_short = input()
print("")


# In[ ]:


####################
# 
# 長期アクセストークン取得
# 
####################

# リクエストURL
url_first = "https://graph.facebook.com/v3.0/oauth/access_token"

# パラメータ
params_short = { 
    "grant_type": "fb_exchange_token",
    "client_id": app_id,
    "client_secret": app_secret,
    "fb_exchange_token": access_token_short
}
 
# リクエスト
res_short = requests.get(url_first, params=params_short).json()

# 長期アクセストークン取得
access_token_long = res_short["access_token"]


# In[ ]:


####################
# 
# ID取得
# 
####################

# リクエストURL
url_id = 'https://graph.facebook.com/v3.0/me'

# パラメータ
params_id = { "access_token": access_token_long }

# リクエスト
res_id = requests.get(url_id, params=params_id).json()

# ID取得
my_id = res_id["id"]


# In[ ]:


####################
# 
# 無期限アクセストークン取得
# 
####################

# リクエストURL
url_indefinite = f'https://graph.facebook.com/v3.0/{my_id}/accounts'

# パラメータ
params_indefinite = { "access_token": access_token_long}

# リクエスト
res_indefinite = requests.get(url_indefinite, params=params_indefinite).json()


# In[ ]:


# データ整形
tokens = []
for val in res_indefinite["data"]:
    access_token = val["access_token"]
    name = val["name"]
    token = {
        "name": name,
        "access_token": access_token
    }
    tokens.append(token)
    
# 出力
print("\n------result----------\n")
for val in tokens:
    print(val["name"])
    print(val["access_token"])
    print("")
print("------result----------\n\n")


# In[ ]:


print("Click Enter")
input()

