####################
# 
# モジュール
#  
####################

# 標準
import sys
import re
import os
import glob
import codecs
import datetime

# 拡張
import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

# 自作
import EasyScraping as es




####################
# 
# 変数
#  
####################

# モジュール名
module = "CreatorStudio"

# クリエイタースタジオのURL
url_cs = 'https://business.facebook.com/creatorstudio'

# FBのログイン情報
fb_id   = es.get_fb_info()["id"]   # ID
fb_pass = es.get_fb_info()["pass"] # パスワード






####################
# 
# 関数(クリエイタースタジオ起動)
#  
####################

# クリエイタースタジオにアクセス
def access_to_cs(driver):
    try:
        driver.get(url_cs)
        es.wait()
    except:
        function = sys._getframe().f_code.co_name
        message = 'クリエイタースタジオへのアクセスに失敗しました。'
        es.notice_error(module, function, message)

# ログインフォームに遷移
def move_to_login_form(driver):
    try:
        xpath = '/html/body/div/div[1]/div[2]/div/div[2]/div/div/div/div[2]/div'
        es.click_by_xpath(driver, xpath)
    except:
        function = sys._getframe().f_code.co_name
        message = 'ログインフォームへの遷移に失敗しました。'
        es.notice_error(module, function, message)

# メールアドレスの入力
def input_mail(driver):
    try:
        # インプットタグのXpath
        xpath   = '//*[@id="email"]'

        # インプットタグの要素を取得
        elm   = driver.find_element_by_xpath(xpath)

        # # インプットタグに情報を入力
        elm.clear()
        elm.send_keys(fb_id)
        es.wait(1)
    except:
        function = sys._getframe().f_code.co_name
        message = 'メールアドレスの入力に失敗しました。'
        es.notice_error(module, function, message)

# パスワードの入力
def input_pass(driver):
    try:
        # インプットタグのXpath
        xpath   = '//*[@id="pass"]'

        # インプットタグの要素を取得
        elm   = driver.find_element_by_xpath(xpath)

        # # インプットタグに情報を入力
        elm.clear()
        elm.send_keys(fb_pass)
        es.wait(1)
    except:
        function = sys._getframe().f_code.co_name
        message = 'パスワードの入力に失敗しました。'
        es.notice_error(module, function, message)
    
# ログインボタンクリック
def click_login_btn(driver):
    try:
        xpath = '//*[@id="loginbutton"]'
        es.click_by_xpath(driver, xpath)
    except:
        function = sys._getframe().f_code.co_name
        message = 'ログインボタンのクリックに失敗しました。'
        es.notice_error(module, function, message)

# Instagramモードに移行
def change_ig_mode(driver):

    try:
        mode_insta_xpath = '//*[@id="media_manager_chrome_bar_instagram_icon"]'
        es.click_by_xpath(driver, mode_insta_xpath)
    except:
        function = sys._getframe().f_code.co_name
        message = 'Instagramモードへの移行に失敗しました。'
        es.notice_error(module, function, message)

# ログイン
def login(driver, fb_id=fb_id, fb_pass=fb_pass):
    try:
        # ログインフォームに遷移
        move_to_login_form(driver)

        # メールアドレスとパスワードを入力
        input_mail(driver)
        input_pass(driver)

        # ログインボタンクリック
        click_login_btn(driver)

        # インスタグラムモードに移行
        mode_insta_xpath = '//*[@id="media_manager_chrome_bar_instagram_icon"]'
        es.click_by_xpath(driver, mode_insta_xpath)
    except:
        function = sys._getframe().f_code.co_name
        message = 'ログインに失敗しました。'
        es.notice_error(module, function, message)

