# -*- coding:utf-8 -*-


import logging
import ssh_connection
import paramiko
import sys


def get_ssh_obj(ip, user="root", password="root"):
    ssh_obj = ssh_connection.SSHConnection(ip, 22, user, password)
    return ssh_obj


def exec_unzip_tarfile(ssh_obj, tarfile, dest_path=""):
    if dest_path == "":
        command = "tar -zxvf " + tarfile
    else:
        command = "tar -zxvf " + tarfile + " -C " + dest_path
    result = ssh_obj.exec_command2(command)
    return result


def set_javahome_on_linux(ssh_obj, javahome="/usr/java/jdk1.8.0_77"):
    print "begin set javahome on  " + ssh_obj.get_host() + " JAVAHOME :" + javahome
    set_javahome = 'echo "export JAVA_HOME=' + javahome + '"  >> /etc/profile'
    set_path = "echo 'export PATH=$JAVA_HOME/bin:$PATH' >> /etc/profile"
    set_javahome_result = ssh_obj.exec_command(set_javahome)
    set_path_result = ssh_obj.exec_command(set_path)
    print 'set_javahome_result:', set_javahome_result
    print 'set_path_result:', set_path_result
    command_check = "source /etc/profile; echo $JAVA_HOME; echo $PATH"
    check_result = ssh_obj.exec_command(command_check)
    return check_result


def check_linux_port_use(ssh_obj, port):
    result = ssh_obj.exec_command("lsof -i:" + str(port))
    if result:
        print port, "is already in used!!!!"
        return True
    return False


def mkdir_on_linux(ssh_obj, dirpath):
    print "begin mkdir on " + ssh_obj.get_host() + "  dir: " + dirpath
    command = 'mkdir -p ' + dirpath
    result = ssh_obj.exec_command2(command)
    return result


def copy_file_to_linux(ssh_obj, filepath, destpath):
    out = ssh_obj.put(filepath, destpath)
    ssh_obj.close()
    return out


def get_upload_rate(ssh_obj):
    return ssh_obj.sftp.put.rate


def get_download_rate(ssh_obj):
    return ssh_obj.sftp.download.rate


def exec_shell_command(ssh_obj, cmd):
    """
        :param ssh_obj:
        :param cmd:
        :return: exec console log
        """
    out = ssh_obj.exec_command(cmd)
    ssh_obj.close()
    return out


def exec_shell_command2(ssh_obj, cmd):
    """
    :param ssh_obj:
    :param cmd:
    :return: True /False
    """
    out = ssh_obj.exec_command2(cmd)
    ssh_obj.close()
    return out


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

    
def progress_bar(transferred, to_be_transferred, suffix=''):
    # print "Transferred: {0}\tOut of: {1}".format(transferred, toBeTransferred)
    bar_len = 60
    filled_len = int(round(bar_len * transferred/float(to_be_transferred)))
    percents = round(100.0 * transferred/float(to_be_transferred), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()

    
def sshclient(ip, username, passwd, cmd):
    try:  
        ssh = paramiko.SSHClient()  
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
        ssh.connect(ip, 22, username, passwd, timeout=5)
        stdin, stdout, stderr = ssh.exec_command(cmd)  
        data = stdout.read()
        if len(data) > 0:
            print "INFO:", data.strip()
            return data
        err = stderr.read()
        if len(err) > 0:
            print "ERROR:", err.strip()
            return err 
        ssh.close()
    except Exception, e:
        print('download exception:', e)
        print ip, 'Error\n'

        
def sftp_upload(host, port, username, password, local, remote):
    sf = paramiko.Transport((host, port))
    sf.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(sf)
    try:
        sftp.put(local, remote)
        # if os.path.isdir(local):
        #    for f in os.listdir(local):
        #        sftp.put(os.path.join(local+f), os.path.join(remote+f))
        # else:
        #   sftp.put(local, remote)
    except Exception, e:
        print('upload exception:', e)
    sf.close()


def sftp_download(host, port, username, password, local, remote):
    sf = paramiko.Transport((host, port))
    sf.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(sf)
    try:
        sftp.get(remote, local)
        # if os.path.isdir(local):
        #    for f in sftp.listdir(remote):
        #         sftp.get(os.path.join(remote+f), os.path.join(local+f))
        # else:
        #    sftp.get(remote, local)
    except Exception, e:
        print('download exception:', e)
    sf.close()


if __name__ == "__main__":
    print 123
    

