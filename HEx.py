#===========================================================#
#           HEx Library Selenium Adaptation 2019            #
#                 Coded By Swapz and M47Z                   #
#===========================================================#
# Dependencies: requests bs4 selenium lxml progressbar2
import os
import sys
import time
import requests
import progressbar
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.webdriver import WebDriver

Captcha_Error_Fault = 'please check the captcha box'
Captcha_Error_Token = "The reCAPTCHA wasn't entered correctly. Go back and try it again.(reCAPTCHA said: )"

class API:
    class Check:
        def _2captcha(Apikey):
            r = requests.get('http://2captcha.com/res.php?action=getbalance&key=' + Apikey).text
            if r == 'ERROR_KEY_DOES_NOT_EXIST':
                return False
            else:
                return True
        def _9kweu(Apikey):
            session = requests.post(
                    "https://www.9kw.eu/index.cgi?apikey=" + Apikey + "&action=usercaptchaguthaben")
            if "API key not found" in session.text:
                return False
            return True
        def _anticaptcha(Apikey):
            json_info = {"clientKey": Apikey}
            r = requests.post('https://api.anti-captcha.com/getBalance', json=json_info)
            if str(json.loads(r.text)['errorCode']) == "ERROR_KEY_DOES_NOT_EXIST":
                return False
            return True
    class Solver:
        def _2captcha(apikey, sitetoken, siteurl):
            taskID = requests.get('http://2captcha.com/in.php?key=' + apikey + '&method=userrecaptcha&googlekey=' + sitetoken + '&pageurl=' + siteurl + '&here=now').text.split("|")[1]
            i = 0
            while not "OK|" in requests.get('http://2captcha.com/res.php?key=' + apikey + '&action=get&id=' + taskID).text:
                time.sleep(3)
                i += 1
                if i >= 500:
                    return 0, 0
            token = requests.get('http://2captcha.com/res.php?key=' + apikey + '&action=get&id=' + taskID).text.split("|")[1]
            return token, taskID
        def _9kweu(apikey, sitetoken, siteurl):
            session = requests.post(
                    "https://www.9kw.eu/index.cgi?apikey=" + apikey + "&action=usercaptchaupload&interactive=1&file-upload-01=" + sitetoken + "&oldsource=recaptchav2&pageurl=" + siteurl)
            session_id = str(session._content).replace("b'", "").replace("'", "")
            i = 0
            while len(requests.get('https://www.9kw.eu/index.cgi?apikey=' + apikey + '&action=usercaptchacorrectdata&id=' + session_id).text) < 100:
                time.sleep(3)
                if 'ERROR NO USER' in requests.get('https://www.9kw.eu/index.cgi?action=userhistorydetail&id=' + session_id + '&apikey=' + apikey).text:
                    raise EnvironmentError
                i += 1
                if i >= 500:
                    return 0, 0
            token = requests.get('https://www.9kw.eu/index.cgi?apikey=' + apikey + '&action=usercaptchacorrectdata&id=' + session_id).text
            return token, session_id
        def _anticaptcha(apikey, sitetoken, siteurl):
            json_info = {"clientKey": apikey, "task": {"type": "NoCaptchaTaskProxyless", "websiteURL": siteurl, "websiteKey": sitetoken}}
            r = requests.post('https://api.anti-captcha.com/createTask', json=json_info)
            taskID = int(json.loads(r.text)['taskId'])
            i = 0
            while not json.loads(requests.post('https://api.anti-captcha.com/getTaskResult', json={"clientKey": apikey, "taskId": taskID}).text)['status'] == 'ready':
                time.sleep(3)
                i += 1
                if i >= 500:
                    return 0, 0
            r = requests.post('https://api.anti-captcha.com/getTaskResult', json={"clientKey": apikey, "taskId": taskID})
            token = json.loads(r.text)['solution']['gRecaptchaResponse']
            return token, taskID
    class Report:
        def _2captcha(apikey, taskID):
            requests.post("http://2captcha.com/res.php?key=" + Apikey + "&action=reportbad&id=" + taskID)
