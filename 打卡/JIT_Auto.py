import os
import smtplib
import pyautogui
from email.mime.text import MIMEText
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# 注：需将个人教务系统账号密码以及相关邮箱信息分别存放在同目录下的myInfo.txt和emailInfo.txt文件中
with open('D:\PyCharmWorkSpace\打卡\myInfo.txt', 'r') as f:
    # 个人账号信息封装在myInfo.txt文件中，其中依次存放账号、密码信息（用空格分开）
    myInfo = f.read()
    myInfo = myInfo.split()
    usr_name = myInfo[0]
    usr_password = myInfo[1]


# 打卡
def checkIn():
    driver = webdriver.Chrome()
    driver.get("http://ehall.jit.edu.cn/new/index.html")
    print("加载“我的金科院”页面成功！")
    # 打开Chrome浏览器并进入我的金科院首页  注：需下载webdriver（Chrom版）放在Chrom根目录下，MacOS放在Python根目录下

    driver.maximize_window()
    now_handle = driver.current_window_handle
    driver.switch_to.window(now_handle)
    try:
        WebDriverWait(driver, 1800).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".amp-no-login-zh")))
    finally:
        sleep(1)
    driver.find_element_by_css_selector(".amp-no-login-zh").click()
    # 等待首页的登录按钮加载完成后点击登录按钮

    now_handle = driver.current_window_handle
    driver.switch_to.window(now_handle)
    print("加载登录页面成功!")

    driver.find_element_by_id("username").clear()
    driver.find_element_by_id("password").clear()
    driver.find_element_by_id("username").send_keys(usr_name)
    sleep(1)
    driver.find_element_by_id("password").send_keys(usr_password)
    sleep(1)
    driver.find_element_by_css_selector(".ipt_btn_dl").click()
    # 进入登录界面后填写用户名和密码并点击登录

    now_handle = driver.current_window_handle
    print("加载“学生桌面”页面成功!")
    sleep(1)
    driver.switch_to.window(now_handle)
    try:
        WebDriverWait(driver, 1800).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".card-myFavorite-content-item > .style-scope:nth-child(4) .widget-title")))
    finally:
        sleep(1)

    driver.find_element_by_css_selector(
        ".card-myFavorite-content-item > .style-scope:nth-child(4) .widget-title").click()
    # 成功进入学生桌面后等待“健康信息填报系统”按钮加载完成，加载完成后点击它进入打卡页面

    windos = driver.window_handles
    driver.switch_to.window(windos[-1])
    # 切换到新打开的打卡页面窗口
    print("加载“信息填报”页面成功!")
    sleep(1)
    now_handle = driver.current_window_handle
    try:
        WebDriverWait(driver, 1800).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".bh-mb-16 > .bh-btn-primary")))
    finally:
        sleep(1)
    driver.find_element_by_css_selector(".bh-mb-16 > .bh-btn-primary").click()
    # 等待“新增”按钮加载完成，加载完成后点击“新增”按钮
    print("点击“新增”按钮")

    now_handle = driver.current_window_handle
    driver.switch_to.window(now_handle)

    # 判断是否已经打卡过
    try:
        driver.find_element_by_xpath("//div[text()='今日已填报！']")
        # 如果点击“新增”按钮时弹出已填报的对话框说明已经打卡过了。
        print("今日已打卡！无需再次打卡！")
        sentEmail()
        shutdown()
        driver.quit()
        return
    except:
        print("今日还未打卡！开始打卡!")

    sleep(3)
    try:
        WebDriverWait(driver, 1800).until(
            EC.presence_of_element_located((By.NAME, "DZ_DZBZ")))
    finally:
        sleep(1)

    js = "var q=document.documentElement.scrollTop=1300"
    driver.execute_script(js)
    # 将页面滚动

    # print("请将光标移动到“14天内是否去过南京以外城市！！！")
    # sleep(3)
    # x, y = pyautogui.position()
    # print("14天内是否去过南京以外城市 ：", x, y)
    # pyautogui.moveTo(x, y)
    sleep(1)
    pyautogui.click(378, 767)
    x, y = pyautogui.position()
    print(x, y)
    # 将光标移动到“14天内是否去过南京以外城市”并点击

    # print("请将光标移动到“是”！！！")
    # sleep(3)
    # x, y = pyautogui.position()
    # print("是 ：", x, y)
    # pyautogui.moveTo(x, y)
    sleep(3)
    pyautogui.click(241, 583)
    x, y = pyautogui.position()
    print(x, y)
    # 将光标移动到“是”并点击

    sleep(3)
    driver.find_element_by_id("save").click()
    print("点击“保存”按钮")
    # 等待“保存”按钮加载完成，加载完成后点击“保存”按钮

    now_handle = driver.current_window_handle
    driver.switch_to.window(now_handle)

    try:
        WebDriverWait(driver, 1800).until(
            EC.presence_of_element_located((By.XPATH, "//label[text()='否']")))
    finally:
        sleep(1)
    driver.find_element_by_xpath("//label[text()='否']").click()
    # 等待“是否”对话框加载完成，加载完成后点击“否”单选框
    print("选择“否”")
    sleep(5)
    driver.find_element_by_xpath("//button[contains(@class,'bh-btn bh-btn-primary')]").click()
    print("点击“确定“按钮")
    # 点击提交后打卡成功

    now_handle = driver.current_window_handle
    driver.switch_to.window(now_handle)
    sleep(5)
    try:
        WebDriverWait(driver, 1800).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".bh-mb-16 > .bh-btn-primary")))
    finally:
        sleep(1)
    driver.find_element_by_css_selector(".bh-mb-16 > .bh-btn-primary").click()
    # 通过再次点击“新增”按钮来测试打卡是否成功
    print("再次点击“新增”按钮以测试打卡成功否")
    try:
        driver.find_element_by_xpath("//div[text()='今日已填报！']")
        # 如果再次点击“新增”按钮时弹出已填报的对话框说明打卡成功了。
        print("打卡成功！")
    except:
        print("打卡失败！将尝试再次进行打卡！")
        checkIn()
        # 若没有成功则再次执行打卡程序。

    sleep(3)
    driver.quit()
    sentEmail()
    # 发送邮件通知打卡成功
    print("一分钟后将关机！！！")
    sleep(5)
    shutdown()
    # 关机


