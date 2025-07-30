import time
import paramiko

TIMEOUT = 10 # seconds

class SSHClient:
    """ A class to handle SSH connections """
    def __init__(self, host:str, username:str, password:str, port:int =22, encoding = "utf-8"):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.encoding = encoding
        self.client = None
        self.channel = None

    def connect(self):
        """
        ssh 연결을 수행합니다.
        
        """
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
            self.channel = None
        except paramiko.SSHException as e:
            print(f"SSH 연결 오류 : {e}")
            self.client = None
            self.channel = None
        except Exception as e:
            print(f"알 수 없는 오류 : {e}")
            self.client = None
            self.channel = None

    def execute_command(self, commands:list) -> list[str]:
        if self.client is None:
            print("연결되어 있지 않음")
            return None

        result = []
        # NOTE : invoke_shell > send 
        for cmd in commands:
            try:
                self.channel.send(cmd + '\n').encode((self.encoding))
                output = self.receive_check()
                result.append(output)
            except TimeoutError as e:
                print(f"[{cmd}] 실행 중 타임아웃: {e}")
                result.append(f"ERROR: {e}")

        return result

    # NOTE : prompt는 list 로 받아 여러 ssh 환경에서 확인 할수 있도록
    def receive_check(self, prompt: str = "#", timeout: int = TIMEOUT) -> str:
        """
        프롬프트 입력줄이 나올때 까지의 입력을 기다립니다.
        """
        output = ""
        end_time = time.time() + timeout
        while time.time() < end_time:
            if self.channel.recv_ready():
                output_chunk = self.channel.recv(4096).decode(self.encoding)
                output += output_chunk

                if any(output.strip().endswith(p) for p in prompt):
                    return output
            else:
                time.sleep(0.2)

        raise TimeoutError("응답 대기 시간 초과")


    # NOTE : exit 명령어를 보내어 종료하는 서버도 있음
    def close(self):
        """
        작업을 끝내고 종료합니다.
        """
        if self.channel is not None:
            self.channel.close()
        self.client.close()
        print("ssh 실행 종료")
