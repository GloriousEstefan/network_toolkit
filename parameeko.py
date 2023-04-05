from paramiko import AutoAddPolicy, SSHClient, AuthenticationException, SSHException
from socket import timeout


class GetInfo(object):
    def __init__(self, ip_address, username, password):
        self.ip_address = ip_address
        self.username = username
        self.password = password
        self.ssh_client = None


    def connect(self):
        try:
            self.ssh_client = SSHClient()

            self.ssh_client.set_missing_host_key_policy(AutoAddPolicy())
            
            self.ssh_client.connect(self.ip_address, username=self.username, password=self.password)

        except AuthenticationException as e:
            raise AuthenticationException(f"Failed to connect to {self.ip_address}: {e}")

        except SSHException as e:
            raise SSHException(f"Failed to connect to {self.ip_address}: {e}")
        
        except timeout:
            raise TimeoutError(f"Failed to connect to {self.ip_address}: Connection timed out.")
            
        
    def show_run(self):
        if not self.ssh_client:
            self.connect()

        stdin, stdout, stderr = self.ssh_client.exec_command("show run | include aaa")
        output = stdout.read().decode()

        return output


    def disconnect(self):
        if self.ssh_client:
            self.ssh_client.close()