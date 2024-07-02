
# 🪝 RickPhis

The most professional tool ever created and developed for Instagram

---
##  Explanation

RickPhis differs from others in that it is designed to test the information entered by the user and give the user a real login experience. It was developed to alert you when you enter incorrect information and encourage you to enter correct information.


# ⁉️ HOW TO USE

#### The working principle of the tool is based on the hacker's arguments and these arguments are as follows:
- -s / --site 
- -ng / --ngrok-token
- -l / --lang
- -p / --port 
- -o / --output
- -c / --check
- --location / --loc
- --headless / --heoff

---
 #### -s/--site | --site 1 
 is a required argument and cannot be left blank. it must be prefixed with the number of the relevant site.

---
#### -ng/--ngrok-token | --ngrok-token 2abcd_345efgh
you have to make the adjustment by giving your own ngrok token
---
#### -l/--lang  | -l en
you can specify the language of the target page by giving a country code. if you do not use this argument, the default is English.

---
#### -p/--port |--port 8080
you can specify the connection point where the site will be published.

---
#### -o/--output  | -o login.txt
In response to this argument, it creates a file with the name and extension you provide and saves the victim's information there.

---
#### --loc/-location  | --location https://examplesite.com
When the user clicks on the sign in button they are redirected to instagram by default, but you can change this with this argument. 

---
#### -c/--check | --check
this command does not require any arguments. when given, it tests the victim's inputs with the original instagram, reflecting them as true or false to you and the victim

---
#### --heoff/--headless | --headless
this command does not require any arguments. when given, it runs the tool in headless mode.

---
-s 1 -l en -p 8080 -o test.txt --location https://www.instagram.com -c

---
## 🪧 USED
- **html**
- **css**
- **Python**
  - _colorama_ 
  - _selenium_ 
  - _webdriver-manager_
---


# Problem Management
the tool is coded according to the default kali-linux settings. for example it uses the firefox driver in the check section. if you are using something different you need to change the relevant section. (file:server.py line:96)

test the respective connection several times yourself. because sometimes it can fail due to web/instagram etc. If you get a 500 error code, stop and restart the server

this tool only works on linux. not configured for windows/mac or others (it can be made to work with minor modifications)

#### ☎️ I have tried my best to prevent possible errors and I have made tests for this. If you still get an error that you cannot handle, open a issue or write to me via [Telegram](https://t.me/HackerRick)

---
# 🔧 Installation


`git clone https://github.com/Rickidevs/RickPhis.git`

`cd RickPhis`

`./setup.sh` 

---
setup.sh file will do the necessary installations, if you create an alias you can easily call the tool from anywhere by typing `Rickphis`, but if you don't, the tool directory will be in /opt

`python3 /opt/RickPhis/server.py`  - to run without alias

---

# ⚖️ Disclaimer

This phishing tool has been developed strictly for educational purposes to demonstrate the potential vulnerabilities and techniques used in cybersecurity. The purpose of this tool is to aid in understanding and improving cybersecurity measures, and to help protect against phishing attacks.

#### Important Notices:

**Legal Use Only:** This tool is intended for use in controlled environments with proper authorization. Unauthorized use of this tool to access, retrieve, or manipulate information from any system without explicit permission from the system owner is illegal and unethical.

**Responsibility:** The creator of this tool assumes no responsibility for any damages or consequences that arise from the misuse of this tool. The user is solely responsible for ensuring that they use this tool in a lawful and ethical manner.
Educational Intent: This tool is provided "as is" without any warranties of any kind. It is intended solely for educational and research purposes, and not for any malicious intent.

**Compliance:** Users must comply with all applicable laws, regulations, and ethical guidelines while using this tool.

🚨 By using this tool, you agree to these terms and acknowledge that you understand the legal and ethical implications of phishing and cybersecurity practices.

---

## Feedback

If you have any feedback, please reach out to us at [Telegram](https://t.me/HackerRick)
