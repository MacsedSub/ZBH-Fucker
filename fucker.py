import threading # 多线程模块
import queue # 队列模块
import requests
import time
import random
import json
import os
import re
import traceback
from urllib.parse import quote
from config import fakeVisitorCount
from config import startUserID
from config import spreadToken
from config import UAs
from config import province
from config import city
from config import scode

class ProtectThread(threading.Thread):

    def __init__(self,num):
        threading.Thread.__init__(self,name = 'pro' + str(num))
        self.num = num
        self.setName('pro' + str(num))
   
    def run(self):
        print('守护进程' + str(self.num) +'已启动')
        initThreadsName = ['IP']
        for i in range(1,fakeVisitorCount):
            initThreadsName.append(str(i))
        while True:
        
            print('守护进程' + str(self.num) + '正在进行守护')
        
            nowThreadsName=[]#用来保存当前线程名称
            now=threading.enumerate()#获取当前线程名
            for i in now:
                nowThreadsName.append(i.getName())#保存当前线程名称
            
            for ip in initThreadsName:
                if  ip in nowThreadsName:
                    pass #当前某线程名包含在初始化线程组中，可以认为线程仍在运行
                else:
                    
                    if ip == 'IP':
                        print ('==='+ 'IPGeter不在线，正在重新启动' + '===')
                        IPThread = IPGeter(IPList,UserIDList,currentUserID)
                        IPThread.start()
                        IPThread.join()
                    
                    elif ip == 'pro1':
                        print ('==='+ '保护进程1不在线，正在重新启动' + '===')
                        protectT = ProtectThread(1)
                        protectT.start()
                        ProtectTs.append(protectT)
                        protectT.join()
                    elif ip == 'pro2':
                        print ('==='+ '保护进程2不在线，正在重新启动' + '===')
                        protectT = ProtectThread(2)
                        protectT.start()
                        ProtectTs.append(protectT)
                        protectT.join()
                    elif ip != 'MainThread':
                        print ('==='+ 'FakeVisitor进程'+ ip + ' 不在线，正在重新启动' + '===')
                        VisitorT = FakeVisitor(int(ip),IPList,UserIDList)
                        VisitorT.start()
                        VisitorTs.append(VisitorT)
                        VisitorT.join()
                
            time.sleep(1)#隔一段时间重新运行，检测有没有线程down

class IPGeter(threading.Thread):  # 解析线程类
 # 初始化属性
    def __init__(self,ips,users,currentUserID):
        threading.Thread.__init__(self,name = 'IP')
        self.ips=ips
        self.users = users
        self.currentUserID = currentUserID
        self.setName('IP')
    def run(self):
        print('启动IP获取者')
        # 无限循环，
        while True:
        
            if len(self.ips) == 0 or len(self.users) == 0:
            
                if len(self.ips) == 0:
                    print('IP池耗尽，正在获取新的代理')
                    
                    url = 'http://www.66ip.cn/nmtq.php?getnum=20&isp=0&anonymoustype=4&start=&ports=&export=&ipaddress=&area=0&proxytype=0&api=66ip'
                    
                    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
                    
                    ip_port_format = '[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}:[0-9]{1,5}'
                    try:
                        response = requests.get(url,headers=headers)
                        
                    except requests.ConnectionError as e:
                        print('IP代理请求异常，稍后会重试，若一直异常，请检查你的代理设置 WARNING：该请求不可通过终端socks5代理发送')
                    else:

                        if response.status_code == 200:
                        
                            rawData = response.content.decode('gbk')
                            proxyAll = re.findall(ip_port_format,rawData)
                            
                            for ip in proxyAll:
                                self.ips.append(ip)
                            print('获取代理成功')
                        else:
                            print('获取代理请求错误状态码：' + str(response.status_code))
                            print('获取代理失败，1秒后重试')
                    
                        
                if len(self.users) == 0:
                    print('用户ID耗尽，正在获取新的用户ID')
                    for i in range(0,fakeVisitorCount):
                        self.users.append(self.currentUserID + i)
                    
                    self.currentUserID = self.currentUserID + fakeVisitorCount
                    print('用户ID获取成功')
                
            else:
                time.sleep(1)
        
        print('IP获取者退出')

class FakeVisitor(threading.Thread):

    def __init__(self,num,ips,users):
        threading.Thread.__init__(self,name = str(num))
        self.ips=ips
        self.users = users
        self.num = num
        self.setName(str(num))
    
    def run(self):
        print('FakeVisitor ' + str(self.num) + '已启动')
        
        global successCount
        
        while True:
        
            if len(self.ips) == 0 or len(self.users) == 0:
                print('FakeVisitor ' + str(self.num) + '暂无可用IP/用户ID 1秒后重新获取')
                time.sleep(1)
            else:
                ip = self.ips[0]
                del self.ips[0]
                user = self.users[0]
                del self.users[0]
                
                proxies = {'http':'http://' + ip , 'https' : 'https://' + ip}
                
                url = 'http://admin.zhinengdayi.com/front/spread/bindUserAndSpread?frontUserId='+str(user)+'&spreadToken='+spreadToken
                
                headers = {'User-Agent': random.sample(UAs,1)[0]}
                
                try:
                    response = requests.get(url,headers = headers,proxies = proxies)
                except requests.ConnectionError as e:
                    print('ID:' + str(user) + ' 绑定ID-Token请求异常，将会更换IP&ID重试')
                else:

                    if response.status_code == 200:
                    
                        recordCount = 0
                        
                        url = 'http://admin.zhinengdayi.com/weixin/api/user/addUserViewLog?userId='+ str(user) +'&userProvince='+ quote(province) +'&userCity='+ quote(city) +'&sCode='+ scode + '&infoId=&majorId=&viewSourceUrl=&pageUrl=http%3A%2F%2Fweixin.zhinengdayi.com%2Fbuild%2Findex.html%3Fscode%3D'+ scode +'%23%2F%3Fuid%3D'+ str(user) +'%26spreadToken%3D' + spreadToken
                        
                        headers = {'User-Agent': random.sample(UAs,1)[0]}
                        
                        for i in range(1,6):
                        
                            print('ID:' + str(user) + ' 正在进行第' + str(i) + '次增加访问记录请求')
                        
                            try:
                                response = requests.get(url,headers = headers,proxies = proxies)
                            except requests.ConnectionError as e:
                                print('ID:' + str(user) + ' 的第' + str(i) + '次增加访问记录请求异常，将会重试')
                            else:
                        
                                if response.status_code == 200:
                                    recordCount = recordCount + 1
                        
                            time.sleep(random.randint(2,5))
                    
                        if recordCount >= 4:
                            
                            lock.acquire()
                            successCount = successCount + 1
                            print('成功增加一个有效用户，总共已完成' + str(successCount) + '个,ID是' + str(user))
                            lock.release()
                    
                        else:
                            print(str(user) + '的访问请求失败，将会更换ID重试')
                    
                time.sleep(random.randint(1,3))
    
    


IPList = []
UserIDList = []
VisitorTs = []
ProtectTs = []
currentUserID = startUserID
successCount = 0
lock = threading.Lock()

IPThread = IPGeter(IPList,UserIDList,currentUserID)

IPThread.start()

for i in range(1,fakeVisitorCount):
    VisitorT = FakeVisitor(i,IPList,UserIDList)
    VisitorT.start()
    VisitorTs.append(VisitorT)

for i in range(1,2):
    protectT = ProtectThread(i)
    protectT.start()
    ProtectTs.append(protectT)


IPThread.join()

for VisitorT in VisitorTs:
    VisitorT.join()

for protectT in ProtectTs:
    protectT.join()
