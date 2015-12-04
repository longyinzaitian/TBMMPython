#coding:utf-8
__author__ = 'CQC'
# 我的博客地址：http://blog.csdn.net/u010156024/article/details/49977219
# 如有疑问，欢迎博客留言评论交流
import re
import urllib2

import tool

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
        pattern = re.compile('<div class="list-item".*?pic-word.*?'+
                             '<a href="(.*?)".target=.*?<img src="(.*?)".alt.*?'+
                             '<a class="lady-name".href="(.*?)".target=.*?>(.*?)'+
                             '</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>',re.S)
        items = re.findall(pattern,page)
        contents = []
        for item in items:
            print item
            contents.append([item[0],item[1],item[2],item[3],item[4],item[5]])
        return contents

    #将一页淘宝MM的信息保存起来
    def savePageInfo(self,pageIndex):
        #获取第一页淘宝MM列表
        contents = self.getContents(pageIndex)
        for item in contents:
            #item[0]个人详情URL,item[1]头像URL,item[2]是个人信息地址，item[3]姓名,
            #item[4]年龄,item[5]居住地
            print u"发现一位模特,名字叫",item[3],u"芳龄",item[4],u",她在",item[5]
            print u"正在偷偷地保存",item[3],"的信息"
            print u"又意外地发现她的个人地址是",item[0] #这个地址需要登录
            print u"名字对应的个人信息地址是",item[2]  #这个地址有用
            #个人详情页面的URL
            detailURL = item[0]
            print 'detailURL=https:%s' %detailURL
    def savePagesInfo(self,start,end):
        for i in range(start,end+1):
            print u"正在偷偷寻找第",i,u"个地方，看看MM们在不在"
            self.savePageInfo(i)
#传入起止页码即可，在此传入了1,10,表示抓取第1到10页的MM
spider = Spider()
spider.savePagesInfo(1,10)
