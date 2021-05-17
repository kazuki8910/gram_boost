####################
# 
# モジュール
#
####################

# 既存
import json
import sys
import traceback
import time
import datetime
import random

# 拡張
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import chromedriver_binary

# LINE関連
from linebot import LineBotApi
from linebot.models import TextSendMessage

# Sheet API関連
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 自作
from settings import BASE_DIR



####################
# 
# 変数
#
####################

# モジュール名
module = "EasyScraping"

# LINE Message APIのアクセストークン
MASSAGE_API_TOKEN = 'kTSQzgP+QRrJpLNEkZEPtvXL8yzvlPxSHzh+ZeILehChZH7wBuGeArGvSstYW2Zwct/hQWd4otq41CWuNE2A3mHT/zzcxnKpEPY6B2hJ2PtoqSqIB4On4HxhB2r3fx3HE/QNc9i+3HYaabwCitlLZwdB04t89/1O/w1cDnyilFU='






####################
# 
# 関数(基本)
#  
####################

# LINEにメッセージを送信する関数
def send_line(message):
    line_bot_api = LineBotApi(MASSAGE_API_TOKEN)
    messages = TextSendMessage(text=message)
    line_bot_api.broadcast(messages=messages)


# エラーメッセージを出力する関数
def notice_error(module="", function="", message=""):
    # エラーメッセージを変数化
    top = '\n\n--------------------エラーメッセージ--------------------\n\n'
    btm = '\n\n------------------END:エラーメッセージ------------------\n\n'
    detail = f'{traceback.format_exc()}\n'
    message = f'{message}\n'
    func = f'エラーが起きた関数：{function}\n'
    module = f'エラーが起きたモジュール：{module}\n'
    time_now = f'{datetime.datetime.now().strftime("%m月%d日 %H時%M分%S秒")}\n'


    error_text = top + detail + message + func + module + time_now + btm

    # エラー文出力
    print(error_text)
    send_line(error_text)

    sys.exit(0)


# アカウントの情報を取得する関数
def get_account_info(account):
    try:
        info_path = f'{BASE_DIR}\\accounts\\instagram\\{account}.json'
        info_json = open(info_path, 'r', encoding="utf-8_sig")
        info = json.load(info_json)
    except:
        function = sys._getframe().f_code.co_name
        message = "アカウント情報の取得に失敗しました。"
        notice_error(module, function, message)
    return info


# FBの情報を取得
def get_fb_info():
    try:
        info_path = f'{BASE_DIR}\\accounts\\facebook\\kumagai_kazuki.json'
        info_json = open(info_path, 'r', encoding="utf-8_sig")
        info = json.load(info_json)
    except:
        function = sys._getframe().f_code.co_name
        message = "アカウント情報の取得に失敗しました。"
        notice_error(module, function, message)
    return info


# シートの命名規則を取得
def get_sheet_name_convention():
    try:
        file_path = f'{BASE_DIR}\\config\\other\\sheet.json'
        json_file = open(file_path, 'r', encoding="utf-8_sig")
        value = json.load(json_file)
        return value
    except:
        function = sys._getframe().f_code.co_name
        message = "スプレッドシートの命名規則の取得に失敗しました。"
        notice_error(module, function, message)


# 動作を一時停止する関数
def wait(start=3.0, span=1.0):
    time.sleep(random.uniform(start, start+span))






####################
# 
# 関数(情報取得系)
#  
####################

# Xpathから要素を取得
def get_elm_by_xpath(driver, xpath):
    try:
        elm = driver.find_element_by_xpath(xpath)
        return elm
    except:
        function = sys._getframe().f_code.co_name
        message = f'Xpathが存在しません。\n要素取得に失敗しました。\n指定した要素{xpath}'
        notice_error(module, function, message)

