#!/usr/bin/env python
# coding: utf-8

# In[1]:


# サービス化にする際の積み残し
# ・Seleniumグリッドの導入
# ・競合が弱くないかのチェック
# ・投稿のいいね数がリーチ数よりも少なかったときの対処
# ・フォロワー取得


# In[2]:


# 自動いいねツール


# In[3]:


# モジュール
import sys
import json
import time
import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.path.append("module")
import EasyScraping as es
import Instagram as ig


# In[4]:


# 対象アカウント
accounts = [
    "bijo_film",  # 美女フィルム
    # "ayano_bbj",  # コスメ（あやの）
    "camp__film", # キャンプフィルム
]


# In[5]:


# ブラウザ起動
drivers = {}
for account in accounts:
    ####################
    # 
    # 設定値取得
    # 
    ####################

    # アカウントの情報を取得
    account_info = es.get_account_info(account) # アカウント情報
    account_pass = account_info["pass"]         # パスワード
    profile_url  = ig.url_ig + '/' + account # プロフィールURL

    # Chrome起動
    driver = es.start_chrome(session=False)
    
    # インスタにログイン
    ig.login(driver, account, account_pass)
    
    # 連想配列に格納
    drivers[account] = {
        'driver': driver,     # ドライバ
        'info': account_info, # アカウント情報
        'profile_url': profile_url # プロフィールURL
    }


# In[6]:


for i in range(12):
    
    for key in drivers:
            
        print(f'{key}のいいね中')
        
        # Driver
        driver = drivers[key]["driver"]
        
        # アカウント情報を配列から取得
        account_info = drivers[key]["info"]
        profile_url  = drivers[key]["profile_url"]
        
        # いいねの上限に関する値
        al_info = account_info["automatic_like"]   # 自動いいねに関する情報
        release_min    = al_info["release_min"]    # これ以上のフォローでフォロー解除する
        release_follow = al_info["release_follow"] # 一回に解除するフォロー数
        set_reach      = al_info["reach"]          # リーチ数
        max_follow     = al_info["max_follow"]     # 1ループでフォローする上限

        # ライバルアカウント
        rival_account = random.choice(account_info['rivals'])

        # スプレッドの情報
        sheet_key = account_info["sheet"]["key"] # シートキー        
        
        
        ####################
        #
        # フォロー解除
        #
        ####################

        ig.al_release_follow(driver, profile_url, release_min, release_follow)
        
        
        
        ####################
        #
        # いいね先のリスト取得
        #
        ####################

        # 競合のアカウントに移動
        driver.get(rival_account)
        es.wait()
        
        # 1つ目の投稿クリック
        ig.click_first_post(driver)

        # いいねしたアカウントのリストを表示
        ig.show_favo_account_list(driver)

        # いいねするユーザーのリストを取得するループ
        user_urls = ig.get_favo_user_list(driver, set_reach)


        
        ####################
        #
        # 自動いいね・フォロー
        #
        ####################

        # いいねとフォローのカウント
        favo_count   = 0 # いいねした数
        favo_user    = 0 # いいねしたユーザー数
        follow_count = 0 # フォローした数

        # いいね・フォローするループ
        for user_url in user_urls:

            # ユーザーのプロフィールに遷移
            driver.get(user_url)
            es.wait()

            # 投稿数を取得
            post_num = ig.get_post_num(driver)

            # 鍵垢の判定
            is_lock = ig.is_lock(driver)

            # 投稿数が０か鍵垢のときはフォローする
            if(post_num == 0 or is_lock):
                # フォローする
                do_follow = ig.do_follow(driver, max_follow, follow_count)

                # フォロー数のカウント
                if(do_follow):
                    follow_count += 1

            # 1つ目の投稿をいいね
            if(post_num > 0 and not is_lock):
                # 1つ目の投稿をクリック
                ig.click_first_post(driver)

                # いいね！
                do_favo = ig.do_favo(driver)

                # いいねした数とユーザー数をカウント
                if(do_favo):
                    favo_user  += 1
                    favo_count += 1

            # # 2つ目の投稿をいいね
            # if(post_num > 1 and not is_lock):
            #     # 1つ前の投稿ボタンをクリック
            #     ig.click_right_post_arrow(driver)

            #     # いいね！
            #     do_favo = ig.do_favo(driver)

            #     # いいねした数とユーザー数をカウント
            #     if(do_favo):
            #         favo_count += 1

        # レポート用の配列に格納
        this_report = {
            "reach": int(set_reach),     # リーチ数
            "favo_user": int(favo_user), # いいねしたユーザー数
            "favo": int(favo_count),     # いいねした数
            "follow": int(follow_count)  # フォローした数
        }
        
        
        
        #########################
        #
        # スプシに記録
        #
        #########################

        ig.output_report(sheet_key, this_report)
        
    
    
    # 休憩
    print(f'休憩中：{i}')
    time.sleep(5400)


# In[ ]:





# In[ ]:





# In[ ]:




