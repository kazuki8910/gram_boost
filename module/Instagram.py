# モジュール

# 標準
import sys
import traceback

# 拡張
import requests
from selenium.webdriver.common.keys import Keys

# 自作
import EasyScraping as es





# 変数

# インスタグラムのURL
url_ig = 'https://www.instagram.com'

# モジュール名
module = "Instagram"





####################
# 
# 関数(基本)
#  
####################





####################
# 
# 関数(情報取得系)
#  
####################

# アカウントのフォロー数取得
def get_follow(driver):
    try:
        xpath = '/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span'
        elm = driver.find_element_by_xpath(xpath)
        text = int(elm.text)
    except:
        function = sys._getframe().f_code.co_name
        message = 'アカウントのフォロー数取得に失敗しました。'
        es.notice_error(module, function, message)

    return text


# 投稿画像のURLを取得
def get_post_img_url(driver):

    # 画像URLを格納するリスト
    img_urls = []

    # URLを取得するループ
    while True:

        # 投稿画像のラッパー
        xpath = '/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div'
        elm = driver.find_element_by_xpath(xpath)

        # 画像URLをリストに追加
        imgs = elm.find_elements_by_tag_name("img")
        for val in imgs:
            img_url = val.get_attribute('src')
            if not(img_url in img_urls):
                img_urls.append(img_url)

        # 進むボタンをクリック
        try:
            elm = driver.find_element_by_class_name('coreSpriteRightChevron')
            elm.click()
            es.wait(0.5, 0.5)
            
        # 最後の画像でループ終了
        except:
            break

    return img_urls





####################
# 
# 関数(操作系)
#  
####################

####################
# 
# ログイン
#  
####################

# ログインフォームへの遷移（セッションなし）
def move_to_login_form(driver):
    try:
        move_form_xpath = '/html/body/div[1]/section/main/article/div[2]/div/div/div[3]/span/button'
        move_form_elm = es.get_elm_by_xpath(driver, move_form_xpath)
        move_form_elm.click()
        es.wait()
    except:
        function = sys._getframe().f_code.co_name
        message = 'ログインフォームへの遷移（セッションなし）に失敗しました。'
        es.notice_error(module, function, message)

# ログイン操作（セッションなし）
def oparate_login(driver, login_id, login_pass):
    try:
        # IDを入力
        id_xpath = '//*[@id="loginForm"]/div/div[1]/div/label/input'
        id_elm = driver.find_element_by_xpath(id_xpath)
        id_elm.send_keys(login_id)
        es.wait(1, 0.5)

        # パスワードを入力
        pass_xpath = '//*[@id="loginForm"]/div/div[2]/div/label/input'
        pass_elm = driver.find_element_by_xpath(pass_xpath)
        pass_elm.send_keys(login_pass)
        es.wait(1, 0.5)

        # ログインボタンをクリック
        btn_xpath = '//*[@id="loginForm"]/div/div[3]/button'
        btn_elm = driver.find_element_by_xpath(btn_xpath)
        btn_elm.click()
        es.wait()
    except:
        function = sys._getframe().f_code.co_name
        message = 'ログイン操作(セッションなし)に失敗しました。'
        es.notice_error(module, function, message)

# ログインフォームへ移動（セッションあり）
def move_to_login_form_session(driver):
    try:
        # アカウントアイコンをクリック
        icon_xpath = '/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[5]/span/img'
        icon_elm = es.get_elm_by_xpath(driver, icon_xpath)
        icon_elm.click()
        es.wait()
        
        # アカントを切り替えるボタンをクリック
        change_xpath = '/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div[2]/div[2]/div[1]/div'
        change_elm = es.get_elm_by_xpath(driver, change_xpath)
        change_elm.click()
        es.wait()

        # 既存のアカウントにログインをクリック
        btn_xpath = '/html/body/div[5]/div/div/div[3]/button'
        btn_elm = es.get_elm_by_xpath(driver, btn_xpath)
        btn_elm.click()
        es.wait()

    except:
        function = sys._getframe().f_code.co_name
        message = 'ログインフォームへ移動（セッションあり）に失敗しました。'
        es.notice_error(module, function, message)

