#version:1.0
#Copyright 2021  github.com/bilibili12433014
#originally made by:
#bilibili user:明媚的山岚
#uid:12433014
#e-mail:bilibili12433014@qq.com
#qq群:676475241

print('''version:1.0
使用说明：
软件支持自动打开扫雷(win7)
支持F6重启
支持空格键快速关闭
支持失败自动重启
支持胜利后自动重启
不支持在游戏过程中手动重置，请使用F6
不支持移动或放大游戏窗口，请放大或移动后F6重启软件
不支持识别数字8
只支持最基本的推理
有任何建议或疑问请加QQ群

originally made by:
bilibili user:明媚的山岚
uid:12433014
e-mail:bilibili12433014@qq.com
qq群:676475241
如果喜欢的话，关注我吧！
github:https://github.com/bilibili12433014/minesweeper-helper
up主主页：https://space.bilibili.com/12433014
（已复制到粘贴板,软件运行时按F12可快捷打开）
''')

from time import sleep
pos_a=(0,0)
pos_b=(0,0)
ele_len=0
block=[]
x_rate=1561/1732
y_rate=834/1013
from ctypes import *
import numpy as np
import win32gui, win32ui, win32con, win32api,time,os,cv2,threading
os.system('echo ' + "https://space.bilibili.com/12433014" + '| clip')
os.startfile("C:\\Program Files\\Microsoft Games\\Minesweeper\\MineSweeper.exe")
def open_page():
    while True:
        sleep(0.05)
        while not (win32api.GetKeyState(win32con.VK_F12)==1 or win32api.GetKeyState(win32con.VK_F12)==0):
            os.system('start ' + "https://space.bilibili.com/12433014")
            while not (win32api.GetKeyState(win32con.VK_F12)==1 or win32api.GetKeyState(win32con.VK_F12)==0):
                sleep(0.5)

threading.Thread(target=open_page,args=()).start()
sleep(1)
x_long=30
y_long=16
def window_capture(filename):
    
    aa,bb=win32api.GetCursorPos()
    #win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
    #win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP,0,0)
    win32api.SetCursorPos((0,0))
    sleep(0.005)
    hwnd = 0  # 窗口的编号，0号表示当前活跃窗口
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取监控器信息
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    # print w,h　　　#图片大小
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    hh=True
    while hh:
        try:
            saveBitMap.SaveBitmapFile(saveDC, filename)
            hh=False
        except:
            sleep(0.05)
    win32api.SetCursorPos((aa,bb))
class ele:
    def __init__(self,x,y):
        self.pos=(x,y)
        self.center_pos=(int(pos_a[0]+x*ele_len-0.5*ele_len),
                    int(pos_a[1]+y*ele_len-0.5*ele_len))
        #print((self.center_pos[0],self.center_pos[1]))
        threading.Thread(target=self.init_color,args=()).start()
        #self.start_color=self.get_color(self.center_pos[0],self.center_pos[1])
        self.have=-2
        self.opened=False
        self.bomb=False
        self.clear=False
        if x==0 or y==0 or x==x_long+1 or y==y_long+1:
            self.opened=True
    def init_color(self):
        self.start_color=self.get_color(self.center_pos[0],self.center_pos[1])
    def get_color(self,x, y):
        global img
        (b,g,r)=img[y,x]
        return (b,g,r)
        #gdi32 = windll.gdi32
        #user32 = windll.user32
        #hdc = windll.user32.GetDC(None)
        # 获取颜色值
        #pixel = windll.gdi32.GetPixel(windll.user32.GetDC(None), x, y)  
        # 提取RGB值
        #r = pixel & 0x0000ff
        #g = (pixel & 0x00ff00) >> 8
        #b = pixel >> 16
        #return [r, g, b]
    def open(self):
        self.click(self.center_pos)
        #self.flash()
    def set_bomb(self):
        self.bomb=True
        self.opened=True
        win32api.SetCursorPos(self.center_pos)
        sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
        sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
        sleep(0.01)
    def middle(self):
        win32api.SetCursorPos(self.center_pos)
        sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN,0,0)
        sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP,0,0)
        sleep(0.01)
    def click(self):
        win32api.SetCursorPos(self.center_pos)
        sleep(0.05)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0) #鼠标左键按下
        sleep(0.05)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0) #鼠标左键拾起
        sleep(0.1)
    def set_have(self):
        br=False
        '''
        if br==False:
            for i in range(-5,5):
                for ii in range(-5,5):
                    if abs(color[0]-3)+abs(color[1]-1)+abs(color[2]-252)<5:
                        self.opened=True
                        self.bomb=True
                    if not br==False:
                        break
                if not br==False:
                    break
        if br==False:
            for i in range(-5,5):
                for ii in range(-5,5):
                    if abs(color[0]-190)+abs(color[1]-80)+abs(color[2]-64)<30:
                        self.have=1
                        br=True
                    if not br==False:
                        break
                if not br==False:
                    break
        if br==False:
            for i in range(-5,5):
                for ii in range(-5,5):
                    if abs(color[0]-190)+abs(color[1]-80)+abs(color[2]-64)<30:
                        self.have=1
                        br=True
                    if not br==False:
                        break
                if not br==False:
                    break#'''
        #'''
        color_mount=[0,0,0,0,0,0,0,0,0,0]
        for i in range(-5,5):
            for ii in range(-5,5):
                color=self.get_color(self.center_pos[0]+i,self.center_pos[1]+ii)
                if abs(color[0]-3)+abs(color[1]-1)+abs(color[2]-252)<5:
                    self.opened=True
                    self.bomb=True
                    br=not False
                elif abs(color[0]-193)+abs(color[1]-86)+abs(color[2]-68)<30:
                    color_mount[1]=color_mount[1]+1
                elif abs(color[0]-16)+abs(color[1]-110)+abs(color[2]-39)<30:
                    color_mount[2]=color_mount[2]+1
                elif abs(color[0]-7)+abs(color[1]-5)+abs(color[2]-172)<30:
                    color_mount[3]=color_mount[3]+1
                elif abs(color[0]-132)+abs(color[1]-0)+abs(color[2]-1)<30:
                    color_mount[4]=color_mount[4]+1
                elif abs(color[0]-2)+abs(color[1]-0)+abs(color[2]-124)<15:
                    color_mount[5]=color_mount[5]+1
                elif abs(color[0]-126)+abs(color[1]-123)+abs(color[2]-4)<15:
                    color_mount[6]=color_mount[6]+1
                elif abs(color[0]-24)+abs(color[1]-23)+abs(color[2]-168)<5:
                    color_mount[7]=color_mount[7]+1
                else:
                    color_mount[0]=color_mount[0]+1
                if not br==False:
                    break
            if not br==False:
                break
        if not br==True:
            i=8
            for ii in range(1,8):
                if color_mount[i]<color_mount[ii]:
                    i=ii
            self.have=i
        if self.have==8:
            self.have=0
        #print(str(color_mount)+str(self
        #'''
        '''for i in range(-5,5):
            for ii in range(-5,5):
                color=self.get_color(self.center_pos[0]+i,self.center_pos[1]+ii)
                if abs(color[0]-3)+abs(color[1]-1)+abs(color[2]-252)<5:
                    self.opened=True
                    self.bomb=True
                elif abs(color[0]-190)+abs(color[1]-80)+abs(color[2]-64)<30:
                    self.have=1
                    br=True
                elif abs(color[0]-193)+abs(color[1]-86)+abs(color[2]-68)<30:
                    self.have=1
                    br=True
                elif abs(color[0]-16)+abs(color[1]-110)+abs(color[2]-39)<30:
                    self.have=2
                    br=True
                elif abs(color[0]-7)+abs(color[1]-5)+abs(color[2]-172)<30:
                    self.have=3
                    br=True
                elif abs(color[0]-132)+abs(color[1]-0)+abs(color[2]-1)<30:
                    self.have=4rn
                    br=True
                elif abs(color[0]-2)+abs(color[1]-0)+abs(color[2]-124)<15:
                    self.have=5
                    br=True
                elif abs(color[0]-126)+abs(color[1]-123)+abs(color[2]-4)<15:
                    self.have=6
                    br=True
                elif abs(color[0]-24)+abs(color[1]-23)+abs(color[2]-168)<5:
                    self.have=7
                    br=True
                else:
                    self.have=0
                if not br==False:
                    break
            if not br==False:
                break#'''
        self.opened=True
        if self.have==0:
            self.clear=True
        else:
            global operate_list
            operate_list.append(self.pos)
    def flash(self):
        #global gdi32,user32,hdc
        #gdi32 = windll.gdi32
        #user32 = windll.user32
        #hdc = user32.GetDC(None)
        #hdc = windll.user32.GetDC(None)
        window_capture("haha.jpg")
        global img
        img=cv2.imread("haha.jpg")
        for x in range(1,x_long+1):
            for y in range(1,y_long+1):
                if block[x][y].opened==False and block[x][y].bomb==False:
                    threading.Thread(target=block[x][y].check_color,args=()).start()
                    #block[x][y].check_color()
    def check_color(self):
        if(not self.start_color==self.get_color(self.center_pos[0],self.center_pos[1])):
            self.set_have()
    def operate(self):
        global doing
        i=self.have
        i_b=0
        i_n=[]
        i_o=0
        near=[(self.pos[0]-1,self.pos[1]-1),
              (self.pos[0]-1,self.pos[1]),
              (self.pos[0],self.pos[1]-1),
              (self.pos[0]-1,self.pos[1]+1),
              (self.pos[0]+1,self.pos[1]+1),
              (self.pos[0]+1,self.pos[1]),
              (self.pos[0],self.pos[1]+1),
              (self.pos[0]+1,self.pos[1]-1)]
        for ii in near:
            try:
                if block[ii[0]][ii[1]].opened:
                    i_o=i_o+1
                    if block[ii[0]][ii[1]].bomb:
                        i_b=i_b+1
                else:
                    i_n.append(ii)
            except:
                print(ii)
        if i_o==8:
            return
        if i_b==i:
            self.middle()
            self.clear=True
            doing=1
        if i-len(i_n)-i_b==0:
            doing=1
            for iii in i_n:
                block[iii[0]][iii[1]].set_bomb()
        #self.flash()
        #if i-i_b==1 and len(i_n)==1:
        #    block[i_n[0][0]][i_n[0][1]].set_bomb()
        #    doing=1
        #if i-i_b==0:
        #    for iii in near:
        #        if block[iii[0]][iii[1]].opened==False and block[iii[0]][iii[1]].bomb==False:
        #            block[iii[0]][iii[1]].click()
        #            doing=1
        #    self.clear=True
def get_pos():
    global pos_a,ele_len,pos_b
    while win32gui.FindWindow("Minesweeper",u"扫雷")==0:
        sleep(0.5)
    hld=win32gui.FindWindow("Minesweeper",u"扫雷")
    hld=win32gui.FindWindowEx(hld,None, "Static",None)
    a,b,c,d=win32gui.GetWindowRect(hld)
    print(win32gui.GetWindowRect(hld))
    pos_a=(a+0.5*(c-a)*(1-x_rate),b+0.5*(d-b)*(1-y_rate))
    pos_b=(c,d)
    ele_len=((c-a)/x_long*x_rate+(d-b)/y_long*y_rate)/2
    print(pos_a)
    #print(pos_b)
    print(ele_len)


get_pos()
win32api.SetCursorPos((pos_b[0]-5,pos_b[1]-5))
sleep(0.1)
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0) #鼠标左键按下
sleep(0.1)
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0) #鼠标左键拾起
sleep(0.2)
win32api.keybd_event(82,0)
sleep(0.05)
win32api.keybd_event(82,0,win32con.KEYEVENTF_KEYUP)
sleep(0.1)
win32api.keybd_event(win32con.VK_F2,0)
sleep(0.05)
win32api.keybd_event(win32con.VK_F2,0,win32con.KEYEVENTF_KEYUP)
sleep(0.1)
win32api.keybd_event(78,0)
sleep(0.05)
win32api.keybd_event(78,0,win32con.KEYEVENTF_KEYUP)
sleep(0.1)
win32api.SetCursorPos((0,0))
sleep(0.1)
window_capture("haha.jpg")
img=cv2.imread("haha.jpg")
for x in range(0,x_long+2):
    i=[]
    for y in range(0,y_long+2):
        i.append(ele(x,y))
    block.append(i)

def print_color():
    for x in range(1,x_long+1):
        for y in range(1,y_long+1):
            print((x,y),end="")
            print(block[x][y].center_pos,end="")
            print(block[x][y].start_color)
        print("")
def pos():
    for x in range(1,x_long+1):
        for y in range(1,y_long+1):
            sleep(0.1)
            win32api.SetCursorPos(block[x][y].center_pos)
def show_color():
    aa,bb=win32api.GetCursorPos()
    sleep(0.05)
    win32api.SetCursorPos((0,0))
    sleep(0.05)
    window_capture("haha.jpg")
    img=cv2.imread("haha.jpg")
    print(img[bb,aa])
    win32api.SetCursorPos((aa,bb))
