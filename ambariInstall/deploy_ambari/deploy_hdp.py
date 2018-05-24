# -*- coding:utf-8 -*-

from utils import *
import os,sys
import requests


def deploy_ambari_hdp(uuid, ip, user="root", password="Letmein123"):
    taskdir = os.path.join(os.getcwd(), "..\\" + uuid)
    write_file(os.path.join(taskdir, 'hdp_status.txt'), 'deploying')
    logger = create_log(os.path.join(taskdir, 'deploy_hdp.log'))
    logger.info("start to install httpd .")
    httpd_port = install_httpd(logger, ip, user, password)
    # 上传  ambari 和 hdp 包
    logger.info("start to upload hdp package.")
    ambari_url = 'http://' + ip + ":" + httpd_port + '/ambari'
    hdp_url = 'http://' + ip + ":" + httpd_port + '/hdp/centos7'
    hdp_utlis_url = 'http://' + ip + ":" + httpd_port + '/hdp/HDP-UTILS/'
    if test_url(ambari_url, 'AMBARI') and test_url(hdp_url, 'hadoop') and test_url(hdp_utlis_url, 'hadoop'):
        write_file(os.path.join(taskdir, 'hdp_status.txt'), 'success')
        logger.info("hdp package is already upload ,then exit")
        return True
    mkdir_on_linux('/var/www/html/hdp/HDP_UTIL', ip, user, password)
    mkdir_on_linux('/var/www/html/ambari', ip, user, password)
    mkdir_on_linux('/home/ambariTemp', ip, user, password)
    logger.info("mkdir /var/www/html/hdp and /var/www/html/ambari and /home/ambariTemp")
    hdp_name = 'HDP-2.5.0.0-centos7-rpm.tar.gz'
    hdp_util_name = 'HDP-UTILS-1.1.0.21-centos7.tar.gz'
    ambari_name = 'ambari-2.4.1.0-centos7.tar.gz'
    hdp_path = os.path.join(os.getcwd(), "ambariInstall\\uploadToLinuxFile\\HDP-2.5.0.0-centos7-rpm.tar.gz")
    hdp_util_path = os.path.join(os.getcwd(), "ambariInstall\\uploadToLinuxFile\\HDP-UTILS-1.1.0.21-centos7.tar.gz")
    ambari_path = os.path.join(os.getcwd(), "ambariInstall\\uploadToLinuxFile\\ambari-2.4.1.0-centos7.tar.gz")
    copy_hdp_log = copy_file_to_linux(hdp_path, ip, '/home/ambariTemp/', user, password)
    logger.info(copy_hdp_log)
    copy_hdp_util_log = copy_file_to_linux(hdp_util_path, ip, '/home/ambariTemp/', user, password)
    logger.info(copy_hdp_util_log)
    copy_ambari_log = copy_file_to_linux(ambari_path, ip, '/home/ambariTemp/', user, password)
    logger.info(copy_ambari_log)
    logger.info("copy hdp ambari utils complete")
    # 解压
    exec_unzip_tarfile('/home/ambariTemp/'+hdp_name, ip, '/var/www/html/hdp/', user, password)
    exec_unzip_tarfile('/home/ambariTemp/'+hdp_util_name, ip, '/var/www/html/hdp/HDP_UTIL/', user, password)
    exec_unzip_tarfile('/home/ambariTemp/'+ambari_name, ip, '/var/www/html/ambari/', user, password)
    logger.info("unzip hdp ambari utils complete")
    # 启动 httpd
    if test_url(ambari_url, 'AMBARI') and test_url(hdp_url, 'hadoop') and test_url(hdp_utlis_url, 'hadoop'):
        write_file(os.path.join(taskdir, 'hdp_status.txt'), 'success')
        return True
    else:
        write_file(os.path.join(taskdir, 'hdp_status.txt'), 'failed')
        logger.error("hdp local repo is not available,please check")
        exit(1)
    return True


def upload_hdp_repo(ambari_url,hdp_url,hdp_utlis_url):

    pass


def install_httpd(logger, ip, user="root", password="Letmein123", ):
    # 检查是否安装httpd
    yum_install_httpd = exec_shell_command2('yum list installed  | grep httpd', ip, user, password)
    if yum_install_httpd.find('httpd') > -1:
        print 'httpd is already install'
        logger.info('httpd is already install')
    else:
        # yum install httpd -y
        logger.info('httpd is not install ,then start to install httpd ,please ensure yum is useful to install httpd')
        install_yum_log = exec_shell_command2("yum -y install httpd ", ip, user, password)
        print install_yum_log
        logger.info(install_yum_log)
        #   离线安装 按照顺序 apr apr-util httpd-tools mailcap  httpd
        # check port and status
    httpd_port = exec_shell_command2("cat /etc/httpd/conf/httpd.conf | grep ^Listen | awk '{print $2}'", ip,
                                     user, password)
    httpd_status = exec_shell_command2('systemctl status httpd | grep Active', ip, user, password)
    if httpd_status.find('running') > 0:
        logger.info('httpd service is active running on port ' + str(httpd_port))
        return httpd_port
    if check_linux_port_use(httpd_port, ip, user, password):
        # 端口 被占用，修改为 79 端口
        logger.warning(httpd_port + " port is already used ,then update httpd use 79 port ")
        exec_shell_command("sed -i 's/Listen " + str(httpd_port) + "/Listen 79/' /etc/httpd/conf/httpd.conf", ip,
                           user, password)
        httpd_port = 79
    # 重启动httpd
    exec_shell_command2("systemctl restart httpd", ip, user, password)
    logger.info("start to  check httpd status ")
    check_httpd_status = exec_shell_command2("systemctl status httpd", ip, user, password)
    if check_httpd_status.find('running'):
        print 'httpd service is active running '
        logger.info('httpd service is active running')
        logger.info('httpd use the port  is ' + str(httpd_port))
    else:
        logger.error("httpd install and start error , please login the control node to make sure httpd service active")
        sys.exit(1)
    return httpd_port


def test_url(url, keyword):
    response = requests.get(url)
    if response.status_code == 200:
        text = response.text
        if text.find(keyword) > 0:
            return True
    return False


if __name__ == "__main__":
    pass