# 起動
def start_up_cs(driver):
    try:
        # クリエイタースタジオにアクセス
        access_to_cs(driver)

        # タイトル取得(タイトルタグの中身でログイン済みかどうかを判別する)
        title = driver.title

        # 未ログインなら、ログインする
        if(title == "Facebookクリエイタースタジオ"):
            login(driver)

        # ログイン済の場合、Instagramモードに切り替え
        elif(re.fullmatch('\(?[0-9]*\)?\s*クリエイタースタジオ', title)):
            change_ig_mode(driver)

        # それ以外
        else:
            function = sys._getframe().f_code.co_name
            message = 'クリエイタースタジオの起動に失敗しました。\ntitleタグが予期せぬ値です。'
            es.notice_error(module, function, message)

    except:
        function = sys._getframe().f_code.co_name
        message = 'クリエイタースタジオの起動に失敗しました。'
        es.notice_error(module, function, message)





####################
# 
# 関数(自動投稿)
#  
####################

# 「投稿を作成」ボタンをクリック
def click_create_post(driver):
    try:
        xpath = '/html/body/div[1]/div[1]/div/div[2]/div/div/div[2]/div[1]/div[1]/div[1]/div/div/div'
        es.click_by_xpath(driver, xpath)
    except:
        function = sys._getframe().f_code.co_name
        message = '「投稿を作成」ボタンのクリックに失敗しました。'
        es.notice_error(module, function, message)


# 「Instagramフィード」ボタンをクリック
def click_ig_feed(driver):
    try:
        xpaths = [
            '/html/body/div[3]/div[1]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div/div/div',
            '/html/body/div[4]/div[1]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div/div/div',
            '/html/body/div[5]/div[1]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div/div/div',
        ]
        elm = es.get_elm_by_xpaths(driver, xpaths)
        elm.click()
        es.wait(5)
    except:
        function = sys._getframe().f_code.co_name
        message = '「Instagramフィード」ボタンのクリックに失敗しました。'
        es.notice_error(module, function, message)


# 投稿するアカウントを選択
def choice_post_account(driver, account_id):
    try:
        # アカウントのリストを取得
        xpath = '/html/body/div/div/div/div/div[3]/div'
        accounts = es.get_elms_by_xpath(driver, xpath)
        # 該当するアカウントをクリック
        account = list(filter(lambda val: val.text == account_id , accounts))[0]
        account.click()
        es.wait()
    except:
        function = sys._getframe().f_code.co_name
        message = '投稿するアカウント選択に失敗しました。'
        es.notice_error(module, function, message)


# 投稿文生成
def create_post_text(temp, user_name, user_id, post_text):
    try:
        # 投稿文生成
        created_post_text = temp[0] + user_name + temp[1] + user_id + temp[2] + post_text + temp[3]
        # 絵文字除去
        non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), "")
        created_post_text = created_post_text.translate(non_bmp_map)
        # <br>タグを改行に変換
        created_post_text = created_post_text.replace('<br>', '\n')

        return created_post_text
    
    except:
        function = sys._getframe().f_code.co_name
        message = '投稿文の生成に失敗しました。'
        es.notice_error(module, function, message)


# 投稿文入力
def input_post_text(driver, post_text):
    try:
        xpath = '/html/body/div/div/div/div/div[2]/div[1]/div/div[2]/div[1]/div/div/div[2]/div/div/div/div/span'
        elm = es.get_elms_by_xpath(driver, xpath)[0]
        elm.send_keys(post_text)
        es.wait(1)
    except:
        function = sys._getframe().f_code.co_name
        message = '投稿文の入力に失敗しました。'
        es.notice_error(module, function, message)


# 動画・画像ファイルをアップロード
def click_add_contents(driver):
    try:
        # 保存した画像・動画のリスト
        files = glob.glob(f'{es.BASE_DIR}\\temporary\\*')
        
        # ファイルをアップロード
        for file in files:
            # 「コンテンツを追加」ボタンをクリック
            # 取り得るXpath「/html/body/div[*]/div/div/div/div[2]/div[1]/div/div[*]/div/div/div/span」
            xpath = '/html/body/div/div/div/div/div[2]/div[1]/div/div/div/div/div/span'
            elm = es.get_elms_by_xpath(driver, xpath)[0]
            elm.click()
            es.wait(1)
            
            # アップロードするinputタグ取得
            # 取り得るXpath「/html/body/div[*]/div/div/div/div/div/a/div[2]/input」
            xpath = '/html/body/div/div/div/div/div/div/a/div[2]/input'
            elm = es.get_elms_by_xpath(driver, xpath)[0]
            
            
            # ファイルをアップロード
            elm.send_keys(file)
            es.wait(5)

            # ローカルのファイルを削除
            os.remove(file)
            es.wait(1)


    except:
        function = sys._getframe().f_code.co_name
        message = '動画・画像のアップロードにファイルに失敗しました'
        es.notice_error(module, function, message)


