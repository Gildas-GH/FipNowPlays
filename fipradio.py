import requests
import time
import subprocess

URL = 'http://www.fipradio.fr/livemeta/7'

def retrieve():
    data = requests.get(URL).json()
    level = data['levels'][0]
    uid = level['items'][level['position']]
    step = data['steps'][uid]
    return step

def main():
    last_data = None
    while True:
        try:
            data = retrieve()
        except Exception:
            time.sleep(2)
            continue

        if data != last_data:
            msg = "{title} — {authors} ({anneeEditionMusique})".format(**data)
            msg2 = msg.title()
            print(msg2)
            subprocess.Popen(['toot', 'post', msg2])
        last_data = data
        time.sleep(10)

if __name__ == '__main__':
    import traceback
    try:
        main()
    except:
        with open('/tmp/fip-crash.log', 'w') as f:
            traceback.print_exc(file=f)
