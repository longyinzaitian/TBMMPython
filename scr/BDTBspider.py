#_*_encoding=utf8_*_
'''
Created on 2015年11月22日

@author: 15361
'''
import urllib2
import re
import os
from scr.tool import Tool

class BDTB:
    def __init__(self):
#       'http://tieba.baidu.com/p/3138733512?see_lz=1&pn=1'  百度贴吧URL地址
        self.baseUrl = 'http://tieba.baidu.com/p/'
        self.seellz = '?see_lz=' #=1只看楼主 =0查看全部
        self.urlpn = '&pn=' #代表页码
        self.tool =Tool()
    
    #帖子的每一个回复内容写入文件中
    def writeTxt(self,strs,f):
        f.writelines(strs)
    
    #获取四个信息，用户名，内容，楼层，时间
    def decodePageContent(self,pagecontent):
        #获取四个信息，用户名d，内容，(),楼层，时间
#         pattern = re.compile('<div.class="d_author">.*?<ul class="p_author">.*?'+
#                              '<li class="d_name.*?<a.*?target="_blank">(.*?)</a>.*?'+
#                              '<div class="d_post_content_main.*?<div class="p_content ".*?<cc>.*?'+
#                              '<div.*?class="d_post_content j_d_post_content.*?>(.*?)'+
#                               '</div>.*?</cc>.*?'+
#                              '<div class="core_reply j_lzl_wrapper">.*?'+
#                              '<div class="core_reply_tail clearfix">.*?'+
#                              '<div class="post-tail-wrap">.*?<span class="j_jb_ele">.*?</span>'+
#                              '(.*?)'+
#                              '<span class="tail-info">(.*?)'+'[\u697c]'+'</span>.*?'+
#                              '<span class="tail-info">(.*?)</span>.*?</div>.*?'+
#                              '<ul class="p_props_tail props_appraise_wrap"></ul>',re.S)
        pattern = re.compile('<div.class="d_author">.*?<ul class="p_author">.*?'+
                             '<li class="d_name.*?<a.*?target="_blank">(.*?)</a>.*?'+
                             '<div class="d_post_content_main.*?<div class="p_content'+
                             ' ".*?<cc>.*?'+
                             '<div.*?class="d_post_content j_d_post_content.*?>(.*?)'+
                             '</div>.*?</cc>.*?'+
                             '<div class="core_reply j_lzl_wrapper">.*?'+
                             '<div class="core_reply_tail clearfix">.*?'+
                             '<div class="post-tail-wrap">'+
                             '(.*?)</div>',re.S)
#         pattern = re.compile('<div class="d_author">.*?<ul class="p_author">.*?'+
#                              '<li class="d_name".*?<a.*?'+
#                              'target="_blank">(.*?)</a>',re.S)
#         pattern = re.compile('<li class="d_name" data-field=".*?<a data-field=".*?'+
#                              'target="_blank">(.*?)</a>.*?</li>',re.S)
#         pattern = re.compile('<div class="d_author">(.*?)</div>',re.S)
        content = re.findall(pattern, pagecontent)
        print "len=",len(content)
        ls = []
        tail2 = re.compile('<span class="tail-info">(.*?)</span>.*?'+
                           '<span class="tail-info">(.*?)</span>', re.S)
        tail3 = re.compile('<span class="tail-info">.*?</span>.*?'+
                           '<span class="tail-info">(.*?)</span>.*?'+
                           '<span class="tail-info">(.*?)</span>',re.S)
        import sys;reload(sys);sys.setdefaultencoding('utf8');
        for item in content:
            n = re.subn('tail-info', 'tail', item[2])
            if n[1]==4:
                group3 = re.search(tail3, item[2])
                ls.append((item[0],item[1],group3.group(1),group3.group(2)))
            elif n[1]==3:
                group2 = re.search(tail2, item[2])
                ls.append((item[0],item[1],group2.group(1),group2.group(2)))
            else:
                print 'n error n=',n[1],'=='+item[2].decode('utf-8')
        return ls
    #获取帖子标题
    def decodeTieziTitle(self,pagecontent):
        pattern = re.compile('<h\d.*?class="core_title_txt.*?>(.*?)</h\d>',re.S)
        title = re.findall(pattern, pagecontent)
        return title[0]
    #获取页面回复数量和总页码
    def decodePageContentNum(self,pagecontent):
        patten = re.compile('<li class="l_reply_num".*?<span class="red".*?>(.*?)'+
                            '</span>.*?<span class="red".*?>(.*?)</span>',re.S)
        num =re.search(patten, pagecontent);
        return num
    #获取页面html文本内容
    def getPageContent(self,url):
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read().decode('UTF-8')
    def start(self):
        urlid = raw_input("输入贴吧帖子ID：").strip()
        see_lz = raw_input("是否只看楼主的帖子(是输入1，否输入0)：")
        sss = self.baseUrl+urlid+self.seellz+str(see_lz)+self.urlpn+str(1)
#         sss = 'http://tieba.baidu.com/p/3138733512?see_lz=0&pn=1'
        print 'url=',sss
        pagecontent = self.getPageContent(\
                sss)
        num = self.decodePageContentNum(pagecontent)
        print num.group(1),u'回复贴，共',num.group(2),u'页'
        self.pagenum = num.group(2)  #保存页码数量
        self.title = self.decodeTieziTitle(pagecontent)
        import sys;reload(sys);sys.setdefaultencoding('utf8');
        if see_lz==1:
            f = open(self.title+'-楼主.txt'.encode('utf-8'),'w+')
        else:
            f = open(self.title+'-全部.txt'.encode('utf-8'),'w+')
        self.writeTxt(num.group(1)+' post number,'+num.group(2)+'page number'+os.linesep,f)
        print u'帖子标题:%s' %self.title
        
        for i in range(int(self.pagenum)+1):#range函数不包括最大的值
            pagecontent = self.getPageContent(\
                self.baseUrl+urlid+self.seellz+str(see_lz)+self.urlpn+str(i))
            content = self.decodePageContent(pagecontent)
            picpattern = re.compile('<img class="BDE_Image" src="(.*?)".*?',re.S)
            #获取四个信息，用户名，内容，楼层，时间
            for con in content:
                print '*'*20
                strcon = '*'*20+os.linesep
                print u'楼层：',con[2]
                strcon += '楼层：'+con[2].encode('utf-8')+os.linesep
                print u'时间：',con[3]
                strcon += '时间：'+con[3].encode('utf-8')+os.linesep
                print u'用户名字：',con[0]
                strcon += '用户名字：'+con[0].encode('utf-8')+os.linesep
                li = re.findall(picpattern, con[1])
                if li is not None:
                    for l in li:
                        print u'内容图片：',l
                        strcon += '内容图片：'+l.encode('utf-8')+os.linesep
                print u'内容：',self.tool.replace(con[1])
                strcon += '内容：'+self.tool.replace(con[1]).encode('utf-8')+os.linesep
                self.writeTxt(strcon+os.linesep,f)
bdtb = BDTB()
bdtb.start()
