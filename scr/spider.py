#coding:utf-8
__author__ = 'CQC'
# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import tool
import os
#抓取MM
class Spider:
    #页面初始化
    def __init__(self):
        self.siteURL = 'http://mm.taobao.com/json/request_top_list.htm'
        self.tool = tool.Tool()
    #获取索引页面的内容
    def getPage(self,pageIndex):
        url = self.siteURL + "?page=" + str(pageIndex)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read().decode('gbk')
    #获取索引界面所有MM的信息，list格式
    def getContents(self,pageIndex):
        page = self.getPage(pageIndex)
        # 这里获取六条信息 个人信息网址，头像图片地址，美眉个人信息页地址，美眉名字，年龄，居住地址
        pattern = re.compile('<div class="list-item".*?pic-word.*?<a href="(.*?)".target=.*?<img src="(.*?)".alt.*?<a class="lady-name".href=(.*?).target=.*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>',re.S)
        items = re.findall(pattern,page)
        contents = []
        for item in items:
            contents.append([item[0],item[1],item[2],item[3],item[4],item[5]])
        return contents
    #获取MM个人详情页面
    def getDetailPage(self,infoURL):
        response = urllib2.urlopen("https:"+infoURL)
        return response.read().decode('gbk')
    #获取个人文字简介
    def getBrief(self,page):
        pattern = re.compile('.*?<div.class="mm-aixiu-content".*?>(.*?)<!–',re.S)
        result = re.search(pattern,page)
        if result is not None:
            return self.tool.replace(result.group(0))
        else:
            print 'getBrief()==empty'
            return 'empty'
    #获取页面所有图片
    def getAllImg(self,page):
        pattern = re.compile('.*?<div class="mm-aixiu-content".*?>(.*?)<!–',re.S)
        #个人信息页面所有代码
        content = re.findall(pattern,page)
        #从代码中提取图片
        patternImg = re.compile('<img.*?src="(.*?)">',re.S)
        images = re.findall(patternImg,content[0])
        return images
    #保存多张写真图片
    def saveImgs(self,images,name):
        number = 1
        print u"发现",name,u"共有",len(images),u"张照片"
        for imageURL in images:
            splitPath = imageURL.split('.')
            fTail = splitPath.pop()
            if len(fTail) > 3:
                fTail = "jpg"
            fileName = name + "/" + str(number) + "." + fTail
            self.saveImg(imageURL,fileName)
            number += 1
    # 保存头像
    def saveIcon(self,iconURL,name):
        splitPath = iconURL.split('.')
        fTail = splitPath.pop()
        fileName = name + "/icon." + fTail
        self.saveImg(iconURL,fileName)
    #保存个人简介
    def saveBrief(self,content,name):
        fileName = name + "/" + name + ".txt"
        f = open(fileName,"w+")
        print u"正在偷偷保存她的个人信息为",fileName
        f.write(content.encode('utf-8'))
    #传入图片地址，文件名，保存单张图片
    def saveImg(self,imageURL,fileName):
         u = urllib.urlopen(imageURL)
         data = u.read()
         f = open(fileName, 'wb')
         f.write(data)
         print u"正在悄悄保存她的一张图片为",fileName
         f.close()
    #创建新目录
    def mkdir(self,path):
        path = path.strip()
        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists=os.path.exists(path)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            print u"偷偷新建了名字叫做",path,u'的文件夹'
            # 创建目录操作函数
            os.makedirs(path)
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print u"名为",path,'的文件夹已经创建成功'
            return False
    #将一页淘宝MM的信息保存起来
    def savePageInfo(self,pageIndex):
        #获取第一页淘宝MM列表
        contents = self.getContents(pageIndex)
        for item in contents:
            #item[0]个人详情URL,item[1]头像URL,item[2]是个人信息地址，item[3]姓名,item[4]年龄,item[5]居住地
            print u"发现一位模特,名字叫",item[3],u"芳龄",item[4],u",她在",item[5]
            print u"正在偷偷地保存",item[3],"的信息"
            print u"又意外地发现她的个人地址是",item[0]
            print u"名字对应的个人信息地址是",item[2]
            #个人详情页面的URL
            detailURL = item[0]
            print 'detailURL=%s' %detailURL
            #得到个人详情页面代码
#             detailPage = self.getDetailPage(detailURL)
#             #获取个人简介
#             brief = self.getBrief(detailPage)
#             #获取所有图片列表
#             images = self.getAllImg(detailPage)
#             self.mkdir(item[2])
#             #保存个人简介
#             self.saveBrief(brief,item[2])
#             #保存头像
#             self.saveIcon(item[1],item[2])
#             #保存图片
#             self.saveImgs(images,item[2])
    #传入起止页码，获取MM图片
    def savePagesInfo(self,start,end):
        for i in range(start,end+1):
            print u"正在偷偷寻找第",i,u"个地方，看看MM们在不在"
            self.savePageInfo(i)
#传入起止页码即可，在此传入了2,10,表示抓取第2到10页的MM
spider = Spider()
spider.savePagesInfo(1,10)