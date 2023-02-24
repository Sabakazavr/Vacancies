import time as tm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import datetime

proj_hrefs = []

file = Service("./chromedriver.exe")

options = webdriver.ChromeOptions()
options.headless = True

browser = webdriver.Chrome(service=file, options=options)

def login():
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

    keys = browser.find_element(By.ID, "searchpro-sterms")
    keys.clear()
    keys.send_keys("Дизайн, UX/UI, Web, Веб, Сайт, Пост")

    browser.find_element(By.XPATH,
                         "/html/body/div[3]/div[2]/div/form/div/div[1]/div[1]/div/div[1]/label[7]/input").click()
    browser.find_element(By.XPATH,
                         "/html/body/div[3]/div[2]/div/form/div/div[1]/div[1]/div/div[1]/label[9]/input").click()

    browser.find_element(By.ID, "searchpro-premium_access").click()

    browser.find_element(By.ID, "searchBtn").click()

def parse():
    browser.refresh()
    tm.sleep(1)

    list = browser.find_element(By.CLASS_NAME, "list-view")
    projects = list.find_elements(By.CLASS_NAME, "project")
    answers = []
    flag = False
    for project in projects:
        href = project.find_element(By.CLASS_NAME, "description").get_attribute("href")
        if href not in proj_hrefs:
            proj_hrefs.append(href)
            answer = []
            title = project.find_element(By.CLASS_NAME, "title").text
            desc = project.find_element(By.CLASS_NAME, "description").text
            cost = project.find_element(By.CLASS_NAME, "cost").text
            term = project.find_element(By.XPATH, "//div[@class='term']/span").text
            answer.extend([href, title, desc, cost, term])
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
                proj_hrefs.remove(href)

    if flag:
        return(answers)
    else:
        return False
    browser.close()