# タグ付け
def add_tag(driver, user_id):
    try:
        # 一枚目の画像をクリック
        xpath = '//*[@id="creator_studio_sliding_tray_root"]/div/div/div[2]/div[1]/div/div[5]/div/div/div/div/div[2]/div/div[2]/div/div[1]/div'
        elm = es.get_elms_by_xpath(driver, xpath)[0]
        elm.click()
        es.wait()

        # タグ付けの部分をクリック
        xpaths = [
            '/html/body/div[5]/div/div/div/div[2]/div/div[3]/div[2]/div/div/div[1]/div/div/div/span', # 動画の場合
            '//*[@id="mediaManagerInstagramComposerMediaTagging"]/div' # 画像の場合
        ]
        elm = es.get_elm_by_xpaths(driver, xpaths)
        elm.click()
        es.wait(1)

        # 検索欄にIDを入力
        xpaths = [
            '/html/body/div[5]/div/div/div/div[2]/div/div[3]/div[2]/div/div/div[1]/div/div/span/label/input', # 動画の場合
            '//*[@id="mediaManagerInstagramComposerMediaTaggingWrapper"]/div[2]/div/span/label/input' # 画像の場合
        ]
        elm = es.get_elm_by_xpaths(driver, xpaths)
        elm.send_keys(user_id)
        es.wait(1)

        # 候補から指定のアカウントを選択
        xpath = '/html/body/div/div/div/div/div/ul/li'
        elms = es.get_elms_by_xpath(driver, xpath)
        for elm in elms:
            xpaths = [
                'div/div/div/span[1]', # 動画の場合
                'div/div[2]/div/div' # 画像の場合
            ]
            this_id = es.get_elm_by_xpaths(elm, xpaths).text
            if(this_id == user_id):
                elm.click()
                es.wait(1)
                break

        # 保存するボタンを押す
        xpath = '/html/body/div/div/div/div/div[3]/div/div[2]/div'
        elm = es.get_elms_by_xpath(driver, xpath)[0]
        elm.click()
        es.wait(1)

    except:
        function = sys._getframe().f_code.co_name
        message = 'タグ付けに失敗しました。'
        es.notice_error(module, function, message)


# Facebookに投稿するをクリック
def check_facebook_post(driver):
    try:
        # Facebookに投稿をクリック
        xpath = '/html/body/div/div/div/div/div[2]/div[1]/div/div[6]/span[2]/div/div/button'
        elm = es.get_elms_by_xpath(driver, xpath)[0]
        elm.click()
        es.wait(1)
    except:
        function = sys._getframe().f_code.co_name
        message = 'Facebookに投稿するをチェックるすのに失敗しました。'
        es.notice_error(module, function, message)


# 公開する
def click_publish(driver):
    try:
        xpath = '/html/body/div/div/div/div/div[3]/div[2]/button'
        elm = es.get_elms_by_xpath(driver, xpath)[0]
        elm.click()
        es.wait(10)
    except:
        function = sys._getframe().f_code.co_name
        message = '投稿を公開するボタンのクリックに失敗しました。'
        es.notice_error(module, function, message)


# 引用した投稿をリストから削除
def remove_post_from_stock(account_id):
    try:
        # シートから情報取得
        url = es.get_account_info(account_id)["sheet"]["gas"]
        sheet_name = es.get_sheet_name_convention()["post_stock"]["name"]

        # パラメータ
        param = { 
            "func": "remove_row",
            "sheet_name": sheet_name,
            "position": 2,
            "amount": 1
        }
        
        # GASにGETリクエスト
        requests.get(url, params=param)

    except:
        function = sys._getframe().f_code.co_name
        message = '引用した投稿をストックから削除するのに失敗しました。'
        es.notice_error(module, function, message)

