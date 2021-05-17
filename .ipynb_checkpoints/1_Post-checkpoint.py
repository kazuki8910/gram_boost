#!/usr/bin/env python
# coding: utf-8

# In[10]:


####################
#
# 自動投稿
#
####################

####################
# 
# モジュール
# 
####################

# 標準
import sys

# 自作
sys.path.append('module')
import EasyScraping as es
import CreatorStudio as cs
import Instagram as ig


# In[11]:


####################
# 
# 変数
# 
####################

# アカウントID
account_ids = [
    'camp__film',
    'bijo_film'
]


# In[12]:


####################
# 
# 自動投稿のループ
# 
####################


# In[13]:


for account_id in account_ids:
    
    print(f'\n{account_id}')
    
    ###################
    #
    # アカウント情報取得
    #
    ###################

    account_info = es.get_account_info(account_id)
    
    

    ####################
    # 
    # シートから投稿のストックを取得
    # 
    ####################
    
    print('シートから引用する投稿を取得中')

    # シートの命名規則を取得
    sheet_name_conv = es.get_sheet_name_convention()

    # シートキー取得
    try:
        sheet_key = account_info["sheet"]["key"]
    except:
        function = sys._getframe().f_code.co_name
        message = "JSONファイルのシートキーの取得に失敗しました。"
        es.notice_error(function, message)

    # シートの認証
    gc = es.sheet_auth()

    # シートから引用する投稿のURLを取得
    try:
        # シートを取得
        sheet_stock = gc.open_by_key(sheet_key).worksheet(sheet_name_conv['post_stock']['name'])

        # URLが何列目に格納されているのか取得
        sheet_stock_values = sheet_stock.get_all_values()
        sheet_stock_head     = sheet_stock_values[0]
        stock_url_col = int(sheet_stock_head.index("投稿のURL"))

        # 投稿のURLを取得
        stock_url = sheet_stock_values[1][stock_url_col]

    except:
        function = sys._getframe().f_code.co_name
        message = "引用投稿（ストック）の取得に失敗しました。"
        es.notice_error(function, message)
        
    print('取得完了')
    
    

    ####################
    # 
    # 引用する投稿の情報を取得
    # 
    ####################
    
    print('引用する投稿の情報を取得中')

    # Chrome起動
    driver = es.start_chrome(headless=False)

    # 投稿のURLに遷移
    try:
        driver.get(stock_url)
        es.wait()
    except:
        function = sys._getframe().f_code.co_name
        message = '引用した投稿への移動に失敗しました。'
        es.notice_error(function, message)

    # 画像・動画ファイルをローカルに保存
    ig.save_file(driver)

    # 投稿文取得
    post_text = ig.get_post_text(driver)

    # プロフィール画面に遷移
    ig.move_to_profile_from_post(driver)

    # ユーザーID取得
    user_id = ig.get_user_id(driver)

    # ユーザー名
    user_name = ig.get_user_name(driver)
    
    print('取得完了')
    
    

    ####################
    #
    # クリエイタースタジオから投稿
    # 
    ####################
    
    print('クリエイタースタジオから投稿中')

    # クリエイタースタジオ起動
    cs.start_up_cs(driver)

    # 投稿を作成ボタンクリック
    cs.click_create_post(driver)

    # 「Instagramフィードボタン」をクリック
    cs.click_ig_feed(driver)

    # 投稿するアカウントを選択
    cs.choice_post_account(driver, account_id)

    # 投稿文生成
    created_post_text = cs.create_post_text(account_info['template'], user_name, user_id, post_text)

    # 投稿文入力
    cs.input_post_text(driver, created_post_text)

    # ファイルのアップロード
    cs.click_add_contents(driver)

    # タグ付け
    cs.add_tag(driver, user_id)

    # Facebookに投稿をクリック
    cs.check_facebook_post(driver)

    # 公開する
    cs.click_publish(driver)
    
    print('投稿完了')
    
    # ブラウザを閉じる
    driver.quit()
    
    print('引用した投稿をリストから削除中')

    # 引用した投稿をリストから削除
    cs.remove_post_from_stock(account_id)
    
    print('削除完了')
    es.send_line(f'投稿完了{account_id}')


# In[14]:


print('Click Enter')
input()