# ログイン操作（セッションあり）
def oparate_login_session(driver, login_id, login_pass):
    try:
        # IDを入力
        # インプット要素取得
        id_xpath = '/html/body/div[5]/div/div/div[2]/div/div/div/form/div[1]/div[1]/div/label/input'
        id_elm = es.get_elm_by_xpath(driver, id_xpath)
        # 中身削除
        id_elm.send_keys(Keys.CONTROL + "a")
        es.wait(0)
        id_elm.send_keys(Keys.DELETE)
        es.wait(0)
        # ID入力
        id_elm.send_keys(login_id)
        es.wait(1)

        # パスワードを入力
        # インプット要素取得
        pass_xpath = '/html/body/div[5]/div/div/div[2]/div/div/div/form/div[1]/div[2]/div/label/input'
        pass_elm = es.get_elm_by_xpath(driver, pass_xpath)
        # 中身削除
        pass_elm.send_keys(Keys.CONTROL + "a")
        es.wait(0)
        pass_elm.send_keys(Keys.DELETE)
        es.wait(0)
        # ID入力
        pass_elm.send_keys(login_pass)
        es.wait(1)

        # ログインボタンクリック
        btn_xpath = '/html/body/div[5]/div/div/div[2]/div/div/div/form/div[1]/div[4]/button'
        btn_elm = es.get_elm_by_xpath(driver, btn_xpath)
        btn_elm.click()
        es.wait()

    except:
        function = sys._getframe().f_code.co_name
        message = 'ログイン操作(セッションあり)に失敗しました。'
        es.notice_error(module, function, message)

# ログイン
def login(driver, insta_id, insta_pass):
    try:
        # インスタグラムにアクセス
        driver.get(url_ig)
        es.wait()

        # ログイン済みかどうかの判別（h1タグの有無で判別）
        h1_tag = driver.find_elements_by_tag_name('h1')
        is_login = len(h1_tag) == 0


        # 別のアカウントにログイン済だった場合のログイン操作
        if(is_login):
            move_to_login_form_session(driver)
            oparate_login_session(driver, insta_id, insta_pass)
        

        # 初回のログイン操作
        else:
            # ログイン履歴がある場合はログインフォームに移動する
            form_tag = driver.find_elements_by_tag_name('form')
            if(len(form_tag) == 0):
                move_to_login_form(driver)

            # ログイン情報の入力
            oparate_login(driver, insta_id, insta_pass)


    except:
        function = sys._getframe().f_code.co_name
        message = 'インスタグラムへのログインに失敗しました。'
        es.notice_error(module, function, message)

# フォロー中のリストを表示（プロフィール画面でフォローをクリック）
def display_follow(driver):
    try:
        xpath = '/html/body/div[1]/section/main/div/header/section/ul/li[3]/a'
        elm = driver.find_element_by_xpath(xpath)
        elm.click()
        es.wait()
    except:
        function = sys._getframe().f_code.co_name
        message = 'フォロー中のリスト表示に失敗しました。'
        es.notice_error(module, function, message)

# ログインを促す下のバナー削除
def delete_login_banner(driver):
    try:
        xpath = "/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div/div/button"
        elm = driver.find_element_by_xpath(xpath)
        elm.click()
        es.wait(1)
    except:
        True








####################
# 
# 関数（自動いいね）
#  
####################

# フォロー解除
def al_release_follow(driver, profile_url, release_min, release_follow):
    # profile_url：プロフィールのURL
    # release_min：これ以下のフォロー数だと、解除しない
    # release_follow：フォローの解除数

    try:
        # プロフィールに遷移(1回で移動できない時があるから、2回移動)
        for i in range(2):
            driver.get(profile_url)
            es.wait()

        # フォロー数取得
        follows = get_follow(driver)

        # フォロー解除するかどうかの判別
        if(follows > release_min):

            # フォロー中のリスト表示
            display_follow(driver)

            # 一番下までスクロール
            selector = 'body > div.RnEpo.Yx5HN > div > div > div.isgrP' # スクロールする要素のCSSセレクター
            item_xpath = [ # 取り得るXpath
                '/html/body/div[5]/div/div/div[2]/ul/div/li[1]/div',
                '/html/body/div[4]/div/div/div[2]/ul/div/li[1]/div'
            ]
            scroll_item = es.get_elm_by_xpaths(driver, item_xpath) # スクロールする要素
            scroll_height = scroll_item.size['height'] # 一回分のスクロール量取得
            for i in range(follows): # スクロール
                es.scroll(driver, selector, scroll_height)
                es.wait(0.1, 0.1)

            # フォロー解除ボタンの要素を取得
            xpaths = [
                '/html/body/div[4]/div/div/div[2]/ul/div/li/div/div[2]/button',
                '/html/body/div[5]/div/div/div[2]/ul/div/li/div/div[2]/button'
            ]
            elms = es.get_elms_by_xpaths(driver, xpaths)

            # フォロー解除のループ
            for i, elm in enumerate(reversed(elms)):

                # 解除数に到達したらループ終了
                if(i >= release_follow):
                    break

                elm.click() # フォロー中ボタンクリック
                es.wait(1)

                # フォローをやめるボタンをクリック
                release_xpaths = [
                    '/html/body/div[5]/div/div/div/div[3]/button[1]',
                    '/html/body/div[6]/div/div/div/div[3]/button[1]'
                    
                ]
                release_elm = es.get_elm_by_xpaths(driver, release_xpaths)
                release_elm.click()
                es.wait(1)

    # エラー時の動作
    except:
        function = sys._getframe().f_code.co_name
        message = 'フォロー解除中にエラーが起きました。'
        es.notice_error(module, function, message)

