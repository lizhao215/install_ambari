# -*- coding:utf-8 -*-

from utils import *
import os


def deploy_ambari_server(uuid, serverip, ip, user="root", password='Letmein123'):
    taskdir = os.path.join(os.getcwd(), uuid)
    write_file(os.path.join(taskdir, 'server_status.txt'), 'deploying')
    logger = create_log(os.path.join(taskdir, 'deploy_server.log'))
    logger.info("begin to deploy agents...")
    logger.info("begin to copy start_server.sh  to control node")
    mkdir_on_linux('/home/centos', ip, user, password)
    copy_file_to_linux(os.path.join(taskdir, '..\\ambariInstall\\uploadToLinuxFile\\start_server.sh'), ip,
                       '/home/centos/', user, password)
    logger.info("copy  start_server.sh  to control node  success")
    cmd = 'chmod 777 /home/centos/start_server.sh; cd /home/centos/; ./start_server.sh ' + serverip
    logger.info("begin to exec: " + cmd)
    log_text = exec_shell_command2(cmd, ip, user, password)
    logger.info(log_text)
    write_file(os.path.join(taskdir, 'server_status.txt'), 'success')