def show_state():
    for y in range(1,y_long+1):
        for x in range(1,x_long+1):
            if block[x][y].opened:
                if block[x][y].have==0:
                    print("  ",end="")
                elif block[x][y].bomb:
                    print(" X",end="")
                else:
                    print(" ",end="")
                    print(block[x][y].have,end="")
            else:
                print(" 0",end="")
        print("")
import os
operate_list=[]
def force_close():
    while True:
        sleep(0.5)
        if not (win32api.GetKeyState(win32con.VK_SPACE)==1 or win32api.GetKeyState(win32con.VK_SPACE)==0):
            os.system("taskkill /f /pid MineSweeper.exe")
            os._exit(0)
            os.system("taskkill /f /pid py.exe")
            os.system("taskkill /f /pid python.exe")
            os.system("taskkill /f /pid pyw.exe")
            os.system("taskkill /f /pid pythonw.exe")
            exit(0)

threading.Thread(target=force_close,args=()).start()
def start():
    global operate_list
    global doing
    doing=1
    while True:
        doing=1
        while doing:
            doing=0
            block[int(0.5*x_long)][int(0.5*y_long)].flash()
            print("-----------------------------------------------------")
            show_state()
            for i in range(0,len(operate_list)):
                if i>=len(operate_list):
                    break
                x=operate_list[i][0]
                y=operate_list[i][1]
                if block[x][y].clear==True:
                    operate_list.pop(i)
                    doing=1
                else:
                    block[x][y].operate()
        print("-----------------------------------------------------")
        show_state()
        print("None")
        while (win32api.GetKeyState(1)==1 or win32api.GetKeyState(1)==0) and (win32api.GetKeyState(2)==1 or win32api.GetKeyState(2)==0):
            sleep(0.01)
        while not((win32api.GetKeyState(1)==1 or win32api.GetKeyState(1)==0) and (win32api.GetKeyState(2)==1 or win32api.GetKeyState(2)==0)):
            sleep(0.01)
        '''for i in range(20):
            if (win32api.GetKeyState(win32con.VK_F6)==1 or win32api.GetKeyState(win32con.VK_F6)==0):
                sleep(0.25)'''
                
        '''for x in range(1,31):
            for y in range(1,17):
                if block[x][y].clear==False and block[x][y].opened:
                    block[x][y].operate()'''
#start()
def win():
    while True:
        sleep(1)
        hld=win32gui.FindWindow("#32770",u"游戏胜利")
        if not hld==0:
            while win32gui.FindWindow("#32770",u"游戏胜利"):
                sleep(0.5)
            #a,b,c,d=win32gui.GetWindowRect(hld)
            try:
                os.system("start 扫雷.py")
            except:
                os.system("start 扫雷.exe")
            os._exit(0)
        else:
            hld=win32gui.FindWindow("#32770",u"游戏失败")
            if not hld==0:
                try:
                    os.system("start 扫雷.py")
                except:
                    os.system("start 扫雷.exe")
                os._exit(0)
        #hld=win32gui.FindWindowEx(hld,None, "Static",None)
threading.Thread(target=win,args=()).start()
def re_start():
    while True:
        sleep(0.01)
        if not (win32api.GetKeyState(win32con.VK_F6)==1 or win32api.GetKeyState(win32con.VK_F6)==0):
            try:
                os.system("start 扫雷.py")
            except:
                os.system("start 扫雷.exe")
            os._exit(0)
win32api.SetCursorPos(block[int(0.5*x_long)][int(0.5*y_long)].center_pos)
while (win32api.GetKeyState(1)==1 or win32api.GetKeyState(1)==0) and (win32api.GetKeyState(2)==1 or win32api.GetKeyState(2)==0):
    sleep(0.01)
while not((win32api.GetKeyState(1)==1 or win32api.GetKeyState(1)==0) and (win32api.GetKeyState(2)==1 or win32api.GetKeyState(2)==0)):
    sleep(0.01)
block[int(0.5*x_long)][int(0.5*y_long)].flash()
sleep(0.2)
show_state()
if (win32api.GetKeyState(win32con.VK_F6)==1 or win32api.GetKeyState(win32con.VK_F6)==0):
    threading.Thread(target=start,args=()).start()
else:
    print("debug模式启动，轻松开F6")
sleep(3)
threading.Thread(target=re_start,args=()).start()