class Misc:
    getSiteToken = lambda driver: driver.page_source.split("'sitekey':'")[1].split("'")[0]
    getCwd = lambda: os.path.dirname(sys.executable) if hasattr(sys, 'frozen') else os.path.dirname(os.path.realpath(sys.argv[0]))
    cls = lambda: os.system('cls' if os.name == 'nt' else 'clear')
    def progress_Bar(i):
        widgets = [progressbar.Percentage(), progressbar.Bar(), progressbar.ETA()]
        bar = progressbar.ProgressBar(widgets=widgets, max_value=i).start()
        for t in range(i):
            time.sleep(1)
            bar.update(t + 1)
        bar.finish()
    def check_Page(driver):
        driver.get("https://hackerwars.io/")
        if not "Hacker Wars is an online hacking simulation game. Play" in driver.page_source:
            return False
        return True
    def check_Login(driver, user):
        driver.get("https://hackerwars.io/profile")
        if not user in driver.find_element_by_xpath('//*[@id="content"]/div[3]/div/div/div/div[1]/ul/li[1]/a/span[2]').text:
            return False
        return True
    def check_CFBypass(driver):
        if not "Please allow up to 5 seconds" in driver.page_source:
            return False
        return True
    def openTab(driver):
        bak = driver.current_window_handle
        driver.execute_script("window.open(\"\", \"_blank\");")
        driver.switch_to_window(driver.window_handles[-1])
        return bak
    def closeTab(driver, tab):
        driver.execute_script("window.close();")
        driver.switch_to_window(tab)
        return
class User:
    def login(driver, user, password, apiSolver, apikey):
        while True:
            while True:
                driver.get("https://hackerwars.io/")
                if Misc.check_Page(driver):
                    break
                if Misc.check_CFBypass(driver):
                    time.sleep(5)
                    continue
                time.sleep(120)
            if Misc.check_Login(driver, user):
                return
            driver.find_element_by_id('login-username').send_keys(username)
            driver.find_element_by_id('password').send_keys(password)
            token, taskID = apiSolver(apikey, Misc.getSiteToken(driver), driver.current_url)
            driver.execute_script('document.getElementById("g-recaptcha-response").innerHTML = "{}"'.format(token))
            time.sleep(1)
            driver.find_element_by_id('login-submit').click()
            time.sleep(3)
            if Captcha_Error_Token in driver.page_source:
                if API.Check._2captcha(apikey):
                    API.Report._2captcha(apikey, taskID)
                    continue
            if Captcha_Error_Fault in driver.page_source:
                continue
            if Misc.check_Page(driver):
                break
            if Misc.check_CFBypass(driver):
                time.sleep(5)
                continue
            time.sleep(120)
        return
    def ip(driver):
        bak = Misc.openTab(driver)
        driver.get("https://hackerwars.io/")
        ip = driver.find_element_by_xpath('/html/body/div[5]/div[1]/div/div[1]/span').text
        Misc.closeTab(driver, bak)
        return ip
    def money(driver):
        bak = Misc.openTab(driver)
        driver.get("https://hackerwars.io/")
        money = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/span').text
        Misc.closeTab(driver, bak)
        return money
    def space(driver):
        bak = Misc.openTab(driver)
        driver.get("https://hackerwars.io/software")
        space = driver.find_element_by_xpath('//*[@id=\"softwarebar\"]/div/span').text
        Misc.closeTab(driver, bak)
        return space
