# encoding:utf-8
import requests as r
from base64 import b64encode as e
import sys,os,bua,threading,time
from PIL import Image,ImageDraw
import numpy as np
class thread_rec(threading.Thread):
    def __init__(self,d,n):threading.Thread.__init__(self);self.d,self.n=d,n
    def run(self):rec(self.d,self.n,1)
class thread_wi(threading.Thread):
    def __init__(self,d,n):threading.Thread.__init__(self);self.d,self.n=d,n
    def run(self):wi(self.d,self.n,1)
class thread_print_rec(threading.Thread):
    def __init__(self):threading.Thread.__init__(self)
    def run(self):
        global li,enp,cl
        while(enp==0):
            lt=li.copy()
            print("\033c", end="");print('活跃线程数：{}'.format(threading.activeCount()))
            for a in range(30):
                try:print('线程{}：正在执行第{}张'.format(a+1,lt[a]))
                except:print('线程{}：未运行'.format(a+1))
            try:print('目前位置：第{}/{}张'.format(int(np.asarray(lt).mean()),cl*2))
            except:pass
            time.sleep(0.1)
class thread_print_wi(threading.Thread):
    def __init__(self):threading.Thread.__init__(self)
    def run(self):
        global li,enp,cl
        while(enp==1):
            lt=li.copy()
            print("\033c", end="");print('活跃线程数：{}'.format(threading.activeCount()))
            for a in range(30):
                try:print('线程{}：正在执行第{}张'.format(a+1,lt[a]))
                except:print('线程{}：未运行'.format(a+1))
            try:print('目前位置：第{}/{}张'.format(int(np.asarray(lt).mean()),cl*2))
            except:pass
            time.sleep(0.1)
def spl(n,d,wh,r2,m):
    ex=os.path.exists('webcam split/{}.jpg'.format(n+m))
    if not ex:
        img=Image.open('Webcam/{}'.format(d))
        try:m2=bua.a(r2,img.size[0],0.012254902,0.2,0.4) if wh else img.size[0]/2
        except BaseException as e:
            if(isinstance(e,SystemExit)):print('程序退出');quit()
            elif(isinstance(e,BaseException)):error(e,'sql')
            m2=1632
        if not ex[0]:
            iml=img.crop((0,0,m2,img.size[1]))
            iml.save('webcam split/{}.jpg'.format(n+m))
            iml.close()
        if not ex[1]:
            imr=img.crop((m2,0,img.size[0],img.size[1]))
            imr.save('webcam split/{}.jpg'.format(n+1+m))
            imr.close()
        img.close()
        f=open('missing.txt','a');f.write('\n无文字内容：{}'.format(d));f.close()
def rec(d,n,mo):
    global li,m,k;li.append(n)
    try:
        ex,r2=os.path.exists('webcam recognize/{}.dict'.format(d[:-4])),False
        if not ex:
            f=open('Webcam/{}'.format(d),'rb')
            u=["{}rest/2.0/ocr/v1/accurate?access_token={}".format(m,k['access_token']),{"image":e(f.read()),'paragraph':'true','probability':'true'},{'content-type':'application/x-www-form-urlencoded'}]
            f.close()
            try:r2=r.post(u[0],data=u[1],headers=u[2])
            except:pass
        if r2 or ex:
            try:
                wr,lo,pt='words_result','location',['left','top','width','height']
                if not ex:
                    r2=r2.json()
                    f=open('webcam recognize/{}.dict'.format(d[:-4]),'w+');f.write(repr(r2));f.close()
                else:
                    f=open('webcam recognize/{}.dict'.format(d[:-4]),'r');r2=eval(f.read());f.close()
                if not wr in r2:raise KeyboardInterrupt
                if(r2[wr]==[]):raise KeyboardInterrupt
                if not os.path.exists('webcam loss/{}'.format(d)):
                    img=Image.open('Webcam/{}'.format(d))
                    img.convert('RGBA')
                    im=img.copy()
                    for f in r2[wr]:
                        pil=Image.new('RGBA',(f[lo][pt[2]],f[lo][pt[3]]),'#00BFFF')
                        dr=ImageDraw.Draw(pil)
                        dr.rectangle((3,3,f[lo][pt[2]]-4,f[lo][pt[3]]-3),fill='#87CEEB')
                        pil.putalpha(128)
                        im.paste(pil,(f[lo][pt[0]],f[lo][pt[1]]),mask=pil.split()[3])
                        pil.close()
                    im.save('webcam loss/{}'.format(d))
                    img.close();im.close()
                #spl(n,d,True,r2,mo)
            except BaseException as e2:
                if(isinstance(e2,KeyboardInterrupt)):pass
                    #spl(n,d,False,r2,mo)
                elif(isinstance(e2,SystemExit)):print('程序退出');quit()
                elif(isinstance(e2,BaseException)):error(e2,'rec')
    except BaseException as e2:
        if(isinstance(e2,SystemExit)):quit()
        elif(isinstance(e2,BaseException)):error(e2,'rec all')
    li.remove(n)
def wi(d,n,m):
    try:
        global li;li.append(n)
        img=Image.open('webcam split/{}.jpg'.format(str(n+m)))
        if not(img.size[0]==d.size[0]):
            a=d.copy()
            a.paste(img,((d.size[0]-img.size[0])//2,0))
            a.save('webcam split/{}.jpg'.format(str(n+m)))
            a.close();del a
        img.close();del img
        li.remove(n)
    except BaseException as e2:
        if(isinstance(e2,SystemExit)):print('程序退出');quit()
        elif(isinstance(e2,BaseException)):error(e2,'wi')
def main():
    try:
        print("\033c", end="")
        print('正在获取access token...')
        global m,k;m='https://aip.baidubce.com/'
        r1=r.get('{}oauth/2.0/token?grant_type=client_credentials&client_id=[CI]&client_secret=[CS]'.format(m))
        if r1:
            k=r1.json()
            if 'error' in k:print('ERROR  ',k['error'],':',k['error_description'])
            elif 'access_token' in k:
                print('获取成功，开始识别');global li,enp,cl
                c,n,li=[a[4:] for a in os.popen('cd Webcam;tree').read().split('\n')[:-2][1:]],-1,[]
                cl,ti,enp=len(c),0,0#enp用数字防止多线程输出
                thread_print_rec().start()#这里将输出线程与主线程分离开来，以加快速度
                while(True):#在线程内容文本显示上，更新太快，并且并行的结果就是看不见状态
                    if(threading.activeCount()<32):#三倍的并发能力，原来QPS是3，现在可以到9
                        n+=2
                        print(int((n+1)/2),cl)
                        if(int((n+1)/2)<=cl):thread_rec(c[int((n-1)/2)],n).start()#每当有线程结束时，都会立即被分配一个新的项目
                        elif(threading.activeCount()==2):break#这说明print进程和主进程的存在
            else:print('请在运行前修改此文件中的[CI]和[CS]为相应的百度云Client ID和Client Secret，我不想有人拿这个帐号的CI和CS去干些不可告人的事情。')
    except BaseException as e2:
        if(isinstance(e2,SystemExit)):print('程序退出');quit()
        elif(isinstance(e2,BaseException)):error(e2,'main')
def error(e2,pre):
    er='error.txt';aft='{}发生错误：{}'.format(pre,repr(e2))
    if(os.path.exists(er)):f=open(er,'a');f.write('\n{}'.format(aft));f.close()
    else:f=open(er,'w+');f.write(aft);f.close()
    del f,er,e2
if __name__ == '__main__':main()
