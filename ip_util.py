import ipaddress


"""
ipaddress.ip_address() : ip 주소를 객체로 만들어준다.
ipaddress.ip_network() : network 객체로 만들어 준다.


"""

class IpUtil:
    """
    ip 관련 유틸리티 함수 모음
    """
    @staticmethod
    def is_valid_ip(ip: str) -> bool:
        """
        IP 형식이 유효한지 확인합니다.
        """
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError as e:
            print(f"아이피 형식을 확인해주세요 : {e}")
            return False
        
    @staticmethod
    def cidr_to_netmask(cidr: int) -> str:
        """
        CIDR 숫자를 서브넷 마스크 형식으로 변환합니다.
        예) 24 -> '255.255.255.0'
        """
        try:
            net = ipaddress.IPv4Network(f'0.0.0.0/{cidr}')
            return str(net.netmask)
        except ipaddress.NetmaskValueError:
            raise ValueError("올바른 CIDR 숫자를 입력해주세요 (0~32)")
        except Exception:
            raise ValueError("에러가 발생하였습니다.")
    
    @staticmethod
    def netmask_to_cidr(netmask: str) -> str:
        """
        서브넷 마스크를 CIDR 형식 문자열로 변환합니다.
        예) '255.255.255.0' -> '/24'
        """
        try:
            network = ipaddress.IPv4Network(f"0.0.0.0/{netmask}")
            return f"/{network.prefixlen}"
        except ipaddress.NetmaskValueError:
            raise ValueError("올바른 서브넷 마스크를 입력해주세요.")
        except Exception:
            raise ValueError("에러가 발생하였습니다.")
        
    @staticmethod
    def guess_cidr_by_zero(ip: str) -> str:
        """
        IP 주소에서 0의 개수에 따라 CIDR을 추정합니다.
        예:
            192.192.0.0 -> /16
            182.0.0.0   -> /8
            10.10.10.10 -> /32
        """
        try:
            ip_obj = ipaddress.ip_address(ip)
            if ip_obj.version != 4:
                raise ValueError("IPv4 주소만 지원됩니다.")

            parts = ip.split(".")
            zero_count = sum(1 for part in parts if part == "0")

            if zero_count == 3:
                return "/8"
            elif zero_count == 2:
                return "/16"
            elif zero_count == 1:
                return "/24"
            else:
                return "/32"
        except Exception:
            raise ValueError("올바른 IPv4 주소를 입력해주세요.")
        
    @staticmethod
    def ip_in_cidr(ip: str, cidr: str) -> bool:
        """
        특정 IP가 CIDR 범위 내에 포함되는지 확인합니다.
        """
        try:
            ip_obj = ipaddress.ip_address(ip)
            # NOTE : strict = False 시 192.88.88.8/24 값 이 들어 올 시 192.88.88.0/24 으로 자동 변환 합니다.
            net:list = ipaddress.ip_network(cidr, strict=False)

            # NOTE : net 변수는 list 의 값을 갖는다. index로 접근이 가능함
            # ipaddress.ip_network(192.88.88.0/24) 일때
            # net[0] -> 192.88.88.0
            # net[1] -> 192.88.88.1 ...

            return ip_obj in net
        except Exception:
            raise ValueError("입력된 IP 또는 CIDR 형식이 잘못되었습니다.")
    