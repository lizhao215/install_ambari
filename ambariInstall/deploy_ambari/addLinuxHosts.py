# -*- coding:utf-8 -*-

import os


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
    print 'result:', result.read()
    return result.read()


def start_ambari_agent(serverIP):
    # 复制hosts.txt repo至control节点，遍历host 调用脚本

    pass


def start_ambari_server(serverIP):
    # 调用脚本
    pass


def create_repo_file():
    # sed 命令 只修改ip 和端口
    pass


if __name__ == "__main__":
    current_path = os.getcwd()
    global pscp_tool
    global plink_tool
    plink_tool = os.path.join(current_path, "ambariInstall\linuxConnTools\plink.exe")
    pscp_tool = os.path.join(current_path, "ambariInstall\linuxConnTools\pscp.exe")
    print current_path

    #testfilepath = os.path.join(current_path, "ambariInstall\uploadToLinuxFile\jdk-8u77-linux-x64.tar.gz")
    #check_linux_port_use(80, '172.16.16.47', user='root', password='Letmein123')
    #set_javahome_on_linux('/home/123/2334/34', '172.16.16.47', user='root', password='Letmein123')
    #copy_file_to_linux(testfilepath, '172.16.16.47', '/home/ambari-test/', user="root", password="Letmein123")


