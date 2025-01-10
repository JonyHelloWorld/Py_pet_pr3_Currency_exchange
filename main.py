import json
import logging.config
import requests
import sqlite3

from http.server import HTTPServer, BaseHTTPRequestHandler #SimpleHTTPRequestHandler


from logging import getLogger

try:
    with open("Log/logging.conf", "r") as file:
        config = json.load(file)
        print("JSON загружен успешно.")

except json.JSONDecodeError as e:
    print("Ошибка в JSON-файле:", e)

logging.config.dictConfig(config)
logger = getLogger()#

class request_handler(BaseHTTPRequestHandler):


    def do_GET(self):
        if self.path == "/hello":
            response_body = b"<html><body><h1>Hello, World!</h1></body></html>"
            logging.debug(f"Получен GET-запрос: {self.path}")

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-Length", str(len(response_body)))
            self.end_headers() # конец заголовков, далее тело ответа
            self.wfile.write(response_body)
            logger.debug(f"Ответ: 200 OK для {self.path}")
            logger.debug(f"переход на /hello и ответ Hello, World!,  длина ответа {len(response_body)}")

        elif self.path == "/save":
            logging.debug(f"Получен GET-запрос: {self.path}")
            self.send_response(200)
            self.send_header("Content-Disposition", "attachment; filename=\"sample.txt\"")
            self.end_headers() # конец заголовков, далее тело ответа
            self.wfile.write(b"<html><body><h1>go to main.py</h1></body></html>")
            logger.debug(f"Ответ: 200 OK для {self.path}")
            logger.debug("сохраняю (скачиваю) файл sample.txt")

        elif self.path == "/main":
            logging.debug(f"Получен GET-запрос: {self.path}")
            self.send_response(200)
            self.send_header("Location", "http://localhost:8000/hello")
            self.end_headers() # конец заголовков, далее тело ответа
            self.wfile.write(b"<html><body><h1>go to main.py</h1></body></html>")
            logger.debug(f"Ответ: 200 OK для {self.path}")
            logger.debug("переход на main")

        else:
            logging.debug(f"Получен не правильный GET-запрос: {self.path}, ответ 404")
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")
            logger.debug(f"Ответ: 404 для {self.path}")
            logger.debug("переход на неизвестную страницу")


    def do_POST(self):
        if self.path == '/post':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            print(f"Получены данные: {post_data.decode('utf-8')}")
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "success"}')


# Подключаемся к базе данных
with sqlite3.connect("currency.db") as connection:
    # Создаем объект курсор
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL # "DEFAULT 18" - по умолчанию будет 18
        )
    """)
    # cursor.execute("""DROP TABLE user""") - удалили таблицу

    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Jony", 48))

    # connection.commit() - commit не нужен, если используем with

    # метод execute(SQL) - выполняет SQL запрос

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall() # считывает все строки
    # cursor.fetchmany(size) — считывает только указанное количество строк.
    # cursor.fetchone() — считывает одну строку за раз.
    #     row = cursor.fetchone()
    #     while row:
    #         print(row)
    #         row = cursor.fetchone()

    print(rows)

# Закрываем соединение
# connection.close() - когда используем with то соединение можно уже не закрывать

if __name__ == '__main__':
    server = HTTPServer(("127.0.0.1", 8000), request_handler)
    logger.debug(f"Сервер запущен на порту {8000}.")
    # request_handler.save_file('http://localhost:8000/sample.txt', 'sample.txt')
    server.serve_forever()

# шаблоны методов
# self.send_response(code, message=None)
# self.send_header(header, value)  - - self.send_response(404, "Page Not Found")
# self.wfile.write(data)
# data: байтовые данные, которые нужно отправить клиенту
# Строки (типа str) должны быть предварительно преобразованы в байты.

# html
# html_content = "<html><body><h1>Welcome to my server!</h1></body></html>"
# self.wfile.write(html_content.encode("utf-8"))
# json
# response_data = {"key": "value", "status": "ok"}
# self.wfile.write(json.dumps(response_data).encode("utf-8"))
# скачать файл
# with open("example.txt", "rb") as file:
#     self.wfile.write(file.read())

# можно вызвать несколько раз
# self.wfile.write(b"First part of the message.\n")
# self.wfile.write(b"Second part of the message.")


# заголовок для переадресации
# self.send_header("Location", "http://localhost:8000/hello")
# заголовок для скачивания файла
# self.send_header("Content-Disposition", "attachment; filename=\"sample.txt\"")

# примеры get и post запросов через терминал
# curl http://localhost:8000/hello
# curl -X POST http://localhost:8000/post -H "Content-Type: application/json" -d '{"name": "Johy", "age": 48}'


    # @staticmethod
    # def save_file(url, save_path):
    #     try:
    #         response = requests.get(url) # объект с ответом сервера на запрос
    #         logger.debug(f"Ответ: {response.status_code}")
    #         logger.debug(f"response: {response}")
    #         logger.debug(response.raise_for_status())
    #
    #         response.raise_for_status() # проверяет статусный код ответа
    #         # если 200 то продолжится выполнение, если 400 то перейдет к except
    #         with open(save_path, 'wb') as file: # Открывает файл для записи в бинарном режиме (wb)
    #             # по указанному пути save_path, with автоматически закрывает файл после завершения блока
    #             file.write(response.content)
    #             # Записывает содержимое ответа (response.content) в открытый файл.
    #             # response.content — это байтовые данные, полученные с сервера
    #             logger.debug(f"Файл успешно сохранён в: {save_path}")
    #     except requests.exceptions.RequestException as e:
    #         logger.debug(f"Ошибка при скачивании: {e}")


# logger.debug("запустил __init__")

    # save_file('http://localhost:8000/main.py', 'main2.py')



# python3 -m http.server 8000 - запуск локального сервера
# Теперь файл доступен по адресу http://localhost:8000
