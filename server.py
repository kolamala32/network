import socket
import threading

# Список подключенных клиентов
clients = []
# История чата
chat_history = []

# Функция для обработки подключения клиента
def client_thread(client_socket, addr):
    client_name = client_socket.recv(1024).decode('utf-8')
    welcome_message = f"{client_name} присоединился к чату!"
    broadcast_message(welcome_message)
    clients.append((client_socket, client_name))
    try:
        while True:
            # Получаем сообщение от клиента
            message = client_socket.recv(1024).decode('utf-8')
            if not message or message.lower() == 'exit':
                break
            full_message = f"{client_name}: {message}"
            # Сохраняем сообщение в истории чата
            chat_history.append(full_message)
            # Отправляем сообщение всем подключенным клиентам
            broadcast_message(full_message)
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        # Удаляем клиента из списка при отключении
        clients.remove((client_socket, client_name))
        client_socket.close()
        broadcast_message(f"{client_name} покинул чат.")

# Функция для отправки сообщений всем клиентам
def broadcast_message(message):
    for c, _ in clients:
        try:
            c.sendall(message.encode('utf-8'))
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")

# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к порту
server_socket.bind(('localhost', 12345))

# Слушаем входящие подключения
server_socket.listen()

print("Сервер запущен и ожидает подключения...")

try:
    while True:
        # Принимаем подключение
        client_socket, addr = server_socket.accept()
        # Создаем новый поток для обработки подключения
        thread = threading.Thread(target=client_thread, args=(client_socket, addr))
        thread.daemon = True  # Устанавливаем поток как демон
        thread.start()
except KeyboardInterrupt:
    print("Сервер останавливается...")
finally:
    # Закрываем все клиентские соединения
    for c, _ in clients:
        c.close()
    server_socket.close()