# 引用した投稿をリストから削除(NEW)
def remove_post_list(sheet):
    try:
        sheet.delete_row(2)
    except:
        function = sys._getframe().f_code.co_name
        message = '引用した投稿をストックから削除するのに失敗しました。'
        es.notice_error(module, function, message)
    





####################
# 
# 関数(インサイト取得)
#  
####################

####################
# 
#アカウント選択
#  
####################

# アカウント選択ボタンをクリック
def click_choice_account(driver):
    try:
        elm_id = 'tabHeader'
        elm = driver.find_element_by_id(elm_id)
        elm.click()
        es.wait()

    except:
        function = sys._getframe().f_code.co_name
        message = 'アカウント選択ボタンのクリックに失敗しました。'
        es.notice_error(module, function, message)

# 指定したアカウント以外のチェックを外す
def remove_check_by_accounts(driver, account_id):
    try:
        # アカウントのリストを取得
        xpath = '/html/body/div[1]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div[3]/div[1]/div/div/div/div/div[3]/div[1]'
        elms = es.get_elms_by_xpath(driver, xpath)

        # 指定したアカウント以外のリスト
        not_targets = list(filter(lambda x: x.text!=account_id, elms))

        # 指定してないアカウントをクリックしてチェックを外す
        for val in not_targets:
            val.click()
            es.wait(0.5)
        
    except:
        function = sys._getframe().f_code.co_name
        message = '指定したアカウント以外のチェックを外すのに失敗しました。'
        es.notice_error(module, function, message)

# View ボタンをクリック
def click_view_btn(driver):
    try:
        xpath = '/html/body/div[1]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div[4]/div[2]/div'
        elm = es.get_elm_by_xpath(driver, xpath)
        elm.click()
        es.wait()
    except:
        function = sys._getframe().f_code.co_name
        message = 'View ボタンをクリックに失敗しました。'
        es.notice_error(module, function, message)

# アカウント選択
def choice_account(driver, account_id):
    try:
        # アカウント選択ボタンをクリック
        click_choice_account(driver)

        # 指定したアカウント以外のチェックを外す
        remove_check_by_accounts(driver, account_id)

        # View ボタンをクリック
        click_view_btn(driver)
    
    except:
        function = sys._getframe().f_code.co_name
        message = 'アカウント選択に失敗しました。'
        es.notice_error(module, function, message)


####################
#
# データ取得
#
####################

# 投稿のインサイト画面に遷移
def move_insight(driver, ind):
    try:
        # 1つ目の投稿の場合
        if(ind == 0):
            xpath = '/html/body/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div/div/div/span/i'
        # 2つ目の投稿の場合
        else:
            xpath = '/html/body/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div/div[2]/div/div[8]/div/div/div/span/i'
        
        elm = es.get_elm_by_xpath(driver, xpath)
        elm.click()
        es.wait()
    except:
        function = sys._getframe().f_code.co_name
        message = "投稿のインサイト画面への遷移に失敗しました。"
        es.notice_error(module, function, message)

# 投稿のURL取得
def get_post_url(driver):
    try:
        # 投稿に遷移
        xpath = '/html/body/div[4]/div/div/div/div[3]/div[1]/div'
        elm = es.get_elm_by_xpath(driver, xpath)
        elm.click()
        es.wait(1)
        driver.switch_to.window(driver.window_handles[1])
        es.wait(1)

        # URL取得
        url = driver.current_url
        
        # 元のウィンドウに戻る
        driver.close()
        es.wait(1)
        driver.switch_to.window(driver.window_handles[0])

        return url

    except:
        function = sys._getframe().f_code.co_name
        message = "投稿のURL取得に失敗しました。"
        es.notice_error(module, function, message)

