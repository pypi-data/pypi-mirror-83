from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as options
import parser_bankr_lib.SQL_connect as SQL
import time
from bs4 import BeautifulSoup
import sys


class Parse(ABC):
    infos = []
    @staticmethod
    def get_browser():
        driver = SQL.Config("config.env").get_config()["webdriver"]
        chromium = SQL.Config("config.env").get_config()["chrome"]
        option = options()
        #option.binary_location = chromium
        option.add_argument("-headless")
        option.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36")
        return webdriver.Chrome(executable_path=driver, chrome_options=option)

    @abstractmethod
    def parse(self):
        pass


class ParserFedresurs(Parse):
    __route = "https://bankrot.fedresurs.ru/TradeList.aspx"

    def parse(self):
        browser = self.get_browser()
        browser.get(self.__route)
        time.sleep(2)
        i = 1
        page = 1
        soup = BeautifulSoup(browser.page_source, "html.parser")
        soup = soup.find("tr", class_="pager").find("tr").find_all("td")
        maxS = len(soup)
        loop = 0
        while(True):
            if i<maxS:
                sys.stdout.write(f"Page {page}\n")
                page+= 1
                browser.find_element_by_class_name("pager").find_element_by_tag_name("tr").find_elements_by_tag_name("td")[i].click()
                elements = BeautifulSoup(browser.page_source, "html.parser")
                elements = elements.find("table", class_='bank')
                elements = elements.find_all("tr")
                elements = elements[1:-2]
                for element in elements:
                    els = element.find_all("td")
                    res = els[2].get_text().replace("\t", "").replace("\n", "").replace(".", "-") + ":00"
                    res1 = res[res.find(" "):]
                    res2 = res[res.rfind("-")+1:res.find(" ")]+"-" + res[res.find("-")+1:res.rfind("-")] +"-" + res[:res.find("-")]
                    res3 = els[1].get_text().replace("\t","").replace("\n", "").replace(".","-")+":00"
                    res4 = res3[res3.find(" "):]
                    res5 = res3[res3.rfind("-") + 1:res3.find(" ")] + "-" + res3[res3.find("-") + 1:res3.rfind("-")] + "-" + res3[:res3.find("-")]
                    status = els[7].get_text().replace("\t","").replace("\n", "")
                    if status.find("прием") != -1:
                        status = 0
                    else:
                        status = 1
                    apptype = els[6].get_text().replace("\t","").replace("\n", "")
                    if apptype.find("Открытая") != -1:
                        apptype = 0
                    else:
                        apptype = 1
                    self.infos.append(
                        {
                            "BidID": els[0].get_text().replace("\t","").replace("\n", ""),
                            "BidDate": res5+res4,
                            "DeployDate": res2 + res1,
                            "AgencyURL": "https://bankrot.fedresurs.ru" + els[3].find("a").get("href"),
                            "Obligor": "https://bankrot.fedresurs.ru" + els[4].find("a").get("href"),
                            "BidType": els[5].get_text().replace("\t","").replace("\n", ""),
                            "Status": status,
                            "AppType": apptype
                        }
                    )
                i+=1
                time.sleep(2)
            else:
                i = 1
                soup = BeautifulSoup(browser.page_source, "html.parser")
                soup = soup.find("tr", class_="pager").find("tr").find_all("td")
                maxS = len(soup)
                if soup[maxS-1].get_text() != "...":
                    loop += 1
                if loop == 2:
                    break