####################
# 
# いいねするリスト取得
#  
####################

# 1つ目の投稿クリック
def click_first_post(driver):
    try:
        xpath = '/html/body/div/section/main/div/div/article/div[1]/div/div[1]/div[1]/a'
        elm = es.get_elms_by_xpath(driver, xpath)[0]
        elm.click()
        es.wait(5)
    except:
        function = sys._getframe().f_code.co_name
        message = '1つ目の投稿のクリックに失敗しました。'
        es.notice_error(module, function, message)

# いいねしたアカウントのリストを表示
def show_favo_account_list(driver):
    try:
        xpaths = [
            '/html/body/div/div[2]/div/article/div[3]/section[2]/div/div/button',
            '/html/body/div/div[2]/div/article/div[3]/section[2]/div/div/a',
        ]
        elm = es.get_elms_by_xpaths(driver, xpaths)
        elm[0].click()
        es.wait(10)
    except:
        function = sys._getframe().f_code.co_name
        message = 'いいねしたアカウントの表示に失敗しました。'
        es.notice_error(module, function, message)

# いいねするユーザーのリストを取得する
def get_favo_user_list(driver, set_reach):
    try:
        # 格納用
        user_urls = set([])

        # 取得するループ
        while(True):
            # ユーザーのURLを取得
            xpath = '/html/body/div[6]/div/div/div[2]/div/div/div[1]'
            elm = es.get_elm_by_xpath(driver, xpath)
            url_elm = elm.find_element_by_tag_name('a')
            user_url = url_elm.get_attribute('href')
            user_urls.add(user_url)
            
            # リーチ数分取得したらループから抜ける
            if(len(user_urls) >= set_reach):
                break
            
            # 1つ分スクロール
            elm_height = elm.size["height"]
            selector = 'body > div.RnEpo.Yx5HN > div > div > div.Igw0E.IwRSH.eGOV_.vwCYk.i0EQd > div'
            es.scroll(driver, selector, elm_height)
            es.wait(0.1, 0.1)

        return user_urls

    except:
        function = sys._getframe().f_code.co_name
        message = 'いいねするユーザーリストの取得に失敗しました。'
        es.notice_error(module, function, message)


# いいね！
def do_favo(driver):
    try:
        # いいねボタンの要素
        xpath = '/html/body/div[5]/div[2]/div/article/div[3]/section[1]/span[1]/button'
        elm = es.get_elm_by_xpath(driver, xpath)

        # いいね済みかどうかの判定
        icon = elm.find_element_by_tag_name('svg')
        is_favoed = icon.get_attribute('aria-label')
        if(is_favoed == 'いいね！'):
            
            # いいね！
            elm.click()
            es.wait(1)

            # いいねしたらTrueを返す
            return True

        # いいねしなかったらFalseを返す
        return False

    except:
        function = sys._getframe().f_code.co_name
        message = 'いいね！に失敗しました。'
        es.notice_error(module, function, message)


# 1個前の投稿ボタンをクリック
def click_right_post_arrow(driver):
    try:
        selector = 'coreSpriteRightPaginationArrow'
        right_btn = driver.find_element_by_class_name(selector)
        right_btn.click()
        es.wait(5)
    except:
        function = sys._getframe().f_code.co_name
        message = '1個前の投稿ボタンをクリックに失敗しました。'
        es.notice_error(module, function, message)


# 投稿数取得
def get_post_num(driver):
    try:
        # 投稿数取得
        xpath = '/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span'
        elm = es.get_elm_by_xpath(driver, xpath)
        post_num = elm.text

        # 数値型に変換
        if(post_num == 'NaN'):
            post_num = 0
        elif("万" in post_num):
            post_num = int(float(post_num.replace("万","")) * 1000)
        else:
            post_num = int(post_num)

        return post_num

    except:
        function = sys._getframe().f_code.co_name
        message = '投稿数の取得に失敗しました。'
        es.notice_error(module, function, message)


