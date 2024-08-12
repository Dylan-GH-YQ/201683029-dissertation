import socket
import threading
import json

SERVER_ADDRESS = '0.0.0.0'
SERVER_PORT = 5200

rooms = {}

def handle_client(conn, addr):
    print(f"New connection from {addr}")
    room_number = None
    try:
        data = conn.recv(1024).decode('utf-8')
        message = json.loads(data)
        room_number = message.get('game_id')
        if room_number not in rooms:
            rooms[room_number] = []
        rooms[room_number].append(conn)
        
        if len(rooms[room_number]) == 1:
            conn.sendall(json.dumps({'type': 'waiting', 'message': f'Waiting for another player to join room {room_number}...'}).encode('utf-8'))
            print(f"Player joined room {room_number}. Waiting for another player.")
        elif len(rooms[room_number]) == 2:
            print(f"Starting game in room {room_number}")
            for i, player_conn in enumerate(rooms[room_number]):
                color = 'black' if i == 0 else 'white'
                player_conn.sendall(json.dumps({'type': 'start', 'player': i + 1, 'color': color}).encode('utf-8'))
            print(f"Game started in room {room_number} with two players.")
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            message = json.loads(data)
            handle_game_message(room_number, conn, message)
            
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        if room_number in rooms and conn in rooms[room_number]:
            rooms[room_number].remove(conn)
            if not rooms[room_number]:
                del rooms[room_number]
        conn.close()




def handle_game_message(room_number, conn, message):
    if room_number in rooms:
        for player_conn in rooms[room_number]:
            if player_conn != conn:
                player_conn.sendall(json.dumps(message).encode('utf-8'))

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_ADDRESS, SERVER_PORT))
    server.listen(5)
    print(f"Server started on {SERVER_ADDRESS}:{SERVER_PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == '__main__':
    main()
