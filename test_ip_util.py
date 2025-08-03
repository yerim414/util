from ip_util import IpUtil


# is_valid_ip 테스트
result1 = IpUtil.is_valid_ip("12.12.12.12")
result2 = IpUtil.is_valid_ip("0.0.0.0")
result3 = IpUtil.is_valid_ip("8.8.8.8.8.8")
result4 = IpUtil.is_valid_ip("172.13.21.256")

# # cidr_to_netmask 테스트
print(IpUtil.cidr_to_netmask(32))
print(IpUtil.cidr_to_netmask(21))
print(IpUtil.cidr_to_netmask(34)) # NetmaskValueError


# netmask_to_cidr 테스트
print(IpUtil.netmask_to_cidr("255.255.255.255"))
print(IpUtil.netmask_to_cidr("255.255.255.0"))
print(IpUtil.netmask_to_cidr("255.255.0.0"))
print(IpUtil.netmask_to_cidr("255.255.255.256")) # NetmaskValueError


# ip_in_cidr 테스트
print(IpUtil.ip_in_cidr("192.168.0.0", "192.168.0.25"))

# guess_cidr_by_zero 테스트
print(IpUtil.guess_cidr_by_zero("192.168.0.0"))

