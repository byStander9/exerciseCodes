from xmlrpc.server import SimpleXMLRPCServer

# 서버 종료 플래그
is_running = True

# 원격에서 호출할 수 있는 함수 정의
def add(x, y):
    return x + y

def multiply(x, y):
    return x * y

# 상태 저장용 변수
state = {"count": 0}

# 상태를 변경하는 함수
def increment():
    state["count"] += 1
    return state["count"]

def get_count():
    return state["count"]

# RPC 서버 생성
# server = SimpleXMLRPCServer(("localhost", 8000))
# print("RPC 서버가 실행 중입니다...")

# # 함수 등록
# server.register_function(add, "add")  # 'add' 함수 등록
# server.register_function(multiply, "multiply")  # 'multiply' 함수 등록

# server.register_function(increment, "increment")
# server.register_function(get_count, "get_count")

# server.serve_forever()

def shutdown():
    global is_running
    is_running = False
    return "서버가 종료됩니다."

# 서버 실행 함수
def start_server():
    global is_running
    with SimpleXMLRPCServer(("localhost", 8000)) as server:
        server.register_function(add, "add")
        server.register_function(multiply, "multiply")  # 'multiply' 함수 등록
        server.register_function(shutdown, "shutdown")
        server.register_function(increment, "increment")
        server.register_function(get_count, "get_count")
        print("RPC 서버가 실행 중입니다...")

        # 무한 루프 대신 상태를 체크하며 실행
        while is_running:
            server.handle_request()  # 한 번씩 요청을 처리

        print("RPC 서버가 종료되었습니다.")

# 서버 실행
start_server()