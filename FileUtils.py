#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from Images import Images


class FileUtils:
    def __init__(self, jsonfile, readmefile):
        # work_dir = os.path.abspath(".")
        self.local_json_path = os.path.join("json", jsonfile)
        self.readme_path = readmefile
        self.dic =  {
                     "images": [],
                     "months": {
                                "archive": [],
                                "active": []
                               }
                    }

    # 读取保存的json文件
    def loadJson(self):
        if os.path.exists(self.local_json_path):
            with open(self.local_json_path, "r", encoding="utf-8")as f:
                local_json = json.load(f)
                return local_json
        else:
            return self.dic

    # 将图片信息写入json文件
    def dumpImagesJson(self, jsonData, item):
        if not jsonData or jsonData == None:
            jsonData = self.dic

        with open(self.local_json_path, 'w', encoding="utf-8")as f:
            jsonData["images"].append(item.toJson())
            f.write(json.dumps(jsonData, indent=2, ensure_ascii=False))

    # 将存档年月信息写入json文件
    def dumpMonthsJson(self, jsonData, month):
        if not jsonData or jsonData == None:
            jsonData = self.dic

        with open(self.local_json_path, "w", encoding="utf-8")as f:
            f.write(json.dumps(jsonData, indent=2, ensure_ascii=False))

    # 主目录的README.md
    def writeToReadme(self, items, today, months="", region=""):
        if items == None or today == None:
            return

        # 主目录的readme只展示最近30天的图片
        # regions = ["en-US", "zh-CN", "ja-JP", "en-IN", "pt-BR", "fr-FR", "de-DE", "en-CA", "en-GB", "it-IT", "es-ES", "fr-CA"]
        # 中文 | English(US) | 日本語 | Hindi/हिन्दी/India | Português do Brasil | Français | Deutsch | English(CA) | English(GB) | Italiano | Español | Français(CA) |
        with open(self.readme_path, "w", encoding="utf-8")as f:
            f.write("## Bing Wallpaper\n")
            f.write("[中文](README.md) | \
                    [English(US)](en-US.md) | \
                    [日本語](ja-JP.md) | \
                    [English(IN)](en-IN.md) | \
                    [Português do Brasil](pt-BR.md) | \
                    [Français](fr-FR.md) | \
                    [Deutsch](de-DE.md) | \
                    [English(CA)](en-CA.md) | \
                    [English(GB)](en-GB.md) | \
                    [Italiano](it-IT.md) | \
                    [Español](es-ES.md) | \
                    [Français(CA)](fr-CA.md) |\
                    \n\n")
            f.write(today.toLarge())
            f.write('\n\n|      |      |      |\n')
            f.write('| :----: | :----: | :----: |\n')
            index = 1
            item_list = [ item for item in items["images"] ][-31:-1]
            item_list.reverse()
            for el in item_list:
                el = Images(el)
                f.write('|' + el.toString())
                if index % 3 == 0:
                    f.write('|\n')
                index += 1
            if index % 3 != 1:
                f.write('|')

            f.write("\n\n")
            if region == "zh-CN":
                f.write("### 历史存档:\n")
            else:
                f.write("### Archive:\n")
            for i in months:
                path = os.path.join("archive", region, i, "README.md")
                # if len(months) == 1:
                #     i = months[0] 
                f.write("[{}-{}]({}) | ".format(i[:4], i[-2:], path))

    # 每月存档readme
    def writeToArchive(self, items, path, month):
        rows = [ item for item in items["images"] if item["enddate"].startswith(str(month)) ]
        last = rows.pop()
        rows.reverse()
        file = os.path.join(path, "README.md")
        with open(file, "w", encoding="utf-8")as f:
            f.write('## Bing Wallpaper ({}-{})\n'.format(month[:4],month[-2:]))
            last = Images(last)
            f.write(last.toLarge())
            f.write('\n\n|      |      |      |\n')
            f.write('| :----: | :----: | :----: |\n')
            index = 1
            for row in rows:
                row = Images(row)
                f.write('|' + row.toString())
                if index % 3 == 0:
                    f.write('|\n')
                index += 1
            if index % 3 != 1:
                f.write('|')