# フォローする
def do_follow(driver, max_follow, follow_count):
    try:
        xpaths = [
            '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button',
            '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/button'
        ]
        elm = es.get_elm_by_xpaths(driver, xpaths)
        elm_text = elm.text

        if(elm_text == 'フォローする' and max_follow > follow_count):
            elm.click()
            es.wait()
            return True
        return False
    except:
        function = sys._getframe().f_code.co_name
        message = 'フォローに失敗しました。'
        es.notice_error(module, function, message)


# 鍵垢かどうかの判定
def is_lock(driver):
    try:
        # 返り値格納
        is_lock = False

        # h2タグを取得
        h2s = driver.find_elements_by_tag_name('h2')

        # h2タグが存在し、最後のh2タグの中身が「このアカウントは非公開です」だった場合、鍵垢判定True
        if(len(h2s) > 0):
            h2 = h2s[-1]
            if(h2.text == 'このアカウントは非公開です'):
                is_lock = True

        return is_lock

    except:
        function = sys._getframe().f_code.co_name
        message = '鍵垢の判定に失敗しました。'
        es.notice_error(module, function, message)


# シートにレポートを出力
def output_report(sheet_key, this_report):
    # シートの命名規則を取得
    report_sheet = es.get_sheet_name_convention()["favo_report"]
    sheet_name = report_sheet["name"]
    report_head = report_sheet["head"]

    # Sheet API認証
    gc = es.sheet_auth()

    # レポートシートを取得
    workbook  = gc.open_by_key(sheet_key)
    worksheet = workbook.worksheet(sheet_name)

    # レポートシートのカラム数取得
    report_col = worksheet.row_values(1)
    col_len = len(report_col)

    # 書き換える行を取得
    report_row = worksheet.range(2, 1, 2, col_len)

    # シートにレポートを反映
    for key in this_report:
        update_col = report_col.index(report_head[key]) # 書き換えるカラム数
        this_val = report_row[update_col].value # シートに書かれてる値を取得
        
        # 値がなかった場合、そのまま入力する
        if(this_val == ""):
            report_row[update_col].value = this_report[key]
            
        # 値があった場合、合算する
        else:
            report_row[update_col].value = int(this_val) + this_report[key]
            
    worksheet.update_cells(report_row) # アップデート









####################
#
# 関数（自動投稿）
#
####################

# 画像・動画ファイルを保存する関数（保存するだけ）
def save_file_part(driver, xpaths, ind):
    try:
        # Xpathのリストから画像/動画を取得
        content = es.get_elm_by_xpaths(driver, xpaths)
        response = requests.get(content.get_attribute('src')).content

        # ファイルの拡張子決定
        if(content.tag_name == 'img'):
            file_type = "jpg"
        elif(content.tag_name == 'video'):
            file_type = "mp4"

        # 画像/動画を保存
        with open(f'temporary/content_{ind}.{file_type}', "wb") as f:
            f.write(response)

    except:
        function = sys._getframe().f_code.co_name
        message = '画像・動画ファイルの保存に失敗しました。'
        es.notice_error(module, function, message)


# 画像・動画を保存する関数（色々加味したやつ）
def save_file(driver):
    try:
        # 投稿画像のラッパー
        xpath_wrapper = '/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div[1]'

        # 画像が２枚以上あった場合（進むボタンの有無で判定）
        ind = 1 # インデックス番号
        if(len(driver.find_elements_by_class_name('coreSpriteRightChevron')) == 1):

            next_btn = driver.find_element_by_class_name('coreSpriteRightChevron') # 次に進むボタンの要素

            # 画像/動画をローカルファイルに保存するループ
            while(True):
                # 進むボタンと戻るボタンの要素をリストで取得
                is_next_btn = len(driver.find_elements_by_class_name('coreSpriteRightChevron'))
                is_prev_btn = len(driver.find_elements_by_class_name('coreSpriteLeftChevron'))

                # 一枚目だった場合のXpath
                if(is_prev_btn == 0):
                    xpaths = [
                        f'{xpath_wrapper}/div[2]/div/div/div/ul/li[2]/div/div/div/div[1]/img',          # 画像1
                        f'{xpath_wrapper}/div[2]/div/div/div/ul/li[2]/div/div/div/div[1]/div[1]/img',   # 画像2
                        f'{xpath_wrapper}/div[2]/div/div/div/ul/li[2]/div/div/div/div[1]/div/div/video' # 動画
                    ]

                # 二枚目以降だった場合のXpath
                elif(is_prev_btn == 1):
                    xpaths = [
                        f'{xpath_wrapper}/div[2]/div/div/div/ul/li[3]/div/div/div/div[1]/img',          # 画像1
                        f'{xpath_wrapper}/div[2]/div/div/div/ul/li[3]/div/div/div/div[1]/div[1]/img',   # 画像2
                        f'{xpath_wrapper}/div[2]/div/div/div/ul/li[3]/div/div/div/div[1]/div/div/video' # 動画
                    ]

                # 動画・画像を保存
                save_file_part(driver, xpaths, ind)

                # 最後の画像/動画でbreak
                if(is_next_btn == 0):
                    break

                # 次の画像・動画に進む
                next_btn.click()
                es.wait(1)
                ind += 1

        # 画像/動画が一枚の時
        else:
            # コンテンツのXpath
            xpaths = [
                # 動画の場合
                '/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/div/div/video',
                # 画像の場合
                '/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/div[1]/img',
                '/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/img'
                
            ]
            # 画像・動画を保存
            save_file_part(driver, xpaths, ind)

    except:
        function = sys._getframe().f_code.co_name
        message = '画像・動画ファイルの保存に失敗しました。'
        es.notice_error(module, function, message)


