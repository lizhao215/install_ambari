# -*- coding:utf-8 -*-


from utils import *
import os


def deploy_ambari_agent(uuid, serverip, ip, user="root", password='Letmein123'):
    taskdir = os.path.join(os.getcwd(), uuid)
    write_file(os.path.join(taskdir, 'agents_status.txt'), 'deploying')
    logger = create_log(os.path.join(taskdir, 'deploy_agents.log'))
    logger.info("begin to deploy agents...")
    # hosts = get_hosts_list(logger, taskdir)
    # for key, value in hosts.items():
    #     print 'deploy :', key + ':' + value
    logger.info("begin to copy  hosts.txt and start_allAgent.sh to control node ")
    mkdir_on_linux('/home/centos', ip, user, password)
    copy_file_to_linux(os.path.join(taskdir, 'hosts.txt'), ip, '/home/centos/', user, password)
    copy_file_to_linux(os.path.join(taskdir, '..\\ambariInstall\\uploadToLinuxFile\\start_allAgent.sh'), ip,
                       '/home/centos/', user, password)
    logger.info("copy  hosts.txt and start_allAgent.sh to control node  success !")
    cmd = 'chmod 777 /home/centos/start_allAgent.sh; cd /home/centos/; ./start_allAgent.sh ' + serverip
    logger.info("begin to exec: " + cmd)
    log_text = exec_shell_command2(cmd, ip, user, password)
    logger.info(log_text)
    write_file(os.path.join(taskdir, 'agents_status.txt'), 'success')


def get_hosts_list(taskdir):
    hosts = {}
    text = readlines_file(os.path.join(taskdir, 'hosts.txt'))
    for line in text:
        try:
            ip = line.strip().split(' ')[0]
            node = line.strip().split(' ')[1]
            hosts[ip] = node
        except Exception, e:
            print e.message
            print line, 'format is error !!!'
    return hosts


