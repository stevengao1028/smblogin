# -*- coding: utf-8 -*-
import subprocess,os
import base64

conpath=os.getcwd()
confile=conpath+r"\conf.ini"
if not os.path.isfile(confile):
    try:
        file = open(confile, 'w')
    finally:
        if file:
            file.close()


def loadconf():
    diskinfo = getshare()
    with open(confile, 'r') as f1:
        for lines in f1.readlines():
            line = lines.rstrip('\n')
            is_ok = 0
            if len(line.split('##')) != 4:
                continue
            user = line.split('##')[0]
            encryp_pass = line.split('##')[1]
            password = base64.decodestring(encryp_pass)
            ip = line.split('##')[2]
            share = line.split('##')[3]
            for each in diskinfo:
                if len(each['path'].split('\\')) == 4:
                    exsit_ip = each['path'].split('\\')[2]
                    exsit_share = each['path'].split('\\')[3]
                    exsit_status = each['status']
                    exsit_disk = each['driver']
                    if share.decode('gbk').encode('utf-8') == exsit_share and ip == exsit_ip and exsit_status != "OK":
                        exe_con = r"net use  " + exsit_disk + " \\\\" + exsit_ip + "\\" + exsit_share + " " + password + " /user:" + user + " /persistent:no"
                        con_result = subprocess.Popen(exe_con, shell=True)
                        is_ok = 1
                        break
                    elif share.decode('gbk').encode('utf-8') == exsit_share and ip == exsit_ip and exsit_status == "OK":
                        is_ok = 1
                        break
            if is_ok == 0:
                cmd_add = r"net use * \\" + ip + "\\" + share + " " + password + " /user:" + user + " /persistent:no"
                exe_result = subprocess.Popen(cmd_add, shell=True)



def getshare():
    cmd_get = "net use"
    cmd_result=os.popen(cmd_get).read().decode('gbk').encode('utf-8')
    share_list=[]
    for line in cmd_result.split('\n'):
        eachline=line.split()
        if len(eachline) > 2 and "\\" in eachline[2] :
            share = {'driver':eachline[1],'status':eachline[0],'path':eachline[2]}
            share_list.append(share)
        # if len(eachline) == 6 and eachline[3]=="Microsoft":
        #     share = {'driver':eachline[1],'status':eachline[0],'path':eachline[2]}
        #     share_list.append(share)
    result = share_list
    return result


if __name__ == "__main__":
    loadconf()