class Soft:
    def version(driver, softwareId):
        bak = Misc.openTab(driver)
        driver.get("https://hackerwars.io/software?id=" + softwareId)
        r = driver.find_element_by_xpath('//*[@id="content"]/div[3]/div/div/div/div[2]/div[1]/div[1]/div[2]/table/tbody/tr[2]/td[2]').text
        Misc.closeTab(driver, bak)
        return r
    def licensed(driver, softwareId):
        bak = Misc.openTab(driver)
        driver.get("https://hackerwars.io/software?id=" + softwareId)
        r = driver.find_element_by_xpath('//*[@id="content"]/div[3]/div/div/div/div[2]/div[1]/div[1]/div[2]/table/tbody/tr[3]/td[2]/font').text
        Misc.closeTab(driver, bak)
        return r
    def name(driver, softwareId):
        bak = Misc.openTab(driver)
        driver.get("https://hackerwars.io/software?id=" + softwareId)
        r = driver.find_element_by_xpath('//*[@id="content"]/div[3]/div/div/div/div[2]/div[1]/div[1]/div[2]/table/tbody/tr[1]/td[2]').text
        Misc.closeTab(driver, bak)
        return r
    def id(driver, softwareName):
        bak = Misc.openTab(driver)
        driver.get("https://hackerwars.io/software")
        trs = driver.find_element_by_xpath('//*[@id="content"]/div[3]/div/div/div/div[2]/div/table/tbody').find_elements_by_tag_name('tr')
        r = ""
        for tr in trs:
            if softwareName in tr.text:
                r = tr.get_attribute("id")
        Misc.closeTab(driver, bak)
        return r
    def delete(driver, id):
        bak = Misc.openTab(driver)
        driver.get('https://hackerwars.io/software.php?action=del&id=' + id, cookies=cookies)
        Misc.closeTab(driver, bak)
        return
    def research(driver, softwareId, delete, apiSolver, apikey):
        while True:
            while True:
                driver.get("https://hackerwars.io/university?id=" + softwareId)
                if Misc.check_Page(driver):
                    break
                if Misc.check_CFBypass(driver):
                    time.sleep(5)
                    continue
                time.sleep(120)
            driver.find_element_by_id("research").click()
            time.sleep(1)
            token, taskID = apiSolver(apikey, Misc.getSiteToken(driver), driver.current_url)
            driver.execute_script('document.getElementById("g-recaptcha-response").innerHTML = "{}"'.format(token))
            if delete:
                driver.find_element_by_xpath('//*[@id="research-area"]/div[1]/div/div[2]/form/div[2]/div/input').click()
            time.sleep(2)
            driver.find_element_by_xpath('//*[@id="research-area"]/div[1]/div/div[2]/form/div[5]/button').click()
            time.sleep(3)
            if Captcha_Error_Token in driver.page_source:
                if API.Check._2captcha(apikey):
                    API.Report._2captcha(apikey, taskID)
                    continue
            if Captcha_Error_Fault in driver.page_source:
                continue
            if Misc.check_Page(driver):
                break
            if Misc.check_CFBypass(driver):
                time.sleep(5)
                continue
            time.sleep(120)
class Task:
    def time(driver, id):
        bak = Misc.openTab(driver)
        driver.get('https://hackerwars.io/processes')
        soup = BeautifulSoup(driver.page_source, "lxml")
        tasks = soup.find('div', attrs={'class': 'widget-content padding noborder'}).find_all('li')
        for task in tasks:
            taskInfo = task.find('div', attrs={'class': 'process'})
            if id == taskInfo['data-process-id']:
                return int(taskInfo['data-process-timeleft'])
        Misc.closeTab(driver, bak)
        return 0
    def delete(driver, id):
        bak = Misc.openTab(driver)
        driver.get('https://hackerwars.io/processes?pid=' + id + '&del=1')
        Misc.closeTab(driver, bak)
        return
    def id(driver, target):
        bak = Misc.openTab(driver)
        driver.get('https://hackerwars.io/processes')
        soup = BeautifulSoup(driver.page_source, 'lxml')
        tasks = soup.find('div', attrs={'class': 'widget-content padding noborder'}).find_all('li')
        for task in tasks:
            name = task.find('div', attrs={'class': 'proc-desc'}).text
            if target in name:
                return task.find('div', attrs={'class': 'process'})['data-process-id']
        Misc.closeTab(driver, bak)      
        return 0  
    def complete(driver, id):
        bak = Misc.openTab(driver)
        driver.get('https://hackerwars.io/processes?pid=' + id)
        Misc.closeTab(driver, bak)
        return
    def name(driver, id):
        bak = Misc.openTab(driver)
        driver.get('https://hackerwars.io/processes')
        soup = BeautifulSoup(driver.page_source, 'lxml')
        tasks = soup.find('div', attrs={'class': 'widget-content padding noborder'}).find_all('li')
        for task in tasks:
            taskInfo = task.find('div', attrs={'class': 'process'})
            if id == taskInfo['data-process-id']:
                return task.find('div').text
        Misc.closeTab(driver, bak)
        return ""
class Selenium:
    def open(cwd):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--incognito")
        return webdriver.Chrome(options=chrome_options, executable_path="{}/chromedriver.exe".format(cwd))