# 发邮件
def sentEmail():
    with open('D:\PyCharmWorkSpace\打卡\emailInfo.txt', 'r') as f1:
        # 电子邮箱信息封装在emailInfo.txt文件中，其中依次存放SMTP服务器地址、发送者邮箱账号、发送者QQ邮箱授权码、接收者邮箱账号信息（用空格分开）
        # 注：需进QQ邮箱设置中开启POP3/SMTP服务（开户后会显示授权码，务必记下，登录邮箱时要用到）、IMAP/SMTP服务，
        # 并勾选“收取我的文件夹”、“SMTP发信后保存到服务器”，也可使用其他邮箱，使用方法见百度
        emailInfo = f1.read()
        emailInfo = emailInfo.split()
        host = emailInfo[0]
        sender = emailInfo[1]
        qqCode = emailInfo[2]
        receiver = emailInfo[3]
    port = 465
    body = '<h1>你已成功打卡</h1>'
    msg = MIMEText(body, 'html')
    msg['subject'] = '打卡通知'
    msg['from'] = sender
    msg['to'] = receiver

    s = smtplib.SMTP_SSL(host, port)
    s.login(sender, qqCode)
    # sender就是要登录的邮箱的账号，qqCode就是QQ邮箱的授权码
    s.sendmail(sender, receiver, msg.as_string())
    print("成功发送邮件！")
    # 发送邮件的函数，打卡完成后发送一封email到接收者邮箱


# 关机
def shutdown():
    os.system("shutdown -s -t  60 ")
    print("一分钟后关机！！！")


if __name__ == "__main__":
    checkIn()
    # # 测试用，立即执行checkIn函数
    # schedule.every().day.at("00:00").do(checkIn)
    # 晚上12点时执行打卡的函数，成功后会发送邮件提示并自动关机
    #
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
