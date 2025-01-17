import xmlrpc.client

# RPC 서버에 연결
proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

# 원격 함수 호출
result_add = proxy.add(10, 5)  # 10 + 5 = 15
result_multiply = proxy.multiply(10, 5)  # 10 * 5 = 50
result_increment = proxy.increment()
result_get_count = proxy.get_count()
result_shutdown = proxy.shutdown()

print(f"Add 결과: {result_add}")  # 출력: Add 결과: 15
print(f"Multiply 결과: {result_multiply}")  # 출력: Multiply 결과: 50
print(f"increment 결과: {result_increment}")
print(f"get_count 결과: {result_get_count}")
print(f"shutdonw 결과: {result_shutdown}")