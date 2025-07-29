import paramiko

TIMEOUT = 10 # seconds

class SSHClient:
    """ A class to handle SSH connections """
    def __init__(self, host:str, username:str, password:str, port:int =22):
        self.host = host
        self.username = username
        self.password = password
        self.port = port

        self.client = None
        self.channel = None

    def connect(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            self.client.connect(
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                timeout=TIMEOUT
            )

            self.channel = self.client.invoke_shell(
                term='xterm',
                width=80,
                height=24   
            )

        except paramiko.AuthenticationException:
            print("인증 실패")
            self.client = None
        except paramiko.SSHException as e:
            print(f"SSH 연결 오류 : {e}")
            self.client = None
        except Exception as e:
            print(f"알 수 없는 오류 : {e}")
            self.client = None

    def execute_command(self, commands:list):
        if self.client is None:
            print("연결되어 있지 않음")
            return None

        # NOTE : invoke_shell > send 
        for cmd in commands:
            self.channel.send(cmd + '\n')

    def recevie_check(self, prompt: str = "#", timeout: int = TIMEOUT) -> str:
        pass


    def close(self):
        pass