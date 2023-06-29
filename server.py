import socket
import pickle
import select
import time
from client import packing
from collections import defaultdict

HOST = '0.0.0.0'
PORT = 8080
MSG_SIZE = 8192
TIMEOUT = 100
SLEEP_TIME = 0.5

def def_value():
    return 0

client_name_dict = {} # key: name, value: socket
client_sock_dict = {} # key: socket, value: name
passive_list = [] # List of clients who are waiting for opponent
opponent_dict = {} # key: name, value: opponent name
match_result = {} # key: (name1, name2), value: result
match_cnt = defaultdict(def_value)
match_order_recv_cnt = defaultdict(def_value)
match_end_cnt = defaultdict(def_value)


# def sending_trash(conn):
#     while True:
#         conn.send(' '.encode())
#         time.sleep(1)

# def handle_disconnect(conn, addr):
#     while True:
#         try:
#             data = conn.recv(8192).decode('utf-8')
#         except:
#             continue
#         if 'disconnect' in data:
#             print(f'{addr} disconnected')
            

def is_socket_closed(sock: socket.socket) -> bool:
    try:
        # this will try to read bytes without blocking and also without removing them from buffer (peek only)
        data = sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
        if len(data) == 0:
            return True
    except BlockingIOError:
        return False  # socket is open and reading from it would block
    except ConnectionResetError:
        return True  # socket was closed for some other reason
    except Exception as e:
        return False
    return False

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(200) # Up to 200 clients
    print("---------------------------------")
    print("Reversi server is running...")
    socket_list = [s]
    while True:
        connections, _, _ = select.select(socket_list, [], [])
        for sock in connections:
            if sock is s:
                conn, addr = s.accept()
                socket_list.append(conn) 
            else:
                try:
                    content = sock.recv(MSG_SIZE).decode('utf-8')
                except:
                    print('client disconnected')
                    sock.close()
                    socket_list.remove(sock)
                    try:
                        name = client_sock_dict[sock]
                        if name in passive_list:
                            passive_list.remove(name)

                        if name in opponent_dict:
                            try:
                                client_name_dict[opponent_dict[name]].sendall('opponent_disconnected'.encode())
                            except:
                                print("[ERROR] Send Error")
                            del opponent_dict[opponent_dict[name]]
                            del opponent_dict[name]
                        
                        del client_name_dict[name]
                        del client_sock_dict[sock]
                        continue
                    # print exceptions
                    except Exception as e:
                        print(e)
                        continue

                content = content.split('#')
                if content != [""] and content != ['no_event'] and content != ['online_list']: print(content)
                if content[0] == 'running_disconnect':
                    name = content[1]
                    try:
                        client_name_dict[opponent_dict[name]].sendall(packing(["opponent_disconnect"]))
                    except:
                            print("[ERROR] Send Error")
                    for match in match_result: 
                        if match[0] == name or match[1] == name:
                            print(f'remove match {match}')
                            del match_result[match]
                            break
                    del opponent_dict[opponent_dict[name]]
                    del opponent_dict[name]
                    
                if content[0] == 'disconnect':
                    # disconnect while running game
                    sock.close()
                    socket_list.remove(sock)
                    try:
                        name = client_sock_dict[sock]
                        if name in passive_list:
                            passive_list.remove(name)

                        if name in opponent_dict:
                            if opponent_dict[name] in client_name_dict:
                                try:
                                    client_name_dict[opponent_dict[name]].sendall('opponent_disconnected'.encode())
                                except:
                                    print("[ERROR] Send Error")
                            del opponent_dict[name]
                        if name in client_name_dict:
                            del client_name_dict[name]
                    except:
                        pass
                    if sock in client_sock_dict:
                        del client_sock_dict[sock]
                                
                elif content[0] == 'register':
                    client_name = content[1]
                    client_mode = content[2]
                    name_list = list(client_name_dict.keys())
                    for name in name_list:
                        if is_socket_closed(client_name_dict[name]):                        
                            if name in passive_list:
                                passive_list.remove(name)

                            if name in opponent_dict:
                                opponent = opponent_dict[name]
                                match = (max(name, opponent), min(name, opponent))
                                if match in match_result:
                                    del match_result[match]
                                if match in match_cnt:
                                    del match_cnt[match]
                                if match in match_order_recv_cnt:
                                    del match_order_recv_cnt[match]
                                if match in match_end_cnt:
                                    del match_end_cnt[match]
                                try:
                                    client_name_dict[opponent_dict[name]].sendall('opponent_disconnected'.encode())
                                except:
                                    print("[ERROR] Send Error")
                                del opponent_dict[opponent_dict[name]]
                                del opponent_dict[name]
                            
                            del client_name_dict[name]
                    if client_name in client_name_dict:
                        print('Name already exists')
                        try:
                            sock.sendall('Name already exists'.encode('utf-8'))
                        except:
                            print("[ERROR] Send Error")
                        continue
                        
                    client_name_dict[client_name] = sock
                    client_sock_dict[sock] = client_name
                    print(f'Client {client_name} connected')
                    try:
                        sock.sendall('Connected'.encode('utf-8'))
                    except:
                        print("[ERROR] Send Error")
                    if client_mode == 'passive':
                        passive_list.append(client_name)
                        
                elif content[0] == 'online_list':
                    for name in passive_list:
                        if is_socket_closed(client_name_dict[name]):
                            if name in passive_list:
                                passive_list.remove(name)

                            if name in opponent_dict:
                                try:
                                    client_name_dict[opponent_dict[name]].sendall('opponent_disconnected'.encode())
                                except:
                                    print("[ERROR] Send Error")
                                del opponent_dict[opponent_dict[name]]
                                del opponent_dict[name]
                            
                            del client_name_dict[name]
                    try:
                        sock.sendall(pickle.dumps(passive_list))
                    except:
                        print("[ERROR] Send Error")
                    
                elif content[0] == 'active_req':
                    active_player = content[1]
                    opponent = content[2]
                    passive_list.remove(opponent)
                    opponent_dict[opponent] = active_player
                    opponent_dict[active_player] = opponent
                    try:
                        client_name_dict[opponent].sendall(f'req {client_sock_dict[sock]}'.encode())
                    except:
                        print("[ERROR] Send Error")
                
                elif content[0] == 'passive_confirm':
                    passive_player = content[1]
                    opponent = content[2]
                    match = (max(passive_player, opponent), min(passive_player, opponent))
                    if opponent in client_name_dict:
                        try:
                            client_name_dict[opponent].sendall('agree'.encode())
                            sock.sendall('success_send_agree'.encode())
                        except:
                            print("[ERROR] Send Error")
                    else:
                        try:
                            sock.sendall('opponent_disconnected'.encode())
                        except:
                            print("[ERROR] Send Error")
                    match_order_recv_cnt[match] = 0
                        
                elif content[0] == 'game_order':
                    first_game = True if content[1] == 'first' else False
                    passive = True if 'passive' in content[2]  else False
                    game_order = 'black' if (first_game and not passive) or (not first_game and passive) else 'white'
                    try:
                        sock.sendall(game_order.encode())
                    except:
                        print("[ERROR] Send Error")
                
                elif content[0] == 'play':
                    name = content[1]
                    try:
                        client_name_dict[opponent_dict[name]].sendall(packing(["play", content[2], content[3]]))
                    except:
                        print("[ERROR] Send Error")
                    
                elif content[0] == 'no_event':
                    pass
                    #sock.sendall('fuck_you'.encode())
                
                elif content[0] == 'END1':
                    name = content[1]
                    opponent = opponent_dict[name]
                    match = (max(name, opponent), min(name, opponent))
                    match_cnt[match] += 1
                    if name == match[0]:
                        match_result[match] = {
                            name: int(content[2]),
                            opponent: int(content[3])
                        }
                    if match_cnt[match] == 2:
                        try:
                            client_name_dict[name].sendall("END1".encode())
                            client_name_dict[opponent].sendall("END1".encode())
                        except:
                            print("[ERROR] Send Error")
                        match_order_recv_cnt[match] = 0
                elif content[0] == 'END2':
                    name = content[1]
                    opponent = opponent_dict[name]
                    match = (max(name, opponent), min(name, opponent))
                    if match_end_cnt[match] == 0:
                        match_result[match][name] += int(content[2])
                        match_result[match][opponent] += int(content[3])
                        match_end_cnt[match] += 1
                    elif match_end_cnt[match] == 1:
                        try:
                            sock.sendall(pickle.dumps(match_result[match]))
                            client_name_dict[opponent].sendall(pickle.dumps(match_result[match]))
                        except:
                            print("[ERROR] Send Error")
                        match_end_cnt[match] = 0
                        match_cnt[match] = 0
                elif content[0] == 'get_order':
                    name = content[1]
                    if name in opponent_dict:
                        opponent = opponent_dict[name]
                    else:
                        try:
                            sock.sendall('opponent_disconnected'.encode())
                        except:
                            print("[ERROR] Send Error")
                        continue
                    match = (max(name, opponent), min(name, opponent))
                    match_order_recv_cnt[match] += 1
                    if match_order_recv_cnt[match] == 2:
                        try:
                            client_name_dict[opponent].sendall('OK'.encode())
                            client_name_dict[name].sendall('OK'.encode())
                        except:
                            print("[ERROR] Send Error")
