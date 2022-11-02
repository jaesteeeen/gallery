#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from pathlib import *
import calendar
from queue import Queue
import requests
from FileUtils import FileUtils
from Images import Images


class Gallery:

    def __init__(self, region):
        self.bing_url = "https://www.bing.com"
        self.url = "https://global.bing.com/HPImageArchive.aspx?format=js&idx=0&n=9&pid=hp&FORM=BEHPTB&uhd=1&uhdwidth=3840&uhdheight=2160&setmkt={}&setlang=en"
        self.headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42"
                        }
        self.region = region
        if region == "zh-CN":
            self.readmefile = "README.md"
        else:
            self.readmefile = region + ".md"
        self.jsonfile = region + ".json"

    def get_gallery(self):
        result = requests.get(self.url.format(self.region), headers=self.headers).json()

        file = FileUtils(self.jsonfile, self.readmefile)
        all = file.loadJson()

        if not result.get("images"):
            print("API接口出错啦! 请检查接口!")
        
        json_list = result["images"]
        items = [ item for item in json_list ]
        for item in items[::-1]:
            item = Images(item, self.bing_url)
            if item.date not in [ row["enddate"] for row in all["images"] ]:
                file.dumpImagesJson(all, item)
                print("{}的json数据更新完成!".format(self.region))

        today = Images(result["images"][0], self.bing_url)
        temp = [ item["enddate"][:6] for item in all["images"] ]
        months = list(set(temp))
        months.sort(key=temp.index)
        months.reverse()
        file.writeToReadme(all, today, months, self.region)
        print("主目录{}的README已重新生成!".format(self.region))
        print("-------------------------------")


    def archive(self):
        file = FileUtils(self.jsonfile, self.readmefile)
        all = file.loadJson()
        if not all["months"]["archive"]:
            if all["months"]["active"]:
                months = all["months"]["active"]
            else:
                temp = [ item["enddate"][:6] for item in all["images"] ]
                months = list(set(temp))
                months.sort(key=temp.index)
        elif all["months"]["archive"]:
            if all["months"]["active"]:
                months = all["months"]["active"]
            else:
                old_archive = all["months"]["archive"]
                total = [ item["enddate"][:6] for item in all["images"] ]
                months = list(set(total) - set(old_archive))
        
        for month in months:
            path = PurePosixPath("archive", self.region, month)
            Path(path).mkdir(parents=True, exist_ok=True)
            file.writeToArchive(all, path, month)
            print("{}历史存档整理完成!".format(self.region))
            print("*******************************")
            lastdate = month + str(calendar.monthrange(int(month[:4]), int(month[-2:]))[1])
            if lastdate in [ item["enddate"] for item in all["images"] ]:
                if all["months"]["active"]:
                    all["months"]["active"].remove(month)
                all["months"]["archive"].append(month)
            else:
                if not all["months"]["active"]:
                    all["months"]["active"].append(month)
            file.dumpMonthsJson(all, month)


regions = ["en-US", "zh-CN", "ja-JP", "en-IN", "pt-BR", "fr-FR", "de-DE", "en-CA", "en-GB", "it-IT", "es-ES", "fr-CA"]
# 中文 | English(US) | 日本語 | Hindi/हिन्दी/India | Português do Brasil | Français | Deutsch | English(CA) | English(GB) | Italiano | Español | Français(CA) |
q = Queue()

if __name__ == "__main__":
    for region in regions:
        gallery = Gallery(region)
        q.put(gallery.get_gallery())
        q.put(gallery.archive())
        q.get()
        q.get()