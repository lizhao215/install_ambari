# -*- coding:utf-8 -*-

import os
import logging

global pscp_tool
global plink_tool
plink_tool = os.path.join(os.getcwd(), "ambariInstall\linuxConnTools\plink.exe")
pscp_tool = os.path.join(os.getcwd(), "ambariInstall\linuxConnTools\pscp.exe")


def exec_unzip_tarfile(tarfile, ip, dest_path="", user="root", password="root"):
    if dest_path == "":
        command = "tar -zxvf " + tarfile
    else:
        command = "tar -zxvf " + tarfile + " -C " + dest_path
    result = exec_shell_command(command, ip, user, password)
    return result


def set_javahome_on_linux(javahome, ip, user="root", password="root"):
    print "begin set javahome on  " + ip + " JAVAHOME :" + javahome
    command_set_javahome = 'echo "export JAVA_HOME=/usr/java/jdk1.8.0_77"  >> /etc/profile'
    command_set_path = "echo 'export PATH=$JAVA_HOME/bin:$PATH' >> /etc/profile"
    set_javahome_result = exec_shell_command(command_set_javahome, ip, user, password)
    set_path_result = exec_shell_command(command_set_path, ip, user, password)
    print 'set_javahome_result:', set_javahome_result
    print 'set_path_result:', set_path_result
    command_check = "source /etc/profile; echo $JAVA_HOME; echo $PATH"
    check_result = exec_shell_command2(command_check, ip, user, password)
    return check_result


def check_linux_port_use(port, ip, user="root", password="root"):
    print "begin check linux " + ip + " port :" + str(port)
    command = 'lsof -i:' + str(port)
    result = exec_shell_command(command, ip, user, password)
    if result == 0:
        print port, "is already in used!!!!"
        return True
    return False


def mkdir_on_linux(dirpath, ip, user="root", password="root"):
    print "begin mkdir on " + ip + "  dir: " + dirpath
    command = 'mkdir -p ' + dirpath
    result = exec_shell_command(command, ip, user, password)
    return result


def copy_file_to_linux(filepath, ip, destpath, user="root", password="root"):
    print "start copy " + filepath + " to " + ip
    command = 'echo y | ' + pscp_tool + ' -l  ' + user + ' -pw ' + ' "' + password + '" ' \
              + filepath + ' ' + ip + ':' + destpath
    print command
    result = os.system(command)
    print 'result:', result
    return result


    # os.system()返回 退出码 适合于  上传文件,  mkdir, exprot >>  tar  无明显输出的可通过返回值确认是否成功
def exec_shell_command(cmd, ip, user="root", password="root"):
    print "start exec " + cmd + " on " + ip + "  user:" + user
    command = 'echo y | ' + plink_tool + ' -l  ' + user + ' -pw ' + ' "' + password + '" ' + ip + ' "' + cmd + '"'
    print command
    result = os.system(command)
    print 'result:', result
    return result


    # os.popen()返回 输出结果 ，需要 检查 返回内容
def exec_shell_command2(cmd, ip, user="root", password="root"):
    print "start exec " + cmd + " on " + ip + "  user:" + user
    command = 'echo y | ' + plink_tool + ' -l  ' + user + ' -pw ' + ' "' + password + '" ' + ip + ' "' + cmd + '"'
    print command
    result = os.popen(command)
    console_text = result.read()
    print 'result:', console_text
    result.close()
    return console_text


def readlines_file(file_path):
    with open(file_path, 'r') as f:
        return f.readlines()


def read_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()


def write_file(file_path, text=' '):
    with open(file_path, 'w') as f:
        f.write(text)


def create_log(log_file):
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


if __name__ == "__main__":
    print 123
    # a = exec_shell_command2("yum list installed  | grep httpd", '172.16.16.40', user="root", password="Letmein123")


