
# 🪝 RickPhis

The most professional tool ever created and developed for Instagram

---
##  Explanation

RickPhis is a tool with the most up-to-date interface and the most realistic login experience. It is simple to use and almost identical to other cybersecurity tools. 

# ⁉️ HOW TO USE

- **set <args> <value>**  *you can change the argument values with this command*

---
- **show options**  *see your current settings*

---
- **exit**   *RickPhis - terminates*

---
- **help** *shows help menu*

---
- **clear** *cleans console*

---

#### The working principle of the tool is based on the hacker's arguments and these arguments are as follows:
- lang
- port 
- output
- check
- ngrok
- location
- headless

---
#### lang  | set lang az
you can specify the language of the target page by giving a country code. if you do not use this argument, the default is English.

---
#### port | set port 8080
you can specify the connection point where the site will be published.

---
#### output  | set output login.txt
It creates a file with the given name and extension and saves the victim's information there.

---
#### location  | set location https://examplesite.com
When the user clicks the login button they are redirected to instagram by default, but you can change that with this argument. NOTE: when linking, you need to start from http:// or https:// or you will not get the result you want 

---
#### check | set check true
it tests the user information entered by the victim in your interface in the background to see if it is correct or incorrect. if it is incorrect, it notifies the victim that he entered the information incorrectly and encourages him to enter it again. it is deactivated by default. it is recommended to use it, but the response to the victim is delayed by 5-10 seconds, so take this risk

---
#### headless | set headless true 
it is related to the check command. while the typed information is being tested, the scanner is opened on your device and the entries are filled in automatically, you have full control, but it is automatic. it is recommended to turn it off. this saves time in the response delay. 

---
#### ngrok | set ngrok 12abcd_34dfvc
phsihing site is running on local server, if you want to tunnel with ngrok we provide you this possibility, you just need to give ngrok token. it is completely up to you to do this

---

## 🪧 USED
- **html**
- **css**
- **Python**
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

`chmod +x setup.sh`

`./setup.sh` 

`python3 /opt/RickPhis/server.py`  - to run RickPhis

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
