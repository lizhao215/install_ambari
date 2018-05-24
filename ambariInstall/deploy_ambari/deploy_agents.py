# -*- coding:utf-8 -*-


from utils import *
import os


def deploy_ambari_agent(uuid, serverip, ip, user="root", password='Letmein123'):
    taskdir = os.path.join(os.getcwd(), "..\\" + uuid)
    write_file(os.path.join(taskdir, 'agents_status.txt'), 'deploying')
    hosts = get_hosts_list(taskdir)
    for key, value in hosts.items():
        print 'begin deploy :', key + ':' + value
    copy_file_to_linux(os.path.join(taskdir, 'hosts.txt'), ip, '/home/centos/', user, password)
    copy_file_to_linux(os.path.join(os.getcwd(), '..\\uploadToLinuxFile\\start_allAgent.sh'), ip,
                       '/home/centos/', user, password)
    cmd = 'chmod 777 /home/centos/start_allAgent.sh; cd /home/centos/; ./start_allAgent.sh ' + serverip + \
          ' > /home/centos/deploy_' + uuid + '_agent.log'
    exec_shell_command(cmd, ip, user, password)
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


