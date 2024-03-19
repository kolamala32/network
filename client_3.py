import socket
import threading

def receive_messages(sock):
    while True:
        try:
            # Получаем данные от сервера
            data = sock.recv(1024)
            if not data:
                break
            print(f"{data.decode('utf-8')}")
        except Exception as e:
            print(f"Ошибка при получении сообщения: {e}")
            break

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаемся к серверу
client_socket.connect(('localhost', 12345))

# Получаем запрос на ввод имени
print("Введите ваше имя: ")
client_name = input()

# Отправляем имя серверу
client_socket.sendall(client_name.encode('utf-8'))

# Запускаем поток для приема сообщений
thread = threading.Thread(target=receive_messages, args=(client_socket,))
thread.start()

try:
    while True:
        # Отправляем сообщение серверу
        message = input()
        if message.lower() == 'exit':  # Команда для выхода
            break
        client_socket.sendall(message.encode('utf-8'))
except KeyboardInterrupt:
    print("Клиент отключается...")
finally:
    client_socket.close()