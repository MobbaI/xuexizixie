import urllib.error
import urllib.request
import re

class Tool:
    removeImg = re.compile('<img.*?>| {7}|')
    removeAddr = re.compile('<a.*?>|</a>')
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    replaceTD = re.compile('<td>')
    replacePara = re.compile('<p.*?>')
    replaceBR = re.compile('<br><br>|<br>')
    removeExtraTag = re.compile('<.*?>')
    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        return x.strip()

class BDTB:

    def __init__(self, baseUrl, seeLZ, pageNum=1):
        self.baseUrl = baseUrl
        self.seeLZ = '?see_lz=' + str(seeLZ)
        self.tool = Tool()
        self.PageNum = pageNum

    def getPage(self):
        try:
            url = self.baseUrl + self.seeLZ + '&pn=' + str(self.PageNum)
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            return response.read().decode('utf-8')
        except urllib.error.URLError as e:
            if hasattr(e, 'reason'):
                print("连接百度贴吧失败，错误原因：" + e.reason)
                return None

    def getTitle(self):
        page = self.getPage()
        pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>', re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getPageNum(self):
        page = self.getPage()
        pattern = re.compile('<li class="l_reply_num.*?<span class="red" style.*?<span class="red">(.*?)</span>', re.S)
        num = re.findall(pattern, page)
        return num

    def getContent(self):
        txts = ''
        num = self.getPageNum()
        pattern = re.compile('<div id="post_content.*?>(.*?)</div>', re.S)
        while True:
            page = self.getPage()
            items = re.findall(pattern, page)
            for item in items:
                txt = self.tool.replace(item) + '\n\n\n\n\n----------------------------------------------------' \
                                                '-----------------------------------\n\n\n\n'
                txts += txt
            self.PageNum += 1
            if self.PageNum > int(num[0]):
                break
        return txts


baseURL = 'https://tieba.baidu.com/p/4973334088'
bdtb = BDTB(baseURL, 1)
content = bdtb.getContent()
file = open('贫僧为什么不可以谈恋爱.txt', 'w')
file.writelines(content)
file.close()