# 投稿文を取得
def get_post_text(driver):
    try:
        # 投稿文取得
        post_xpath = '/html/body/div[1]/section/main/div/div[1]/article/div[3]/div[1]/ul/div/li/div/div/div[2]/span'
        post_elm   = es.get_elm_by_xpath(driver, post_xpath)
        post_text  = post_elm.get_attribute('innerHTML')

        # ハッシュタグ削除
        tags = post_elm.find_elements_by_tag_name('a')
        for tag in tags:
            post_text = post_text.replace(str(tag.get_attribute('outerHTML')), '')

        return post_text

    except:
        function = sys._getframe().f_code.co_name
        message = '投稿文の取得に失敗しました。'
        es.notice_error(module, function, message)


# プロフィール画面に遷移
def move_to_profile_from_post(driver):
    try:
        # プロフィール画面に遷移
        xpaths = [
            '/html/body/div[1]/section/main/div/div/article/header/div[2]/div[1]/div[1]/a',
            '/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[1]/span/a'
        ]
        elm = es.get_elm_by_xpaths(driver, xpaths)
        driver.get(elm.get_attribute('href'))
        es.wait()
    
    except:
        function = sys._getframe().f_code.co_name
        message = 'プロフィール画面への遷移に失敗しました。'
        es.notice_error(module, function, message)


# ユーザーID取得取得
def get_user_id(driver):
    try:
        # ユーザーID取得のラッパーを取得
        class_wrapper = 'nZSzR'
        elm_wrapper = driver.find_element_by_class_name(class_wrapper)

        # ユーザーID取得
        tags_user_id = [
            'h1',
            'h2'
        ]
        user_id_elm = es.get_elm_by_tags(elm_wrapper, tags_user_id)
        user_id = user_id_elm.text

        return user_id

    except:
        function = sys._getframe().f_code.co_name
        message = 'ユーザーIDの取得に失敗しました。'
        es.notice_error(module, function, message)


# ユーザー名取得取得
def get_user_name(driver):
    try:
        # ユーザー名
        user_name_elm = driver.find_element_by_tag_name('h1')
        user_name = user_name_elm.text
        return user_name
    except:
        return ''
        # function = sys._getframe().f_code.co_name
        # message = 'ユーザー名の取得に失敗しました。'
        # es.notice_error(module, function, message)





####################
#
# 投稿リストアップ
#
####################

# 投稿のいいね数取得
def get_favo_from_posts(driver, posts):
    try:
        # 投稿の情報を取得するループ
        post_info = []
        for ind,post in enumerate(posts):
            # 投稿にホバー
            es.hover(driver, post)
            es.wait(0.5, 0.1)

            # いいね数取得
            xpath_favo = 'a/div/ul/li[1]/span[1]'
            elm = es.get_elms_by_xpath(post, xpath_favo)[0]
            post_info.append([ind, elm.text]) # [インデックス番号, いいね数]
            es.wait(0.1)

            # 21個目で終了（それ以上だとログインを強制される）(ログインしてると問題ない)
            # if(ind>19):
            #     break

        return post_info
        
    except:
        function = sys._getframe().f_code.co_name
        message = '投稿のいいね数取得に失敗しました。'
        es.notice_error(module, function, message)

# 投稿一覧から投稿のURLを取得
def get_post_url_from_post_list(post):
    try:
        # 投稿のURLを取得
        elm_url = es.get_elm_by_xpath(post, "a")
        url = elm_url.get_attribute('href')
        return url

    except:
        function = sys._getframe().f_code.co_name
        message = '投稿のURL取得に失敗しました。'
        es.notice_error(module, function, message)









