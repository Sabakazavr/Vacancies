import time as tm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import datetime

proj_hrefs_frlnc = []
proj_hrefs_fl = []

file = Service("./chromedriver.exe")

options = webdriver.ChromeOptions()
#options.headless = True

def open():
    global browser
    browser = webdriver.Chrome(service=file, options=options)

    browser.get('https://freelance.ru')

    browser.execute_script("window.open('');")
    browser.switch_to.window(browser.window_handles[1])
    browser.get('https://www.fl.ru/projects/category/dizajn/')

def login_frlnc():
    browser.switch_to.window(browser.window_handles[0])
    browser.get('https://freelance.ru/login/')
    tm.sleep(1)
    login = browser.find_element(By.NAME, 'login')
    login.clear()
    login.send_keys("Solovey20140")

    password = browser.find_element(By.NAME, 'passwd')
    password.clear()
    password.send_keys("20andrus02")

    check = browser.find_element(By.NAME, 'check_ip')
    check.click()

    browser.find_element(By.NAME, "submit").click()
    tm.sleep(1)

    browser.get('https://freelance.ru/project/search/pro')
    tm.sleep(1)

    """keys = browser.find_element(By.ID, "searchpro-sterms")
    keys.clear()
    keys.send_keys("Дизайн, UX/UI, Web, Веб, Сайт, Пост")"""

    browser.find_element(By.XPATH,
                         "/html/body/div[3]/div[2]/div/form/div/div[1]/div[1]/div/div[1]/label[7]/input").click()
    browser.find_element(By.XPATH,
                         "/html/body/div[3]/div[2]/div/form/div/div[1]/div[1]/div/div[1]/label[9]/input").click()

    browser.find_element(By.ID, "searchpro-premium_access").click()

    browser.find_element(By.ID, "searchBtn").click()

def parse_frlnc():
    try:
        browser.switch_to.window(browser.window_handles[0])
        browser.refresh()
        tm.sleep(1)

        list = browser.find_element(By.CLASS_NAME, "list-view")
        projects = list.find_elements(By.CLASS_NAME, "project")
        answers = []
        flag = False
        for project in projects:
            href = project.find_element(By.CLASS_NAME, "description").get_attribute("href")
            if href not in proj_hrefs_frlnc:
                time_str = project.find_element(By.CLASS_NAME, "timeago").get_attribute("datetime")
                time = datetime.datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S+0300')
                time_now = datetime.datetime.now()
                div = time_now - time
                div_in_s = div.total_seconds()
                hours = divmod(div_in_s, 3600)[0]
                if hours <= 4:
                    proj_hrefs_frlnc.append(href)
                    answer = []
                    title = project.find_element(By.CLASS_NAME, "title").text
                    desc = project.find_element(By.CLASS_NAME, "description").text
                    cost = project.find_element(By.CLASS_NAME, "cost").text
                    term = project.find_element(By.XPATH, "//div[@class='term']/span").text
                    answer.extend(["freelance.ru", title, cost, term, desc, href])
                    answers.append(answer)
                    flag = True
            else:
                time_str = project.find_element(By.CLASS_NAME, "timeago").get_attribute("datetime")
                time = datetime.datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S+0300')
                time_now = datetime.datetime.now()
                div = time_now - time
                div_in_s = div.total_seconds()
                hours = divmod(div_in_s, 3600)[0]
                if hours >= 240:
                    proj_hrefs_frlnc.remove(href)

        if flag:
            return(answers)
        else:
            return False
    except:
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        browser.close()
        do_all()

def parse_fl():
    try:
        browser.switch_to.window(browser.window_handles[1])
        browser.refresh()
        tm.sleep(1)

        list = browser.find_element(By.CLASS_NAME, "b-page__lenta")
        projects = list.find_elements(By.CLASS_NAME, "b-post")
        answers = []
        flag = False
        for project in projects:
            href = project.find_element(By.CLASS_NAME, "b-post__link").get_attribute("href")
            if href not in proj_hrefs_fl:
                time_str = project.find_element(By.CLASS_NAME, "b-post__foot").find_elements(By.CLASS_NAME, "b-post__txt")[0].text.splitlines()[2]
                if all([x not in time_str for x in ["часов", "4 часа", "день", "дней"]]):
                    proj_hrefs_fl.append(href)
                    answer = []
                    title = project.find_element(By.CLASS_NAME, "b-post__link").text
                    desc = project.find_element(By.CLASS_NAME, "b-post__txt").text
                    cost = project.find_element(By.CLASS_NAME, "b-post__price").text
                    term = "-"
                    answer.extend(["fl.ru", title, cost, term, desc, href])
                    answers.append(answer)
                    flag = True
            else:
                time_str = project.find_element(By.CLASS_NAME, "b-post__foot").find_elements(By.CLASS_NAME, "b-post__txt")[0].text.splitlines()[2]
                if any([x in time_str for x in ["часов", "4 часа", "день", "дней"]]):
                    proj_hrefs_fl.remove(href)

        if flag:
            return(answers)
        else:
            return False
    except:
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        browser.close()
        do_all()

def all_parse():
    answer = []
    flag = False
    a = parse_frlnc()
    if a:
        answer.extend(a)
        flag = True
    b = parse_fl()
    if b:
        answer.extend(b)
        flag = True
    if flag:
        return answer
    else:
        return flag

def do_all():
    open()
    login_frlnc()
    answer = []
    flag = False
    a = parse_frlnc()
    if a:
        answer.extend(a)
        flag = True
    b = parse_fl()
    if b:
        answer.extend(b)
        flag = True
    if flag:
        return answer
    else:
        return flag