# インプ取得
def get_post_imp(driver):
    try:
        xpath = '/html/body/div[4]/div/div/div/div[2]/div[2]/div[4]/div[5]/div[1]/div[2]/strong'
        elm = es.get_elm_by_xpath(driver, xpath)
        imp = elm.text
        return imp
    except:
        function = sys._getframe().f_code.co_name
        message = "インプの取得に失敗しました。"
        es.notice_error(module, function, message)

# リーチ取得
def get_post_reach(driver):
    try:
        xpath = '/html/body/div[4]/div/div/div/div[2]/div[2]/div[4]/div[4]/div/div[2]/strong'
        elm = es.get_elm_by_xpath(driver, xpath)
        val = elm.text
        return val
    except:
        function = sys._getframe().f_code.co_name
        message = "リーチの取得に失敗しました"
        es.notice_error(module, function, message)

# フォロー外リーチ取得
def get_post_unfollow_reach(driver):
    try:
        xpath = '/html/body/div[4]/div/div/div/div[2]/div[2]/div[4]/div[2]/div/span[3]'
        elm = es.get_elm_by_xpath(driver, xpath)
        val = re.sub(r'\D', '', elm.text) + '%'
        return val
    except:
        function = sys._getframe().f_code.co_name
        message = "フォロー外リーチの取得に失敗しました"
        es.notice_error(module, function, message)

# プロフアクセス取得
def get_post_profile(driver):
    try:
        xpath = '/html/body/div[4]/div/div/div/div[2]/div[2]/div[3]/div[3]/div/div[2]/strong'
        elm = es.get_elm_by_xpath(driver, xpath)
        val = elm.text
        return val
    except:
        function = sys._getframe().f_code.co_name
        message = "プロフアクセスの取得に失敗しました"
        es.notice_error(module, function, message)

# フォロワー増加取得
def get_post_follow(driver):
    try:
        xpath = '/html/body/div[4]/div/div/div/div[2]/div[2]/div[4]/div[3]/div/div[2]/strong'
        elm = es.get_elm_by_xpath(driver, xpath)
        val = elm.text
        return val
    except:
        function = sys._getframe().f_code.co_name
        message = "フォロワー増加の取得に失敗しました"
        es.notice_error(module, function, message)

# いいね数取得
def get_post_favo(driver):
    try:
        xpath = '/html/body/div[4]/div/div/div/div[2]/div[2]/div[2]/div[2]/div/div[1]/div/strong'
        elm = es.get_elm_by_xpath(driver, xpath)
        val = elm.text
        return val
    except:
        function = sys._getframe().f_code.co_name
        message = "いいね数の取得に失敗しました"
        es.notice_error(module, function, message)

# コメント数取得
def get_post_comment(driver):
    try:
        xpath = '/html/body/div[4]/div/div/div/div[2]/div[2]/div[2]/div[2]/div/div[2]/div/div/strong'
        elm = es.get_elm_by_xpath(driver, xpath)
        val = elm.text
        return val
    except:
        function = sys._getframe().f_code.co_name
        message = "コメント数の取得に失敗しました"
        es.notice_error(module, function, message)

# 保存数取得
def get_post_save(driver):
    try:
        xpath = '/html/body/div[4]/div/div/div/div[2]/div[2]/div[2]/div[2]/div/div[3]/div/div/strong'
        elm = es.get_elm_by_xpath(driver, xpath)
        val = elm.text
        return val
    except:
        function = sys._getframe().f_code.co_name
        message = "保存数の取得に失敗しました"
        es.notice_error(module, function, message)

# 完了ボタンクリック
def click_done_btn(driver):
    try:
        xpath = '/html/body/div[4]/div/div/div/div[3]/div[2]/div'
        elm = es.get_elm_by_xpath(driver, xpath)
        elm.click()
        es.wait()
    except:
        function = sys._getframe().f_code.co_name
        message = "完了ボタンのクリックに失敗しました。"
        es.notice_error(module, function, message)

