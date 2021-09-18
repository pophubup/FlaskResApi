from selenium import webdriver
from time import sleep
import os
import json

class DATOInforLoader():
    def __init__(self, username, filepath, totalpage):
        self.url = "https://twlolstats.com/summoner/?summoner={}".format(
            username)
        self.path = filepath
        self.totalpage = totalpage

    def __CreateDriver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless") #無頭模式
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(
            executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        driver.maximize_window()
        driver.get(self.url)
        str1 = driver.title
       
        if str1 == 'Server Error (500)':
            return (404, "Not Found Resource")
         
        return (200 ,driver)
    def __GetData(self):
        status, driver = self.__CreateDriver()
        if status == 404:
            return (404, driver)
        gather2 = []
        x = [i for i in range(2, self.totalpage) if i != self.totalpage]
        for i in x:
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            sleep(1)
            str = '#game{} input'.format(i)
            driver.find_elements_by_css_selector(str)[0].click()
            sleep(1)
            str = '#game{} table tbody td:nth-child(3) div:nth-child(1) b'.format(
                i)
            isWin = driver.find_elements_by_css_selector(str)
            str2 = '#game{} table tbody td:nth-child(3) div:nth-child(2)'.format(
                i)
            Kind = driver.find_elements_by_css_selector(str2)
            str3 = '#game{} table tbody td:nth-child(3) div:nth-child(3)'.format(
                i)
            FinshTime = driver.find_elements_by_css_selector(str3)
            str4 = '#game{} table tbody td:nth-child(3) div:nth-child(4)'.format(
                i)
            TotalHour = driver.find_elements_by_css_selector(str4)
            final1 = [{"index": g + 1, "isWinOrFail": isWin[g].text, "type": Kind[g].text,
                       "finishTime": FinshTime[g].text, "totalPlayHour": TotalHour[g].text} for g, v in enumerate(isWin)]
            gather2.append({"page": i, "result": final1})
            isWin = driver.find_elements_by_css_selector(
                'table:nth-child(2) tbody td:nth-child(3) div:nth-child(1) b')
            Kind = driver.find_elements_by_css_selector(
                'table:nth-child(2) tbody td:nth-child(3) div:nth-child(2)')
            FinshTime = driver.find_elements_by_css_selector(
                'table:nth-child(2) tbody td:nth-child(3) div:nth-child(3)')
            TotalHour = driver.find_elements_by_css_selector(
                'table:nth-child(2) tbody td:nth-child(3) div:nth-child(4)')
            final1 = [{"index": g + 1, "isWinOrFail": isWin[g].text, "type": Kind[g].text,
                       "finishTime": FinshTime[g].text, "totalPlayHour": TotalHour[g].text} for g, v in enumerate(isWin)]
            gather2.insert(0, {"page": 1, "result": final1})
        return (200 , gather2)

    def DataAsJsonData(self):
        return self.__GetData()

    def DataAsJsonPhysicalFile(self):
        state, result = self.__GetData()
        if state == 404:
            return "No Resource Found"
        with open(self.path, 'w') as outfile:
            json.dump(result, outfile, sort_keys=True, indent=4,
                      ensure_ascii=False)
        return "Save Finished"

##
# obj = DATOInforLoader(
#    "fdsfds", r'C:\Users\Yohoo\Desktop\myAllTest\zWebCrawlingRepository\pys\data.json', 10)

# print(obj.DataAsJsonPhysicalFile())
