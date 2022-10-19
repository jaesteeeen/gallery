#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time


class Images():
    def __init__(self, jsonData, bing_url=""):
        if jsonData == None:
            return None

        # 图片地址
        url = jsonData['url']
        if "&" in  url:
            self.image_url = bing_url + url[:url.index('&')]
        else:
            self.image_url = url

        # 图片时间
        enddate = jsonData['enddate']
        self.date = enddate
        timeStruct = time.strptime(enddate, "%Y%m%d")
        self.showDate = time.strftime("%Y-%m-%d", timeStruct)
        self.showMonth = self.showDate[:7]

        # 图片版权
        self.desc = jsonData['copyright']
        self.copyrightlink = jsonData['copyrightlink'] 

    # markdown文件 格式化显示图片
    def toString(self):
        url = self.image_url + "&pid=hp&w=384&h=216&rs=1&c=4"
        return "![]({}){} [download 4k]({})".format(url, self.showDate, self.image_url)

    # markdown文件 格式化today显示
    def toLarge(self):
        url = self.image_url + "&w=1000"
        return "![]({})Today: [{}]({})".format(url, self.desc, self.image_url)

    # 新增json数据的格式化
    def toJson(self):
        return {
                "enddate": self.date,
                "url": self.image_url,
                "copyright": self.desc,
                "copyrightlink": self.copyrightlink
               }