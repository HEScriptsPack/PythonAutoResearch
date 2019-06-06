#===========================================================#
#              Simple HEx Auto Research 2019                #
#                      Coded By M47Z                        #
#===========================================================#
# Dependencies: HEx Library Selenium Adaptation
# Note: It needs chromedriver.exe on same Folder and Chrome installed!
import time
import HEx

username = ""                                   #Username
password = ""                                   #Password
software = ""                                   #Software Name (not All Necessarly)
apikey = ""                                     #API Key
apisolver = HEx.API.Solver._2captcha            #Api Solver Function

cwd = HEx.Misc.getCwd()
driver = HEx.Selenium.open(cwd)

while True:
    if not HEx.Misc.check_Login(driver, username):
        print("[?] Login in...")
    
        HEx.User.login(driver, username, password, apisolver, apikey)
        HEx.Misc.cls()
        
        print("[?] Logged in as {}!".format(username))
        
    softID = HEx.Soft.id(driver, software)
    softFullName = HEx.Soft.name(driver, softID)
    softVersion = HEx.Soft.version(driver, softID)
        
    print("[+] Researching Software {} {}...".format(username, softFullName, softVersion))
    
    HEx.Soft.research(driver, softID, True, apisolver, apikey)
    
    print("[+] Research Process Started!")
    
    taskID = HEx.Task.id(software)
    taskTime = HEx.Task.time(driver, taskID)
    
    print("[+] Waiting {} Until Research is Done...".format(taskTime))
    
    HEx.Misc.progress_Bar(taskTime)
    
    print("[+] Research Process Finished!")
    
    if not HEx.Misc.check_Login(driver, username):
        print("[?] Login in...")
    
        HEx.User.login(driver, username, password, apisolver, apikey)
        HEx.Misc.cls()
        
        print("[?] Logged in as {}!".format(username))
        
    HEx.Task.complete(taskID)
    softID = HEx.Soft.id(driver, software)
    softFullName = HEx.Soft.name(driver, softID)
    softVersion = HEx.Soft.version(driver, softID)
    
    print("[+] Software {} Reached {}!".format(softFullName, softVersion))