# Xpathから存在する要素を全取得
def get_elms_by_xpath(driver, xpath):
    # 該当する要素を全取得
    elms = driver.find_elements_by_xpath(xpath)
    if(len(elms) == 0):
        function = sys._getframe().f_code.co_name
        message = f'指定したXpathが存在しません。\n要素取得に失敗しました。\n指定した要素{xpath}'
        notice_error(module, function, message)
    else:
        return elms

# 取り得るXpathから存在する要素を取得
def get_elm_by_xpaths(driver, xpaths):
    for xpath in xpaths:
        try:
            elm = driver.find_element_by_xpath(xpath)
            break
        except:
            continue
    else:
        function = sys._getframe().f_code.co_name
        message = f'Xpathが存在しません。\n要素取得に失敗しました。\n指定した要素{xpaths}'
        notice_error(module, function, message)
    return elm

# 取り得るXpathから存在する全取得要素を取得
def get_elms_by_xpaths(driver, xpaths):
    try:
        for xpath in xpaths:
            elms = driver.find_elements_by_xpath(xpath)
            if(len(elms) > 0):
                break
        else:
            function = sys._getframe().f_code.co_name
            message = f'指定した要素の取得に失敗しました。\n指定した要素{xpaths}'
            notice_error(module, function, message)
        return elms
    except:
        function = sys._getframe().f_code.co_name
        message = f'Xpathが存在しません。\n要素取得に失敗しました。\n指定した要素{xpaths}'
        notice_error(module, function, message)



# 取り得るタグから存在する要素を取得
def get_elm_by_tags(driver, tags):
    for tag in tags:
        try:
            elm = driver.find_element_by_tag_name(tag)
            break
        except:
            continue
    else:
        function = sys._getframe().f_code.co_name
        message = f'タグが存在しません。\n要素取得に失敗しました。\n指定した要素{tags}'
        notice_error(module, function, message)
    return elm



####################
# 
# 関数(操作系)
#  
####################

# Chrome起動
def start_chrome(headless=False, session=True, secret=False):
    try:
        # オプション指定
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox') # セキュリティブロックオフ
        options.add_argument('--disable-gpu') # 
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) # 自動操作の表示オフ
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-dev-shm-usage') # shm無効

        # ヘッドレスモード
        if(headless):
            options.add_argument('--headless') # ヘッドレスモード)

        # セッション
        if(session):
            options.add_argument(f'user-data-dir={BASE_DIR}\\session') # セッション偽装

        # シークレットモード
        if(secret):
            options.add_argument('--incognito')

        # Chrome起動
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(1280, 720)
        time.sleep(1)

        return driver

    except:
        function = sys._getframe().f_code.co_name
        message = f'Chromeの起動に失敗しました。'
        notice_error(module, function, message)


# Xpathから要素をクリック
def click_by_xpath(driver, xpath, start=3.0, span=1.0):
    elm = driver.find_element_by_xpath(xpath)
    elm.click()
    wait(start, span)


# 要素をスクロール
def scroll(driver, css_selector, amount):
    elm = driver.find_elements_by_css_selector(css_selector)
    if(len(elm) != 0):
        driver.execute_script( \
            f'const scroll = document.querySelector("{css_selector}");' \
            f'scroll.scrollBy(0,{amount});' \
        )
    else:
        function = sys._getframe().f_code.co_name
        message = f'スクロールする要素がありません。\n指定したCSSのセレクター:"{css_selector}"'
        notice_error(module, function, message)


# 要素にホバー
def hover(driver, elm):
    try:
        actions = ActionChains(driver)
        actions.move_to_element(elm).perform()
    except:
        function = sys._getframe().f_code.co_name
        message = f'要素のホバーに失敗しました:"{elm}"'
        notice_error(module, function, message)






####################
# 
# 関数(Sheet API)
#  
####################

# Sheet APIの認証
def sheet_auth():
    try:
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(f'{BASE_DIR}\\config\\api\\sheet_api.json', scope)
        gc = gspread.authorize(credentials)
        return gc
    except:
        function = sys._getframe().f_code.co_name
        message = "Sheet APIの認証に失敗しました。"
        notice_error(module, function, message)



