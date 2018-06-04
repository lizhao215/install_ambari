# coding=utf-8
import paramiko


class SSHConnection(object):
    def __init__(self, host, port, username, password):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._transport = None
        self._sftp = None
        self._client = None
        self.putrate = 0
        self.downloadrate = 0
        self._connect()

    def get_host(self):
        return self._host

    def _connect(self):
        transport = paramiko.Transport((self._host, self._port))
        transport.connect(username=self._username, password=self._password)
        self._transport = transport

    def progress_put(self, transferred, to_be_transferred, suffix=''):
        percents = round(100.0 * transferred / float(to_be_transferred), 1)
        self.putrate = percents

    def progress_download(self, transferred, to_be_transferred, suffix=''):
        percents = round(100.0 * transferred / float(to_be_transferred), 1)
        self.downloadrate = percents

    def download(self, remotepath, localpath):
        if self._sftp is None:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
        self._sftp.get(remotepath, localpath, callback=self.progress_download)

    def put(self, localpath, remotepath):
        if self._sftp is None:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
        self._sftp.put(localpath, remotepath, callback=self.progress_put)

    def exec_command(self, command):
        if self._client is None:
            self._client = paramiko.SSHClient()
            self._client._transport = self._transport
        stdin, stdout, stderr = self._client.exec_command(command)
        out = stdout.read()
        err = stderr.read()
        return out, err

    def exec_command2(self, command):
        if self._client is None:
            self._client = paramiko.SSHClient()
            self._client._transport = self._transport
        stdin, stdout, stderr = self._client.exec_command(command)
        out = stdout.read()
        err = stderr.read()
        if len(err) > 0:
            print err.strip()
            return False
        else:
            return True

    def close(self):
        if self._transport:
            self._transport.close()
        if self._client:
            self._client.close()


if __name__ == "__main__":
    conn = SSHConnection('192.168.87.200', 22, 'username', 'password')
    localpath = 'hello.txt'
    remotepath = '/home/hupeng/WorkSpace/Python/test/hello.txt'
    print 'downlaod start'
    conn.download(remotepath, localpath)
    print 'download end'
    print 'put begin'
    conn.put(localpath, remotepath)
    print 'put end'

    conn.exec_command('whoami')
    conn.exec_command('cd WorkSpace/Python/test;pwd')
    conn.exec_command('pwd')
    conn.exec_command('tree WorkSpace/Python/test')
    conn.exec_command('ls -l')
    conn.exec_command('echo "hello python" > python.txt')
    conn.exec_command('ls hello')
    conn.close()

