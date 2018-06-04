# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
import json
from deploy_ambari.deploy_agents import *
from deploy_ambari.deploy_server import *
from deploy_ambari.deploy_hdp import *
import thread
import uuid


def index(request):
    context = {}
    menu = request.GET.get("detail")
    param = request.GET.get("param")
    if menu:
        context['detail'] = menu
    else:
        context['detail'] = 'ambari.html'
    if param:
        context['param'] = param

    return render(request, 'index.html', context)


def hello(request):
     return HttpResponse("Welcome to use my website to deploy ambari cluster ! ")


def input2(request):
    context = {}
    context['hello'] = 'this is test page !'
    return render(request, 'input2.html', context)


def input_ambari(request):
    context = {}
    context['hello'] = 'this is test page !'
    return render(request, 'input_ambari.html', context)


def hdp_yum_repo(request):
    context = {}
    return render(request, 'install_hdp_repo.html', context)


def config_without_password_login(request):
    context = {}
    return render(request, 'config_without_password_login.html', context)


def zabbix(request):
    context = {}
    return render(request, 'zabbix.html', context)


def zabbix_proxy(request):
    context = {}
    return render(request, 'zabbix_proxy.html', context)


def ambari_install_progress(request):
    context = {}
    taskid = request.GET.get('taskid')
    context['taskid'] = taskid
    taskdir = os.path.join(os.getcwd(), taskid)
    context['nodes'] = get_hosts_list(taskdir)
    print 'context', context
    return render(request, 'ambari_install_progress.html', context)


def ambari_install_submit(request):
    context = {}
    if request.method == 'GET':
        serverip = request.GET.get("serverip")
        controlip = request.GET.get("controlip")
        controlpwd = request.GET.get("controlpwd")
        hosts = request.GET.get("hosts")
    print "serverip： ", serverip
    print "controlip： ", controlip
    print "controlpwd： ", controlpwd
    print "hosts： ", hosts
    taskid = str(uuid.uuid1())
    context['taskid'] = taskid
    resp = {'status': "SUCCESS", 'taskid': taskid}
    thread.start_new_thread(deploy_ambari, (taskid, controlip, controlpwd, serverip, hosts))
    return HttpResponse(json.dumps(resp), content_type="application/json")


def deploy_ambari(taskid, controlip, controlpwd, serverip, hosts):
    print taskid, controlip, controlpwd, serverip, hosts
    taskdir = os.path.join(os.getcwd(), taskid)
    os.mkdir(taskdir)
    write_file(os.path.join(taskdir, 'hosts.txt'), hosts)
    write_file(os.path.join(taskdir, 'server.txt'), serverip)
    write_file(os.path.join(taskdir, 'control.txt'), controlip + ' ' + controlpwd)
    write_file(os.path.join(taskdir, 'hdp_status.txt'), 'prepare')
    write_file(os.path.join(taskdir, 'agents_status.txt'), 'prepare')
    write_file(os.path.join(taskdir, 'server_status.txt'), 'prepare')
    # deploy_ambari_hdp(taskid, controlip, user="root", password=controlpwd)
    deploy_ambari_agent(taskid, serverip, controlip, user="root", password=controlpwd)
    deploy_ambari_server(taskid, serverip, controlip, user="root", password=controlpwd)


def ambari_status_query(request):
    if request.method == 'GET':
        taskid = request.GET.get("taskid")
    print taskid
    taskdir = os.path.join(os.getcwd(), taskid)
    hdp_status = read_file(os.path.join(taskdir, 'hdp_status.txt'))
    agents_status = read_file(os.path.join(taskdir, 'agents_status.txt'))
    server_status = read_file(os.path.join(taskdir, 'server_status.txt'))
    resp = {"hdp_status": hdp_status, "agents_status": agents_status, "server_status": server_status}
    print resp
    return HttpResponse(json.dumps(resp), content_type="application/json")


def query_hdp_log(request):
    taskid = request.GET.get("taskid")
    taskdir = os.path.join(os.getcwd(), taskid)
    log_file = os.path.join(taskdir, "deploy_hdp.log")
    log_text = read_file(log_file)
    resp = {'log': log_text}
    return HttpResponse(json.dumps(resp), content_type="application/json")


def query_server_log(request):
    taskid = request.GET.get("taskid")
    taskdir = os.path.join(os.getcwd(), taskid)
    log_file = os.path.join(taskdir, "deploy_server.log")
    log_text = read_file(log_file)
    resp = {'log': log_text}
    return HttpResponse(json.dumps(resp), content_type="application/json")


def query_agents_log(request):
    taskid = request.GET.get("taskid")
    taskdir = os.path.join(os.getcwd(), taskid)
    log_file = os.path.join(taskdir, "deploy_agents.log")
    log_text = read_file(log_file)
    resp = {'log': log_text}
    return HttpResponse(json.dumps(resp), content_type="application/json")


def query_agent_log(request):
    resp = {'log': 'this is agent log'}
    # get agent  node  /home/centos/ambari_agent_install.log
    return HttpResponse(json.dumps(resp), content_type="application/json")





