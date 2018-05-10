# -*- coding: utf-8 -*-
from Tkinter import *
from tkinter import ttk
import subprocess,os
import time
import base64



conpath=os.getcwd()
confile=conpath+r"\conf.ini"
if not os.path.isfile(confile):
    try:
        file = open(confile, 'w')
    finally:
        if file:
            file.close()

bgpic=conpath+r'\pic\login.gif'
if not os.path.isfile(bgpic):
    os._exit(1)

logo=conpath+r'\pic\users.ico'
if not os.path.isfile(logo):
    logo=""

class Logon ():
    def __init__(self,root):
        self.filename = bgpic
        self.photo = PhotoImage(file=self.filename)
        self.lab0 = Label(root,image=self.photo)
        self.lab0.grid()


        self.lab1 = Label(root)
        self.lab1.place(x=10,y=320)

        self.ent1 = Entry(root,borderwidth = 2)
        self.ent1.place(x=70,y=152)
        self.ent2 = Entry(root, show="*",borderwidth =2)
        self.ent2.place(x=70,y=180)
        self.ent3 = Entry(root,borderwidth = 2)
        self.ent3.place(x=70,y=208)
        self.ent4 = Entry(root,borderwidth = 2)
        self.ent4.place(x=70,y=235)

        self.button1 = Button(root,width=20,bg="LightSteelBlue",text="提          交  ",command=self.Submit)
        self.button1.place(x=68,y=280)


        self.box = ttk.Combobox(width=25)
        self.box.place(x=300,y=152)

        self.button2 = Button(root, bg="LightSteelBlue", text="手动加载", command=self.loadconf, width=27)
        self.button2.place(x=300, y=250)

        self.button3 = Button(root,bg="LightSteelBlue", text="删      　   除",command=self.delshare,width=27)
        self.button3.place(x=300,y=280)

        self.loadconf()


    def Submit(self):
        self.lab1["text"] = ""
        user = self.ent1.get().encode('gbk')
        password = self.ent2.get()
        encryp_pass=base64.encodestring(password)
        ip = self.ent3.get()
        share = self.ent4.get().encode('gbk')
        if not user or not password or not ip or not share:
            self.lab1["text"] = "信息不能为空"
            return 1
        cmd_add = "net use * \\\\"+ip+"\\"+share+" "+password+" /user:"+user
        exe_result=subprocess.Popen(cmd_add, shell=True)
        t=0
        self.lab1["text"] = str(exe_result.pid)
        while (t<4) and (exe_result.poll() is None):
            t+=1;
            time.sleep(1);
        if exe_result.poll()==0:
            self.putbox()
            with open(confile, 'a') as f:
                f.write(user+"##"+encryp_pass.strip()+"##"+ip+"##"+share+'\n')
                self.lab1["text"] = "登录成功"
        else:
            self.lab1["text"] = "登录失败"
            exe_result.kill()
        self.ent2.delete(0,len(password))


    def delshare(self):
        self.lab1["text"] = ""
        if self.box.get()!="None":
            device = self.box.get().split()[0]
            path = self.box.get().split()[1]
            ip =path.split('\\')[2]
            share =path.split('\\')[3]
            cmd_del = "net use "+device+" /del "
            exe_result = subprocess.call(cmd_del,shell=True)
            if exe_result == 0:
                self.putbox()
                with open(confile, "r") as f:
                    lines = f.readlines()
                with open(confile, "w") as f_w:
                    for line in lines:
                        if ip in line.decode('gbk') and share in line.decode('gbk'):
                            continue
                        f_w.write(line)

                self.lab1["text"] = "删除成功"
            else:
                self.lab1["text"] = "删除失败"
                pass


    def putbox(self):
        diskinfo = self.getshare()
        disklist = []
        if len(diskinfo) > 0:
            for each in diskinfo:
                disklist.append(each['driver']+" "+each['path'])
        else:
            disklist.append("None")
        self.box['values'] = disklist
        self.box.current(0)


    def loadconf(self):
        diskinfo = self.getshare()
        with open(confile, 'r') as f1:
            for lines in f1.readlines():
                line =lines.rstrip('\n')
                num =0
                if len(line.split('##')) !=4:
                    continue
                user=line.split('##')[0]
                encryp_pass=line.split('##')[1]
                password=base64.decodestring(encryp_pass)
                ip=line.split('##')[2]
                share=line.split('##')[3]
                if len(diskinfo) > 0:
                    for each in diskinfo:
                        if len(each['path'].split('\\')) ==4:
                            exsit_ip = each['path'].split('\\')[2]
                            exsit_share = each['path'].split('\\')[3]
                            if share.decode('gbk').encode('utf-8') ==exsit_share and ip == exsit_ip:
                                num=1
                if num ==0:
                    cmd_add = r"net use * \\" + ip + "\\" + share + " " + password + " /user:" + user
                    exe_result = subprocess.Popen(cmd_add, shell=True)
                    t = 0
                    while (t < 2) and (exe_result.poll() is None):
                        t += 1;
                        time.sleep(1);
                    exe_result.kill()
        self.lab1["text"] = "加载完成"
        self.putbox()

    def getshare(self):
        cmd_get = "net use"
        cmd_result=os.popen(cmd_get).read().decode('gbk').encode('utf-8')
        share_list=[]
        for line in cmd_result.split('\n'):
            eachline=line.split()
            if len(eachline) == 6 and eachline[3]=="Microsoft":
                share = {'driver':eachline[1],'status':eachline[0],'path':eachline[2]}
                share_list.append(share)
        result = share_list
        return result



root = Tk()
root.title("共享登录")
root.iconbitmap(logo)
#窗口大小
width ,height= 520, 350
#窗口居中显示
root.geometry('%dx%d+%d+%d' % (width,height,(root.winfo_screenwidth() - width ) / 2, (root.winfo_screenheight() - height) / 2))
#窗口最大值
root.maxsize(520, 350)
#窗口最小值
root.minsize(520, 350)
app = Logon(root)
root.mainloop()