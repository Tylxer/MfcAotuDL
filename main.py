# -*- coding: utf-8 -*-
import json
import requests
import os
import time
import urllib
import queue
import threading
import platform
import datetime
from requests.adapters import HTTPAdapter

def geturl(url,num,file):
    downurl = queue.Queue()
    res = request_get(url)
    savenum = []
    if res.status_code == 200:
        temp = res.text.splitlines()
        temp = dels(temp)
        for i in temp:
            currentnum = findnum(i)
            if currentnum > num:
                k = url[0:url.rfind('/') + 1] + i               
                downurl.put(k)
                savenum.append(currentnum)
        print(savenum)
        return downurl,savenum
    else:
        print(url+'m3u8列表已经失效,错误代码'+str(res.status_code))
        return None,savenum

def dels(list):
    b = list[:]
    for i in list:
        if '#'in i:
            b.remove(i)
    list = b
    return list

def maindown(url):
    print('准备下载')
    #获取本地目录
    #清空或删除filetext文件
    savenum = [0]
    sleepnum = 0
    file = path 
    while True:
        tempnum = []
        downurl,tempnum = geturl(url,max(savenum),file)  
        if downurl != None:
            if not downurl.empty():     
                savenum = savenum + tempnum
                print('开始下载')
                sleepnum = 0
                start = datetime.datetime.now()
                size = downurl.qsize()
                for l in range(2):
                    d = download(downurl,file)
                    d.start()
                end = datetime.datetime.now()
                print('平均耗时: '+ str((end-start).seconds/size))
            else:
                if sleepnum == 5:
                    print('TS下载完成')
                    break
                else:
                    sleepnum  = sleepnum + 1
                    time.sleep(3)
        else:
            print('无下载文件')
            break
        
    #cmd = 'ffmegp  -f concat -i filelist.txt -vcodec copy -acodec copy output.mp4'
    #result = subprocess.Popen(cmd)
    #print(result)



class download(threading.Thread):#下载程序
    def __init__(self,que,file):
        threading.Thread.__init__(self)
        self.que = que
        self.file = file
    def run(self):
        while True:
            if not self.que.empty():
                url = self.que.get()
                r = request_get(url)
                if r.status_code == 200:
                    with open(self.file + str(findnum(url))  + '.ts','wb') as a:
                        a.write(r.content)
                    print('已下载' + str(findnum(url)))
                else:
                    print(str(findnum(url)) + '下载失败错误代码'+str(r.status_code))
            else:
                time.sleep(2)
                break


def findnum(url):#获取TS链接的序号num
    start = url.rfind('_') + 1
    end = url.rfind('.ts')
    num = url[start:end]
    num = int(num)
    return num

def request_get(url):
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=4))
    s.mount('https://', HTTPAdapter(max_retries=4))
    r = s.get(url)
    return r
    

if __name__ == '__main__':
    sys = platform.system()
    if sys == "Windows":
        path = 'e:/temp/'
    else:
        path = '/root/temp/'
    ol_url = queue.Queue()
    url1 = input('输入url:')
    url2 = input('输入url:')
    ol_url.put(url1)
    ol_url.put(url2)
    threads = []
    for i in range(2):
        d = threading.Thread(target=maindown,args = [ol_url.get()])
        threads.append(d)
    for d in threads:
        d.start()

    
