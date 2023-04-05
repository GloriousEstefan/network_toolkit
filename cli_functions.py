from paramiko import SSHException, AuthenticationException
from parameeko import GetInfo
from subprocess import run
from is_ip_valid import is_ip_valid
from getpass import getpass


def open_file():
        run(["start", "iplist.txt"], shell=True)


class ScriptLoop(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.valid_ips = []
        self.output = ""

    def get_username(self):
        self.username = input("Enter your username: ")


    def get_password(self):
        self.password = getpass("Enter your password: ")


    def read_file(self):
        with open('iplist.txt', 'r') as f:
            file_contents = [item.strip() for item in f.readlines()]

        if not file_contents:
            print("File is empty")

        self.valid_ips = [ip for ip in file_contents if is_ip_valid(ip)]

        return self.valid_ips
    

    def write_file(self):
        with open("output.txt", "a") as f:
            f.write(self.output)


    def run_script(self):
        if not self.username:
            self.get_username()

        if not self.password:
            self.get_password()

        if not self.valid_ips:
            self.read_file()

        for valid_ip in self.valid_ips:
            device = GetInfo(ip_address=valid_ip, username=self.username, password=self.password)
        
            try:
                device.connect()

            except AuthenticationException as e:
                print(f"An error occurred: {e}")
                continue

            except SSHException as e:
                print(f"An error occurred: {e}")
                continue

            except TimeoutError as e:
                print(f"An error occurred: {e}")
                continue

            else:
                self.output = device.show_run()
                print(self.output)
                self.write_file()

            finally:
                device.disconnect()