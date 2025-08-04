from concurrent.futures import ThreadPoolExecutor, as_completed
import socket

class PortScanner:
    def __init__(self, target_ip:str, ports:list[int], timeout: int = 5):
        self.target_ip = target_ip
        self.ports = ports
        self.timeout = timeout    

    def scan(self) -> dict[int, bool]:
        """
        모든 포트를 병렬로 스캔하고 결과를 반환합니다.
        
        Returns:
            dict[int, bool]: 포트 번호, True or False
        """
        results = {}

        # NOTE : ThreadPoolExecutor 파이썬 내장 병렬 처리 도구
        with ThreadPoolExecutor(max_workers=100) as executor:
            # NOTE : _is_port_open 병렬 처리
            future_to_port = {executor.submit(self._is_port_open, port): port for port in self.ports}

            for future in as_completed(future_to_port):
                port, is_open = future.result()
                results[port] = is_open

        return results
    
    def _is_port_open(self, port: int) -> tuple[int, bool]:
        """포트가 열려 있는지 확인합니다.

        Args:
            port (int): 검사하고자 하는 포트

        Returns:
            tuple(int, bool): 포트와 결과를 리턴합니다.
        """
        # NOTE : AF_INET -> Ipv4 검사, SOCK_STREAM -> TCP
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                result = sock.connect_ex((self.target_ip, port))
                return port, result == 0
        except Exception:
            return port, False
    


if __name__ == "__main__":
    # NOTE : loalhost로 진행
    # TODO : ip도 리스트로 여러개 보낼 수 있게
    scanner = PortScanner("127.0.0.1", ports=[22, 80])
    result = scanner.scan()
    print(result)