# データ取得
def get_insight(driver, ind):
    # 投稿のインサイト画面に遷移
    move_insight(driver, ind)

    # 格納用データ
    val = {}

    val["url"]            = get_post_url(driver)            # 投稿のURL取得
    val["imp"]            = get_post_imp(driver)            # インプ取得
    val["reach"]          = get_post_reach(driver)          # リーチ取得
    val["unfollow_reach"] = get_post_unfollow_reach(driver) # フォロー外リーチ
    val["profile"]        = get_post_profile(driver)        # プロフアクセス
    val["follow"]         = get_post_follow(driver)         # フォロワー増加
    val["favo"]           = get_post_favo(driver)           # いいね数
    val["comment"]        = get_post_comment(driver)        # コメント数
    val["save"]           = get_post_save(driver)           # 保存数

    # 完了ボタンクリック
    click_done_btn(driver)

    return val


####################
#
# 投稿日時、ストーリー投稿かどうかの判別
#
####################

# 一つ分スクロール
def scroll_content(driver):
    try:
        # スクロール量の取得
        amount_xpath = '/html/body/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div/div[2]/div/div[1]'
        amount_elm = es.get_elm_by_xpath(driver, amount_xpath)
        amount = amount_elm.size["height"]

        # CSSセレクター指定
        css_selector = '#mediaManagerContentTable > div > div > div > div.ReactVirtualized__Grid._1zmk'

        # 一つ分スクロール
        es.scroll(driver, css_selector, amount)
        es.wait(1)

    except:
        function = sys._getframe().f_code.co_name
        message = "一つ分スクロール"
        es.notice_error(module, function, message)

# 投稿がストーリーかどうかの判別(ストーリー以外でTrue)
def is_feed(driver, ind):
    try:
        # 1つ目の投稿の場合
        if(ind == 0):
            xpath = '/html/body/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div/div/div/span/i'
        # 2つ目の投稿の場合
        else:
            xpath = '/html/body/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div/div[2]/div/div[8]/div/div/div/span/i'
        
        elm = es.get_elm_by_xpath(driver, xpath)
        is_feed = not 'sx_10e267' in elm.get_attribute('class')

        return is_feed

    except:
        function = sys._getframe().f_code.co_name
        message = "ストーリー投稿かどうかの判別に失敗しました。"
        es.notice_error(module, function, message)

# 投稿日取得
def get_post_date(driver, ind):
    try:
        # Xpath指定
        if(ind == 0):
            xpath = '/html/body/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div/div[2]/div/div[5]/div/div/div/div/div[1]/div/div[1]'
        else:
            xpath = '/html/body/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div/div[2]/div/div[11]/div/div/div/div/div[1]/div/div[1]'

        # 値取得
        elm_date = es.get_elm_by_xpath(driver, xpath)
        post_date = elm_date.text

        # 今日の日付
        today = datetime.datetime.today()

        # 日付型に変換
        if(post_date == '今日'):
            post_date = today
        elif(post_date == '昨日'):
            post_date = today - datetime.timedelta(days=1)
        else:
            post_date = datetime.datetime.strptime(post_date, '%Y/%m/%d')

        return post_date
    
    except:
        function = sys._getframe().f_code.co_name
        message = "投稿日の取得に失敗しました。"
        es.notice_error(module, function, message)

# 投稿時間取得
def get_post_time(driver, ind):
    try:
        # Xpath指定
        if(ind == 0):
            xpath = '/html/body/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div/div[2]/div/div[5]/div/div/div/div/div[1]/div/div[2]'
        else:
            xpath = '/html/body/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div/div[2]/div/div[11]/div/div/div/div/div[1]/div/div[2]'

        elm_time = es.get_elm_by_xpath(driver, xpath)
        post_time = elm_time.text

        return post_time

    except:
        function = sys._getframe().f_code.co_name
        message = "投稿時間の取得に失敗しました。"
        es.notice_error(module, function, message)

# 投稿日が取得範囲内か判別
def within_range(post_date, DAYS_AGO):
    try:
        today = datetime.datetime.today()
        val = (today - post_date).days <= DAYS_AGO
        return val
    except:
        function = sys._getframe().f_code.co_name
        message = "投稿日が範囲内かの判別に失敗しました。"
        es.notice_error(module, function, message)



