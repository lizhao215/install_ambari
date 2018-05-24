# -*- coding:utf-8 -*-

from utils import *
import os


def deploy_ambari_server(uuid, serverip, ip, user="root", password='Letmein123'):
    taskdir = os.path.join(os.getcwd(), "..\\" + uuid)
    write_file(os.path.join(taskdir, 'server_status.txt'), 'deploying')
    copy_file_to_linux(os.path.join(os.getcwd(), '..\\uploadToLinuxFile\\start_server.sh'), ip,
                       '/home/centos/', user, password)
    cmd = 'chmod 777 /home/centos/start_server.sh; cd /home/centos/; ./start_server.sh ' + serverip + \
          "> /home/centos/deploy_" + uuid + '_server.log'
    exec_shell_command(cmd, ip, user, password)
    write_file(os.path.join(taskdir, 'agents_status.txt'), 'success')






